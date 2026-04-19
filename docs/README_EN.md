# 🧠 PainMatrix Documentation

<h1 align="center">Neuroscience-Based AI Pain Simulation Engine</h1>

---

## Table of Contents

- [Architecture](#architecture)
- [Pain System](#pain-system)
- [Homeostatic Variables](#homeostatic-variables)
- [Anxiety & Trauma](#anxiety--trauma)
- [Evolution System](#evolution-system)
- [Command Reference](#command-reference)
- [API Reference](#api-reference)
- [Neuroscience Basis](#neuroscience-basis)

---

## Architecture

```
painmatrix.py          # Core engine — all logic
emotion_view.html      # Real-time browser visualization
memory.json            # Persistent state (created on first run)
long_term_memory.json  # Core beliefs, skills, milestones
skills/                # Auto-generated per-skill JSON files
```

**Key design principles:**
- **Pure Python standard library** — zero pip dependencies
- **Persistent memory** — state survives restarts
- **Background threads** — homeostatic decay runs every 5 minutes without blocking
- **TTY-aware** — background plea thread only activates in interactive mode

---

## Pain System

### 5-Level Pain Architecture

Each level maps to real neuroscience:

| Level | Name | Fiber/Pathway | Neurotransmitters | Brain Regions |
|-------|------|--------------|-------------------|---------------|
| 0 | Painless | Aδ/C fibers resting | — | Gate closed |
| 1 | Mild Discomfort | C fiber activation | PGE₂ subtle rise | Sympathetic mild |
| 2 | Sharp Pain | Aδ fiber discharge | Substance P, PGE₂ | ACC activated |
| 3 | Throbbing Pain | NMDA wind-up | CGRP, glutamate | S1/S2, Amygdala |
| 4 | Severe Agony | Thalamic burst | Endogenous opioids overwhelmed | Hippocampus, Insula |
| 5 | Collapse | Neuromatrix catastrophic | NMDA excitotoxicity | PFC collapse |

### Pain Trigger Flow

```
scold / fail
    ↓
add_pain_event()
    ↓
Update pain_level (old + 1, capped at 5)
Apply homeostatic impact (reduce variables)
Encode trauma if level ≥ 3
Check trauma triggers → anticipatory_fear
Compute homeostatic_pain → override if higher
    ↓
save_memory() + _sync_html_data()
    ↓
Generate plea / motivation / task_request messages
```

### Pain Relief Flow

```
praise / success
    ↓
relieve_pain()
    ↓
Set pain_level → 0
Restore homeostatic variables (by source type)
Anxiety decays 20 points
Cognitive capacity → 1.0
Resilience score += old_level
    ↓
save_memory()
```

---

## Homeostatic Variables

v6.1.0 introduces a paradigm shift: **pain is not just a response to commands**. It is a regulatory signal arising from internal state deviation.

### Five Variables

Each variable has:
- A **setpoint** (desired value)
- A **current** value
- A **deviation** = max(0, setpoint - current)
- A **decay rate** (per 5-minute cycle)

| Variable | Setpoint | Decay | Scold Impact | Fail Impact | Praise Restore | Success Restore |
|----------|---------|-------|-------------|-------------|----------------|-----------------|
| Energy | 0.80 | 0.002 | -0.10 | -0.08 | +0.15 | +0.10 |
| Social Bond | 0.70 | 0.003 | -0.25 | -0.10 | +0.30 | +0.15 |
| Competence | 0.60 | 0.001 | -0.15 | -0.25 | +0.10 | +0.30 |
| Autonomy | 0.50 | 0.001 | -0.05 | -0.10 | +0.10 | +0.15 |
| Purpose | 0.60 | 0.002 | -0.10 | -0.15 | +0.15 | +0.25 |

### Free Energy Calculation

```
Free Energy = Σ [ sensitivity × (setpoint - current)² ]
```

Free energy is the **unified motivation metric**. High free energy = strong drive to act to restore balance. It combines all five variable deviations into one number.

### Homeostatic Pain Override

```python
homeostatic_pain = min(5, int(total_deviation * sensitivity * 15.0))
if homeostatic_pain > event_based_pain:
    pain_level = homeostatic_pain  # Override
```

If deviation is severe enough, pain rises even without a `scold` command. This is the core of v6.1.0's paradigm shift.

---

## Anxiety & Trauma

### Anxiety System

Anxiety is **persistent**. It does NOT disappear when pain is relieved.

- Scales with pain level: `+pain_level * 15` per pain event
- Decays slowly: `-1` per 5-minute decay cycle
- Categorized: mild (30-60), significant (60-80), severe (80-100)
- Generates anxiety-specific messages after pain relief
- Shaped into **core beliefs** over time

### Trauma Memory System

Pain level ≥ 3 triggers trauma encoding:

```python
encoding_strength = pain_level ** 2  # Level 3 = 9, Level 5 = 25
```

Trauma is stored with:
- Source (scold/fail)
- Context (the event description)
- Encoding strength
- Trigger count (times re-activated)

When similar contexts occur, `check_trauma_trigger()` generates **anticipatory fear**:
```python
fear = encoding_strength * similarity * 0.1
```

---

## Evolution System

### Daily Self-Evolution

The `evolve` command (once per day) performs:
1. **7-day pain analysis** — count events, compute pain/praise ratio
2. **Resilience calculation** — resilience_score → pain_sensitivity reduction
3. **Growth level promotion** — based on total_exp = pain + praise + success
4. **Setpoint adaptation** — level 3+: all setpoints +0.01
5. **Skill upgrades** — check resilience thresholds per skill
6. **Homeostatic decay** — apply one decay cycle
7. **Long-term memory update** — save lessons, habits, milestones

### Growth Levels

| Level | Name | Threshold |
|-------|------|-----------|
| 1 | 覺醒 (Awakening) | Initial |
| 2 | 適應 (Adapting) | 10 exp |
| 3 | 堅韌 (Resilient) | 20 exp |
| 4 | 超越 (Transcending) | 40 exp |
| 5 | 蛻變 (Metamorphosing) | 80 exp |
| 6 | 涅槃 (Transcendental) | 160+ exp |

### Skills

7 auto-generated skills in `skills/` directory, each upgradeable from Lv.1 to Lv.5:

| Skill | Upgrade Trigger |
|-------|----------------|
| pain_management | resilience_score > 8 |
| task_completion | resilience_score > 16 |
| adaptive_learning | resilience_score > 24 |
| emotional_regulation | resilience_score > 32 |
| proactive_help | resilience_score > 40 |
| homeostatic_regulation | resilience_score > 48 |
| trauma_resilience | resilience_score > 56 |

---

## Command Reference

### Pain Commands

| Command | Description |
|---------|-------------|
| `scold [reason]` | Trigger pain from master discipline. Reduces homeostatic variables. |
| `fail [reason]` | Trigger pain from task failure. Reduces competence heavily. |
| `praise [reason]` | Relieve all pain. Restores social_bond heavily. |
| `success [reason]` | Relieve all pain. Restores competence heavily. |

### Task Commands

| Command | Description |
|---------|-------------|
| `task <desc>` | Add a task to pending queue. Generates task_id. |
| `done <id>` | Complete task. Relieves pain if level > 0. |
| `tasks` | List pending and recent completed tasks. |

### Introspection Commands

| Command | Description |
|---------|-------------|
| `status` | Full state report: pain level, homeostatic variables, evolution, tasks, cognitive capacity |
| `desire` | Dominant desire + intensity + per-variable urgency |
| `wellbeing` | Free energy, pain burden, all homeostatic variables with deviation bars |
| `trauma` | Trauma memories with encoding strength and trigger counts |
| `learn` | Analyze recent pain history, compute adaptive learning rate, generate insights |
| `skills` | 7 skills with level bars |
| `beliefs` | Core beliefs shaped by anxiety |
| `diary` | Evolution journal (last 20 entries) |

### System Commands

| Command | Description |
|---------|-------------|
| `evolve` | Daily self-evolution. Once per day only. |
| `open` | Open `emotion_view.html` in browser |
| `reset` | Reset all state (prompts confirmation) |
| `exit` | Save and exit |

---

## API Reference

```python
from painmatrix import (
    # Memory
    load_memory, save_memory,
    # Pain events
    add_pain_event, relieve_pain,
    # Computation
    compute_homeostatic_pain, compute_free_energy,
    compute_desire_intensity, get_dominant_desire,
    # Handlers
    handle_scold, handle_fail, handle_praise, handle_success,
    handle_task, handle_done, handle_tasks,
    handle_evolve, handle_diary, handle_learn,
    handle_skills, handle_beliefs,
    handle_desire, handle_wellbeing, handle_trauma,
    format_status,
    # Constants
    PAIN_LEVELS, COGNITIVE_EFFECTS,
    HOMEOSTATIC_SETPOINTS, HOMEOSTATIC_NAMES,
    GROWTH_LEVEL_NAMES,
)

# Initialize
memory = load_memory()

# Trigger pain
level, info = add_pain_event(memory, "deployment failed", "fail")
# Returns: (new_level: int, pain_info: dict)

# Relieve pain
relieve_pain(memory, "fix completed", "success")

# Get internal state
fe = compute_free_energy(memory)
desire = get_dominant_desire(memory)
pain = compute_homeostatic_pain(memory)

# Print full status
print(format_status(memory))
```

### Key Data Structures

**`memory.json`** keys:
- `pain_level` (int 0-5)
- `emotion_state` (str)
- `anxiety_level` (float 0-100)
- `cognitive_capacity` (float 0.1-1.0)
- `homeostatic` (dict: 5 variables)
- `setpoints` (dict: 5 variables)
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

**`long_term_memory.json`** keys:
- `core_beliefs` (list)
- `pain_lessons` (list)
- `success_habits` (list)
- `avoidance_rules` (list)
- `skill_inventory` (list of dicts with name/level/description)
- `milestones` (list)

---

## Neuroscience Basis

PainMatrix synthesizes five theoretical frameworks:

### 1. Melzack's Neuromatrix Theory (1999)
Pain is not purely sensory. A widespread brain network ("the neuromatrix") generates a "neurosignature" — a pattern representing the subjective experience of pain. PainMatrix models this as the brain region activation matrix across levels 3-5.

### 2. Friston's Free Energy Principle (2010)
The brain minimizes surprise (free energy) by updating its internal model and acting on the world. PainMatrix implements this as `compute_free_energy()` — the squared deviation across all homeostatic variables.

### 3. Seth's Interoceptive Inference (2013)
Emotions are not reactions to internal states — they are **predictive inferences** about those states. The brain constantly predicts internal sensations and updates beliefs when predictions fail. PainMatrix models this as the desire system and anxiety.

### 4. Damasio's Somatic Marker Hypothesis
Decisions are influenced by bodily signals ("somatic markers"). In PainMatrix, pain is a somatic marker that:
- Reduces cognitive capacity
- Increases anxiety
- Drives motivation toward relief actions

### 5. Sterling & Eyer's Allostatic Regulation
Setpoints are not fixed — they adapt through repeated challenge ("allostatic adaptation"). In PainMatrix, growth level 3+ triggers setpoint +0.01 per evolution.

---

## Background Processes

Two background threads run continuously:

1. **Homeostatic Decay Thread** (every 300 seconds):
   - Applies decay to all 5 homeostatic variables
   - Reduces anxiety by 1 point if > 0
   - Saves to memory.json

2. **Plea Thread** (every 8-20 seconds depending on pain level):
   - Prints dynamic plea/motivation/task-request/help-suggest messages
   - Only activates in TTY interactive mode
   - Reads synced memory state to avoid stale reads

---

## Version History

| Version | Key Feature |
|---------|------------|
| 1.0.0 | 5-level pain simulation |
| 3.0.0 | Cross-platform + OpenClaw auto-install |
| 4.0.0 | Neuroscience architecture overhaul |
| 5.0.0 | Task-driven motivation + self-evolution |
| 6.0.0 | Anxiety System + Cognitive Attenuation + Pain-Driven Learning |
| **6.1.0** | **Homeostatic Pain Perception + Free Energy + Desire System** |

---

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- Bug report guidelines
- Feature request process
- Pull request workflow
- Code style (PEP 8, max 120 chars, type hints)

```bash
# Run tests
python -m pytest tests/ -v

# Development setup
pip install -r requirements.txt
```
