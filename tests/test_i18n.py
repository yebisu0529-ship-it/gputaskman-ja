from __future__ import annotations

import ast
import contextlib
import io
import json
import os
import string
import tempfile
import unicodedata
import unittest
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from markdown_it import MarkdownIt
from rich.cells import cell_len, set_cell_size
from rich.console import Console
from rich.text import Text
from textual.binding import Binding
from textual.widgets import DataTable, Markdown, Static

import gputaskman
from gputaskman import diff as diff_module
from gputaskman import locale_ja, report
from gputaskman.app import COLUMNS, EXPLAIN, HELP_MD, KIND_STYLE, MODEL_COLUMNS, GpuTaskManager, HelpScreen, help_markdown
from gputaskman.cli import main
from gputaskman.collector import Collector, ProcRow
from gputaskman.dxgi import Adapter
from gputaskman.handy import HandyEvidence, inspect_handy
from gputaskman.i18n import _, _windows_ui_language, current_language, detect_language, fit, set_language
from gputaskman.llm import LlmView, ServerInfo, build_view
from gputaskman.nvml import NvDevice
from gputaskman.pdh import AdapterGpu, ProcGpu
from gputaskman.procinfo import ProcDetail, make_model
from gputaskman.report import to_text
from test_core import gguf, snapshot
from test_diff import llm as llm_view
from test_diff import proc as diff_proc
from test_diff import snap as diff_snap

GiB = 1 << 30
MiB = 1 << 20


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
    ids |= {report.METAL_NOTE, report.WSL_EMPTY, report.DRM_RESIDENT_NOTE, report.WSL_NOTE, report.WSL_HOST_NOTE,
            report.INFERRED_NOTE, report.ORDER_NOTE} | set(report.DRM_NOTES.values())
    ids |= {label for _key, label in diff_module.DEVICE} | set(diff_module.SEGMENT_ORDER)
    ids |= {"runtime-reported", "estimated"}  # diff's per-segment source, translated where its text is built
    ids |= static_host_statuses() | gguf_kinds()
    ids.add("palette")  # Textual's own Footer label for ctrl+p, translated by the same active_bindings override
    return ids


def string_literals(expression):
    if isinstance(expression, ast.Constant) and isinstance(expression.value, str):
        return [expression.value]
    if isinstance(expression, ast.IfExp):
        return string_literals(expression.body) + string_literals(expression.orelse)
    return []


def gguf_kinds():
    """What GgufInfo.kind can return. The code compares these, so they are translated where they are shown."""
    tree = ast.parse((PACKAGE / "gguf.py").read_text(encoding="utf-8"))
    kind = next(node for cls in tree.body if isinstance(cls, ast.ClassDef) and cls.name == "GgufInfo"
                for node in cls.body if isinstance(node, ast.FunctionDef) and node.name == "kind")
    return {value for node in ast.walk(kind) if isinstance(node, ast.Return) for value in string_literals(node.value)}


def static_host_statuses():
    """Literals assigned to a .status or .host_status attribute; the f-string ones are dynamic and stay English."""
    found = set()
    for _path, tree in package_trees():
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and any(
                    isinstance(target, ast.Attribute) and target.attr in ("status", "host_status")
                    for target in node.targets):
                found |= {value for value in string_literals(node.value) if value}
    return found


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
            "ja": (["終了", "並べ替え", "グラフ", "すべて/上位", "一時停止", "説明", "コマンドパレット"], "閉じる"),
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
                for name in ("GPU", "SMクロック", "VRAM", "メモリ稼働率", "温度", "電力", "エンコーダー", "デコーダー"):
                    self.assertIn(name, charts)
                for line in charts.splitlines():
                    self.assertRegex(set_cell_size(line, 21)[-8:], r"^ *(\d+(%| MHz| W|°C)|N/A)$")
                note = str(app.query_one("#chart-note", Static).content)
                self.assertEqual(note, "直近のサンプル ・ 空白 = 読み取りなし ・ 電力 0-150 W ・ SMクロック 0-3003 MHz")
                text = self.screen_text(app)
                for label in ("グラフ", "すべてのグラフ", "クリックで選択 ・ cキーで切り替え"):
                    self.assertIn(label, text)
                device = "\n".join(line.plain for line in app.render_device(s).renderables)
                for label in ("メモリ稼働率 10%", "スロットリング: sw-power-cap", "空き 6.00 GB"):
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
                self.assertIn("GPUメモリについて何がわかるのか？", text)
                self.assertIn("階層", text)
                self.assertNotIn("What can be known", text)


class ReportTextTests(unittest.TestCase):
    def setUp(self):
        self.addCleanup(set_language, "en")

    def fixture(self):
        s = snapshot()
        s.driver, s.cuda = "560.94", "12.6"
        s.nv = NvDevice(index=0, util_gpu=50, util_mem=10, temp=49, power_w=72, power_limit_w=150, sm_clock=1500,
                        video_clock=900, driver_model="WDDM")
        s.procs.append(ProcRow(30, "ゲーム用のとても長い名前のアプリケーション.exe", "3D/game", ProcGpu(dedicated=512 * MiB),
                               ProcDetail(30, "game")))
        return s

    def table(self, text):
        lines = text.splitlines()
        header = next(index for index, line in enumerate(lines) if "VRAM" in line and "GPU%" in line)
        return lines[header], lines[header + 1:lines.index("", header)]

    def test_english_header_is_byte_for_byte_the_original(self):
        header, _rows = self.table(to_text(self.fixture()))
        self.assertEqual(header, f"{'PID':>7}  {'PROCESS':<24} {'KIND':<10} {'RUNTIME':<24} {'VRAM':>9} {'SPILL':>8} "
                                 f"{'PAGED':>8} {'GPU%':>5}  INSIDE")

    def test_japanese_header_and_device_lines(self):
        set_language("ja")
        text = to_text(self.fixture())
        header, rows = self.table(text)
        self.assertEqual(header.split(), ["PID", "プロセス", "種類", "ランタイム", "VRAM", "共有RAM", "非常駐", "GPU%", "中身"])
        self.assertIn("コンポジター", "\n".join(rows))
        first, memory = text.splitlines()[:2]
        self.assertEqual(first, "GPU  ドライバー 560.94  CUDA 12.6  WDDM")
        self.assertEqual(memory, "VRAM 10.00 GB / 16.00 GB   共有RAM 1.00 GB")
        self.assertIn("メモリ稼働率 10%", text)
        self.assertNotIn("mem-bandwidth", text)

    def test_every_row_keeps_the_vram_column_at_the_headers_cell_offset(self):
        for language in ("en", "ja"):
            with self.subTest(language=language):
                set_language(language)
                header, rows = self.table(to_text(self.fixture()))
                end = cell_len(header[:header.index("VRAM") + len("VRAM")])
                self.assertEqual(len(rows), 3)
                for row, vram in zip(rows, ("8.00 GB", "2.00 GB", "512 MB")):
                    self.assertEqual(set_cell_size(row, end)[-9:], f"{vram:>9}", row)
                self.assertIn("ゲーム用のとても長い名前", rows[2])
                self.assertNotIn("ゲーム用のとても長い名前の", rows[2])

    def test_provenance_notes_are_translated_with_their_markers(self):
        set_language("ja")
        marked = ProcGpu(attributed=False, inferred=GiB, inferred_by="consistent")
        guessed = ProcGpu(attributed=False, inferred=GiB, inferred_by="order")
        self.assertTrue(report.inferred_note(marked).startswith("* 対応付け済み: サイズは正確です"))
        self.assertTrue(report.inferred_note(guessed).startswith("? 順序による推測: "))
        for reason, note in report.DRM_NOTES.items():
            translated = report.drm_note(ProcGpu(drm_reason=reason))
            self.assertNotEqual(translated, note, reason)
            self.assertIn("n/a", translated)
        self.assertEqual(report.drm_note(ProcGpu()), "")

    def test_wsl_note_translates_static_host_statuses_and_leaves_dynamic_ones_english(self):
        s = snapshot()
        s.backend = "wsl"
        for status, japanese in (("off (--no-host)", "オフ (--no-host)"), ("starting", "開始中"),
                                 ("unavailable (OSError: boom)", "unavailable (OSError: boom)")):
            s.host_status = status
            with self.subTest(status=status):
                set_language("ja")
                self.assertTrue(report.wsl_note(s).startswith("WSL: VRAMとエンジン負荷は"))
                self.assertTrue(report.wsl_note(s).endswith(f"Windowsホストのカウンター: {japanese}。"))
                set_language("en")
                self.assertEqual(report.wsl_note(s), f"{report.WSL_NOTE} Windows host counters: {status}.")
        set_language("ja")
        s.host_status = "ok (last Windows sample 5s old)"
        self.assertTrue(report.wsl_note(s).startswith("WSL + Windowsホストのカウンター"))
        s.host_status = ""
        self.assertTrue(report.wsl_note(s).endswith("各プロセスの取り分ではありません。"))


class DiffTextTests(unittest.TestCase):
    def setUp(self):
        self.addCleanup(set_language, "en")
        self.before = diff_snap([diff_proc(1, "dwm.exe", vram=2 * GiB),
                                 diff_proc(2, "llama-server", vram=5 * GiB, ports=[8080], llm=llm_view(4096, GiB // 2))],
                                used=8 * GiB, attributed=7 * GiB)
        self.after = diff_snap([diff_proc(1, "dwm.exe", vram=2 * GiB),
                                diff_proc(22, "llama-server", vram=9 * GiB, ports=[8080], llm=llm_view(32768, 4 * GiB),
                                          files=[r"D:\models\q.gguf"]),
                                diff_proc(3, "python.exe", vram=GiB)],
                               used=13 * GiB, attributed=12 * GiB, taken=142.5)

    def text(self, language):
        set_language(language)
        return diff_module.to_text(diff_module.diff(self.before, self.after))

    def test_english_text_is_unchanged(self):
        lines = self.text("en").splitlines()
        self.assertIn(f"{'DEVICE (measured)':<26}{'BEFORE':>11}{'AFTER':>11}{'CHANGE':>11}", lines)
        self.assertIn(f"{'PROCESSES (dedicated)':<22}{'PID':>14}  {'MATCH':<11}{'BEFORE':>11}{'AFTER':>11}{'CHANGE':>11}"
                      f"{'SHARED +/-':>11}", lines)
        self.assertIn(f"  {'kv':<8} {'512 MB':>9} -> {'4.00 GB':>9}  {'+3.50 GB':>9}  estimated", lines)

    def test_japanese_text_names_provenance_in_japanese_only(self):
        text = self.text("ja")
        for expected in ("gputaskman diff: RTX (wddm)、42.5秒間隔", "デバイス（実測）", "変更前", "変更後", "増減", "専用GPUメモリ使用量",
                         "未帰属", "プロセス（専用）", "照合", "共有増減", "一覧になし", "  コンテキスト長  4096 -> 32768",
                         "  KVキャッシュ    512 MB ->   4.00 GB   +3.50 GB  推定", "  モデルファイルを新たに検出: ",
                         "llama-server (2->22)", "「一覧になし」は、そのスナップショットに"):
            self.assertIn(expected, text)
        for english in ("DEVICE", "BEFORE", "AFTER", "CHANGE", "Measured counters", "not listed", "estimated",
                        "runtime-reported", "model file", "context length", "process(es)"):
            self.assertNotIn(english, text)

    def test_runtime_reported_segments_say_so(self):
        self.before["processes"][1]["llm"] = llm_view(4096, GiB // 2, exact=True)
        self.after["processes"][1]["llm"] = llm_view(32768, 4 * GiB, exact=True)
        self.assertIn("ランタイム報告", self.text("ja"))
        self.assertIn("runtime-reported", self.text("en"))

    def test_every_row_is_as_many_cells_wide_as_its_table_header(self):
        for language, device_header, process_header in (("en", "DEVICE (measured)", "PROCESSES (dedicated)"),
                                                        ("ja", "デバイス（実測）", "プロセス（専用）")):
            with self.subTest(language=language):
                lines = self.text(language).splitlines()
                device = next(index for index, line in enumerate(lines) if line.startswith(device_header))
                process = next(index for index, line in enumerate(lines) if line.startswith(process_header))
                for table in (lines[device:device + 5], lines[process:process + 3]):
                    self.assertEqual({cell_len(line) for line in table}, {cell_len(table[0])}, table)


class DataStringTests(unittest.TestCase):
    def setUp(self):
        self.addCleanup(set_language, "en")

    def llm_view(self, **extra):
        meta = {"block_count": 32, "context_length": 4096, "attention.head_count": 32, "attention.head_count_kv": 8,
                "embedding_length": 4096, "general.name": "Snapshot_Cfg", **extra}
        info = gguf("qwen35", **meta)
        info.layer_bytes = {index: 10 * MiB for index in range(32)}
        with patch("gputaskman.procinfo.read_gguf", return_value=info):
            model = make_model("snapshot.gguf", 1000, 0, True, "mapped", "")
        detail = ProcDetail(10, "llama-server.exe", models=[model])
        server = ServerInfo("llama-server", "http://127.0.0.1:1", n_ctx=4096, model_path=model.path)
        return detail, server, info

    def test_segments_and_notes_follow_the_language_and_keep_their_markers(self):
        for language, labels, notes in (
            ("en", ["weights", "KV cache (4,096 ctx, f16) est. max", "compute buffers + runtime"],
             ["Sliding-window attention (1024 tokens): most layers keep a short KV window, so the real KV cache is "
              "smaller than this estimate.", "KV cost 128 KB/token (f16): 4k ctx = 512 MB, 32k ctx = 4.00 GB.",
              "! 512 MB is in SHARED GPU memory (system RAM over PCIe). May include pinned host buffers; under VRAM "
              "pressure, fallback can slow inference."]),
            ("ja", ["重み", "KVキャッシュ (4,096 ctx, f16) 推定（上限）", "計算バッファー + ランタイム"],
             ["スライディングウィンドウアテンション（1024トークン）: 多くのレイヤーはKVを短いウィンドウ分しか保持しないため、"
              "実際のKVキャッシュはこの推定より小さくなります。",
              "KVコスト 128 KB/token (f16): 4k ctx = 512 MB、32k ctx = 4.00 GB。",
              "! 512 MBが共有RAM（PCIe経由でGPUからアクセスするシステムRAM）にあります。ピン留めされたホストバッファーを含む場合があります。"
              "VRAMが逼迫すると、フォールバックによって推論が遅くなることがあります。"])):
            with self.subTest(language=language):
                set_language(language)
                detail, server, info = self.llm_view(**{"attention.sliding_window": 1024})
                with patch("gputaskman.llm.read_gguf", return_value=info):
                    view = build_view(detail, 2 * GiB, 512 * MiB, server)
                self.assertEqual([segment.label for segment in view.segments], labels)
                self.assertEqual([segment.kind for segment in view.segments], ["weights", "kv", "runtime"])
                self.assertEqual(view.notes, notes)
                self.assertTrue(view.notes[-1].startswith("!"))

    def test_buffer_log_segments_name_their_devices(self):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "server.log"
            log.write_text("llama_context: CPU_Mapped model buffer size = 30 MiB\n"
                           "llama_context: CUDA0 model buffer size = 100 MiB\n"
                           "llama_context: CUDA0 KV buffer size = 30 MiB\n"
                           "llama_context: CUDA0 compute buffer size = 5 MiB\n", encoding="utf-8")
            for language, labels, note in (
                ("en", ["weights (CUDA0)", "KV cache (CUDA0)", "compute buffers (CUDA0)", "runtime and other overhead"],
                 "30 MB of weights are on the CPU side (partial offload or CPU-mapped)."),
                ("ja", ["重み (CUDA0)", "KVキャッシュ (CUDA0)", "計算バッファー (CUDA0)", "ランタイムなどのオーバーヘッド"],
                 "重みのうち30 MBはCPU側にあります（部分オフロード、またはCPUにマップ済み）。"),
            ):
                with self.subTest(language=language):
                    set_language(language)
                    detail, _server, info = self.llm_view()
                    with patch("gputaskman.llm.read_gguf", return_value=info):
                        view = build_view(detail, GiB, 0, None, str(log))
                    self.assertEqual([segment.label for segment in view.segments], labels)
                    self.assertIn(note, view.notes)

    def test_evidence_and_kind_labels_keep_the_provenance_ladder(self):
        decided = gguf("qwen35", block_count=2, context_length=4096)
        with patch("gputaskman.procinfo.read_gguf", return_value=decided):
            hinted = make_model("OpenJev.gguf", 1000, 0, True, "mapped", "")
        installed = make_model("OpenJev.safetensors", 1000, 0, False, "installed", "")
        cmdline = make_model("a.gguf", 1000, 0, False, "cmdline", "")
        api = make_model("b.gguf", 1000, 0, False, "api", "")
        both = make_model("c.gguf", 1000, 0, False, "mapped", "")
        both.add_source("api")
        for language, expected in (
            ("en", ["in use (mapped)", "likely decision model (name)", "installed, not proven loaded", "launch arg",
                    "reported (api)", "confirmed (api+mapped)"]),
            ("ja", ["使用中（マップ済み）", "判断モデルの可能性（名前から）", "インストール済み、ロードは未確認", "起動引数",
                    "ランタイム報告 (api)", "確認済み (api+mapped)"]),
        ):
            with self.subTest(language=language):
                set_language(language)
                self.assertEqual([hinted.evidence, hinted.kind_label, installed.evidence, cmdline.evidence, api.evidence,
                                  both.evidence], expected)
        self.assertEqual(hinted.kind_hint, "decision model")
        self.assertEqual(hinted.kind, "LLM")

    def test_gguf_kinds_are_translated_where_shown_and_compared_in_english(self):
        set_language("ja")
        cases = {"LLM": "LLM", "decision model": "判断モデル", "embedding model": "埋め込みモデル", "reranker": "リランカー",
                 "speech model": "音声モデル", "vision projector": "ビジョンプロジェクター", "LoRA adapter": "LoRAアダプター"}
        for kind, japanese in cases.items():
            with self.subTest(kind=kind):
                self.assertEqual(_(kind), japanese)
        view = LlmView(models=[gguf("clip"), gguf("qwen3", **{"general.type": "adapter"})])
        self.assertEqual([model.kind for model in view.models], ["vision projector", "LoRA adapter"])
        self.assertEqual(ProcRow(1, "x", "LLM", ProcGpu(), ProcDetail(1, "x"), view).inside,
                         "+ビジョンプロジェクター, +LoRAアダプター")
        self.assertEqual(view.kind_label(0), "ビジョンプロジェクター")

    def test_inside_summaries(self):
        hinted = make_model("OpenJev.safetensors", 1000, 0, False, "mapped", "")
        installed = make_model("OpenJev.safetensors", GiB, 0, False, "installed", "")
        rows = {
            "handy last": ProcRow(1, "handy.exe", "AI", ProcGpu(), ProcDetail(1, "handy.exe"),
                                  handy=HandyEvidence("a/b.gguf", "a/model.gguf", "loaded", "2026-11-02T23:01:00+00:00")),
            "handy selected": ProcRow(1, "handy.exe", "AI", ProcGpu(), ProcDetail(1, "handy.exe"),
                                      handy=HandyEvidence("handy/model.gguf")),
            "mapped": ProcRow(1, "python.exe", "AI", ProcGpu(), ProcDetail(1, "python.exe", models=[hinted])),
            "installed": ProcRow(1, "python.exe", "AI", ProcGpu(), ProcDetail(1, "python.exe", candidates=[installed])),
            "compositor": ProcRow(1, "dwm.exe", "compositor", ProcGpu(), ProcDetail(1, "dwm.exe")),
            "wsl-vm": ProcRow(1, "vm", "wsl-vm", ProcGpu(), ProcDetail(1, "vm")),
            "external": ProcRow(1, "x", "external", ProcGpu(), ProcDetail(1, "x")),
            "kernel": ProcRow(1, "System", "kernel", ProcGpu(), ProcDetail(1, "System")),
            "browser": ProcRow(1, "edge", "browser", ProcGpu(), ProcDetail(1, "edge")),
            "video": ProcRow(1, "v", "video", ProcGpu(), ProcDetail(1, "v")),
            "3D/game": ProcRow(1, "g", "3D/game", ProcGpu(), ProcDetail(1, "g")),
        }
        expected = {
            "en": {
                "handy last": "Handy last log (loaded): model.gguf",
                "handy selected": "Handy selected (not load proof): model.gguf",
                "mapped": "OpenJev.safetensors (likely decision model (name))",
                "installed": "installed (unproven): OpenJev.safetensors 1.00 GB (likely decision model (name))",
                "compositor": "desktop back buffers + composed frames",
                "wsl-vm": "all Linux GPU memory (every WSL distro + WSLg)",
                "external": "a process in another PID namespace (host or another container)",
                "kernel": "driver/kernel allocations", "browser": "page textures, video, canvas/WebGL",
                "video": "video frames (decode/encode)", "3D/game": "textures, meshes, render targets",
            },
            "ja": {
                "handy last": "Handyの最新ログ（loaded）: model.gguf",
                "handy selected": "Handyで選択中（ロードの証拠ではありません）: model.gguf",
                "mapped": "OpenJev.safetensors（判断モデルの可能性（名前から））",
                "installed": "インストール済み（未確認）: OpenJev.safetensors 1.00 GB（判断モデルの可能性（名前から））",
                "compositor": "デスクトップのバックバッファーと合成済みフレーム",
                "wsl-vm": "LinuxのGPUメモリすべて（全WSLディストリビューションとWSLg）",
                "external": "別のPID名前空間のプロセス（ホストまたは別のコンテナー）",
                "kernel": "ドライバー/カーネルによる割り当て", "browser": "ページのテクスチャ、ビデオ、canvas/WebGL",
                "video": "ビデオフレーム（デコード/エンコード）", "3D/game": "テクスチャ、メッシュ、レンダーターゲット",
            },
        }
        for language, texts in expected.items():
            set_language(language)
            for name, row in rows.items():
                with self.subTest(language=language, row=name):
                    self.assertEqual(row.inside, texts[name])

    def test_handy_event_names_are_translated_where_the_log_is_read(self):
        with tempfile.TemporaryDirectory() as directory:
            appdata, localappdata = Path(directory) / "Roaming", Path(directory) / "Local"
            log_dir = localappdata / "com.pais.handy" / "logs"
            log_dir.mkdir(parents=True)
            (appdata / "com.pais.handy").mkdir(parents=True)
            (log_dir / "handy.log").write_text(
                "[2026-11-02][23:01:00][transcription][INFO] Loaded whisper model 'model-Q8_0.gguf'\n"
                "[2026-11-02][23:01:03][transcription][INFO] Model unloaded due to inactivity (took 20ms)\n",
                encoding="utf-8")
            started = datetime(2026, 11, 2, 23, 0, tzinfo=timezone.utc).timestamp()
            events = {}
            for language in ("en", "ja"):
                set_language(language)
                with patch.dict("gputaskman.handy._log_cache", clear=True):
                    events[language] = inspect_handy(started, str(appdata), str(localappdata))
        self.assertEqual((events["en"].last_event, events["ja"].last_event), ("unloaded", "アンロード済み"))
        self.assertEqual({event.last_model for event in events.values()}, {"model-Q8_0.gguf"})

    def test_counter_status_and_outside_rows_are_built_in_the_selected_language(self):
        for language, mismatch, outside in (
            ("en", "Windows GPU counters could not be matched to the selected adapter; VRAM and processes are "
                   "unavailable. This can occur in GPU-PV VMs.", "(outside this container)"),
            ("ja", "WindowsのGPUカウンターを、選択したアダプターに対応付けられませんでした。VRAMとプロセスは取得できません。"
                   "GPU-PVのVMでは発生することがあります。", "（このコンテナーの外）"),
        ):
            with self.subTest(language=language):
                set_language(language)
                c = Collector.__new__(Collector)
                c.adapter = Adapter(0x4bb7, "GPU", 0x10DE, 16 * GiB, 0, False)
                c.adapters = [c.adapter]
                c.gpu_index, c.scan_budget, c.host, c.host_status = 0, None, None, ""
                c.nvml = Mock(ok=False)
                c.counters = Mock(outside={0x4bb7: {99: ProcGpu(dedicated=58 * MiB)}})
                c.counters.sample.return_value = ({0x4bf1: {}}, {0x4bf1: AdapterGpu(dedicated=GiB, shared=0)})
                c.inspector, c.prober = Mock(), Mock()
                with patch("gputaskman.collector.BACKEND", "wddm"):
                    s = c.sample()
                self.assertEqual(s.counter_status, mismatch)
                self.assertEqual([row.name for row in s.procs], [outside])
                self.assertEqual(s.procs[0].detail.name, outside)

    def test_scan_notes_and_wsl_reasons(self):
        from gputaskman.drm import DrmCounters
        from gputaskman.wslhost import ContextTracker

        for language, status, reason in (
            ("en", "/nope is not readable", "1 Linux GPU process(es) without a VM context to match "
                                            "(one may not have created its GPU context yet)"),
            ("ja", "/nopeを読み取れません", "VMコンテキストと対応付けられないLinux GPUプロセスが1個あります"
                                       "（GPUコンテキストをまだ作成していない可能性があります）"),
        ):
            with self.subTest(language=language), tempfile.TemporaryDirectory() as directory:
                set_language(language)
                counters = DrmCounters(found=[], proc="/nope")
                counters._clients()
                self.assertEqual(counters.status, status)
                tracker = ContextTracker(path=os.path.join(directory, "ctx.json"), boot_id="boot", self_pid=1)
                _guesses, why = tracker.update(7, [], [(5, 1.0)])
                self.assertEqual(why, reason)
        set_language("ja")
        self.assertEqual(_("; ").join(["a", "b"]), "a。b")


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

    def test_text_output_follows_the_flag_then_the_environment(self):
        japanese = {"GPUTASKMAN_LANG": "ja"}
        self.assertIn("プロセス", self.run_cli("--once", env=japanese))
        self.assertIn("プロセス", self.run_cli("--once", "--lang", "ja"))
        english = self.run_cli("--once", "--lang", "en", env=japanese)
        self.assertIn("PROCESS", english)
        self.assertNotIn("プロセス", english)

    def test_option_errors_are_reported_in_the_selected_language(self):
        for args, expected in ((["--lang", "ja", "--gpu", "-1"], "--gpuには0以上のインデックスを指定してください"),
                               (["--lang", "ja", "-i", "0"], "--intervalには0より大きい有限の数値を指定してください")):
            with self.subTest(args=args):
                err = io.StringIO()
                with patch("sys.argv", ["gputaskman", *args]), contextlib.redirect_stderr(err), \
                        self.assertRaises(SystemExit):
                    main()
                self.assertIn(expected, err.getvalue())

    def test_diff_text_follows_the_language_and_diff_json_stays_english(self):
        with tempfile.TemporaryDirectory() as directory:
            before, after = (os.path.join(directory, name) for name in ("before.json", "after.json"))
            for path, data in ((before, diff_snap([], used=GiB, attributed=GiB)),
                               (after, diff_snap([diff_proc(1, "x", vram=GiB)], used=2 * GiB, attributed=2 * GiB))):
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f)
            for args, env, expected in ((["--lang", "ja"], {}, "デバイス（実測）"),
                                        ([], {"GPUTASKMAN_LANG": "ja"}, "デバイス（実測）"),
                                        (["--lang", "en"], {"GPUTASKMAN_LANG": "ja"}, "DEVICE (measured)")):
                with self.subTest(args=args, env=env):
                    out = io.StringIO()
                    with patch("sys.argv", ["gputaskman", "diff", before, after, *args]), \
                            contextlib.redirect_stdout(out), patch.dict(os.environ, env):
                        main()
                    self.assertIn(expected, out.getvalue())
            out = io.StringIO()
            with patch("sys.argv", ["gputaskman", "diff", before, after, "--json", "--lang", "ja"]), \
                    contextlib.redirect_stdout(out):
                main()
            self.assertEqual(json.loads(out.getvalue())["device"]["vram_used"]["delta"], GiB)
            self.assertEqual(current_language(), "en")


if __name__ == "__main__":
    unittest.main()
