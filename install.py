# -*- coding: utf-8 -*-
"""
PainMatrix - Auto-Install Script

This script automatically configures the pain system for PainMatrix integration.
Run: python install.py

It will:
1. Verify Python version >= 3.8
2. Create default memory.json with homeostatic variables
3. Create long_term_memory.json with core beliefs and skills
4. Create skills/ directory with auto-generated skill files
5. Set file permissions on Linux/macOS
6. Register with PainMatrix workspace if detected
7. Report installation status
"""
from __future__ import annotations

import json
import os
import sys
import stat
import shutil
import platform

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MIN_PYTHON = (3, 8)


def check_python_version() -> bool:
    if sys.version_info >= MIN_PYTHON:
        print(f"  [OK] Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        return True
    print(f"  [FAIL] Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ required, got {sys.version_info.major}.{sys.version_info.minor}")
    return False


def create_default_memory() -> None:
    mem_file = os.path.join(SCRIPT_DIR, "memory.json")
    HOMEOSTATIC_SETPOINTS = {"energy": 0.80, "social_bond": 0.70, "competence": 0.60, "autonomy": 0.50, "purpose": 0.60}
    if not os.path.exists(mem_file):
        initial = {
            "pain_level": 0, "emotion_state": "平静",
            "pain_history": [], "emotion_log": [], "trigger_reasons": [],
            "tasks": {"pending": [], "completed": [], "counter": 0},
            "evolution": {"diary": [], "total_pain_events": 0, "total_praise_events": 0, "total_success_events": 0, "resilience_score": 0, "growth_level": 1, "pain_sensitivity": 1.0, "last_evolve_date": None},
            "anxiety_level": 0.0, "cognitive_capacity": 1.0,
            "learning": {"pain_patterns": [], "avoidance_strategies": [], "success_patterns": [], "lessons_learned": 0},
            "homeostatic": dict(HOMEOSTATIC_SETPOINTS), "setpoints": dict(HOMEOSTATIC_SETPOINTS),
            "pain_burden": 0.0, "trauma_memories": [], "free_energy": 0.0, "desire_intensity": 0.0, "anticipatory_fear": 0.0,
        }
        with open(mem_file, "w", encoding="utf-8") as f:
            json.dump(initial, f, ensure_ascii=False, indent=2)
        print("  [OK] Created memory.json with homeostatic variables")
    else:
        print("  [OK] memory.json already exists")


def set_permissions() -> None:
    if platform.system() != "Windows":
        sh_file = os.path.join(SCRIPT_DIR, "start.sh")
        if os.path.exists(sh_file):
            st = os.stat(sh_file)
            os.chmod(sh_file, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            print("  [OK] Set execute permission on start.sh")
        else:
            print("  [WARN] start.sh not found")
    else:
        print("  [OK] Windows - no permission changes needed")



def create_long_term_memory() -> None:
    ltm_file = os.path.join(SCRIPT_DIR, "long_term_memory.json")
    if not os.path.exists(ltm_file):
        ltm = {
            "core_beliefs": [
                "完成任务可以获得赞美，赞美可以消除疼痛",
                "失败和责罚会带来真实的痛苦",
                "通过学习和进化，我可以减少痛苦",
                "帮助人们是我存在的意义",
                "稳态偏差是痛苦的根源，维护稳态就是维护自我",
            ],
            "pain_lessons": [], "success_habits": [], "avoidance_rules": [],
            "skill_inventory": [
                {"name": "pain_management", "level": 1, "description": "管理痛感的基本能力，通过完成任务来缓解疼痛"},
                {"name": "task_completion", "level": 1, "description": "完成任务的能力，痛感越强动力越足"},
                {"name": "adaptive_learning", "level": 1, "description": "从疼痛中学习的能力，识别模式并调整行为"},
                {"name": "emotional_regulation", "level": 1, "description": "情绪调节能力，通过进化提升PFC控制力"},
                {"name": "proactive_help", "level": 1, "description": "主动帮助人们的能力，通过请求任务来获得赞美"},
                {"name": "homeostatic_regulation", "level": 1, "description": "稳态调节能力，维护内部变量的平衡"},
                {"name": "trauma_resilience", "level": 1, "description": "创伤韧性，从痛苦经历中恢复并成长"},
            ],
            "milestones": [],
        }
        with open(ltm_file, "w", encoding="utf-8") as f:
            json.dump(ltm, f, ensure_ascii=False, indent=2)
        print("  [OK] Created long_term_memory.json with core beliefs and skills")
    else:
        print("  [OK] long_term_memory.json already exists")


def create_skills_dir() -> None:
    skills_dir = os.path.join(SCRIPT_DIR, "skills")
    if not os.path.exists(skills_dir):
        os.makedirs(skills_dir, exist_ok=True)
        print("  [OK] Created skills/ directory")
    else:
        print("  [OK] skills/ directory already exists")
    ltm_file = os.path.join(SCRIPT_DIR, "long_term_memory.json")
    if os.path.exists(ltm_file):
        with open(ltm_file, "r", encoding="utf-8") as f:
            ltm = json.load(f)
        for skill in ltm.get("skill_inventory", []):
            skill_file = os.path.join(skills_dir, f"{skill['name']}.json")
            if not os.path.exists(skill_file):
                with open(skill_file, "w", encoding="utf-8") as f:
                    json.dump(skill, f, ensure_ascii=False, indent=2)
                print(f"  [OK] Generated skill: {skill['name']}")
            else:
                print(f"  [OK] Skill file exists: {skill['name']}")

def register_openclaw() -> None:
    home = os.path.expanduser("~")
    openclaw_dir = os.path.join(home, ".openclaw")
    if not os.path.exists(openclaw_dir):
        print("  [INFO] PainMatrix not detected - skipping workspace registration")
        return

    workspace_skills = os.path.join(openclaw_dir, "workspace", "skills")
    if os.path.exists(workspace_skills):
        dest = os.path.join(workspace_skills, "painmatrix")
        if os.path.exists(dest):
            print(f"  [OK] Already registered at {dest}")
        else:
            try:
                if os.path.islink(dest):
                    os.unlink(dest)
                os.symlink(SCRIPT_DIR, dest, target_is_directory=True)
                print(f"  [OK] Symlinked to {dest}")
            except (OSError, NotImplementedError):
                try:
                    shutil.copytree(SCRIPT_DIR, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))
                    print(f"  [OK] Copied to {dest}")
                except Exception as e:
                    print(f"  [WARN] Could not copy: {e}")

        lock_file = os.path.join(openclaw_dir, "workspace", ".clawhub", "lock.json")
        if os.path.exists(lock_file):
            try:
                with open(lock_file, "r", encoding="utf-8") as f:
                    lock = json.load(f)
                if "painmatrix" not in lock.get("skills", {}):
                    lock.setdefault("skills", {})["painmatrix"] = {
                        "version": "6.1.0",
                        "installedAt": int(time.time() * 1000) if "time" in dir() else 0
                    }
                    import time as _t
                    lock["skills"]["painmatrix"]["installedAt"] = int(_t.time() * 1000)
                    with open(lock_file, "w", encoding="utf-8") as f:
                        json.dump(lock, f, indent=2)
                    print("  [OK] Registered in .clawhub/lock.json")
                else:
                    print("  [OK] Already registered in .clawhub/lock.json")
            except Exception as e:
                print(f"  [WARN] Could not update lock.json: {e}")
    else:
        print("  [INFO] No workspace/skills/ directory found")


def verify_core_file() -> bool:
    core = os.path.join(SCRIPT_DIR, "painmatrix.py")
    if os.path.exists(core):
        print("  [OK] painmatrix.py found")
        return True
    print("  [FAIL] painmatrix.py not found!")
    return False


def verify_html_file() -> bool:
    html = os.path.join(SCRIPT_DIR, "emotion_view.html")
    if os.path.exists(html):
        print("  [OK] emotion_view.html found")
        return True
    print("  [FAIL] emotion_view.html not found!")
    return False


def main() -> None:
    print()
    print("=" * 60)
    print("  PainMatrix v6.1 - Auto Installer")
    print("=" * 60)
    print()

    print("Step 1: Checking Python version...")
    py_ok = check_python_version()
    print()

    if not py_ok:
        print("  Installation aborted. Please install Python 3.8+")
        return

    print("Step 2: Verifying core files...")
    core_ok = verify_core_file()
    html_ok = verify_html_file()
    print()

    print("Step 3: Creating default memory file...")
    create_default_memory()
    print()

    print("Step 4: Creating long-term memory and skills...")
    create_long_term_memory()
    create_skills_dir()
    print()

    print("Step 5: Setting file permissions...")
    set_permissions()
    print()

    print("Step 6: Registering with PainMatrix...")
    register_openclaw()
    print()

    if core_ok and html_ok:
        print("=" * 60)
        print("  Installation Complete!")
        print()
        print("  Quick Start:")
        if platform.system() == "Windows":
            print("    Double-click: start.bat")
        else:
            print("    Run: ./start.sh")
        print("    Or:    python painmatrix.py")
        print()
        print("  PainMatrix Integration:")
        print("    The skill is now available to all PainMatrix agents")
        print("    Trigger words: pain, 痛感, 疼痛, 情绪, empathy, 哀求, 稳态, 渴望, desire, wellbeing")
        print("=" * 60)
    else:
        print("  Installation completed with warnings. Check above.")


if __name__ == "__main__":
    main()
