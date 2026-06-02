#!/usr/bin/env python3
"""Read-only storage scanner (Linux / Arch).

Collects disk usage, system info, and per-directory size breakdowns for the
hot spots that typically eat disk on a Linux desktop, and emits one JSON blob
to stdout for Claude to interpret and classify.

STRICTLY READ-ONLY: only sizes/lists/reads metadata (du, findmnt, btrfs).
Never creates, moves, or deletes anything.

btrfs caveat: on copy-on-write filesystems `du` reports apparent size. Snapshots
share extents, so deleting a file that still exists in a /.snapshots snapshot
frees nothing until that snapshot is removed. `system.btrfs` surfaces this so the
analysis can warn instead of promising space that won't come back.

Output shape:
{
  "generated_at", "scan_seconds",
  "system": {os, build, arch, user, home, filesystem,
             disk_total, disk_used, disk_free, purgeable, disk_name,
             disks: [{name, total, used, free}],          # real block mounts
             btrfs: {snapshots_path, snapshot_count, note} | null},
  "groups": { "<group>": [{name, path, size_kb, size_h}], ... }
}
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time

HOME = os.path.expanduser("~")

# Pseudo / virtual filesystems we never report as "disks".
PSEUDO_FS = {
    "proc", "sysfs", "tmpfs", "devtmpfs", "devpts", "cgroup", "cgroup2",
    "securityfs", "pstore", "bpf", "tracefs", "debugfs", "configfs", "mqueue",
    "hugetlbfs", "fusectl", "ramfs", "autofs", "efivarfs", "binfmt_misc",
    "fuse.portal", "fuse.gvfsd-fuse", "overlay", "squashfs", "nsfs", "rpc_pipefs",
}


def human(kb):
    """KB number -> human string like '12.3 GB'."""
    n = float(kb) * 1024
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{n:.1f} {unit}" if unit not in ("B", "KB") else f"{int(n)} {unit}"
        n /= 1024


def run(cmd, timeout=180):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).stdout
    except Exception:
        return ""


def du_children(path, min_kb=51200, limit=40):
    """Size every immediate child of `path` via `du -sk -x`, sorted desc.

    -x keeps du on a single filesystem so it never wanders into a nested mount
    (e.g. a bind-mounted subvolume or something under ~/mnt).
    """
    if not os.path.isdir(path):
        return []
    results = []
    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return [{"name": "(permission denied)", "path": path,
                 "size_kb": 0, "size_h": "?", "denied": True}]
    for name in entries:
        if name in (".", ".."):
            continue
        child = os.path.join(path, name)
        if os.path.islink(child):
            continue
        out = run(["du", "-sk", "-x", child], timeout=120)
        m = re.match(r"\s*(\d+)", out)
        if not m:
            continue
        kb = int(m.group(1))
        if kb < min_kb:
            continue
        results.append({"name": name, "path": child, "size_kb": kb, "size_h": human(kb)})
    results.sort(key=lambda r: r["size_kb"], reverse=True)
    return results[:limit]


def xdg_dir(key, default):
    """Resolve an XDG user dir (e.g. XDG_DOWNLOAD_DIR) from env or user-dirs.dirs."""
    env = os.environ.get(key)
    if env and os.path.isdir(env):
        return env
    cfg = os.path.join(HOME, ".config", "user-dirs.dirs")
    if os.path.isfile(cfg):
        try:
            with open(cfg, encoding="utf-8") as f:
                m = re.search(rf'{key}="([^"]+)"', f.read())
            if m:
                p = m.group(1).replace("$HOME", HOME)
                if os.path.isdir(p):
                    return p
        except OSError:
            pass
    return default


CACHE = os.path.join(HOME, ".cache")
SHARE = os.path.join(HOME, ".local", "share")

LINUX_DEV_CACHE_PATHS = [
    "~/.cache/pip", "~/.cache/uv", "~/.cache/yay", "~/.cache/paru",
    "~/.cache/go-build", "~/.cache/huggingface", "~/.cache/torch",
    "~/.cache/pypoetry", "~/.cache/electron", "~/.cache/ms-playwright",
    "~/.cargo", "~/.rustup", "~/.npm", "~/.pnpm-store", "~/.bun",
    "~/.gradle", "~/.m2", "~/.nuget", "~/go/pkg", "~/.conda",
    "~/.local/share/containers", "~/.local/share/virtualenvs",
]


def dev_caches_linux():
    results = []
    for p in LINUX_DEV_CACHE_PATHS:
        path = os.path.expanduser(p)
        if not os.path.isdir(path):
            continue
        out = run(["du", "-sk", "-x", path], timeout=180)
        m = re.match(r"\s*(\d+)", out)
        if not m:
            continue
        kb = int(m.group(1))
        if kb < 51200:
            continue
        results.append({"name": os.path.basename(path.rstrip("/")) or path,
                        "path": path, "size_kb": kb, "size_h": human(kb)})
    results.sort(key=lambda r: r["size_kb"], reverse=True)
    return results


def list_mounts_linux(root_source):
    """Real block-device mounts, one entry per physical device.

    btrfs exposes each subvolume as its own mount (/, /home, /.snapshots, ...)
    all backed by the same device and the same free space. Collapsing by device
    avoids showing the same capacity five times.
    """
    out = run(["findmnt", "-rn", "-o", "TARGET,FSTYPE,SOURCE"])
    disks, seen = [], set()
    for line in out.splitlines():
        parts = line.split()
        if len(parts) < 3:
            continue
        target, fstype, source = parts[0], parts[1], parts[2]
        if fstype in PSEUDO_FS:
            continue
        dev = source.split("[")[0]  # strip btrfs [/subvol] suffix
        if dev in seen:
            continue
        seen.add(dev)
        try:
            t, u, f = shutil.disk_usage(target)
        except Exception:
            continue
        if t == 0:  # AppImage / FUSE loop mounts report zero capacity — skip noise
            continue
        disks.append({"name": target, "total": human(t // 1024),
                      "used": human(u // 1024), "free": human(f // 1024),
                      "fstype": fstype})
    return disks


def btrfs_info():
    """Snapshot awareness for btrfs roots. Counts /.snapshots entries if readable."""
    snap_root = "/.snapshots"
    if not os.path.isdir(snap_root):
        return {"snapshots_path": None, "snapshot_count": 0,
                "note": "btrfs root, no /.snapshots subvolume found (snapper not in use?)."}
    try:
        count = sum(1 for e in os.scandir(snap_root) if e.is_dir())
    except (PermissionError, OSError):
        count = -1
    note = ("btrfs CoW: `du` shows apparent size. Files still referenced by a "
            "snapshot keep occupying space until the snapshot is deleted "
            "(`snapper list` / `sudo snapper -c <cfg> delete <n>`). "
            "Quote freeable space as an estimate, not a guarantee.")
    return {"snapshots_path": snap_root, "snapshot_count": count, "note": note}


def system_info_linux():
    info = {}
    pretty = ""
    try:
        with open("/etc/os-release", encoding="utf-8") as f:
            m = re.search(r'PRETTY_NAME="([^"]+)"', f.read())
            pretty = m.group(1) if m else ""
    except OSError:
        pass
    info["os"] = pretty or ("Linux " + run(["uname", "-r"]).strip())
    info["build"] = "kernel " + run(["uname", "-r"]).strip()
    info["arch"] = run(["uname", "-m"]).strip()
    info["user"] = os.environ.get("USER", "") or run(["whoami"]).strip()
    info["home"] = HOME
    total, used, free = "?", "?", "?"
    try:
        t, u, f = shutil.disk_usage("/")
        total, used, free = human(t // 1024), human(u // 1024), human(f // 1024)
    except Exception:
        pass
    info["disk_total"], info["disk_used"], info["disk_free"] = total, used, free
    root_source = run(["findmnt", "-no", "SOURCE", "/"]).strip()
    info["filesystem"] = run(["findmnt", "-no", "FSTYPE", "/"]).strip() or "?"
    info["purgeable"] = ""
    info["disk_name"] = "/"
    info["disks"] = list_mounts_linux(root_source)
    info["btrfs"] = btrfs_info() if info["filesystem"] == "btrfs" else None
    return info


def scan_linux():
    targets = [
        ("home", HOME, 102400),
        ("cache", CACHE, 51200),
        ("local_share", SHARE, 51200),
        ("config", os.path.join(HOME, ".config"), 51200),
        ("downloads", xdg_dir("XDG_DOWNLOAD_DIR", os.path.join(HOME, "Downloads")), 51200),
        ("flatpak", os.path.join(HOME, ".var", "app"), 51200),
        ("trash", os.path.join(SHARE, "Trash"), 1024),
        ("dev_caches", None, 51200),
    ]
    groups = {}
    for key, path, floor in targets:
        groups[key] = dev_caches_linux() if key == "dev_caches" else du_children(path, min_kb=floor)
    return system_info_linux(), groups


def main():
    started = time.time()
    if not sys.platform.startswith("linux"):
        print(json.dumps({"error": "unsupported_platform", "platform": sys.platform,
                          "message": "this build of scan.py targets Linux only."},
                         ensure_ascii=False))
        return
    system, groups = scan_linux()
    data = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "system": system,
        "groups": groups,
        "scan_seconds": round(time.time() - started, 1),
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
