#!/usr/bin/env python3
"""Serve the storage report with a guarded one-click trash API (Linux).

Starts on 127.0.0.1 + a random port + a random per-session token, serves the
interactive report, and exposes POST /action to move allowlisted paths to the
freedesktop Trash (reversible) or open them in the file manager. Stop with Ctrl+C.

Usage:
    server.py <analysis.json>

SAFETY MODEL — read before changing:
- Trash only, no permanent delete. The destructive primitive is `gio trash`
  (freedesktop Trash, recoverable from the file manager). There is deliberately
  no `rm` path: on btrfs "freeing space" isn't immediate anyway, and a
  misclassified item should always be recoverable.
- Allowlist: only paths listed in this report's green/yellow `trash_paths` are
  accepted for trashing; `open` additionally allows yellow `path` and red
  `app_paths`. Every request path is realpath-resolved and must be in the
  allowlist AND under $HOME. Anything else is rejected.
- Bound to 127.0.0.1 only; every POST requires the session token; Host header
  must be 127.0.0.1/localhost (blocks DNS-rebinding from a malicious page).
- The browser confirms each action before sending.
"""
import json
import os
import secrets
import subprocess
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "report_template.html")
HOME = os.path.realpath(os.path.expanduser("~"))
TOKEN = secrets.token_urlsafe(24)

DATA = {}
TPL = ""
TRASH_ALLOW = set()
OPEN_ALLOW = set()


def expand(p):
    return os.path.realpath(os.path.expanduser(p))


def load(src):
    with open(src, encoding="utf-8") as f:
        data = json.load(f)
    with open(TEMPLATE, encoding="utf-8") as f:
        tpl = f.read()
    # Two allowlists, narrow to wide:
    #   trash = green + yellow trash_paths (recoverable move to Trash)
    #   open  = trash set + yellow path + red app_paths (non-destructive reveal)
    trash_allow, open_allow = set(), set()
    for it in data.get("green", []) + data.get("yellow", []):
        for p in (it.get("trash_paths") or []):
            rp = expand(p)
            trash_allow.add(rp)
            open_allow.add(rp)
    for it in data.get("yellow", []):
        if it.get("path"):
            rp = expand(it["path"])
            if os.path.exists(rp):
                open_allow.add(rp)
    for it in data.get("red", []):
        for p in (it.get("app_paths") or []):
            rp = expand(p)
            if os.path.exists(rp):
                open_allow.add(rp)
    return data, tpl, trash_allow, open_allow


def move_to_trash(path):
    # gio trash -> freedesktop Trash (~/.local/share/Trash), recoverable.
    r = subprocess.run(["gio", "trash", "--", path], capture_output=True, text=True)
    if r.returncode != 0:
        raise OSError((r.stderr or "gio trash 失败").strip())


def open_in_file_manager(path):
    # Non-destructive: reveal the location so the user reviews/deletes it themselves.
    target = path if os.path.isdir(path) else os.path.dirname(path)
    r = subprocess.run(["xdg-open", target], capture_output=True, text=True)
    if r.returncode != 0:
        raise OSError((r.stderr or "xdg-open 失败").strip())


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json"):
        b = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            blob = json.dumps(DATA, ensure_ascii=False)
            cfg = json.dumps({"token": TOKEN, "endpoint": "/action"})
            html = TPL.replace("__REPORT_DATA__", blob).replace("__DELETE_CONFIG__", cfg)
            self._send(200, html, "text/html; charset=utf-8")
        else:
            self._send(404, "not found", "text/plain")

    def do_POST(self):
        if self.path != "/action":
            self._send(404, json.dumps({"ok": False, "error": "not found"}))
            return
        # DNS-rebinding guard: only accept local Host
        host = (self.headers.get("Host") or "").split(":")[0]
        if host not in ("127.0.0.1", "localhost"):
            self._send(403, json.dumps({"ok": False, "error": "host 不被允许"}))
            return
        n = int(self.headers.get("Content-Length", 0))
        try:
            req = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            self._send(400, json.dumps({"ok": False, "error": "请求格式错误"}))
            return
        if req.get("token") != TOKEN:
            self._send(403, json.dumps({"ok": False, "error": "token 校验失败"}))
            return
        mode = req.get("mode")
        allow = {"trash": TRASH_ALLOW, "open": OPEN_ALLOW}.get(mode)
        if allow is None:
            self._send(400, json.dumps({"ok": False, "error": "未知操作"}))
            return
        done = []
        for p in (req.get("paths") or []):
            rp = expand(p)
            if rp not in allow:
                self._send(403, json.dumps({"ok": False, "error": "路径不在白名单：%s" % p}))
                return
            # second guard: must live under $HOME
            if not (rp == HOME or rp.startswith(HOME + os.sep)):
                self._send(403, json.dumps({"ok": False, "error": "路径越界：%s" % p}))
                return
            try:
                if mode == "open":
                    open_in_file_manager(rp)
                elif not os.path.exists(rp):
                    pass  # already gone, treat as success
                else:
                    move_to_trash(rp)
                done.append(p)
            except Exception as e:
                self._send(500, json.dumps({"ok": False, "error": str(e)}))
                return
        self._send(200, json.dumps({"ok": True, "done": done}))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    global DATA, TPL, TRASH_ALLOW, OPEN_ALLOW
    DATA, TPL, TRASH_ALLOW, OPEN_ALLOW = load(sys.argv[1])
    srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = srv.server_address[1]
    url = "http://127.0.0.1:%d/" % port
    print("报告服务已启动：" + url)
    print("可移到回收站 %d 项 | 可打开文件夹 %d 项（页面上点按钮操作）"
          % (len(TRASH_ALLOW), len(OPEN_ALLOW)))
    print("用完按 Ctrl+C 停止服务（服务关掉后按钮即失效）")
    webbrowser.open(url)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止服务。")


if __name__ == "__main__":
    main()
