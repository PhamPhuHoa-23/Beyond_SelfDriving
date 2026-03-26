# Beyond Self-Driving — Project Plan & Documentation
## Manim Video (3B1B Style) — ICCV 2025 Tutorial

---

## Project Overview

| Field | Value |
|---|---|
| Tutorial | Beyond Self-Driving (UCLA Mobility Lab, ICCV 2025) |
| Style | 3Blue1Brown — dark backgrounds, animated mascots, progressive reveal |
| Render quality (test) | `-ql` (480p 15fps) |
| Render quality (final) | `-qh` (1080p 60fps) or `-qk` (2160p 60fps) |
| Manim version | Community v0.20.1 |
| Python env | Base conda (`C:\Users\admin\miniconda3\Scripts\manim.exe`) |
| Project root | `drivex/` |

> **IMPORTANT — Environment note**: Manim is installed in the **base** conda environment,
> NOT in `manim_env`. Run `manim` directly (do not `conda activate manim_env` before rendering,
> or ensure base env is active). The `manim_env` conda environment only has pip/setuptools.

---

## Directory Structure

```
drivex/
├── __init__.py
├── PLAN.md                  ← this file
│
├── components/              ← reusable building blocks
│   ├── __init__.py          # re-exports everything
│   ├── colors.py            # canonical color palette (all COL_* prefixed)
│   ├── mascots.py           # CarMascot, PiMascot VGroup classes
│   ├── thought_bubble.py    # ThoughtBubble, PIBubble, SpeechBubble
│   ├── roadmap.py           # RoadmapStrip (full + mini variants)
│   ├── title_card.py        # PartTitleCard + make_part_title_card()
│   └── slide_helper.py      # SlideImage with graceful fallback
│
├── scenes/
│   ├── __init__.py
│   ├── intro/               # INTRODUCTION (3 scenes)
│   │   ├── i01_title_card.py
│   │   ├── i02_hook.py
│   │   └── i03_roadmap.py
│   ├── part01/              # Part 01 — Overview & VLA (9 scenes)
│   │   ├── p01_s01_opening.py
│   │   ├── p01_s02_genai_boom.py
│   │   ├── p01_s03_av_arch.py
│   │   ├── p01_s04_longtail.py
│   │   ├── p01_s05_fm_empower.py
│   │   ├── p01_s06_vla_roadmap.py
│   │   ├── p01_s07_vla_arch.py
│   │   ├── p01_s08_autovla.py
│   │   └── p01_s09_takeaways.py
│   ├── part02/              # Part 02 — Cooperative Perception (5+ scenes)
│   │   └── p02_s01_title.py (+ stubs p02_s02–p02_s05)
│   ├── part03/              # Part 03 — Infrastructure & Calibration (6+ scenes)
│   │   └── p03_s01_title.py (+ stubs p03_s02–p03_s06)
│   └── part04/              # Part 04 — Efficiency & Scalability (5+ scenes)
│       └── p04_s01_title.py (+ stubs p04_s02–p04_s05)
│
├── assets/                  ← user-provided images go here
│   ├── car_mascot.svg        # (optional) replaces geometric fallback
│   ├── pi_mascot.svg         # (optional) replaces geometric fallback
│   ├── part01/
│   ├── part02/
│   ├── part03/
│   └── part04/
│
└── render/
    ├── render_intro.ps1
    ├── render_part01.ps1
    ├── render_part02.ps1
    ├── render_part03.ps1
    └── render_part04.ps1
```

---

## Scene Inventory

### Introduction (est. 3 min)

| ID | File | Class | Status | Duration |
|---|---|---|---|---|
| I-01 | `scenes/intro/i01_title_card.py` | `I01TitleCard` | ✅ Complete | ~45s |
| I-02 | `scenes/intro/i02_hook.py` | `I02Hook` | ✅ Complete | ~75s |
| I-03 | `scenes/intro/i03_roadmap.py` | `I03Roadmap` | ✅ Complete | ~30s |

### Part 01 — AI Foundation Models Meet Autonomous Driving (est. 12–15 min)

| ID | File | Class | Status | Description |
|---|---|---|---|---|
| 1-01 | `scenes/part01/p01_s01_opening.py` | `P01S01Opening` | ✅ Complete | Opening question + PI mascot |
| 1-02 | `scenes/part01/p01_s02_genai_boom.py` | `P01S02GenAIBoom` | ✅ Complete | GenAI capability explosion |
| 1-03 | `scenes/part01/p01_s03_av_arch.py` | `P01S03AVArch` | ✅ Complete | Modular vs E2E vs Hybrid |
| 1-04 | `scenes/part01/p01_s04_longtail.py` | `P01S04LongTail` | ✅ Complete | Long-tail distribution |
| 1-05 | `scenes/part01/p01_s05_fm_empower.py` | `P01S05FMEmpower` | ✅ Complete | FM × AV requirements matrix |
| 1-06 | `scenes/part01/p01_s06_vla_roadmap.py` | `P01S06VLARoadmap` | ✅ Complete | VLA timeline + DriveLM chain |
| 1-07 | `scenes/part01/p01_s07_vla_arch.py` | `P01S07VLAArch` | ✅ Complete | 4 VLA architectures |
| 1-08 | `scenes/part01/p01_s08_autovla.py` | `P01S08AutoVLA` | ✅ Complete | AutoVLA dual-mode + training |
| 1-09 | `scenes/part01/p01_s09_takeaways.py` | `P01S09Takeaways` | ✅ Complete | 2×2 takeaway grid |

### Part 02 — Cooperative Perception (est. 12–15 min)

| ID | File | Class | Status | Description |
|---|---|---|---|---|
| 2-01 | `scenes/part02/p02_s01_title.py` | `P02S01Title` | ✅ Complete | Part title card |
| 2-02 | `scenes/part02/p02_s01_title.py` | `P02S02Background` | ⬜ Stub | Traffic death stats / Waymo |
| 2-03 | `scenes/part02/p02_s01_title.py` | `P02S03Evolution` | ⬜ Stub | Single-agent AV evolution timeline |
| 2-04 | `scenes/part02/p02_s01_title.py` | `P02S04Occlusion` | ⬜ Stub | Occlusion problem (LiDAR blind zone) |
| 2-05 | `scenes/part02/p02_s01_title.py` | `P02S05RelatedWorks` | ⬜ Stub | V2VNet → Where2comm timeline |

### Part 03 — Infrastructure-Assisted Sensing (est. 12–15 min)

| ID | File | Class | Status | Description |
|---|---|---|---|---|
| 3-01 | `scenes/part03/p03_s01_title.py` | `P03S01Title` | ✅ Complete | Part title card |
| 3-02 | `scenes/part03/p03_s01_title.py` | `P03S02FourPillars` | ⬜ Stub | Hardware / Data / Calib / Localization pillars |
| 3-03 | `scenes/part03/p03_s01_title.py` | `P03S03HardwareData` | ⬜ Stub | RSU hardware + dataset scale |
| 3-04 | `scenes/part03/p03_s01_title.py` | `P03S04Calibration` | ⬜ Stub | Roadside calibration pipeline |
| 3-05 | `scenes/part03/p03_s01_title.py` | `P03S05Localization` | ⬜ Stub | HD map-free localization |
| 3-06 | `scenes/part03/p03_s01_title.py` | `P03S06DigitalTwin` | ⬜ Stub | Digital twin pipeline |

### Part 04 — Efficiency & Scalability (est. 12–15 min)

| ID | File | Class | Status | Description |
|---|---|---|---|---|
| 4-01 | `scenes/part04/p04_s01_title.py` | `P04S01Title` | ✅ Complete | Part title card |
| 4-02 | `scenes/part04/p04_s01_title.py` | `P04S02WhyEfficiency` | ⬜ Stub | Why efficiency matters |
| 4-03 | `scenes/part04/p04_s01_title.py` | `P04S03DataBottleneck` | ⬜ Stub | Data generation bottleneck |
| 4-04 | `scenes/part04/p04_s01_title.py` | `P04S04TrainingBottleneck` | ⬜ Stub | Training cost (SFT→GRPO) |
| 4-05 | `scenes/part04/p04_s01_title.py` | `P04S05InferenceBottleneck` | ⬜ Stub | Inference time constraints |

---

## Color Palette

Defined in `components/colors.py`. Always import from there — never hardcode hex.

| Constant | Hex | Usage |
|---|---|---|
| `BG_DARK` | `#0F172A` | Default scene background |
| `BG_BLACK` | `#0D0D0D` | Ultra-dark overlay sections |
| `COL_NAVY` | `#1F3864` | Headers, heavy boxes |
| `COL_BLUE` | `#2E75B6` | Accent, arrows, highlights |
| `COL_GOLD` | `#E8A838` | Quotes, emphasis, key terms |
| `COL_LIGHT_BLUE` | `#EAF4FB` | Info boxes, subtitles |
| `COL_WHITE` | `#FFFFFF` | Body text on dark bg |
| `COL_RED` | `#C0392B` | Warnings, ✗ marks |
| `COL_GREEN` | `#27AE60` | ✓ marks, positive outcomes |
| `COL_PURPLE` | `#7C3AED` | VLA, AI model accents |
| `COL_INFRA_ORANGE` | `#F97316` | Infrastructure highlights (Part 03) |
| `COL_SENSOR_CYAN` | `#06B6D4` | Sensor data (Part 03) |
| `COL_INT8_GREEN` | `#10B981` | INT8/quantization (Part 04) |
| `COL_ENERGY_YELLOW` | `#FBBF24` | Energy / compute cost (Part 04) |

---

## Asset Conventions

Images are loaded by `SlideImage("partXX/slide_NN_description.png")`.
The helper shows a labeled placeholder rectangle if the file is missing —
so renders always succeed even without real assets.

Place real images here:
```
drivex/assets/
├── part01/slide_01_*.png    # GenAI icons, AV diagram, etc.
├── part02/slide_01_*.png    # Cooperative perception diagrams
├── part03/slide_01_*.png    # RSU hardware, calibration images
└── part04/slide_01_*.png    # Efficiency charts
```

---

## Mascots

| Mascot | Class | Description |
|---|---|---|
| `CAR` | `CarMascot` | Guide character — car-shaped, BLUE body |
| `PI` | `PiMascot` | Curious questioner — round, GOLD |

Both fall back to simple geometric VGroups if SVG files are missing.
To use real SVGs: place `car_mascot.svg` and `pi_mascot.svg` in `drivex/assets/`.

Animate with: `idle_bounce(mascot, amplitude=0.08, run_time=1.5)`

---

## How to Render

### Single scene (fastest — for testing):
```powershell
cd c:\Users\admin\Downloads\ML\Lab01_3B1B\drivex
manim -ql scenes\intro\i01_title_card.py I01TitleCard
```

### Full part:
```powershell
cd c:\Users\admin\Downloads\ML\Lab01_3B1B\drivex
.\render\render_intro.ps1
.\render\render_part01.ps1
.\render\render_part02.ps1
.\render\render_part03.ps1
.\render\render_part04.ps1
```

### Final quality render (when ready):
Replace `-ql` with `-qh` (1080p) or `-qk` (4K) in the render scripts.

### Output location:
`drivex/media/videos/<scene_folder>/480p15/<ClassName>.mp4`

---

## Component API Reference

### `SlideImage(rel_path, width, height)`
Load an image from `assets/`. Shows labeled placeholder if missing.
```python
img = SlideImage("part01/slide_05_fm_diagram.png", width=5, height=3)
```

### `RoadmapStrip(current_part, mini, spine_width)`
5-node journey strip. `mini=True` for bottom-of-screen strip in title cards.
```python
strip = RoadmapStrip(current_part=1, mini=True)
```

### `PartTitleCard` / `make_part_title_card()`
Reusable part title with roadmap strip.
```python
scene = make_part_title_card(
    part_num=2,
    title="Cooperative Perception",
    speaker="...",
    callback_quote="..."
)
```

### `PIBubble(target, text, position)` / `SpeechBubble(target, text, position)`
Thought/speech bubbles auto-positioned relative to a target mobject.
```python
bubble = PIBubble(pi_mascot, "Why cooperate?", position=UP)
```

---

## Implementation Status Summary

| Part | Scenes complete | Scenes total |
|---|---|---|
| INTRO | 3 | 3 |
| Part 01 | 9 | 9 |
| Part 02 | 1 | 5+ |
| Part 03 | 1 | 6+ |
| Part 04 | 1 | 5+ |
| **Total** | **15** | **28+** |

---

## Next Implementation Steps

1. **Implement Part 02 full scenes** — read `spec_prompts/spec_part02.md`
   - `p02_s02_background.py` → crowd grid, death statistics, Waymo 80% reduction
   - `p02_s03_evolution.py` → PnPNet → GameFormer → UniAD → DiffusionDrive timeline
   - `p02_s04_occlusion.py` → LiDAR single vs multi-agent blind zone comparison
   - `p02_s05_related_works.py` → V2VNet, V2X-ViT, Where2comm, CodeFilling

2. **Implement Part 03 full scenes** — read `spec_prompts/spec_part03.md`

3. **Implement Part 04 full scenes** — read `spec_prompts/spec_part04.md`

4. **Update render scripts** — each stub class will move to its own file;
   update file paths in `render_part02.ps1` etc. accordingly

5. **Provide real assets** — replace placeholder rectangles with actual images
