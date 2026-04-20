@echo off
cd /d D:\PainMatrix
start /b python api_server.py
timeout /t 3 >nul
python -c 'import requests; d=requests.get("http://127.0.0.1:17888/api/state",timeout=5).json(); print("free_energy:", d.get("free_energy"), "| pain_burden:", d.get("pain_burden"), "| anticipatory_fear:", d.get("anticipatory_fear"))'
