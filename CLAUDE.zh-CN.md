# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在本仓库中工作时提供指引。

## 项目概述

Clash 代理规则提供者仓库 — 一组通过 jsDelivr CDN 分发给 Clash / OpenClash 客户端的 YAML 规则文件。无应用运行时，纯数据/内容仓库。

CDN URL 格式：`https://cdn.jsdelivr.net/gh/heximao/clash-proxy/<filename>.yaml`

## 常用命令

本仓库无构建系统、测试套件或 linter，验证需手动进行：

```bash
# 校验 YAML 语法
python -c "import sys,yaml; yaml.safe_load(sys.stdin)" < SomeFile.yaml

# 检查跨文件重复规则（输出 DUPLICATES.md + duplicates.json）
python3 scripts/find_duplicates.py

# 从 Loyalsoldier 上游合并最新拒绝规则至 reject.yaml
python3 scripts/merge_reject_from_loyalsoldier.py

# 将章节注释标题规范化为 `# === Title ===` 格式
python3 scripts/normalize_yaml_comments.py
```

## 文件格式规则

每个 `.yaml` 规则文件**必须**以 `payload:` 作为根键开头。使用的规则类型：

- `DOMAIN-SUFFIX,example.com` — 大多数网站首选
- `DOMAIN-KEYWORD,keyword`
- `IP-CIDR,1.1.1.1/32,no-resolve`
- `PROCESS-NAME,BinaryName` — 谨慎使用，仅限桌面应用

使用 `DOMAIN-SUFFIX`（连字符），**而非** `DOMAIN_SUFFIX`（下划线）。

## 约定

- **命名**：新文件使用 `lowercase.yaml`，多词用连字符（如 `hk-broker.yaml`、`fin-media.yaml`）。
- **分组**：使用 `# === Service Name ===` 注释头按服务/类别分组规则。
- **兜底文件**：`proxy.yaml`（代理路由）和 `direct.yaml`（直连）存放杂项规则。主要服务（Apple、Google、Microsoft、AI 等）有各自专属文件。
- **reject.yaml**（约 7 MB）由 GitHub Actions 每日从 Loyalsoldier 上游自动生成 — 请勿手动编辑其中来自上游的 `DOMAIN-SUFFIX` 条目。
- **log/**：OpenClash 运行日志（流量日志和插件日志）。日志中 `match Match` 表示该域名未匹配任何规则，落入了"漏网之鱼"策略组。需定期将这些域名归类到对应的规则文件中。

## 规则文件一览

| 文件 | 说明 |
|------|------|
| **apple.yaml** | Apple 服务（App Store、iCloud 等） |
| **claude.yaml** | Claude / Anthropic |
| **crypto.yaml** | 加密货币交易所与钱包 |
| **direct.yaml** | 兜底直连 — 国内及可直连的海外域名 |
| **direct-ai.yaml** | 可直连的 AI 服务 |
| **fin-media.yaml** | 财经媒体与数据 |
| **fin-tech.yaml** | 金融科技工具（TradingView 等） |
| **github.yaml** | GitHub 及相关开发者工具 |
| **google.yaml** | Google 服务 |
| **hk-bank.yaml** | 香港银行（汇丰、ZA、汇立等）+ 财经媒体 |
| **hk-broker.yaml** | 港美股券商（TradingView、长桥、IBKR 等） |
| **line.yaml** | LINE 即时通讯 |
| **meta.yaml** | Facebook、Instagram、WhatsApp、Threads |
| **microsoft.yaml** | Microsoft 服务（Office、Azure 等） |
| **nvidia.yaml** | NVIDIA 服务 |
| **openai.yaml** | OpenAI（ChatGPT、API 等） |
| **pornhub.yaml** | Pornhub |
| **proxy.yaml** | 兜底代理 — 需代理的杂项域名 |
| **proxy-ai.yaml** | 需代理的 AI 服务 |
| **reject.yaml** | 广告/追踪/恶意软件拦截 — 由 Loyalsoldier 上游自动生成，勿手动编辑 |
| **social.yaml** | 社交平台（Reddit、Discord、Pinterest 等） |
| **spotify.yaml** | Spotify |
| **streaming.yaml** | 流媒体服务（Netflix、Disney+、HBO 等） |
| **telegram.yaml** | Telegram |
| **us-broker.yaml** | 美股券商 |
| **x.yaml** | Twitter / X |
| **youtube.yaml** | YouTube |

## 同步规则

当 `CLAUDE.md` 更新时，`CLAUDE.zh-CN.md` 也必须同步更新。更新之后并检查两份文档全文内容是否一致，如不一致，询问用户改如何修改。

## Git 工作流

编辑本地文件时，始终遵循以下顺序：

1. **检查远程** — 执行 `git fetch` 并对比本地与远程（`git status` 或 `git rev-list`）。若远程有新提交，先 `git pull --rebase`。
2. **编辑本地文件** — 进行修改。
3. **提交并推送** — 暂存、提交，然后 `git push`。

确保本地分支与远程同步后再推送，禁止跳过检查直接 push。

## 提交规范

- 提交信息（commit message）尽量使用中文。

## CI/CD

单一 GitHub Actions 工作流（`auto-merge-reject.yml`）每日 00:20 UTC 运行，调用 `scripts/merge_reject_from_loyalsoldier.py` 并自动提交 `reject.yaml` 的变更。
