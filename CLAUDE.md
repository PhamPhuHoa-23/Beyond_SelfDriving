# CLAUDE.md — Beyond Self-Driving (3B1B-style Manim Tutorial)

> Project-level knowledge for any Claude session opening this repo.
> Source: ICCV 2025 tutorial **"Beyond Self-Driving"** by UCLA Mobility Lab.
> Goal: produce a 3Blue1Brown-style animated tutorial video summarizing 5 parts (~50–60 min total) on a **WHITE background**, with narrative mascots and clean layouts.

---

## TL;DR for a fresh Claude session

1. **Working code lives in [drivex/](drivex/).** It already has draft scenes from ~1 month ago that need rework.
2. **[drivex_white/](drivex_white/) is an earlier white-theme test** — *do not* edit it; treat it as a reference snapshot. Active work is on `drivex/`.
3. **Authoritative narrative** is in [materials/scripts/](materials/scripts/) (`script_part1.md` … `script_part5.md`) and the original slide PDFs in [materials/slides/](materials/slides/).
4. **Detailed rework plans** live in [plans/](plans/). Read [plans/00_MASTER_PLAN.md](plans/00_MASTER_PLAN.md) first, then the per-part plan you are executing.
5. **Three review rounds** have already happened — every scene-level critique is consolidated in [plans/09_FIX_CHECKLIST.md](plans/09_FIX_CHECKLIST.md). When you touch a scene, check that file.
6. **The user is Vietnamese-speaking** and writes specs in mixed Vietnamese / English. Comment style and narration may be Vietnamese; on-screen text should be **English** (per first review feedback: "Pi đang nói tiếng việt, đổi hết thành tiếng anh").

---

## Project structure

```
Lab01_3B1B/
├── CLAUDE.md                      ← this file
├── README.md                      ← env setup (conda, LaTeX, Latin Modern Roman)
├── requirements.txt
│
├── drivex/                        ← MAIN WORKING CODE (white theme already applied)
│   ├── __init__.py
│   ├── PLAN.md                    ← legacy plan, partially stale
│   ├── components/                ← reusable building blocks
│   │   ├── colors.py              ← canonical palette (white BG, dark text)
│   │   ├── mascots.py             ← CarMascot, PiMascot
│   │   ├── thought_bubble.py      ← speech / thought bubbles
│   │   ├── roadmap.py             ← 5-node journey strip
│   │   ├── title_card.py          ← reusable part title
│   │   └── slide_helper.py        ← SlideImage with placeholder fallback
│   ├── scenes/
│   │   ├── intro/                 ← I-01..I-03 (3 scenes)
│   │   ├── part01/                ← P01-S01..P01-S09 (9 scenes — Foundation Models)
│   │   ├── part02/                ← P02-S01..P02-S12 (12 scenes — Cooperative Perception)
│   │   ├── part03/                ← P03-S01..P03-S14 (14 scenes — Sim-to-Real)
│   │   ├── part04/                ← P04-S01..P04-S10 (10 scenes — Efficiency)
│   │   └── part05/                ← P05-S01..P05-S09 (9 scenes — Physical AI; legacy/ subdir is old)
│   └── render/                    ← per-part PowerShell render scripts
│
├── drivex_white/                  ← REFERENCE SNAPSHOT — do not edit
│
├── materials/                     ← source of truth for content
│   ├── slides/                    ← original .pdf / .pptx — Part 1..5
│   ├── scripts/                   ← Vietnamese narration drafts per part
│   ├── images/                    ← extracted slide images per part
│   ├── chat_plan.md               ← initial brainstorm (slide-by-slide summary)
│   └── drivex_tutorial.md         ← extended notes
│
├── spec_prompts/                  ← scene production specs (older format) + 3 review rounds
│   ├── spec_intro_part01.md
│   ├── spec_part02.md … spec_part05.md
│   ├── spec_review_first.md       ← 1st pass review
│   ├── spec_review_twice.md       ← 2nd pass review
│   └── spec_review_third.md       ← 3rd pass review
│
├── plans/                         ← NEW rework plans (this session) — execute these
│   └── *.md
│
├── media/                         ← Manim render output (auto-generated)
└── merge_videos.{ps1,py}          ← post-render concatenation
```

---

## Tech stack

| Layer | Tool |
|---|---|
| Animation engine | `manim` (Community v0.20.1) |
| Voiceover (later) | `manim-voiceover` (needs the `pkg_resources` patch — see README) |
| Math rendering | LaTeX (MiKTeX/TeX Live) + Latin Modern Roman font |
| Python env | Base conda (`C:\Users\admin\miniconda3\Scripts\manim.exe`) — NOT `manim_env` |
| Quality flags | `-ql` (480p15 preview) · `-qh` (1080p60 final) · `-qk` (4K) |
| Platform | Windows 11, PowerShell shell |

> **Critical env note:** Manim is in the *base* conda env. Running `conda activate manim` will fail. Just call `manim` directly.

---

## Rendering quick reference

```powershell
# Single scene (testing)
manim -ql drivex\scenes\part01\p01_s01_opening.py P01S01Opening

# Whole part
.\drivex\render\render_part01.ps1 -ql

# Final 1080p pass
.\drivex\render\render_all_final.ps1
```

Output lands at `media/videos/<scene_file>/480p15/<ClassName>.mp4` (or `1080p60/`).

---

## Design constraints (from user, 2026-05-10)

These are *durable preferences* — not just for one scene. Apply across the project.

### Background & color
- **White background everywhere** (`BG_DARK = "#FFFFFF"`). The previous dark theme is rejected.
- The "xanh đen" (deep navy) accent is *only* welcome on **Part transition cards** (between parts). Body scenes stay white.
- Text is dark navy `#334155` / `COL_NAVY`; never pure black.

### Mascots
- Two mascots: **PI** (curious questioner, asks "why?") and **CAR** (guide, answers / drives the narrative). Both must appear consistently.
- The user has art at [materials/images/DriveX_MasCot.jpg](materials/images/DriveX_MasCot.jpg) and [materials/images/mascot_drivex.png](materials/images/mascot_drivex.png) — feel free to reference, but the geometric fallback in `mascots.py` is acceptable for now ("code chỉ cần add đại 1 dummy image là được").

### Speech / thought bubbles
- **Tight fit to text** — width = text_width + small horizontal pad. Do NOT pad to 4 sides equally.
- Slim border (1.5–2pt), small corner radius. Not the chunky dark-fill style currently in `thought_bubble.py`.
- **Never overlap** other content. If a bubble would collide with the next animation step, fade it out first.
- All on-screen text in **English**.

### Layout discipline (failure modes from prior reviews)
- Text labels next to nodes / arrows must not crowd the geometry. If a label "feels close," fade it out before the next reveal — don't try to solve overlap by moving by 0.1u.
- Boxes / pipeline blocks must align on a shared baseline — both visually and via Manim's `align_to` / `arrange`. Don't eyeball offsets.
- Distributions / charts: **draw axes first, then data**. Several P01/P02 scenes have the inverse and look wrong.
- Roadmap strip (5-node mini at bottom of part title cards): zigzag labels (alternating up/down) must not collide with content above them. If they do, kill the labels — keep just the dots.
- Endings of scenes must `FadeOut` everything that won't carry into the next scene. A common bug across the draft: orphaned text reappears at the end (P01-S06, P01-S08, P02-S03).

### Narrative
- Match content to original scripts in `materials/scripts/` and slides in `materials/slides/`. The drafts simplified some papers down to bare names — re-check the script and reintroduce the *reason* each paper is mentioned (the user's note: "có lẽ bạn nên check lại vì presenter gốc nêu nó ra ắc hẳn phải có lý do").
- Tone: explanatory like 3B1B. Not a slide bullet list.

---

## Workflow for any rework task

1. Read `plans/00_MASTER_PLAN.md` for the phase you're in.
2. Read the relevant per-part plan (`plans/04_*.md` … `plans/08_*.md`).
3. Cross-check `plans/09_FIX_CHECKLIST.md` for known issues on that scene.
4. Edit the scene file in `drivex/scenes/<part>/<scene>.py`.
5. Render at `-ql` to verify; iterate.
6. When the scene visibly meets the spec, mark it done in the plan file.

---

## What NOT to do

- Don't edit `drivex_white/` — it's a reference snapshot.
- Don't add a new color hex — import from [drivex/components/colors.py](drivex/components/colors.py) and add it there if missing.
- Don't write multi-paragraph docstrings in scene files. The original draft uses Unicode box-drawing comments that got mangled to `â”€` characters — strip them when you touch a file. One-line section comments are fine.
- Don't introduce dark-theme assumptions (e.g., light-colored text on dark fill) — they look wrong on the new white BG.
- Don't keep "let everything fade back in at the end" patterns. Every scene must end clean.
