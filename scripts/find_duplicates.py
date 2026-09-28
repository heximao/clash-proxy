#!/usr/bin/env python3
"""Scan YAML files for rule entries and report duplicates.
Generates: DUPLICATES.md and duplicates.json
Also prints per-file intra-file duplicates.

Exit code: 0 when no duplicates found, 1 when any cross-file or
intra-file duplicate exists (reports are still written either way).
"""
import re
import sys
import json
from pathlib import Path

root = Path('.')
# Reports are written next to this script (scripts/), while scanning stays at repo root.
out_dir = Path(__file__).resolve().parent
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
cross_file = [(rule, fs) for rule, fs in rule_map.items() if len(fs) > 1]
cross_file.sort(key=lambda x: (-len(x[1]), x[0]))
intra_dup_total = sum(len(dups) for dups in file_dups.values())

md = []
md.append('# Duplicate Rules Report\n')
md.append('Rules appearing in more than one file:\n')
for rule, fileset in cross_file:
    md.append(f'- `{rule}`: {len(fileset)} files')
    for f in sorted(fileset):
        md.append(f'  - {f}')

md.append('\nPer-file intra-file duplicates (same rule repeated within the same file):\n')
for f, dups in file_dups.items():
    if dups:
        md.append(f'- {f}:')
        for r in dups:
            md.append(f'  - `{r}`')

(out_dir / 'DUPLICATES.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
(out_dir / 'duplicates.json').write_text(json.dumps({'rule_map': {k:sorted(list(v)) for k,v in rule_map.items()}, 'file_dups': file_dups}, indent=2), encoding='utf-8')

print(f'Wrote {out_dir / "DUPLICATES.md"} and {out_dir / "duplicates.json"}')
print(f'Cross-file duplicate rules: {len(cross_file)}; intra-file duplicate entries: {intra_dup_total}')

# Non-zero exit when duplicates exist, so callers/CI can gate on the status.
sys.exit(1 if cross_file or intra_dup_total else 0)
