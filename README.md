# Beyond Self-Driving — ICCV 2025 Tutorial

Manim-based animated video series for the **ICCV 2025 "Beyond Self-Driving"** tutorial, covering Foundation Models, Cooperative Automation, and Real-World Sensor Integration for autonomous driving.

---

## 📋 Prerequisites

### 1. Conda (Miniforge)

```bash
brew install miniforge
```

### 2. Python Environment

```bash
conda create -n manim python=3.10
conda activate manim
pip install -r requirements.txt
```

> **Note:** `manim-voiceover` requires a manual patch to work with Conda.
> In `~/miniforge3/envs/manim/lib/python3.10/site-packages/manim_voiceover/__init__.py`,
> replace `pkg_resources` with `importlib.metadata`.

### 3. LaTeX (MacTeX) — Required for math rendering

Install MacTeX for `pdflatex` support:

```bash
brew install --cask mactex-no-gui
```

After installation, add to your shell profile (`~/.zshrc`):

```bash
export PATH="/Library/TeX/texbin:$PATH"
```

Then reload:

```bash
source ~/.zshrc
```

### 4. Latin Modern Roman font — Required for proper text rendering

The project uses **Latin Modern Roman** (included with MacTeX).
After installing MacTeX, copy the fonts to the system font directory:

```bash
# Copy Latin Modern fonts for Pango/Manim to detect
find /usr/local/texlive -name "lmroman*.otf" 2>/dev/null | head -5 | xargs -I{} cp {} ~/Library/Fonts/
fc-cache -fv
```

Verify the font is detected:

```bash
fc-list | grep "Latin Modern Roman"
```

---

## 📁 Project Structure

```
Beyond_SelfDriving/
├── drivex_video/
│   ├── scenes/
│   │   ├── part1/          # Foundation Models for AV (17 scenes)
│   │   ├── part2/          # Cooperative Automation (9 scenes)
│   │   └── part3/          # Real-World Sensor Integration (10 scenes)
│   └── styles/
│       ├── theme.py        # Global color palette & font config
│       └── mascot_fx.py    # ThoughtBubble animation component
├── materials/
│   └── images/             # Slide assets (part1/, part2/, etc.)
├── render_part1.sh         # Render all Part 1 scenes
├── render_part2.sh         # Render all Part 2 scenes
├── render_part3.sh         # Render all Part 3 scenes
└── requirements.txt
```

---

## 🎬 Rendering

Each render script accepts a quality flag: `-ql` (preview, 480p) or `-qh` (final, 1080p).

```bash
conda activate manim

# Preview quality
bash render_part1.sh -ql
bash render_part2.sh -ql

# High quality (for final export)
bash render_part1.sh -qh
bash render_part2.sh -qh
```

Output videos are saved to:
```
media/videos/<scene_file>/1080p60/<SceneName>.mp4
```

### Render a single scene

```bash
conda activate manim
manim -qh drivex_video/scenes/part1/04_challenges.py CornerCases
```

---

## 🎨 Design System

- **Font:** Latin Modern Roman (LaTeX standard serif font)
- **Background:** `#1C1C1C` (deep dark gray)
- **Accent colors:** UCLA Blue `#2774AE`, UCLA Gold `#FFD100`, Sky Blue `#58C4DD`
- **Style config:** `drivex_video/styles/theme.py`

---

## 📦 Part 3 Setup

Part 3 scenes require slide images extracted from `Part 3.pdf`:

1. Place `Part 3.pdf` at `materials/slides/Part 3.pdf`
2. Run:
```bash
conda activate manim
pip install pymupdf
python extract_part3_slides.py
```
3. Then render: `bash render_part3.sh -qh`

---

## 🛠 Troubleshooting

| Problem | Fix |
|---|---|
| `pdflatex not found` | Add `/Library/TeX/texbin` to PATH |
| Latin Modern Roman not detected | Run `fc-cache -fv` then restart terminal |
| `ModuleNotFoundError: pkg_resources` | Patch `manim_voiceover/__init__.py` (see setup step 2) |
| Broken letter spacing in Text() | Increase `font_size` to ≥ 22 for Latin Modern Roman |
