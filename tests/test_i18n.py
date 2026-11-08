from __future__ import annotations

import ast
import contextlib
import io
import json
import os
import string
import unicodedata
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from markdown_it import MarkdownIt
from rich.cells import cell_len, set_cell_size
from rich.console import Console
from rich.text import Text
from textual.binding import Binding
from textual.widgets import DataTable, Markdown, Static

import gputaskman
from gputaskman import locale_ja, report
from gputaskman.app import COLUMNS, EXPLAIN, HELP_MD, KIND_STYLE, MODEL_COLUMNS, GpuTaskManager, HelpScreen, help_markdown
from gputaskman.cli import main
from gputaskman.i18n import _, _windows_ui_language, current_language, detect_language, fit, set_language
from gputaskman.nvml import NvDevice
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


PACKAGE = Path(gputaskman.__file__).parent
UNSAFE_FOR_CP932_PIPES = "〜—−"


def package_trees():
    for path in sorted(PACKAGE.glob("*.py")):
        if path.name != "locale_ja.py":
            yield path, ast.parse(path.read_text(encoding="utf-8"))


def translated_arguments():
    for path, tree in package_trees():
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "_":
                yield path.name, node.lineno, node.args[0]


def literal_msgids():
    return {arg.value for _file, _line, arg in translated_arguments()
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str)}


def source_strings():
    return {node.value for _path, tree in package_trees() for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)}


def render_time_msgids():
    """Strings the code translates through a variable, so the scan for _("...") cannot see them."""
    ids = set(HELP_MD.strip().split("\n\n")) | set(EXPLAIN.values()) | set(KIND_STYLE)
    ids |= set(GpuTaskManager.CHARTS) | {name for name, _key in GpuTaskManager.SORTS}
    ids |= set(COLUMNS) | {column for column in MODEL_COLUMNS if column}
    for screen in (GpuTaskManager, HelpScreen):
        ids |= {binding.description for binding in Binding.make_bindings(screen.BINDINGS)}
    ids |= {report.METAL_NOTE, report.WSL_EMPTY, report.DRM_RESIDENT_NOTE}
    ids.add("palette")  # Textual's own Footer label for ctrl+p, translated by the same active_bindings override
    return ids


def placeholders(text):
    return sorted((name, spec) for _literal, name, spec, _conversion in string.Formatter().parse(text) if name is not None)


def ambiguous_width(text):
    return {char for char in text if unicodedata.east_asian_width(char) == "A"}


class CatalogTests(unittest.TestCase):
    def test_every_msgid_the_code_translates_has_an_entry(self):
        missing = sorted((literal_msgids() | render_time_msgids()) - set(locale_ja.MESSAGES))
        self.assertEqual(missing, [], "missing from locale_ja.MESSAGES")

    def test_no_catalog_key_is_stale(self):
        known = literal_msgids() | render_time_msgids() | source_strings()
        self.assertEqual(sorted(key for key in locale_ja.MESSAGES if key not in known), [],
                         "in locale_ja.MESSAGES but nowhere in the source")

    def test_translated_calls_pass_a_message_id_and_never_a_built_string(self):
        built = [f"{file}:{line}" for file, line, arg in translated_arguments() if isinstance(arg, (ast.JoinedStr, ast.BinOp))]
        self.assertEqual(built, [], "_() needs the English template; format its result instead")

    def test_catalog_source_has_no_duplicate_keys(self):
        tree = ast.parse(Path(locale_ja.__file__).read_text(encoding="utf-8"))
        keys = [key.value for node in ast.walk(tree) if isinstance(node, ast.Dict) for key in node.keys
                if isinstance(key, ast.Constant) and isinstance(key.value, str)]
        self.assertEqual(sorted({key for key in keys if keys.count(key) > 1}), [])

    def test_placeholders_match_between_key_and_value(self):
        for key, value in locale_ja.MESSAGES.items():
            with self.subTest(key=key[:60]):
                self.assertEqual(placeholders(value), placeholders(key))

    def test_values_encode_in_cp932_and_avoid_characters_cp932_pipes_mangle(self):
        for key, value in locale_ja.MESSAGES.items():
            with self.subTest(key=key[:60]):
                value.encode("cp932")
                self.assertEqual(sorted(set(value) & set(UNSAFE_FOR_CP932_PIPES)), [])

    def test_values_add_no_ambiguous_width_character_the_key_lacks(self):
        for key, value in locale_ja.MESSAGES.items():
            with self.subTest(key=key[:60]):
                self.assertEqual(sorted(ambiguous_width(value) - ambiguous_width(key)), [])


class HelpTests(unittest.TestCase):
    def setUp(self):
        self.addCleanup(set_language, "en")

    def test_english_help_is_the_source_text(self):
        self.assertEqual(help_markdown(), HELP_MD)

    def test_every_help_paragraph_is_translated_and_keeps_its_markup(self):
        set_language("ja")
        for paragraph in HELP_MD.strip().split("\n\n"):
            translated = _(paragraph)
            with self.subTest(paragraph=paragraph[:40]):
                self.assertNotEqual(translated, paragraph)
                for token in MarkdownIt("gfm-like").parse(translated):
                    for child in token.children or []:
                        if child.type == "text":
                            self.assertNotIn("*", child.content, "emphasis did not close, so the asterisks show")
                            self.assertNotIn("`", child.content)


class UiTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        backend = patch("gputaskman.app.BACKEND", "wddm")
        backend.start()
        self.addCleanup(backend.stop)
        self.addCleanup(set_language, "en")

    def screen_text(self, app):
        return " ".join(ET.fromstring(app.export_screenshot()).itertext()).replace(" ", " ")

    def chart_text(self, app):
        widget = app.query_one("#charts", Static)
        output = io.StringIO()
        Console(file=output, width=widget.content_size.width, color_system=None).print(widget.content)
        return output.getvalue()

    def inspector_text(self, app):
        return "\n".join(line.plain for line in app.query_one("#inspector", Static).content.renderables
                         if isinstance(line, Text))

    async def test_footer_and_help_screen_bindings_follow_the_language(self):
        expected = {
            "en": (["Quit", "Sort", "Chart", "All/Top", "Pause", "Explain", "palette"], "Close"),
            "ja": (["終了", "並べ替え", "グラフ", "全部/上位", "一時停止", "説明", "コマンドパレット"], "閉じる"),
        }
        for language, (footer, close) in expected.items():
            with self.subTest(language=language):
                set_language(language)
                with patch.object(GpuTaskManager, "poll"):
                    app = GpuTaskManager()
                    async with app.run_test(size=(160, 48)) as pilot:
                        app.apply(snapshot())
                        await pilot.pause()
                        self.assertEqual([key.description for key in app.query("FooterKey")], footer)
                        await pilot.press("question_mark")
                        await pilot.pause()
                        self.assertIsInstance(app.screen, HelpScreen)
                        self.assertEqual(app.screen.active_bindings["escape"].binding.description, close)
                        app.action_show_help_panel()
                        await pilot.pause()
                        self.assertIn(close, self.screen_text(app))

    async def test_japanese_table_headers_kinds_and_sort_names(self):
        set_language("ja")
        with patch.object(GpuTaskManager, "poll"):
            app = GpuTaskManager()
            async with app.run_test(size=(160, 48)) as pilot:
                app.apply(snapshot())
                await pilot.pause()
                table = app.query_one("#procs", DataTable)
                self.assertEqual([column.label.plain for column in table.columns.values()],
                                 ["PID", "プロセス", "種類", "ランタイム", "VRAM", "共有RAM", "非常駐", "GPU%", "3D", "Copy",
                                  "Video", "中身"])
                self.assertEqual(table.get_cell("10", "Kind").plain, "LLM")
                self.assertEqual(table.get_cell("20", "Kind").plain, "コンポジター")
                self.assertEqual(table.border_subtitle, "並べ替え: VRAM  ・  上位のプロセス")
                subtitles = []
                for _step in app.SORTS:
                    await pilot.press("s")
                    subtitles.append(table.border_subtitle)
                self.assertEqual(subtitles, [f"並べ替え: {name}  ・  上位のプロセス"
                                             for name in ("GPU%", "共有RAM", "非常駐", "名前", "VRAM")])
                await pilot.press("a")
                self.assertEqual(table.border_subtitle, "並べ替え: VRAM  ・  すべてのプロセス")

    async def test_english_table_is_unchanged(self):
        set_language("en")
        with patch.object(GpuTaskManager, "poll"):
            app = GpuTaskManager()
            async with app.run_test(size=(160, 48)) as pilot:
                app.apply(snapshot())
                await pilot.pause()
                table = app.query_one("#procs", DataTable)
                self.assertEqual([column.label.plain for column in table.columns.values()],
                                 ["PID", "Process", "Kind", "Runtime", "VRAM", "Spill", "Paged", "GPU%", "3D", "Copy",
                                  "Video", "What's inside"])
                self.assertEqual(table.get_cell("20", "Kind").plain, "compositor")
                self.assertEqual(table.border_subtitle, "sort: VRAM  ·  top processes")

    async def test_japanese_dashboard_charts_and_pause_marker(self):
        set_language("ja")
        with patch.object(GpuTaskManager, "poll"):
            app = GpuTaskManager()
            async with app.run_test(size=(180, 50)) as pilot:
                s = snapshot()
                s.nv = NvDevice(index=0, util_gpu=50, util_mem=10, temp=49, power_w=72, power_limit_w=150,
                                sm_clock=1500, sm_clock_max=3003, throttle=["sw-power-cap"])
                app.apply(s)
                await pilot.pause()
                charts = self.chart_text(app)
                for name in ("GPU", "SMクロック", "VRAM", "メモリ稼働", "温度", "電力", "エンコーダー", "デコーダー"):
                    self.assertIn(name, charts)
                for line in charts.splitlines():
                    self.assertRegex(set_cell_size(line, 21)[-8:], r"^ *(\d+(%| MHz| W|°C)|N/A)$")
                note = str(app.query_one("#chart-note", Static).content)
                self.assertEqual(note, "直近のサンプル ・ 空白 = 読み取りなし ・ 電力 0-150 W ・ SMクロック 0-3003 MHz")
                text = self.screen_text(app)
                for label in ("グラフ", "すべてのグラフ", "クリックで選択 ・ cキーで切り替え"):
                    self.assertIn(label, text)
                device = "\n".join(line.plain for line in app.render_device(s).renderables)
                for label in ("メモリ稼働 10%", "スロットリング: sw-power-cap", "空き 6.00 GB"):
                    self.assertIn(label, device)
                self.assertNotIn("一時停止中", device)
                await pilot.press("p")
                device = "\n".join(line.plain for line in app.render_device(s).renderables)
                self.assertIn("[一時停止中]", device)

    async def test_japanese_inspector_labels_and_kind_explanation(self):
        set_language("ja")
        with patch.object(GpuTaskManager, "poll"):
            app = GpuTaskManager()
            async with app.run_test(size=(180, 50)) as pilot:
                app.apply(snapshot())
                await pilot.pause()
                header = app.query_one("#inspector", Static).content.renderables[0].plain
                self.assertEqual(header, "VRAM 8.00 GB   共有RAM 1.00 GB   非常駐(推定) 0 MB   エンジン アイドル")
                self.assertIn("サーバー llama-server http://127.0.0.1:8080", self.inspector_text(app))
                await pilot.press("down")
                await pilot.pause()
                inspector = app.query_one("#inspector", Static)
                self.assertEqual(inspector.border_title, "dwm.exe (20) - コンポジター")
                self.assertIn("デスクトップウィンドウマネージャー: 自身のバックバッファーと", self.inspector_text(app))
                self.assertEqual(self.inspector_text(app).splitlines()[0],
                                 "VRAM 2.00 GB   共有RAM 0 MB   非常駐(推定) 1.00 GB   エンジン アイドル")

    async def test_japanese_help_screen_renders_the_translated_markdown(self):
        set_language("ja")
        with patch.object(GpuTaskManager, "poll"):
            app = GpuTaskManager()
            async with app.run_test(size=(160, 48)) as pilot:
                app.apply(snapshot())
                await pilot.press("question_mark")
                await pilot.pause()
                self.assertEqual(app.screen.query_one(Markdown).source, help_markdown())
                text = self.screen_text(app)
                self.assertIn("GPUメモリについて何がわかるのか?", text)
                self.assertIn("階層", text)
                self.assertNotIn("What can be known", text)


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
