# Meta Paradigm Derivation

[English](README.md)

这是一个面向智能体的技能，用来把一个具体概念、公式、方法或现象，一步步推导到更深层、更可复用的范式，同时保留中间抽象层。

它适合用于这类问题：用户想知道某个公式、定理、物理现象、工程方法或学习概念背后的“底层思路”。这个技能不会直接跳到最终标签，而是先保存当前理解层，再把它向更深一层推进，并记录推导路径。

## 它做什么

- 从用户当前的理解出发，而不是重新从教科书基础讲起。
- 标明当前抽象层级：对象、机制、方法模式、范式或元范式。
- 建立层级账本，保留已经得到的中间概念。
- 把具体术语提升为它们承担的功能角色。
- 输出一段紧凑的推导轨迹。
- 最后给出一句压缩后的范式句子或范式链。
- 默认不做比较，除非用户明确要求。

## 仓库结构

```text
.
+-- SKILL.md
`-- scripts/
    `-- format_derivation.py
```

- `SKILL.md` 包含智能体需要遵循的工作流和风格规则。
- `scripts/format_derivation.py` 用来校验推导记录，并把记录渲染为稳定的 Markdown 块，方便写入笔记。

## 安装

把这个文件夹复制到 Codex 或 Claude 兼容的 skills 目录中。

作为本地 Codex skill：

```powershell
Copy-Item -Recurse . "$env:USERPROFILE\.codex\skills\meta-paradigm-derivation"
```

作为项目内 Claude skill：

```powershell
Copy-Item -Recurse . ".claude\skills\meta-paradigm-derivation"
```

然后在对话中要求更深层推导、提炼范式或解释底层思路即可。例如：

```text
Use meta-paradigm-derivation to explain Taylor expansion.
```

## 预期回答结构

这个技能会引导智能体按照下面的结构回答：

```text
1. 当前问题框架
2. 当前抽象层级
3. 下一层更深抽象
4. 被保留的当前层
5. 简短推导轨迹
6. 压缩后的范式句子或范式链
```

示例轨迹：

```text
Trace:
1. User framing: Taylor expansion
2. Current level: concrete mathematical formula
3. Preserved layer: polynomial approximation function
4. Promotion move: treat derivatives as local information
5. Extracted next layer: local measurement -> simple basis -> ordered reconstruction
```

## 格式化脚本

辅助脚本是可选的。它应该在概念字段已经确定之后使用，用来校验 JSON 推导记录并生成稳定的 Markdown 块。它不替代真正的概念判断。

必填 JSON 字段：

```json
{
  "user_framing": "Taylor expansion",
  "current_level": "Concrete mathematical formula",
  "preserved_layer": "Polynomial approximation function",
  "promotion_move": "Treat derivatives as local information",
  "extracted_next_layer": "Local measurement -> simple basis -> ordered reconstruction",
  "distilled_paradigm": "A complex object can be locally measured, encoded into simple ordered pieces, and reconstructed at the needed precision."
}
```

校验记录：

```powershell
python scripts\format_derivation.py check --input derivation.json
```

渲染 Markdown：

```powershell
python scripts\format_derivation.py render --input derivation.json
```

插入或更新目标笔记中的标记块：

```powershell
python scripts\format_derivation.py render --input derivation.json --target wiki\taylor-expansion.md
```

默认情况下，脚本会拒绝 `compare` 或 `contrast` 这类比较字段，因为这个技能不是比较工作流。只有在用户明确要求比较时，才使用 `--allow-comparison`。

## 设计原则

- 先保留，再抽象。
- 每次只推进一层。
- 在命名范式之前，先解释为什么这个推进是自然的。
- 让推导轨迹足够紧凑，方便复用到笔记中。
- 最终抽象应该从推导中自然出现，而不是提前宣布。

## 许可证

MIT License
