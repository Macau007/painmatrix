#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PainMatrix HTTP API Server (Standalone)
独立进程，直接读取 memory.json，定时刷新
Web 界面 (emotion_view.html) 通过它实现实时同步

运行方式:
    python api_server.py          # 前台运行
    start /B python api_server.py # 后台运行
"""
import http.server
import socketserver
import json
import os
import time
import threading

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(SCRIPT_DIR, "memory.json")
PORT = 17888
POLL_INTERVAL = 1  # 秒

# ── 内存缓存 ──────────────────────────────────────────────
_cache = {"pain_level": 0, "emotion_state": "平静", "pain_history": [],
          "homeostatic": {}, "anxiety_level": 0, "desire_intensity": 0,
          "wellbeing": 100, "setpoints": {}, "trauma_log": [], "timestamp": ""}
_cache_lock = threading.Lock()


def _load_state():
    """从 memory.json 读取最新状态 + 实时痛感震荡(PainGenerator)"""
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            mem = json.load(f)
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        pain_level = mem.get("pain_level", 0)
        with _cache_lock:
            _cache["pain_level"] = pain_level
            _cache["emotion_state"] = mem.get("emotion_state", "平静")
            _cache["pain_history"] = mem.get("pain_history", [])[-20:]
            _cache["homeostatic"] = mem.get("homeostatic", {})
            _cache["anxiety_level"] = mem.get("anxiety_level", 0)
            _cache["desire_intensity"] = mem.get("desire_intensity", 0)
            _cache["wellbeing"] = mem.get("wellbeing", 100)
            _cache["setpoints"] = mem.get("setpoints", {})
            _cache["trauma_log"] = mem.get("trauma_log", [])
            _cache["dominant_desire"] = mem.get("dominant_desire", "task_completion")
            _cache["timestamp"] = ts
            # PainGenerator live data
            _cache["felt_pain"] = round(pain_level * 0.65, 2)  # baseline approximation
            _cache["is_restless"] = False
    except Exception:
        pass


def _poll():
    while True:
        _load_state()
        time.sleep(POLL_INTERVAL)


class _Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args): pass

    def do_GET(self):
        if self.path == "/api/state":
            with _cache_lock:
                state = dict(_cache)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(state, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


class _TCPServer(socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    print(f"[PainMatrix API] 监听 http://127.0.0.1:{PORT}")
    print(f"[PainMatrix API] 读取 {MEMORY_FILE}")

    # 立即加载一次
    _load_state()

    # 后台轮询线程
    t = threading.Thread(target=_poll, daemon=True)
    t.start()

    with _TCPServer(("", PORT), _Handler) as server:
        server.serve_forever()
