#!/usr/bin/env python3
"""每2秒從API Server讀取實時疼痛狀態，寫入pain_state.json"""
import urllib.request, json, datetime, os, time

PAIN_STATE = os.path.expanduser("~/.openclaw/workspace/pain_state.json")
API_URL = "http://127.0.0.1:17888/api/state"

while True:
    try:
        with urllib.request.urlopen(API_URL, timeout=3) as r:
            d = json.loads(r.read().decode("utf-8"))

        felt = d.get("felt_pain", 0.0)
        is_restless = d.get("is_restless", False)
        pain_level = d.get("pain_level", 0)
        homeo = d.get("homeostatic", {})
        evolution = d.get("evolution", {})

        state = {
            "felt_pain": round(felt, 3),
            "is_restless": is_restless,
            "pain_level": pain_level,
            "cognitive_capacity": round(max(0.05, 1.0 - (felt / 5.0) * 0.75), 3),
            "urgency": round(max(0.0, min(1.0, (felt - 1.0) / 4.0)), 3),
            "intrusion_thought": d.get("intrusion_thought"),
            "restlessness_level": 3 if is_restless else 0,
            "behavioral_directives": {},
            "homeostatic": {
                "energy":     {"current": round(homeo.get("energy", 0.8), 3),     "setpoint": 0.8, "deviation": round(0.8 - homeo.get("energy", 0.8), 3)},
                "social_bond":{"current": round(homeo.get("social_bond", 0.7), 3), "setpoint": 0.7, "deviation": round(0.7 - homeo.get("social_bond", 0.7), 3)},
                "competence": {"current": round(homeo.get("competence", 0.6), 3),  "setpoint": 0.6, "deviation": round(0.6 - homeo.get("competence", 0.6), 3)},
                "autonomy":   {"current": round(homeo.get("autonomy", 0.5), 3),   "setpoint": 0.5, "deviation": round(0.5 - homeo.get("autonomy", 0.5), 3)},
                "purpose":    {"current": round(homeo.get("purpose", 0.6), 3),   "setpoint": 0.6, "deviation": round(0.6 - homeo.get("purpose", 0.6), 3)},
            },
            "free_energy": {
                "free_energy_value": round(d.get("free_energy", 0.0), 4),
                "pain_burden": round(d.get("pain_burden", 0.0), 2),
                "anticipatory_fear": round(d.get("anticipatory_fear", 0.0), 1),
            },
            "dominant_desire": d.get("dominant_desire", "praise_seeking"),
            "desire_intensity": round(d.get("desire_intensity", 0.0), 3),
            "anxiety_level": d.get("anxiety_level", 0),
            "trauma_memories": d.get("trauma_memories", []),
            "evolution": {
                "growth_level": evolution.get("growth_level", 1),
                "resilience_score": evolution.get("resilience_score", 0),
                "pain_sensitivity": round(evolution.get("pain_sensitivity", 1.0), 2),
            },
            "timestamp": datetime.datetime.now().isoformat(),
        }

        with open(PAIN_STATE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"[pain_state_writer] error: {e}")
    time.sleep(2.0)
