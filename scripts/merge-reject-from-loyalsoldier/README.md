# merge-reject-from-loyalsoldier

从 Loyalsoldier 上游拉取拦截域名列表，增量合并进 [reject.yaml](../../reject.yaml)。

- **上游地址**：`https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/reject.txt`
- **规则归一化**：上游的 `+.example.com`、裸域名 `example.com` 统一转换为 `DOMAIN-SUFFIX,example.com`（小写）；其他规则类型忽略。
- **增量合并**：保留 `reject.yaml` 已有全部规则，仅追加新规则，置于 `# === Auto merged from Loyalsoldier reject.txt ===` 注释分组下。
- 要求 `reject.yaml` 必须以 `payload:` 开头，否则脚本报错退出。

## 用法

```bash
# 在仓库根目录执行（脚本以相对路径读写 reject.yaml，依赖当前工作目录）：从网络拉取上游并合并
python3 scripts/merge-reject-from-loyalsoldier/merge_reject_from_loyalsoldier.py

# 使用本地文件作为上游来源（调试 / 离线场景）
python3 scripts/merge-reject-from-loyalsoldier/merge_reject_from_loyalsoldier.py --source-file /path/to/reject.txt
```

## 与 GitHub Actions 的关系

该脚本由 [auto-merge-reject.yml](../../.github/workflows/auto-merge-reject.yml) 工作流每日 **00:20 UTC** 自动执行，有新增规则时自动提交 `reject.yaml`。因此 `reject.yaml` 禁止手动编辑；本地手动执行仅用于验证合并结果。

## 环境要求

- Python 3.10+（脚本使用了 `str | None` 类型注解语法）；
- 联网执行时需要能访问 jsDelivr CDN。
