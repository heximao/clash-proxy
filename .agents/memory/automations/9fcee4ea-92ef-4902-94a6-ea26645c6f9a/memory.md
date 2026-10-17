# 自动化执行记忆：昨日日志漏网之鱼归类

## 运行契约（每次必读）
- 任务：`@skill:fill-domains-from-log 处理昨日日志域名`，数据源 `~/.config/clash.meta/logs/<昨日日期前缀>`，先 cp 到 `log/clashx-meta-log/`。
- **Git 走 skill v2.2.0 的直提 main 流程**（2026-10-17 起取消分支制度，本地只保留 main）：`git fetch origin` → `git checkout main && git pull --rebase origin main` → 确认与远程双向 `0 0` → 在 main 上完成全部 yaml 改动与自检 → 更新 changelog → 显式列文件暂存（**清单须包含 `changelog.md`——2026-10-17 起已入库跟踪，变更随提交走**；**禁止 `git add -A` / `git add .`**）→ 提交前再 fetch 校验 `0 0` → `git commit`（中文信息）→ `git push origin main` → 确认 `0 0`。禁止任何形式强推；`reject.yaml` 不得暂存。
- **冲突处理（重要）**：skill 要求落盘前用 `AskUserQuestion` 由用户裁决归属（v2.1.0 起该步明确定义为 review 关卡），但自动化无人值守、禁止使用 AskUserQuestion。约定默认策略：**只补录「与已覆盖主域同厂商、语义无歧义的兄弟域」；其余存疑项一律不写入 yaml**，在 changelog 与运行结果里列出「待人工确认」清单。不要因为无法提问就大范围自行拍板。自动化运行即视为用户已授权按此默认策略执行 review 环节。
- 禁止编辑 `reject.yaml`；禁止查询/核对 reject.yaml；提交时确认 `reject.yaml` 未被暂存。
- 已判定「无主端点」的历史项（antpeak.com / hibchr.com / zorvian.com）不再提问、不重复收录。
- **每次先做日志差集检查**：对比 `~/.config/clash.meta/logs/` 与 `log/clashx-meta-log/`，凡源目录有而仓库 `log/` 无的日期一并补处理（自动化可能漏跑）。2026-10-11 即因此发现并补处理了 `2026-10-09_09-45-38`；2026-10-12 因此 cp 入库了当天的 `2026-10-12_09-38-05`。
- **Git 代理探测（2026-10-12 起）**：本机 git 配置 `http.proxy`/`https.proxy` = `http://127.0.0.1:7893`，但该端口**可能无监听**（ClashX 未运行时）。`git fetch` 报 `Failed to connect to 127.0.0.1 port 7893` 时，先实测直连（`curl --noproxy '*' -s -o /dev/null -w '%{http_code}' https://github.com`，返回 200 即可直连），然后统一用 **`git -c http.proxy= -c https.proxy= <cmd>`** 禁用代理执行。zsh 变量不做词分割，封装成函数 `gitx() { git -c http.proxy= -c https.proxy= "$@"; }`。RDAP/DoH 仍需 7893 代理。

## 运行历史
### 2026-10-17 12:41（处理 2026-10-16 两个目录 + 2026-10-17，第 11 次运行）—— 补录 3 项
- 数据源：`log/clashx-meta-log/2026-10-16_19-43-14`（昨日第二个目录，仓库从未入库）、`2026-10-16_08-15-39`（源端当日续写，新增 `15-16-40` / `15-16-55` / `18-36-09` 三个 core，已 `cp -R <src>/. <dst>/` 同步）、`2026-10-17_08-38-11`（今日，上轮未入库）。
- 提取：10-16_19-43-14 → match 102 + 裸 IP 2；oc-cn 24 + 裸 IP 1。10-17_08-38-11 → match 6；oc-cn 37 + 裸 IP 1。10-16_08-15-39 增量 → match 新增 2（`photon.codes`）。
- **补录 3 项（feature `4baebfb` → main merge `49934ad`，已推送，`0 0`）**：`bytedance.yaml`「字节系 CDN / 配置」+`doubaocdn.com`（Feishu 进程；`doubao.com` 锚点 + 同组 `volces.com`/`volccdn.com` 成对先例）、+`bytednsdoc.com`（Trae CN Helper；`byte*` 族）；`wechat.yaml`「微信主域」+`wechat.com`（WeChat 进程；品牌字面 + 锚点文件）。
- 待人工确认 10 项：`logitech.io`（第三轮）、`oceanengine.com`（第七轮）、`ntp.org.cn`、`yhgfb-cn-static.com`、`mdoelscope.ai`（仿冒域）、`applogcdn.com`（新）、`photon.codes`（新）、`temu.com`（新）、ad-tech 约 45 主域（归 reject 上游，禁核对故仅记录）。
- 整批跳过：antpeak/hibchr/zorvian（无主端点）、etahub/cloudflareinsights/clarity.ms（reject 上游）、`*.dotnxdomain.net`/`*.dashnxdomain.net`/`*.starnxdomain.net`（DNS 探针伪域名族，本轮新增过滤类别）、wpad、bilibili 系、微信系、mountaintoys.cn、jsdelivr.net；裸 IP `120.53.53.53` / `1.1.1.1` / `8.8.8.8`（均已覆盖）。
- 自检：跨文件重复 1（历史基线）、文件内 0，新增 0；`bytedance.yaml`(23) / `wechat.yaml`(7) 语法通过。
- **新增经验（判定）**：**「品牌 + 固定后缀」成对先例是第三条可复用补录路径** —— 同分组内 `volces.com` 与 `volccdn.com` 并存即确立「主域 + 同品牌 CDN 域」成组约定，故 `doubao.com` → `doubaocdn.com` 零歧义。排序：同标签 TLD 变体 ≥ 成对先例 ≥ 命名族 > 进程证据。
- **新增经验（过滤）**：Chrome 浏览产生的 ad-tech 主域（criteo/taboola/teads/moloco 等）与 NextDNS/DNSSEC 探针族（`*nxdomain.net`）会各自贡献 40+ / 60+ 条噪音，必须整批归入「不落盘 + 不计入待判」，否则真实信号被淹没。
- **新增经验（流程）**：**昨日可能有多个日期目录**（`08-15-39` 与 `19-43-14`），按日期前缀全取，不能只取第一个。

### 2026-10-16 12:41（处理 2026-10-15 / 2026-10-16 日志，第 10 次运行）—— 补录 2 项
- 数据源：`log/clashx-meta-log/2026-10-15_08-42-40`（昨日）与 `log/clashx-meta-log/2026-10-16_08-15-39`（今日）。**昨日目录 `diff -rq` 与仓库副本完全一致 → 零新增**（本日上午人工会话已处理完其全部增量）；**实质产出全部来自今日目录** —— 该目录上轮仅「cp 入库备用、未分析」，且源目录当日追加至 12:13（新增 3 个 core 日志），本轮 `cp -R <src>/. <dst>/` 同步后提取到增量。
- 提取：10-15 → match Match 域名 80 + 裸 IP 0；oc-cn-domain 域名 65 + 裸 IP 1（120.53.53.53 已覆盖）。10-16 → match Match 域名 4 + 裸 IP 1；oc-cn-domain 域名 34 + 裸 IP 1（同上）。
- **补录 2 项（提交 155bd0b → main merge 0fabf39，已推送，0 0）**：`direct.yaml`「证书验证」分组 +`DOMAIN-SUFFIX,digicert.cn`（源 `cacerts.digicert.cn`，进程 trustd，组内已有 `cacerts.digicert.com`：同品牌标签 + 同主机前缀 + 进程语义三重印证）；`apple.yaml`「Apple 推送 apsd」分组 +`IP-CIDR,17.57.0.147/32,no-resolve`（源 `17.57.0.147:443`，进程 iCloudNotificationAgent，同组已有 `17.57.145.0/24`）。
- 待人工确认 10 项（未落盘）：`mdoelscope.ai`（**本轮新增**，与已覆盖 `modelscope.ai` 仅字母转位之差，疑似错拼/仿冒域，**不是 TLD 变体**，不得补录）、`oceanengine.com`（第六轮遗留）、`logitechg.com`、`logitech.io`、`fastly-analytics.com`、`surfsharkdns.com`、`icanhazip.com`、`123169.xyz`、`999831.xyz`、`111666.best`。
- 整批跳过：bilibili 系 / 微信系 / WPS 系 / 商汤系 / 腾讯系（cloud.tencent.com、tencent-cloud.cn、gtimg.cn）/ mountaintoys.cn / myip.ipip.net / tuna / brew.sh / gnu.org / team-cymru.com / hm.baidu.com / 裸 IP 120.53.53.53 / monitor_browser。历史跳过：etahub.com、static.cloudflareinsights.com、antpeak/hibchr/zorvian。
- 自检：跨文件重复 1 项（settings.crashlytics.com 历史基线）、文件内 0，新增 0；direct.yaml(240)/apple.yaml(102) 语法通过。
- **新增经验（流程）**：**增量可能落在「今日」目录而非「昨日」目录**。差集带出的目录必须真正跑一遍提取，不能因为「所属日期不是昨日」就只 cp 不分析 —— 本轮唯一的实际产出就来自「今日」目录。
- **新增经验（环境）**：**`diff -rq` 会出现双向「Only in」**。ClashX Meta 会轮转/裁剪 core 日志：源目录已删的旧 core 仍留在仓库副本，源目录新生成的 core 仓库没有（本轮 10-16 目录中 `08-16-20`/`09-37-37` 仅存仓库、`12-10-27`/`12-13-14`/`12-13-41` 仅存源）。用 `cp -R <src>/. <dst>/` 只增不删即可保全证据；判「有无增量」以**源目录新增文件**为准。
- **新增经验（判定）**：**裸 IP 补录的判据不是「同主域」，而是「同厂商 IP 分组已存在」**。本轮 `17.57.0.147`（进程 iCloudNotificationAgent）能补入 apple.yaml，靠的是该文件已有「Apple 推送 apsd」分组（`17.57.145.0/24`）—— 进程 + 既有同厂商 IP 段分组的双重印证。

### 2026-10-15 15:29（处理 2026-10-14 / 2026-10-15 日志，第 9 次运行）—— 补录 3 项
- 数据源：`log/clashx-meta-log/2026-10-14_08-44-29`（昨日）、`log/clashx-meta-log/2026-10-15_08-42-40`（今日）。差集检查发现两者源目录有、仓库 `log/` 无 → 已 `cp -R` 入库，差集复核为空。
- 提取：10-14 → match Match 2 + 裸 IP 0；oc-cn-domain ~95 + 裸 IP 1（120.53.53.53 已覆盖）。10-15 → match Match 30 余（browserleaks DNS 探针随机子域、`*.u.fastly-analytics.com`、surfsharkdns、icanhazip）+ 裸 IP 0；oc-cn-domain ~43 + 裸 IP 1。
- **补录 3 项（提交 2cd9aeb → main merge d9dceb7，已推送，0 0）**：`proxy.yaml`「IP综合测试」+`DOMAIN-SUFFIX,browserleaks.net`、+`DOMAIN-SUFFIX,browserleaks.org`（凭组内既有 `browserleaks.com`，同标签多 TLD 兄弟域）；`wechat.yaml` 新增「微信小程序服务」分组 +`DOMAIN-SUFFIX,servicewechat.com`（源 `res.servicewechat.com`，进程 WeChatAppEx Helper，品牌在域名内，微信厂商文件已存在）。
- 待人工确认（未落盘）：logitechg.com（新，logioptionsplus_updater，Logitech 无已覆盖主域）、logitech.io（遗留）、fastly-analytics.com（与库内 fastly.net 非同品牌）、surfsharkdns.com、icanhazip.com、123169.xyz、999831.xyz（新）、111666.best、oceanengine.com（第四轮遗留）。browserleaks.net/.org 本轮解决、移出清单。
- 整批跳过：bilibili 系 / 微信系 / ipip.net（direct.yaml）/ mountaintoys.cn / 裸 IP 120.53.53.53；历史跳过：etahub.com、static.cloudflareinsights.com、antpeak/hibchr/zorvian。
- 自检：跨文件重复 1 项（settings.crashlytics.com 历史基线）、文件内 0，新增 0；proxy.yaml(847)/wechat.yaml(6) 语法通过。
- **新增经验（判定，重要）**：**按「品牌标签」而非「全域名」grep 全库**。前几轮只 grep `browserleaks.net` 得 NONE 即列待确认，漏掉 `.com` 锚点；改用标签 `browserleaks` grep 才发现 `proxy.yaml:147` 已有 `browserleaks.com` → `.net`/`.org` 成为零歧义 TLD 变体补录。**TLD 变体路径：同标签在库内有任一 TLD 被覆盖，其余 TLD 属可补录范围。**
- **新增经验（环境）**：git 代理 7893 本轮**可用**、GitHub 直连不通（curl 000），git 走默认代理配置即成功（同 10-13，与 10-12 相反）—— 印证「每轮必须现场双探测」。

### 2026-10-13 12:41（处理 2026-10-13 两个日志目录，第 7 次运行）—— 补录 3 项
- 数据源：`log/clashx-meta-log/2026-10-13_09-14-45` 与 `2026-10-13_11-06-26`（差集检查发现源目录有、仓库 `log/` 无 → 已 cp 入库，差集复核为空）；昨日 `2026-10-12_09-38-05` 与仓库副本 `diff -rq` 完全一致（源目录自上次 cp 后未增长）→ 上轮已处理，**零新增**。
- 提取：09-14-45 → match Match 21 + 裸 IP 0；oc-cn-domain 57 + 裸 IP 1（120.53.53.53 已覆盖）。11-06-26 → match Match 0；oc-cn-domain 5（微信系）+ 裸 IP 1。
- **补录 3 项（提交 98efe77 → main dec0f07，已推送）**：`tencent.yaml`「腾讯子域补充」+`DOMAIN-SUFFIX,time1.cloud.tencent.com`（`*.tencent.com` 精确子域安全区）；`bytedance.yaml` 新增「字节系 CDN / 配置」组 +`DOMAIN-SUFFIX,bytescm.com`、+`DOMAIN-SUFFIX,bytetcc.com`（源 `lf-cdn-tos.bytescm.com` / `lf3-config.bytetcc.com`，进程 Feishu；`byte*` 前缀同族先例 byteimg/bytetos/byteacctimg/bytedanceapi）。
- 待人工确认 12 项（未落盘）：asus.com 系 12 个主机名（华硕无任何现有覆盖，建 asus.yaml 属新增厂商文件）、bazaarvoice.com、fonts.net、logitech.io、codegang.top、romleyuan.com、oceanengine.com（连续第三轮遗留）、gd.gov.cn、gdzwfw.gov.cn、sz.gov.cn、ntp.org.cn、yhgfb-cn-static.com。
- 整批跳过：bilibili 系 / 微信系（weixinbridge+qpic+qlogo）/ baidu / mountaintoys.cn / 裸 IP 120.53.53.53 / monitor_browser / wpad。历史已判跳过：`akstat.io`、`go-mpulse.net`（changelog 早前条目已登记为「reject.yaml 上游已收录」）。
- 自检：跨文件重复 1 项（settings.crashlytics.com 历史基线）、文件内 0，新增 0；tencent.yaml(14)/bytedance.yaml(21) 语法通过。
- **新增经验（环境）**：**git 代理 7893 本轮恢复可用**（与 10-12 相反），GitHub 直连反而不通（curl 000），git 操作走默认代理配置即成功。**每轮开始前先探测 `nc -z 127.0.0.1 7893` 与 GitHub 直连，按结果择路**，不要沿用上一轮的结论。
- **新增经验（判定）**：`byte*` 前缀族的补录依据是「缩写/半品牌前缀 + 文件内同族先例」，同 `bdimg.com`（凭 `bdstatic.com`）路径；而 `yhgfb-cn-static.com` 虽同由 Feishu 发起，但域内无品牌标识且不符合任何既有命名族，仍留待人工确认 —— **进程证据只能加分，不能单独作为补录依据**。

### 2026-10-12 12:41（处理 2026-10-12 / 2026-10-11 日志，第 6 次运行）—— 补录 2 项
- 数据源：`log/clashx-meta-log/2026-10-12_09-38-05`（今日日志，差集检查发现源目录有、仓库 `log/` 无 → 已 cp 入库）；昨日 `2026-10-11_08-33-37` 复核**零新增**（该轮 10-11 已处理）。
- 提取：2026-10-12 → match Match 域名 24 + 裸 IP 0；oc-cn-domain 域名约 60 + 裸 IP 1（120.53.53.53 已覆盖）。2026-10-11 → match Match 12 + 裸 IP 0；oc-cn-domain 3 + 裸 IP 1，全部已覆盖。
- **补录 2 项（提交 ab077f0，已推送）**：`baidu.yaml` +`DOMAIN-SUFFIX,bdimg.com`（apps.bdimg.com，同厂商先例 bdstatic.com）；`microsoft.yaml`「第三方依赖服务」+`DOMAIN-SUFFIX,sentry-cdn.com`（browser.sentry-cdn.com，与 sentry.io 同厂商，同组已有 intercom.io+intercomcdn.com 的「厂商+CDN」成组约定）。
- 待人工确认 19 项（未落盘）：yipee.cc、webpushr.com、cyntelli.com、canvasjs.com、firstpromoter.com、jquery.com、yadro.ru、reincubate.com、adgeek.net、imei.org、imei.info、iunlocker.com、gtranslate.net、fontawesome.com、wrappixel.com、apeaksoft.com、i4.cn、volceapplog.com、oceanengine.com（上轮遗留）。
- 整批跳过：bilibili 系 / zhihu+zhimg / baidu+bdstatic / mountaintoys.cn / 裸 IP 120.53.53.53 / monitor_browser。历史跳过：static.cloudflareinsights.com（reject 上游）、antpeak/hibchr/zorvian（无主端点）。
- 自检：跨文件重复 1 项（settings.crashlytics.com 历史基线）、文件内 0，新增 0；baidu.yaml(3)/microsoft.yaml(71) 语法通过。
- Git：feature ab077f0 → main `--no-ff` 合并 11291cb → push（c444b06..11291cb）→ `0  0` → 切回 feature。
- **新增经验（环境）**：**git 代理 7893 本次失效**（无监听），`git fetch` 报 connect 失败；实测 GitHub **直连可达**，改用 `git -c http.proxy= -c https.proxy=` 禁用代理完成全部 git 操作。zsh 变量不做词分割，封装成函数 `gitx() { git -c http.proxy= -c https.proxy= "$@"; }` 使用。**git 操作前先探测代理可用性，不可用即直连**。
- **新增经验（判定）**：**「同厂商兄弟域」优先看目标文件内的成组约定**。microsoft.yaml「第三方依赖服务」组已有 `intercom.io` + `intercomcdn.com`，故 `sentry.io` + `sentry-cdn.com` 属同一约定下的零歧义补录；`volceapplog.com` 虽疑为火山引擎（repo 内 volces.com/volccdn.com 先例），但**发起进程为 firefox、无字节系进程证据**，按「需外部知识定厂商」留待人工确认 —— 进程证据缺失时应降级处理。

### 2026-10-11 12:41（处理 2026-10-10 日志，第 5 次运行）—— 昨日日志零新增
- 数据源：`log/clashx-meta-log/2026-10-10_10-25-01`（该日志本日上午已被两次运行处理过，本次为当日再次触发）。提取：match Match 域名 9 + 裸 IP 0；oc-cn-domain 域名 86 + 裸 IP 1（120.53.53.53，已覆盖）。
- **昨日日志逐项复核后零新增**：9 个 match Match 全部已覆盖（contrib.rocks→github.yaml；deepwiki/railway/zeabur/onorca.dev/macked.site/turingfraud.net→proxy.yaml；cdn.ripperhe.com→direct.yaml 精确 DOMAIN）或属历史跳过（etahub.com / cloudflareinsights.com→reject 上游）；oc-cn-domain 86 项主域全部已覆盖（weixin.com、hellogithub.com、zvo.cn、bobtranslate.com、gitcode.com、copilot.tencent.com、lightai.cloud.tencent.com 等）。
- **差集检查发现 5 个源有仓库无的历史目录**：`2026-10-01_09-40-31`、`2026-10-01_10-09-27`、`2026-10-01_10-32-57`、`2026-10-03_08-54-53`、`2026-10-04_10-20-36`。已 cp 入库（差集复核为空）并提取。经 changelog 交叉核验，10-01/10-04 内容此前已处理（仅缺 log 副本，属早期运行未 cp 的复制缺口）；10-03 无对应 changelog 条目。
- 补录 1 条（提交 b6e4c20，已推送）：`bytedance.yaml` 新增「字节系 API」分组 +`DOMAIN-SUFFIX,bytedanceapi.com`（源 10-03 日志 `imagex.bytedanceapi.com`，Trae CN Helper 8 次；同厂商+品牌在域名内+进程三重证据）。
- 待人工确认 19 项（未落盘）：hisball.com、qiyukf.com、127.net、centralnic.com、gdzwfw.gov.cn、gd.gov.cn、sz.gov.cn、browserleaks.net、fastly-analytics.com、surfsharkdns.com、icanhazip.com、sibforms.com、trendshift.io、iconscout.com、nocobase.com、schemastore.org、111666.best、123169.xyz、oceanengine.com（上轮遗留）。
- 自检：跨文件重复 1 项（settings.crashlytics.com 历史基线）、文件内 0 项，新增 0；bytedance.yaml payload 19 条语法通过。
- Git：feature 提交 b6e4c20 → main `--no-ff` 合并 11a2315 → push（6d4ec95..11a2315）→ `0  0` → 切回 feature。
- 新增经验：**差集 ≠ 漏跑**，必须用 changelog 交叉核验（对得上历史落点即属复制缺口，不重做）；**提交信息里的数字先算准再写**（本次写「13 个」实际 19 项，已推送无法改）。

### 2026-10-11（处理 2026-10-10 日志 + 补处理 2026-10-09，第 4 次运行）
- 数据源：`log/clashx-meta-log/2026-10-10_10-25-01`（昨日）+ `log/clashx-meta-log/2026-10-09_09-45-38`（差集检查发现从未处理）。
- 10-10：match Match 域名 9 + 裸 IP 0；oc-cn-domain 域名约 80 + 裸 IP 1（120.53.53.53，已覆盖）；归并主域后 22 个待判主域。10-09：match Match 2 + 裸 IP 0；oc-cn-domain 约 33 + 裸 IP 1（已覆盖）。
- 覆盖整批跳过：bilibili 系、微信系、mountaintoys.cn、裸 IP 120.53.53.53。
- 跳过（历史已判）：etahub.com、cloudflareinsights.com（均 reject 上游收录）、cdn.ripperhe.com（direct.yaml 精确 DOMAIN 已覆盖）。
- 补录 1 组 2 条（提交 af26864，已推送）：`tencent.yaml` 新增「腾讯子域补充」组 +copilot.tencent.com、+lightai.cloud.tencent.com（均为 `*.tencent.com` 精确子域，归属零歧义）。
- 待人工确认 12 项（未落盘）：contrib.rocks、deepwiki.com、macked.site、railway.com、zeabur.com、onorca.dev、hellogithub.com、zvo.cn、bobtranslate.com、gitcode.com、turingfraud.net、vsassets.io。
- 自检：跨文件重复 2 项（历史基线）、文件内 0 项，新增 0；tencent.yaml 语法通过（payload 13 条）。
- 提交前远程有 reject.yaml 自动合并 f9eee7c，工作区干净，直接 `git pull --rebase` 快进。
- 新增经验：**批量 grep 命中 ≠ 主域已覆盖**。`direct.yaml` 的 `DOMAIN,cdn.ripperhe.com` 是精确主机规则，不代表覆盖 `ripperhe.com` 主域，故 `bobtranslate.com` 不满足「同厂商兄弟域」补录条件。判定前必须回看命中行的规则类型。另：`*.tencent.com` 子域是零歧义补录安全区；`vsassets.io` / `gitcode.com` 这类需外部知识定厂商的，一律留待人工确认。

### 2026-10-09（处理 2026-10-08 日志，第 2 次运行）
- 数据源：`log/clashx-meta-log/2026-10-08_09-27-03`。提取后：match Match 域名 9 + 裸 IP 0；oc-cn-domain 域名约 100 + 裸 IP 1；归并主域后 15 个待判主域。
- 覆盖整批跳过：bilibili 系、微信系、mountaintoys.cn → direct.yaml、tencent.com/gtimg.com → tencent.yaml；裸 IP 120.53.53.53 已覆盖。
- 跳过（历史已判 reject 上游收录）：etahub.com（changelog 2026-09-30 已记录），本次日志再现仍跳过。
- 补录 2 项（提交 4299b51，已推送）：`pornhub.yaml` 的 xvideos 组 +xvideos-cdn.com、+xvideos.net（与已覆盖 xvideos.com 同厂商，沿用该文件「站点主域+同名 CDN 域」成组约定）。
- 待人工确认（未落盘）：mmcdn.com、agego.com、tracesof.net；上期遗留 ethyca.com/proigor.com/kejitt.top/vzuu.com/static.cloudflareinsights.com 本次未再现。
- 自检：跨文件重复 2 项（历史基线）、文件内 0 项，新增 0；pornhub.yaml 语法通过。
- 提交前远程有 reject.yaml 自动合并 be9033d，已 stash→pull --rebase→stash pop 同步。
- 新增经验：**判断「同厂商无歧义兄弟域」时先看目标文件既有分组约定**。pornhub.yaml 一直是「成人站点主域 + 其同名 CDN 域（phncdn/ypncdn/rdtcdn/t8cdn）」成组收录，故 xvideos-cdn.com / xvideos.net 随 xvideos.com 入同组属零歧义补录；而 mmcdn.com 名称与 xvideos 无关联，即便同属成人视频 CDN 也不满足「无歧义」，仍留待人工确认——不要因语义相近就扩充补录范围。

### 2026-10-08（处理 2026-10-07 日志，首次运行）
- 数据源：`log/clashx-meta-log/2026-10-07_10-26-33`。提取后：match Match 域名 10 + 裸 IP 4；oc-cn-domain 域名约 100 + 裸 IP 1；归并主域后 26 个待判主域。
- 覆盖整批跳过：bilibili 系、微信系、jsdelivr.net/mountaintoys.cn/zhihu.com/aikobo.cn → direct.yaml、baidu.com → baidu.yaml；5 个裸 IP 全部已覆盖。
- 补录 3 项（提交 7ace9e1，已推送）：`direct.yaml` +zhimg.com、`baidu.yaml` +bdstatic.com、`tencent.yaml` +gtimg.com。
- 待人工确认（未落盘）：ethyca.com、etahub.com、proigor.com、kejitt.top、vzuu.com、static.cloudflareinsights.com。
- 自检：跨文件重复 2 项（历史基线，与 reject 无关的两条：空占位 paypal/steam、settings.crashlytics.com direct/google），新增 0；三文件 yaml.safe_load 通过。
- 环境坑：`git fetch` 首报 SSL_ERROR_SYSCALL（瞬时故障），重试即成功（counts 0 0）；无需改 proxy 配置。
