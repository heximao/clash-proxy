#!/usr/bin/env python3
"""Scan YAML files for rule entries and report duplicates.
Generates: DUPLICATES.md and duplicates.json
Also prints per-file intra-file duplicates.
"""
import re
from pathlib import Path
import json

root = Path('.')
files = sorted(root.rglob('*.yaml'))
rule_re = re.compile(r"^\s*-\s*(.+)$")

rule_map = {}  # rule -> set(files)
file_rules = {}
file_dups = {}

for p in files:
    text = p.read_text(encoding='utf-8')
    lines = text.splitlines()
    seen = {}
    rules = []
    dups = []
    for ln in lines:
        m = rule_re.match(ln)
        if m:
            rule = m.group(1).strip()
            rules.append(rule)
            if rule in seen:
                dups.append(rule)
            seen[rule] = seen.get(rule, 0) + 1
            rule_map.setdefault(rule, set()).add(str(p))
    file_rules[str(p)] = rules
    file_dups[str(p)] = sorted(set(dups))

# Prepare DUPLICATES.md
md = []
md.append('# Duplicate Rules Report\n')
md.append('Rules appearing in more than one file:\n')
for rule, fileset in sorted(rule_map.items(), key=lambda x: (-len(x[1]), x[0])):
    if len(fileset) > 1:
        md.append(f'- `{rule}`: {len(fileset)} files')
        for f in sorted(fileset):
            md.append(f'  - {f}')

md.append('\nPer-file intra-file duplicates (same rule repeated within the same file):\n')
for f, dups in file_dups.items():
    if dups:
        md.append(f'- {f}:')
        for r in dups:
            md.append(f'  - `{r}`')

(Path(root) / 'DUPLICATES.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
(Path(root) / 'duplicates.json').write_text(json.dumps({'rule_map': {k:sorted(list(v)) for k,v in rule_map.items()}, 'file_dups': file_dups}, indent=2), encoding='utf-8')

print('Wrote DUPLICATES.md and duplicates.json')

# Exit status
import sys
sys.exit(0)
