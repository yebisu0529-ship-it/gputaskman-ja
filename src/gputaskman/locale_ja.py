"""Japanese catalog: each key is an English string exactly as it appears in the source.

A key with no entry falls back to English. tests/test_i18n.py names the missing and the stale keys.
"""

from __future__ import annotations

MESSAGES: dict[str, str] = {}
