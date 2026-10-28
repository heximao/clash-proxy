# probe-domains

单域名批量查证网络侧证据，供 fill-issues-domain skill 第 2 步（L3 网络查证）使用。
一次输出 SOA / NS / A / CNAME / RDAP / HTTP 标题，覆盖判定归属所需的全部一手字段。

## 用法

```bash
PY=/Users/saibopika/.workbuddy/binaries/python/envs/default/bin/python
$PY .agents/skills/fill-issues-domain/scripts/probe-domains/probe_domains.py \
    applogcdn.com yjz.hk freloop.com [--json /tmp/probe.json] [--no-http]
```

`--no-http` 跳过首页抓取（纯 DNS 查证更快）；`--json` 落盘供后续汇总。
代理地址可用环境变量 `PROBE_PROXY` 覆盖（默认 `http://127.0.0.1:7893`）。

## 字段判读

| 字段 | 判读方式 |
|---|---|
| `SOA(邮箱)` | 权威区 SOA 的 rname。厂商自建权威 DNS 时直接暴露母公司域（`dnsadmin.bytedance.com` ⇒ 字节），**最硬的归属锚点** |
| `NS` | DNS 服务商：`volc-dns`(火山/字节)、`nsone`(NS1)、`awsdns`(AWS)、`alidns`+`hichina`(阿里/国内)、`vanitydns`(白标)、`cloudflare`(隐私保护，无信息) |
| `A` / `CNAME` | CNAME 链常暴露所有者调度域（`bytedns3.com` ⇒ 字节、`bplslb.com` ⇒ BytePlus） |
| `RDAP` | registrar + 注册日期 + 实体。**注册商不是归属判据**，只作旁证；`.hk` / `.co` 无 RDAP 数据属正常 |
| `HTTP` | 首页状态 + `<title>`，是「这个域到底做什么服务」最快的一手证据（429/403 多为反爬或 Cloudflare 挑战，不代表无主） |

## 实现要点

- **DoH 直连**（`--noproxy '*'`），RDAP/HTTP 走代理——`rdap.org` 直连返空。
- 本机 `dig` 返回 `198.18.x` fake-ip（Clash TUN fake-ip 模式），**不可用于 A 记录判定**，故一律 DoH。
- SOA 在区顶点常落在 DoH 的 `Authority` 段而非 `Answer`，脚本已做回退，避免把 SOA 串误当 A 记录。
- RDAP 默认重试 3 次（`rdap.org` 首次常返空/SSL EOF）。
