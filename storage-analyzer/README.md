# storage-analyzer

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
