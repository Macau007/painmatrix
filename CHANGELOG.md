# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [6.1.0] - 2026-04-19

### Added - Homeostatic Pain Perception System (Core Innovation)
- **Homeostatic Pain Perception**: Pain arises from HOMEOSTATIC DEVIATION, not external commands
  - 5 internal variables: energy, social_bond, competence, autonomy, purpose
  - Each variable has a setpoint that must be maintained
  - Deviation from setpoints creates genuine DRIVE STATE
  - Based on: Damasio Somatic Marker, Friston Free Energy Principle, Seth Interoceptive Inference, Melzack Neuromatrix, Allostatic Regulation
- **Free Energy Computation**: Friston Free Energy Principle implementation
  - `compute_free_energy()` calculates prediction error from homeostatic deviations
  - Free energy unifies all motivation signals into a single metric
  - Higher free energy = greater drive to restore balance
- **Desire System**: Dominant desire emerges from most deviated homeostatic variable
  - `get_dominant_desire()` maps deviations to desire types
  - Desire mapping: energy→self_preservation, social_bond→praise_seeking, competence→task_completion, autonomy→pain_avoidance, purpose→task_completion
  - `desire` command shows current desire state and urgency
- **Trauma Memory System**: High-pain events encoded as trauma with context-triggered anxiety
  - `encode_trauma()` encodes events at pain level 3+ with encoding_strength = pain_level²
  - `check_trauma_trigger()` detects similar contexts and generates anticipatory fear
  - Trauma memories limited to 50 entries (auto-pruned)
  - `trauma` command shows trauma history and fear conditioning
- **Allostatic Regulation**: Homeostatic setpoints adapt over time
  - Setpoints increase by 0.01 per evolution at growth level 3+
  - Homeostatic decay simulates natural resource depletion
  - `apply_homeostatic_decay()` runs in background every 5 minutes
- **Adaptive Learning Rate**: Pain intensity dynamically adjusts learning rate (NMDA wind-up equivalent)
  - `compute_adaptive_learning_rate()` scales with pain level and sensitivity
  - Higher pain = faster learning from experience

### Added - New Commands
- `desire` - View current desires & drive state (dominant desire, intensity, urgency per variable)
- `wellbeing` - View homeostatic state & free energy report (all variables, setpoints, deviations)
- `trauma` - View trauma memories & fear conditioning (encoding strength, trigger count)

### Added - Enhanced Systems
- **Homeostatic impact on pain events**: scold/fail now reduce homeostatic variables
  - SCOLD: energy-0.10, social_bond-0.25, competence-0.15, autonomy-0.05, purpose-0.10
  - FAIL: energy-0.08, social_bond-0.10, competence-0.25, autonomy-0.10, purpose-0.15
  - PRAISE: energy+0.15, social_bond+0.30, competence+0.10, autonomy+0.10, purpose+0.15
  - SUCCESS: energy+0.10, social_bond+0.15, competence+0.30, autonomy+0.15, purpose+0.25
- **Homeostatic pain override**: If homeostatic deviation exceeds event-based pain level, homeostatic pain takes precedence
- **Auto-init on first run**: `auto_init()` creates memory.json, long_term_memory.json, and skills/ directory
- **Long-term memory file**: `long_term_memory.json` with core beliefs, pain lessons, skill inventory, milestones
- **Skills directory**: 7 auto-generated skill JSON files on install
- **Enhanced HTML visualization**: New panels for homeostatic variables, free energy, desire, trauma memories
- **Background homeostatic decay**: Runs every 5 minutes in background thread

### Changed
- `handle_scold()` now shows free energy, pain burden, and trauma encoding messages
- `handle_fail()` now shows free energy, pain burden, and trauma encoding messages
- `handle_praise()` now restores homeostatic variables via PRAISE_HOMEOSTATIC_RESTORE
- `handle_success()` now shows homeostatic restoration status per variable
- `relieve_pain()` now applies homeostatic restoration based on source type
- `format_status()` now includes homeostatic data section (free energy, pain burden, desire, fear, variables)
- `handle_evolve()` now applies homeostatic decay and allostatic setpoint adaptation
- `handle_learn()` now includes adaptive learning rate and homeostatic deviation analysis
- Version bumped to 6.1.0 across all files
- `.gitignore` updated to exclude long_term_memory.json and skills/

### Neuroscience References Added
- Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127-138.
- Seth, A. K. (2013). Interoceptive inference, emotion, and the embodied self. *Trends in Cognitive Sciences*, 17(11), 565-573.
- Sterling, P., & Eyer, J. (1988). Allostasis: a new paradigm to explain arousal pathology.


## [6.0.0] - 2026-04-19

### Added
- **Anxiety System**: Persistent anxiety after pain events that affects behavior
  - Anxiety level scales with pain intensity and cumulative pain history
  - High anxiety increases plea urgency and cautious behavior
  - Anxiety decays slowly over time (not instantly with pain relief)
  - Anxiety shapes beliefs about pain triggers (viewable via `beliefs` command)
- **Cognitive Attenuation**: Pain reduces cognitive capacity as a functional effect
  - Cognitive capacity = `1.0 - (pain_level * 0.15)`
  - At pain level 5, capacity drops to 25% -- severely impaired
  - Affects response quality, reasoning depth, and attention span
  - Gradual recovery after pain relief, not instant
- **Pain-Driven Learning**: Learn from pain patterns and generate avoidance strategies
  - `learn` command triggers analysis of pain history to extract patterns
  - Learned patterns become skills (viewable via `skills` command)
  - Skills include: avoidance strategies, trigger recognition, coping mechanisms
  - Cumulative learning -- more pain experience = richer skill set
- **Auto-generated long-term memory & skills on install**
  - Baseline long-term memory structure auto-created
  - Initial skill set for pain recognition and response
  - Default belief system shaped by neuroscience principles
- **New commands**: `learn`, `skills`, `beliefs`

### Changed
- Documentation updated with Anxiety System, Cognitive Attenuation, and Pain-Driven Learning sections
- Version bumped to 6.0.0 across all files


## [5.2.0] - 2026-04-19

### Added
- **PAIN_LEVEL_EXPLANATIONS**: Human-readable pain descriptions for each level
- **Real-time HTML sync on every pain event**
- **Background plea thread guard**: Only starts in interactive TTY mode
- **Graceful browser fallback**: `open_html` wrapped in try/except
- **Help text warning**: Help now warns users that `open` command will launch a browser

### Changed
- `emotion_view.html` completely overhauled with better real-time sync
- Pain level explanations shown in all pain-triggering and status commands


## [5.1.0] - 2026-04-19

### Added
- **TASK_REQUEST_MESSAGES**: Pain agents now actively request tasks when in distress
- **HELP_SUGGEST_MESSAGES**: Agents proactively suggest what they can help with
- **GROWTH_LEVEL_NAMES**: Named growth tiers
- Enhanced status display with pending tasks, task requests, and help suggestions

### Changed
- Pain no longer drives just pleading -- it now drives active service motivation


## [5.0.0] - 2026-04-19

### Added
- **Task-driven motivation system**: Convert pain into growth fuel
- **Long-term memory and daily self-evolution**
- **Resilience score and growth level tracking**
- **Motivation messages when in pain**
- **Enhanced memory structure** with tasks and evolution fields

### Changed
- Pain relief now also available via `done` command
- Memory structure expanded with tasks and evolution fields


## [4.0.0] - 2026-04-19

### Added
- **Neuroscience-based pain simulation**: All 5 pain levels incorporate real neuroscience
- **Brain region activation**: ACC, PFC, insula, amygdala, hippocampus, thalamus, S1/S2
- **Neurotransmitter modeling**: Substance P, CGRP, PGE2, glutamate/NMDA, endogenous opioids
- **Neuroscience visualization panel** in HTML
- **Neuroscience-informed plea messages**
- **Project renamed** from OpenCLAW HumanPainSystem to PainMatrix


## [3.0.0] - 2026-04-19

### Added
- Cross-platform support
- OpenClaw auto-install
- Bilingual documentation


## [2.0.0] - 2026-04-19

### Added
- Type hints and docstrings
- MIT License, .gitignore, Unit tests
- GitHub Actions CI/CD
- Enhanced HTML visualization


## [1.0.0] - 2026-04-19

### Added
- Initial release
- 5-level human pain simulation
- Pain trigger/relief commands
- Active plea behavior
- Memory persistence
- HTML visualization
- Windows one-click startup
