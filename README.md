<div align="center">

# 🧰 kingjinsight-skills

Personal AI skills I actually use — open-sourced here.

![License](https://img.shields.io/badge/LICENSE-MIT-3081F7)
![Skills](https://img.shields.io/badge/SKILLS-1-2ea44f)
![AgentSkills](https://img.shields.io/badge/AGENTSKILLS-STANDARD-8957e5)

![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-D97757?logo=anthropic&logoColor=white)
![Codex](https://img.shields.io/badge/Codex-Skill-412991?logo=openai&logoColor=white)
![OpenCode](https://img.shields.io/badge/OpenCode-Skill-FB923C)

</div>

Each skill is a self-contained folder with a `SKILL.md` (and optional `scripts/`, `assets/`, `references/`), following the [Agent Skills](https://agentskills.io) open standard. It works with Claude Code, Codex, OpenCode, and other agents. The agent auto-loads a skill when your request matches its trigger description — no manual invocation needed.

## 📋 Skills

| Skill | What it does | Platform | Trigger examples |
|---|---|---|---|
| [storage-analyzer](storage-analyzer/) | Read-only disk analysis → tiered cleanup report (🟢/🟡/🔴) → interactive HTML with one-click move-to-trash | Linux / Arch (btrfs-aware) | "磁盘满了", "清理空间", "storage analysis", "disk cleanup" |

## 📦 Install

Just tell your coding agent (Claude Code / Codex / OpenCode / …) to install it — paste the skill's link:

> Install this skill for me: https://github.com/Kingjinsight/kingjinsight-skills/tree/main/\<skill>

Replace `\<skill>` with the skill you want. The agent clones it into the right skills directory for you — no manual path setup. Start a new session afterward so it loads.

<details>
<summary>Manual install</summary>

```bash
git clone https://github.com/Kingjinsight/kingjinsight-skills.git
cp -r kingjinsight-skills/storage-analyzer ~/.claude/skills/   # or your agent's skills dir
```
</details>

---

## storage-analyzer

Read-only storage analysis for Linux desktops, tuned for **Arch + btrfs**. It scans where disk space usually goes, lets Claude classify every heavy item into three tiers, and produces a polished interactive HTML report. Optionally, it serves the report locally with one-click **move-to-trash** buttons (reversible only — no permanent delete).

**Pipeline:** scan (read-only) → Claude classifies → HTML report → optional local server.

```bash
python3 scripts/scan.py > /tmp/storage_scan.json     # read-only scan
# Claude reads the JSON + references/linux.md, writes /tmp/storage_analysis.json
python3 scripts/server.py /tmp/storage_analysis.json  # interactive report + trash buttons
```

**Tiers**
- 🟢 **Auto-cleanable** — pure regenerable caches (pip/uv/yay/paru/cargo/npm/go-build, thumbnails). Gets a one-click *move-to-trash* button when inside `$HOME`; otherwise a copy-paste command.
- 🟡 **Needs your judgment** — contains user data (Flatpak app data, container images, documents, `node_modules`). Gets an *open in file manager* button; trash only for verified-safe subpaths.
- 🔴 **Handle with care** — apps/data better removed via proper uninstall. Open-in-file-manager only; never a delete button.

**Safety model**
- Scan is strictly read-only.
- The web server binds `127.0.0.1` + random port + per-session token; validates the `Host` header (anti DNS-rebind); every path is realpath-resolved and must be in the allowlist **and** under `$HOME`.
- Trash only — uses `gio trash` (recoverable from the file manager). There is no permanent-delete button by design.

**Dependencies:** Python 3 standard library only. Runtime needs `du`, `findmnt`, `uname`; trash/open need `gio` and `xdg-open`. `compsize` / `paccache` are optional enhancers.

**Layout**
```
storage-analyzer/
├── SKILL.md                     # trigger + workflow Claude follows
├── scripts/
│   ├── scan.py                  # read-only scanner → JSON
│   ├── build_report.py          # JSON → static HTML report
│   └── server.py                # JSON → served report + guarded trash API
├── assets/report_template.html  # report UI
└── references/linux.md          # Arch/btrfs data-layout & tiering guide
```

## License

[MIT](LICENSE) © 2026 Kingjinsight
