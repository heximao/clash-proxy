# CLAUDE.md

This file provides guidance to Agent when working with code in this repository.

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

# Merge latest reject rules from Loyalsoldier upstream into Reject.yaml
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

- **Naming**: `CapitalCase.yaml` for new files (e.g., `SocialMedia.yaml`).
- **Deprecation**: Rename retired files with `弃用` suffix (e.g., `ServiceName弃用.yaml`) — do not delete.
- **Grouping**: Use `# === Service Name ===` comment headers to group rules by service/category.
- **Catch-all files**: `Proxy.yaml` (proxy routing) and `Direct.yaml` (direct connection) hold miscellaneous rules. Major services (Apple, Google, Microsoft, AI, etc.) have dedicated files.
- **Reject.yaml** (~6.7 MB) is auto-generated daily by GitHub Actions from Loyalsoldier's upstream — do not manually edit its `DOMAIN-SUFFIX` entries from that source.
- **log/**: OpenClash runtime logs (traffic logs and plugin logs). Log entries showing `match Match` indicate domains that didn't match any rule and fell through to the "漏网之鱼" (unmatched) policy group. Periodically review these domains and categorize them into the appropriate rule files.

## Rule Files

| File | Description |
|------|-------------|
| **Proxy.yaml** | Catch-all for sites that need proxy — miscellaneous blocked/overseas domains |
| **Direct.yaml** | Catch-all for sites that can connect directly — domestic & unblocked overseas |
| **Reject.yaml** | Ad/tracking/malware blocking — auto-generated from Loyalsoldier upstream, do not manually edit |
| **Google.yaml** | Google services |
| **Youtube.yaml** | YouTube |
| **Telegram.yaml** | Telegram |
| **Meta.yaml** | Facebook, Instagram, WhatsApp, Threads |
| **X.yaml** | Twitter / X |
| **LINE.yaml** | LINE messenger |
| **Spotify.yaml** | Spotify |
| **Streaming.yaml** | Streaming services (Netflix, Disney+, HBO, etc.) |
| **Social.yaml** | Social platforms (Reddit, Discord, Pinterest, etc.) |
| **Pornhub.yaml** | Pornhub |
| **AI.yaml** | AI services (ChatGPT alternatives, Perplexity, etc.) |
| **OpenAI.yaml** | OpenAI (ChatGPT, API, etc.) |
| **ClaudeAI.yaml** | Claude / Anthropic |
| **Github.yaml** | GitHub and related developer tools |
| **Apple.yaml** | Apple services (App Store, iCloud, etc.) |
| **Microsoft.yaml** | Microsoft services (Office, Azure, etc.) |
| **NVIDIA.yaml** | NVIDIA services |
| **Crypto.yaml** | Cryptocurrency exchanges and wallets |
| **hk-broker.yaml** | Brokerages (TradingView, Longbridge, IBKR, etc.) |
| **hk-bank.yaml** | Hong Kong banks (HSBC, ZA, Welab, etc.) + financial media |
| **Fin-Media.yaml** | Financial media and data |
| **DNS.yaml** | DNS servers |

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

A single GitHub Actions workflow (`auto-merge-reject.yml`) runs daily at 00:20 UTC. It calls `scripts/merge_reject_from_loyalsoldier.py` and auto-commits changes to `Reject.yaml`.
