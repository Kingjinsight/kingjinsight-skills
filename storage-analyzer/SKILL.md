---
name: storage-analyzer
description: >
  Linux（Arch）只读存储分析助手。扫描整机磁盘占用，找出占空间大户，把每一项分成
  🟢可自动清理 / 🟡需人工判断 / 🔴谨慎清理 三级并给出可执行处置方案，生成排版精美、
  可折叠、命令可一键复制的交互式 HTML 报告，并可起本地服务在网页上一键移到回收站。
  扫描全程只读。务必在以下场景使用：用户说"存储分析""磁盘满了""硬盘满了""空间不够"
  "清理空间""清理磁盘""占空间""哪些东西占地方""帮我看看存储""看一下电脑存储/空间"
  "存储空间""电脑空间不够""内存满了/不够/不足""看下内存/存储"（中文口语里"内存"
  常指存储空间）"storage analysis""disk cleanup""清缓存""磁盘清理""pacman 缓存"
  "占用根分区"；或用户抱怨电脑没空间、想知道什么东西吃硬盘、想要清理建议时。注意：
  若用户明确指运行内存/RAM（如"哪个进程吃内存""内存占用高"），那是 RAM 不是存储，
  不属于本 skill。
---

# Storage Analyzer (Linux / Arch)

对 Linux 做一次只读存储分析，产出交互式 HTML 报告。流程：扫描 → 分析分级 → 生成网页 → 打开。
本机基准：**Arch Linux + btrfs（子卷 `@`、快照 `/.snapshots`）+ Hyprland/KDE + `gio` 回收站 + dolphin**。

## 铁律

- **全程只读。** 只能跑扫描/统计/列目录/读元信息（`du`、`df`、`findmnt`、`btrfs`、`stat`、`ls`）。绝对禁止 `rm`、`mv`、清空回收站、改权限等任何写操作。
- **删除命令只展示，不执行。** 报告里给出的清理命令供用户自己在终端确认后运行。即使用户在对话里说"帮我删"，也要先停下确认（命中全局红线：删除文件必须先问），不要直接代跑。
- **本 skill 网页端只移回收站、不做永久删除。** `server.py` 用 `gio trash`（可还原）；没有永久删除按钮。
- **btrfs：估算要标清。** 写时复制 + 快照共享区块，删的文件若还被 `/.snapshots` 快照引用则不释放空间。"可释放空间"一律说是估算，并提示快照影响。
- **路径、命令保留原文不翻译。**

## 执行流程

### Step 1 扫描（只读）

```bash
python3 scripts/scan.py > /tmp/storage_scan.json
```

`scan.py` 扫 home、`~/.cache`、`~/.local/share`、`~/.config`、Downloads、`~/.var/app`（Flatpak）、回收站、开发缓存，用 `du -sk -x` 算大小（`-x` 不跨挂载点，避免误入 `/mnt/*`）。输出 JSON：`system`（系统/磁盘信息，含 `disks` 按物理设备去重的全部挂载 + `btrfs` 快照信息）+ `groups`（各组子目录大小，已降序、过滤 50MB 以下）。读不到的目录标 `denied`，需在报告里列出。

### Step 2 分析与分级

读 [references/linux.md](references/linux.md)（讲东西存哪、怎么辨认、归哪一级、Arch 专属清理、btrfs 注意事项）。然后读 `/tmp/storage_scan.json`：

1. **挑 Top 5** 占用大户，判定类型（系统资产/应用本体/应用数据/应用缓存/开发缓存/用户文件/媒体内容/下载内容/容器镜像/回收站/其他）。
2. **识别"神秘大目录"**：`~/.var/app` 下的 Flatpak、`~/.local/share` 里不明的大目录，查清属于哪个 App、装的是什么。必要时 `ls`/`du` 深入一层看清楚，但仍只读。
3. **三级分类 = 清理决策清单，不是全盘点。** 只把"存在'要不要动它'这个决策"的项放进三灯；日常在用的正常应用、操作系统本身、海量零碎小文件不进三灯，落在磁盘条蓝色"系统及其他"里。
   - 🟢 **可自动清理**：纯缓存、临时文件、安装包残留，明确可再生且不丢用户数据（pip/uv/yay/paru/go-build/npm/cargo 缓存、浏览器缓存、缩略图）。给：预估释放空间、清理前需关闭的进程、可一键复制的清理命令。**$HOME 内的可再生缓存子目录给 `trash_paths`** → 网页出现「移到回收站」按钮。**不在 $HOME 的（pacman 缓存 `/var/cache/pacman/pkg`、docker、journald）只给命令、不给按钮**（白名单限 $HOME、要 sudo）。
   - 🟡 **需人工判断**：含用户数据或有判断成本（Flatpak 应用数据、容器镜像、文档、`node_modules`、聊天记录）。给内容画像 + 至少 3 句处置路径（应用内清理 / 命令工具 / 文件管理器手动审查）+ 风险提示。所有橙灯项服务模式下自动有「在文件管理器打开」按钮；有核实过、删了不破坏应用的安全子路径才给 `trash_paths`（橙灯只准移回收站、可逆）。口吻中性像产品说明。
   - 🔴 **谨慎清理（有决策但不建议手删）**：想卸的大应用、重复装的东西、运行中应用的核心数据等。给"为什么不建议手删" + `indirect_release` 写**具体卸载步骤**（`sudo pacman -Rns <pkg>`、`yay -Rns`、`flatpak uninstall`、孤儿包 `pacman -Qtdq` 等，可照做）。应用项给 `app_paths` → 网页出现「在文件管理器打开」按钮。**红灯不给删除按钮。** 纯系统文件、btrfs 快照不单独列红卡，归蓝色；系统层面释放技巧（删旧快照、清 pacman 缓存、`journalctl --vacuum-size`、重启释 swap）写进 `summary.long_term`。

**大小字段写干净**：`size`/`size_estimate` 用"约 14 GB""合计约 8.6 GB"即可，不要再加"（估算）"。

### Step 3 生成交互报告

把分析结果写成 analysis JSON（schema 见 `scripts/build_report.py` 顶部注释）。

**🟢 项要带 `trash_paths`**（具体可删的绝对路径数组，须在 $HOME 内）——这是网页移回收站按钮的前提，漏了按钮不出现。pacman/docker/journald 这类系统级清理不放 `trash_paths`，写成 `commands`。

**默认用服务模式（`server.py`）打开报告**：
```bash
python3 scripts/server.py /tmp/storage_analysis.json   # 自动开浏览器，Ctrl+C 停
```
`server.py` 起在 127.0.0.1 + 随机端口 + 随机 token。🟢/🟡 项的 `trash_paths` 给「移到回收站」(可逆)；🟡 给「在文件管理器打开」；🔴 的 `app_paths` 给「在文件管理器打开」。**安全模型**：`gio trash` 只允许绿/黄灯 `trash_paths`；`open`（`xdg-open`，非破坏性）额外允许黄灯 `path` + 红灯 `app_paths`。所有请求 realpath 校验 + 必须在 $HOME 内 + token + Host 校验，每次点击浏览器先 confirm。**无永久删除。**

仅当用户明确只想要一份可分享/留存的只读文件时，才用静态模式（无按钮，`file://` 碰不到文件系统）：
```bash
python3 scripts/build_report.py /tmp/storage_analysis.json ~/storage-report.html && xdg-open ~/storage-report.html
```

**排障：网页上没有移回收站按钮** = 要么开的是静态报告（改用 `server.py`），要么 🟢 项漏了 `trash_paths`（补上重启服务）。

报告阅读流（固定顺序）：磁盘总览卡片（容量 + 进度条 + 三色容量 pills + 系统信息 + btrfs 快照数）→ 占用排行 Top5 → 执行建议 → 🟢🟡🔴 三级可折叠卡片（命令一键复制）→ 长期优化建议。即"现状 → 诊断 → 处方 → 操作 → 预防"。

`summary.overview` 写成一句话洞察（最大占用是什么、能释放多少）。磁盘进度条把"已用"拆段：绿(可自动清)+橙(需手动)+红(已识别不建议动项)+蓝(系统及其他=已用−绿−橙−红)，余下为可用。`summary.tier_stats` 的 green/yellow/red 都要以可解析的 GB 数字开头（如"约 27.8 GB"）。`/mnt/Windows`、`/mnt/Ubuntu` 等外挂分区只在磁盘总览展示，绝不进三灯。

### Step 4 对话里给摘要

报告生成后，在对话里用一段话给结论先行的摘要：总可释放估算（注明 btrfs 快照可能影响实际释放）、最该先清的 2-3 项、风险最高的一项。细节让用户看网页。

## 依赖与运行前提

- 全部脚本是 **Python 3 标准库**，零第三方依赖（不用 pip install）。
- 需要系统自带的 `du`、`findmnt`、`uname`；服务模式删除依赖 `gio`（glib2，桌面环境一般已装），打开目录依赖 `xdg-open`（xdg-utils）。
- `compsize`（看 btrfs 真实占用）、`paccache`（pacman-contrib）是可选增强，没有也能跑。
- 本 skill 是 **agent 驱动**：扫描出数据后由 agent（Claude）做分级分析，不是双击即用的独立 App。

## 平台状态

- **Linux / Arch + btrfs**：本 skill 的目标系统，已按 btrfs 快照、pacman/yay/flatpak/docker 清理、`gio trash`、`xdg-open` 适配。
- 仅支持 Linux；`scan.py`/`server.py` 在非 Linux 上会拒绝运行。

## 长期优化建议素材（写进报告 summary.long_term）

- btrfs：用 `snapper list` 看快照，调小时间线/数量上限，删旧快照才真正还空间；`btrfs filesystem usage /`、`compsize` 看真实占用
- pacman：定期 `paccache -rk2`、清孤儿包 `pacman -Qtdq | sudo pacman -Rns -`
- Flatpak/Docker：`flatpak uninstall --unused`、`docker system prune`
- 日志：`sudo journalctl --vacuum-size=500M`
- 可视化工具：`ncdu`、`baobab`（GNOME 磁盘分析）、`filelight`（KDE）
- 大文件归档到 NAS / 外置盘 / `/mnt` 其他分区
