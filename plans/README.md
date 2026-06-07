# Plans Index

Detailed rework plans for the Beyond Self-Driving Manim tutorial. Read in order.

| # | File | What's in it |
|---|---|---|
| 00 | [00_MASTER_PLAN.md](00_MASTER_PLAN.md) | Overview, phases, acceptance gates |
| 01 | [01_DESIGN_SYSTEM.md](01_DESIGN_SYSTEM.md) | White theme, colors, typography, **bubble specs**, mascot specs, layout rules |
| 02 | [02_COMPONENTS.md](02_COMPONENTS.md) | Exact edits to `drivex/components/*.py` (Phase 1) |
| 03 | [03_NARRATIVE_AUDIT.md](03_NARRATIVE_AUDIT.md) | Slide-to-scene mapping, why each paper is named, **creative liberty rules** |
| 04 | [04_PART_INTRO_AND_PART01.md](04_PART_INTRO_AND_PART01.md) | Per-scene plan: Intro (3) + Part 1 (9 scenes) |
| 05 | [05_PART02.md](05_PART02.md) | Per-scene plan: Part 2 (12 scenes) |
| 06 | [06_PART03.md](06_PART03.md) | Per-scene plan: Part 3 (14 scenes) |
| 07 | [07_PART04.md](07_PART04.md) | Per-scene plan: Part 4 (10 scenes) |
| 08 | [08_PART05.md](08_PART05.md) | Per-scene plan: Part 5 (9 scenes) |
| 09 | [09_FIX_CHECKLIST.md](09_FIX_CHECKLIST.md) | Consolidated fix list from 3 review rounds + universal rules |
| 10 | [10_EXECUTION_WORKFLOW.md](10_EXECUTION_WORKFLOW.md) | Step-by-step procedure for executing per scene |

## Recommended reading order for Sonnet 4.6

1. [../CLAUDE.md](../CLAUDE.md) — orient yourself
2. [00_MASTER_PLAN.md](00_MASTER_PLAN.md) — what's the overall goal
3. [10_EXECUTION_WORKFLOW.md](10_EXECUTION_WORKFLOW.md) — how to do work
4. [01_DESIGN_SYSTEM.md](01_DESIGN_SYSTEM.md) — visual language
5. Then jump to the specific part you're executing.

`09_FIX_CHECKLIST.md` is a lookup — read the row when you open a scene file, not end-to-end.

## Quick command reference

```powershell
# Render single scene (preview)
manim -ql drivex\scenes\part01\p01_s04_longtail.py P01S04LongTail

# Render whole part
.\drivex\render\render_part01.ps1

# Smoke test (after Phase 1)
manim -ql drivex\scenes\_smoke_test.py SmokeTest

# Final 1080p (only after user sign-off)
.\drivex\render\render_all_final.ps1
```

## Key decisions captured here

- **White background** is the new default. Navy is reserved for part-title cards and the final emotional dark frame.
- **Tight bubbles**: text + small pad. No more 3.2u-wide bubbles for "Hi.".
- **One PI bubble at a time**: show, hold ≥ 1s, fade. Don't stack.
- **English on screen.** Vietnamese narration is for voiceover only.
- **Axes before data.** Always.
- **Scene end is clean.** No leftover mobjects.
- **Roadmap strip** = title-card-only feature. Body scenes don't show it.
- **Creative liberty granted** for layout/redrawing/quote-promotion; locked for paper names, numbers, argument order.
