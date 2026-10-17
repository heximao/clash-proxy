# normalize-yaml-comments

将各 YAML 规则文件中的分组注释标题统一为：

```text
# === Service Name ===
```

## 识别规则（启发式）

一行注释若在其后 3 个非空行内出现 `- ` 开头的规则行，则视为分组标题。处理时会：

- 去掉标题前后多余的 `>`、`===`、`-` 等装饰符号；
- 统一输出为 `# === 标题 ===`；
- 若标题前没有空行，自动补一个空行。

## 用法

```bash
# 在仓库根目录执行（脚本扫描当前工作目录）
python3 scripts/normalize-yaml-comments/normalize_yaml_comments.py
```

递归扫描仓库下所有 `.yaml` / `.yml` 文件，仅当文件实际发生变化时才写回；运行结束打印被修改的文件数量及路径。
