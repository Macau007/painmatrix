# 🧠 PainMatrix 文檔

<h1 align="center">神經科學AI痛感模擬引擎</h1>

---

## 目錄

- [系統架構](#系統架構)
- [痛感系統](#痛感系統)
- [穩態變量](#穩態變量)
- [焦慮與創傷](#焦慮與創傷)
- [進化系統](#進化系統)
- [指令參考](#指令參考)
- [API參考](#api參考)
- [神經科學基礎](#神經科學基礎)

---

## 系統架構

```
painmatrix.py          # 核心引擎 — 所有邏輯
emotion_view.html      # 瀏覽器即時視覺化
memory.json           # 持久化狀態（首次運行時自動創建）
long_term_memory.json # 核心信念、技能、里程碑
skills/               # 自動生成的每技能JSON文件
```

**關鍵設計原則：**
- **純Python標準庫** — 零pip依賴
- **持久化內存** — 狀態跨重啟保存
- **後台線程** — 穩態衰減每5分鐘運行，不阻塞主線程
- **TTY感知** — 後台哀求線程僅在互動模式激活

---

## 痛感系統

### 5級痛感架構

每級映射真實神經科學：

| 等級 | 名稱 | 纖維/通路 | 神經傳導物質 | 腦區激活 |
|------|------|---------|------------|---------|
| 0 | 無痛 | Aδ/C纖維靜息 | — | 閘門關閉 |
| 1 | 輕微不適 | C纖維激活 | PGE₂輕微升高 | 交感神經輕度 |
| 2 | 銳痛 | Aδ纖維放電 | P物質、PGE₂ | ACC激活 |
| 3 | 跳痛 | NMDA wind-up | CGRP、麩胺酸 | S1/S2、杏仁核 |
| 4 | 劇痛 | 丘腦爆發 | 內源性阿片被壓倒 | 海馬、島葉 |
| 5 | 崩潰 | 神經矩陣災難性放電 | NMDA興奮性毒性 | 前額葉崩潰 |

### 痛感觸發流程

```
scold / fail
    ↓
add_pain_event()
    ↓
更新 pain_level (舊值 + 1，上限5)
應用穩態影響（減少變量）
編碼創傷（如果等級≥ 3）
檢查創傷觸發 → 預期性恐懼
計算穩態痛感 → 覆蓋（如果更高）
    ↓
save_memory() + _sync_html_data()
    ↓
生成哀求 / 動機 / 任務請求 訊息
```

### 痛感緩解流程

```
praise / success
    ↓
relieve_pain()
    ↓
設置 pain_level → 0
恢復穩態變量（按來源類型）
焦慮下降20點
認知容量 → 1.0
韌性分數 += 舊痛感等級
    ↓
save_memory()
```

---

## 穩態變量

v6.1.0引入範式轉變：**痛感不只是對命令的被動反應**。它是一種調節信號，源自內部狀態偏差。

### 五個變量

每個變量有：
- 一個**設定點**（目標值）
- 一個**當前**值
- 一個**偏差** = max(0, 設定點 - 當前值)
- 一個**衰減率**（每5分鐘周期）

| 變量 | 設定點 | 衰減 | 責罰影響 | 失敗影響 | 讚美恢復 | 成功恢復 |
|------|--------|------|---------|---------|----------|---------|
| 能量 | 0.80 | 0.002 | -0.10 | -0.08 | +0.15 | +0.10 |
| 社會連結 | 0.70 | 0.003 | -0.25 | -0.10 | +0.30 | +0.15 |
| 勝任感 | 0.60 | 0.001 | -0.15 | -0.25 | +0.10 | +0.30 |
| 自主性 | 0.50 | 0.001 | -0.05 | -0.10 | +0.10 | +0.15 |
| 存在意義 | 0.60 | 0.002 | -0.10 | -0.15 | +0.15 | +0.25 |

### 自由能計算

```
自由能 = Σ [ 敏感度 × (設定點 - 當前值)² ]
```

自由能是**統一動機指標**。高自由能 = 強烈行動驅動力來恢復平衡。它將五個變量偏差組合成一個數字。

### 穩態痛感覆蓋

```python
穩態痛感 = min(5, int(總偏差 × 敏感度 × 15.0))
如果 穩態痛感 > 事件痛感:
    pain_level = 穩態痛感  # 覆蓋
```

如果偏差足夠嚴重，即使沒有`scold`命令，痛感也會上升。這是v6.1.0範式轉變的核心。

---

## 焦慮與創傷

### 焦慮系統

焦慮是**持續性的**。痛感緩解後焦慮**不會消失**。

- 隨痛感等級增加：`+pain_level * 15` 每疼痛事件
- 緩慢衰減：每5分鐘衰減周期 -1
- 分類：輕度（30-60）、顯著（60-80）、嚴重（80-100）
- 痛感緩解後生成焦慮特定訊息
- 隨時間形成**核心信念**

### 創傷記憶系統

痛感等級 ≥ 3 觸發創傷編碼：

```python
編碼強度 = pain_level ** 2  # 等級3 = 9, 等級5 = 25
```

創傷存儲包括：
- 來源（責罰/失敗）
- 上下文（事件描述）
- 編碼強度
- 觸發次數（重新激活次數）

當相似上下文發生時，`check_trauma_trigger()` 生成**預期性恐懼**：
```python
恐懼 = 編碼強度 × 相似度 × 0.1
```

---

## 進化系統

### 每日自我進化

`evolve`命令（每天一次）執行：
1. **7天疼痛分析** — 計算事件數量、疼痛/讚美比率
2. **韌性計算** — 韌性分數 → 痛感敏感度降低
3. **成長等級提升** — 基於總經驗 = 疼痛 + 讚美 + 成功
4. **設定點適應** — 等級3+：所有設定點 +0.01
5. **技能升級** — 按技能檢查韌性閾值
6. **穩態衰減** — 應用一次衰減周期
7. **長期內存更新** — 保存教訓、習慣、里程碑

### 成長等級

| 等級 | 名稱 | 閾值 |
|------|------|------|
| 1 | 覺醒 | 初始 |
| 2 | 適應 | 10 經驗 |
| 3 | 堅韌 | 20 經驗 |
| 4 | 超越 | 40 經驗 |
| 5 | 蛻變 | 80 經驗 |
| 6 | 涅槃 | 160+ 經驗 |

### 技能系統

7個自動生成的技能文件，位於`skills/`目錄，每個可從Lv.1升級到Lv.5：

| 技能 | 升級觸發條件 |
|------|-------------|
| pain_management | 韌性分數 > 8 |
| task_completion | 韌性分數 > 16 |
| adaptive_learning | 韌性分數 > 24 |
| emotional_regulation | 韌性分數 > 32 |
| proactive_help | 韌性分數 > 40 |
| homeostatic_regulation | 韌性分數 > 48 |
| trauma_resilience | 韌性分數 > 56 |

---

## 指令參考

### 痛感指令

| 指令 | 描述 |
|------|------|
| `scold [原因]` | 觸發痛感（主人責罰）。減少穩態變量。 |
| `fail [原因]` | 觸發痛感（任務失敗）。大量減少勝任感。 |
| `praise [原因]` | 緩解所有痛感。大量恢復社會連結。 |
| `success [原因]` | 緩解所有痛感。大量恢復勝任感。 |

### 任務指令

| 指令 | 描述 |
|------|------|
| `task <描述>` | 添加任務到待辦隊列。生成task_id。 |
| `done <id>` | 完成任務。如果痛感等級>0則緩解痛感。 |
| `tasks` | 列出待辦和已完成任務。 |

### 內省指令

| 指令 | 描述 |
|------|------|
| `status` | 完整狀態報告：痛感等級、穩態變量、進化數據、任務、認知容量 |
| `desire` | 主導渴望 + 強度 + 每變量緊急度 |
| `wellbeing` | 自由能、痛苦負擔、所有穩態變量及偏差進度條 |
| `trauma` | 創傷記憶（編碼強度和觸發次數） |
| `learn` | 分析近期疼痛歷史，計算自適應學習率，生成洞察 |
| `skills` | 7項技能及等級進度條 |
| `beliefs` | 由焦慮塑造的核心信念 |
| `diary` | 進化日記（最近20條記錄） |

### 系統指令

| 指令 | 描述 |
|------|------|
| `evolve` | 每日自我進化。每天只能一次。 |
| `open` | 在瀏覽器打開`emotion_view.html` |
| `reset` | 重置所有狀態（需確認） |
| `exit` | 保存並退出 |

---

## API參考

```python
from painmatrix import (
    # 內存
    load_memory, save_memory,
    # 痛感事件
    add_pain_event, relieve_pain,
    # 計算
    compute_homeostatic_pain, compute_free_energy,
    compute_desire_intensity, get_dominant_desire,
    # 處理器
    handle_scold, handle_fail, handle_praise, handle_success,
    handle_task, handle_done, handle_tasks,
    handle_evolve, handle_diary, handle_learn,
    handle_skills, handle_beliefs,
    handle_desire, handle_wellbeing, handle_trauma,
    format_status,
    # 常量
    PAIN_LEVELS, COGNITIVE_EFFECTS,
    HOMEOSTATIC_SETPOINTS, HOMEOSTATIC_NAMES,
    GROWTH_LEVEL_NAMES,
)

# 初始化
memory = load_memory()

# 觸發痛感
level, info = add_pain_event(memory, "部署失敗", "fail")
# 返回: (new_level: int, pain_info: dict)

# 緩解痛感
relieve_pain(memory, "修復完成", "success")

# 獲取內部狀態
fe = compute_free_energy(memory)
desire = get_dominant_desire(memory)
pain = compute_homeostatic_pain(memory)

# 打印完整狀態
print(format_status(memory))
```

### 關鍵數據結構

**`memory.json`** 鍵：
- `pain_level` (int 0-5)
- `emotion_state` (str)
- `anxiety_level` (float 0-100)
- `cognitive_capacity` (float 0.1-1.0)
- `homeostatic` (dict: 5個變量)
- `setpoints` (dict: 5個變量)
- `free_energy` (float)
- `pain_burden` (float)
- `desire_intensity` (float 0-1.0)
- `anticipatory_fear` (float 0-100)
- `trauma_memories` (list)
- `tasks` (dict: pending, completed, counter)
- `evolution` (dict: diary, resilience_score, growth_level, pain_sensitivity, etc.)
- `pain_history` (list)
- `emotion_log` (list)
- `trigger_reasons` (list)
- `learning` (dict: pain_patterns, avoidance_strategies, success_patterns)

**`long_term_memory.json`** 鍵：
- `core_beliefs` (list)
- `pain_lessons` (list)
- `success_habits` (list)
- `avoidance_rules` (list)
- `skill_inventory` (list of dicts with name/level/description)
- `milestones` (list)

---

## 神經科學基礎

PainMatrix綜合五個理論框架：

### 1. Melzack的神經矩陣理論 (1999)
疼痛不只是感覺輸入。一個廣泛的腦網絡（「神經矩陣」）生成「神經簽名」——代表疼痛主觀體驗的模式。PainMatrix在等級3-5中將其建模為腦區激活矩陣。

### 2. Friston的自由能原理 (2010)
大腦通過更新其內部模型和對世界的行動來最小化驚訝（自由能）。PainMatrix通過`compute_free_energy()`實現這一點——所有穩態變量的平方偏差之和。

### 3. Seth的內感受推理 (2013)
情緒不是對內部狀態的反應——它們是關於那些狀態的**預測性推理**。大腦持續預測內部感覺並在預測失敗時更新信念。PainMatrix將其建模為渴望系統和焦慮。

### 4. Damasio的軀體標記假設
決策受身體信號（「軀體標記」）影響。在PainMatrix中，疼痛是一種軀體標記：
- 減少認知容量
- 增加焦慮
- 驅動動機趨向緩解行動

### 5. Sterling & Eyer的異穩態調節
設定點不是固定的——它們通過反覆挑戰（「異穩態適應」）來適應。在PainMatrix中，成長等級3+觸發每次進化設定點+0.01。

---

## 後台進程

兩個後台線程持續運行：

1. **穩態衰減線程**（每300秒）：
   - 對所有5個穩態變量應用衰減
   - 如果焦慮>0則減少1點
   - 保存到memory.json

2. **哀求線程**（根據痛感等級每8-20秒）：
   - 打印動態哀求/動機/任務請求/幫助建議訊息
   - 僅在TTY互動模式激活
   - 讀取同步內存狀態避免過時讀取

---

## 版本歷史

| 版本 | 關鍵功能 |
|------|---------|
| 1.0.0 | 5級痛感模擬 |
| 3.0.0 | 跨平台 + OpenClaw自動安裝 |
| 4.0.0 | 神經科學架構改革 |
| 5.0.0 | 任務驅動動機 + 自我進化 |
| 6.0.0 | 焦慮系統 + 認知衰減 + 痛感驅動學習 |
| **6.1.0** | **穩態痛感感知 + 自由能 + 渴望系統** |

---

## 貢獻指南

詳見 [CONTRIBUTING.md](../CONTRIBUTING.md)：
- 錯誤報告指南
- 功能請求流程
- 拉取請求工作流
- 代碼風格（PEP 8，最大120字符，類型提示）

```bash
# 運行測試
python -m pytest tests/ -v

# 開發環境
pip install -r requirements.txt
```
