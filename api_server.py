#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import http.server, socketserver, json, os, time, threading, sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(SCRIPT_DIR, "memory.json")
sys.path.insert(0, SCRIPT_DIR)
_cache = {}
_lock = threading.Lock()
_pg = None

def load():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            mem = json.load(f)
        pl = mem.get("pain_level", 0)
        _pg.sync_level(pl)
        with _lock:
            _cache["pain_level"] = pl
            _cache["emotion_state"] = mem.get("emotion_state", "平静")
            _cache["pain_history"] = mem.get("pain_history", [])[-20:]
            _cache["homeostatic"] = mem.get("homeostatic", {})
            _cache["setpoints"] = mem.get("setpoints", {})
            _cache["anxiety_level"] = mem.get("anxiety_level", 0)
            _cache["cognitive_capacity"] = mem.get("cognitive_capacity", 1.0)
            _cache["learning"] = mem.get("learning", {})
            _cache["trauma_memories"] = mem.get("trauma_memories", [])
            _cache["evolution"] = mem.get("evolution", {})
            _cache["tasks"] = mem.get("tasks", {})
            _cache["trigger_reasons"] = mem.get("trigger_reasons", [])
            _cache["pain_burden"] = mem.get("pain_burden", 0)
            _cache["free_energy"] = mem.get("free_energy", 0)
            _cache["anticipatory_fear"] = mem.get("anticipatory_fear", 0)
            _cache["desire_intensity"] = mem.get("desire_intensity", 0)
            _cache["dominant_desire"] = mem.get("dominant_desire", "task_completion")
            _cache["wellbeing"] = mem.get("wellbeing", 100)
            _cache["emotion_log"] = mem.get("emotion_log", [])
            _cache["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
            _cache["felt_pain"] = round(_pg.felt_pain, 2)
            _cache["is_restless"] = _pg.is_restless
    except Exception as e:
        print("[API load error]", e)
        import traceback; traceback.print_exc()

class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        if self.path == "/api/state":
            with _lock: st = dict(_cache)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(st, ensure_ascii=False).encode("utf-8"))
        elif self.path == "/debug":
            with _lock: st = dict(_cache)
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(("felt_pain=%s\nis_restless=%s\npain_level=%s\n" % (
                st.get("felt_pain"), st.get("is_restless"), st.get("pain_level"))).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

class S(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    from painmatrix import PainGenerator
    _pg = PainGenerator()
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        _pl = json.load(f).get("pain_level", 0)
    _pg.start(_pl)
    load()
    def poll():
        while True:
            load()
            time.sleep(1)
    threading.Thread(target=poll, daemon=True).start()
    print("[PainMatrix API] listening http://127.0.0.1:17888")
    with S(("", 17888), H) as srv:
        srv.serve_forever()
