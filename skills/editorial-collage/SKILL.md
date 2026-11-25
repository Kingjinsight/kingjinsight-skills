---
name: "editorial-collage"
description: "生成档案拼贴风（复古版画剪贴、哑光色块、细线网格、亮色圆点，类似 Anthropic 网站插画）的文章题图、封面和网站横幅时使用。"
---

# Editorial Collage

## 风格是什么

每张图都像档案馆里拼出来的一小块：一张复古的科学版画或旧照片剪贴（一棵树、一只罗盘、一把钥匙、一枚贝壳），放在一两块哑光纯色上，叠一层细黑线网格或几何线稿，再点一个亮色圆点。不讲故事，只放一个物件、一个结构、一个记号，让读者自己联想。

多张这样的小方块用米白缝隙拼在一起，就是网站横幅。

## 视觉规则

**底色**（大块纯色，哑光、平涂，带极轻的纸纹）：

| 色 | 值 | 色 | 值 |
|---|---|---|---|
| 灰粉 | `#D8B9BC` | 柠檬黄 | `#E3DA6A` |
| 鼠尾草绿 | `#A9B8A6` | 橄榄绿 | `#7D8A55` |
| 雾蓝 | `#9DB4D6` | 赤陶 | `#D47A5E` |
| 牛皮纸 | `#C8A77A` | 米白 | `#E9E3D3` |
| 炭黑 | `#1E1E1E` | 缝隙 | `#F5F4EE` |

一块里最多两种底色，常见做法是对半或四分切开。

**记号色**（只用在小圆点、节点、一根线上，面积很小）：绿 `#3FAE4F`、红 `#E0463C`、亮蓝 `#3A78D4`。

**物件**，从这几类里选，每块只放一个主物件：

- 复古科学版画：树、贝壳剖面、大脑剖面、月面、星图、罗盘玫瑰、鸟、植物标本。
- 黑白或半调的工具照片：锤子、钥匙、挂锁、圆规、尺、量角器、天平、剪刀、铅笔。
- 剪影：白色植物剪影压在蓝底上（蓝晒感）、陶罐、拼图块、希腊柱线稿。
- 纸和质感：方格纸、横线纸、地图、大理石纹、旧纸边。

**结构线**（细、黑、手工感）：方格网格、正弦波、来回折线、多面体、花形几何、节点连线图、由小方块组成的像素图案。

**组合方式**：照片质感 + 纯色块 + 线稿，三层叠在一起，留大量平面空间。物件常常被色块边缘裁掉一部分，或一半落在一块颜色上、另一半在另一块上。

**禁止**：任何文字、字母、数字、logo；人脸和人物；3D 渲染、光泽、霓虹、渐变光晕；机器人、芯片、发光大脑、电路板等"AI 科技感"套路；扁平商业矢量和卡通。

## 两种出图

| 模式 | 比例 | 怎么排 |
|---|---|---|
| 单块 | 1:1、4:5 或 3:2 | 一个物件 + 一两块底色 + 一层线稿 + 至多一个圆点 |
| 拼贴横幅 | 3:1（网站横幅）或 16:9 | 4–8 块大小不一的方块，米白细缝隙分开，网格对齐；每块是一个单块；整体颜色分布均匀，不要两块同色相邻 |

横幅在手机上会被裁成约 2:1，把最能代表文章的那一块放在中间。

## 工作流

1. **读文章**，找出核心意思，挑 1 个（单块）或 4–8 个（横幅）物件和结构，物件之间要能互相呼应（例如"测量"：尺、量角器、天平、网格上的一个点）。只给想法时，列出物件和每块的底色，不出图。
2. **写提示词**，用下面的模板，每版单独生成，默认出 2 版。
3. **检查**：有没有文字或数字、有没有人物、颜色是否哑光、物件是否被主体抢走空间、横幅中间那块是否最好。不合格就改提示词重生成，不要硬修。
4. **交付**：保存原始 PNG，用到网站时另存 JPEG（质量 85 左右）。说明出了几版、尺寸、推荐哪版。

## 提示词模板

单块：

```text
Create one archival editorial collage tile, aspect ratio {1:1}.
Matte flat colour field: {e.g. dusty pink #D8B9BC on the left half, sage #A9B8A6 on the right}, with a faint paper grain.
Main object: {e.g. a vintage scientific engraving of a nautilus shell cross-section}, cut out and placed {where}, partly cropped by the colour edge.
Line layer: {e.g. a thin black square grid over one half} and one small {green #3FAE4F} dot on {where}.
Calm, intellectual, restrained, like a page from a museum archive. Lots of flat empty space.
No text, letters, numbers or logos. No people or faces. No 3D, gloss, neon, glow, robots, chips or circuit boards. No flat cartoon vector style.
```

拼贴横幅：

```text
Create one wide editorial collage banner, aspect ratio 3:1, made of {6} rectangular tiles of different sizes arranged on a grid, separated by thin off-white #F5F4EE gutters.
Each tile is a small archival collage: one cut-out object (vintage scientific engraving or black-and-white photo of a tool) on one or two matte flat colour fields, with a thin black line motif and at most one small coloured dot.
Tiles, left to right:
1. {object} on {colour}, {line motif}
2. ...
Put the most important tile, {which}, in the centre. Spread the colours so no two neighbouring tiles share a colour.
Palette: dusty pink #D8B9BC, lemon yellow #E3DA6A, sage #A9B8A6, olive #7D8A55, powder blue #9DB4D6, terracotta #D47A5E, kraft #C8A77A, cream #E9E3D3, charcoal #1E1E1E; tiny accent dots only in green #3FAE4F, red #E0463C or blue #3A78D4.
No text, letters, numbers or logos. No people or faces. No 3D, gloss, neon, glow, robots, chips or circuit boards.
```

## 怎么调用生图

- **在 Codex 里**：直接调用 `image_gen`，有参考图时放进 `referenced_image_paths`。
- **在 Claude Code（King 的 Mac 上）**：在终端里非交互地跑 Codex：

  ```bash
  mkdir -p <输出目录>/v1 && cd <输出目录>/v1
  codex exec --skip-git-repo-check -m gpt-6-sol -s workspace-write [-i 参考图.png] - < prompt.txt
  ```

  - `-m gpt-6-sol` 必须写：默认的 `gpt-6.1-sol` 用 ChatGPT 账号登录会报错。
  - 不在受信任的 git 仓库里时要加 `--skip-git-repo-check`。
  - 提示词末尾写明 "Save the image as ./<文件名>.png"，并要求它报告图片尺寸。
  - 同时跑几版时每版用自己的文件夹，不然会拿错彼此的文件。
  - 宽图可以直接要（"use the widest size available, ideally 3:1"），实测能拿到 2172×724。
- **在云端的 Claude（claude.ai、手机、云端会话）**：这里没有生图工具。如果连着 King 的 Mac，就开一个 Remote Control 会话，按上一条在 Mac 上跑 Codex，再把图拿回来；没连着就告诉 King 需要在 Mac 上跑。

## 参考图

King 可能会给一张风格截图当参考：只用来对齐质感和配色，作为参考图传给生图工具。不要把别人的作品存进仓库，也不要逐块复刻里面的构图和物件。