# 证据采集（L1–L5）与三类证据判读

本 skill 第 2 步的展开细则。**按层推进，命中即停**——L1 最便宜也最容易被跳过，L5 是兜底。

## L1 先查 reject.yaml 覆盖（最容易被跳过、也最省力）

```bash
PY=/Users/saibopika/.workbuddy/binaries/python/envs/default/bin/python
$PY .agents/skills/fill-issues-domain/scripts/verify-landing/verify_landing.py \
    --domains <域名...>
```

`config.yaml` 的 `rules` 第一条就是 `RULE-SET,reject,REJECT`，**`reject.yaml` 命中的域名补录到任何业务文件都永不生效**。先查覆盖：命中即直接转 skip，查归属是白做功。

2026-10-28 轮 16 项中有 3 项（`featureassets.org` / `wdfl.co` / `nsvcs.net`）早已被 reject 上游收录，正是这一步省掉的。注意 `DOMAIN-SUFFIX,ingesteer.services-prod.nsvcs.net` 这类**精确主机**规则也算覆盖了主域的对应子域——父域无其他端点时按不落盘处理。

**不要用 `grep -c` 多模式统计 `reject.yaml`**（10MB / 24 万行，`-c` 与 `-n` 会给出矛盾结果，2026-10-28 实测），用脚本或 Python 逐行扫。`verify_landing.py` 已实现逐行扫描，结果可复现。

## L2 库内品牌锚点

```bash
$PY scripts/check-coverage/check_coverage.py <主域...>
```

`BRAND-ANCHOR` 命中说明库内已有该品牌其它 TLD/兄弟域，按 AGENTS.md 判据 1–5 直接落盘。**标签须逐字符相同**，字母转位/形近是仿冒域（`mdoelscope.ai` ↔ `modelscope.ai`），绝不补录。

## L3 网络查证

```bash
$PY .agents/skills/fill-issues-domain/scripts/probe-domains/probe_domains.py \
    <域名...> --json /tmp/probe-$(date +%F).json
```

代理不可用（`nc -z 127.0.0.1 7893` 失败）时**不要无限重试**：把该项标记「下轮重试」原样留在表里，本轮按无结论处理，正常收尾。

**automation 预审模式**（v2.0.0 新增，见 `automation-pre-ruling.md`）：cron 轮也跑这一步，但结果只写入预审报告 `reports/pre-ruling-YYYY-MM-DD.md`，不动表、不动 skip-list、不写 changelog 定案段；交互式会话再据预审报告走第 5 步批量提问。

## L4 日志共现

```bash
$PY .agents/skills/fill-issues-domain/scripts/log-cooccurrence/log_cooccurrence.py \
    <域名...> --top 10
```

传主域即可（脚本按后缀匹配子域）。命中 0 次通常是该域只在未归档的当天日志里出现，先把日志 cp 归档再跑（`fill-domains-from-log` skill 第 1 节）。

## L5 兜底

查完仍无结论时，按下文「现行归属口径」处理。**只有用户明确要求保留观察时才留在表里**。

## 三类证据怎么读

### SOA 管理员邮箱 = 最硬锚点

`probe-domains` 输出的 `SOA(邮箱)` 取的是权威区 SOA 的 rname 字段。厂商自建权威 DNS 时它直接暴露母公司域：

| 实测 | 结论 |
|---|---|
| `applogcdn.com` → `ns1.volc-dns.com. dnsadmin.bytedance.com.` | 字节（该轮据此定 `bytedance.yaml`） |
| NS 为 `*-m.ns1pcdn.net` + NS1 | 多租户 CDN，无品牌指向 → 无锚点 |

### ASN 直接判厂商，注册商不是判据

CNAME 跳到云厂商 SLB 域名后，A 记录 IP 的 ASN 往往就是答案：

```bash
curl -s --max-time 10 "https://ipwho.is/<ip>" | $PY -c "import json,sys;c=json.load(sys.stdin)['connection'];print(c['asn'],c['org'])"
```

`perfops.byte-test.com` → CNAME `bplslb.com` → `71.18.228.101` AS396986 Bytedance Inc / `101.47.92.142` AS150436 BytePlus ⇒ 字节海外。**这条证据直接推翻了「阿里云注册 + alidns NS 不符字节惯例」的旧挂起理由**——注册商/NS 只是旁证，端点归属优先。

`ipinfo.io` 与 `rdap.org/ip` 走代理常返空，用 `ipwho.is`。

### 首页标题 = 最快的服务定性

| 实测 | 定性 |
|---|---|
| `111666.best` → 「16图床，永久免费，无需登录的图床」 | 图床（`i.` 子域即图片域） |
| `pixpix.com` → 「PixPix — AI Product Image & Video Generator for E-commerce」 | AI SaaS → `proxy-ai.yaml` |
| `sitemana.com` → 「Your conversion catalyst」+ 与 doubleclick 同批 | 广告追踪 → skip |

`403 Just a moment...` / `429` 多为 Cloudflare 挑战或反爬，**不代表无主**，只说明该端点在防抓取。
