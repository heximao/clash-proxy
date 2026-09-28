# scripts 脚本说明

本目录存放 clash-proxy 仓库的维护脚本，均使用 Python 3 标准库实现，无需安装第三方依赖。

> **注意**：所有脚本内部均以仓库根目录为基准使用相对路径（如 `Path('.')`、`reject.yaml`），必须在**仓库根目录**下执行，而不是在 `scripts/` 目录内执行。

## 脚本一览

| 脚本 | 作用 | 是否修改规则文件 |
|------|------|------------------|
| [find_duplicates.py](find_duplicates.py) | 扫描全部 YAML 规则文件，检查跨文件 / 文件内重复规则 | 否（仅生成报告） |
| [merge_reject_from_loyalsoldier.py](merge_reject_from_loyalsoldier.py) | 从 Loyalsoldier 上游合并最新广告/拦截域名到 `reject.yaml` | 是（仅 `reject.yaml`） |
| [normalize_yaml_comments.py](normalize_yaml_comments.py) | 将各 YAML 文件中的分组注释标题统一为 `# === Title ===` 格式 | 是（原地修改） |

## find_duplicates.py

递归扫描仓库根目录下所有 `.yaml` 文件，提取每一条规则（`- ` 开头的列表项），检查两类重复：

- **跨文件重复**：同一条规则出现在多个文件中；
- **文件内重复**：同一条规则在同一个文件中出现多次。

运行后在 `scripts/` 目录（与脚本同级）生成两份报告：

- `scripts/DUPLICATES.md`：人类可读的 Markdown 报告；
- `scripts/duplicates.json`：机器可读的 JSON，包含每条规则所在文件列表（`rule_map`）和每个文件的内部重复项（`file_dups`）。

扫描范围始终是运行时的当前目录（仓库根目录），仅报告输出路径固定在脚本所在目录。

```bash
# 在仓库根目录执行
python3 scripts/find_duplicates.py
```

脚本始终以退出码 0 结束，发现重复时需人工查看报告并决定保留位置。

## merge_reject_from_loyalsoldier.py

从 Loyalsoldier 上游拉取拦截域名列表，合并进 [reject.yaml](../reject.yaml)。

- **上游地址**：`https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/reject.txt`
- **规则归一化**：上游的 `+.example.com`、裸域名 `example.com` 统一转换为 `DOMAIN-SUFFIX,example.com`（小写）；其他规则类型忽略。
- **增量合并**：保留 `reject.yaml` 中已有全部规则，仅追加新规则，新规则放在 `# === Auto merged from Loyalsoldier reject.txt ===` 注释分组下。
- 要求 `reject.yaml` 必须以 `payload:` 开头，否则脚本报错退出。

```bash
# 在仓库根目录执行：从网络拉取上游并合并
python3 scripts/merge_reject_from_loyalsoldier.py

# 使用本地文件作为上游来源（调试 / 离线场景）
python3 scripts/merge_reject_from_loyalsoldier.py --source-file /path/to/reject.txt
```

该脚本同时由 GitHub Actions 工作流 [auto-merge-reject.yml](../.github/workflows/auto-merge-reject.yml) 每日 **00:20 UTC** 自动执行，有新增规则时会自动提交 `reject.yaml`。因此 `reject.yaml` 禁止手动编辑。

## normalize_yaml_comments.py

递归扫描仓库下所有 `.yaml` / `.yml` 文件，将分组注释标题规范化为统一格式：

```text
# === Service Name ===
```

识别规则（启发式）：一行注释若在其后 3 个非空行内出现 `- ` 开头的规则行，则视为分组标题。处理时会：

- 去掉标题前后多余的 `>`、`===`、`-` 等装饰符号；
- 统一输出为 `# === 标题 ===`；
- 若标题前没有空行，自动补一个空行。

仅当文件实际发生变化时才写回，运行结束后打印被修改的文件数量及路径。

```bash
# 在仓库根目录执行
python3 scripts/normalize_yaml_comments.py
```

## 环境要求

- Python 3.10+（脚本使用了 `str | None` 类型注解语法）；
- `merge_reject_from_loyalsoldier.py` 联网执行时需要能访问 jsDelivr CDN。
