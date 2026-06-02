# Linux / Arch 数据布局与分级参考

分析 Linux 扫描结果时读这份。讲"东西存在哪、怎么辨认、归哪一级"。本机基准：
**Arch Linux + btrfs（子卷 `@`、快照在 `/.snapshots`）+ Hyprland/KDE + `gio` 回收站 + dolphin + pacman/yay/flatpak/docker**。

## btrfs 铁律（影响"能释放多少"的判断）

- `du` 报的是**表观大小**。btrfs 写时复制 + 压缩 + 快照共享区块，删一个文件如果它还存在于 `/.snapshots` 的某个快照里，**不会释放任何空间**，要删掉对应快照才行。
- 涉及"可释放空间"一律说"估算"，并提示 btrfs 快照可能让实际释放低于估算。
- 想看真实占用：`btrfs filesystem usage /`、`compsize <dir>`（需装 `compsize`）。看快照：`snapper list` 或 `sudo btrfs subvolume list /`。
- `/`、`/home`、`/.snapshots`、`/var/cache/pacman/pkg`、`/var/log` 多半是同一块盘上的不同子卷，**共享同一份剩余空间**——报告里"其他磁盘"已按物理设备去重，别把子卷当独立盘。

## 关键目录

| 目录 | 装什么 | 典型分级 |
|---|---|---|
| `~/.cache/*`（pip、uv、yay、paru、go-build、huggingface、torch、mesa_shader_cache、thumbnails） | 缓存，可再生 | 🟢 可自动清 |
| `~/.cargo`、`~/.rustup`、`~/.npm`、`~/.pnpm-store`、`~/.bun`、`~/.gradle`、`~/.m2`、`~/.nuget`、`~/go/pkg`、`~/.conda` | 开发缓存/工具链 | 🟢（`.rustup`/`.conda` 是工具链非纯缓存，删了要重装，归🟡更稳） |
| `~/.local/share/Trash` | 回收站本身 | 🟢 提示清空才真正释放 |
| `~/.var/app/<id>`（Flatpak 应用数据） | 应用配置/缓存/用户数据 | 🟡（cache 子目录可🟢） |
| `~/.local/share/containers`（podman 镜像/层） | 容器镜像 | 🟡 用 `podman system prune` |
| `~/.config/*`、`~/.local/share/*`（聊天记录、笔记、Electron 应用数据） | 用户数据 | 🟡 多为用户数据 |
| `~/Downloads` 的 `.pkg.tar.zst`/`.iso`/`.AppImage` | 安装包/镜像残留 | 🟢/🟡 |
| 普通用户文件（文档、视频、项目代码 `node_modules`） | 用户内容 | 🟡 |
| 系统目录、内核、`/.snapshots` 快照 | 系统 | 不上灯，归蓝色"系统及其他" |
| `/mnt/Windows`、`/mnt/Ubuntu` 等外挂分区 | 别的操作系统/外部盘 | **不上灯、不给删除**，只在磁盘总览里展示 |

## Arch 专属清理（写命令，多数不在 $HOME → 只展示命令，不给网页按钮）

`/var/cache/pacman/pkg` 在 root 名下、要 sudo，**网页删除按钮够不到**（白名单限 $HOME），一律以一键复制命令给出：

- pacman 包缓存：`paccache -rk2`（留最近 2 版）、`paccache -ruk0`（删已卸载包的全部缓存）、或 `sudo pacman -Sc`
- 孤儿包：`pacman -Qtdq | sudo pacman -Rns -`（先 `pacman -Qtdq` 看清单）
- AUR helper 缓存：`yay -Sc`、`rm -rf ~/.cache/yay`、`paru -Sc`
- Flatpak 未用运行时：`flatpak uninstall --unused`
- Docker：`docker system prune -a`（看 `docker system df`），数据在 `/var/lib/docker`（root，命令处理）
- journald 日志：`journalctl --disk-usage` 看大小，`sudo journalctl --vacuum-size=500M`
- 缩略图缓存：`~/.cache/thumbnails`

## 间接释放（写进 long_term，不上红灯）

- btrfs 快照策略：`snapper` 时间线/数量上限调小；删旧快照才真正还空间
- 重启释放 tmpfs / swap 临时占用
- 大文件归档到 NAS / 外置盘 / `/mnt` 其他分区

## 删除机制

`server.py` 在 Linux 用 `gio trash` 送进 freedesktop 回收站（`~/.local/share/Trash`，dolphin 里可见可还原）；打开目录用 `xdg-open`（Hyprland 下唤起 dolphin）。本 skill **不提供永久删除按钮**——网页只移回收站，永久删除请用户自己在终端确认后跑命令。🟢 项的 `trash_paths` 必须在 `$HOME` 内，否则过不了白名单与 HOME 越界校验（如 pacman 缓存 → 走命令不走按钮）。
