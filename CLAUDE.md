# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project

*Beyond Self-Driving* is a 5-part animated ICCV 2025 tutorial video (~50–60 min total) built with **ManimGL**. The five parts form a causal chain:

| Part | Title | Core question answered |
|---|---|---|
| 1 | Foundation Models for AV | Why do foundation models matter, and how do VLAs work? |
| 2 | Cooperative Perception | How do multiple agents fuse spatio-temporal information? |
| 3 | Sim-to-Real Engineering | How is this actually deployed on real hardware? |
| 4 | Efficiency | How do we scale up data, training, and inference? |
| 5 | Physical AI | How do we extend from cars to a human-centric world? |

Each part's bridge scene motivates the next, so parts should feel narratively connected.

---

## Repository layout

```
studio/             — ManimGL animation package (primary codebase)
  CLAUDE.md         — Render commands, env setup, ManimGL quirks, full component map
  REWORK_PROMPTS.md — 5-phase fix guide (quote fix → images → layout → polish → render)
  components/       — Shared palette, typography, layout, animation helpers
  scenes/           — 84 scene files: intro/ + part01/–part05/

materials/
  scripts/          — Original Vietnamese narration scripts (slide-based; slightly outdated)
  slides/           — Presenter slide PDFs/PPTXs (source of technical content)
  images/           — Extracted slide images per part

plans/              — 12 execution/design plan files from planning sessions
spec_prompts/       — Scene-level production specs + three review rounds

studio_scripts/     — Authoritative scene-aligned scripts (coherent with current code)

render_studio_all.ps1   — Batch render all scenes at low quality
merge_videos.ps1        — Post-render video concatenation
```

---

## Rendering

See `studio/CLAUDE.md` for full environment setup, render flags, ManimGL vs. Manim CE API differences, component map, and known quirks (white text, curly quotes, depth testing).

Default for user-requested renders: use HD (`--hd`), not low-quality preview (`-l`), unless the user explicitly asks for preview/low quality.

Quick render reference (Windows):
```powershell
$env:PYTHONPATH = "C:\Users\admin\Downloads\ML\Lab01_3B1B"
# Single scene (HD)
manimgl -w --hd studio/scenes/part01/p01_s02a_genai_timeline.py P01S02AGenAITimeline
# All scenes
.\render_studio_all.ps1
```

Quick render reference (macOS — this machine; `manimgl` lives in the `manim` conda env, NOT on base PATH):
```bash
cd "/Users/phu-quynguyen-lam/o D/Beyond_SelfDriving"
PYTHONPATH="$PWD" /Users/phu-quynguyen-lam/miniforge3/envs/manim/bin/manimgl \
  -w --hd studio/scenes/part01/p01_s02a_genai_timeline.py P01S02AGenAITimeline
```

Output: `videos/<ClassName>.mp4`. Frame extraction with ffmpeg + more detail in `studio/CLAUDE.md`.

---

## Scene naming

Files follow `p<part>_s<num>[a|b|c]_<slug>.py`, class names match `P01S02AGenAITimeline`. Intro scenes use `i01_`–`i04_` / `I01TitleCard`–`I04BridgeToP1`.

3D scenes (`Studio3DScene`): `i02_the_hook.py` and `p02_s05_radar_waves.py` — skip during layout-only edits.

---

## Scripts

`studio_scripts/script_part1.md`–`script_part5.md` are the **authoritative narration scripts**, organized by scene class (`## [ClassName — "Scene Title"]`). Use these for voice recording and when checking whether scene content matches narration.

`materials/scripts/` is an older reference (slide-based, pre-code). When a scene changes significantly, update the matching section in `studio_scripts/`.

---

## Design rules (non-negotiable)

- Background: `BG_PAPER` (`#FFF9E6`) everywhere; `BG_TITLECARD` only for dark quote-card scenes
- Every scene ends with `self._close()` — final frame must be blank BG_PAPER
- Axes animated **before** data (`axes_deploy()` returns `(axes, anim)` — play anim first)
- No curly quotes `" "` in `Text()` literals — use ASCII `"` or explicit `“`/`”`
- Never hardcode hex colors — import from `studio/components/colors.py`
- On-screen text: English only; narration: Vietnamese (in `studio_scripts/`)
