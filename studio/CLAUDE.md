# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Session orientation

`studio/` is the ManimGL animation package for the *Beyond Self-Driving* tutorial video.
Read this file first, then `studio/REWORK_PROMPTS.md` for the staged repair plan (5 phases:
quote fixes → image placeholders → layout → visual polish → final render).

## Working directory & env

```powershell
# From repo root — always set before rendering
$env:PYTHONPATH = "C:\Users\admin\Downloads\ML\Lab01_3B1B"
$env:PATH = "C:\Users\admin\miniconda3\Scripts;C:\Users\admin\miniconda3\Library\bin;" + $env:PATH
```

The PowerShell render script sets these automatically. All `manimgl` calls use the full path
`C:\Users\admin\miniconda3\Scripts\manimgl.exe` internally.

## Render commands

Default for user-requested renders: use HD (`--hd`), not low-quality preview (`-l`), unless the user explicitly asks for preview/low quality.

Single scene (HD by default):

```powershell
manimgl -w --hd studio/scenes/intro/i01_title_card.py I01TitleCard
```

`-w` is **required**. Without it ManimGL opens an interactive window instead of writing a file.

| Flag | Output |
|---|---|
| `-l` | 480p15 preview |
| `-m` | 720p30 |
| `--hd` | 1080p60 |
| `--uhd` | 4K |

Output lands at: `videos/<ClassName>.mp4`

Batch render all scenes:

```powershell
.\render_studio_all.ps1
```

### macOS (this machine)

**After finishing any scene change, always produce a final HD render (`--hd`) of every scene you
touched** — preview (`-l`) is only for fast iteration while working. When the edit is done and
verified, re-render that scene at `--hd` so the committed output is HD. Do this automatically;
don't wait to be asked.

`manimgl` lives in the `manim` conda env (there is **no** `manimgl` on the base PATH; the bare
`manim` resolves to Manim CE — do not use it). Render a single scene from the repo root:

```bash
cd "/Users/phu-quynguyen-lam/o D/Beyond_SelfDriving"
# fast preview while iterating
PYTHONPATH="$PWD" /Users/phu-quynguyen-lam/miniforge3/envs/manim/bin/manimgl \
  -w -l studio/scenes/part01/p01_s03b_e2e.py P01S03BE2E
# final HD render once the change is done (REQUIRED before considering the task finished)
PYTHONPATH="$PWD" /Users/phu-quynguyen-lam/miniforge3/envs/manim/bin/manimgl \
  -w --hd studio/scenes/part01/p01_s03b_e2e.py P01S03BE2E
```

`PYTHONPATH="$PWD"` replaces the Windows `Lab01_3B1B` path so `from studio.components import …`
resolves. `-w` is still required. Output: `videos/<ClassName>.mp4`.

Extract a specific frame for review (ffmpeg/ffprobe are at `/opt/homebrew/bin`, not in the env):

```bash
# inspect duration, then grab the frame at timestamp t (seconds)
ffprobe -v error -show_entries format=duration -of csv=p=0 videos/P01S03BE2E.mp4
ffmpeg -y -loglevel error -ss 8.8 -i videos/P01S03BE2E.mp4 -frames:v 1 videos/check.png
```

## Runtime

All studio scenes use **ManimGL v1.7.2**. The bare `manim` command may point to Manim CE —
always call `manimgl` explicitly.

```python
from manimlib import *   # NOT from manim import *
```

Key API differences from Manim CE:

| Manim CE | ManimGL |
|---|---|
| `Create(mob)` | `ShowCreation(mob)` |
| `MathTex(r"...")` | `Tex(r"...")` |
| `self.camera.frame` | `self.frame` |
| `--renderer=opengl` flag | not needed |
| `media/videos/` output | `videos/` output |

## Scene pattern

```python
from manimlib import *
from studio.components import StudioScene  # or Studio3DScene


class MyScene(StudioScene):
    PART_NUM = 2          # sets self.PART_COLOR and self.PART_PASTEL via PART_PALETTES
    SCENE_TITLE = "..."

    def construct(self):
        header = self._open()   # title bar + separator; returns VGroup
        # ... build content ...
        self._close()           # FadeOut all live mobjects
```

- `_open(title=None)` — uses `self.SCENE_TITLE` if no argument.
- `_close(*extra, fade_lag=0.04)` — FadeOut everything on screen plus any extras passed in.
  Every scene must end with `_close()` so the final frame is blank (BG_PAPER cream).
- `_roadmap_strip()` — 5-dot strip (active dot = part color). Call in part title cards.

**3D scenes** use `Studio3DScene`. Default camera: `self.frame.reorient(-30, 70)`.
Depth testing: `mob.apply_depth_test()` for background; `mob.deactivate_depth_test()` then
`self.remove(mob); self.add(mob)` for foreground. Skip i02 and p02_s05 during layout phases —
their 3D geometry should only be touched for explicit bug fixes.

Per-part accent / pastel from `PART_PALETTES`:

| Part | Accent | Pastel |
|---|---|---|
| 0 (intro) | ACCENT_BLUE | PASTEL_BLUE |
| 1 | ACCENT_BLUE | PASTEL_BLUE |
| 2 | ACCENT_TEAL | PASTEL_TEAL |
| 3 | ACCENT_GREEN | PASTEL_GREEN |
| 4 | ACCENT_AMBER | PASTEL_AMBER |
| 5 | ACCENT_PINK | PASTEL_PINK |

## Component map

```text
studio/components/
  colors.py       — BG_PAPER, ACCENT_*, INK_*, PASTEL_*, GOLD_RICH, RED_ERROR, …
  typography.py   — FONT_PRIMARY (CMU Serif), SIZE_*, text/bold_text/italic_text/math helpers
  layout.py       — zone constants + arrangers (see below)
  base_scene.py   — StudioScene, Studio3DScene
  agents.py       — vehicle_icon, pedestrian_icon, rsu_icon, drone_icon, agent_trail
  signals.py      — radar_shells_2d/3d, sensor_cone, v2x_link, ambient_glow
  annotations.py  — callout, error_callout, thought_bubble, contribution_badge, key_number
  pipeline.py     — pipeline_block, pipeline_row, stage_panel, pipeline_arrow
  animations.py   — forge_text, particle_assemble, write_chiseled, dust_dissolve, scan_reveal
  model_viz.py    — EmbeddingArray, WeightMatrix, attention animation
  charts.py       — axes_deploy, bar_reveal, curve_trace, scatter_rain
  assets.py       — img_or_placeholder (soft-fail image helper)
  __init__.py     — re-exports all of the above
```

Never hardcode hex colors in scene files — import from `colors.py`. Typography helpers default
to `INK_DARK` and `FONT_PRIMARY`; call them instead of constructing raw `Text()`.

## Layout zone constants (layout.py)

```
TITLE_Y     = 3.2    # scene title bar center
SEP_Y       = 2.85   # separator line
CONTENT_TOP = 2.7    # top of usable content area
CONTENT_BOT = -3.2   # bottom of usable content area
FOOTER_Y    = -3.5   # footer zone
LEFT_X      = -4.0   # left column center
RIGHT_X     = 4.0    # right column center
MAX_TEXT_X  = 6.5    # canvas right edge (safe)
```

Canvas: 14.22 × 8.00 Manim units. Safe zone: x ∈ [-6.5, 6.5], y ∈ [-3.8, 3.8].

Prefer zone helpers over raw `move_to()`:
`place_title`, `place_left`, `place_right`, `place_footer`,
`two_column`, `three_column`, `content_row`, `content_column`, `grid_4`

Charts: **always animate axes before data**. Use `axes_deploy()` from `charts.py` which returns
`(axes, AnimationGroup)` — play the animation before adding bars, curves, or dots.

## Image placeholder pattern

```python
from studio.components import img_or_placeholder

card = img_or_placeholder(
    "studio/assets/images/p01_s07a/bevdriver_arch.png",
    label="BEVDriver architecture",
    width=3.2,
)
```

Returns `ImageMobject` if the file exists, otherwise a labeled placeholder rectangle (no crash).
Asset path convention: `studio/assets/images/<scene_id>/<image_name>.png`

## Known quirks

### White text (invisible on BG_PAPER)

ManimGL on this system can ignore `color=` on `Text()` in edge cases, producing white-on-white
characters. `StudioScene` and `Studio3DScene` override `add()` / `play()` with
`_force_text_contrast()` automatically. If you build a `VGroup` outside `self.play()` / `self.add()`
and add it later, call `self._force_text_contrast(mob)` manually first.

### Curly quotes in Text()

Unicode curly quotes `"` (U+201C) / `"` (U+201D) inside `Text()` literals may be dropped
silently by ManimGL's Pango layer on Windows.

```powershell
# Detect
rg -n "[\x{201C}\x{201D}]" studio/scenes --glob "*.py"
```

Fix — use ASCII quotes or explicit escapes:

```python
# ASCII (preferred when typographic distinction isn't needed)
Text('"The world is compositional."')

# Explicit escape (when open/close distinction matters)
Text('“The world is compositional.”')
```

Known affected files: `p05_s04a_compositional_quote.py` (lines 19–20), `p02_s01_title.py` (line 54).
