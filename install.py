# -*- coding: utf-8 -*-
"""
PainMatrix - Auto-Install Script

This script automatically configures the pain system for PainMatrix integration.
Run: python install.py

It will:
1. Verify Python version >= 3.8
2. Create default memory.json if not exists
3. Set file permissions on Linux/macOS
4. Register with PainMatrix workspace if detected
5. Report installation status
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
    if not os.path.exists(mem_file):
        initial = {"pain_level": 0, "emotion_state": "平静", "pain_history": [], "emotion_log": [], "trigger_reasons": []}
        with open(mem_file, "w", encoding="utf-8") as f:
            json.dump(initial, f, ensure_ascii=False, indent=2)
        print("  [OK] Created memory.json")
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
                        "version": "3.0.0",
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
    print("  PainMatrix v4.0 - Auto Installer")
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

    print("Step 4: Setting file permissions...")
    set_permissions()
    print()

    print("Step 5: Registering with PainMatrix...")
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
        print("    Trigger words: pain, 痛感, 疼痛, 情绪, empathy, 哀求")
        print("=" * 60)
    else:
        print("  Installation completed with warnings. Check above.")


if __name__ == "__main__":
    main()
