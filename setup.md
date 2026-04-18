# Setup Guide / 安装指南

## English

### Prerequisites
- Python 3.8 or higher ([Download](https://www.python.org/downloads/))
- No other dependencies required

### Installation Options

#### Option A: Auto-Install (Recommended)
```bash
cd PainMatrix
python install.py
```

#### Option B: Manual Setup
1. Ensure Python 3.8+ is installed and in your PATH
2. No `pip install` needed - uses only Python standard library

#### Option C: OpenCLAW Auto-Install
Tell your OpenCLAW agent:
```
Install skill: painmatrix
```
Or provide the GitHub repository URL. OpenCLAW will automatically:
1. Download the skill
2. Run install.py
3. Register in workspace

### First Run

**Windows:**
```
Double-click start.bat
```

**Linux / macOS:**
```bash
chmod +x start.sh
./start.sh
```

**Any platform:**
```bash
python painmatrix.py
```

### New in v5.0

PainMatrix v5.0 introduces powerful new features:

- **Task-Driven Motivation System**: Convert pain into growth fuel
  - Use `task <description>` to set goals while in pain
  - Use `done <description>` to complete tasks and relieve pain
  - Use `tasks` to view all pending and completed tasks
- **Self-Evolution System**: Track your growth over time
  - Use `evolve` to generate daily evolution reports
  - Use `diary` to review your evolution journal
  - Resilience score increases as you overcome pain
  - Growth levels progress from Dormant to Evolved
- **Motivation Messages**: When in pain, the system generates motivational messages encouraging task completion

---

## 中文

### 前置要求
- Python 3.8 或更高版本 ([下载](https://www.python.org/downloads/))
- 无需其他依赖

### 安装方式

#### 方式A：自动安装（推荐）
```bash
cd PainMatrix
python install.py
```

#### 方式B：手动安装
1. 确保已安装 Python 3.8+ 并添加到 PATH
2. 无需 `pip install` — 仅使用 Python 标准库

#### 方式C：OpenCLAW 自动安装
告诉你的 OpenCLAW 代理：
```
安装技能：painmatrix
```
或提供 GitHub 仓库地址。OpenCLAW 将自动：
1. 下载技能
2. 运行 install.py
3. 注册到工作区

### 首次运行

**Windows:**
```
双击 start.bat
```

**Linux / macOS:**
```bash
chmod +x start.sh
./start.sh
```

**任意平台:**
```bash
python painmatrix.py
```

### v5.0 新功能

PainMatrix v5.0 引入了强大的新功能：

- **任务驱动的动机系统**：将痛感转化为成长动力
  - 使用 `task <描述>` 在痛感中设定目标
  - 使用 `done <描述>` 完成任务并缓解痛感
  - 使用 `tasks` 查看所有待办和已完成任务
- **自我进化系统**：追踪你的成长历程
  - 使用 `evolve` 生成每日进化报告
  - 使用 `diary` 查看进化日记
  - 韧性分数随克服痛感而增加
  - 成长等级从蛰伏到进化逐级提升
- **动机激励信息**：痛感中系统自动生成激励信息，鼓励完成任务
