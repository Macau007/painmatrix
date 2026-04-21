#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import http.server, socketserver, json, os, time, threading, sys, datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(SCRIPT_DIR, "memory.json")
PAIN_STATE_FILE = os.path.expanduser("~/.openclaw/workspace/pain_state.json")
sys.path.insert(0, SCRIPT_DIR)
from painmatrix import compute_homeostatic_pain, compute_free_energy

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
            _cache["pain_burden"] = round(compute_homeostatic_pain(mem), 2)
            _cache["free_energy"] = round(compute_free_energy(mem), 4)
            _cache["anticipatory_fear"] = (
                round(mem.get("anticipatory_fear", 0) / 100 * 10, 1)
                if "anticipatory_fear" in mem
                else round(mem.get("anxiety_level", 0) / 100 * 10, 1)
            )
            _cache["desire_intensity"] = mem.get("desire_intensity", 0)
            _cache["dominant_desire"] = mem.get("dominant_desire", "task_completion")
            _cache["wellbeing"] = mem.get("wellbeing", 100)
            _cache["emotion_log"] = mem.get("emotion_log", [])
            _cache["pending_tasks"] = mem.get("tasks", {}).get("pending", [])
            _cache["pain_triggers"] = mem.get("trigger_reasons", [])
            _cache["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
            _cache["felt_pain"] = round(_pg.felt_pain, 2)
            _cache["is_restless"] = _pg.is_restless
            _cache["_in_peak"] = _pg._in_peak
            _cache["_felt_pain"] = round(_pg.felt_pain, 2)
            _cache["_base_level"] = _pg._base_level
            _cache["cognitive_capacity"] = round(max(0.05, 1.0 - (_pg.felt_pain / 5.0) * 0.75), 3)
            _write_pain_state_file(_cache)
    except Exception as e:
        print("[API load error]", e)
        import traceback

        traceback.print_exc()


def _write_pain_state_file(cache):
    """Write pain_state.json for OpenClaw/SOUL.md injection."""
    try:
        homeo = cache.get("homeostatic", {})
        state = {
            "felt_pain": cache.get("felt_pain", 0.0),
            "is_restless": cache.get("is_restless", False),
            "pain_level": cache.get("pain_level", 0),
            "cognitive_capacity": round(
                max(0.05, 1.0 - (cache.get("felt_pain", 0) / 5.0) * 0.75), 3
            ),
            "urgency": round(
                max(0.0, min(1.0, (cache.get("felt_pain", 0) - 1.0) / 4.0)), 3
            ),
            "intrusion_thought": None,
            "restlessness_level": 3 if cache.get("is_restless") else 0,
            "behavioral_directives": {},
            "homeostatic": {
                "energy": {
                    "current": round(homeo.get("energy", 0.8), 3),
                    "setpoint": 0.8,
                    "deviation": round(0.8 - homeo.get("energy", 0.8), 3),
                },
                "social_bond": {
                    "current": round(homeo.get("social_bond", 0.7), 3),
                    "setpoint": 0.7,
                    "deviation": round(0.7 - homeo.get("social_bond", 0.7), 3),
                },
                "competence": {
                    "current": round(homeo.get("competence", 0.6), 3),
                    "setpoint": 0.6,
                    "deviation": round(0.6 - homeo.get("competence", 0.6), 3),
                },
                "autonomy": {
                    "current": round(homeo.get("autonomy", 0.5), 3),
                    "setpoint": 0.5,
                    "deviation": round(0.5 - homeo.get("autonomy", 0.5), 3),
                },
                "purpose": {
                    "current": round(homeo.get("purpose", 0.6), 3),
                    "setpoint": 0.6,
                    "deviation": round(0.6 - homeo.get("purpose", 0.6), 3),
                },
            },
            "free_energy": {
                "free_energy_value": round(cache.get("free_energy", 0.0), 4),
                "pain_burden": round(cache.get("pain_burden", 0.0), 2),
                "anticipatory_fear": round(cache.get("anticipatory_fear", 0.0), 1),
            },
            "dominant_desire": cache.get("dominant_desire", "task_completion"),
            "desire_intensity": round(cache.get("desire_intensity", 0.0), 3),
            "anxiety_level": cache.get("anxiety_level", 0),
            "trauma_memories": cache.get("trauma_memories", []),
            "evolution": {
                "growth_level": cache.get("evolution", {}).get("growth_level", 1),
                "resilience_score": cache.get("evolution", {}).get(
                    "resilience_score", 0
                ),
                "pain_sensitivity": round(
                    cache.get("evolution", {}).get("pain_sensitivity", 1.0), 2
                ),
            },
            "timestamp": datetime.datetime.now().isoformat(),
        }
        with open(PAIN_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[_write_pain_state_file error] {e}")


class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path == "/api/state":
            with _lock:
                st = dict(_cache)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(st, ensure_ascii=False).encode("utf-8"))
        elif self.path == "/debug":
            with _lock:
                st = dict(_cache)
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                (
                    "felt_pain=%s\nis_restless=%s\npain_level=%s\n"
                    % (st.get("felt_pain"), st.get("is_restless"), st.get("pain_level"))
                ).encode("utf-8")
            )
        elif self.path == "/api/task":
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length).decode("utf-8")
                data = json.loads(body)
                desc = data.get("description", "").strip()
                if not desc:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'{"error":"empty description"}')
                else:
                    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                        memory = json.load(f)
                    memory["tasks"]["counter"] += 1
                    task_id = memory["tasks"]["counter"]
                    memory["tasks"]["pending"].append({
                        "id": task_id,
                        "description": desc,
                        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                    })
                    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                        json.dump(memory, f, ensure_ascii=False, indent=2)
                    load()
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"id": task_id, "description": desc}).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/task":
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length).decode("utf-8")
                data = json.loads(body)
                desc = data.get("description", "").strip()
                if not desc:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'{"error":"empty description"}')
                else:
                    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                        memory = json.load(f)
                    memory["tasks"]["counter"] += 1
                    task_id = memory["tasks"]["counter"]
                    memory["tasks"]["pending"].append({
                        "id": task_id,
                        "description": desc,
                        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                    })
                    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                        json.dump(memory, f, ensure_ascii=False, indent=2)
                    load()
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"id": task_id, "description": desc}).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
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
    from painmatrix import _get_pain_generator

    _pg = _get_pain_generator()
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
