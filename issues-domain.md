# issues-domain：待人工判定域名

本文件登记 `fill-domains-from-log` 流程中**证据不足、无法判定归属**的域名，按登记轮次追加，留待用户（野人）人工判定。维护规范：fill-domains-from-log skill 第 6b 节（v2.8.0 起）。

## 使用说明

- **登记**：第 6 步 RDAP / DoH 查证后仍无归属结论的主域（含判据 5「无锚点厂商文件」的大型公司主域），追加到表尾；已在表中的域名不重复登记。
- **排序**：按登记日期升序——最早挂起、长期未定案的排在前面，便于优先处理。
- **数据口径**：「命中子域（次数）」取该域最近一轮的日志实证（轮次为日志日期，非处理日期）；进程为发起进程名。
- **定案闭环**：用户给出归属 → 补录对应 yaml、移除本表该行、skip-list `manual` 项同步移除；用户裁决不收录 → 移除本表该行、skip-list 改 `skip` 模式、AGENTS.md「已裁决结论」清单留痕（交互式会话）。
- **三处一致**：本表 ↔ skip-list `manual` 段 ↔ changelog「待人工确认」段，数量与条目须一致（交互式会话第 0 节对齐检查）。
- **不进表的类**（已裁决，无需用户判定）：无主端点（`antpeak.com` 类）、广告/追踪类、reject 上游已收录、伪域名/探针族——均为 skip-list `skip` 模式。
- **automation 说明**：本文件是普通仓库文件（不同于受保护的 AGENTS.md），automation 轮可直接追加并随轮提交推送；行的移除只发生在用户定案后。

## 待判定域名（共 28 项）

| # | 域名 | 登记日期 | 命中子域（次数） | 进程 | 已查证据 | 存疑点 / 待定夺 |
|---|---|---|---|---|---|---|
| 1 | oceanengine.com | 2026-10-11 | athena-api.（×2，10-17 日志） | Lark Helper | 判据 5 无锚点厂商文件；RDAP 查证无归属结论；10-17 轮已「连续第七轮遗留」 | 巨量引擎为字节旗下广告平台——归 `bytedance.yaml` 还是按广告类不落盘 |
| 2 | ntp.org.cn | 2026-10-11 | edu.（×14）/ cn.（×8，10-20 日志） | Lark Helper | 国内 NTP 时间服务；运营方需外部知识确认，RDAP 无结论 | 归 `direct.yaml`「公共 DNS / NTP」类分组还是独立处理 |
| 3 | yhgfb-cn-static.com | 2026-10-11 | lf-rc1.（×2，10-17 日志） | Feishu | 域内无字节/飞书品牌标识，不匹配 `byte*` 命名族（判据 4 不适用） | 静态资源 CDN 归属待定 |
| 4 | logitech.io | 2026-10-15 | flow.（10-19 日志 ×92）/ device-compatibility.np.、datapipeline.（10-20 日志各 ×1） | logioptionsplus_agent | 判据 5：无 `logitech.yaml` 锚点文件；10-17 轮已「连续第三轮遗留」 | 是否建 `logitech.yaml` 厂商文件（罗技 Options+ 遥测/更新端点） |
| 5 | applogcdn.com | 2026-10-17 | lf-static.（10-16 日志） | — | 无品牌标识、无既有命名族 | CDN 归属待定 |
| 6 | photon.codes | 2026-10-17 | app. / spectrum.（10-16 日志） | curl | 无产品指向，RDAP 无结论 | 海外杂项归 `proxy.yaml` 还是继续挂起 |
| 7 | temu.com | 2026-10-17 | www.（10-16 日志） | Chrome Helper | 跨境电商，无覆盖锚点 | 海外电商归 `proxy.yaml` 还是建专属分组 |
| 8 | mdoelscope.ai | 2026-10-17 | mdoelscope.ai（×2，:80，10-17 日志） | firefox | 与已覆盖 `modelscope.ai` 仅字母转位之差（`mdoel`↔`model`），判据 1 不适用——仿冒域 | 已判定仿冒不补录，待用户确认后转 skip 模式 |
| 9 | logitechg.com | 2026-10-18 | updates.optionsplus.（×2，10-20 日志） | logioptionsplus_updater | 判据 5 无锚点（Logitech G 系，与 `logitech.io` 同族） | 同 `logitech.io`——是否建 Logitech 厂商文件 |
| 10 | logitech.com | 2026-10-20 | updates.（×1，10-19 日志）/ geo-location-finder.（×1，10-20 日志） | logioptionsplus_agent | 判据 5 无锚点（罗技主域，与 logitech.io/logitechg.com 同族） | 同 `logitech.io` |
| 11 | 123169.xyz | 2026-10-20 | api.（10-19 日志 ×26 / 10-20 日志 ×2） | firefox | Dynadot 注册 + Cloudflare NS 隐私保护，无归属线索 | 用户主动高频访问的用途待确认（疑自建服务/API） |
| 12 | 111666.best | 2026-10-20 | i.（10-19 日志 ×24 / 10-20 日志 ×6） | firefox | 同 `123169.xyz` 模式（Cloudflare 隐私保护） | 同 `123169.xyz` |
| 13 | 999831.xyz | 2026-10-20 | cf.（10-19 日志 ×3 / 10-20 日志 ×1） | firefox | 同 `123169.xyz` 模式（Cloudflare 隐私保护） | 同 `123169.xyz` |
| 14 | yjz.hk | 2026-10-20 | yjz.hk（×2，10-19 日志） | WorkBuddy Helper | .hk 无 RDAP 数据 + Cloudflare A 记录，无归属线索 | 归属待定 |
| 15 | tsight.io | 2026-10-20 | tsight.io（×2，10-19 日志） | WorkBuddy Helper | 无归属线索，RDAP 无结论 | 归属待定 |
| 16 | nsvcs.net | 2026-10-20 | ingesteer.services-prod.（×1，10-19 日志） | firefox | AWS Route53 NS，无品牌指向（遥测摄入端点） | 归属待定 |
| 17 | ns1pcdn.net | 2026-10-20 | 9y49n2-m. / 5bav82-m. / 1xtsor1-m. / 1lmnv6z-m. / 1a4s4dv-m.（各 ×1，10-19 日志） | firefox | CSC 企业注册 + NS1；与 `mountaintoys.cn` 同批 CDN 模式但判据 2 不满足 | CDN 归属待定 |
| 18 | sitemana.com | 2026-10-20 | p.（10-19 日志 ×22 / 10-20 日志 ×8） | Google Chrome Helper | Squarespace + CloudFront A 记录，疑似广告验证但证据不足 | 广告验证端点——按 reject 上游类不落盘还是留 |
| 19 | featureassets.org | 2026-10-20 | featureassets.org（×1，10-19 日志） | firefox | MarkMonitor 企业域 + GCP A 记录，疑似追踪但证据不足 | 归属待定 |
| 20 | jd.com | 2026-10-21 | www.（×1，10-20 日志） | firefox | 判据 5：京东官网，大型公司宜建独立厂商文件，automation 不代建（`asus.com` 先例） | 是否建 `jd.yaml` |
| 21 | mi.com | 2026-10-21 | www.（×1，10-20 日志） | firefox | 判据 5：小米官网，同 `jd.com` | 是否建 `mi.yaml`（或并入既有厂商文件） |
| 22 | zoom.us | 2026-10-21 | zoom.us / st1.zoom.us（各 ×1，10-20 日志） | firefox | 判据 5：Zoom 品牌主域无厂商文件 | 是否建 `zoom.yaml` |
| 23 | qualcomm.cn | 2026-10-21 | www.（×1，10-20 日志） | firefox | 判据 5：高通中国官网，qualcomm 字面无厂商文件 | 建厂商文件还是归 `direct.yaml` 杂项 |
| 24 | cloudflare-cn.com | 2026-10-21 | www.（×1，10-20 日志） | firefox | 判据 5：Cloudflare 中国站，cloudflare 字面无厂商文件 | 建厂商文件还是归 proxy/direct 杂项 |
| 25 | sinaimg.cn | 2026-10-21 | tva1.（×1，10-20 日志） | firefox | 新浪图床 CDN；新浪系（`weibo.com`/`sina.com.cn`）全库未覆盖 | 宜建新浪系文件待定夺 |
| 26 | tcsdk.com | 2026-10-21 | tcsdk.com（×1，10-20 日志） | firefox | DNSPod 注册 + 腾讯 `ns-open` NS + EdgeOne 403，疑国内 SDK/广告端点，无品牌指向 | 归属待定 |
| 27 | pixpix.com | 2026-10-21 | www. / pixpix.com（各 ×1，10-20 日志） | firefox | GoDaddy + Cloudflare 无主端点（同 `123169.xyz` 模式） | 归属待定 |
| 28 | byte-test.com | 2026-10-21 | perfops.（×2，10-20 日志） | firefox | byte* 字面但注册模式（阿里云 + alidns NS，2021 注册）与字节惯例（MarkMonitor + bytedns）不符；CNAME `bplslb.com`（自有 bpldns NS）无定论 | 是否按判据 4 归字节系 |

> 登记日期说明：2026-10-17 之前挂起的历史项（第 1–4 行）按 changelog「连续第 N 轮遗留」反推取近似值；其余为首次挂起轮的 changelog 条目日期。
