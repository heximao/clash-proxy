# verify-landing

定案闭环校验器，供 fill-issues-domain skill 第 7 步（校验）使用。一次核清四件事：
域名落在哪个业务 yaml、是否被 `reject.yaml` 覆盖、skip-list 里是什么模式、yaml 是否可解析。

## 用法

```bash
PY=/Users/saibopika/.workbuddy/binaries/python/envs/default/bin/python
cd /Users/saibopika/clash-proxy
$PY .agents/skills/fill-issues-domain/scripts/verify-landing/verify_landing.py \
    --domains applogcdn.com byte-test.com sitemana.com \
    --yaml bytedance.yaml proxy.yaml
```

`--expect` 默认 `auto`：域名在 `reject.yaml` 命中或 skip-list 为 `skip` 时按 skip 项校验，
否则按落盘项校验；也可强制 `--expect landing` / `--expect skip`。

## 判定

| verdict | 含义 | 应出现在 |
|---|---|---|
| `OK` | 恰好落在 1 个业务 yaml | 落盘项（期望态） |
| `MISSING` | 业务 yaml 里都没有 | 转 skip 项（期望态，且 reject 命中或 skip-list 有 `skip`） |
| `DUP` | 落在多个业务 yaml | 必须消除 |
| `IN-REJECT` | 声称落盘但 reject.yaml 里也有 | 必须改判 —— reject 是 `rules` 首条，落盘永不生效 |

退出码：`0` 无异常，`1` 存在异常项。

## 为什么要用脚本而不是 grep

`reject.yaml` 约 10MB、24 万行，多模式 `grep -c` 与 `grep -n` 会给出互相矛盾的结果
（2026-10-28 实测：`-c` 报 1，`-n` 无输出）。本脚本用 Python 逐行扫描，结果可复现；
同时能识别 `DOMAIN-SUFFIX,ingesteer.services-prod.nsvcs.net` 这类**精确主机**规则对主域的部分覆盖，
输出命中行号供人工判断。

其他约定：空文件（如未落内容的本地 `cn.yaml`）自动跳过；`config.yaml` 为本地配置，不参与扫描。
