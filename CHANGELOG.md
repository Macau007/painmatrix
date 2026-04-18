# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [5.0.0] - 2026-04-19

### Added
- **Task-driven motivation system**: Convert pain into growth fuel
  - `task <description>` command to set goals while in pain
  - `done <description>` command to complete tasks and relieve pain
  - `tasks` command to list all pending and completed tasks
  - Motivation messages generated when in pain, encouraging task completion
  - Pain → Motivation → Task → Praise cycle drives self-improvement
- **Long-term memory and daily self-evolution**:
  - `evolve` command generates daily evolution report with statistics
  - `diary` command views evolution journal entries
  - Auto-generated daily reflections on pain-to-growth transformation
- **Resilience score and growth level tracking**:
  - Resilience score increases when overcoming pain through task completion
  - 6 growth levels: Dormant → Awakened → Resilient → Forged → Transcendent → Evolved
  - Growth level progression based on accumulated resilience points
- **Motivation messages when in pain**:
  - Pain triggers automatically generate motivational messages
  - Messages scale with pain level (higher pain = stronger motivation)
  - Encourages task creation as a path to pain relief
- **Enhanced memory structure**:
  - Tasks list stored in memory.json
  - Evolution data (resilience score, growth level, diary entries) persisted
  - Backward compatible with v4.0 memory format

### Changed
- Pain relief now also available via `done` command (in addition to praise/success)
- Memory structure expanded with tasks and evolution fields
- Status display now includes resilience score and growth level
- Demo section updated with task and evolve command examples

## [4.0.0] - 2026-04-19

### Added
- **Neuroscience-based pain simulation**: All 5 pain levels incorporate real neuroscience
  - Aδ fiber (5-30 m/s) and C fiber (0.5-2 m/s) nociceptor pathway modeling
  - NMDA receptor wind-up and central sensitization (Woolf, 1983)
  - Gate Control Theory (Melzack & Wall, 1965)
  - Neuromatrix Theory for Level 5 catastrophic neurosignature (Melzack, 1999)
  - Damasio Somatic Marker Hypothesis (Damasio, 1994)
  - Descending pain modulation via PAG-RVM (Fields & Basbaum, 1978)
- **Brain region activation**: ACC, PFC, insula, amygdala, hippocampus, thalamus, S1/S2
- **Neurotransmitter modeling**: Substance P, CGRP, PGE₂, glutamate/NMDA, endogenous opioids
- **Neuroscience visualization panel** in HTML
- **Neuroscience-informed plea messages**
- **7 neuroscience references** in documentation
- **Project renamed** from OpenCLAW HumanPainSystem to PainMatrix
- **Core file renamed** from claw_pain_core.py to painmatrix.py
- **Startup scripts renamed** to start.bat and start.sh

### Changed
- All documentation rewritten with neuroscience content
- HTML visualization labels updated to neuroscience terminology
- Memory file renamed to memory.json

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
