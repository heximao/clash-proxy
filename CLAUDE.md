# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Clash proxy rule-provider repository — a collection of YAML rule files served via jsDelivr CDN for Clash / OpenClash clients. No application runtime; this is a pure data/content repository.

CDN URL pattern: `https://cdn.jsdelivr.net/gh/heximao/clash-proxy/<filename>.yaml`

## Key Commands

There is no build system, test suite, or linter configured. Verification is manual:

```bash
# Validate YAML syntax
python -c "import sys,yaml; yaml.safe_load(sys.stdin)" < SomeFile.yaml

# Check for duplicate rules across files (outputs DUPLICATES.md + duplicates.json)
python3 scripts/find_duplicates.py

# Merge latest reject rules from Loyalsoldier upstream into reject.yaml
python3 scripts/merge_reject_from_loyalsoldier.py

# Normalize section comment headings to `# === Title ===` format
python3 scripts/normalize_yaml_comments.py
```

## File Format Rules

Every `.yaml` rule file **must** start with `payload:` as the root key. Rule types used:

- `DOMAIN-SUFFIX,example.com` — preferred for most sites
- `DOMAIN-KEYWORD,keyword`
- `IP-CIDR,1.1.1.1/32,no-resolve`
- `PROCESS-NAME,BinaryName` — use sparingly, desktop apps only

Use `DOMAIN-SUFFIX` (hyphen), **not** `DOMAIN_SUFFIX` (underscore).

## Conventions

- **Naming**: `lowercase.yaml` with hyphens for multi-word names (e.g., `hk-broker.yaml`, `fin-media.yaml`).
- **Grouping**: Use `# === Service Name ===` comment headers to group rules by service/category.
- **Catch-all files**: `proxy.yaml` (proxy routing) and `direct.yaml` (direct connection) hold miscellaneous rules. Major services (Apple, Google, Microsoft, AI, etc.) have dedicated files.
- **reject.yaml** (~7 MB) is auto-generated daily by GitHub Actions from Loyalsoldier's upstream — do not manually edit its `DOMAIN-SUFFIX` entries from that source.
- **log/**: OpenClash runtime logs (traffic logs and plugin logs). Log entries showing `match Match` indicate domains that didn't match any rule and fell through to the "漏网之鱼" (unmatched) policy group. Periodically review these domains and categorize them into the appropriate rule files.

## Rule Files

| File | Description |
|------|-------------|
| **proxy.yaml** | Catch-all for sites that need proxy — miscellaneous blocked/overseas domains |
| **direct.yaml** | Catch-all for sites that can connect directly — domestic & unblocked overseas |
| **reject.yaml** | Ad/tracking/malware blocking — auto-generated from Loyalsoldier upstream, do not manually edit |
| **google.yaml** | Google services |
| **youtube.yaml** | YouTube |
| **telegram.yaml** | Telegram |
| **meta.yaml** | Facebook, Instagram, WhatsApp, Threads |
| **x.yaml** | Twitter / X |
| **line.yaml** | LINE messenger |
| **spotify.yaml** | Spotify |
| **streaming.yaml** | Streaming services (Netflix, Disney+, HBO, etc.) |
| **social.yaml** | Social platforms (Reddit, Discord, Pinterest, etc.) |
| **pornhub.yaml** | Pornhub |
| **claude.yaml** | Claude / Anthropic |
| **openai.yaml** | OpenAI (ChatGPT, API, etc.) |
| **direct-ai.yaml** | AI services accessible via direct connection |
| **proxy-ai.yaml** | AI services requiring proxy |
| **github.yaml** | GitHub and related developer tools |
| **apple.yaml** | Apple services (App Store, iCloud, etc.) |
| **microsoft.yaml** | Microsoft services (Office, Azure, etc.) |
| **nvidia.yaml** | NVIDIA services |
| **crypto.yaml** | Cryptocurrency exchanges and wallets |
| **hk-broker.yaml** | Hong Kong brokerages (TradingView, Longbridge, IBKR, etc.) |
| **us-broker.yaml** | US brokerages |
| **hk-bank.yaml** | Hong Kong banks (HSBC, ZA, Welab, etc.) + financial media |
| **fin-media.yaml** | Financial media and data |

## Sync Rule

When `CLAUDE.md` is updated, `CLAUDE.zh-CN.md` must also be updated to stay in sync.

## Git Workflow

When editing local files, always follow this sequence:

1. **Check remote** — run `git fetch` and compare local vs remote (`git status` or `git rev-list`). If remote has new commits, `git pull --rebase` first.
2. **Edit local files** — make your changes.
3. **Commit & push** — stage, commit, then `git push`.

Never push without first ensuring the local branch is up to date with the remote.

## Commit Convention

- Commit messages should be written in Chinese.

## CI/CD

A single GitHub Actions workflow (`auto-merge-reject.yml`) runs daily at 00:20 UTC. It calls `scripts/merge_reject_from_loyalsoldier.py` and auto-commits changes to `reject.yaml`.
