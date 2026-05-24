#!/usr/bin/env python3
"""Merge Loyalsoldier reject list into Reject.yaml.

- Source: https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/reject.txt
- Target file: Reject.yaml
- Keeps existing Reject.yaml rules, appends only new DOMAIN-SUFFIX rules.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.request import urlopen
import argparse

SOURCE_URL = "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/reject.txt"
TARGET = Path("Reject.yaml")
SECTION_HEADER = "# === Auto merged from Loyalsoldier reject.txt ==="

RULE_RE = re.compile(r"^\s*-\s*(.+?)\s*$")


def normalize_source_line(line: str) -> str | None:
    s = line.strip()
    if not s or s.startswith("#"):
        return None

    # Handle YAML payload list items: - '+.example.com'
    if s.startswith("-"):
        s = s[1:].strip()
    s = s.strip("'\"")

    # Loyalsoldier reject format often uses +.domain entries.
    if s.startswith("+.") and len(s) > 2:
        return f"DOMAIN-SUFFIX,{s[2:].lower()}"

    # Accept existing Clash rule format from source.
    if "," in s:
        kind, value, *rest = [x.strip() for x in s.split(",")]
        kind = kind.upper().replace("_", "-")
        if kind == "DOMAIN-SUFFIX" and value:
            return f"DOMAIN-SUFFIX,{value.lower()}"
        return None

    # Plain domain line in reject.txt.
    if re.match(r"^[A-Za-z0-9.-]+$", s):
        return f"DOMAIN-SUFFIX,{s.lower()}"

    return None


def load_existing_rules(text: str) -> tuple[list[str], set[str]]:
    lines = text.splitlines()
    existing_rules: list[str] = []
    existing_set: set[str] = set()

    for ln in lines:
        m = RULE_RE.match(ln)
        if not m:
            continue
        rule = m.group(1).strip()
        if not rule:
            continue
        existing_rules.append(rule)
        existing_set.add(rule)

    return lines, existing_set


def fetch_source_rules(raw: str) -> list[str]:

    out: list[str] = []
    seen: set[str] = set()
    for ln in raw.splitlines():
        rule = normalize_source_line(ln)
        if not rule or rule in seen:
            continue
        seen.add(rule)
        out.append(rule)
    return out


def merge(source_file: str | None = None) -> int:
    if not TARGET.exists():
        raise FileNotFoundError(f"{TARGET} not found")

    text = TARGET.read_text(encoding="utf-8")
    lines, existing = load_existing_rules(text)

    if source_file:
        raw = Path(source_file).read_text(encoding="utf-8", errors="replace")
    else:
        with urlopen(SOURCE_URL, timeout=30) as resp:
            raw = resp.read().decode("utf-8", errors="replace")

    source_rules = fetch_source_rules(raw)
    new_rules = [r for r in source_rules if r not in existing]

    if not new_rules:
        print("No new rules to merge.")
        return 0

    # Ensure file starts with payload root key.
    if not lines or lines[0].strip() != "payload:":
        raise ValueError("Reject.yaml must start with 'payload:'")

    out_lines = list(lines)
    if out_lines and out_lines[-1].strip() != "":
        out_lines.append("")
    out_lines.append(SECTION_HEADER)
    for rule in new_rules:
        out_lines.append(f"  - {rule}")
    out_lines.append("")

    TARGET.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"Merged {len(new_rules)} new rules into {TARGET}.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", help="Use local source file instead of network URL.")
    args = parser.parse_args()
    try:
        raise SystemExit(merge(source_file=args.source_file))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
