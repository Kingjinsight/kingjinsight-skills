# 生图提示词

每张单独生成。调用 `image_gen` 时，把 `assets/character-reference.jpg` 作为 `referenced_image_paths` 传入。

## 单张生成模板

```text
Generate one standalone 16:9 horizontal Chinese article illustration.

Use the attached character sheet only as identity reference for King. Do not reproduce the six-character sheet, pose lineup, grid, or original composition. Create one new scene.

Visual DNA:
Pure white #FFFFFF background. Minimalist charcoal-black #242629 hand-drawn line art with slightly wobbly thin pen lines. Lots of empty white space. Sparse low-saturation color fills and short handwritten Chinese annotations. Clean, direct, mildly absurd product-sketch feeling. No gradients, shadows, paper texture, beige background, noise, dense panels, commercial vector style, PPT infographic, formal flowchart, children's book, cute mascot poster, anime polish, 3D figurine, or realistic UI.

Recurring character:
King, a calm young adult creator in compact 3.5–4-head hand-drawn proportion. Preserve the attached reference identity: tousled fluffy short hair with one lifted tuft, black vertical oval eyes, tiny restrained mouth, loose deep-ocean-blue #2E486E crew-neck T-shirt, warm-bone #F3EDE4 cropped loose pants, simple round-toe sneakers. Keep face and limbs mostly unfilled white. King must physically perform the core conceptual action and change the state of the scene. He is not a lecturer, bystander, child, mascot, or decorative sticker.

Theme:
{正文配图主题}

Structure:
{流程 / 系统局部 / 前后对比 / 角色状态 / 概念隐喻 / 方法分层 / 地图路线 / 小分镜}

Core idea:
{唯一核心意思}

Physical metaphor:
{把抽象概念变成什么物理变化}

Composition:
{King 在哪里、正在做什么、主物件是什么、画面状态如何改变}

Chinese handwritten labels:
{标注词1} / {标注词2} / {标注词3} / {可选标注词4} / {可选标注词5}

Color roles:
Charcoal black #242629 for line art, primary text, objects, and structure.
Deep ocean blue #2E486E for King's T-shirt and a few core anchors.
{默认从以下选择一种；只有问题走向解决时最多选择两种：soft coral #DF7565 for problems/conflicts/key results; muted old gold #D3AD58 for movement/progress/energy; soft sage #7FA294 for feedback/AI assistance/stable state.}
Warm bone #F3EDE4 only for King's pants and tiny object fills, never for the background.

Constraints:
Explain only one core structure. Keep the main subject around 40%–60% of canvas and preserve at least 35% empty white space. Keep total colored area around 15%–20%, with deep ocean blue as the largest colored area. Use 2–5 short Chinese labels, each 2–8 characters. Use at most 0–3 arrows. Do not place a category title in the top-left. Do not write the structure type. Do not make King overly cute, childish, chibi, rosy-cheeked, big-eyed, or expressive. Do not copy any prior case composition. Clear in one second, strange on first glance, quiet and clean.
```

## 人物修复

```text
Edit only King to match the attached character reference more closely: restore the tousled short hair with one lifted tuft, black vertical oval eyes, tiny restrained mouth, loose deep-ocean-blue #2E486E T-shirt, warm-bone #F3EDE4 cropped loose pants, simple round-toe sneakers, and compact young-adult 3.5–4-head proportion. Keep King's existing action, pose, location, surrounding objects, labels, composition, pure white background, line style, colors, and aspect ratio unchanged. Do not make him younger or cuter.
```

## 去幼态

```text
Regenerate the same concept and layout. Keep King recognizable from the attached reference, but make him read as a calm young adult creator rather than a child or mascot. Reduce head exaggeration, remove blush and decorative expressions, use restrained oval eyes and a tiny neutral mouth, and make his hands visibly perform the conceptual task. Preserve the clean sparse hand-drawn style and pure white background.
```

## 去 PPT

```text
Regenerate the same core meaning as one sparse physical scene. Remove title, grid, cards, formal nodes, borders, legend, and excess arrows. Let King physically create the change using one low-tech object. Keep 2–5 short Chinese handwritten labels, pure white background, lots of empty space, and the fixed color system.
```

## 去标题

```text
Edit the provided image. Remove only the handwritten category title "{要删除的文字}" and its underline. Fill that area with clean #FFFFFF white matching the background. Preserve King, actions, objects, labels, colors, line style, composition, aspect ratio, and image quality. Add nothing.
```
