"""Message lookup: the English strings in the source are the message ids, a catalog supplies the translation.

The library default is English. Only the command line chooses a language, once, before it renders anything.
"""

from __future__ import annotations

import ctypes
import os
import sys
from collections.abc import Mapping

from rich.cells import cell_len, set_cell_size

LANGUAGES = ("en", "ja")
LANG_JAPANESE = 0x11  # primary language id inside a Windows LANGID

_language = "en"
_messages: Mapping[str, str] = {}


def _windows_ui_language() -> int | None:
    if sys.platform != "win32":
        return None
    try:
        return ctypes.windll.kernel32.GetUserDefaultUILanguage()
    except (AttributeError, OSError):
        return None


def detect_language(environ: Mapping[str, str] = os.environ) -> str:
    choice = environ.get("GPUTASKMAN_LANG", "").strip().lower()
    if choice in LANGUAGES:
        return choice
    for name in ("LC_ALL", "LC_MESSAGES", "LANG"):
        value = environ.get(name, "").strip()
        if value:
            return "ja" if value.lower().startswith("ja") else "en"
    ui_language = _windows_ui_language()
    return "ja" if ui_language is not None and ui_language & 0x3FF == LANG_JAPANESE else "en"


def set_language(lang: str) -> None:
    global _language, _messages
    if lang == "auto":
        lang = detect_language()
    if lang not in LANGUAGES:
        raise ValueError(f"unsupported language {lang!r}; expected auto, {', '.join(LANGUAGES)}")
    if lang == "ja":
        from .locale_ja import MESSAGES

        _messages = MESSAGES
    else:
        _messages = {}
    _language = lang


def current_language() -> str:
    return _language


def _(msgid: str) -> str:
    return _messages.get(msgid, msgid)


def fit(text: str, width: int, align: str = "<") -> str:
    """Pad or crop text to exactly `width` terminal cells; a wide character takes two."""
    if align not in ("<", ">"):
        raise ValueError(f"unsupported alignment {align!r}")
    short = width - cell_len(text)
    if align == ">" and short >= 0:
        return " " * short + text
    return set_cell_size(text, width)
