# 更新记录

## 2026-10-26 漏网之鱼归类：yupao.com 1 域补录 direct.yaml（automation 轮）

- **数据来源**：`log/clashx-meta-log/2026-10-25_08-40-46`（cp 只读复制自 `~/.config/clash.meta/logs/` 昨日唯一文件夹，4 个日志文件；`log/clashx-meta-log/` 无上轮遗留存量，cp 前确认目标侧无同名防套娃）。
- **提取量**（结构化脚本，过滤伪域名 3、探针 0、私有 IP 0）：候选 173（`match Match` 7 / `oc-cn-domain` 166），归并主域 30、公网裸 IP 0；skip-list 命中 `skip` 1 行（1 主域 `etahub.com` reject 上游）、`manual` 3 行（3 主域均已登记 issues-domain.md 表）。
- **查重**：30 主域全走 stdin 喂 `check_coverage.py` → COVERED 29 / UNCOVERED 1（BRAND-ANCHOR 0）；唯一未覆盖 `yupao.com`。
- **补录明细**（1 域、1 文件、既有组追加，依据留痕）：
  - **`direct.yaml` 既有「国内平台 / CDN 杂项」组追加 1 域**：`yupao.com`（玉拍文玩平台主域；2026-10-25 轮 changelog 已记录 `yupaowang.com` HTTP 301 重定向 yupao.com + DoH NS alidns + 阿里云北京 IP 确认国内；判据 2 同厂商兄弟域 + 文件内既有成组约定；`oc-cn-domain` 命中确认 CN 直连可达）。
- **未收录及原因**：无新无法判定项；3 个 manual-review 命中（`checktrustworthiness.com` / `featureassets.org` / `nsvcs.net`）均已在 skip-list `manual` + issues-domain.md 表中，不重复登记。
- **整批跳过**（skip-list `skip` 命中 1 行审计照抄）：`etahub.com`（4 次 firefox，reject 上游已收录）。
- **待人工确认**（manual-review 3 行照抄，均已在 issues-domain.md 表中不重复登记）：`checktrustworthiness.com`（global-iuni.×2 curl，#16）、`featureassets.org`（×2 firefox，已挂起）、`nsvcs.net`（ingesteer.services-prod.×1 firefox，已挂起）。
- **自检结果**：`find_duplicates.py` 业务文件间重复保持基线 1 条（`settings.crashlytics.com` direct/google），**本次新引入 0**——`yupao.com` 在 DUPLICATES.md 中 0 出现（DUPLICATES.md 与 HEAD 一致）；`duplicates.json` +3 行（`yupao.com` 作为 direct.yaml 新规则入解析数据，非重复）。`yaml.safe_load` direct.yaml 通过（payload 300，较上轮 299 +1 吻合）；1 条新规则经 `check_coverage.py` 复核 COVERED（covered 1 / uncovered 0）。
- **skip-list**：本轮无新增/移除项。
- **AGENTS.md 同步延后**：本轮 skip-list 无新增项，AGENTS.md「已裁决结论」清单无待同步内容。
- Git：main 提交 `<hash>` → push → 同步 `0 0`（hash 回填按既有纪律顺延下轮）。

## 2026-10-25 漏网之鱼归类：国内数据/CDN 5 域、海外视频调研 3 域、网易系 1 域补录，Sigmob 广告 skip、checktrustworthiness 留人工（automation 轮）

- **数据来源**：`log/clashx-meta-log/2026-10-24_08-18-26`（cp 只读复制自 `~/.config/clash.meta/logs/` 昨日唯一文件夹，4 个日志文件；`log/clashx-meta-log/` 无上轮遗留存量，cp 前确认目标侧无同名防套娃）。
- **提取量**（结构化脚本，过滤伪域名 4、探针 0、私有 IP 0）：候选 151（`match Match` 22 / `oc-cn-domain` 129），归并主域 70、公网裸 IP 0；skip-list 命中 `skip` 10 行（6 主域）、`manual` 6 行（5 主域）。
- **查重**：70 主域全走 stdin 喂 `check_coverage.py` → COVERED 57 / UNCOVERED 12（BRAND-ANCHOR 3，均属 `163.com` 同标签 TLD 变体锚点 netease-music.yaml）。
- **补录明细**（9 域、3 文件、1 个新分组 + 2 处既有组追加，依据逐条留痕）：
  - **`direct.yaml` 既有「国内平台 / CDN 杂项」组追加 5 域**：`growingio.com`（DoH NS vip3/vip4.alidns.com 国内 + A 117.50.x 国内 IP，GrowingIO 国内用户行为分析平台，api-os 端点）、`yupaowang.com`（DoH NS alidns + A CNAME prod-mse-external-lb → 123.56/39.97 阿里云北京 + HTTP 301 重定向 yupao.com 玉拍文玩平台，国内）、`cdqlkj.cn`（`.cn` 按用户 10-22 裁定 + DoH NS alidns + A CNAME prod-mse-external-lb.yupaowang.com，与 yupaowang 同系统同款 NS）、`zgzpsjz.com`（DoH NS alidns + A 39.107.57.143 阿里云北京，staticscdn 静态 CDN 端点）、`giocdn.com`（DoH NS dns17/18.hichina.com 阿里万网国内注册 + assets 子域 CNAME giocdn.com.edgekey.net Akamai CDN，国内注册商实证）。
  - **`proxy.yaml` 新组「漏网之鱼（2026-10-25 补录）海外杂项」3 域**：`wistia.com`（Wistia 海外视频托管平台，Obsidian Helper 访问 fast/embed-ssl/distillery/pipedream 端点）、`wistia.net`（判据 1 同品牌 `wistia.com` TLD 变体，同批补录）、`qualtrics.com`（Qualtrics 海外调研/体验管理平台 SAP 收购，siteintercept 网站拦截调研端点 + zncvyyewtkgdypjbg-riotgames 哈希定制前缀，非纯广告追踪）。
  - **`netease-music.yaml` 既有「网易门户 / CDN」组追加 1 域**：`321fenx.com`（DoH NS ns1-8.nease.net + ns1-6.166.com 网易自有 + A 42.186.x 网易 IP 段，同 `127.net` 先例 2026-10-21 判据；nstool. 子域 DNS 工具端点）。
- **不补录**：`163.com`（BRAND-ANCHOR 锚点 netease-music.yaml，命中 `www.163.com` 已被 `DOMAIN,www.163.com`@netease-music.yaml:27 精确覆盖——判据 8 精确主机规则 ≠ 主域覆盖，回看命中行规则类型该命中已覆盖；2026-10-21 轮故意用精确主机而非主域，本轮不补 `DOMAIN-SUFFIX,163.com`）。
- **未收录及原因**：
  - `sigmob.cn` → 广告/追踪类整批不落盘（Sigmob 移动广告聚合平台 dc./tm. SDK 端点，DoH NS alidns 国内但属广告 SDK；先例 `mmstat.com`），skip-list `skip`。
  - `checktrustworthiness.com` → 证据不足留人工（DoH NS AWS Route53 + 主域无 A 记录 + `global-iuni.` 子域 CNAME alb-*.us-east-1.alb.aliyuncs.com AWS US-East ALB + checktrustworthiness 追踪/信誉检查语义无品牌实锤），三处留痕 skip-list `manual` + `issues-domain.md` #16 + 本段。
- **整批跳过**（skip-list `skip` 命中 10 行审计照抄）：`mmstat.com`（12，阿里妈妈统计）、`jpush.cn`（8 含 ali-stats/config/user/gd-stats 四子域，reject 上游）、`antpeak.com`（2，无主端点）、`zorvian.com`（2，无主端点）、`hibchr.com`（2 含 plus.，无主端点）、`cloudflareinsights.com`（1，reject 上游）。
- **待人工确认**（manual-review 6 行照抄，前 5 项已在 issues-domain.md 表中不重复登记）：`byte-test.com`（perfops.×6 firefox）、`pixpix.com`（×4 + www.×1 firefox）、`featureassets.org`（×2 firefox）、`nsvcs.net`（ingesteer.services-prod.×2 firefox）、`mdoelscope.ai`（×1 firefox，仿冒待用户确认转 skip）；**本轮新挂起** `checktrustworthiness.com`（global-iuni.×2，登记 #16）。
- **自检结果**：`find_duplicates.py` 业务文件间重复保持基线 1 条（`settings.crashlytics.com` direct/google），**本次新引入 0**——9 个新域名在 DUPLICATES.md 中 0 出现（DUPLICATES.md 与 HEAD 一致）；`duplicates.json` +27 行（全量数据随规则数增加）。`yaml.safe_load` 三文件通过（payload：direct 299 / proxy 890 / netease-music 27，均与上轮基线 + 本次新增数吻合）；9 条新规则经 `check_coverage.py` 复核全部 COVERED（covered 9 / uncovered 0）。
- **AGENTS.md 同步延后**：本轮 skip-list 新增 2 项（`sigmob.cn` `skip` + `checktrustworthiness.com` `manual`），AGENTS.md「已裁决结论」清单同步按纪律延后至交互式会话（automation 轮写受保护文件必被 BLOCKED）。
- Git：main 提交 `012ea5d` → push → 同步 `0 0`。

## 2026-10-24 漏网之鱼归类：金山系 5 域、智谱 AI 2 域、长桥 2 域、友盟、腾讯直播 SDK 等 16 域补录，穿山甲广告系 4 域不落盘（automation 轮）

- **数据来源**：`log/clashx-meta-log/2026-10-23_08-33-17`（cp 只读复制自 `~/.config/clash.meta/logs/` 昨日唯一文件夹，4 个日志文件；`log/clashx-meta-log/` 无上轮遗留存量，cp 前确认目标侧无同名防套娃）。
- **提取量**（结构化脚本，过滤伪域名 14、探针 0、私有 IP 0）：候选 247（`match Match` 4 / `oc-cn-domain` 243），归并主域 61、公网裸 IP 0；skip-list 命中 `skip` 10 行、`manual` 1 行。
- **查重**：61 主域全走 stdin 喂 `check_coverage.py` → COVERED 40 / UNCOVERED 21（BRAND-ANCHOR 0）；21 未覆盖主域逐一检索 changelog 历史均无往期判定记录（新候选）。
- **补录明细**（16 域、5 文件、3 个新分组 + 3 处既有组追加，依据逐条留痕）：
  - **金山系 5 域 → `direct.yaml` 既有「金山办公 / WPS」组追加**：`kdocs.cn`（金山文档，WPS 在线文档，判据 2 同厂商兄弟域——direct 金山组已有 wps.cn/wpscdn.cn/qwps.cn/ksosoft.com/ksord.com；.cn 按用户 10-22 裁定）、`docer.com`（WPS 稻壳内容市场，命中子域 wps-docer-property.file.docer.com 自证 WPS 归属）、`ksyun.com`（金山云，ks3-cn-beijing 对象存储端点）、`ksyuncs.com`（金山云存储域变体，同轮 ksyun 成组先例）、`wpsdns.com`（WPS DNS，ksopush 推送端点，wps 前缀命名族）。
  - **国内导购 / 数据服务 5 域 → `direct.yaml` 新组「国内电商导购 / 数据服务」**：`smzdm.com`（什么值得买，国内知名导购平台，RDAP eName 2010 老牌注册 + DNSV5 NS 国内实证，用户 10-22 裁定「高度归属国内 → direct、不新建厂商文件」；22 子域 analytics-api 等高频）、`zdmimg.com`（smzdm 图片 CDN：zdm+img 命名 + RDAP eName/DNSV5 与 smzdm.com 完全同款，判据 3 主域+同品牌衍生域成对）、`hzchengdun.com`（杭州诚盾，RDAP 阿里云 HiChina + ALIBABADNS NS + A 记录 59.82.x 国内）、`soboten.com`（DNSPod 注册 + DoH CNAME 阿里云高防 aliyunddos1020.com，高度国内；soboten 与智齿 sobot.com 标签不同不适用判据 1）、`sensorsdata.cn`（神策数据，国内用户行为分析 SDK，.cn 按用户 10-22 裁定）。
  - `umeng.com` → `alibaba.yaml` 新组「友盟+ / Umeng」：友盟+，RDAP 阿里云注册 + NS 全 ALIBABADNS（阿里收购系实证），alibaba.yaml 已有独立子品牌先例（taobao/tmall/amap/alipay），判据 2 同厂商兄弟域 + 文件内成组约定；cnlogs/aspect-upush/errnewlog 等统计推送端点为功能性 SDK 非纯广告。
  - `tlivesdk.com` → `tencent.yaml` 既有「腾讯云」组追加：腾讯云 MLVB（移动直播）SDK 拉流域名（mlvbdc 子域 + 哈希前缀推拉流模式为腾讯云直播典型特征 + DNSPod 腾讯系注册 + 2024 新注册带 transfer/update prohibited 腾讯批量特征），tencent.yaml 已有腾讯云独立主域先例（myqcloud/qcloud/tencentcloud）。
  - **长桥证券 2 域 → `hk-broker.yaml` 既有「券商」组追加**：`longbridgeapp.com`（api-status 长桥 App 服务端，判据 2 同厂商兄弟域——文件已有 longbridge.com/.cn/longbridgewhale）、`pbkrs.com`（pub. 端点，bkrs 命名族与文件内 lbkrs.com/wbkrs.com/wbrks.com 同词根 + DoH CNAME 阿里云香港 ALB（长桥基建特征），判据 3 成对先例）。
  - **智谱 AI 2 域 → `direct-ai.yaml` 新组「智谱 AI / Z.ai」**：`bigmodel.cn`（智谱开放平台，.cn 国内大模型）、`z.ai`（智谱 AI 国际品牌 Z.AI（北京智谱华章，SEHK: 2513），zcode.z.ai 为 ZCode AI coding agent 官网（Wikipedia/官网实证）；oc-cn-domain 命中即 OpenClash 判定 CN 直连可达 + firefox 16 次访问成功，直连实证归 direct-ai；DoH CNAME 阿里云新加坡 ALB 仅为托管位置）。
- **未收录及原因**（广告/追踪类整批不落盘纪律，skip-list `skip` 4 项，先例 pangle-ads.com）：
  - `pangolin-sdk-toutiao.com` / `pangolin-sdk-toutiao1.com` → 字节穿山甲广告联盟 SDK（api-access 端点），skip-list `skip`。
  - `pglstatp-toutiao.com` → 穿山甲视频素材 CDN（pgl=pangolin；sf*-fe-tos/p26-be-pack-sign 端点；anti-AD GitHub issue #494 收录请求 + Netify 关联 TouTiao 应用双重佐证），skip-list `skip`。
  - `adhuanxiao.com` → 广告 SDK 疑似（ad 前缀 + sdk. 端点 + 火山引擎云托管 180.184.x，注册商新网与字节惯例不符判第三方广告公司，主体不明），skip-list `skip`。
- **整批跳过**（skip-list `skip` 命中 10 行审计照抄）：`antpeak.com`（14，无主端点）、`zorvian.com`（14，无主端点）、`hibchr.com`（12 含 plus.，无主端点）、`sg.mmstat.com`（3，阿里妈妈统计）、`static.cloudflareinsights.com`（2，reject 上游）、`www.clarity.ms`（2，reject 上游）、`www.codarka.com`（2，无主端点）、`ali-stats.jpush.cn`（1，reject 上游）、`this-url-does-not-exist-<uuid>.invalid`（1，RFC 2606 保留 TLD 探针）。
- **待人工确认**：`mdoelscope.ai`（manual-review 照抄：仿冒域 5 次 firefox，已在 issues-domain.md 表中不重复登记，待用户确认转 skip）；`wdfl.co` → **本轮新挂起**（manual：.co 无 RDAP 数据 + r. 子域 CNAME CloudFront 短链 + 1 次命中无进程，无归属线索，三处留痕 issues-domain.md #15 + skip-list `manual` + 本段）。
- **自检结果**：`find_duplicates.py` 业务文件间重复保持基线 1 条（`settings.crashlytics.com` direct/google），**本次新引入 0**——16 个新域名在 DUPLICATES.md 中 0 出现，DUPLICATES.md 与 HEAD 一致（duplicates.json 全量数据随规则数更新 +48 行）；报告口径 68 跨文件 / 26 文件内系未跟踪归档目录 `followups/` 旧 yaml 副本 + `config.yaml` 策略组名噪声（23）+ 基线 1 叠加，均非本轮引入。`yaml.safe_load` 五文件通过（payload：direct 294 / alibaba 14 / tencent 27 / hk-broker 12 / direct-ai 14，均与上轮基线 + 本次新增数吻合）；16 条新规则经 `check_coverage.py` 复核全部 COVERED（covered 16 / uncovered 0）。
- **AGENTS.md 同步延后**：本轮 skip-list 新增 5 项（pangolin-sdk-toutiao.com / pangolin-sdk-toutiao1.com / pglstatp-toutiao.com / adhuanxiao.com `skip` + wdfl.co `manual`），AGENTS.md「已裁决结论」清单同步按纪律延后至交互式会话（automation 轮写受保护文件必被 BLOCKED）。
- Git：main 提交 `b44637d` → push → 同步 `0 0`。

## 2026-10-23 漏网之鱼归类：东方财富系、银联、奇虎 360、字节电商 CDN 等 24 条补录（automation 轮）

- **数据来源**：`log/clashx-meta-log/2026-10-22_09-17-18`（cp 只读复制自 `~/.config/clash.meta/logs/` 昨日唯一文件夹，4 个日志文件；`log/clashx-meta-log/` 无上轮遗留存量，cp 前确认目标侧无同名防套娃）。
- **提取量**（结构化脚本，过滤伪域名 0、探针 0、私有 IP 0）：候选 177（`match Match` 16 / `oc-cn-domain` 161），归并主域 55、公网裸 IP 0；skip-list 命中 `skip` 21 行、`manual` 2 行。
- **查重**：55 主域全走 stdin 喂 `check_coverage.py` → COVERED 30 / UNCOVERED 25（BRAND-ANCHOR 0）；25 主域逐一检索 changelog 历史均无往期判定记录（新候选）。
- **补录明细**（24 域、4 文件、4 个新分组 + 2 处既有组追加，依据逐条留痕）：
  - **东方财富系 7 域 → `direct.yaml` 新组「东方财富 / 东方财富证券」**：`eastmoney.com`（RDAP 阿里云 2002 老牌注册 + alidns NS，国内财经门户/证券，本轮 32 子域 securities/mobappconfig 等）、`18.cn`（DoH NS vip3/vip4.alidns.com 与 eastmoney.com 完全一致，东方财富证券官方主域，tradegateway/tradenoticemix 交易端点）、`eastmoneysec.com`（DoH NS alidns 同款 + east money sec 字面）、`dfcfw.com`（东方财富网缩写，gbfek/gbres 端点）、`dfcfs.cn`（dfcf* 命名族 + DoH NS alidns + .cn 按用户 10-22 裁定归 direct）、`dflcs.cn`（df* 命名族 + appserverlisttx 子域 tx/mix 后缀同 18.cn 交易端点命名模式 + DoH NS alidns）、`emhudong.cn`（em* 命名族与同轮 30+ eastmoney emXXX 端点一致 + DoH NS alidns + gbapi A 记录全国内云厂商 + .cn 裁定；官网标题空，归组以命名族与同款 NS 为据）。
  - **银联 2 域 → `direct.yaml` 新组「银联 UnionPay」**：`95516.com`（95516 = 银联官方热线，appcashier 收银台 / base / open / switch / tysdk 支付 SDK 端点）、`cup.com.cn`（China UnionPay 缩写官方域名，antifraud / pay / bill 端点）。
  - **奇虎 360 3 域 → `direct.yaml` 新组「奇虎 360」**：`360.cn`（360 品牌字面）、`qhimg.com`（Qihoo Image，jspassport.ssl 通行证）、`qhres2.com`（Qihoo Resources，s.ssl 静态资源）——用户 2026-10-22 裁定不新建厂商文件、高度归属国内归 direct。
  - **`direct.yaml` 既有组追加 5 域**：`qibingdaojia.com` →「国内招聘 / 生活服务」组（首页标题实证「奇兵到家-全国家具,卫浴,智能锁,门窗,晾衣架-家居安装维修服务平台」+ RDAP 阿里云，wxapipreview 小程序预览端点 45 次）；`mihuashi.com`（首页标题「米画师 - 带给你自由、高效、专业的美术工作体验」+ RDAP 阿里云 2015 注册）、`bmcx.com`（RDAP 阿里云 HiChina 2005 老站 + alidns，便民查询网 wannianrili 万年日历）、`szxhdz.com`（官网标题「深圳市星火电子工程公司」+ RDAP 厦门易名注册 + DNSPod NS + 子域 CNAME 华为云 WAF）、`wxgateway.com`（RDAP DNSPod 注册 + dnsv5 NS + report-online.sh A 记录上海电信，tcsdk.com 同模式先例）→「国内平台 / CDN 杂项」组。
  - **字节系 4 域 → `bytedance.yaml`**：`toutiao.com` → 主组 douyin.com 后追加（今日头条主域，zhanzhang 站长端点，判据 5 品牌字面 + 厂商文件已落盘）；`ecombdimg.com`、`bytegoofy.com`、`bytelb.net` →「字节系 CDN / 配置」组追加——`ecombdimg.com`（抖店官方文档 op.jinritemai.com 实证 `.ecombdimg.com/obj/ecom-shop` 商品图片 URL + ICP 备案「电商静态资源服务」+ RDAP 阿里云注册，抖音电商图片静态资源域，DoH CNAME 白山云 bsgslb.com 调度国内 IP；判据 5）、`bytegoofy.com`（byte 命名族判据 4 + lf1-cdn-tos Feishu CDN 模式同 larkoffice / feishucdn 先例）、`bytelb.net`（byte 命名族判据 4 + direct-dualstack.eeft-lb-v3.lf 子域 + Lark Helper 进程，字节负载均衡端点）。
  - **海外杂项 2 域 → `proxy.yaml` 新组「漏网之鱼（2026-10-23 补录）海外杂项」**：`ctfassets.net`（Contentful Assets CDN，海外 headless CMS 标准资源域 images.ctfassets.net）、`statsigapi.net`（Statsig 实验平台 API 端点域，海外 SaaS）。
  - `unsloth.ai` → `proxy-ai.yaml`「AI 服务」组追加：Unsloth 开源 LLM 微调框架文档站（docs. 子域，WebKit 进程），同 muse.ai / mistral.ai / midjourney.com 先例。
- **未收录及原因**：`codarka.com` → 无主端点不归类（RDAP NameCheap 2025-05-12 新注册 + Cloudflare NS + www NXDOMAIN + 首页空响应，1 次命中无进程指向），同 antpeak.com / hibchr.com / zorvian.com 模式，skip-list `skip`。
- **整批跳过**（skip-list `skip` 命中 21 行审计照抄）：`cloudflareinsights.com`（2 子域 20 行，reject 上游）、`statcounter.com`（1 子域 8 行，网站访问统计）、`antpeak.com`（6 行，无主端点已裁决）、`clarity.ms`（4 子域 12 行，reject 上游）、`zorvian.com`（6 行，无主端点）、`hibchr.com`（2 子域 7 行，无主端点）、`etahub.com`（4 行，reject 上游）、`mmstat.com`（4 行，阿里妈妈统计）、`taboola.com`（2 子域 4 行，内容推荐广告）、`jpush.cn`（6 子域 6 行，reject 上游）。
- **待人工确认**（manual-review 2 行照抄，均已在 issues-domain.md 表中不重复登记）：`freloop.com`（×5：curl ×2 疑为上轮 automation RDAP 自查流量回写进 10-22 日志、其余 3 次同上轮 firefox 模式，连续第 2 轮）、`sitemana.com`（p. ×2 Google Chrome Helper，连续第 4 轮）。
- **自检结果**：`find_duplicates.py` 业务文件间重复保持基线 1 条（`settings.crashlytics.com` direct/google），**本次新引入 0**——本轮 24 个新域名在 DUPLICATES.md 中 0 出现（DUPLICATES.md 与 HEAD 一致）；报告口径 68 跨文件 / 26 文件内系未跟踪归档目录 `followups/` 旧 yaml 副本（67 跨 + 3 内）+ `config.yaml` 策略组名噪声（23）+ 基线 1 叠加，均非本轮引入。`yaml.safe_load` 四文件通过（payload 条数：direct 284 / bytedance 30 / proxy 887 / proxy-ai 38，均与上轮基线 + 本次新增数吻合）；24 条新规则经 `check_coverage.py` 复核全部 COVERED（covered 24 / uncovered 0）。
- **AGENTS.md 同步延后**：本轮 skip-list 新增 1 项（codarka.com `skip`），AGENTS.md「已裁决结论」清单同步按纪律延后至交互式会话（automation 轮写受保护文件必被 BLOCKED）。
- Git：main 提交 `<hash>` → push → 同步 `0 0`（hash 回填按既有纪律顺延下轮）。

## 2026-10-22 漏网之鱼归类：拼多多、揽岳 Lexmount、支付宝/蚂蚁、Apple AMPAE 等 14 条补录（automation 轮）

- **数据来源**：`log/clashx-meta-log/2026-10-21_09-17-30`（cp 只读复制自 `~/.config/clash.meta/logs/` 昨日唯一文件夹，4 个日志文件；`log/clashx-meta-log/` 无上轮遗留存量，cp 前确认目标侧无同名防套娃）。
- **提取量**（结构化脚本，过滤伪域名 6、探针 0、私有 IP 0）：候选 114（`match Match` 43 / `oc-cn-domain` 71），归并主域 67、公网裸 IP 0；skip-list 命中 `skip` 13 行、`manual` 4 行。
- **查重**：67 主域全走 stdin 喂 `check_coverage.py` → COVERED 49 / UNCOVERED 18（含 BRAND-ANCHOR 2）。
- **补录明细**（14 条新增 + 1 条扩域替换、6 文件、5 个新分组，依据逐条留痕）：
  - **拼多多 2 域 → `direct.yaml` 新组「拼多多」**：`pinduoduo.com`（abtk/apm-a/ta/th/xg 等 9 子域 oc 命中，国内电商巨头，用户 2026-10-22 裁定「高度归属国内 → direct.yaml」）、`pddpic.com`（pdd 品牌字面 + 与 pinduoduo.com 同批成组，img/avatar 子域图片 CDN）。
  - **揽岳智能 2 域 → `direct.yaml` 新组「揽岳智能 Lexmount」**：`lexmount.com` + `lexmount.cn`（`browser.lexmount.com` firefox 访问；直连首页实证「Lexmount | AI Browser Infrastructure」+ © 深圳市揽岳智能科技有限公司 + 粤ICP备2025476131号，LexBrowser AI 云浏览器平台，高度归属国内；.cn 主域由官网 JS 显式 zh 分流（browser.lexmount.cn），判据 1 同标签 TLD 零歧义补录；RDAP 阿里云 HiChina 注册）。
  - **支付宝 / 蚂蚁 2 域 → `alibaba.yaml` 新组「支付宝 / 蚂蚁集团」**：`alipay.com`（判据 5 alipay 品牌字面 + alibaba.yaml 阿里系文件已落盘；mdap. 端点 oc 命中；config.yaml「阿里巴巴」策略组默认 DIRECT）、`alipayobjects.com`（gw. 静态资源，RDAP NS1-4.ALIPAY.COM 蚂蚁自有 NS 实证）。
  - **阿里 CDN 2 域 → `alibaba.yaml`「CDN / 云」组追加**：`aliapp.org`（RDAP CSC 企业注册 + ns3-5.aliyun.com 阿里云 NS 实证，cdn.ynuf. 安全 JS CDN）、`alibabachengdun.com`（alibaba 品牌字面判据 5 + RDAP NS1/2.ALIBABADNS.CN/COM 阿里自有 DNS 实证，mum. 阿里云成都端点）。
  - `ampaeservices.com` → `apple.yaml` 新组「AMPAE Services」：RDAP COM LAUDE 品牌注册商 + A-D.NS.APPLE.COM 苹果自有 NS，DoH CNAME 链 `afs.ampaeservices.com → afs.ampservices.v.aaplimg.com → 17.57.10.x`（aaplimg.com Apple CDN 域 + AS714 IP 段）三重实证，Apple 媒体服务端点（afs. 无进程 oc 命中）。
  - `muse.ai` → `proxy-ai.yaml`「AI 服务」组追加：首页标题「Muse — Your Personal AI Agent」实证，海外 AI 服务需代理（firefox 31 次）。
  - `convex.dev` → `proxy.yaml`「漏网之鱼（2026-10-21 补录）海外杂项」组 convex.cloud 旁追加：判据 1 BRAND-ANCHOR `convex.cloud`@proxy.yaml 同标签 TLD 变体（上轮即以 convex.dev 官网标题实证补录 convex.cloud，本轮官网本体现身）。
  - `cdn-go.cn` → `direct.yaml`「国内平台 / CDN 杂项」组追加：用户 2026-10-22 裁定「.cn 全部归 direct.yaml」（curl 1 次 oc 命中）。
  - **RDAP 注册局端点 2 条 → `direct.yaml` 新组「域名查询 / RDAP」**：`DOMAIN,rdap.nic.download`、`DOMAIN,rdap.registry.cloud`（Agent 自用查询端点，AGENTS.md 已裁决先例 rdap.org/verisign.com/crt.sh → RDAP 组；精确主机避免兜注册局主域，同 rdap.centralnic.com 先例，curl 进程自证）。
  - **`google.yaml` 扩域替换 1 条**：`DOMAIN-SUFFIX,a.run.app` → `DOMAIN-SUFFIX,run.app`（判据 1 BRAND-ANCHOR a.run.app@google.yaml；run.app 全域属 Google Cloud Run，本轮命中部署 URL `bded8a3c6ae-1-1053047382554.us-central1.run.app`；原 a.run.app 覆盖的 antigravity 更新器子域为新规则子集，语义不变）。
- **未收录及原因**：
  - `freloop.com` → **新挂起待人工**（manual）：NameCheap 注册（2025-05）+ Cloudflare NS + 首页 429 / 直连 SSL 失败，firefox 访问主域 3 次无产品指向——同 pixpix.com 模式，三处留痕（issues-domain.md #14 + skip-list `manual` + 本段）。
  - `fbthirdpartypixel.com` → 广告/追踪类整批不落盘（Meta Pixel 第三方追踪域 metadotcom. 端点，先例 clarity.ms / mmstat.com），skip-list `skip`。
  - `sc-static.net` → 广告/追踪类整批不落盘（Snap Pixel 静态资源域，firefox 6 次），skip-list `skip`。
  - `this-url-does-not-exist-<uuid>.invalid` → RFC 2606 保留 TLD 连通性探针，伪域名不归类；skip-list 新增 `invalid` 后缀条目（后缀匹配覆盖未来 UUID 变体）。
- **整批跳过**（skip-list `skip` 命中 13 行审计照抄）：`clarity.ms`（4 子域 30 行，reject 上游）、`statcounter.com`（2 子域 30 行，网站访问统计）、`mmstat.com`（6，阿里妈妈统计）、`taboola.com`（3 子域 10 行，内容推荐广告）、`antpeak.com` / `zorvian.com`（各 1，无主端点已裁决）、`cloudflareinsights.com`（1，reject 上游）。
- **待人工确认**（manual-review 4 行照抄，前 3 项已在 issues-domain.md 表中不重复登记）：`sitemana.com`（p. ×8 Google Chrome Helper，连续第 3 轮）、`pixpix.com`（×5 firefox + www. ×1 curl，连续第 2 轮）、`byte-test.com`（perfops. ×6 firefox，连续第 2 轮）、`freloop.com`（×3 firefox，**本轮新登记**）。
- **自检结果**：`find_duplicates.py` 业务文件间重复基线 1 条（`settings.crashlytics.com` direct/google）不变，**本次新引入 0**——DUPLICATES.md 与 HEAD 逐字节一致；报告口径 68 跨文件 / 26 文件内系未跟踪归档目录 `followups/` 旧 yaml 副本（67 跨文件 + 3 文件内）+ `config.yaml` 策略组名噪声（23）+ 基线 1 叠加所致，均非本轮引入、非业务规则重复。`yaml.safe_load` 六文件通过（direct 267 / alibaba 13 / apple 103 / google 97 / proxy 885 / proxy-ai 37 payload）；14 条新增 + 1 条替换经 `check_coverage.py` 复核全部 COVERED（nic.download / registry.cloud 为 DOMAIN 精确主机命中，判据 8）。
- **AGENTS.md 同步延后**：本轮 skip-list 新增 4 项（fbthirdpartypixel.com / sc-static.net / invalid `skip` + freloop.com `manual`），AGENTS.md「已裁决结论」清单同步按纪律延后至交互式会话（automation 轮写受保护文件必被 BLOCKED）。
- Git：main 提交 `<hash>` → push → 同步 `0 0`（hash 回填按既有纪律顺延下轮）。

## 2026-10-22 fill-domains-from-log skill v2.9.0：issues-domain.md 只保留待判定域名，定案记录收敛到 changelog（main 直接提交，交互会话）

- **触发**：用户要求——流程上 issues 只保留待处理的 domain，记录写到 changelog 就可以。
- **skill v2.9.0 改动**（`.agents/skills/fill-domains-from-log/SKILL.md`）：
  - 第 6b 节「文件定位」明确：`issues-domain.md` **只保留待判定域名**——定案去向与依据只写 `changelog.md`，本表不留定案记录段；行被移除即净出，表始终等于「当前待判定集合」。
  - front matter description、第 13 节核对项同步（定案记录只写 changelog，表不留定案段）。
- **issues-domain.md 整改**：移除 10-22 裁定轮在表尾留的「2026-10-22 定案记录」段——15 项定案去向与依据在 changelog「2026-10-22 issues-domain 用户裁定」条目已完整留痕，无信息损失；表现在为纯待判定表（13 项，与 skip-list `manual` 段一致）。
- **AGENTS.md 同步**（工作区改动，**未提交**）：blockquote 补「表只保留待判定域名，定案记录以 changelog 为准」clause；文件内用户未完成的 SPEC/ 重构继续不打包。
- **MEMORY.md 同步**（随本轮提交）：目录结构节与 Skill 流程裁决节补「表只保留待判定域名，定案记录只写 changelog」。
- **自检**：`grep -c '^| [0-9]' issues-domain.md` = 13 = skip-list manual 段条目数；全文已无「定案记录」段残留；无 yaml 规则改动，不涉及 find_duplicates / safe_load。
- Git：main 提交 `<hash>` → push → 同步 `0 0`。

## 2026-10-22 issues-domain 用户裁定：15 项落盘（direct 9 / proxy 6），13 项继续挂起（交互轮）

- **触发**：用户对 `issues-domain.md` 待人工判定表给出裁定——**`.cn` 全部加入 `direct.yaml`；agent 判断高度归属国内的也加入 `direct.yaml`；不需要新建厂商文件**（海外知名公司杂项归 `proxy.yaml`）；无国内实证且无海外公司归属的继续挂起，不强行归类。
- **查重**：15 个待落盘主域全部走 `check_coverage.py` stdin → UNCOVERED 15（BRAND-ANCHOR 仅 `ntp.org.cn` 命中 `0.openwrt.pool.ntp.org`/`ubuntu.pool.ntp.org` 两个 NTP pool 锚点，均为 pool 子域而非 `ntp.org.cn` 本身，不构成覆盖）。
- **补录明细**（15 域、2 文件、5 个新分组）：
  - **`direct.yaml` 9 条**：新组「NTP 时间服务（2026-10-22 漏网之鱼补录）」`ntp.org.cn`（.cn，国内 NTP 池 `cn./edu.` 子域，Lark Helper；直连组已有 OpenWrt NTP 先例）；新组「国内电商 / 厂商官网（2026-10-22 漏网之鱼补录）」`jd.com`（京东）、`mi.com`（小米）、`qualcomm.cn`（高通中国官网，.cn）、`cloudflare-cn.com`（Cloudflare 中国站）；新组「国内平台 / CDN 杂项（2026-10-22 漏网之鱼补录）」`oceanengine.com`（字节旗下巨量引擎）、`sinaimg.cn`（新浪图床，.cn）、`yhgfb-cn-static.com`（Feishu 进程 CDN，`lf-rc1.` 子域）、`tcsdk.com`（DNSPod 注册 + 腾讯 `ns-open` NS + EdgeOne，国内 SDK/CDN 端点）。
  - **`proxy.yaml` 6 条**：新组「Logitech（2026-10-22 漏网之鱼补录）」`logitech.io` / `logitech.com` / `logitechg.com`（罗技 Options+ 遥测与更新端点，海外公司不新建厂商）；新组「漏网之鱼（2026-10-22 补录）海外杂项」`zoom.us`（Zoom 主域 + `st1.` 子域）、`temu.com`（跨境电商）、`photon.codes`（无国内实证，按海外杂项兜底）。
- **继续挂起 13 项**（不满足「.cn / 高度国内」，亦无海外公司归属，按「不强行归类」纪律留在 `issues-domain.md`）：`applogcdn.com`、`mdoelscope.ai`（仿冒域，AGENTS.md 已裁决不补录，待用户确认转 skip）、`123169.xyz`、`111666.best`、`999831.xyz`（Cloudflare 隐私保护三连，firefox 高频，疑用户自建服务）、`yjz.hk`、`tsight.io`、`nsvcs.net`、`ns1pcdn.net`、`sitemana.com`、`featureassets.org`、`pixpix.com`、`byte-test.com`（阿里云/alidns 国内倾向但非「高度国内」实证）。`mdoelscope.ai` 用户本轮未表态，按原状留表。
- **三处同步**（skill 第 6b 节定案闭环）：`issues-domain.md` 移除 15 行（28 → 13，表尾新增「2026-10-22 定案记录」段）；skip-list `manual` 移除同 15 项（28 → 13）并补裁定注释；AGENTS.md「已裁决结论」补裁定规则行 + 挂起清单刷新为 13 项（**工作区改动，未提交**——文件内有用户未完成的 SPEC/ 重构，不打包）；`.agents/memory/MEMORY.md` 同款同步（随本轮提交）。
- **自检结果**：`find_duplicates.py` 业务文件间重复保持基线 1 条（`settings.crashlytics.com` direct/google），本次新引入 0；15 条新规则经 `check_coverage.py` 复核全部 COVERED；`yaml.safe_load` 校验通过（direct.yaml 260 / proxy.yaml 884 条 payload）。
- Git：main 提交 `<hash>` → push → 同步 `0 0`。

## 2026-10-22 fill-domains-from-log skill v2.8.0：证据不足项登记 issues-domain.md 待人工表，既有 28 项 manual 挂起项种子导入（main 直接提交，交互会话）

- **触发**：用户要求——对于证据不足无法判定归属的域名，写入 `issues-domain.md` 用表格列出，留用户判定。
- **skill v2.8.0 改动**（`.agents/skills/fill-domains-from-log/SKILL.md`）：
  - **新增第 6b 节「issues-domain.md 登记（证据不足项的最终去向）」**：第 6 步 RDAP/DoH 查询后仍无法判定归属的主域（含判据 5「无锚点厂商文件」的大型公司主域，如 `jd.com` / `mi.com` / `zoom.us`——automation 不代建厂商文件），在 changelog「待人工」+ skip-list `manual` 之外**必须写入仓库根 `issues-domain.md` 待人工表**（7 列：`# | 域名 | 登记日期 | 命中子域（次数） | 进程 | 已查证据 | 存疑点 / 待定夺`）；已在表不重复登记；按登记日期升序（长期挂起项保持可见）；命中数据必须取日志实证不得凭记忆；**行只许因用户定案移除**（补录 yaml 或裁决不收录两种闭环），agent 不得自行删行；`skip` 类已裁决项（无主端点/广告追踪/reject 上游/伪域名）不进表；automation 可直接追加（非受保护文件）。
  - 全文同步：处理流程框图（第 6 步后接 6b 分支）、核心原则 1（三处留痕）、第 0 节对齐检查（增 issues-domain.md ↔ skip-list manual 一致性）、第 2 节（manual-review 段与 skip-list 维护入口补表格视图）、第 5 节（裁决规则两条 bullet）、第 6 节（末两条 bullet）、第 10 节（暂存清单补 issues-domain.md）、第 13 节（changelog 模板 + 新增 issues-domain.md 核对项，收尾改四件）、第 14 节（新增两条硬性约束）。
- **issues-domain.md 种子导入**（新文件，已入 git 跟踪）：既有 skip-list `manual` 全集 **28 项**一次性建表——2026-10-11~10-15 历史挂起 4 项（`oceanengine.com`、`ntp.org.cn`、`yhgfb-cn-static.com`、`logitech.io`，按 changelog「连续第 N 轮遗留」反推登记日期）、10-17 轮 4 项（`applogcdn.com`、`photon.codes`、`temu.com`、`mdoelscope.ai`）、10-18 轮 1 项（`logitechg.com`）、10-20 轮 10 项（`logitech.com`、`123169.xyz`、`111666.best`、`999831.xyz`、`yjz.hk`、`tsight.io`、`nsvcs.net`、`ns1pcdn.net`、`sitemana.com`、`featureassets.org`）、10-21 轮 9 项（`jd.com`、`mi.com`、`zoom.us`、`qualcomm.cn`、`cloudflare-cn.com`、`sinaimg.cn`、`tcsdk.com`、`pixpix.com`、`byte-test.com`）。**命中子域/次数/进程全部从 `log/.archive/` 已处理日志实测 grep 补全**（10-17/10-18/10-19/10-20 四批日志），非凭记忆填写。
- **AGENTS.md 同步**（交互会话动作，已改工作区）：目录结构树补 `issues-domain.md` 行；「已裁决结论」blockquote 后补 `manual` 项表格视图说明。**注意：AGENTS.md 工作区另有用户未提交的 SPEC/ 重构改动（§3 followups / §6 SPEC / §13 git 指针，2026-10-19 晚引入），本轮未纳入提交**，留待用户自行处置；`.agents/memory/2026-10-19.md` 的 DNS 治理未提交改动同样未动。
- **extract 脚本 README 同步**：manual-review 段与 skip-list.txt 节补 `issues-domain.md` 表格视图注记。
- **自检**：issues-domain.md 28 行与 skip-list `manual` 段逐条比对一致（28 = 28）；`git status` 确认本轮仅暂存 5 个文件（SKILL.md / issues-domain.md / extract README / changelog.md / 当日 memory），`reject.yaml` 未暂存；无 yaml 规则改动，不涉及 find_duplicates / safe_load。
- Git：main 提交 `<hash>` → push → 同步 `0 0`。

## 2026-10-21 漏网之鱼归类：腾讯云系 9 域、网易 CDN、海外杂项等补录 42 规则（automation 轮）

- **数据来源**：`log/clashx-meta-log/2026-10-20_08-40-01`（cp 只读复制自 `~/.config/clash.meta/logs/`，昨日 1 个文件夹 5 个日志文件，含 2 个 core 日志——10-20 当天内核重启一次；`log/clashx-meta-log/` 无上轮遗留存量，cp 后 `diff -rq` 校验与源一致）。
- **提取量**（结构化脚本，已过滤伪域名 4、探针 0、私有 IP 0）：候选 190（`match Match` 93 / `oc-cn-domain` 97），归并主域 92、公网裸 IP 0；skip-list 命中 `skip` 20 行、`manual` 7 行（本轮前口径）。
- **查重**：92 主域全走 stdin 喂 `check_coverage.py` → COVERED 31 / UNCOVERED 61（含 BRAND-ANCHOR 19）。
- **并发冲突处理**：本轮查重后，用户交互轮提交 `e2a6302`（13:51，`openai.yaml` 补录 `sora.com`）与本轮独立裁决重叠；本轮已撤销自己的 Sora 组追加、保留用户版本，`sora.com` 计入已覆盖不重复补录。
- **补录明细**（42 条规则、12 文件、13 个分组，依据逐条留痕）：
  - **腾讯云系 6 域 → `tencent.yaml`「腾讯云」组追加**：`qcloud.com`（判据 4 qcloud* 命名族、`myqcloud.com` 先例；RDAP MarkMonitor 上海 + NS ns1-4.qq.com 实证）、`qcloudimg.com`（判据 4；RDAP MarkMonitor 上海 + ns-open.qq.com）、`tencentcloud.com`（判据 5 tencent 字面；RDAP ns-open.qq.com + DoH CNAME 腾讯 EdgeOne）、`tencent-cloud.com`（判据 1 BRAND-ANCHOR `tencent-cloud.cn`@tencent.yaml）、`tencentcs.cn`（判据 5；腾讯云 COS 官方存储桶域，RDAP 404 系 .cn 无数据）、`cloudcachetci.com`（RDAP MarkMonitor + ns-open.qq.com 腾讯实证，腾讯云国际 CDN 缓存域，同批 `cloudcache.tencent-cloud.com`/`cloudcache.tencentcs.cn` 场景）。
  - **腾讯账号 / 内部办公 3 条 → `tencent.yaml` 新组**：`DOMAIN,api.account.tencent.com` + `DOMAIN,oauth2.account.tencent.com`（判据 6 `*.tencent.com` 精确子域零歧义安全区）、`woa.com`（RDAP MarkMonitor 上海 + ns-open.qq.com 腾讯实证，WoA 腾讯内部办公域；`yehe.woa.com` firefox 访问）。
  - `bytecdn.com` → `bytedance.yaml`「字节系 CDN / 配置」组：判据 4 byte* 命名族；DoH CNAME 链实证 `lf-arcosite.bytecdn.com.bytedns3.com`（字节自有 DNS 调度域）→ queniubg.com 海外节点。
  - **网易 2 域 → `netease-music.yaml` 新组「网易门户 / CDN」**：`DOMAIN,www.163.com`（判据 1 BRAND-ANCHOR `music.163.com`/`api.iplay.163.com` 同标签 + 判据 8 精确主机规则不覆盖主域）、`127.net`（RDAP NS ns1-8.nease.net/166.com 网易自有 NS 实证，注册 1998；`necaptcha.nosdn.127.net` = 网易易盾验证码 + 网易对象存储 CDN）。
  - `xhscdn.com` → `xhs.yaml` 新组「小红书 CDN」：判据 5 xhs 品牌字面 + `xhs.yaml`（小红书）已落盘；`fe-static.xhscdn.com` 小红书前端静态资源。
  - **`proxy.yaml` 16 条**：`yahoo.co.jp`（判据 1 BRAND-ANCHOR yahoo.com@proxy.yaml:769，追加锚点旁）、`nintendo.co.jp`（判据 1 nintendo.com/net 锚点旁）、`1password.com`（「密码管理器」组 bitwarden.com/net 先例）、`kali.download`（「Linux 社区」组，Kali 官方下载域；RDAP Gandi + Cloudflare 海外）、`gitlab.com`（「开发者工具」组，Git 托管海外服务，schemastore.org 类比）、`net.coffee`（「网络检测工具」组追加——HTTP 首页标题「IP 查询 - IP分流测试」实证 + 哈希子域模式同 `dnscheck.tools`，10-19 DNS 泄露排查场景延续；RDAP Spaceship + Cloudflare，2025-07 新注册）、新组「漏网之鱼（2026-10-21 补录）海外杂项」10 域：`bbc.com`（国际媒体，同文件 nyt.com 先例）、`shopify.com`、`noon.com`、`takealot.com`、`mlstatic.com`（海外电商，直连不稳定）、`producthunt.com`、`signal.org`、`apify.com`（海外知名服务兜底）、`convex.cloud`（Convex 后端平台部署域 `wry-manatee-359.convex.cloud`，convex.dev 官网标题实证）、`mupdf.com`（MuPDF 官网，python3.12 = PyMuPDF 更新检查，RDAP Gandi 海外）。
  - **`direct.yaml` 4 条**：`sony.jp`（判据 1 BRAND-ANCHOR sony.com@direct.yaml:132 锚点旁，索尼日本官网可直连）、新组「域名 / IP 查询」：`ip.cn`（DoH 解析与 ip138.com 共享 138.113.62.x 段 + oc 类别国内直达；RDAP 404 系 .cn）、`ip138.com`（国内老牌 IP 查询站，RDAP eName + DNSPod dnsv4 国内实证）、新组「域名查询 / RDAP」：`DOMAIN,rdap.centralnic.com`（AGENTS.md 明文 Agent 自用查询端点 → RDAP 组 + curl(3) 进程自证 + 同组 rdap.org/verisign.com/crt.sh 成组先例；精确主机避免兜 CentralNic 注册商主域）。
  - **`proxy-ai.yaml` 2 条 → 「AI 服务」组追加**：`mistral.ai`（Mistral AI 法国模型公司，RDAP Cloudflare 留痕）、`midjourney.com`（Midjourney AI 绘图）——需代理 AI 服务无厂商专属文件，按 proxy-ai 兜底。
  - **`streaming.yaml` 2 条**：`nflxext.com`（netflix 组追加，判据 2 同厂商兄弟域——`assets.nflxext.com` Netflix 静态资源）、`crunchyroll.com`（新组，Crunchyroll 动漫流媒体，同文件流媒体主题）。
  - `cdninstagram.com` → `meta.yaml`：判据 5 instagram 品牌字面 + `instagram.com` 已落盘（Instagram CDN `static.cdninstagram.com`）。
  - **`crypto.yaml` 2 条**：`binance.info`（判据 1 BRAND-ANCHOR binance.com@crypto.yaml:5 锚点旁）、`crypto.com`（Crypto.com 交易所，同文件 binance/okx/bybit 交易所先例）。
  - `stripe.network` → `microsoft.yaml`：判据 1 BRAND-ANCHOR stripe.com@microsoft.yaml:87 锚点旁（`m.stripe.network` Stripe 移动端点，CodeBuddy Studio Helper 进程）。
  - `naver.com` → `line.yaml` 新组「Naver」：判据 1 BRAND-ANCHOR line.naver.jp@line.yaml:5（naver 标签同 TLD 变体；Naver 门户与 LINE 同属 Naver 集团）。
- **未收录及原因**：
  - COVERED 31 项整批跳过（规则集先于本地 yaml 匹配，不代表规则缺失）：`bilibili.yaml` 5（hdslb/bilibili/bilivideo.com/bilivideo.cn/biliimg）、`wechat.yaml` 5（qlogo.cn/qpic.cn/weixinbridge/weixin/wechat.com）、`steam.yaml`（steampowered.com）、`baidu.yaml`（baidu.com）、`direct.yaml` 8（rdap.org/digicert.cn/mountaintoys.cn/verisign.com/arin.net/apnic.net/iana.org/ipip.net）、`proxy.yaml` 4（dnscheck.tools/icanhazip.com/surfsharkdns.com/addr.tools）、`openstreetmap.org`、`publicinterestregistry.org`、`deepseek.com`（direct-ai）、`wise.com`（us-payment）、`twitchcdn.net`（streaming）、`servicewechat.com`（wechat）。
  - 广告/追踪类 9 主域不落盘（AGENTS.md「整批不落盘」纪律，只记录不判断、不核对 reject.yaml；已入 skip-list `skip` 模式）：`creativecdn.com`、`criteo.com`、`everesttech.net`、`mathtag.com`、`mookie1.com`、`teads.tv`、`iprsoftwaremedia.com`（进程均 Chrome Helper）、`pangle-ads.com`（字节穿山甲国际广告平台 analytics 端点，Chrome）、`mmstat.com`（友盟+/阿里妈妈网页统计——RDAP 阿里云注册 + SOA alibabadns.com 阿里系实证，但统计追踪场景按纪律不落业务文件）。
  - `sora.com`：用户交互轮 `e2a6302` 已补录 `openai.yaml`，本轮去重。
  - `byte-test.com`：byte* 字面但注册模式（阿里云 + alidns NS，2021 注册）与字节域名惯例（MarkMonitor + bytedns）不符，`perfops.byte-test.com` CNAME `bplslb.com`（自有 bpldns NS，2022 注册）无定论——不强行按判据 4 归类，留人工。
- **待人工确认**（本轮新增 9 项，均入 skip-list `manual`）：`jd.com`（京东官网，大型公司宜建独立厂商文件，automation 不代建——`asus.com` 先例）、`mi.com`（小米官网，同前）、`zoom.us`（Zoom 品牌主域无厂商文件）、`qualcomm.cn`（高通中国，qualcomm 字面无厂商文件，判据 5）、`cloudflare-cn.com`（Cloudflare 中国站，cloudflare 字面无厂商文件，判据 5）、`sinaimg.cn`（新浪图床，新浪系 weibo.com/sina.com.cn 全库未覆盖，宜建新浪系文件待用户定夺）、`tcsdk.com`（DNSPod 注册 + 腾讯 ns-open NS + EdgeOne 403，疑国内 SDK/广告端点，无品牌指向）、`pixpix.com`（GoDaddy + Cloudflare 无主端点，firefox 访问 www. 主站，同 `123169.xyz` 模式）、`byte-test.com`（见上）。既有挂起本轮命中 7 行照抄：`edu.ntp.org.cn`/`cn.ntp.org.cn`（Lark Helper ×14/×8）、`p.sitemana.com`（Chrome ×8）、`i.111666.best`（firefox ×6）、`api.123169.xyz`、`updates.optionsplus.logitechg.com`、`cf.999831.xyz`。
- **自检结果**：`find_duplicates.py` 跨文件重复 68 条中 67 条涉及未跟踪 `followups/active/` 存档副本（含 followups 内 OpenAI/AI/Spotify/弃用等存档 yaml 与业务 yaml 天然重合），业务文件间重复保持基线 1 条（`settings.crashlytics.com` direct/google），**本次新引入 0 项**（发现并修复 1 项并发引入的 intra-file 重复：openai.yaml `sora.com` 与用户提交 `e2a6302` 重叠，已撤销本轮追加）；文件内重复 26 条 = `config.yaml` 策略组/DNS 值噪声 23 + `followups/active` 存档 3，业务文件 0。42 条新规则经 `check_coverage.py` 复核全部 COVERED。`yaml.safe_load` 校验通过（payload 条数）：tencent 26 / bytedance 26 / netease-music 26 / xhs 2 / proxy 878 / direct 251 / proxy-ai 36 / streaming 13 / meta 28 / crypto 28 / microsoft 72 / line 21；openai.yaml 13（未编辑，HEAD 状态）。skip-list 消化验证：同日志重跑候选 190→170、manual 18 行、skip 29 行，数字自洽。
- **AGENTS.md 同步延后**：本轮新增 18 条已裁决项（9 skip + 9 manual）已落 skip-list + changelog；AGENTS.md「已裁决结论」清单为受保护文件，同步留待交互式会话（第 0 节对齐检查）。
- Git：main 提交 `<hash>` → push → 同步 `0 0`。

## 2026-10-21 openai.yaml：补录 sora.com（交互轮）

- **触发**：用户直接指定将 `sora.com` 添加到 `openai.yaml`。
- **查重**：`check_coverage.py sora.com` → UNCOVERED（BRAND-ANCHOR 0），全库无既有覆盖。
- **补录明细**：`sora.com` → `openai.yaml`，规则 `DOMAIN-SUFFIX,sora.com`，紧邻 `chatgpt.com` / `openai.com` 产品主域之后：Sora 为 OpenAI 官方视频生成产品，同文件已有两产品主域成组先例（判据 5——品牌归属明确且厂商文件已落盘，产品域与厂商主域同文件维护）。
- **自检结果**：`find_duplicates.py` 跨文件重复 68 条中 67 条均涉及未跟踪本地目录 `followups/active/2026/2026-10/`（任务存档旧配置 yaml 副本，与业务 yaml 天然大面积重合），业务文件间重复保持基线 1 条（`settings.crashlytics.com` direct/google），**本次新引入 0 项**（`sora.com` 不在报告中）；文件内重复 26 条 = `config.yaml` 策略组/DNS 值噪声 23 + `followups/active` 存档副本 3，业务文件 0。`openai.yaml` payload 13 条，`yaml.safe_load` 通过。
- **Git 操作链**：`git fetch origin` + `origin/main...HEAD` 双向 `0 0` → 显式暂存 `openai.yaml` + `changelog.md` + `scripts/find-duplicates/DUPLICATES.md` + `scripts/find-duplicates/duplicates.json` → commit → push → 复核 `0 0`。

## 2026-10-20 漏网之鱼归类：DNS 泄露排查工具链、字节系、RDAP 等补录 19 域（automation 轮）

- **数据来源**：`log/clashx-meta-log/2026-10-19_09-47-52`、`2026-10-19_22-53-45`、`2026-10-19_23-59-44`（cp 只读复制自 `~/.config/clash.meta/logs/`，昨日 3 个文件夹共 14 个日志文件；`log/clashx-meta-log/` 无上轮遗留存量）。背景：用户 10-19 晚 22:40–23:50 进行 DNS 泄露排查（详见 `.agents/memory/2026-10-19.md`），产生大量网络检测站流量，为本轮候选主力。
- **提取量**（结构化脚本，已过滤伪域名 43、探针 0、私有 IP 0）：候选 670（`match Match` 566 / `oc-cn-domain` 104），归并主域 62 + 公网裸 IP 3（`120.53.53.53`、`1.1.1.1`、`8.8.8.8`）；skip-list 命中 `skip` 10 行（映射 `clarity.ms` 6 子域、`cloudflareinsights.com`、`antpeak.com`/`hibchr.com`/`zorvian.com`）、`manual` 4 行（`logitech.io`、`logitechg.com`、`ntp.org.cn`×2）。
- **查重**：62 主域 + 3 IP 全走 stdin 喂 `check_coverage.py` → COVERED 26（含 3 IP）/ UNCOVERED 39 / BRAND-ANCHOR 0。
- **补录明细**（19 域、4 文件、8 个分组）：
  - `douyin.com` → `bytedance.yaml`「ByteDance / 字节跳动」主组：判据 5——抖音为字节核心品牌、厂商文件已落盘，子域 `tos-d-x-lf.douyin.com` 由 Trae CN Helper（字节系进程）访问，双佐证。
  - `bytedancevod.com` → `bytedance.yaml`「字节系 CDN / 配置」组（组头日期合并至 10-20）：判据 4——bytedance 品牌字面 + Trae CN Helper 进程，同组既有 `bytescm.com`/`bytednsdoc.com` 先例。
  - `marketbeat.com` → `fin-media.yaml`「财经媒体」组：美股市场数据/资讯站，Chrome 访问 `www.marketbeat.com` 18 次，同组既有 `seekingalpha.com`/`investing.com`。
  - 网络检测工具 9 域 → `proxy.yaml`「漏网之鱼（2026-10-20 补录）网络检测工具」组（海外服务、国内直连不稳，均为 DNS 泄露排查场景）：`icanhazip.com`（Cloudflare IP echo，110 次）、`ipleak.net`（DNS/IP 泄露测试，300+ 检测子域）、`dnscheck.tools`（DNSSEC 检测，80+ 子域）、`surfsharkdns.com`（Surfshark VPN DNS 测试探针）、`addr.tools`（IP 查询）、`ip-api.com`（IP 地理查询，edns 检测子域）；`brokendnssec.net`、`every1dns.net`、`encryptedsni.com` 三域 RDAP 实证同一所有者（同 NS `carl/cruz.ns.cloudflare.com`、同 2018-08 注册期，`is-doh/is-dot/is-cf.help` 命名），为配套 DNS 检测探针组。
  - `openstreetmap.org` → `proxy.yaml`「漏网之鱼（2026-10-20 补录）地图瓦片」组：OSM 瓦片源 `a/b/c.tile.openstreetmap.org`（firefox 18 次），国内直连不稳。
  - `b-cdn.net` → `proxy.yaml`「漏网之鱼（2026-10-20 补录）CDN 服务商」组：RDAP NS `ns1/2/3.bunnydns.com` 实证 BunnyCDN 共享分发域。
  - `comparitech.com` → `proxy.yaml`「漏网之鱼（2026-10-20 补录）海外杂项」组：VPN/安全产品比较内容站（WorkBuddy Helper，DNS 泄露调研附带）。
  - `apnic.net` + `arin.net` → `direct.yaml`「域名查询 / RDAP（2026-10-20 漏网之鱼补录）」组：`rdap.apnic.net`/`rdap.arin.net`，同文件成组先例 `rdap.org`/`verisign.com`/`publicinterestregistry.org`（判据 2）。
  - `iana.org` → 同组：`data.iana.org` 为 IANA 域名体系基础设施（root zone 数据，DNSSEC 检测访问），国内可直连。
  - `doh.pub` → `direct.yaml`「公共 DNS / DoH（2026-10-20 漏网之鱼补录）」组：腾讯 DNSPod 公共 DoH 端点，国内服务可直连。
- **未收录及原因**：
  - COVERED 26 项整批跳过（规则集先于本地 yaml 匹配，不代表规则缺失）：`bilibili.yaml` 7 主域（hdslb/bilibili/bilivideo.com/bilivideo.cn/biligame/biliimg/biliapi）、`wechat.yaml` 5 主域（weixinbridge/qpic/qlogo/weixin/wechat.com）、`direct.yaml` 8 主域（zhipin/bosszhipin/mountaintoys.cn/rdap.org/ipip.net/jsdelivr/publicinterestregistry.org/verisign.com）+ IP `120.53.53.53`、`baidu.yaml`、`firefox.yaml`（mozilla.com）、`proxy.yaml`（schemastore.org）、IP `1.1.1.1`（dns.yaml+proxy.yaml）、IP `8.8.8.8`（dns.yaml+google.yaml）。
  - 广告/追踪类 9 主域不落盘（AGENTS.md「整批不落盘」纪律，只记录不判断、不核对 reject.yaml）：`fastly-analytics.com`、`statcounter.com`、`marketo.net`、`taboola.com`、`appier.net`、`mfadsrvr.com`、`onetag-sys.com`、`outbrain.com`、`rfihub.com`——进程均 Chrome Helper / firefox。已入 skip-list（`skip` 模式，原因注明广告/追踪类）防下轮重复处理。
  - 证据不足留人工 10 项（已入 skip-list `manual` 模式，均经 RDAP/DoH 查证后无结论）：`logitech.com`（判据 5 无 `logitech.yaml` 锚点，`updates.logitech.com`，与 logitech.io/logitechg.com 同族）；`123169.xyz`（Dynadot + Cloudflare NS 隐私保护，无归属线索，但 firefox 主动高频访问 `api.` 子域 26 次）、`111666.best`（同模式，24 次）、`999831.xyz`（同模式，3 次）——用户主动访问待确认用途；`yjz.hk`（.hk 无 RDAP 数据 + Cloudflare A 记录）；`tsight.io`（WorkBuddy Helper 访问，无线索）；`nsvcs.net`（AWS Route53 NS，`ingesteer.services-prod.` 遥测摄入端点，无品牌指向）；`ns1pcdn.net`（CSC 企业注册 + NS1，与 `mountaintoys.cn` 同批 CDN 子域模式但判据 2 不满足，无品牌锚点）；`sitemana.com`（Squarespace + CloudFront A 记录，疑似广告验证但证据不足）；`featureassets.org`（MarkMonitor 企业域 + GCP A 记录，疑似追踪但证据不足）。
- **待人工确认**（skip-list `manual` 全集 19 条目，本轮命中 4 + 新增 10）：`logitech.io`（`flow.logitech.io` logioptionsplus_agent ×92）、`logitechg.com`（×2）、`ntp.org.cn`（`edu.`/`cn.` Lark Helper ×15/×9）为既有挂起命中；本轮新增 10 项见上；其余既有挂起未命中（oceanengine.com、yhgfb-cn-static.com、applogcdn.com、temu.com、photon.codes、mdoelscope.ai）。
- **自检结果**：`find_duplicates.py` 业务文件间跨文件重复 1 条 = 历史基线（`settings.crashlytics.com` direct/google），**本次新引入 0 项**；本轮 19 个新增域经 duplicates.json 全库比对（含 followups/ 存档副本）零重复；42 个业务文件内重复 0。报告总量膨胀（跨文件 1343 / 文件内 34）系上轮交互会话引入的未跟踪目录 `followups/active/2026/2026-10/`（任务存档旧配置 yaml 副本，与根目录业务 yaml 天然大面积重合）与 `config.yaml` 策略组/DNS 值噪声（23 条）——非业务规则重复；`followups/` 归属 SPEC/FOLLOWUPS.md 管辖，本轮不动，其存档 yaml 是否纳入 .gitignore 待交互式会话裁决。`yaml.safe_load` 校验通过：bytedance.yaml 25 / fin-media.yaml 12 / proxy.yaml 862 / direct.yaml 247 条 payload。
- **AGENTS.md 同步延后**：本轮新增 19 条已裁决项（9 skip + 10 manual）已落 skip-list + changelog；AGENTS.md「已裁决结论」清单为受保护文件，同步留待交互式会话（第 0 节对齐检查）。
- Git：main 提交 `<hash>` → push → 同步 `0 0`。

## 2026-10-19 AGENTS.md 修订：修正 3 处事实过期 + 对齐 skip-list + 补齐 4 处文档缺口（交互轮）

- **触发**：用户要求审查 AGENTS.md 可优化点；审查方式为与仓库实际状态逐项交叉核对（`ls` / `git status` / `git log` / skip-list / 脚本 docstring / changelog 格式 / README 表）。
- **P0 事实过期修正**：
  - `proxy.yaml` WhatsApp 误写注释头：文档记「784 行、43 条」，实测 **790 行、其后 135 条**（`grep -n` 定位 + 行计数核实；该组为 Google 系域名 `1e100.net` / `appspot.com` 等，新增规则历年追加在最后一个注释头下导致膨胀）。`direct.yaml`「腾讯云-香港」同步校准为 44–177 行 133 条（实测行计数）。
  - `domain-distribution.html` 已不存在（`ls` 确认），从「仓库状态」移除该条。
  - changelog 标题格式规范由 `（<branch> → <merge commit>）` 改为 `（<轮次>，如 automation 轮 / 交互轮）`——2026-10-17 取消分支制后实际条目均无 branch / merge commit。
- **P1 漂移与缺口补齐**：
  - 已裁决清单对齐 skip-list：补 `www.z` / `www.zhipin`（WorkBuddy AI Helper 截断主机名，2026-10-19 裁决入 skip-list）；「统计口径」伪域名过滤示例同步补列。
  - `.gitignore` 快照补 `__pycache__/` 与 `.config`（实际文件 9 项，文档原列 7 项）。
  - 「仓库状态」与「重复规则自检闭环」补 `config.yaml` 说明：未跟踪也未 gitignore，`find_duplicates.py` 会扫到它，其 intra-file「重复」实为策略组名 / DNS 配置值噪声（2026-10-19 实测 23 条），不是规则重复，避免误判为新引入。
  - 「常用命令」补 `check_coverage.py` stdin 批量用法与「`-` 与位置参数混用会吞掉 stdin」陷阱（2026-10-19 实测），补 `--quiet`。
- **P2 文字与结构优化**：修 5 处 typo（L3 括号全半宽混用、L35 缺空格、L42「存放」重复、L44 冒号后多空格、L199「按时定期」措辞）；目录结构树补 `AGENTS.md` / `CLAUDE.md`（符号链接）/ `.agents/memory/` / `log/` 四个子目录；「日志差集纪律」首条拆为 4 个子级；规则文件数改为指针化（不再硬编码 43，指向 README 表）。
- **自检**：`git diff --stat` 仅 `AGENTS.md` + `changelog.md` + 本轮 memory 日记三个文件；过期引用（784 / domain-distribution / branch 格式 / 43 条 / 134 条）grep 清零；README、skip-list、scripts、全部 yaml 未动。
- **Git 操作链**：动手前 `git fetch origin` + `origin/main...HEAD` 双向 `0 0` → 修订 → changelog 顶部追加 → 显式暂存 3 文件 → commit → push → 复核 `0 0`。

## 2026-10-19 漏网之鱼归类：极验验证码、微信支付、SchemaStore 等 5 域归档（automation 轮）

- **数据来源**：`log/clashx-meta-log/2026-10-18_08-09-12`（cp 只读复制自 `~/.config/clash.meta/logs/2026-10-18_08-09-12`，4 个日志文件，昨日日志；`log/clashx-meta-log/` 无上轮遗留存量）。
- **提取量**（结构化脚本，已过滤伪域名 3、探针 0、私有 IP 0）：候选 116（`match Match` 4 / `oc-cn-domain` 112），归并主域 25 + 公网裸 IP 1；skip-list 命中 `skip` 3（无主端点）、`manual` 7 行（映射 5 条目）。
- **查重**：25 主域 + IP `120.53.53.53` 喂 `check_coverage.py`（全走 stdin；实测 `-` 与位置参数混用会吞掉 stdin 输入）→ COVERED 19 / UNCOVERED 7（BRAND-ANCHOR 0）。
- **补录明细**（5 域、3 文件、4 个新分组）：
  - `geetest.com` + `geevisit.com` → `direct.yaml`「验证码服务 / 极验（2026-10-19 漏网之鱼补录）」组：极验（GeeTest）验证码 `api.geetest.com`/`static.geetest.com`（oc-cn-domain 走 DIRECT）；`api.geevisit.com` 为极验验证通信姊妹域（判据 2 同厂商兄弟域成组补录）；RDAP 佐证：geetest.com NS `NS3/NS4.DNSV5.COM`（腾讯 DNSPod）、geevisit.com NS `VIP3/VIP4.ALIDNS.COM`（阿里云 DNS），均国内注册。
  - `wechatpay.cn` → `wechat.yaml`「微信支付（2026-10-19 漏网之鱼补录）」组：子域 `gtimg.wechatpay.cn`（WeChat 进程，oc-cn-domain）；判据 5——品牌字面 wechat 在域内 + `wechat.yaml` 已落盘（同 `servicewechat.com` 先例）。
  - `schemastore.org` → `proxy.yaml`「漏网之鱼（2026-10-19 补录）开发者工具」组：`www.schemastore.org`（node 进程拉取 JSON Schema，开发工具链）；SchemaStore 开源项目海外服务，RDAP NS `ns01/ns02.one.com`（海外）。2026-10-11 轮曾留人工（无同厂商参照），本轮以域名语义 + 进程 + RDAP 补齐证据裁决归档。
  - `hasseg.org` → `proxy.yaml`「漏网之鱼（2026-10-19 补录）海外杂项」组：firefox 17 次高频访问、`match Match` 走代理；RDAP NS `ns1.your-server.de`/`ns.second-ns.com`（Hetzner）、DoH A 记录 `162.55.254.99`（Hetzner 段）、wayback 429 无快照；域名无品牌锚点，按海外杂项兜底归档。
- **未收录及原因**：
  - `www.z` / `www.zhipin`：WorkBuddy AI Helper 发起的截断伪域名（无有效 TLD），提取脚本过滤漏网、人工复核排除，不归类；已追加 skip-list（`skip` 模式）防下轮重复处理。
  - COVERED 19 项整批跳过（规则集先于本地 yaml 匹配，不代表规则缺失）：`bilibili.yaml` 7 主域（hdslb/bilibili/bilivideo.com/bilivideo.cn/biligame/biliimg/biliapi）、`direct.yaml` 5 主域（zhipin/bosszhipin/kanzhun/mountaintoys.cn/tsinghua.edu.cn）、`wechat.yaml` 5 主域（weixinbridge/qpic/qlogo/servicewechat/weixin）、`baidu.yaml`（baidu.com）、IP `120.53.53.53`（direct.yaml:275 IP-CIDR）。
  - 广告/追踪类子域不逐一判定（主域均已 COVERED）：`hm.baidu.com`、`badjs.weixinbridge.com`、`t.zhipin.com`/`z.zhipin.com`/`shink.zhipin.com`/`logapi.zhipin.com`/`apm-fe.zhipin.com`、`t.kanzhun.com` 等。
- **待人工确认**（skip-list `manual` 命中 7 行，映射 5 条目，连续挂起）：
  - `edu.ntp.org.cn`（Lark Helper ×22）、`cn.ntp.org.cn`（Lark Helper ×10）——`ntp.org.cn` 待人工；
  - `flow.logitech.io`（logioptionsplus_agent ×12）、`datapipeline.logitech.io`（×1）——`logitech.io` 无锚点厂商文件；
  - `updates.optionsplus.logitechg.com`（logioptionsplus_updater ×2）——`logitechg.com` 无锚点（Logitech G 系）；
  - `athena-api.oceanengine.com`（Lark Helper ×1）——`oceanengine.com` 无锚点；
  - `lf-rc1.yhgfb-cn-static.com`（Feishu ×1）——`yhgfb-cn-static.com` 待人工。
- **自检**：`find_duplicates.py` 跨文件重复 1 条（历史基线 `settings.crashlytics.com` direct/google，非本轮引入）；文件内重复 23 条全在 `config.yaml`（未跟踪的运行配置副本，策略组名/DNS 配置值自然重复，非规则重复；扫描文件数 42→43 系该副本新出现在仓库根）。**本轮新引入重复 0 项**。`yaml.safe_load` 校验通过：direct.yaml 243 条 / proxy.yaml 850 条 / wechat.yaml 8 条 payload。
- **AGENTS.md 同步延后**：`www.z` / `www.zhipin` 伪域名裁决已落 skip-list + changelog；AGENTS.md「已裁决结论」清单为受保护文件，同步留待交互式会话（第 0 节对齐检查）。
- Git：main 提交 `<hash>` → push → 同步 `0 0`。

## 2026-10-18 skill v2.7.0：AGENTS.md 清单同步机制重设计 + logitechg.com 补录 AGENTS/MEMORY 清单（main 直接提交，交互会话）

- **动机**：今晨 automation run（`8c566c0`）实测——AGENTS.md 是受保护 agent 指令文件，cron / automation 会话（无交互用户）中 patch 工具直接 BLOCKED（"requires approval but no interactive user or gateway is present"），「已裁决结论」清单与 skip-list 出现不一致遗留（`logitechg.com` 只进了 skip-list）。
- **设计变更（skill v2.6.0 → v2.7.0）**：
  - **skip-list 定位明确为已裁决项的运行时唯一数据源**（提取脚本只读它）；AGENTS.md「已裁决结论」清单与 `.agents/memory/MEMORY.md` 同构清单定位改为**人类可读快照**。
  - **AGENTS.md 清单同步划为交互式会话专属动作**：skill 第 0 节新增「skip-list ↔ AGENTS.md 清单对齐检查」（仅交互式会话执行，比对三处清单，不一致即补齐随本轮提交）；automation 轮禁止尝试写 AGENTS.md，新裁决项只落 skip-list + changelog 并标注「AGENTS.md 同步延后」，不算失败。
  - 环境坑三处记录（skill 第 15 节、AGENTS.md「常见坑」、MEMORY.md「环境坑」）：AGENTS.md 受保护、cron 不可写。
- **本轮落盘补录（上轮 `8c566c0` 遗留的同步项，本轮交互会话对齐完成）**：
  - AGENTS.md「已裁决结论」长期挂起清单补 `logitechg.com`（Logitech G 系，2026-10-18 裁决，同 `logitech.io`）；节头权威关系表述更新（skip-list 为运行时唯一数据源、清单为快照、同步职责划归交互式会话）。
  - `.agents/memory/MEMORY.md` 同构清单同补 `logitechg.com`；「环境坑」加 AGENTS.md 受保护条目。
  - `skip-list.txt` 头部权威关系注释更新（与新设计一致）。
- **hash 回填（顺延纪律执行）**：v2.6.0 条目 `<hash>` → `371593e`；上轮 logitechg 条目 `<hash>` → `8c566c0`。
- **自检**：本轮未编辑任何规则 yaml，无 `find_duplicates.py` / yaml 语法校验触发（两者仅在编辑规则 yaml 时必做）。
- Git：main 直接提交 `<hash>` → push → 同步 `0 0`。

## 2026-10-18 漏网之鱼处理：logitechg.com 留人工裁决 + skip-list/AGENTS.md 补同步（零补录轮）

- **数据来源**：`log/clashx-meta-log/2026-10-17_08-38-11`（仓库已有，4 个日志文件）。该文件夹为 2026-10-17（昨天）日志，上轮（v2.4.1 护栏）因 app 会话未结束留原地未归档，本轮作为「昨天」处理。
- **提取量**（结构化脚本 `extract_match_domains.py`，已过滤伪域名 12、探针 0、私有 IP 0）：
  - 候选 123（`match Match` 18 / `oc-cn-domain` 105）+ 公网裸 IP 1（`120.53.53.53`）。
  - skip-list 命中：`skip` 3（`hibchr.com`/`antpeak.com`/`zorvian.com` 无主端点）、`manual` 7 行映射 5 项（`ntp.org.cn` 2 子域 Lark Helper、`logitech.io` 2 子域 logioptionsplus_agent、`mdoelscope.ai` 仿冒、`oceanengine.com` Lark Helper、`yhgfb-cn-static.com` Feishu）。
  - 归并主域 32 个 + IP 1。
- **补录明细**：0 个（无新增规则）。32 主域 + 1 IP 经 `check_coverage.py` 判定全部 COVERED——命中 `bilibili.yaml`（hdslb.com/bilibili.com/bilivideo.com/bilivideo.cn/biligame.com/biliimg.com 6 主域）、`us-bank.yaml`（53.com/breadfinancial/capitalone/capitalone360/current/key/marcus/mtb/varomoney/wellsfargo/wf 11 个美国银行主域，进程均 `python3.13`）、`wechat.yaml`（qpic.cn/weixinbridge.com/servicewechat.com/wechat.com/qlogo.cn 5 主域）、`direct-ai.yaml`（sensenova.cn/sensecore.cn/sensecoreapi.cn 商汤系 3 主域）、`direct.yaml`（mountaintoys.cn/itdog.cn/rdap.org/verisign.com 4 主域 + IP `120.53.53.53/32`）、`baidu.yaml`（baidu.com）、`bytedance.yaml`（bytednsdoc.com）。规则集先于本地 yaml 匹配，COVERED 整批跳过，不代表规则缺失。
- **未收录及原因**：
  - **`logitechg.com`**（子域 `updates.optionsplus.logitechg.com`，进程 `logioptionsplus_updater` ×2）→ **留人工**。判据#5：品牌字面「logitech」在域内但**无 `logitech.yaml` 锚点文件**→「无锚点文件即新增厂商文件→一律留人工，即便品牌明确」（与既有 `logitech.io` 同属 Logitech 系挂起项）。`check_coverage` 判 UNCOVERED + BRAND-ANCHOR 0 印证库内无同标签锚点。此为上轮（2026-10-17 itdog 轮，commit `14c677c`）已裁决结论，当时未同步 skip-list，本轮补同步。
- **本轮变更**（非规则补录，为已裁决结论的数据化同步）：
  - `skip-list.txt` `# --- 长期挂起待人工 ---` 段：`logitech.io` 后补 `logitechg.com manual:无锚点厂商文件，留人工（Logitech G 系，与 logitech.io 同）`（机器可读映射，已裁决跳过项唯一数据源；下轮起 logitechg.com 不再进候选段）。
  - `AGENTS.md`「已裁决结论」长期挂起清单的 `logitechg.com` 同步：**被保护文件策略拦截**（AGENTS.md 为受保护 agent 指令文件，cron 无交互用户无法批准写入，patch 工具直接 BLOCKED），留待交互式会话补同步。skip-list 已先行落盘保证 automation 下轮不再重复出现该候选；AGENTS.md 与 skip-list 暂时相差此项，下次交互会话需补齐 `logitechg.com` 以恢复「两者须保持一致」。
- **待人工确认**：9 项（skip-list `manual` 全集）：`logitech.io`、`logitechg.com`（本轮新增同步）、`oceanengine.com`、`ntp.org.cn`、`yhgfb-cn-static.com`、`applogcdn.com`、`temu.com`、`photon.codes`、`mdoelscope.ai`（仿冒）。本轮 manual-review 命中 5 项（ntp.org.cn / logitech.io / mdoelscope.ai / oceanengine.com / yhgfb-cn-static.com），均为既有挂起项，无新增定案。
- **自检结果**：本轮未编辑任何 `.yaml` 规则文件，无 `find_duplicates.py` 重复检查触发、无 yaml 语法校验触发（两者仅在编辑规则 yaml 时必做）。本轮实际落盘变更仅 `skip-list.txt` + `changelog.md`（AGENTS.md 写入被拦截，见上「本轮变更」）。
- Git：main 直接提交 `8c566c0` → push（`371593e..8c566c0`）→ 同步 `0 0`。

## 2026-10-17 fill-domains-from-log skill v2.6.0：提取结构化 + check-coverage 规则级查重 + skip-list 数据化（main 直接提交）

- **动机**：评审 v2.5.0 后用户指示优化。三大短板：① 第 4 步查重是 `grep -l <域名> *.yaml` 子串匹配（`53.com` 误命中 `xxxx53.com`、漏品牌标签锚点）；② 已裁决跳过项散在 AGENTS.md / skill / changelog 三处，每轮人工排除 + 全量读 663 行 changelog 耗 context；③ 提取输出五段纯文本需 agent 二次加工，无私有 IP / 探针族 / skip-list 内置过滤，automation 空结果轮无收尾定义。
- **提取脚本重构**（`.agents/skills/fill-domains-from-log/scripts/extract_match_domains.py` → `scripts/extract-match-domains/`，git mv 保留历史，对齐仓库「每脚本一目录一 README」约定）：结构化输出六段（summary / domains 候选表 `域名|类别|次数|进程` / registrable 主域归并 / public-ips / manual-review / skipped）；内置过滤无 TLD 伪域名、探针族（dotnxdomain/dashnxdomain/starnxdomain、root-key-sentinel-*、wpad）、私有保留 IP 段（ipaddress is_private 系列判据）；新增 `--skip-list` 参数与主域归并（常见二级 TLD 取三级启发式）；修复 v1 process-hints 大小写与域名桶不一致的 bug；IPv6 目标剥方括号。
- **skip-list 数据化**（`scripts/extract-match-domains/skip-list.txt`，新增）：已裁决结论的机器可读映射，`skip` 模式 10 项（reject 上游已收录 7 + 无主端点 3）、`manual` 模式 8 项（长期挂起待人工含 mdoelscope.ai 仿冒域）。AGENTS.md「已裁决结论」仍为判据权威，两者须同步维护（新裁决落 changelog 时同步追加）。
- **新增 `scripts/check-coverage/check_coverage.py`**：YAML 规则级覆盖检查（行级正则解析与 find-duplicates 一致，无 pyyaml 依赖）——DOMAIN-SUFFIX 按自身+逐级父域判覆盖、DOMAIN 精确主机（判据 8 口径）、DOMAIN-KEYWORD 报告为弱证据不算覆盖、IP-CIDR 网段包含判断（判据 7）；未覆盖域名自动扫「品牌标签锚点」（判据 1 机器化，标签逐字符相同才命中，形近/转位天然不误报）；排除 reject.yaml；支持 argv/stdin/`--quiet`；退出码恒 0（查询工具非门禁）。附 README。
- **SKILL.md v2.5.0 → v2.6.0**：流程图与第 2/3/4 节改为脚本化流程；新增第 2b 节「空结果轮收尾」（无候选 → 无 changelog 无提交、照常归档、记 memory 一行）；第 4 步粗判表落盘 `log/.work/YYYY-MM-DD-draft.md` 支持中断续跑（第 11 步 push 后清理）；第 6 节新增代理 7893 可用性探测与降级（不通时待查项顺延下轮，不阻塞 automation）；第 9 节明确 DUPLICATES.md / duplicates.json 均已入库随 yaml 编辑提交；第 13 节改为「收尾核对与记忆」澄清与第 10/12 节职责边界；硬性约束新增「查重必须用 check_coverage 禁止回退 grep 子串匹配」「skip-list 为跳过项唯一数据源」「空结果轮按 2b 收尾」三条。
- **AGENTS.md 同步**：目录结构补 check-coverage 与 skill scripts 子目录；判据 1 注明 BRAND-ANCHOR 已机器化；「已裁决结论」头部加 skip-list 权威源指针与同步纪律；常用命令补 check_coverage.py；仓库状态「加文件前查重」改指 check_coverage；修正目录树中 duplicates.json「本地」为「入库」（实查 git ls-files 已跟踪）。
- **实测**（log/clashx-meta-log/2026-10-17_08-38-11，4 个日志文件）：提取 123 候选域（mm 18 / oc 105）+ 1 公网 IP，skip-list 命中 skip 3 / manual 7，伪域名过滤 12；registrable 段 32 个主域喂 check_coverage：31 COVERED（含命中文件与行号）、1 UNCOVERED（logitechg.com，确为挂起项）；BRAND-ANCHOR 验证 `hdslb.net`→`hdslb.com`、`qpic.com`→`qpic.cn` 正确命中，`mdoelscope.ai` 标签不同不误报；IP 判定 `120.53.53.53`、`17.57.0.147` 均正确判 COVERED。
- 本提交同时带上上轮 hash 回填（v2.5.0 条目 `<hash>` → `f39b892`）与当日 memory 更新。
- Git：main 直接提交 `371593e` → push → 同步 `0 0`。

## 2026-10-17 fill-domains-from-log skill v2.5.0：日志获取回退 cp + 只处理昨天（避免沙箱弹窗、支持 automation 全自动）（main 直接提交）

- 用户裁决：日志获取从移动制（v2.3.0–v2.4.1）**回退 cp 复制 + 只处理昨天**。原因：移动制 `mv` 源目录 `~/.config/clash.meta/logs` 每次触发沙箱授权弹窗（写/删系统配置目录），定时 automation 无人响应会卡死，违背全自动诉求；cp 只读源不弹窗（实测 `ls`/`diff`/`cp` 读 `~/.config` 均无弹窗，`mv`/`rm` 写删才弹）。
- **SKILL.md 改动（v2.4.1 → v2.5.0）**：
  - frontmatter description：移动制 → cp 复制昨天的日志（禁 mv/rm 源目录、支持 automation 全自动）。
  - 第 1 节重写：只处理昨天（当天不处理、更早留存）；`cp -R` 只读复制（禁 mv/rm 源目录，附沙箱弹窗理由）；优先用仓库已有昨天前缀文件夹（无则从源 cp，防 cp 套娃——目标同名跳过）。
  - 第 12 节归档：cp 模式下仓库副本是静态快照（cp 后不再增长）可直接归档；历史 mv 遗留仍在被写的文件夹才需 mtime 检查（v2.4.1 护栏降级为历史场景）。归档仍工作区内 mv，不碰 ~/.config。
  - 硬性约束新增「禁止 mv/rm 源目录 `~/.config/clash.meta/logs`（沙箱弹窗+automation 卡死），日志获取只用 cp 只读源；归档用工作区内 mv」。
  - 流程图第 1 步改「cp 复制昨天的」。
- **AGENTS.md 同步**：「日志差集纪律」首条改回 cp + 只昨天口径；「增量可能落在今日目录」改为「只处理昨天，当天日志留待次日 automation」。
- **MEMORY.md 同步**：日志差集纪律回退 cp + 只昨天（注明回退原因）；Skill 流程裁决追加 v2.5.0 条目（沙箱规则：读 `~/.config` 不弹窗，写/删才弹窗）。
- **遗留处理**：上轮（傍晚八 itdog 验证）mv 进仓库的 `2026-10-17_08-38-11`（今天日志、仍在被 mihomo 写）按新模式「只处理昨天」**本轮不处理**，留 `log/clashx-meta-log/` 原地待明日（10-18）automation 作为「昨天」处理；届时若仍被写（会话未重启）按 v2.4.1 护栏检查 mtime。
- Git：main 直接提交 `f39b892` → push（`a8019f4..f39b892`）→ 同步 `0 0`。

## 2026-10-17 fill-domains-from-log skill v2.4.1：归档护栏——app 会话未结束不归档（main 直接提交）

- 触发：v2.4.0 首次实跑（itdog.cn 轮，提交 `14c677c`）发现边界——被处理的日志文件夹 `2026-10-17_08-38-11` 在 `mv` 移入后仍被 ClashX Meta 内核（mihomo，PID 持有 fd 指向新路径）实时写入（core/mihomo 日志 mtime 17:51 持续更新、进程 `pgrep` 确认在运行）。此时归档会让后续写入落入 `log/.archive/`，污染「已处理完不再动」语义并使下轮 diff 找不到今日日志。
- 改动：skill 第 12 节新增护栏条款「仍在被写入的文件夹不归档」——ClashX Meta 进程在运行 + 日志 mtime 接近当前时间 → 留原地，待 app 重启生成新时间戳文件夹、该文件夹停止增长后再归档。检查方式 `pgrep -fl ClashX` + `ls -lT log/clashx-meta-log/<folder>/`。version v2.4.0 → v2.4.1。
- 本轮 itdog.cn 日志文件夹 `2026-10-17_08-38-11` 按此护栏**未归档**，留 `log/clashx-meta-log/` 原地待 app 重启后再归档。
- Git：main 直接提交 `a8019f4` → push（`14c677c..a8019f4`）→ 同步 `0 0`。

## 2026-10-17 漏网之鱼归类：itdog.cn 归入 direct.yaml（v2.4.0 自主裁决模式首次实跑，main 直接提交）

- **本轮为 fill-domains-from-log skill v2.4.0（自主裁决）首次实跑验证**：全程未向用户提问，归属由 agent 自主裁决 + RDAP/DoH 留痕。流程 `mv 移入 → 提取 → 查重 → 自主裁决 → DoH/dig → 落盘 → 自检` 跑通。
- 数据来源：`log/clashx-meta-log/2026-10-17_08-38-11`（今日目录，`mv` 移入；日志在移入时仍在实时追加，提取为当时快照）。`diff -rq` 源目录仅此一项「Only in 源目录」，无套娃风险。
- 提取量（去重后，已过滤伪域名）：
  - `match Match`：25 域名、0 裸 IP；归并主域后 17 个（`53.com`、`antpeak.com`、`breadfinancial.com`、`capitalone.com`、`current.com`、`logitech.io`、`logitechg.com`、`hibchr.com`、`key.com`、`marcus.com`、`mdoelscope.ai`、`mtb.com`、`rdap.org`、`verisign.com`、`varomoney.com`、`wellsfargo.com`、`zorvian.com`）。
  - `oc-cn-domain`：约 60 域名、1 裸 IP（`120.53.53.53`）；归并主域后约 20 个 + 1 IP。
- 补录明细（1 个）：
  - `DOMAIN-SUFFIX,itdog.cn` → `direct.yaml`「其他国内站点（2026-10-11 漏网之鱼补录）」分组。**判定依据**：rdap.org 对 .cn 无 RDAP 服务（404）；改用阿里 DoH + dig 查得 A 记录 `103.248.152.254`（国内段）+ CNAME `9u8gzsjm.yunzz.net`（国内解析服务）+ .cn TLD + ITDOG 测速站域名语义；按 AGENTS.md「国内经 RDAP/NS 确认 → direct.yaml」裁决。判据留痕：DoH/dig 实测 A 记录 + CNAME 链。
- 未收录及原因：
  - **已覆盖整批跳过**（规则集先于本地 yaml 匹配，不代表缺失）：`us-bank.yaml` 10 美国银行主域（`53.com`/`breadfinancial`/`capitalone`/`current`/`key`/`marcus`/`mtb`/`varomoney`/`wellsfargo`）、`bilibili.yaml` 6 bilibili 主域（`bilibili.com`/`biligame.com`/`hdslb.com`/`bilivideo.com`/`bilivideo.cn`）、`wechat.yaml` 4 微信主域（`weixinbridge.com`/`servicewechat.com`/`wechat.com`/`qlogo.cn`）、`direct-ai.yaml` 3 商汤主域（`sensenova.cn`/`sensecore.cn`/`sensecoreapi.cn`）、`direct.yaml` `mountaintoys.cn`+`120.53.53.53/32`+`rdap.org`+`verisign.com`、`baidu.yaml` `hm.baidu.com`、`bytedance.yaml` `bytednsdoc.com`。
  - **已裁决项跳过**（不查不收）：`antpeak.com`/`hibchr.com`/`zorvian.com`（无主端点）、`mdoelscope.ai`（仿冒域）、`logitech.io`/`ntp.org.cn`/`oceanengine.com`/`yhgfb-cn-static.com`（长期挂起待人工）。
  - **`logitechg.com`**：无 `logitech.yaml` 锚点文件，按判据#5「无锚点即新增厂商文件→留人工」跳过（与既有 `logitech.io` 同属 Logitech 系挂起项）。
  - **自主模式核实陷阱留痕**：`mmbiz.qpic.cn` 主域应为 `qpic.cn`（非 `qlogo.cn`），首轮归并时误并到 `qlogo.cn` 致漏查；精确 grep 后确认 `wechat.yaml:5` 已有 `DOMAIN-SUFFIX,qpic.cn` 覆盖，归入已覆盖跳过。**教训：归并主域须逐字符精确，`grep -l` 子串命中后必须回看命中行规则类型与主域字面。**
- 待人工确认：0 项。
- 自检结果：`find_duplicates.py` 跨文件重复 1（历史基线 `settings.crashlytics.com` direct/google，非本次引入）、文件内 0、**本次新引入 0 项**；`direct.yaml` payload 数 241、`yaml.safe_load` 通过。
- Git：main 直接提交 `14c677c` → push（`bc9927c..14c677c`）→ 同步 `0 0`。

## 2026-10-17 AGENTS.md 同步日志移动制 + fill-domains-from-log skill v2.4.0：归属判定改自主裁决（main 直接提交）

- 用户裁决两项：① 同步 AGENTS.md「日志差集纪律」为移动制口径；② skill 入库 yaml 判定改 agent **自主裁决**，不再经用户确认。
- **AGENTS.md 改动**（「日志差集纪律」节）：首条 `cp -R` 只增不删 → `mv` 移动制（含 mv 套娃防护 + 归档至 `log/.archive/`）；「不能只 cp」→「不能只移入」；注明旧 cp 残留副本当日已由用户清理完毕。
- **SKILL.md 重构（v2.3.0 → v2.4.0）**——取消 review 关卡，归属判定全程自主：
  - frontmatter description：「向用户提问确认归属」→「自主裁决归属（证据不足时自主调用 RDAP/DoH）」。
  - 流程图第 5 步：`AskUserQuestion 交用户裁决（review）` → `自主裁决归属（证据足直接定；不足进 6）`；去掉用户确认分支。
  - 第 5 节重写为「自主裁决归属（留痕可追溯）」：证据充分直接定、证据不足进第 6 节、已裁决项跳过、无主端点兜底不归类、杂项按国内/海外兜底；**留痕要求**（判据条号/进程/RDAP 写 changelog）作为自主模式唯一可追溯手段；保留用户主动介入通道但默认不问。
  - 第 6 节前置条件：「用户已表示无法确定」→「自主判定证据不足项」；查询结果据以定夺不再回问用户；无主端点默认不归类记「待人工」。
  - 第 7 节前提 + 标题：「按用户确认结论执行」→「按自主裁决结论执行」。
  - 第 4 节末「进入第 5 步提问」→「进入第 6 节 RDAP」；进程粗判中浏览器进程「归属必须由用户确认」→「由第 5/6 步自主裁决」。
  - 硬性约束删除「禁止用户确认前落盘」「禁止跳过提问」两条；新增「自主裁决须留痕」「第 4 步禁外部查询、查询集中第 6 节」；「用户明确给归属以用户为准」→「用户主动介入以用户为准、默认不主动问」。
  - 第 1 节历史遗留：注明旧 cp 残留副本当日已清理。
  - changelog 模板「用户判定不归类」→「自主裁决不归类」。
- **MEMORY.md 同步**：日志差集纪律备注改为「AGENTS.md 已同步」；新增「Skill 流程裁决」节记录自主裁决裁决与留痕要求。
- 验证：SKILL.md 全文 grep `用户|AskUserQuestion|review|确认归属|提问` 残留引用均已收敛为自主口径或用户主动介入通道；章节编号 0–15 连续。
- Git：main 直接提交 `bc9927c` → push（`5514a20..bc9927c`）→ 同步 `0 0`。

## 2026-10-17 fill-domains-from-log skill v2.3.0：日志获取改为移动制 + 处理完成归档（main 直接提交）

- 用户裁决：日志流转从「`cp -R` 复制、源目录保留」改为**移动制**——源目录 `~/.config/clash.meta/logs` 的日志**移入** `log/clashx-meta-log/`，本轮分析全部完成（push + 同步 0 0）后再把已处理日志移入同级的 `log/.archive/`。
- SKILL.md 变更明细（v2.2.0 → v2.3.0）：
  - **第 1 节重写**：`mv` 移入替代 `cp -R`；新增 **mv 套娃坑**（目标侧存在同名文件夹时 `mv` 会把源塞进目标内部而不报错，须先 `diff -rq` 比对、只移「Only in 源目录」项）；历史 cp 时代的源目录残留同名旧副本**不主动删除**（破坏性操作，清理由用户裁决）；`log/clashx-meta-log/` 未归档存量（上轮遗留 / 本轮移入）直接纳入提取范围。
  - **新增第 12 节「归档已处理日志」**：push + 0 0 后 `mkdir -p log/.archive` 并移入本轮已处理文件夹；未定案（留待人工）的留在原地，待后续轮次处理完再归档；归档情况记入当日 memory。
  - 流程图新增第 12 步；原 12/13/14 节顺延为 13/14/15，全部交叉引用同步更新（第 6/9 节「见第 14 节」→ 第 15 节，第 10 节「见第 12 节」→ 第 13 节）。
  - 硬性约束新增「禁止跳过日志归档」；环境坑新增 mv 套娃条目；frontmatter description 补移动制语义。
- 连带更新：`.agents/memory/MEMORY.md`「日志差集纪律」首条改为移动制口径。**遗留未同步项**：`AGENTS.md`「日志差集纪律」仍为旧 `cp -R` 口径，与 skill 新流程冲突，本轮未动（用户未授权改 AGENTS.md），待用户裁决是否同步。
- 验证：SKILL.md 全文通读复核，章节编号 0–15 连续、交叉引用全部指向正确。
- Git：main 直接提交 `5514a20` → push（`124486d..5514a20`）→ 同步 `0 0`。

## 2026-10-17 移除远程误入库的 .omc/ 会话文件（main 直接提交）

- 用户裁决：处理掉远程的 `.omc/`。核查：git 索引跟踪着 `.omc/sessions/` 下 **49 个 session JSON**（`git ls-files .omc/` 实查；系早期误提交——`.gitignore` 早已含 `.omc/`，但对已跟踪文件不生效，故一直留在库中）。本地磁盘 `.omc/`（`project-memory.json`、`sessions/`、`state/`）为 OMC 工具运行数据，**全部保留不动**。
- 操作：`git rm -r --cached .omc/` 仅从 git 索引移除（不碰磁盘），配合既有 `.gitignore` 规则此后不再被跟踪；远程下一次 push 后即从仓库消失。
- 流程确认（用户当日明确）：**涉及 changelog.md 的提交一律先写 changelog.md 后 commit**，changelog 变更与业务改动同一提交入库；提交后回填 hash 产生的未暂存改动顺延至下轮提交。
- Git：main 直接提交 `124486d` → push（`54ae7f9..124486d`）→ 同步 `0 0`；`git ls-tree origin/main .omc/` 确认远程已清零，本地磁盘 `.omc/` 完好。

## 2026-10-17 纳入跟踪 .agents/、AGENTS.md、CLAUDE.md、changelog.md、duplicates.json（main 直接提交）

- 用户裁决：`.agents/` 应跟踪、`.omc/` 不跟踪（后者本就被 .gitignore 忽略，维持现状零动作）；`AGENTS.md`、`CLAUDE.md`、`changelog.md`、`scripts/find-duplicates/duplicates.json` 加入跟踪。
- 入库内容核查：`.agents/` 共 20 个文件（项目 skill `fill-domains-from-log`（SKILL.md + extract_match_domains.py）、项目记忆 11 个日度日志 + MEMORY.md、自动化运行契约 memory.md），grep 扫描无 token / key / password 等敏感信息；4 个 `.DS_Store` 被全局 gitignore 挡住未混入。`CLAUDE.md` 以指向 `AGENTS.md` 的符号链接形式跟踪。`duplicates.json` 现仅 118K（脚本已排除 reject.yaml，远小于 2026-09-29 取消跟踪时的约 17MB，无体积顾虑）。
- **连锁更新「未跟踪、不进提交」过期表述**（changelog 入库直接影响下轮提交流程）：
  - `AGENTS.md` 6 处：目录结构图 `.agents/skills/` 标注、changelog 编写约束导语、常用命令 duplicates.json 标注、Git 工作流两条 changelog 表述、末尾跟踪状态附注。
  - `fill-domains-from-log` SKILL.md 3 处：第 4 节读 changelog、第 10 节「先写 changelog + git add 示例加入 changelog.md」、第 12 节残留的「push 后补写」旧流程改为与第 10 步一致。
  - 自动化运行契约（`.agents/memory/automations/.../memory.md`）1 处：暂存清单须包含 `changelog.md`。
  - 新纪律：**changelog.md 变更随对应提交一并入库，不再存在「本地独享账本」**。
- 历史日志中的「未跟踪」表述系当时事实，不回溯修改。
- Git：main 直接提交 `54ae7f9` → push（`5c3b85d..54ae7f9`）→ 同步 `0 0`。

## 2026-10-17 清理误入库 pyc 缓存并忽略 __pycache__/（main 直接提交）

- 触发：用户要求按目录现状提交。核查发现两类情况——`scripts/__pycache__/merge_reject_from_loyalsoldier.cpython-314.pyc` 为**历史误提交入库**的编译缓存（上一轮目录重构清理时已物理删除，删除待提交）；三个 `scripts/*/__pycache__/` 为上轮 `py_compile` 验证新生成的本地缓存。
- 改动：提交 pyc 删除；`.gitignore` 追加 `__pycache__/` 防再犯（有误入库先例，风险真实）。**坑：原 `.gitignore` 末行 `log/` 无换行符，直接 `>>` 追加会拼成 `log/__pycache__/` 一行**，已重写文件修正。
- 顺手清理三个新生成的 `__pycache__/`（untracked，直接删除）。
- **未提交项（按既有裁决保持本地未跟踪）**：`.agents/`、`AGENTS.md`、`CLAUDE.md`、`changelog.md`、`scripts/find-duplicates/duplicates.json`——是否入库由用户后续明确决定。
- Git：main 直接提交 `5c3b85d` → push（`55ad1e0..5c3b85d`）→ 同步 `0 0`。

## 2026-10-17 scripts/ 目录层级重构：脚本迁入独立子目录并适配全部引用（main 直接提交）

- 背景：用户将平铺的三个维护脚本迁入独立子目录（`scripts/find-duplicates/`、`scripts/merge-reject-from-loyalsoldier/`、`scripts/normalize-yaml-comments/`），删除旧总版 `scripts/README.md`。本次完成全部连锁适配。
- 脚本调整（`find_duplicates.py`）：扫描根从 `Path('.')`（依赖 cwd 为仓库根）改为锚定脚本位置向上两级（仓库根），**任意目录可运行**；报告内文件路径改为输出 `relative_to(root)` 相对路径，避免绝对路径（含本机用户名）混入入库的 `DUPLICATES.md`。`merge_reject_from_loyalsoldier.py` 与 `normalize_yaml_comments.py` 仍依赖 cwd（仓库根执行），未改。
- workflow 适配：`auto-merge-reject.yml` 脚本调用路径更新为 `scripts/merge-reject-from-loyalsoldier/merge_reject_from_loyalsoldier.py`（不改则次日 00:20 UTC 定时任务必失败）。
- 引用同步：`fill-domains-from-log` skill（第 9/10/14 节脚本与报告路径、第 7 节占位文件清单更新为「空壳已清零」口径）、`AGENTS.md`（目录结构图、文件分类规则中 workflow 调用路径、常用命令、自检闭环、Git 工作流附注，共 6 处）。两者均为未跟踪本地文件，不进提交。
- **README 事故修正**：用户重写的三个子目录 README 内容全部错乱——`find-duplicates/README.md` 实为 OpenHue 灯光控制文档、`normalize-yaml-comments/README.md` 实为智能家居 skill frontmatter 模板、`merge-reject-from-loyalsoldier/README.md` 实为旧总版 `scripts/README.md` 原文（「本目录」语义失效、`../reject.yaml` 等相对链接自新位置全部指错）。本次按「每脚本一份独立 README」重写，内容以旧总 README 文字与脚本源码为准。
- 附带清理：删除遗留缓存 `scripts/__pycache__/`（对应已迁移脚本的旧 pyc）。
- 验证：三个脚本 `py_compile` 通过；`find_duplicates.py` 新逻辑自 `/tmp` 运行成功，`DUPLICATES.md` 与迁移前报告**逐字节一致**（跨文件重复 1 项 = `settings.crashlytics.com` direct/google 历史基线、文件内 0 项，本次未引入新增重复，退出码 1 系历史基线所致）；全库 grep 确认旧路径引用仅剩 changelog 历史条目（历史账本不改写）。
- Git：main 直接提交 `55ad1e0` → push（`c349502..55ad1e0`）→ 同步 `0 0`。

## 2026-10-17 scripts/README.md：修正 duplicates.json 跟踪状态描述（main 直接提交）

- 背景：当日 `.gitignore` 精简移除了 `scripts/duplicates.json` 的忽略项（该文件自始至终未纳入 git 跟踪），`scripts/README.md` 仍称其「已加入 `.gitignore`」，本次改为「未纳入 git 跟踪」。
- 同日用户裁决**取消分支制度**：所有改动直接在 main 上修改、提交、推送，本地仅保留 main（`feature/workbuddy-add-log-domain` 删除前已验证与 `origin/main` 双向 `0 0`）；「动手前 / 提交前检查本地与远程一致」约束保留并强化。AGENTS.md、fill-domains-from-log skill（v2.1.0 → v2.2.0）、自动化运行契约已同步更新——均为未跟踪本地文件，不影响本提交。
- Git：main 直接提交 `c349502` → push（`4946c64..c349502`）→ 同步 `0 0`。

## 2026-10-17 .gitignore：精简忽略规则（feature/gitignore-trim → 4946c64）

- 需求：用户手动修改 `.gitignore`，要求与远程同步。
- 改动：移除 5 项忽略规则——`.agents/`、`AGENTS.md`、`CLAUDE.md`、`changelog.md`、`scripts/duplicates.json`（连同 duplicates.json 的注释行一并删除），`log/` 移至末行；保留 `.claude/`、`.omc/`、`.trae/`、`.workbuddy-ai/`、`.workbuddy/`、`.codebuddy/`、`log/`。
- **本次仅提交 `.gitignore` 本身**。被取消忽略的文件（`.agents/`、`AGENTS.md`、`CLAUDE.md`、`changelog.md`、`scripts/duplicates.json`）**仍未纳入 git 跟踪**，是否入库由用户后续决定；工作区另有两个与本次无关的未跟踪目录 `scripts/find-duplicates/`、`scripts/normalize-yaml-comments/`（仅含 README），未做任何处理。
- 影响提示：`.agents/` 取消忽略后，项目记忆（`.agents/memory/`）与项目 skill 不再受 ignore 保护——今后若误用 `git add -A` 会一并带入暂存区，必须坚守「显式列文件、禁止批量跟踪」纪律。
- Git：feature/gitignore-trim 提交 `6d92ece` → `--no-ff` 合并回 main（`4946c64`）→ push（`1135d54..4946c64`）→ 同步 `0 0` → 工作分支 ff 对齐 → 删临时分支。

## 2026-10-17 steam.yaml：补录 4 个 Steam 常用域名，全库空壳文件清零（feature/steam-domains → 1135d54）

- 需求：用户问还有哪些 yaml 暂时为空、补充常见域名。全库扫描 43 个文件，**仅 `steam.yaml` 一个空壳**（paypal.yaml 已删、xhs.yaml 已有 `zztfly.com`），其余 42 个均有真实规则。
- 收录 4 条：`steampowered.com`（商店/账户/API）、`steamcommunity.com`（社区/市场）、`steamstatic.com`（静态资源/下载 CDN）、`steamchina.com`（蒸汽平台）。
- 核验：DoH 确认；`steamstatic.com` apex 无 A 记录属 CDN 域名正常形态，子域 `cdn.akamai` / `community.akamai` / `cdn.cloudflare.steamstatic.com` 均确认在用（Akamai），`DOMAIN-SUFFIX` 可完整覆盖。
- 未收录及原因：`steamdeck.com`（硬件产品页，非平台常用路径）、`valvesoftware.com`（Valve 官网，非 Steam 平台必需）、`steamserver.net` / `steamusercontent.com`（NOERROR 但无 A 记录、无子域使用证据）、`st.dl.bscstorage.net`（**疑蒸汽平台国内下载 CDN，但 RDAP 显示阿里云注册、无 Valve 归属直接证据，按仓库纪律留待人工确认——用户如可从实际使用确认，下轮补录**）。
- 按约定同步 README 规则文件表：steam 描述「Steam 游戏平台（待补充）」→「Steam 游戏平台（商店、社区、下载 CDN、蒸汽平台）」。
- 重复检查：文件内 0；跨文件仅剩历史基线 `settings.crashlytics.com`（direct/google）。
- Git：feature/steam-domains 提交 `21a6697` → `--no-ff` 合并回 main（`1135d54`）→ push（`af087a7..1135d54`）→ 同步 `0 0` → 工作分支 ff 对齐 → 删临时分支。

## 2026-10-17 README：「项目速览」瘦身降重（用户确认方案一，feature/readme-summary-slim → af087a7）

- 用户质疑「项目速览」是否应与前文重复。经逐项比对确认重复度约八成（12 条陈述中 11 条前文已有），呈报两个方案，用户选方案一（瘦身）。
- 改动：定位句删完整 jsDelivr URL 模式（改为指向「引用方式」）、软件枚举 5 个全举改为「支持 rule-provider 的主流 Clash 系软件（举例 3 个）」；核心事实 5 条并 4 条——「规则形态」与「兜底不漏」合并并指向「配置示例」，「更新机制」改「持续维护」并删去 interval 86400 具体值（前文示例注释与 Q2 已有，数字多头维护易漂移）。
- 保留：定位句、数据来源方法论、reject.yaml 每日自动合并（全文独家信息）、边界声明、适用人群。重复度降至约四成。
- Git：feature/readme-summary-slim 提交 `3d4c6ca` → `--no-ff` 合并回 main（`af087a7`）→ push（`62b177e..af087a7`）→ 同步 `0 0` → 工作分支 ff 对齐 → 删临时分支。
- **方法论沉淀（2026-10-17）**：面向 SEO/AI 的摘要板块，正确姿势是「压缩重述 + 独家事实 + 指针」，不是照搬正文；易漂移的数字（文件数、interval）只在一处出现，其余用指针。

## 2026-10-17 README：D 组小优化 + 文末新增 SEO「关键词」「项目速览」板块（feature/readme-d-and-seo → 62b177e）

- 用户先期只确认了 A+B，本轮补选 D 组，并要求在稳定末尾添加 SEO 关键词提升搜索权重、着重增加能让 AI 采信的内容。
- D 组三项：导语去重（不再与标题重复「互联网域名规则集」，改强调域名来自真实访问请求）；配置示例引导句理顺（「让 Google 走『Google』策略组代理访问，中国流量直连，其余兜底」）；付费代写说明从配置示例中间移至「常见问题」之后，不再打断教学流。
- 文末新增两板块（位于「反馈」之后的稳定位置）：
  - **关键词**：36 个中文词 + 4 个英文词，覆盖软件名（Clash / mihomo / OpenClash / ClashX Meta / Clash Verge / Clash for Android / Stash / Shadowrocket / Surge）、规则形态（rule-provider / RULE-SET / 规则订阅 / 精准分流）、服务类别（Google / ChatGPT / OpenAI / YouTube / Telegram / TikTok / Netflix / GitHub / 券商 / 银行 / 广告过滤）。
  - **项目速览**：面向搜索引擎与 AI 采信的事实块——项目定位、jsDelivr CDN 分发方式与 URL 模式、规则形态（DOMAIN-SUFFIX + RULE-SET 命中即停）、MATCH 兜底机制、更新机制（interval 86400、reject.yaml 每日自动合并）、边界声明（不提供节点与机场）。**所有陈述均为可核实事实**（40 余个文件、每日自动合并等与仓库实际一致），未使用夸张宣传语，这是 AI 采信的关键。
- 校验：配置示例 yaml 块 safe_load 通过；板块顺序核对（…常见问题 → 反馈 → 关键词 → 项目速览）；顺手补齐文件末尾换行。
- Git：feature/readme-d-and-seo 提交 `c001df7` → `--no-ff` 合并回 main（`62b177e`）→ push（`98d9271..62b177e`）→ 同步 `0 0` → 工作分支 ff 对齐 → 删临时分支。
- **至此 2026-10-17 README 五轮改动（配置示例重写 → 新增第四步 → 用户手动重构原样提交 → A+B 修正 → D+SEO）全部完成，C 组（两条 FAQ 恢复）仍挂起未动；其后「项目速览」瘦身一轮见上方条目。**

## 2026-10-17 README 审查修正：笔误与表述问题（用户确认 A+B 两组，feature/readme-review-fixes → 98d9271）

- 应用户要求先审查 README 再确认修改。审查结论：整体骨架良好，无伤筋络骨问题；同时核实 43 个 yaml 文件与表格 43 行一一对应、us-bank/hk-broker/us-broker 描述与内容相符、steam「待补充」准确、xhs.yaml 已有真实内容（`zztfly.com`）。
- 用户确认修改 A（笔误与空格）+ B（表述准确性）两组，C（恢复两条 FAQ）与 D（小优化）明确不动：
  - A：「（通常叫 `config.yaml`）**打**，」去多字、「包含以下 4 类内容组成」改通顺；「比对google」「把facebook.com」补空格；「无需Fork」「设置reject」补空格；付费代写段 `config.yaml` / Issues 空格统一。
  - B：例 3 标题去掉残留「—— 落到第 3 条」；「加一条规则即可」改为两步准确说法（rule-providers 加规则集 + rules 加 `RULE-SET` 行）；tencent.yaml 表格描述「腾讯 / 微信」→「腾讯（QQ、腾讯云等）」（已核实该文件无任何 weixin/wechat 域名，与 wechat.yaml 行矛盾）。
- 校验：配置示例 yaml 块 `yaml.safe_load` 仍通过；diff 仅 9 行替换、无附带改动。
- Git：feature/readme-review-fixes 提交 `98c6916` → `--no-ff` 合并回 main（`98d9271`）→ push（`6add732..98d9271`）→ 同步 `0 0` → 工作分支 ff 对齐 → 删临时分支。
- **仍挂起（用户未选，勿擅自动）**：两条 FAQ（配置粘到哪 / 追加规则集示例）未恢复；L100 句式杂糅、L3 与标题重复「互联网域名规则集」、付费代写说明位置，均维持原样。

## 2026-10-17 us-bank.yaml：补录 52 个常见知名美国银行域名，替换空占位（feature/us-bank-domains → 6add732）

- 需求：用户要求把常见知名的美国地区银行域名加入 us-bank。该文件为 10-17 当日新出现的占位文件（创建动作未单独记入 changelog；10-16 及以前全库为 42 个 yaml，10-17 审查修正时已为 43 个），原文件仅有 `# === 银行 ===` 占位注释、零规则。
- 补录 52 条（均 `DOMAIN-SUFFIX`，分三组）：
  - **全国性大行 14**：chase / jpmorgan / jpmorganchase、bankofamerica / bofa、wellsfargo / wf、citi / citibank / citibankonline、usbank、capitalone / capitalone360、tdbank。
  - **大型地区银行 26**：pnc、truist、53.com（Fifth Third）、regions、key（KeyBank）、huntington、mtb（M&T）、citizensbank、comerica、zionsbank、eastwestbank、santanderbank、popular、firsthorizon、synovus、websterbank、frostbank、arvest、umb、associatedbank、wintrust、cadencebank、southstatebank、trustmark、oldnational、westernalliancebank。
  - **知名线上银行 12**：ally、discover / discoverbank、chime、sofi、marcus（Goldman Sachs）、synchrony / synchronybank、breadfinancial、axosbank、varomoney、current。
- 核验：52 个域名全部经 DoH（走代理）确认有 A 记录；另对 current / wf / capitalone360 / varomoney / breadfinancial 拉首页标题确认身份（53.com / key.com / marcus.com 因反爬未取到标题，域名归属明确）。
- 查重：全库 grep 无冲突——us-broker.yaml 已有 schwab / ibkr / firstrade（券商归券商，未重复收录）；us-payment.yaml 仅 PayPal / Wise。find_duplicates.py：文件内重复 0；跨文件仅剩历史基线 `settings.crashlytics.com`（direct/google，非本次引入）。yaml.safe_load 通过。
- **顺带解决一处历史遗留**：上午用户把 README 的 us-bank 描述改为「美国银行，建议优先直连」时文件还是空占位、名不副实；本次补录后该描述与实际内容一致。
- Git：feature/us-bank-domains 提交 `ea16dc3` → `--no-ff` 合并回 main（`6add732`）→ push（`5eb1d37..6add732`）→ 同步 `0 0` → 工作树切回 feature/workbuddy-add-log-domain 并 ff 对齐 → 删临时分支。

## 2026-10-17 README 文档重构（用户手动编辑，经 feature/readme-manual-update 合入 main）

- 背景：用户手动更新 README 后未提交即认为已 push；实际改动停留在本地工作树（`M README.md`）。本次将其**原样提交**（Agent 未做内容改动），并按分支规则合入 main（提交 `d1aca40` → merge `5eb1d37`，已推送，同步 `0 0`）。
- 内容变更：标题/导语改写；Star 引导移至支持软件列表后并重写、新增付费代写个性化配置说明（不提供节点/机场订阅）；「使用建议」移至规则文件表之后；hk-broker 描述改「港股券商，建议使用代理」（与文件内长桥/uSMART 实际内容相符，旧描述里的 TradingView/IBKR 并不在文件中）；us-bank 描述改「美国银行，建议优先直连」；「配置示例」去掉步骤编号/路径图/汇总表改为连贯叙述；「常见问题」独立成顶级章节（保留 3 条，去掉「配置粘到哪」与「追加规则集」两条）。
- **待用户确认的遗留问题（未改动）**：① `us-bank.yaml` 仍为空占位文件（无任何规则），「建议优先直连」描述与实际内容不符；② 新文案有几处笔误——「（通常叫 `config.yaml`）打，」多了个「打」、「包含以下 4 类内容组成」搭配不当、「比对google 规则集」「把facebook.com 解析成」缺空格。

## 2026-10-17 漏网之鱼归类：doubaocdn.com / bytednsdoc.com 归入 bytedance.yaml、wechat.com 归入 wechat.yaml（自动化运行，第 11 次）

- 数据来源：`log/clashx-meta-log/2026-10-16_19-43-14`（昨日新增目录）、`log/clashx-meta-log/2026-10-16_08-15-39`（昨日目录源端当日续写，新增 3 个 core 文件，已 `cp -R` 只增不删同步）、`log/clashx-meta-log/2026-10-17_08-38-11`（今日目录，上轮未入库）。
- 提取量：`2026-10-16_19-43-14` → `match Match` 域名 102 个 + 裸 IP 2 个（`1.1.1.1` / `8.8.8.8`，`dns.yaml` 已覆盖）；`oc-cn-domain` 域名 24 个 + 裸 IP 1 个（`120.53.53.53`，已覆盖）。`2026-10-17_08-38-11` → `match Match` 域名 6 个；`oc-cn-domain` 域名 37 个 + 裸 IP 1 个。`2026-10-16_08-15-39` 增量 core（`15-16-40` / `15-16-55` / `18-36-09`）→ `match Match` 新增 2 个（`app.photon.codes` / `spectrum.photon.codes`），其余为已处理内容重提取。
- 补录 3 项（提交 `4baebfb` → main merge `49934ad`，已推送，同步 `0 0`）：
  - `bytedance.yaml`「字节系 CDN / 配置」组 +`DOMAIN-SUFFIX,doubaocdn.com`。源 `lf5/lf11/lf26-action-hub-sign.doubaocdn.com`（进程 `Feishu`）。依据：同文件已有 `doubao.com`（品牌锚点）+ 同组已有 `volces.com` 与 `volccdn.com` 的「品牌 + cdn」成组先例，构成零歧义兄弟域。
  - `bytedance.yaml` 同组 +`DOMAIN-SUFFIX,bytednsdoc.com`。源 `lf3-static.bytednsdoc.com`（进程 `Trae CN Helper`）。依据：`byte*` 命名族已覆盖 byteimg / bytetos / byteacctimg / bytedanceapi / bytescm / bytetcc，叠加字节系进程证据，同 `bytescm.com` 判定路径。
  - `wechat.yaml`「微信主域」组 +`DOMAIN-SUFFIX,wechat.com`。源 `mmhead.c2c.wechat.com`（进程 `WeChat`）。依据：品牌字面 `wechat` 在域内 + `wechat.yaml` 已为落盘锚点文件，同 2026-10-15 `servicewechat.com` 判定路径。
- 待人工确认 9 项（未落盘：8 个存疑域名 + 1 个广告/追踪批次，均无「已覆盖主域/厂商锚点」可作参照）：
  - `logitech.io`（`datapipeline.` / `flow.`，`logioptionsplus_agent`，连续第三轮遗留，本仓库无 Logitech 锚点，建 `logitech.yaml` 属新增厂商文件）
  - `oceanengine.com`（`athena-api.`，`Lark Helper`，**连续第七轮遗留**，巨量引擎广告域，无覆盖锚点）
  - `ntp.org.cn`（`cn.` / `edu.`，`Lark Helper`，运营方需外部知识确认）
  - `yhgfb-cn-static.com`（`lf-rc1.`，`Feishu`，域内无字节/飞书品牌标识，不匹配 `byte*` 族）
  - `applogcdn.com`（`lf-static.applogcdn.com`，新出现，无品牌标识亦无既有命名族）
  - `photon.codes`（`app.` / `spectrum.`，`curl`，本轮新增，无产品指向）
  - `temu.com`（`www.`，Chrome Helper，跨境电商，无覆盖锚点）
  - `mdoelscope.ai`（与已覆盖 `modelscope.ai` 仅字母转位之差，疑似错拼/仿冒域，**不是 TLD 变体**，维持不得补录）
  - 广告/追踪类约 45 个主域（`rfihub.com` / `appier.net` / `tribalfusion.com` / `travelaudience.com` / `applovin.com` / `outbrain.com` / `contextweb.com` / `statcounter.com` / `adform.net` / `quantserve.com` / `criteo.com` / `agkn.com` / `dotomi.com` / `adsrvr.org` / `bidr.io` / `inmobi.com` / `mookie1.com` / `moloco.com` / `pacvue.com` / `taboola.com` / `teads.tv` / `mathtag.com` / `stackadapt.com` / `simpli.fi` / `bidswitch.net` / `everesttech.net` / `ipredictive.com` / `onetag-sys.com` 等）—— 按约定归 `reject.yaml` 上游维护，**禁止本地编辑该文件，故本轮未做核对**，仅记录不落盘。
- 整批跳过：`antpeak.com` / `hibchr.com` / `zorvian.com`（用户已判「无主端点，不归类」）；`etahub.com` / `static.cloudflareinsights.com` / `clarity.ms` 系（changelog 已登记 reject 上游收录）；`.dotnxdomain.net` / `.dashnxdomain.net` / `.starnxdomain.net`（DNSSEC/DoH 连通性探针伪域名，同 `wpad`）；bilibili 系（`bilibili.com` / `hdslb.com` / `bilivideo.com` / `bilivideo.cn` / `mcdn.bilivideo.cn` / `biligame.com`）；微信系（`weixin.com` / `weixinbridge.com` / `qpic.cn` / `qlogo.cn` / `servicewechat.com`）；`mountaintoys.cn` / `jsdelivr.net`；裸 IP `120.53.53.53`（direct.yaml 中国移动组）、`1.1.1.1` / `8.8.8.8`（`dns.yaml`）。
- 自检：`find_duplicates.py` 跨文件重复 1 项（`settings.crashlytics.com` direct/google 历史基线）、文件内 0 项，新增 0；`bytedance.yaml`（payload 23）/ `wechat.yaml`（payload 7）`yaml.safe_load` 通过。
- Git：`feature/workbuddy-add-log-domain` 提交 `4baebfb` → `--no-ff` 合并 `49934ad` → push（`dd57903..49934ad`）→ `0	0` → feature 已 ff 对齐 main。

## 2026-10-17 README「配置示例」新增第四步：三次访问的流量路径走一遍（首个走分支规则的改动）

- 需求：在「配置示例」结尾以 `google.com` / `baidu.com` / `facebook.com` 为例，分别对应 rules 的 `RULE-SET,google` / `GEOIP,CN` / `MATCH`，解释具体请求流量路径，给读者直观了解。
- 内容：新增「第四步：看懂一次访问是怎么'走'的」——先重申「命中即停」，再三个示例各按「发起请求 → 规则比对 → 命中即停 → 流量走向」四步分解并配单行路径图（google.com → Google 策略组 → 机场节点；baidu.com → IP 属中国 → DIRECT 直连；facebook.com → 前两条未命中 → MATCH,PROXY 兜底），末尾一张三网站对照表；并说明 facebook.com 走兜底是因最简配置只引用 google.yaml，引导按 Q3 追加规则集。
- 校验：板块内 3 个 yaml 代码块均 `yaml.safe_load` 通过；第四步引用的 rules 与主示例完全一致。
- Git：**首次按当日新规则（任何改动走分支再进 main）执行**——从 main 切 `feature/readme-traffic-path`（提交 `ba32d75`）→ `--no-ff` 合并回 main（`a831088`）→ push（`c33df9d..a831088`）→ 同步 `0 0` → 工作树切回 `feature/workbuddy-add-log-domain` 并 ff 对齐 → 删除已合并的临时分支。

## 2026-10-17 README「配置示例」板块重写为小白友好版（当时直接提交 main，当日即修订为必须走分支）

- 动机：原「配置示例」只有一份裸 YAML，且注释存在多处错漏，网络小白 / 代理软件小白难以读懂。
- 改动内容：
  - 新增「第一步：先看懂 4 个概念」表格——`proxy-providers`（订阅集合）/ `proxy-groups`（策略组）/ `rule-providers`（规则集）/ `rules`（规则），各配一句大白话解释，并补一段四者分工说明。
  - 「第二步：复制最精简配置」重写示例 YAML：修正原草稿注释错误（`type` / `behavior` / `url` 三行注释均误写「规则集名称，可自定义」、`rules:` 块注释误写「规则集名称，可自定」、`interval: 3600` 注释句子截断为「每隔1小时从」）；注释按 CJK 双宽显示宽度统一对齐；订阅集合名由 `cloudflare` 改为 `airport`（原名易与 CDN 混淆）。
  - 修正示例 bug：原 `rules` 引用 `RULE-SET,youtube,...`，但 `rule-providers` 只定义了 `google`，小白照抄必然加载失败；改为引用 `google` 保持自洽。
  - 「第三步：常见问题」5 条：配置粘到哪（按软件分述）/ 没有机场能否用 / 如何追加规则集（附 openai 扩展示例）/ 规则集下载失败排查 / Google 打不开排查。
  - 明确适用软件范围：mihomo / Clash 系（OpenClash、ClashX Meta、Clash Verge、Clash for Android、Stash）；Surge、Shadowrocket 语法不同，引导使用各自软件内置的规则集功能。
- 校验：板块内 2 个 yaml 代码块均 `yaml.safe_load` 通过；另写脚本校验引用一致性——`rules` 引用的 rule-provider / proxy-group、`use` 引用的订阅均已定义。
- Git：main 提交 `c33df9d` → `git push origin main`（`0fabf39..c33df9d`）→ `git rev-list --left-right --count origin/main...HEAD` 输出 `0 0` → 切回 `feature/workbuddy-add-log-domain`。
- 备注：开头一句由「一套长期维护……」补为「clash-proxy是一套长期维护……」，为上一轮遗留的未提交草稿改动，随本提交一并入库。
- **流程修订（当日，用户裁决）**：用户明确「任何改动都走分支，再进 main」，废止「README 等文档类改动可直接提交 main」的做法。规则已同步写入 `AGENTS.md`「Git 工作流」；`fill-domains-from-log` skill 原有「main 全程只读、所有编辑发生在 feature 分支」本就与裁决一致。`c33df9d` 直接提在 main 上属既成事实（禁强推，不回溯历史），**此后一切改动（含文档、脚本）一律先走 feature 分支再 `--no-ff` 合并进 main**。

## 2026-10-16 漏网之鱼归类：digicert.cn 归入 direct.yaml、Apple 推送 IP 归入 apple.yaml（自动化运行）

- 数据来源：
  - `log/clashx-meta-log/2026-10-15_08-42-40`（昨日日志）。`diff -rq` 与仓库副本**完全一致**（该目录本日上午已由人工会话处理过 15:30–次日 00:29 的全部增量）→ **零新增**，逐项复核确认。
  - `log/clashx-meta-log/2026-10-16_08-15-39`（今日日志，上轮 cp 入库备用但未分析）。差集检查发现源目录当日**持续追加至 12:13**（新增 `clashx_core_16_12-10-27/12-13-14/12-13-41.log`）→ 重新 `cp -R` 同步后提取到增量。**本轮的实质产出全部来自该目录。**
- 提取结果：`2026-10-15_08-42-40` → `match Match` 域名 80 个 + 裸 IP 0 个；`oc-cn-domain` 域名 65 个 + 裸 IP 1 个（`120.53.53.53`，已覆盖）。`2026-10-16_08-15-39` → `match Match` 域名 4 个 + 裸 IP 1 个；`oc-cn-domain` 域名 34 个 + 裸 IP 1 个（同上）。
- **补录 2 个目标 / 2 个文件**（无人值守默认策略：仅补「与已覆盖主域同厂商、语义无歧义的兄弟域」）：
  - `direct.yaml`「证书验证（2026-06-25 补录）」分组 +1：`DOMAIN-SUFFIX,digicert.cn`。依据：源 `cacerts.digicert.cn`（`oc-cn-domain` 命中，进程 `trustd`，端口 80 的 CA 证书校验流量），组内已有 `DOMAIN-SUFFIX,cacerts.digicert.com` —— **同品牌标签 `digicert` 在库内已有被覆盖 TLD（`.com`）+ 主机前缀 `cacerts.` 完全一致 + 进程 `trustd` 与分组「证书验证」语义吻合**，三重印证构成零歧义 TLD 变体补录。payload 239 → 240 条。
  - `apple.yaml`「Apple 推送 apsd（2026-09-29 漏网之鱼补录）」分组 +1：`IP-CIDR,17.57.0.147/32,no-resolve`。依据：源 `17.57.0.147:443`（`match Match`，进程 `iCloudNotificationAgent`），与同组既有 `17.57.145.0/24` **同厂商（Apple `17/8` 段）+ 同推送语义 + 同 `17.57.*` 段**，沿用 2026-10 早前「裸 IP 按归属归类并加 `no-resolve`」（先例 `120.53.53.53`）的处理路径。payload 101 → 102 条。
- **待人工确认（未落盘）10 项**：
  - `mdoelscope.ai`（**本轮新增**，源 `mdoelscope.ai:443`，进程 `firefox` 22 次）—— 域名标签与已覆盖的 `modelscope.ai`（`alibaba-global.yaml`）**仅字母转位之差**（`mdoel` ↔ `model`），属疑似错拼 / 仿冒域，**不是同标签 TLD 变体**，不得按兄弟域补录，留待人工裁决。
  - `oceanengine.com`（`athena-api.`，进程 `Lark Helper`，**连续第六轮遗留**）、`logitechg.com`（`updates.optionsplus.logitechg.com`，进程 `logioptionsplus_updater`）、`logitech.io`（上轮遗留）—— 本仓库无对应厂商锚点，建 `logitech.yaml` 属新增厂商文件。
  - `fastly-analytics.com`（`*.u.fastly-analytics.com`，与库内 `fastly.net` 非同品牌）、`surfsharkdns.com`（`*.ipv4.surfsharkdns.com`）、`icanhazip.com`（`ipv4.` / `ipv6.`）—— 独立厂商，无已覆盖锚点。
  - `123169.xyz`（`api.`）、`999831.xyz`（`cf.`）、`111666.best`（`i.`）—— 无品牌标识、无可参照厂商。
- 整批跳过（已被现有规则覆盖，非规则缺失）：bilibili 系（`bilibili.com` / `bilivideo.com` / `bilivideo.cn` / `hdslb.com` / `mcdn.bilivideo.cn` → `bilibili.yaml`）；微信系（`weixinbridge.com` / `qpic.cn` / `qlogo.cn` / `servicewechat.com` → `wechat.yaml`）；WPS 系 5 主域（`wps.cn` / `wpscdn.cn` / `qwps.cn` / `ksosoft.com` / `ksord.com` → `direct.yaml`）；商汤 SenseNova 系 3 主域（`sensecoreapi.cn` / `sensenova.cn` / `sensecore.cn` → `direct-ai.yaml`）；腾讯系（`cloud.tencent.com` / `tencent-cloud.cn` / `gtimg.cn` → `tencent.yaml`）；`mountaintoys.cn` / `myip.ipip.net` / `mirrors.tuna.tsinghua.edu.cn` / `analytics.brew.sh` / `ftpmirror.gnu.org` / `mirror.team-cymru.com` → `direct.yaml` / `proxy.yaml` 已覆盖；`hm.baidu.com` → `baidu.yaml`；裸 IP `120.53.53.53`（`direct.yaml` 中国移动分组）；`monitor_browser`（无 TLD 伪域名，脚本已过滤）。
- 跳过（历史已判定，不重复收录）：`etahub.com` / `static.cloudflareinsights.com`（`reject.yaml` 上游已收录）；`antpeak.com` / `hibchr.com` / `zorvian.com`（2026-10-04 判定无主广告 / 追踪端点）。
- 重复检查结果：`python3 scripts/find_duplicates.py` 扫描 42 个文件 → 跨文件重复 1 项（`DOMAIN-SUFFIX,settings.crashlytics.com`，`direct.yaml` / `google.yaml` 历史基线）、文件内重复 0 项，**本次未引入新增重复**。语法校验：`direct.yaml`（payload 240）、`apple.yaml`（payload 102）均 `yaml.safe_load` 通过。
- Git：feature/workbuddy-add-log-domain 提交 `155bd0b` → `--no-ff` 合并回 main（merge `0fabf39`）→ `git push origin main`（`318bc9d..0fabf39`）→ 同步 `0  0` → 切回 feature。
- 本轮新经验：
  - **增量可能出现在「今日」目录而非「昨日」目录**：本轮昨日（10-15）目录与仓库副本完全一致、零新增，实质产出全部来自今日（10-16）目录 —— 该目录上轮仅「cp 入库备用、未分析」。**差集带出的目录必须真正跑一遍提取，不能因「所属日期不是昨日」就只 cp 不分析。**
  - **`diff -rq` 会出现双向「Only in」**：ClashX Meta 会轮转 / 裁剪 core 日志，源目录可能已删除旧 core 文件而生成新 core 文件（本轮 `2026-10-16_08-15-39` 中 `08-16-20` / `09-37-37` 仅存于仓库副本，`12-10-27` / `12-13-14` / `12-13-41` 仅存于源目录）。同步时用 `cp -R <src>/. <dst>/` 只增不删，可保留全部历史证据；判断「是否有增量」应以**源目录新增文件**为准。
  - **裸 IP 补录的判据是「同厂商 IP 分组已存在」**：`IP-CIDR` 条目不受「同主域」规则约束，改为看进程 + 是否已有同厂商的 IP 段分组（本轮 Apple 推送组已有 `17.57.145.0/24`）。

## 2026-10-16 漏网之鱼归类：10-15 日志增量补录 7 个域名（tencent +3 / proxy +3 / direct +1，人工会话裁决）

- 数据来源：`log/clashx-meta-log/2026-10-15_08-42-40`（昨日日志）。**增量发现**：该目录 10-15 当天运行（changelog 2026-10-15 条目）已处理过 15:30 快照，但源目录当天持续追加至 10-16 00:29，且含 10-15 23:57 重启生成的 `clashx_core_15_23-57-46.log`。本轮 `diff -rq` 发现仓库副本与源目录不一致后重新 `cp -R` 同步并提取，增量中产生新域名；15:30 快照内的主域全部已在当日处理完毕，零新增。另按差集约定将源目录今天生成的 `2026-10-16_08-15-39` 一并入库备用（非本轮目标，未分析）。
- **补录 7 个域名 / 3 个文件**（本轮为人工会话，4 组候选经用户逐项裁决）：
  - `tencent.yaml` +3：`cloud.tencent.com`、`tencent-cloud.cn` 归入「腾讯云」分组（覆盖 act-api./ping./sensors. cloud.tencent.com 与 cloudcache./dscache./qcloudimg. tencent-cloud.cn 共 6 个 oc-cn-domain 域名，进程 firefox）；`gtimg.cn` 归入「腾讯静态资源」分组（源自 `midas.gtimg.cn`，与文件内已有 `gtimg.com` 为同标签多 TLD 变体，锚点明确）。payload 14 → 17。
  - `proxy.yaml` +3：`brew.sh` 追加至 `formulae.brew.sh` 所在「漏网之鱼（2026-06-06）」分组（源自 `analytics.brew.sh`，curl 106 次，Homebrew 遥测端点；用户裁决补主域而非精确子域）；`gnu.org` 归入「Linux 社区」分组（源自 `ftpmirror.gnu.org`，curl 4 次）；`team-cymru.com` 新建「安全研究 / 恶意软件库（2026-10-16 漏网之鱼补录）」分组（源自 `mirror.team-cymru.com`，curl 6 次，Team Cymru 恶意软件哈希库镜像；后两项为用户裁决的海外站点默认归 proxy）。payload 845 → 848。
  - `direct.yaml` +1：`tsinghua.edu.cn` 新建「国内教育网镜像（2026-10-16 漏网之鱼补录）」分组（源自 `mirrors.tuna.tsinghua.edu.cn`，git-remote-http 8 次，清华大学 TUNA 镜像站，用户裁决归 direct）。payload 238 → 239。
- 整批跳过（已被现有规则覆盖，非规则缺失）：bilibili 系（bilibili.com / bilivideo.com / bilivideo.cn / hdslb.com → bilibili.yaml）；微信系（weixinbridge.com / qpic.cn / qlogo.cn / shortcloud.weixin.com / servicewechat.com → wechat.yaml）；WPS 系 5 主域（wps.cn / wpscdn.cn / qwps.cn / ksosoft.com / ksord.com → direct.yaml，进程 wpscloudsvr / wpsoffice）；商汤 SenseNova 系 3 主域（sensecoreapi.cn / sensenova.cn / sensecore.cn → direct-ai.yaml）；mountaintoys.cn → direct.yaml；hm.baidu.com → baidu.yaml；myip.ipip.net → direct.yaml；裸 IP `120.53.53.53`（direct.yaml 中国移动分组）。
- 跳过（历史已判定，不重复添加）：`etahub.com` / `static.cloudflareinsights.com`（reject.yaml 上游已收录）；`antpeak.com` / `hibchr.com` / `zorvian.com`（2026-10-04 判定无主广告/追踪端点）。
- **待人工确认（维持挂起，本轮未再提问）8 项**：`logitechg.com`（Logitech 系，本仓库无覆盖锚点，建 logitech.yaml 属新增厂商文件）、`fastly-analytics.com`（与库内 fastly.net / fastly-edge.com 非同一品牌）、`surfsharkdns.com`（VPN DNS 探针，独立厂商）、`icanhazip.com`（IP 查询，与「IP综合测试」组仅类别相近非同厂商）、`123169.xyz` / `999831.xyz` / `111666.best`（无品牌标识、无可参照厂商）、`oceanengine.com`（巨量引擎广告域，**连续第五轮遗留**，Lark Helper 发起）。
- 重复检查结果：`python3 scripts/find_duplicates.py` → 跨文件重复 1 项（`DOMAIN-SUFFIX,settings.crashlytics.com`，direct.yaml / google.yaml 历史基线）、文件内重复 0 项，本次未引入新增重复。语法校验：tencent.yaml（payload 17）、proxy.yaml（payload 848）、direct.yaml（payload 239）均 `yaml.safe_load` 通过。
- Git：feature/workbuddy-add-log-domain 提交 `45d2fb7` → `--no-ff` 合并回 main（merge `1dd4cac`）→ `git push origin main`（`d9dceb7..1dd4cac`）→ 同步 `0 0` → 切回 feature/workbuddy-add-log-domain。
- 本轮新经验：**当日运行过的日志目录仍可能有增量**。10-15 条目把 `2026-10-15_08-42-40` 作为「今日日志」处理，但 ClashX Meta 日志文件夹当天持续追加（本例跨日至 10-16 00:29，且 23:57 重启新增一个 core 日志文件）。仅凭 changelog 有该目录记录就判「已处理」会漏掉增量；**必须 `diff -rq` 源目录与仓库副本**，不一致时同步后重新提取，再与 changelog 已处理主域集合对比定位增量。

## 2026-10-15 漏网之鱼归类：browserleaks.net / browserleaks.org 归入 proxy.yaml、servicewechat.com 归入 wechat.yaml（自动化运行）

- 数据来源：`log/clashx-meta-log/2026-10-14_08-44-29`（昨日）、`log/clashx-meta-log/2026-10-15_08-42-40`（今日）。差集检查发现源目录 `~/.config/clash.meta/logs/` 有、仓库 `log/` 无的目录共上述 2 个，均已 `cp -R` 只增不删入库，入库后复核无差异。
- 提取结果：
  - `2026-10-14_08-44-29`：`match Match` 域名 2 个（`etahub.com`、`updates.optionsplus.logitechg.com`）、裸 IP 0 个；`oc-cn-domain` 域名约 95 个（bilibili 系 CDN 节点 `cn-*-ct-*` / `upos-sz-*` / `mcdn.bilivideo.cn`、`*.edge.mountaintoys.cn`、微信系 `weixinbridge` / `qpic.cn` / `qlogo.cn` / `shortcloud.weixin.com` 为主）、裸 IP 1 个（`120.53.53.53`，已覆盖）。
  - `2026-10-15_08-42-40`：`match Match` 域名 30 余个（以 `browserleaks` DNS 泄漏探针随机子域、`*u.fastly-analytics.com`、`surfsharkdns.com`、`icanhazip.com` 为主）、裸 IP 0 个；`oc-cn-domain` 域名约 43 个（bilibili 系、微信系、`myip.ipip.net`、`athena-api.oceanengine.com`、`res.servicewechat.com`）、裸 IP 1 个（`120.53.53.53`）。
- **补录 3 个域名 / 2 个文件**：
  - `proxy.yaml`「IP综合测试」分组 +2：`DOMAIN-SUFFIX,browserleaks.net`、`DOMAIN-SUFFIX,browserleaks.org`。依据：该组已覆盖同品牌 `.com`（`browserleaks.com`），`.net` / `.org` 与 `.com` 为同一产品（浏览器指纹 / IP 测试站）的同标签多 TLD 变体，属零歧义兄弟域补录，沿用 2026-10-09 `xvideos.com`→`xvideos.net` 的判定路径。payload 843 → 845 条。
  - `wechat.yaml` 新增「微信小程序服务（2026-10-15 漏网之鱼补录）」分组 +1：`DOMAIN-SUFFIX,servicewechat.com`。依据：源 `res.servicewechat.com`（oc-cn-domain 命中，进程 `WeChatAppEx Helper`），品牌标识 `wechat` 字面在域名内，仓库已有微信厂商文件 `wechat.yaml`（覆盖 `weixin.com` / `weixinbridge.com` / `qpic.cn` / `qlogo.cn`）—— 满足「同厂商 + 语义无歧义」。payload 5 → 6 条。
- **待人工确认（未落盘，均无「已覆盖主域」可作同厂商参照，需外部知识定厂商）**：
  - `logitechg.com`（`updates.optionsplus.logitechg.com`，进程 `logioptionsplus_updater`）、`logitech.io`（上轮遗留）—— Logitech 系，但本仓库无任何已覆盖的 Logitech 主域，建 `logitech.yaml` 属新增厂商文件，留待人工裁决。
  - `fastly-analytics.com`（`*.u.fastly-analytics.com`）—— 与库内 `fastly.net` / `fastly-edge.com` 非同品牌（`analytics` 后缀语义不同），不构成兄弟域。
  - `surfsharkdns.com`（`*.ipv4.surfsharkdns.com`，Surfshark VPN DNS 探针）、`icanhazip.com`（`ipv4.` / `ipv6.`）—— 均为独立厂商，无已覆盖锚点（与「IP综合测试」分组的 `ipify.org` / `ipinfo.io` 仅类别相近、非同厂商）。
  - `123169.xyz`（`api.`）、`999831.xyz`（`cf.`）、`111666.best`（`i.`，上轮遗留）—— 无品牌标识、无可参照厂商。
  - `oceanengine.com`（`athena-api.`，进程 `Lark Helper`，**连续第四轮遗留**）—— 巨量引擎广告域，本仓库无覆盖锚点。
  - `browserleaks` 已解决，移出待确认清单。
- 整批跳过（已被现有规则覆盖，非规则缺失）：bilibili 系（`bilibili.com` / `bilivideo.com` / `bilivideo.cn` / `biliimg.com` / `hdslb.com` → bilibili.yaml）；微信系（`weixin.com` / `weixinbridge.com` / `qpic.cn` / `qlogo.cn` → wechat.yaml）；`ipip.net` → direct.yaml「域名查询」分组；`mountaintoys.cn` → direct.yaml；裸 IP `120.53.53.53`（direct.yaml 中国移动分组）。
- 跳过（历史已判定，不重复添加）：`etahub.com` / `static.cloudflareinsights.com`（reject.yaml 上游已收录）；`antpeak.com` / `hibchr.com` / `zorvian.com`（2026-10-04 判定无主广告/追踪端点）；`monitor_browser`（无 TLD 伪域名，脚本已过滤）。
- 重复检查结果：`python3 scripts/find_duplicates.py` → 跨文件重复 1 项（`DOMAIN-SUFFIX,settings.crashlytics.com`，direct.yaml / google.yaml 历史基线）、文件内重复 0 项，**本次未引入新增重复**。语法校验：`proxy.yaml`（payload 845）、`wechat.yaml`（payload 6）均 `yaml.safe_load` 通过。
- Git：feature `2cd9aeb` → `--no-ff` 合并回 main（merge `d9dceb7`）→ `git push origin main`（`9b1ea21..d9dceb7`）→ 同步 `0  0` → 切回 feature/workbuddy-add-log-domain。
- 本轮新增判定经验：**按「品牌标签」而非「全域名」grep 全库**。前几轮只 grep `browserleaks.net` 得 NONE 即列为待确认，遗漏了 `.com` 锚点；改为按标签 `browserleaks` grep 后才发现 `proxy.yaml` 已有 `browserleaks.com`，`.net` / `.org` 遂成零歧义兄弟域。**TLD 变体（同标签 `.com`/`.net`/`.org`）在库内有任一被覆盖时，其余 TLD 属可补录范围。**

## 2026-10-13 漏网之鱼归类：time1.cloud.tencent.com 归入 tencent.yaml、bytescm.com / bytetcc.com 归入 bytedance.yaml（自动化运行）

- 数据来源：`log/clashx-meta-log/2026-10-13_09-14-45`、`log/clashx-meta-log/2026-10-13_11-06-26`（差集检查发现源目录 `~/.config/clash.meta/logs/` 有、仓库 `log/` 无，已 `cp -R` 入库）。另复核昨日日志 `2026-10-12_09-38-05`：与仓库副本 `diff -rq` 完全一致（源目录内容自上次 cp 后未再增长），该轮已处理，本次零新增。
- 提取结果：
  - `2026-10-13_09-14-45`：`match Match` 域名 21 个、裸 IP 0 个；`oc-cn-domain` 域名 57 个（以 bilibili 系 CDN 节点（`cn-*-ct-*` / `upos-sz-*` / `mcdn.bilivideo.cn` 实例名）、baidu 静态资源、广东政务站、`*.edge.mountaintoys.cn` 为主）、裸 IP 1 个（`120.53.53.53`，已覆盖）。
  - `2026-10-13_11-06-26`：`match Match` 域名 0 个；`oc-cn-domain` 域名 5 个（`badjs.` / `cube.weixinbridge.com`、`mmbiz.` / `mmecoa.qpic.cn`、`wx.qlogo.cn`，进程 `WeChatAppEx Helper` / `WeChat`）、裸 IP 1 个（`120.53.53.53`）。
- 补录 3 个域名 / 2 个文件：
  - `tencent.yaml`「腾讯子域补充」分组 +1：`DOMAIN-SUFFIX,time1.cloud.tencent.com`。依据：`time1.cloud.tencent.com`（oc-cn-domain 命中，进程 `Lark Helper`），属 `*.tencent.com` 精确子域 —— 按既定约定为归属零歧义安全区，与同组 `copilot.tencent.com` / `lightai.cloud.tencent.com` 同类。payload 13 → 14 条。
  - `bytedance.yaml` 新增「字节系 CDN / 配置（2026-10-13 漏网之鱼补录）」分组 +2：`DOMAIN-SUFFIX,bytescm.com`、`DOMAIN-SUFFIX,bytetcc.com`。依据：源日志 `lf-cdn-tos.bytescm.com`、`lf3-config.bytetcc.com`（均 oc-cn-domain 命中，发起进程 `Feishu`，字节系产品），且两域均为 `byte*` 前缀，与文件内既有的 `byteimg.com` / `bytetos.com` / `byteacctimg.com` / `bytedanceapi.com` 同族约定一致 —— 沿用 2026-10-12 `bdimg.com`（凭 `bdstatic.com` 同族先例补入）的判定路径。payload 19 → 21 条。
- 整批跳过（已被现有规则覆盖，非规则缺失）：bilibili 系（`bilibili.com` / `biliapi.com` / `bilivideo.com` / `bilivideo.cn` / `hdslb.com` → bilibili.yaml）；微信系（`weixinbridge.com` / `qpic.cn` / `qlogo.cn` → wechat.yaml）；`baidu.com` → baidu.yaml；`mountaintoys.cn` → direct.yaml；裸 IP `120.53.53.53`（direct.yaml 中国移动分组）；`monitor_browser` / `wpad`（无 TLD 伪域名，脚本已过滤）。
- 跳过（历史已判定，不重复添加、不提问）：`akstat.io`（`17de4c1f.akstat.io`）、`go-mpulse.net`（`c.` / `s.` 子域）—— 二者均已在本文件早前条目的「跳过项（现已被 reject.yaml 覆盖）」清单中登记，直接跳过。
- 待人工确认 12 项（未落盘，均无「已覆盖主域」可作同厂商参照，需外部知识定厂商）：`asus.com` 系（12 个主机名：`asus-brand-assistant.` / `asuschatapi.` / `demeter.` / `dlcdnimgs.` / `dlcdnwebimgs.` / `km-ap.` / `kmpic.` / `mwservice.` / `nomos.` / `odinapi.` / `router.` / `www.`，华硕主域在本仓库无任何覆盖，建 `asus.yaml` 属新增厂商文件，留待人工裁决）、`bazaarvoice.com`（`apps.` / `network-a.`，评论 SaaS）、`fonts.net`（`cdn.fonts.net`）、`logitech.io`（`datapipeline.` / `flow.`，进程 `logioptionsplus_agent`）、`codegang.top`（`mc.`，firefox 80 次）、`romleyuan.com`（`www.`，firefox 156 次）、`oceanengine.com`（`athena-api.`，Lark Helper，**连续第三轮遗留**）、`gd.gov.cn`（`app.` / `statistics.` / `tyrz.`）、`gdzwfw.gov.cn`（`static.` / `www.` / `xtbg.`）、`sz.gov.cn`（`zjj.`，上述三项国内政务站，上轮已列待确认）、`ntp.org.cn`（`cn.` / `edu.`，Lark Helper，运营方需外部知识确认）、`yhgfb-cn-static.com`（`lf-rc1.`，Feishu，域名内无字节/飞书品牌标识，命名约定也不匹配 `byte*` 族）。
- 重复检查：`python3 scripts/find_duplicates.py` 扫描 42 个文件，跨文件重复 1 项、文件内 0 项 —— 仅 `DOMAIN-SUFFIX,settings.crashlytics.com`（direct.yaml / google.yaml）历史基线，本次新引入 0 项。语法校验：tencent.yaml（payload 14 条）、bytedance.yaml（payload 21 条）均通过 `yaml.safe_load`。
- Git：feature/workbuddy-add-log-domain 提交 `98efe77` → main `--no-ff` 合并 `dec0f07` → `git push origin main`（`11291cb..dec0f07`）→ 同步状态 `0  0` → 切回 feature。
- **环境变更（与上轮相反）**：本机代理 `http://127.0.0.1:7893` 本次**恢复可用**（`nc -z` 探测成功），GitHub 直连反而不通（`curl --noproxy` 返回 000），故 git 操作沿用默认配置走代理即成功，无需 `-c http.proxy=` 禁用。结论：每轮开始前先探测 7893 与 GitHub 直连可用性，按结果择路。

## 2026-10-12 漏网之鱼归类：bdimg.com 归入 baidu.yaml、sentry-cdn.com 归入 microsoft.yaml（自动化运行）

- 数据来源：`log/clashx-meta-log/2026-10-12_09-38-05`（今日日志；差集检查发现源目录 `~/.config/clash.meta/logs/` 有、仓库 `log/` 无，已 `cp -R` 入库）。另复核昨日日志 `2026-10-11_08-33-37`（该轮 2026-10-11 已处理过，本次再次核验）。
- 提取结果：
  - 2026-10-12：`match Match` 域名 24 个、裸 IP 0 个；`oc-cn-domain` 域名约 60 个（以 bilibili 系 CDN 节点、zhihu 图片 CDN、baidu 静态资源、`*.edge.mountaintoys.cn` 为主，主域高度集中）、裸 IP 1 个（`120.53.53.53`，已覆盖）。
  - 2026-10-11：`match Match` 域名 12 个、裸 IP 0 个；`oc-cn-domain` 域名 3 个 + 裸 IP 1 个。**逐项复核全部已覆盖或属历史判定项，零新增**（`feishucdn.com` 已入库、`lightai.cloud.tencent.com` 已覆盖、7 个 `*.paypal.com` 由 us-payment.yaml 覆盖、`rdap.org` / `rdap.verisign.com` 由 direct.yaml RDAP 分组覆盖）。
- 补录 2 个域名 / 2 个文件：
  - `baidu.yaml` +1：`DOMAIN-SUFFIX,bdimg.com`。依据：`apps.bdimg.com`（oc-cn-domain 命中），与文件内已覆盖 `baidu.com` / `bdstatic.com` 同系，沿用 2026-10-07 `bdstatic.com` 的「百度静态资源 CDN」补录先例。payload 2 → 3 条。
  - `microsoft.yaml`「第三方依赖服务」分组 +1：`DOMAIN-SUFFIX,sentry-cdn.com`。依据：`browser.sentry-cdn.com`（Sentry 浏览器 SDK CDN），与同组既有 `DOMAIN-SUFFIX,sentry.io` 同厂商；该组已有 `intercom.io` + `intercomcdn.com` 的「厂商 + 其 CDN」成组约定，语义零歧义。payload 70 → 71 条。
- 整批跳过（已被现有规则覆盖，非规则缺失）：bilibili 系（`bilibili.com` / `biliimg.com` / `hdslb.com` / `bilivideo.com` / `bilivideo.cn` / `biligame.com` → bilibili.yaml）；`zhihu.com` / `zhimg.com` → direct.yaml；`baidu.com` / `bdstatic.com` → baidu.yaml；`mountaintoys.cn` → direct.yaml；裸 IP `120.53.53.53`（direct.yaml 中国移动分组）；`monitor_browser`（无 TLD 伪域名）。
- 跳过（历史已判定，不重复添加）：`static.cloudflareinsights.com`（reject.yaml 上游已收录）；`antpeak.com` / `hibchr.com` / `zorvian.com`（2026-10-04 判定无主广告/追踪端点）。
- 待人工确认 19 项（未落盘，均无「已覆盖主域」可作同厂商参照，需外部知识定厂商）：`yipee.cc`（`3c.yipee.cc`）、`webpushr.com`（`analytics.` / `bot.` / `cdn.` 推送服务）、`cyntelli.com`（`caesar-api.` / `cpt.`）、`canvasjs.com`（图表库）、`firstpromoter.com`（联盟 SaaS）、`jquery.com`（`code.jquery.com` CDN）、`yadro.ru`（`counter.yadro.ru` 俄系统计埋点，疑广告追踪）、`reincubate.com`（`di-api.`）、`adgeek.net`（`echo.` / `r.` 广告）、`imei.org`、`imei.info`、`iunlocker.com`、`gtranslate.net`（`tdns3.`）、`fontawesome.com`（`use.` CDN）、`wrappixel.com`、`apeaksoft.com`、`i4.cn`（`d-image.` / `url.` / `www.`，疑爱思助手）、`volceapplog.com`（`mcs.volceapplog.com`，疑火山引擎应用日志，但发起进程为 firefox，无字节系进程证据），以及上轮遗留 `oceanengine.com`（`athena-api.`）。
- 重复检查：`python3 scripts/find_duplicates.py` 扫描 42 个文件，跨文件重复 1 项、文件内 0 项 —— 仅 `DOMAIN-SUFFIX,settings.crashlytics.com`（direct.yaml / google.yaml）历史基线，本次新引入 0 项（脚本退出码 1 系该历史项所致）。语法校验：baidu.yaml（payload 3 条）、microsoft.yaml（payload 71 条）均通过 `yaml.safe_load`。
- Git：feature/workbuddy-add-log-domain 提交 `ab077f0` → main `--no-ff` 合并 `11291cb` → `git push origin main`（`c444b06..11291cb`）→ 同步状态 `0  0` → 切回 feature。
- **环境变更（重要）**：本机 git 配置的代理 `http://127.0.0.1:7893` 本次不可用（无监听进程），`git fetch` 直接报 `Failed to connect to 127.0.0.1 port 7893`；实测 GitHub 直连可达（curl 200），故本次全部 git 操作改用 `git -c http.proxy= -c https.proxy=` 临时禁用代理执行，fetch/pull/push 均成功。RDAP 等外网查询若仍需代理，须先确认 7893 是否恢复。

## 2026-10-11 漏网之鱼归类：bytedanceapi.com 归入 bytedance.yaml（自动化运行，昨日日志零新增）

- 数据来源（主目标）：`log/clashx-meta-log/2026-10-10_10-25-01`（昨日日志，已由本日上午的运行复制入库）。提取未被本仓库规则覆盖的目标去重后：`match Match` 域名 9 个、裸 IP 0 个；`oc-cn-domain` 域名 86 个（以 `*.edge.mountaintoys.cn` CDN 节点名与 `*.mcdn.bilivideo.cn` 缩略图实例名为主，主域高度集中）、裸 IP 1 个（`120.53.53.53`）。
- **昨日日志零新增**：9 个 match Match 域名逐项核验全部已覆盖或属历史已判定项 —— `contrib.rocks`（github.yaml）、`deepwiki.com` / `railway.com` / `zeabur.com` / `www.onorca.dev` / `dl.macked.site`（proxy.yaml，均为 2026-10-11 人工裁决落盘）、`cdn.ripperhe.com`（direct.yaml 精确 `DOMAIN,` 规则）、`etahub.com` / `static.cloudflareinsights.com`（reject.yaml 上游已收录，历史跳过）。oc-cn-domain 侧 `weixin.com`（wechat.yaml）、`hellogithub.com` / `zvo.cn` / `bobtranslate.com` / `gitcode.com`（direct.yaml）、`copilot.tencent.com` / `lightai.cloud.tencent.com`（tencent.yaml）均已覆盖；裸 IP `120.53.53.53` 由 direct.yaml:274 `IP-CIDR,120.53.53.53/32,no-resolve` 覆盖。
- **差集检查（本次新增发现）**：源目录 `~/.config/clash.meta/logs/` 有、仓库 `log/clashx-meta-log/` 无的历史日志目录共 5 个 —— `2026-10-01_09-40-31`、`2026-10-01_10-09-27`、`2026-10-01_10-32-57`、`2026-10-03_08-54-53`、`2026-10-04_10-20-36`，已一并 `cp -R` 入库（差集复核输出为空）并提取补处理。经 changelog 比对，10-01 / 10-04 对应日期此前已有处理记录（2026-09-30 / 10-01 / 10-04 条目：`zoro.build`→direct.yaml、`nube.sh` / `pynesys.io` / `pynecore.org`→proxy.yaml、`longbridge.cn`→hk-broker.yaml、`investsmatters.com` 判 NXDOMAIN 不归类），缺的只是仓库 `log/` 副本，属复制约定缺口而非漏跑；`2026-10-03` 目录无对应 changelog 条目。
- 补录 1 个域名 / 1 个文件：`bytedance.yaml` 新增「字节系 API（2026-10-11 漏网之鱼补录）」分组 +1 —— `DOMAIN-SUFFIX,bytedanceapi.com`。依据：源自 `2026-10-03` 日志的 `imagex.bytedanceapi.com`（`Trae CN Helper` 发起 8 次，oc-cn-domain 命中），与文件内已覆盖 `bytedance.com` 同厂商、品牌直接体现在域名内，且进程为字节系 Trae，属「同厂商无歧义兄弟域」，payload 18 → 19 条。
- 待人工确认 19 项（未落盘，均无「已覆盖主域」可作同厂商参照，需外部知识定厂商）：`hisball.com`（Chrome Helper，无产品指向）、`qiyukf.com` + `127.net`（firefox，疑网易七鱼 / 网易 NOS）、`centralnic.com`（`rdap.centralnic.com`，curl 发起，RDAP 端点，建议归 direct.yaml「域名查询 / RDAP」分组）、`gdzwfw.gov.cn` / `gd.gov.cn` / `sz.gov.cn`（firefox，国内政务站）、`browserleaks.net`、`fastly-analytics.com`、`surfsharkdns.com`、`icanhazip.com`、`sibforms.com`、`trendshift.io`、`iconscout.com`、`nocobase.com`、`schemastore.org`、`111666.best`、`123169.xyz`，以及上轮遗留的 `oceanengine.com`（`athena-api.oceanengine.com`）。
- 跳过（历史已判定，不重复添加）：`antpeak.com` / `hibchr.com` / `zorvian.com`（2026-10-04 判定无主广告/追踪端点）；`etahub.com` / `cloudflareinsights.com` / `clarity.ms`（reject.yaml 上游收录）；`investsmatters.com`（2026-09-30 判 NXDOMAIN 域名失效，不归类）。
- 重复检查：`python3 scripts/find_duplicates.py` 扫描 42 个文件，跨文件重复 1 项、文件内 0 项 —— 仅 `DOMAIN-SUFFIX,settings.crashlytics.com`（direct.yaml / google.yaml）历史基线，本次新引入 0 项。语法校验：bytedance.yaml（payload 19 条）通过 `yaml.safe_load`。
- Git：feature/workbuddy-add-log-domain 提交 `b6e4c20` → main `--no-ff` 合并 `11a2315` → `git push origin main`（`6d4ec95..11a2315`）→ 同步状态 `0  0` → 切回 feature。
- 勘误：本次提交信息中「其余 13 个未覆盖候选域名」为笔误，实际待人工确认 19 项（以本节清单为准）。教训：提交前先算准计数再写入提交信息。

## 2026-10-11 漏网之鱼归类：feishucdn.com 归入 bytedance.yaml（skill v2.1.0 feature 分支循环首次实跑）

- 数据来源：`log/clashx-meta-log/2026-10-11_08-33-37`（差集检查发现源目录有、仓库 `log/` 无；10-10 与 10-09 已在今日两次运行中处理完毕）。提取未被本仓库规则覆盖的目标去重后：`match Match` 域名 12 个、裸 IP 0 个；`oc-cn-domain` 域名 3 个、裸 IP 1 个（`120.53.53.53`，已覆盖）。
- **本次为 skill v2.1.0 新流程（feature 分支循环）的首次实跑验证**，按自动化默认策略执行 review 环节（不调用 AskUserQuestion）。
- 补录 1 个域名 / 1 个文件：`bytedance.yaml`「Feishu / 飞书」分组 +1 —— `DOMAIN-SUFFIX,feishucdn.com`。依据：源自 `lf-imfile-cn.feishucdn.com`（`Lark Helper` 发起，oc-cn-domain 命中），`feishucdn.com` 是已收录 `feishu.cn` 的同厂商 CDN 兄弟域，语义零歧义，payload 17 → 18 条。
- 整批跳过（已被现有规则覆盖，非规则缺失）：`www.` / `c.` / `c6.` / `t.` / `b.stats.` / `slc.stats.` / `ddbm2.` 共 7 个 paypal.com 子域（`us-payment.yaml` 已有 `DOMAIN-SUFFIX,paypal.com`）；`rdap.org` / `rdap.verisign.com`（direct.yaml 域名查询 / RDAP 分组）；`lightai.cloud.tencent.com`（`tencent.yaml:22` 今日已收录，oc-cn-domain 命中系规则集评估优先级）；裸 IP `120.53.53.53`（direct.yaml 中国移动分组）。
- 跳过（历史已判定，不重复添加）：`antpeak.com`、`hibchr.com`、`zorvian.com`（2026-10-04 判定为无主广告/追踪端点）；`monitor_browser`（无 TLD 伪域名，提取脚本已过滤）。
- 待人工确认 1 项（未落盘）：`athena-api.oceanengine.com` —— 发起进程 `Lark Helper`，但 `oceanengine.com` 主域在本仓库无任何业务规则覆盖（仅 reject.yaml 上游有 `ad.` / `analytics.` 子域），判定厂商需外部知识，且属广告域，不满足「同厂商无歧义兄弟域」补录条件。
- 重复检查：`python3 scripts/find_duplicates.py` 扫描 42 个文件，跨文件重复 1 项、文件内 0 项 —— 仅 `DOMAIN-SUFFIX,settings.crashlytics.com`（direct.yaml / google.yaml），为编辑前历史基线，本次新引入 0 项。语法校验：bytedance.yaml（payload 18 条）通过 `yaml.safe_load`。
- Git（v2.1.0 feature 分支循环首次实跑）：第 0 步 fetch → main pull --rebase（`0 0`）→ feature rebase main → feature 提交 `57cae78` → main `--no-ff` 合并 `6d4ec95` → `git push origin main`（`aa2cf28..6d4ec95`）→ 同步状态 `0  0` → 切回 feature。
- **踩坑（已回补进 SKILL.md 第 14 节）**：`git merge --no-ff` 在无交互终端下会打开编辑器等待输入，进程被 SIGTERM 终止（退出码 137），留下 `.git/MERGE_HEAD` 残留。合并内容本身无冲突，改用 `git commit -m` 补完即可。skill 中已改用 `git merge --no-ff --no-edit` 或 `git merge --no-ff -m "<信息>"`。

## 2026-10-11 PayPal 域名归并至 us-payment.yaml，删除空的 paypal.yaml

- 起因：用户要求把 `paypal.com` / `paypalobjects.com` 添加到 `paypal.yaml`。查证发现两者**均已被收录** —— `paypal.com` 在 `us-payment.yaml:4`（同组另有 10 条精确子域`c.` / `d.` / `t.` / `pics.` / `hcaptcha.` 等），`paypalobjects.com` 在 `direct.yaml:116`（混在按字母序排的杂项站点区）。直接追加到 `paypal.yaml` 会立即触发 `find_duplicates.py` 门禁（跨文件重复由2 项升至 4 项），故先向用户确认处理方式。
- 用户裁决：**归并到 us-payment.yaml**，不保留独立的 paypal.yaml。
- 具体变更：
  - `us-payment.yaml`「PayPal」分组 +1：`DOMAIN-SUFFIX,paypalobjects.com`。
  - `direct.yaml` -1：移除杂项区的 `DOMAIN-SUFFIX,paypalobjects.com`（payload 239 → 238 条）。
  - 删除 `paypal.yaml`（`git rm`）—— 该文件仅有无效占位行 `DOMAIN-SUFFIX,`，与 `steam.yaml` 共享同一条空占位，是跨文件重复历史基线之一。删除后 README「规则文件」表同步移除该行。
  - `scripts/DUPLICATES.md`（入库生成物）随重复检查结果更新。
- 重复检查：**跨文件重复由 2 项降至 1 项** —— `DOMAIN-SUFFIX,` 空占位（paypal/steam）随文件删除消失，仅余 `DOMAIN-SUFFIX,settings.crashlytics.com`（direct.yaml / google.yaml）。文件内重复 0 项。扫描文件数 43 → 42。
- 语法校验：direct.yaml（payload 238 条）、us-payment.yaml（16 条）均通过 `yaml.safe_load`。
- 提交前远程已同步（`0	0`）。提交：aa2cf28，已推送 origin/main（推送后 `0	0`）。

## 2026-10-11 漏网之鱼归类：11 项待确认域名按人工裁决落盘（direct +4 / proxy +6 / github +1）

- 数据来源：`log/clashx-meta-log/2026-10-10_10-25-01`（复制自 `~/.config/clash.meta/logs`）。提取未被本仓库规则覆盖的目标去重后：`match Match` 域名 9 个、裸 IP 0 个；`oc-cn-domain` 域名约 80 个（以 `*.edge.mountaintoys.cn` CDN 节点名与 `*.mcdn.bilivideo.cn` 缩略图实例名为主，主域高度集中）、裸 IP 1 个（`120.53.53.53`）。归并主域后 22 个待判主域。
- **本次为人工会话运行，完整执行 skill v2.0.0 的 `AskUserQuestion` 确认环节**，对 4 组候选归属由用户逐项裁决；其中用户对三个国内域名的「疑似国内」判断要求先查注册信息确认，故补走RDAP + DoH 流程。
- **补录 11 个域名、3 个文件**：
  - `direct.yaml`「其他国内站点（2026-10-11 漏网之鱼补录）」+4：`hellogithub.com` / `zvo.cn` / `bobtranslate.com` / `gitcode.com`。前三项经 RDAP + DoH 确认为国内站点 —— `hellogithub.com` NS 为 `DNS29/30.HICHINA.COM`（阿里云万网，2017 注册）；`bobtranslate.com` NS 为 `VIP1/2.ALIDNS.COM`（阿里云，2022 注册，与已有 `cdn.ripperhe.com` 同作者）；`zvo.cn` A 记录落 `123.60.240.82/83`（阿里云杭州）、`api.translate.zvo.cn` 落 `209.209.9.89`。三项注册商字段均为空数组（隐私保护），但NS/A 记录已足以判定归属。`gitcode.com`（A 记录 `116.205.6.180`，国内 IP）由用户直接裁决归direct。
  - `proxy.yaml` 新增 4 个分组 +6：`railway.com` / `zeabur.com`（海外 PaaS，A 记录分别为 `69.46.46.46` / `38.32.110.58`，境外）；`deepwiki.com`（Cognition AI 代码文档站）/ `onorca.dev`（`Orca Helper` 23 次，桌面端 AI 编程工具）；`macked.site`（用户判定为 Mac 资源站，`dl.macked.site` 落 Cloudflare）；`turingfraud.net`（疑似风控/反欺诈，落 `43.163.16.160`）。
  - `github.yaml`「GitHub 相关工具（2026-10-11 漏网之鱼补录）」+1：`contrib.rocks` —— GitHub README 贡献者头像服务，用户裁决归 github.yaml 保持语义内聚。
- 用户裁决不归类：`vsassets.io`（`anthropic.gallery.vsassets.io` / `anthropic.gallerycdn.vsassets.io`，来自 2026-10-09 日志）。
- 已覆盖整批跳过（命中外部 oc-cn-domain 规则集属规则集评估优先级，非规则缺失）：bilibili 系（bilibili.com / biliimg.com / hdslb.com / bilivideo.com / bilivideo.cn / biligame.com → bilibili.yaml）、微信系（weixinbridge.com / qpic.cn / qlogo.cn / weixin.com → wechat.yaml）、mountaintoys.cn → direct.yaml；裸 IP `120.53.53.53` 已由 direct.yaml 中国移动分组 `IP-CIDR,120.53.53.53/32` 覆盖。
- 跳过（历史已判定，不重复添加）：`etahub.com` —— changelog 2026-09-30 已记录其由 reject.yaml 上游收录；`cloudflareinsights.com` —— 同为 reject.yaml 上游已收录（Cloudflare Web Analytics 埋点）；`cdn.ripperhe.com` —— direct.yaml:209 已有精确规则 `DOMAIN,cdn.ripperhe.com`。
- 未归类（沿用历史裁决）：`antpeak.com`、`hibchr.com`、`zorvian.com`（2026-10-04 已判定为无主广告/追踪端点，本次日志未再现）。
- 重复检查：`python3 scripts/find_duplicates.py` 报跨文件重复 2 项、文件内0 项，均为编辑前历史遗留（`DOMAIN-SUFFIX,` 空占位存在于 paypal.yaml / steam.yaml；`DOMAIN-SUFFIX,settings.crashlytics.com` 存在于 direct.yaml / google.yaml），本次新引入 0 项。语法校验：direct.yaml（payload 239 条）、proxy.yaml（843 条）、github.yaml（10 条）均通过 `yaml.safe_load`。
- 提交前远程已同步（`git rev-list --left-right --count origin/main...HEAD` 输出 `0	0`），工作区仅本次三文件改动。
- 提交：f721767，已推送 origin/main（推送后同步状态 `0	0`）。

## 2026-10-11 漏网之鱼归类：copilot.tencent.com / lightai.cloud.tencent.com 归入 tencent.yaml（自动化运行）

- 数据来源：`log/clashx-meta-log/2026-10-10_10-25-01`（昨日日志，主目标）。另发现 `2026-10-09_09-45-38` 从未被处理（changelog 顶部此前为 2026-10-08 条目、仓库 `log/` 下亦无该目录），本次一并补处理以闭合覆盖缺口。
- **提取结果（2026-10-10）**：`match Match` 域名 9 个、裸 IP 0 个；`oc-cn-domain` 域名约 80 个（仍以 `*.edge.mountaintoys.cn` CDN 节点名与 `*.mcdn.bilivideo.cn` 图片缩略图实例名为主，主域高度集中）、裸 IP 1 个（`120.53.53.53`）。归并主域后 22 个待判主域。
- **提取结果（2026-10-09）**：`match Match` 域名 2 个、裸 IP 0 个；`oc-cn-domain` 域名约 33 个（bilibili 系 + 微信系 + 腾讯子域）、裸 IP 1 个（`120.53.53.53`）。归并主域后全部为已覆盖主域，仅 1 个新主域。
- **本次为无人值守定时自动化运行，无法执行 skill v2.0.0 强制的 `AskUserQuestion` 确认环节。** 沿用 2026-10-07 起约定默认策略：仅补录「与已覆盖主域同厂商、语义无歧义的兄弟域」；其余存疑项一律不落盘，留待人工确认（见下方清单）。
- 补录 1 个分组 2 条（`tencent.yaml` 新增「腾讯子域补充（2026-10-11 漏网之鱼补录）」）：
  - `DOMAIN-SUFFIX,copilot.tencent.com` —— 源自 `copilot.tencent.com`（`CodeBuddy CN Helper` 1 次 + `Electron` 1 次，oc-cn-domain 命中）。为 `*.tencent.com` 精确子域，与文件内已有 `ardot.tencent.com` / `galileotelemetry.tencent.com` 同主域、同 CodeBuddy 语义，无歧义。主域 `tencent.com` 按既定约定不做整体兜底（会与 hk-bank.yaml 的 `tpns.hk.tencent.com` 分组语义冲突），故仍用精确子域写法。
  - `DOMAIN-SUFFIX,lightai.cloud.tencent.com` —— 源自 `lightai.cloud.tencent.com`（`Electron` 1 次，oc-cn-domain 命中）。`*.cloud.tencent.com` 为腾讯云自有域名空间，归属腾讯无歧义，随同批补入。
- 已覆盖整批跳过（命中外部 oc-cn-domain 规则集属规则集评估优先级，非规则缺失）：bilibili 系（bilibili.com / biliimg.com / hdslb.com / bilivideo.com / bilivideo.cn / biligame.com → bilibili.yaml）、微信系（weixinbridge.com / qpic.cn / qlogo.cn / weixin.com → wechat.yaml）、mountaintoys.cn → direct.yaml；裸 IP `120.53.53.53` 已由 direct.yaml 中国移动分组 `IP-CIDR,120.53.53.53/32` 覆盖。
- 跳过（历史已判定，不重复添加）：
  - `etahub.com`（firefox 10 次）—— 2026-10-08 / 更早 changelog 已记录由 reject.yaml 上游收录。
  - `cloudflareinsights.com`（`static.cloudflareinsights.com`，firefox 2 次）—— changelog「跳过项」段已记录由 reject.yaml 上游收录（Cloudflare Web Analytics 埋点）。
  - `cdn.ripperhe.com`（firefox 24 次）—— direct.yaml 第 209 行已有精确规则 `DOMAIN,cdn.ripperhe.com`（Bob 翻译作者 CDN），已覆盖。
- 待人工确认（本次不落盘，粗判依据如下；无「已覆盖主域」可作同厂商参照，故一律不自行拍板）：
  - `contrib.rocks`（com.apple.WebKit.Networking 1 次）—— GitHub README 贡献者头像服务。
  - `deepwiki.com`（com.apple.WebKit.Networking 1 次）—— Cognition 的 AI 代码文档站，疑需代理。
  - `macked.site`（`dl.macked.site`，firefox 2 次）—— 疑 macOS 软件下载站（macked），疑可直连；主域 `macked.com` 未被本仓库覆盖。
  - `railway.com`（com.apple.WebKit.Networking 1 次）—— 海外 PaaS，疑需代理。
  - `zeabur.com`（com.apple.WebKit.Networking 1 次）—— 海外 PaaS（中国台湾团队），疑需代理。
  - `www.onorca.dev`（`Orca Helper` 23 次）—— 桌面端 AI 编程工具，厂商归属无法本地确认。
  - `abroad.hellogithub.com`（com.apple.WebKit.Networking 1 次）—— 国内开源项目推荐站 HelloGitHub，疑可直连。
  - `api.translate.zvo.cn`（firefox 8 次）—— 国内开源翻译服务端点，疑可直连。
  - `bobtranslate.com`（firefox 2 次）—— 疑 Bob 翻译官网；direct.yaml 现有条目为精确 `DOMAIN,cdn.ripperhe.com`（非主域规则），不构成「已覆盖主域」，故未按兄弟域补录。
  - `gitcode.com`（com.apple.WebKit.Networking 1 次）—— CSDN 旗下代码托管；本仓库无任何 CSDN 域名可作同厂商参照。
  - `www.turingfraud.net`（无进程提示）—— 疑似风控/反欺诈服务，厂商不明。
  - `vsassets.io`（`anthropic.gallery.vsassets.io` / `anthropic.gallerycdn.vsassets.io`，`Code Helper` 各 2 次，来自 2026-10-09 日志）—— 疑似 Visual Studio Marketplace 资产 CDN；`vsassets` 域名本身无产品指向，且 microsoft.yaml 现有条目（`visualstudio.com` / `vscode-cdn.net` / `vscode-unpkg.net`）中无同名可参照项，故不按「同厂商无歧义」补录。
  - 上期遗留未再出现：`mmcdn.com`、`agego.com`、`tracesof.net`、`ethyca.com`、`proigor.com`、`kejitt.top`、`vzuu.com`（保持不落盘）。
- 未归类（沿用历史裁决，不重复提问）：`antpeak.com`、`hibchr.com`、`zorvian.com`（2026-10-04 已判定为无主广告/追踪端点，本次日志未再现）。
- 重复检查：`python3 scripts/find_duplicates.py` 跨文件重复 2 项、文件内 0 项，均为编辑前历史遗留（`DOMAIN-SUFFIX,` 空占位存在于 paypal.yaml / steam.yaml；`DOMAIN-SUFFIX,settings.crashlytics.com` 存在于 direct.yaml / google.yaml），本次新引入 0 项。语法校验：tencent.yaml 通过 `yaml.safe_load`（payload 13 条）。
- 提交前远程有新提交（reject.yaml 自动合并 f9eee7c，+5257 行），工作区干净，已 `git pull --rebase` 快进同步。
- 提交：af26864，已推送 origin/main（推送后 `git rev-list --left-right --count origin/main...HEAD` 输出 `0	0`）。

## 2026-10-08 漏网之鱼归类：xvideos-cdn.com / xvideos.net 归入 pornhub.yaml（自动化运行）

- 数据来源：`log/clashx-meta-log/2026-10-08_09-27-03`（复制自 `~/.config/clash.meta/logs`，含 clashx_core 3 个 + clashx_mihomo + clashx，共 6 个文件）。提取未被本仓库规则覆盖的目标去重后：`match Match` 域名 9 个、裸 IP 0 个；`oc-cn-domain` 域名约 100 个（主要为 `*.edge.mountaintoys.cn` CDN 节点名与 `*.mcdn.bilivideo.cn` 图片缩略图实例名，数量大但主域高度集中）、裸 IP 1 个（`120.53.53.53`）。归并主域后共 18 个待判主域（oc-cn-domain 12 + match Match 6）。
- **本次为无人值守的定时自动化运行，无法执行 skill v2.0.0 强制的 `AskUserQuestion` 确认环节。** 沿用 2026-10-07 约定默认策略：仅补录与「已覆盖主域」同厂商、语义无歧义的兄弟域；其余存疑项一律不落盘，留待人工在会话中确认。
- 已覆盖整批跳过（命中外部 oc-cn-domain 规则集属规则集评估优先级，非规则缺失）：bilibili 系（bilibili.com / biliimg.com / hdslb.com / bilivideo.com / bilivideo.cn / biligame.com → bilibili.yaml）、微信系（weixinbridge.com / qpic.cn / qlogo.cn → wechat.yaml）、mountaintoys.cn → direct.yaml、tencent.com / gtimg.com → tencent.yaml；裸 IP `120.53.53.53` 已由 direct.yaml 中国移动分组 `IP-CIDR,120.53.53.53/32` 覆盖。
- 补录 2 个主域（`pornhub.yaml` 既有 `# === xvideos ===` 分组下追加，沿用该文件「站点主域 + 同名 CDN 域」成组约定，与 pornhub+phncdn / youporn+ypncdn / redtube+rdtcdn 一致）：
  - `DOMAIN-SUFFIX,xvideos-cdn.com` —— 源自 `assets-cdn77.xvideos-cdn.com` / `thumb-cdn77.xvideos-cdn.com` / `thumbs-gcore.xvideos-cdn.com`（firefox 各 6 次），xvideos 自有视频/缩略图 CDN，与已覆盖 `xvideos.com` 同厂商。
  - `DOMAIN-SUFFIX,xvideos.net` —— 源自 `info.xvideos.net`（firefox 1 次），xvideos 备用主域。
- 跳过（历史已判定，不重复添加）：`etahub.com` —— changelog 2026-09-30 已记录其由 reject.yaml 上游收录（GitHub Actions 维护，本地禁止编辑），本次日志再现（firefox 6 次）仍按规则跳过。
- 待人工确认（本次不落盘，粗判依据如下）：
  - `mmcdn.com`（`thumb.live.mmcdn.com`，firefox 12 次）—— live 缩略图 CDN，语义偏成人视频类，但主域与已覆盖的 xvideos 无名称关联，厂商归属无法本地确认。
  - `agego.com`（`myapi.agego.com` / `verifycdn.agego.com`，firefox 各 4 / 1 次）—— `verify*` 子域疑为年龄验证类服务端点，厂商不明。
  - `tracesof.net`（firefox 1 次）—— 语义不明，无产品指向。
  - 上期遗留未再出现的待确认项：`ethyca.com`、`proigor.com`、`kejitt.top`、`vzuu.com`、`static.cloudflareinsights.com`（本次日志未命中，保持不落盘）。
- 未归类（沿用历史裁决，不重复提问）：`antpeak.com`、`hibchr.com`、`zorvian.com` —— 2026-10-04 已由用户判定为无主广告/追踪端点。
- 重复检查：`python3 scripts/find_duplicates.py` 跨文件重复 2 项、文件内 0 项，均为编辑前历史遗留（`DOMAIN-SUFFIX,` 空占位存在于 paypal.yaml / steam.yaml；`DOMAIN-SUFFIX,settings.crashlytics.com` 存在于 direct.yaml / google.yaml），本次新引入 0 项。语法校验：pornhub.yaml 通过 `yaml.safe_load`。
- 提交前远程有新提交（reject.yaml 自动合并 be9033d，+606 行），已按流程 `git stash` → `git pull --rebase` → `git stash pop` 同步。
- 提交：4299b51，已推送 origin/main（推送后 `git rev-list --left-right --count origin/main...HEAD` 输出 `0	0`）。

## 2026-10-07 漏网之鱼归类：zhimg.com / bdstatic.com / gtimg.com 按厂商补录（自动化运行）

- 数据来源：`log/clashx-meta-log/2026-10-07_10-26-33`（复制自 `~/.config/clash.meta/logs`，含 clashx_core 3 个 + clashx_mihomo + clashx，共 6 个文件）。提取未被本仓库规则覆盖的目标去重后：`match Match` 域名 10 个、裸 IP 4 个；`oc-cn-domain` 域名约 100 个（主要为 `*.edge.mountaintoys.cn` CDN 节点名与 `*.mcdn.bilivideo.cn` 图片缩略图实例名，数量大但主域高度集中）、裸 IP 1 个。归并主域后共 27 个待判主域（oc-cn-domain 17 + match Match 10）。
- **本次为无人值守的定时自动化运行，无法执行 skill v2.0.0 强制的 `AskUserQuestion` 确认环节。** 采用保守默认策略：仅补录与「已覆盖主域」同厂商、语义无歧义的兄弟域；其余存疑项一律不落盘，留待人工在会话中确认（见下方「待人工确认」）。
- 已覆盖整批跳过（命中外部 oc-cn-domain 规则集属规则集评估优先级，非规则缺失）：bilibili 系（bilibili.com / bilivideo.com / bilivideo.cn / biliimg.com / hdslb.com / biligame.com → bilibili.yaml）、微信系（weixinbridge.com / qpic.cn / qlogo.cn → wechat.yaml）、jsdelivr.net / mountaintoys.cn / zhihu.com / aikobo.cn / smallstrawberry.com → direct.yaml、baidu.com → baidu.yaml；裸 IP `1.0.0.1` / `1.1.1.1` / `8.8.4.4` / `8.8.8.8` / `120.53.53.53` 均已被现有规则覆盖。
  - **2026-10-17 复查补记**：`sub1.smallstrawberry.com` 当日命中 8 次，但全部是 `(match Match/)` 错误行格式，按 `match Match using` 行提取的流程覆盖不到该格式，导致原条目整条遗漏（既未入已覆盖也未入待人工）。该域 `direct.yaml` 早已覆盖，不影响补录结果；**提取口径必须同时覆盖两种行格式**（已写入 AGENTS.md「changelog 编写约束」统计口径）。
- 补录 3 个主域（均为已覆盖主域的同厂商兄弟域，无歧义）：
  - `direct.yaml`「其他国内站点」分组追加 `DOMAIN-SUFFIX,zhimg.com` —— 知乎图片 CDN（`pic1.zhimg.com` / `pica.zhimg.com` / `picx.zhimg.com` / `static.zhihu.com` 等，firefox 发起），与同组已有 `zhihu.com` 同系。
  - `baidu.yaml` 追加 `DOMAIN-SUFFIX,bdstatic.com` —— 百度静态资源 CDN（`zz.bdstatic.com`），与已有 `baidu.com` 同系。
  - `tencent.yaml` 新增「腾讯静态资源（2026-10-07 漏网之鱼补录）」分组：`DOMAIN-SUFFIX,gtimg.com` —— 腾讯静态资源域名（`docs.gtimg.com` / `docs2.gtimg.com`，由 `WorkBuddy Helper` 进程发起 26/10 次，属腾讯系）。
- 待人工确认（本次不落盘，粗判依据如下）：
  - `ethyca.com`（`bitly.fides-cdn.ethyca.com`，firefox）—— Ethyca 为隐私合规厂商，Fides 为其同意管理 SDK，疑似追踪/合规类，建议归 `proxy.yaml` 或告知 reject.yaml 覆盖情况。
  - `etahub.com`（firefox，66 次）—— 高频访问，域名语义与归属厂商不明。
  - `proigor.com`（`Google Chrome Helper`，1 次）—— 无产品指向。
  - `kejitt.top`（`www.kejitt.top`，firefox，1 次）—— 疑似国内 .top 站点。
  - `vzuu.com`（`vdn3.vzuu.com`，firefox，1 次）—— 疑似网易视频 CDN，`vdn` 子域结构指向视频分发网络。
  - `static.cloudflareinsights.com` —— Cloudflare Web Analytics 埋点端点，分析/追踪类，与 `clarity.ms` 同性质，未核对 reject.yaml（按规定禁止查询）。
- 未归类（沿用历史裁决，不重复提问）：`antpeak.com`、`hibchr.com`、`zorvian.com` —— 2026-10-04 / 2026-10-05 / 2026-10-06 已由用户判定为无主广告/追踪端点。
- 重复检查：`python3 scripts/find_duplicates.py` 跨文件重复 2 项、文件内 0 项，均为编辑前历史遗留（`DOMAIN-SUFFIX,` 空占位存在于 paypal.yaml / steam.yaml；`DOMAIN-SUFFIX,settings.crashlytics.com` 存在于 direct.yaml / google.yaml），本次新引入 0 项。语法校验：direct.yaml、baidu.yaml、tencent.yaml 均通过 `yaml.safe_load`。
- 提交前远程已同步（首次 `git fetch` 因网络瞬时故障报 `SSL_ERROR_SYSCALL`，重试后成功，`git rev-list --left-right --count origin/main...HEAD` 输出 `0	0`）。
- 提交：7ace9e1，已推送 origin/main（推送后同步校验输出 `0	0`）。

## 2026-10-06 漏网之鱼归类：微信主域 weixin.com、aikobo.cn 补录

- 数据来源：`log/clashx-meta-log/2026-10-06_10-20-03`（复制自 `~/.config/clash.meta/logs`，含 clashx_core 与 clashx_mihomo 共 5 个日志文件），提取未被本仓库规则覆盖的目标去重后，`match Match` 3 个（均为已知无主端点）、`oc-cn-domain` 域名约 130 个（主要为 bilibili 系 CDN 的 `*.mcdn.bilivideo.cn` 图片缩略图实例名与 `*.edge.mountaintoys.cn` CDN 节点名，数量大但主域高度集中），归并主域后共 28 个。
- 26 个主域已被现有 `DOMAIN-SUFFIX` 覆盖，整批跳过（命中外部 OpenClash CN 规则集属规则集评估优先级，非规则缺失）：bilibili 系（bilibili.com / bilivideo.com / bilivideo.cn / biliimg.com / hdslb.com / biligame.com → bilibili.yaml）、微信系（weixinbridge.com / qpic.cn / qlogo.cn → wechat.yaml）、中国移动系（10086.cn / chinamobile.com / online-cmcc.cn / cmcc-cs.cn / komect.com / mmarket.com / miguvideo.com→ direct.yaml）、BOSS 直聘系（zhipin.com / bosszhipin.com / kanzhun.com → direct.yaml）、baidu.com → baidu.yaml、zztfly.com → xhs.yaml、mountaintoys.cn → direct.yaml、裸 IP `120.53.53.53` → direct.yaml。
- 经用户裁决补录2 个主域：
  - `wechat.yaml` 新增「微信主域（2026-10-06 漏网之鱼补录）」分组：`DOMAIN-SUFFIX,weixin.com` —— 源自 `shortcloud.weixin.com`（WeChat 进程，4 次，命中 oc-cn-domain 走 DIRECT）。主域为微信官方服务，与文件内已有 `weixinbridge.com` / `qpic.cn` / `qlogo.cn` 同系；用户选择归wechat.yaml 而非 tencent.yaml，理由是保持微信系语义内聚、避免与 tencent.yaml 的精确子域分组冲突。
  - `direct.yaml` 新增「国内招聘 / 生活服务（2026-10-06 漏网之鱼补录）」分组：`DOMAIN-SUFFIX,aikobo.cn` —— 源自 `boss.aikobo.cn`（firefox 发起，仅 1 次）。域名 `boss.*` 子域结构与语义指向国内招聘类服务，用户裁决与 `zhipin.com` / `bosszhipin.com` / `kanzhun.com` 同组归direct.yaml。
- 未归类：`antpeak.com`、`hibchr.com`、`zorvian.com` —— 沿用 2026-10-04 changelog 中用户已作判定（Cloudflare NS + RDAP 无注册商 + 首页 429/空 + 直连超时 + 仅 `Google Chrome Helper` 进程，无主广告/追踪端点），本次不重复提问、不重复收录。
- 重复检查：`python3 scripts/find_duplicates.py` 跨文件重复 2 项、文件内 0 项，均为编辑前历史遗留（`DOMAIN-SUFFIX,` 空占位存在于 paypal.yaml / steam.yaml；`DOMAIN-SUFFIX,settings.crashlytics.com` 存在于 direct.yaml / google.yaml），本次新引入 0 项。语法校验：wechat.yaml、direct.yaml 均通过 `yaml.safe_load`。
- 提交前远程已同步（`git rev-list --left-right --count origin/main...HEAD` 输出 `0	0`），无需 rebase。
- 提交：a04c1a9，已推送 origin/main（推送后同步校验输出 `0	0`）。

## 2026-10-05 漏网之鱼归类：RDAP/证书工具端点、Spacelama、中国移动 IP 补录

- 数据来源：`log/clashx-meta-log/2026-10-05_06-43-41`（复制自 `~/.config/clash.meta/logs`），提取未被本仓库规则覆盖的目标去重后共 63 个（`match Match` 7 个、`oc-cn-domain` 55 个域名 + 1 个裸 IP）。
- oc-cn-domain 55 个域名全部已被现有 `DOMAIN-SUFFIX` 覆盖并整批跳过：bilibili 系（bilibili.com / bilivideo.com / bilivideo.cn / hdslb.com → bilibili.yaml）、微信系（weixinbridge.com / qpic.cn / qlogo.cn → wechat.yaml）、mountaintoys.cn → direct.yaml、zhipin.com → direct.yaml、codebuddy.cn / ardot.tencent.com / galileotelemetry.tencent.com → tencent.yaml。命中外部 OpenClash CN 规则集是规则集评估优先级问题，非规则缺失。
- match Match 归类（全部经用户裁决）：
  - `direct.yaml`新增「域名查询 / RDAP（2026-10-05 漏网之鱼补录）」分组：`verisign.com`（.com注册局 RDAP，`rdap.verisign.com`）、`crt.sh`（证书透明度日志搜索）。两者均为 Agent 执行域名归属查询时curl 产生的流量，与已有 `rdap.org` 同组。
  - `tencent.yaml` 新增 Spacelama 分组：`spacelama.com`（`blog.spacelama.com`，进程 WorkBuddy Helper；用户裁决归属腾讯）。
  - `direct.yaml` 新增「中国移动（2026-10-05 漏网之鱼补录）」分组：`IP-CIDR,120.53.53.53/32,no-resolve`（oc-cn-domain 命中裸 IP，mihomo 内核发起，用户裁决归中国移动）。
  - `rdap.org` 已由 `direct.yaml` 现有 `DOMAIN-SUFFIX,rdap.org` 覆盖，跳过。
- 未归类：`antpeak.com`、`hibchr.com`、`zorvian.com` —— 沿用 2026-10-04 changelog 中用户已作判定（Cloudflare NS + RDAP 无注册商 + 首页 429/空 + 直连超时 + 仅浏览器进程，无主广告/追踪端点），本次不重复提问、不重复收录。
- 重复检查：`python3 scripts/find_duplicates.py` 跨文件重复 2 项、文件内0 项，均为编辑前历史遗留（`DOMAIN-SUFFIX,` 空占位存在于 paypal.yaml / steam.yaml；`DOMAIN-SUFFIX,settings.crashlytics.com` 存在于 direct.yaml / google.yaml），本次新引入 0 项。语法校验：direct.yaml、tencent.yaml 均通过 `yaml.safe_load`。
- 提交前远程有新提交（reject.yaml 自动合并 738cad3），已按流程 stash → pull --rebase → stash pop 同步。
- 提交：e386cbf，已推送 origin/main（推送后 `git rev-list --left-right --count origin/main...HEAD` 输出 `0	0`）。

## 2026-10-05 README 文档整理（手动更新）

- 「使用建议」的「按需引用」与「示例」两条合并去重，删除重复表述。
- 「支持软件」列表补充「其他同类型软件」。
- 规则文件表中 `reject.yaml` 描述由「广告/追踪/恶意软件拦截（自动同步，勿手动编辑）」改为「广告/追踪/恶意软件拦截（推荐设置reject）」。
- 清理「反馈」段落前多余空行。
- 提交 4449d1b，已推送 origin/main。

## 2026-10-04 漏网之鱼归类：字节海外/ 运营商 / WPS / 腾讯等域名按厂商补录

- 数据来源：`log/2026-10-04_10-20-36`（复制自 `~/.config/clash.meta/logs`），提取未被本仓库规则覆盖的目标去重后共 204 个（`match Match` 18 个、`oc-cn-domain` 186 个），归并主域后为 54 个主域。
- match Match 归类：
  - `bytedance-global.yaml` 新增 TikTok 分组：`tiktok.com`（libraweb-sg.tiktok.com）、`ttwstatic.com`（TikTok 登录站点静态资源）、`byteoversea.com`（字节海外 SDK，mssdk-sg / mon-va 子域）；新增海外埋点分组 `bytedapm.com`、`ibytedapm.com`（字节 APM 埋点）；`Trae AI IDE` 分组追加 `traecdn.ai`（Trae 海外 CDN，lf16-web-neutral.traecdn.ai）。
  - `antpeak.com`、`hibchr.com`、`zorvian.com` **未归类**：三者均为 Cloudflare NS（ALEC/MARGE）、注册信息完全隐私保护、RDAP 无注册商与实体信息、首页 429 或空响应、直连超时，进程均为 `Google Chrome Helper` 且无产品指向，判定为无主广告/追踪类端点，无法确认业务归属，不入规则文件。
- oc-cn-domain 归类（`trae.ai` 等已被现有 `DOMAIN-SUFFIX` 覆盖的主域整批跳过）：
  - `direct.yaml` 新增中国移动分组（2026-10-04）：`10085.cn`、`5gnewcall.cn`、`cmicapm.com`（urlscan 记录 data.cmicapm.com 属China Mobile Group Guangdong）、`cmicrwx.cn`（注册人为中移互联网有限公司）、`gmcc.net`、`migu.cn`（咪咕）；新增金山办公 WPS 分组：`wps.cn`、`wpscdn.cn`、`qwps.cn`、`ksosoft.com`、`ksord.com`（进程 wpscloudsvr / wpsoffice，shuc-other.ksord.com 出现 104 次）；新增国内招聘/生活服务分组：`zhipin.com`、`bosszhipin.com`、`kanzhun.com`（BOSS 直聘系）、`c-ctrip.com`（携程图片CDN）；新增域名查询分组 `ipip.net`。
  - `bytedance.yaml` 新增字节系图片/对象存储 `bytetos.com`、`byteacctimg.com`（账号头像图片），新增 MarsCode 分组 `marscode.cn`。
  - `tencent.yaml` 新增 `codebuddy.cn`（CodeBuddy 下载源）、`ardot.tencent.com`、`galileotelemetry.tencent.com`（伽利略遥测）；未使用 `DOMAIN-SUFFIX,tencent.com` 主域，避免与 hk-bank.yaml 的 `tpns.hk.tencent.com` 分组语义冲突。
  - `google.yaml` 核心域名分组新增 `google.cn`。
  - `clarity.ms`未添加：2026-10-01 记录该域已由 reject.yaml 上游收录，重复添加无意义。
- 重复检查：`python3 scripts/find_duplicates.py` 退出码 1，报告仅剩历史遗留 2 项（`DOMAIN-SUFFIX,` 占位行存在于 paypal.yaml / steam.yaml；`DOMAIN-SUFFIX,settings.crashlytics.com` 存在于 direct.yaml / google.yaml），本次编辑新引入 0 项。语法校验：bytedance / bytedance-global / direct / google / microsoft / tencent 六个文件均通过 `yaml.safe_load`。
- 提交：4388806（主提交）、84c8283（回退 clarity.ms），已推送 origin/main。

## 2026-10-01 漏网之鱼归类：larksuite.com / longbridge.cn 补录

- `DOMAIN-SUFFIX,larksuite.com` 新增至 `bytedance-global.yaml`（Lark 国际版主域，与已有国内 feishu.cn 相对；源自 2026-10-01 日志 oc-cn-domain 命中）。
- `DOMAIN-SUFFIX,longbridge.cn` 新增至 `hk-broker.yaml`（长桥证券国内版主域，与已有 longbridge.com 相对）。
- `clarity.ms`（微软 Clarity Web Analytics）未收录：reject.yaml 上游已收录（分析/追踪类），与 jpush/jiguang 同例不重复添加。
- 重复检查：larksuite.com、longbridge.cn 无跨文件/文件内重复；microsoft.yaml 语法校验通过。
- 附带：changelog.md 取消 git 跟踪、改为纯本地维护（仓库先例为 AGENTS.md / CLAUDE.md，见 244a7bd）；`.trae/`（Trae IDE 本地配置，指向 .agents/skills 的符号链接）加入 .gitignore。

## 2026-10-02 漏网之鱼归类：字节/运营商/商汤等域名按厂商补录

- 数据来源：`log/clashx-meta-log/2026-10-02_09-08-47`（复制自 `~/.config/clash.meta/logs`），提取未被本仓库规则覆盖的目标去重后：`match Match` 3 个、`oc-cn-domain` 约 160 个。
- match Match（3 个）：
  - `githubstatus.com` → `github.yaml`（GitHub 状态页，RDAP 注册商 MarkMonitor、NS 为 GitHub 惯用 NS1/AWSDNS）。
  - `packagecontrol.io` → `direct.yaml`（Sublime Text Package Control 插件仓库，发起进程 plugin_host-3.8 即 Sublime 插件宿主；托管于 Linode，可直连）。
  - `agents.sh` 未归类：`.sh` gTLD，GoDaddy 注册、Cloudflare NS，无有效注册实体信息，进程 firefox 无产品指向，归属不明。
- oc-cn-domain 归类：
  - `direct.yaml` 新增中国移动分组：`10086.cn`、`chinamobile.com`、`online-cmcc.cn`、`cmcc-cs.cn`、`komect.com`（移动爱家平台）、`mmarket.com`（移动 MM 应用商场）、`miguvideo.com`（咪咕视频）；中国电信分组：`189.cn`；开发者服务：`dcloud.net.cn`（DCloud/uni-app）、`packagecontrol.io`；其他国内站点：`telefen.com`（归属未明，CDN CNAME 指向 ctzcdn.cn 中国电信 CDN，oc-cn-domain 判为国内可直连）。
  - `xhs.yaml` 替换占位行：新增 `zztfly.com` —— 小红书 RedNote 遥测端点（Citizen Lab 报告确认 upc.zztfly.com / log-auth.zztfly.com 为 RedNote 追踪域名），该文件由占位转为实规则，README 描述同步更新。
  - `direct-ai.yaml` 新增商汤分组：`sensenova.cn`（日日新大模型 SenseNova）、`sensecore.cn`、`sensecoreapi.cn`（商汤大装置 SenseCore AI 云）。
  - `tencent.yaml` 新增腾讯云分组：`myqcloud.com`（腾讯云 VOD/CDN，license.vod2.myqcloud.com）。
  - `alibaba.yaml` 高德分组追加 `amap.com`（高德地图主域，与已有 autonavi.com 并存）。
- 已在 reject.yaml 收录（未重复添加）：`jpush.cn`、`jiguang.cn`（极光推送，上游广告/追踪列表已收录，为保持无新增重复不在 direct.yaml 重复）。
- 已覆盖（跳过）：bilibili 系（bilibili.com/bilivideo.com/bilivideo.cn/hdslb.com/biliimg.com/biligame.com）、feishu 系（feishu.cn/zijieapi.com/doubao.com/bytedance.com/bdurl.net/larkoffice.com）、微信系（qpic.cn/qlogo.cn/weixinbridge.com）、baidu.com 等主域已收录的众多子域。
- 重复检查：跨文件重复 63 项（历史基线），本次编辑新引入的 2 项（jpush.cn、jiguang.cn 与 reject.yaml 重复）已删除归零；文件内重复 0。github / direct / xhs / tencent / alibaba / direct-ai 六文件 YAML 语法校验通过。

## 2026-09-30 漏网之鱼归类：2026-09-30 日志 match Match 域名补录

- 数据来源：`log/clashx-meta-log/2026-09-30_08-53-16`、`log/clashx-meta-log/2026-09-30_10-24-24`、`log/clashx-meta-log/2026-09-30_10-40-59`（复制自 `~/.config/clash.meta/logs`），提取未被本仓库规则覆盖的目标去重后共 114 个（match Match 16 个、oc-cn-domain 98 个）。
- match Match 处理（16 个域名）：
  - 已覆盖（跳过）：`app/dl/feed.zoro.build` — `direct.yaml` 已有 `DOMAIN-SUFFIX,zoro.build`；`etahub.com`、`static.cloudflareinsights.com` — `reject.yaml` 已收录（GitHub Actions 维护，本地禁止编辑）。
  - NXDOMAIN 不归类：`investsmatters.com` — DNS 查询返回 NXDOMAIN（域名已失效），发起进程 Trae CN Helper，无法确认归属。
  - 新增 `proxy.yaml`：`nube.sh`（Nube Cloud，香港 VPS/云服务商，AS138997，注册商隐私保护但 LowEndTalk 公开信息确认归属 Nube Hong Kong Limited）；`pynesys.io`、`pynecore.org`（PyneSys LLC，Pine Script 兼容的 Python 交易框架，pynecore.org 为开源文档站，pynesys.io 为 API 服务，发起进程 firefox）。
  - 新增 `proxy-ai.yaml`：`jina.ai`（Jina AI Reader API，r.jina.ai 为 URL→Markdown 转换端点，属 AI 基础设施服务，发起进程 curl）。
- oc-cn-domain 处理（98 个域名）：全部已被现有 DOMAIN-SUFFIX 规则覆盖（bilibili.com、bilivideo.com、bilivideo.cn、hdslb.com、biliimg.com、biligame.com → bilibili.yaml；feishu.cn、bytedance.com、zijieapi.com、byteimg.com、doubao.com、bdurl.net、trae.cn、trae.com.cn、mchost.guru、larkoffice.com → bytedance.yaml；larksuite.com → bytedance-global.yaml；autonavi.com → alibaba.yaml；qpic.cn → wechat.yaml；clarity.ms → microsoft.yaml；longbridge.cn → hk-broker.yaml；mountaintoys.cn → direct.yaml）。命中外部 oc-cn-domain 规则集是 Clash 配置中规则集评估优先级问题，非规则缺失。
- 未归类：`investsmatters.com`（NXDOMAIN）；`monitor_browser`（伪域名，脚本已过滤）。
- 重复检查：63 项跨文件重复均为历史遗留（多为与 reject.yaml 重复），本次新增 4 条规则无重复；文件内重复 0。`proxy.yaml`、`proxy-ai.yaml` YAML 语法校验通过。

## 2026-09-30 漏网之鱼归类：2026-09-29 日志域名按厂商补录，新增 baidu.yaml

- 数据来源：`log/clashx-meta-log/2026-09-29_09-24-20`、`log/clashx-meta-log/2026-09-29_11-08-18`（复制自 `~/.config/clash.meta/logs`），match Match 域名 10 个 + 裸 IP 11 个，oc-cn-domain 域名去重后约 250 个。
- match Match 处理（多为滞后命中，不重复添加）：
  - `dl.ccswitch.io` 已由 `proxy-ai.yaml` 的 `ccswitch.io` 覆盖；`firefox-portal-detection.com` 已由 `firefox.yaml` 覆盖；`split-tool.com`、`x2/ye/ye1.i.lencr.org`、`*.lambda-url.us-west-2.on.aws` 已由 `proxy.yaml` 的 `split-tool.com`/`lencr.org`/`on.aws` 覆盖——均为 09-29 00:36 提交（cc882ff）后客户端规则未刷新产生的滞后命中。
  - 11 个 `17.57.145.x` 裸 IP（进程 apsd = Apple 推送）已由 `apple.yaml` 现有 `IP-CIDR,17.57.145.0/24` 覆盖。
  - 新增 3 个 RDAP 域名查询端点归入 `direct.yaml`「域名查询 / RDAP」分组（发起进程 curl）：`rdap.org`（IANA 引导）、`identitydigital.services`（Identity Digital 注册局）、`publicinterestregistry.org`（.org 注册局 PIR）。
- oc-cn-domain 归类（按主域归并，命中子域众多不逐一列出）：
  - `bilibili.yaml` += `biliimg.com`、`bilivideo.cn`（mcdn CDN）、`biligame.com`、`solseed.cn`（`upos-` 前缀与 B 站 CDN 命名一致，CNAME 链入移动 `cdn.10086.cn`，判定为 B 站视频 CDN）。
  - `bytedance.yaml` += `zijieapi.com`、`byteimg.com`、`volces.com`、`volccdn.com`（火山引擎）、`larkoffice.com`（飞书）、`trae.cn`、`trae.com.cn`、`mchost.guru`（Trae CN 及其 API CDN；Trae 为字节 AI IDE，Trae 国际版先例 `trae.ai` 在 `bytedance-global.yaml`）。
  - `tencent.yaml` += `qq.com`、`qq.com.cn`、`workbuddy.cn`、`tencentbuddy.com`（WorkBuddy 经查证为腾讯云 CodeBuddy 团队办公 Agent，`workbuddy.ai` 海外版先例在 `tencent-global.yaml`；`tencentbuddy.com` 注册商为腾讯 DNSPod）。
  - `wechat.yaml` += `qlogo.cn`（升级替换原 `wx.qlogo.cn`）、`qpic.cn`、`weixinbridge.com`（微信图片 CDN 与 JSBridge）。
  - `alibaba.yaml` += `taobao.com`、`tmall.com`、`alibaba.com`、`alibaba-inc.com`、`alicdn.com`、`aliyun.com`、`autonavi.com`（高德）。
  - `direct-ai.yaml` += `deepseek.com`（国内可直连 AI，库内原无覆盖）。
  - `direct.yaml` += `koolcenter.com`、`linkease.com`、`istoreos.com`、`ddnsto.com`（路由器固件 / NAS 生态）、`zhihu.com`、`mountaintoys.cn`（国内 CDN 边缘节点，注册归属未查明，OpenClash CN 规则集已判为国内可直连）。
  - 新建 `baidu.yaml` += `baidu.com`（百度为大型互联网公司，按规范使用独立规则文件），README 规则表同步（新增 baidu 行、更新 alibaba / bytedance 描述）。
- 未归类：`monitor_browser`（Trae 伪域名，脚本已过滤）；`feishu.cn`、`bilibili.com`、`hdslb.com`、`bilivideo.com`、`b23.tv`、`doubao.com`、`bytedance.com`、`bdurl.net` 等主域已收录。
- 重复检查：62 项跨文件重复均为历史遗留（与本次编辑无关），文件内重复 0，本次新增规则无重复；全部被编辑文件 YAML 语法校验通过。

## 2026-09-29 新增 ModelScope：alibaba.yaml / alibaba-global.yaml 替换占位行

- `DOMAIN-SUFFIX,modelscope.cn` 新增至 `alibaba.yaml`，`DOMAIN-SUFFIX,modelscope.ai` 新增至 `alibaba-global.yaml`，两个文件原 `DOMAIN-SUFFIX,` 无效占位行均已替换。
- `modelscope.ai` 原已存在于 `direct-ai.yaml`，按"大厂 AI 优先归入厂商文件"规则从 `direct-ai.yaml` 删除，仅在 `alibaba-global.yaml` 保留。
- 重复检查跨文件重复数保持 62（无新增重复，均为既有项），YAML 语法校验通过。

## 2026-09-29 漏网之鱼归类：trae.ai 归入 bytedance-global.yaml

- 数据来源：`log/clashx-meta-log/2026-09-28_08-21-26/clashx_29_00-40-06.log`，提取落入兜底 `match Match` 的域名去重后共 5 个：`api.trae.ai`、`grow-normal.trae.ai`、`monitor_browser`、`x2.i.lencr.org`、`ye1.i.lencr.org`。
- `DOMAIN-SUFFIX,trae.ai` 新增至 `bytedance-global.yaml`，替换原 `DOMAIN-SUFFIX,` 无效占位行（Trae 为字节跳动 AI IDE，`.ai` 为海外版主域，RDAP 查询注册商 GoDaddy 隐私保护，日志进程上下文为 Electron/Trae IDE）；同步更新 README 规则表描述。
- `lencr.org`（Let's Encrypt OCSP/CRL 端点，Cloudflare 注册）今日已补录至 `proxy.yaml`，本次直接沿用，不再重复添加至 `direct.yaml`。
- `monitor_browser` 为本地伪域名（Trae CN Helper 内部监控），非真实域名，不归类。
- 重复检查跨文件重复数由 63 降至 62（均为本次编辑前已存在的重复），`bytedance-global.yaml` YAML 语法校验通过。

## 2026-09-29 去重：youtu.be、ytimg.com 仅保留在 youtube.yaml

- `DOMAIN-SUFFIX,youtu.be`、`DOMAIN-SUFFIX,ytimg.com` 此前同时存在于 `google.yaml`、`proxy.yaml`、`youtube.yaml`，现按服务归属仅在 `youtube.yaml` 保留，从另外两个文件删除。
- 重复检查跨文件重复数由 64 降至 62，两个被编辑文件 YAML 语法校验通过。

## 2026-09-29 find_duplicates.py 退出码反映重复检查结果

- 脚本原先无论是否存在重复都以退出码 0 结束，无法在 shell / CI 中作为门禁；现改为：**无重复退出 0，存在跨文件或文件内重复退出 1**（两种情况下报告均照常生成）。
- 终端新增重复数量汇总输出（跨文件重复规则数、文件内重复条目数）。
- 同步更新 `scripts/README.md` 与本地 `AGENTS.md` 的自检闭环说明。

## 2026-09-29 scripts/duplicates.json 取消版本跟踪并加入 .gitignore

- `find_duplicates.py` 生成的 `scripts/duplicates.json` 体积约 17MB 且为可随时再生成的本地产物，改用 `git rm --cached` 取消跟踪（本地文件保留），并在 `.gitignore` 中忽略。
- `scripts/DUPLICATES.md` 仍保留版本跟踪；同步更新 `scripts/README.md` 说明。

## 2026-09-29 scripts 目录补充 README，重复报告输出路径移至 scripts/

- 新增 `scripts/README.md`：说明 `find_duplicates.py`、`merge_reject_from_loyalsoldier.py`、`normalize_yaml_comments.py` 三个脚本的用途、用法、输出产物、运行目录要求及与每日 GitHub Actions 的关系。
- `find_duplicates.py` 生成的 `DUPLICATES.md`、`duplicates.json` 由仓库根目录改为输出到脚本所在的 `scripts/` 目录（`Path(__file__).parent`），扫描范围仍为仓库根目录。
- 已通过 `git mv` 将现有两份报告迁移至 `scripts/`，保留重命名历史。

## 2026-09-29 漏网之鱼日志归类（log/ 子目录 clashx 日志全量提取）

数据来源：`log/` 下 19 个子目录中的 clashx_*.log 与 clashx_mihomo.log，提取落入兜底 `match Match`（漏网之鱼）规则的目标，去重后共 **183 个**（域名 169 + 裸 IP 14）。经 whois 归属查询与进程上下文核对后分类如下：

### tencent-global.yaml（腾讯海外 AI）
- `workbuddy.ai`（www.workbuddy.ai 884 次，WorkBuddy AI 主站）
- `codebuddy.ai`（www / download，CodeBuddy 国际版）

### apple.yaml
- `IP-CIDR,17.57.145.0/24`（apsd 推送）
- `IP-CIDR,17.253.0.0/16`（timed NTP 时间同步）

### google.yaml
- `google.co.jp`（www / accounts，DOMAIN-SUFFIX,google.com 不覆盖日本 ccTLD）
- `a.run.app`（Cloud Run，同时覆盖原 antigravity 更新器子域）

### microsoft.yaml
- `playwright.dev`（cdn.playwright.dev）

### firefox.yaml
- `mozilla-backup.org`（aus5 / firefox-settings / content-signature / versioncheck 等）
- `firefox-portal-detection.com`（captive portal 探测）

### meta.yaml
- `facebook.net`（connect.facebook.net）

### crypto.yaml
- `hyperliquid.xyz`（app / api-ui）
- `coingecko.com`、`coinyep.com`（行情数据）
- `web3modal.org`、`privy.io`、`magic.link`（Web3 钱包/认证）

### proxy-ai.yaml
- `newapi.ai`、`newapi.pro`（NewAPI 网关文档）
- `parallel.ai`（search）、`cua.ai`、`keenable.ai`、`flova.ai`、`lobehub.com`、`manus.space`、`agentlane.com`、`ccswitch.io`、`skills.sh`、`skill-history.com`、`browse.sh`

### github.yaml
- `star-history.com`（api）

### fin-media.yaml
- `sec.gov`（美国证监会）
- `tradingcode.net`、`trading-strategies.academy`（交易学习）
- `biggo.com`（finance.biggo.com 比价）

### bytedance.yaml
- `visactor.io`（字节开源可视化）

### hk-broker.yaml
- `wbrks.com`（长桥 CDN，Longbridge Pro SG Helper 进程确认；与已有 wbkrs.com/lbkrs.com 同族）
- `usmartglobal.com`（hk.usmartglobal.com，uSMART）

### us-broker.yaml
- `ibkr.com`（t.ibkr.com，盈透）

### streaming.yaml
- `live-video.net`、`twitchcdn.net`、`pscp.tv`（Twitch 视频分发）

### proxy.yaml
- 证书验证：`lencr.org`（Let's Encrypt OCSP，ye/ye1/ye2/x1/x2）、`crt.sectigo.com`、`ocsp.comodoca4.com`（trustd 系统证书校验；本机直连测试受 TUN 干扰无法确认可直连，先按代理处理）
- 开发者工具：`pythonhosted.org`（PyPI 文件）、`astral.sh`（uv）、`open-vsx.org`（CodeBuddy CN 扩展仓库）、`rgpub.io`
- 文档/状态页平台：`gitbook.io`、`statuspage.io`
- AWS：`awswaf.com`、`on.aws`
- 网站功能组件：`easychat.co`、`omnichat.ai`、`smartlook.cloud`（smartlook.com 已在 reject）、`cdn-ukwest/privacyportal-uk.onetrust.com`、`cdn.cookielaw.org`、`cmp.osano.com`、`cdp.customer.io`、`blacklist.tampermonkey.net`（均为精确 DOMAIN，避免遮蔽 reject 中的追踪子域）
- Docker：`prodregistryv2.org`（registry 别名）
- Riot：`lolesports.com`
- 杂项站点：`manyvids.com`（成人）、`numuki.com`（游戏）、`printfriendly.com`、`split-tool.com`、`xiaowan.hk`、`cdnfonts.com`、`bootstrapcdn.com`、`sublimetext.com`、`sublimehq.com`、`gfis.info`、`aisecmatrix.org`、`api.sunbreak.com`、`cvs.prohost.org`

### direct.yaml
- `60s-api.viki.moe`（docs，实测直连 200）
- `cdn.ripperhe.com`（Bob 翻译作者 CDN）
- `IP-CIDR,192.0.32.59/32`（whois.iana.org，本机 whois 命令）

### reject.yaml（手动补录段，未改动上游条目；该做法已于后续废止——reject.yaml 现由 GitHub Actions 每日自动合并独占维护，禁止人工编辑、禁止查询核对）
- `hibchr.com`、`antpeak.com`、`zorvian.com`、`premzon.com`（NameCheap+Cloudflare 无主体、Chrome 后台加载的疑似追踪域名，如误杀可从该段删除）

### 跳过项（日志时间早于规则更新，现已被 reject.yaml 覆盖）
`etahub.com`、`analytics.tiktok.com`、`analytics-ipv6.tiktokw.us`、`appier.net`、`go-mpulse.net`、`akstat.io`、`siteintercept.qualtrics.com`、`sdk-api-v1.singular.net`、`browser-intake-datadoghq.com`、`cloudflareinsights.com`、`cdn.debugbear.com`、`a.tampermonkey.net`、`smartlook.com`、`beyondwickedmapping.org`、`featureassets.org`、`ingesteer.services-prod.nsvcs.net`、`gssprt.jp`、`player.stats.live-video.net`

### 未处理裸 IP（任播/云厂商 IP，加 /32 属过拟合，暂不处理）
Fastly（151.101.0/64/128/192.223）、Cloudflare（104.21.17.214、172.67.178.84）、AWS（35.84.53.85、44.233.186.238、52.37.99.5、54.151.0.246）、阿里云（47.243.118.180）、腾讯云（43.160.158.125）、192.34.234.30、203.119.87.74

验证：16 个文件 `yaml.safe_load` 全部通过；`find_duplicates.py` 无新增跨文件重复；覆盖率审计 169/169 域名已覆盖。
