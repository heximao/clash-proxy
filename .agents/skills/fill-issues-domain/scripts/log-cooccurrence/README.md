# log-cooccurrence

按日志共现语境反推域名所属应用，供 fill-issues-domain skill 第 2 步（L4 日志共现）使用。

待判定表里的域名往往只剩「一个子域 + 进程名」，单看域名判不出归属。同一应用通常在同一秒内
打出一串请求，因此统计命中时刻 ±N 秒内的其它域名，共现最高的一簇基本就是它所属的产品：

- `p.sitemana.com` 与 `doubleclick` / `googlesyndication` / `statcounter` / `clarity.ms` 同批 ⇒ 广告追踪像素
- `api.123169.xyz` / `i.111666.best` / `cf.999831.xyz` 三者互现，且与 `dnscheck.tools` 同批 ⇒ 同一图床站的 API/图片/前端域
- `yjz.hk` 与 `tsight.io` 同批出现在 `WorkBuddy Helper` 进程 ⇒ 同一应用的两个依赖端点

## 用法

```bash
PY=/Users/saibopika/.workbuddy/binaries/python/envs/default/bin/python
cd /Users/saibopika/clash-proxy
$PY .agents/skills/fill-issues-domain/scripts/log-cooccurrence/log_cooccurrence.py \
    sitemana.com 111666.best --window 6 --top 10
```

| 参数 | 说明 |
|---|---|
| `--root` | 归档日志根（默认 `log/archive`，递归找 `clashx_core_*.log`） |
| `--also` | 额外扫描目录（默认 `log/clashx-meta-log`，存在才加） |
| `--window` | 共现时间窗秒数（默认 6） |
| `--top` | 每域输出几条共现（默认 10） |
| `--keep-resolvers` | 保留纯 IP 目标（默认过滤 `1.1.1.1` / `8.8.8.8` 等解析器噪声） |

## 输出

```text
## sitemana.com | 命中 39 次 | 进程 {'Google Chrome Helper': 39}
   子域 p.sitemana.com                                39
   共现 googleads.g.doubleclick.net                   51
```

## 要点

- **表里登记的是主域，日志里是子域**（`api.` / `i.` / `cf.` / `p.`），脚本按后缀匹配，传主域即可。
- 命中数为 0 通常表示该域只在未归档的当天日志里出现，先把日志 cp 归档再跑。
- 共现是启发式：只说明「同一时段被访问」，需与 SOA/ASN/首页标题交叉验证后再定案。
