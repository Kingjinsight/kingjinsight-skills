---
name: "distill"
description: "当 King 明确说\"沉淀一下\"\"保存一下\"\"记进 lifeos\"\"存到知识库\"时，把当前对话或他给的材料直接压缩成文章写进他的 Obsidian vault（LifeOS），不让他取舍、不要他补输入、不套固定模板。"
---

# 沉淀（distill）

沉淀 = **把聊天记录压缩成文章，直接写进 King 的 vault**。King 不需要做任何额外的输入或选择：不给他候选清单，不等他回编号，不要求他先用自己的话复述。写完告诉他写了什么。

也不套固定模板。`My understanding` / `Background` / `When to use` 这类固定小节会限制压缩的效果，按内容本身最自然的结构来组织：先讲问题，再讲答案；按对话里理解推进的顺序；用小标题、表格、代码块，怎么讲清楚怎么来。

## 触发边界

- 只在 King 明确要求落盘时启动："沉淀一下""保存一下""记进 lifeos""存到知识库"，或直接调用本 skill。
- 什么对话都可以沉淀，普通聊天也行。King 没开口时不启动，也不主动提议"要不要沉淀"。
- King 指定了范围或某一点，就只沉淀那部分；没指定就沉淀这次对话里最近一段连贯的主题。

## 流程

### 0. 找到 vault

按顺序取第一个存在、且根目录有 `AGENT.md` 的路径：

1. 当前所在的 git 仓库根目录（云端会话里，vault 就是克隆下来的 vault 仓库）
2. 环境变量 `LIFEOS_VAULT`
3. `<本机 vault 路径>`（King 的 Mac）

云端会话里这三处都没有时，vault 在私有仓库 `<vault 仓库>`（main 分支）：能挂仓库就克隆它；连着 King 的 Mac，就写 Mac 上的 `<本机 vault 路径>`。

够不着 vault 时：照样把文章写完整，标明该放进哪个文件，交给 King 自己存，并明说这次没有写进 vault，索引和日志都没做。不要新建 vault，也不要说成已经存了。

然后读 `AGENT.md` 和 `Knowledge/_index.md`。frontmatter 约定以 `AGENT.md` 为准。

### 1. 压缩

通读对话，把值得留下的东西压缩成文章：

- **留下**：讲清楚的概念和机制、King 卡住的地方和最后是怎么想通的、他自己的原话和判断、具体例子和代码、结论和下一步。
- **去掉**：寒暄、重复的解释、来回确认、一次性的报错和操作步骤、搜一下就有的通用常识（除非它是理解主线的一环）。
- King 的原话和判断原样保留（不翻译），可以引用；AI 的解释可以直接写进正文，不需要单独隔开。
- 一个主题一篇。对话跨了几个不相关的主题，就分几篇。

### 2. 查重

对每个主题，在 `_index.md` 里找，再用 `rg` 在 vault 里搜两三个关键词。

- 已有页面讲同一件事：在该页面末尾追加一个新小节（带日期），不新建，不改写原有内容。
- 和已有内容矛盾：在相关段落后加 `> [!warning] YYYY-MM-DD 的新看法和上面不一样`，新旧两种说法都留着，并在汇报里指出。
- 已经有同系列的文件夹（比如 `Knowledge/EPL/`），新页面放进去，命名跟着已有文件的风格。

### 3. 写入

写之前重新读一遍目标文件，它可能刚被 Obsidian 或另一台机器改过。

| 内容 | 位置 |
|---|---|
| 概念、方法、判断（大部分沉淀） | `Knowledge/<标题>.md`；有同系列文件夹就放进去；LLM 技术概念进 `Knowledge/LLM/Concepts/` |
| King 表态的一句话立场 | `Beliefs.md` 对应小节末尾追加 `- <原话> (YYYY-MM-DD)` |
| 还没动手的点子 | `Ideas/<名字>.md`（`type: idea`, `status: raw`） |
| 已有项目的结果、结论、下一步 | `Projects/<项目>.md` 的 `## Log` 末尾追加 `- YYYY-MM-DD：…`；没有对应项目笔记就新建一个最简的项目页 |
| King 给的文章、论文、视频、链接 | `Resources/YYYY-MM-DD-<slug>.md`（`type: source`），原文原样放在 `## Raw content`；只有链接就先抓正文，抓不到才请他贴 |

Knowledge 页面只需要 frontmatter，正文结构自由：

```md
---
type: knowledge
tags:
  - <主题>
created: 'YYYY-MM-DD'
origin: distill
---
# <标题>

> YYYY-MM-DD，<当时在做什么>，压缩成一篇。

<正文：按内容最自然的结构写>

## Connections

- [[<已有页面>]] — <为什么相关>
```

`Connections` 只连真实存在的页面；没有自然联系就省掉这一节。

### 4. 更新索引和日志

- 新建或改了 `Knowledge/` 页面：在 `Knowledge/_index.md` 最合适的现有分类加一行 `- [[<页面>]] — <一行摘要> — N sources`（没有合适分类放 `## Orphans`），并把 `last_updated` 改成今天。
- 每次沉淀都在 `Knowledge/_log.md` 末尾追加：

```md
## [YYYY-MM-DD] distill | <这次的主题，一句>
- context: <Claude Code 或 Codex> · <项目名>
- created: [[<新页面>]]
- updated: [[<改过的页面>]]
```

没有的行省略。

### 5. 提交

在 King 的电脑上不要 commit 或 push，vault 由 obsidian-git 自动备份。在云端会话里（vault 是克隆下来的仓库）写完要自己提交并推送：提交信息写 `distill: YYYY-MM-DD <这次的主题>`，不加任何 Claude 署名行；推送前先 `git pull --rebase`；只提交这次写的文件，不碰 `.obsidian/`。推不上去要告诉 King，不能悄悄算了。

### 6. 汇报

```text
沉淀了 2 篇：
- created: [[页面 A]]（<一句话讲了什么>）
- updated: [[页面 B]]（+1 节）
Index: +1 · Log: appended
```

只汇报，不追问。King 想改可以直接说。

## 硬规则

- **不要求 King 输入。** 不发候选清单，不等他选，不要求他复述，不加 `[!todo]` 让他补。
- **不套固定模板。** 只有 frontmatter 是固定的，正文按内容组织。
- **只追加，不改写已有页面。** 这次沉淀新建的页面，King 要求重写时可以整页重写。
- **不碰这些地方：** `Decision Log.md`、`Resources/` 里已经存在的来源卡、`Daily Notes/`、`Reviews/`、`People/`、`Templates/`，以及除 `Beliefs.md` 以外的灵魂文件（`About Me`、`Values`、`Anti-Goals`、`Goals`、`Now`）。
- **不新建顶层文件或文件夹。**
- **链接只连真实存在的页面。**
- **不写密钥、密码和别人的隐私。**
- 对话里反复出现的操作流程不写成笔记，在汇报里提一句"这更适合做成 skill"。