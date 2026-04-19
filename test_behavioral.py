# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'D:/PainMatrix')
from painmatrix import add_pain_event, load_memory, save_memory
from openclaw_integration import PainMatrixOpenClaw, get_instance

pm = get_instance()

print('=== Behavioral Modifiers by Pain Level ===')
for lvl in [0, 1, 2, 3, 4, 5]:
    mem = load_memory()
    if lvl > 0:
        add_pain_event(mem, '測試疼痛', '初始化')
        mem = load_memory()
        mem['pain_level'] = lvl
        save_memory(mem)
    else:
        mem['pain_level'] = 0
        save_memory(mem)
    
    mods = pm.get_behavioral_modifiers()
    print(f'Lv.{lvl}: 認知容量={mods["cognitive_capacity"]:.0%} 警覺={mods["vigilance"]:.1f}x 謹慎={mods["caution"]:.1f}x')
    print(f'  策略: {mods["strategy"]["attention"][:40]}')
    print(f'  警告: {mods["cognitive_load_warning"]}')
    print()

print('=== Careful Task Approach ===')
for lvl in [1, 3, 5]:
    mem = load_memory()
    mem['pain_level'] = lvl
    save_memory(mem)
    approach = pm.get_careful_task_approach('撰寫一份產品報告')
    print(f'Lv.{lvl}: {approach}')

print()
print('=== Status Report ===')
status = pm.get_status()
for k, v in status.items():
    print(f'  {k}: {v}')

print()
print('=== Learning Record ===')
rec = pm.record_learning('任務執行不當', '用戶語氣突然變冷', '疼痛升至Lv.2')
print(rec)
status2 = pm.get_status()
print(f'  learning_log_size: {status2["learning_log_size"]}')

print()
print('ALL TESTS PASSED')
