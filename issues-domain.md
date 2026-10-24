# issues-domain：待人工判定域名

本文件登记 `fill-domains-from-log` 流程中**证据不足、无法判定归属**的域名，按登记轮次追加，留待用户（野人）人工判定。维护规范：fill-domains-from-log skill 第 6b 节（v2.8.0 起）。

## 使用说明

- **登记**：第 6 步 RDAP / DoH 查证后仍无归属结论的主域（含判据 5「无锚点厂商文件」的大型公司主域），追加到表尾；已在表中的域名不重复登记。
- **排序**：按登记日期升序——最早挂起、长期未定案的排在前面，便于优先处理。
- **数据口径**：「命中子域（次数）」取该域最近一轮的日志实证（轮次为日志日期，非处理日期）；进程为发起进程名。
- **定案闭环**：用户给出归属 → 补录对应 yaml、移除本表该行、skip-list `manual` 项同步移除；用户裁决不收录 → 移除本表该行、skip-list 改 `skip` 模式、AGENTS.md「已裁决结论」清单留痕（交互式会话）。
- **本文件只保留待判定域名**：定案去向与依据只写 `changelog.md`，不在本表保留定案记录段；行被移除即净出，表始终等于「当前待判定集合」。
- **三处一致**：本表 ↔ skip-list `manual` 段 ↔ changelog「待人工确认」段，数量与条目须一致（交互式会话第 0 节对齐检查）。
- **不进表的类**（已裁决，无需用户判定）：无主端点（`antpeak.com` 类）、广告/追踪类、reject 上游已收录、伪域名/探针族——均为 skip-list `skip` 模式。
- **automation 说明**：本文件是普通仓库文件（不同于受保护的 AGENTS.md），automation 轮可直接追加并随轮提交推送；行的移除只发生在用户定案后。

## 待判定域名（共 15 项）

| # | 域名 | 登记日期 | 命中子域（次数） | 进程 | 已查证据 | 存疑点 / 待定夺 |
|---|---|---|---|---|---|---|
| 1 | applogcdn.com | 2026-10-17 | lf-static.（10-16 日志） | — | 无品牌标识、无既有命名族 | CDN 归属待定 |
| 2 | mdoelscope.ai | 2026-10-17 | mdoelscope.ai（×2，:80，10-17 日志） | firefox | 与已覆盖 `modelscope.ai` 仅字母转位之差（`mdoel`↔`model`），判据 1 不适用——仿冒域 | 已判定仿冒不补录，待用户确认后转 skip 模式 |
| 3 | 123169.xyz | 2026-10-20 | api.（10-19 日志 ×26 / 10-20 日志 ×2） | firefox | Dynadot 注册 + Cloudflare NS 隐私保护，无归属线索 | 用户主动高频访问的用途待确认（疑自建服务/API） |
| 4 | 111666.best | 2026-10-20 | i.（10-19 日志 ×24 / 10-20 日志 ×6） | firefox | 同 `123169.xyz` 模式（Cloudflare 隐私保护） | 同 `123169.xyz` |
| 5 | 999831.xyz | 2026-10-20 | cf.（10-19 日志 ×3 / 10-20 日志 ×1） | firefox | 同 `123169.xyz` 模式（Cloudflare 隐私保护） | 同 `123169.xyz` |
| 6 | yjz.hk | 2026-10-20 | yjz.hk（×2，10-19 日志） | WorkBuddy Helper | .hk 无 RDAP 数据 + Cloudflare A 记录，无归属线索 | 归属待定 |
| 7 | tsight.io | 2026-10-20 | tsight.io（×2，10-19 日志） | WorkBuddy Helper | 无归属线索，RDAP 无结论 | 归属待定 |
| 8 | nsvcs.net | 2026-10-20 | ingesteer.services-prod.（×1，10-19 日志） | firefox | AWS Route53 NS，无品牌指向（遥测摄入端点） | 归属待定 |
| 9 | ns1pcdn.net | 2026-10-20 | 9y49n2-m. / 5bav82-m. / 1xtsor1-m. / 1lmnv6z-m. / 1a4s4dv-m.（各 ×1，10-19 日志） | firefox | CSC 企业注册 + NS1；与 `mountaintoys.cn` 同批 CDN 模式但判据 2 不满足 | CDN 归属待定 |
| 10 | sitemana.com | 2026-10-20 | p.（10-19 日志 ×22 / 10-20 日志 ×8） | Google Chrome Helper | Squarespace + CloudFront A 记录，疑似广告验证但证据不足 | 广告验证端点——按 reject 上游类不落盘还是留 |
| 11 | featureassets.org | 2026-10-20 | featureassets.org（×1，10-19 日志） | firefox | MarkMonitor 企业域 + GCP A 记录，疑似追踪但证据不足 | 归属待定 |
| 12 | pixpix.com | 2026-10-21 | www. / pixpix.com（各 ×1，10-20 日志） | firefox | GoDaddy + Cloudflare 无主端点（同 `123169.xyz` 模式） | 归属待定 |
| 13 | byte-test.com | 2026-10-21 | perfops.（×2，10-20 日志） | firefox | byte* 字面但注册模式（阿里云 + alidns NS，2021 注册）与字节惯例（MarkMonitor + bytedns）不符；CNAME `bplslb.com`（自有 bpldns NS）无定论 | 阿里云/alidns 国内倾向但非「高度国内」实证——直连还是代理待定夺 |
| 14 | freloop.com | 2026-10-22 | freloop.com（×3，10-21 日志） | firefox | NameCheap 注册（2025-05）+ Cloudflare NS + A 记录，首页 429 / 直连 SSL 失败，无归属线索 | 同 pixpix.com / 123169.xyz 模式，归属待定 |
| 15 | wdfl.co | 2026-10-24 | r.（×1，10-23 日志） | — | .co 无 RDAP 数据；主域无 A 记录；r. 子域 CNAME CloudFront（AWS）短链端点 | 无品牌指向、无进程，短链服务归属待定 |

> 登记日期说明：2026-10-17 之前挂起的历史项按 changelog「连续第 N 轮遗留」反推取近似值；其余为首次挂起轮的 changelog 条目日期。
