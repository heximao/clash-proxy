#!/usr/bin/env python3
"""Normalize section comment headings in YAML files to: # === Title ===

Heuristic: a comment line is considered a section heading if it's a comment
and within the next 3 non-empty lines there's a rule line starting with '-' .
"""
import re
import sys
from pathlib import Path

root = Path('.')
files = sorted(root.rglob('*.yaml')) + sorted(root.rglob('*.yml'))
modified = []

heading_re = re.compile(r"^\s*#\s*(.*)\s*$")

for p in files:
    try:
        text = p.read_text(encoding='utf-8')
    except Exception:
        continue
    lines = text.splitlines()
    changed = False
    out_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = heading_re.match(line)
        if m:
            comment = m.group(1)
            # lookahead for a rule line starting with '-' within next 3 non-empty lines
            found_rule = False
            for j in range(i+1, min(i+5, len(lines))):
                if re.match(r"^\s*-\s+", lines[j]):
                    found_rule = True
                    break
            if found_rule:
                # normalize text: remove leading markers like '>', '===', '-' and trailing ===
                t = comment
                t = re.sub(r"^[>=\-\s]+", "", t)
                t = re.sub(r"\s*[=]+\s*$", "", t)
                t = t.strip()
                if t:
                    new = "# === {} ===".format(t)
                else:
                    new = "# === ==="
                # ensure a blank line before heading unless at top or previous is blank
                if out_lines and out_lines[-1].strip() != '':
                    out_lines.append('')
                out_lines.append(new)
                changed = changed or (new != line)
                i += 1
                # skip original comment line already handled
                continue
        out_lines.append(line)
        i += 1
    if changed:
        p.write_text('\n'.join(out_lines) + '\n', encoding='utf-8')
        modified.append(str(p))

print('MODIFIED', len(modified))
for m in modified:
    print(m)
