from __future__ import annotations

import contextlib
import io
import json
import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from rich.cells import cell_len

from gputaskman import locale_ja
from gputaskman.cli import main
from gputaskman.i18n import _, _windows_ui_language, current_language, detect_language, fit, set_language
from test_core import snapshot

# The suite asserts English output through cli.main(); keep it independent of the machine's display language.
os.environ["GPUTASKMAN_LANG"] = "en"


class DetectLanguageTests(unittest.TestCase):
    def detect(self, environ, ui_language=None):
        with patch("gputaskman.i18n._windows_ui_language", return_value=ui_language):
            return detect_language(environ)

    def test_override_wins_over_the_locale_and_windows(self):
        self.assertEqual(self.detect({"GPUTASKMAN_LANG": "ja", "LANG": "en_US.UTF-8"}, 0x0409), "ja")
        self.assertEqual(self.detect({"GPUTASKMAN_LANG": "en", "LC_ALL": "ja_JP.UTF-8"}, 0x0411), "en")
        self.assertEqual(self.detect({"GPUTASKMAN_LANG": " JA "}), "ja")

    def test_auto_and_unknown_overrides_fall_through_to_the_locale(self):
        for value in ("auto", "", "fr"):
            with self.subTest(value=value):
                self.assertEqual(self.detect({"GPUTASKMAN_LANG": value, "LANG": "ja_JP.UTF-8"}), "ja")
                self.assertEqual(self.detect({"GPUTASKMAN_LANG": value, "LANG": "en_US.UTF-8"}, 0x0411), "en")

    def test_first_non_empty_locale_variable_decides(self):
        cases = [
            ({"LC_ALL": "ja_JP.UTF-8", "LC_MESSAGES": "en_US.UTF-8", "LANG": "en_US.UTF-8"}, "ja"),
            ({"LC_ALL": "", "LC_MESSAGES": "en_US.UTF-8", "LANG": "ja_JP.UTF-8"}, "en"),
            ({"LC_ALL": "", "LC_MESSAGES": "  ", "LANG": "ja_JP.eucJP"}, "ja"),
            ({"LANG": "C.UTF-8"}, "en"),
            ({"LC_ALL": "C", "LANG": "ja_JP.UTF-8"}, "en"),
            ({"LANG": "fr_FR.UTF-8"}, "en"),
        ]
        for environ, expected in cases:
            with self.subTest(environ=environ):
                self.assertEqual(self.detect(environ), expected)

    def test_a_locale_variable_beats_the_windows_display_language(self):
        self.assertEqual(self.detect({"LANG": "en_US.UTF-8"}, 0x0411), "en")
        self.assertEqual(self.detect({"LANG": "ja_JP.UTF-8"}, 0x0409), "ja")

    def test_windows_display_language_is_the_last_resort(self):
        self.assertEqual(self.detect({}, 0x0411), "ja")
        self.assertEqual(self.detect({}, 0x0811), "ja")  # only the primary language id counts
        self.assertEqual(self.detect({}, 0x0409), "en")
        self.assertEqual(self.detect({}, None), "en")

    def test_windows_call_reads_the_display_language_only_on_windows(self):
        windows = SimpleNamespace(windll=SimpleNamespace(kernel32=SimpleNamespace(GetUserDefaultUILanguage=lambda: 0x0411)))
        with patch("gputaskman.i18n.sys.platform", "win32"), patch("gputaskman.i18n.ctypes", windows):
            self.assertEqual(_windows_ui_language(), 0x0411)
        with patch("gputaskman.i18n.sys.platform", "linux"), patch("gputaskman.i18n.ctypes", windows):
            self.assertIsNone(_windows_ui_language())
        with patch("gputaskman.i18n.sys.platform", "win32"), patch("gputaskman.i18n.ctypes", SimpleNamespace()):
            self.assertIsNone(_windows_ui_language())


class SetLanguageTests(unittest.TestCase):
    def setUp(self):
        self.addCleanup(set_language, "en")

    def test_the_library_defaults_to_english_and_passes_unknown_ids_through(self):
        self.assertEqual(current_language(), "en")
        self.assertEqual(_("anything at all"), "anything at all")
        self.assertEqual(_(""), "")

    def test_japanese_uses_the_catalog_and_falls_back_to_english_for_a_missing_key(self):
        with patch.dict(locale_ja.MESSAGES, {"hello": "こんにちは"}):
            set_language("ja")
            self.assertEqual(current_language(), "ja")
            self.assertEqual(_("hello"), "こんにちは")
            self.assertEqual(_("not in the catalog"), "not in the catalog")
            set_language("en")
            self.assertEqual(_("hello"), "hello")

    def test_auto_runs_the_detection(self):
        with patch("gputaskman.i18n.detect_language", return_value="ja"):
            set_language("auto")
        self.assertEqual(current_language(), "ja")

    def test_an_unknown_language_is_rejected_and_changes_nothing(self):
        set_language("ja")
        with self.assertRaises(ValueError):
            set_language("fr")
        self.assertEqual(current_language(), "ja")


class FitTests(unittest.TestCase):
    def test_every_result_is_exactly_the_requested_number_of_cells(self):
        for text in ("", "abc", "abcdefgh", "プロセス", "日本語a", "GPU%", "ランタイム"):
            for width in range(0, 14):
                for align in ("<", ">"):
                    with self.subTest(text=text, width=width, align=align):
                        self.assertEqual(cell_len(fit(text, width, align)), width)

    def test_a_wide_character_is_never_split(self):
        self.assertEqual(fit("日本語", 5), "日本 ")
        self.assertEqual(fit("コンポジター", 10), "コンポジタ")

    def test_ascii_matches_str_format(self):
        for text in ("abc", "abcdefgh", ""):
            self.assertEqual(fit(text, 5), f"{text[:5]:<5}")
            self.assertEqual(fit(text, 5, ">"), f"{text:>5}"[:5])

    def test_right_alignment_pads_on_the_left_in_cells(self):
        self.assertEqual(fit("VRAM", 9, ">"), "     VRAM")
        self.assertEqual(fit("共有RAM", 9, ">"), "  共有RAM")

    def test_an_unknown_alignment_is_rejected(self):
        with self.assertRaises(ValueError):
            fit("x", 3, "^")


class CliLanguageTests(unittest.TestCase):
    def setUp(self):
        self.addCleanup(set_language, "en")

    def run_cli(self, *args, env=None):
        out = io.StringIO()
        with patch("sys.argv", ["gputaskman", *args]), patch("gputaskman.cli.time.sleep"), \
                patch.dict(os.environ, env or {}), patch("gputaskman.collector.Collector") as collector, \
                contextlib.redirect_stdout(out):
            collector.return_value.sample.return_value = snapshot()
            main()
        return out.getvalue()

    def test_main_leaves_the_language_as_it_found_it(self):
        set_language("en")
        self.run_cli("--once", "--lang", "ja")
        self.assertEqual(current_language(), "en")
        with patch("sys.argv", ["gputaskman", "--lang", "ja", "--gpu", "-1"]), \
                contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            main()
        self.assertEqual(current_language(), "en")

    def test_json_is_english_whatever_the_language_setting(self):
        for args, env in ((["--json", "--lang", "ja"], {}), (["--json"], {"GPUTASKMAN_LANG": "ja"})):
            with self.subTest(args=args, env=env):
                set_language("ja")
                with patch("gputaskman.cli.set_language", wraps=set_language) as chosen:
                    data = json.loads(self.run_cli(*args, env=env))
                self.assertEqual(chosen.call_args_list[0].args, ("en",))
                inside = {p["name"]: p["inside"] for p in data["processes"]}
                self.assertEqual(inside["dwm.exe"], "desktop back buffers + composed frames")

    def test_lang_option_is_documented_and_validated(self):
        out = io.StringIO()
        with patch("sys.argv", ["gputaskman", "--help"]), contextlib.redirect_stdout(out), \
                self.assertRaises(SystemExit):
            main()
        self.assertIn("--lang {auto,en,ja}", out.getvalue())
        self.assertIn("GPUTASKMAN_LANG", out.getvalue())
        with patch("sys.argv", ["gputaskman", "--lang", "fr"]), contextlib.redirect_stderr(io.StringIO()), \
                self.assertRaises(SystemExit) as error:
            main()
        self.assertEqual(error.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
