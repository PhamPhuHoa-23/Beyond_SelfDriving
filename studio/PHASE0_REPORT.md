# PHASE 0 REPORT — Discovery & Verification
Generated: 2026-05-22 · Updated after full fix pass

---

## 1. FONT STATUS

| Font | Status | Notes |
|------|--------|-------|
| CMU Serif | **INSTALLED** ✓ | Per-user install, HKCU registry |
| CMU Typewriter Text | **INSTALLED** ✓ | Same package |
| CMU Bright, Concrete, Sans Serif | **INSTALLED** ✓ | 17 CMU families total |
| Latin Modern Roman | Not installed | Not needed — CMU Serif available |

**Install method used:** Downloaded cm-unicode.zip from CTAN (34 OTF files), copied to
`%LOCALAPPDATA%\Microsoft\Windows\Fonts\`, registered all 33 in
`HKCU:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts`.

**Verification:**
```python
import manimpango
[f for f in manimpango.list_fonts() if 'CMU' in f]
# → ['CMU Bright', 'CMU Serif', 'CMU Typewriter Text', ...]  17 families
```

**Font render tests:**
- `manimce -ql`: Phase0FontTest with CMU Serif → **SUCCESS** ✓
- `manimgl -w -l`: ManimGLFontTest with CMU Serif → **SUCCESS** ✓ (~100 fps)

---

## 2. MANIM ENVIRONMENT

| Component | Version | Command | Notes |
|-----------|---------|---------|-------|
| Manim Community | v0.20.1 | `manimce` | Cairo renderer, `from manim import *` |
| ManimGL | v1.7.2 | `manimgl` | OpenGL renderer, `from manimlib import *` |
| manimlib (old) | v0.2.0 | (library only) | Installed as dep; not used directly |

**IMPORTANT:** Installing manimgl overwrote the bare `manim` CLI command.
- `manim` → now manimgl v1.7.2
- `manimce` → Manim Community v0.20.1
- `manimgl` → ManimGL v1.7.2

**All render scripts updated:** `bins/render_all.ps1`, `bins/render_part3.ps1`,
`bins/render_part3_v2.ps1`, `render_all_missing.ps1` — `manim` replaced with `manimce`.

**ffmpeg:** Found at `C:\Users\admin\miniconda3\Library\bin\ffmpeg.exe`.
Added to user PATH permanently via HKCU registry. Required by manimgl for file output.

**Render speed comparison (480p15):**
| Renderer | Scene | Time |
|----------|-------|------|
| manimce | 5-item font test | ~8s |
| manimce | ThreeDScene sphere | ~15s |
| manimgl | 3-anim basic scene | ~3s |
| manimgl | 4-anim font test | ~1.5s |

**MiKTeX / LaTeX:** Active, renders MathTex via dvisvgm. Minor warning about updates
(non-fatal; run `miktex-update` when convenient).

---

## 3. REFERENCE FILES

All 6 files confirmed present and readable:

| File | Lines | Import |
|------|-------|--------|
| `3b1b_videos/custom/logo.py` | 258 | `from manimlib.constants import *` (older style) |
| `3b1b_videos/_2024/transformers/network_flow.py` | 788 | `from manim_imports_ext import *` |
| `3b1b_videos/_2026/hairy_ball/model3d.py` | 354 | `from manim_imports_ext import *` |
| `welchlabs_videos/once_useful_constructs/light.py` | 364 | `from manimlib import *` |
| `welchlabs_videos/_2026/vla/p31_61_1.py` | 1473 | `from manimlib import *` |
| `welchlabs_videos/_2025/generalization/p8_15.py` | 451 | `from manimlib import *` |

`from manimlib import *` now resolves to **manimgl v1.7.2** (installed).
Key classes confirmed available: `InteractiveScene`, `Tex`, `TexText`, `VGroup.f_always`.

**Remaining adaptation gap:** The 3b1b files use `from manim_imports_ext import *` which
is a repo-local file that wraps manimgl + custom helpers. This file is at
`Source_manim_reference/3b1b_videos/manim_imports_ext.py` and requires the 3b1b repo
structure. When adapting patterns from these files, import from `manimlib` directly.

---

## 4. SLIDES & SCRIPTS

### Slides
| File | Status |
|------|--------|
| `materials/slides/Part 1.pdf` | ✓ |
| `materials/slides/Part 2.pptx` | **PPTX only** — no PDF. Convert if needed: `python -m pptx` or LibreOffice |
| `materials/slides/Part 3.pdf` | ✓ |
| `materials/slides/Part 4.pdf` | ✓ |
| `materials/slides/Part 5.pdf` | ✓ |

### Scripts
All 5 confirmed: `script_part1.md` … `script_part5.md` ✓

---

## 5. 3D / OPENGL RENDER CHECK

### manimce `--renderer=opengl`
Renders without crash but **does not write MP4 file** in headless mode.
Do NOT use this flag in render scripts.

### manimce default (cairo) ThreeDScene
Works correctly. Output: `media/.../480p15/*.mp4` ✓
Use `ThreeDScene` with default renderer for any 3D in manimce builds.

### manimgl native OpenGL
Renders correctly once ffmpeg is in PATH.
Output goes to `videos/*.mp4` (different default path from manimce).
`-w` flag required for file output (without it, opens interactive window).
Render speed is significantly faster (~5–10× for simple scenes).

---

## 6. STUDIO BUILD DECISION

Based on "sài manimlib luôn" — **studio/ will be built on manimgl**.

| Aspect | Decision |
|--------|----------|
| Python import | `from manimlib import *` |
| CLI render | `manimgl -w -ql` (low) · `manimgl -w` (1080p) |
| Base class | `Scene` from manimlib (not manim CE `Scene`) |
| Text | `Text(s, font="CMU Serif")` — same API as manimce |
| Math | `Tex(r"...")` (not `MathTex`) |
| Camera | `self.frame` instead of `self.camera.frame` |
| Output dir | `videos/` (default) — configure via `--video_dir` |
| Reference files | Can use welchlabs patterns more directly |

**Font config for manimgl scenes:** CMU Serif confirmed working.

---

## 7. FIXES APPLIED THIS SESSION

| Item | Action | Result |
|------|--------|--------|
| CMU Serif fonts | Downloaded cm-unicode, installed per-user | 17 CMU families in Pango ✓ |
| manimgl | `pip install manimgl` | v1.7.2, `from manimlib import *` works ✓ |
| ffmpeg PATH | Added `miniconda3\Library\bin` to HKCU PATH | manimgl file output works ✓ |
| Render scripts | `manim` → `manimce` in 4 PS1 files | drivex/beyond renders unaffected ✓ |

---

## PHASE 1: DONE ✓

## READY FOR PHASE 1: YES (COMPLETED)

All blockers resolved:
- CMU Serif available in Pango ✓
- manimgl installed and rendering to file ✓
- ffmpeg in PATH ✓
- render scripts updated ✓

**Note:** New terminal sessions will pick up the updated PATH for ffmpeg automatically.
Current session: prepend `C:\Users\admin\miniconda3\Library\bin` manually if needed,
or open a new terminal.
