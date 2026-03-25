# Beyond Self-Driving — ICCV 2025 Tutorial

Manim-based animated video series for the **ICCV 2025 "Beyond Self-Driving"** tutorial, covering Foundation Models, Cooperative Automation, and Real-World Sensor Integration for autonomous driving.

---

## 📋 Prerequisites

### 1. Conda (Miniforge)

| OS | Command |
|---|---|
| **macOS** | `brew install miniforge` |
| **Linux** | `wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh && bash Miniforge3-Linux-x86_64.sh` |
| **Windows** | Download [Miniforge3 installer](https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe) and run it |

### 2. Python Environment

```bash
conda create -n manim python=3.10
conda activate manim
pip install -r requirements.txt
```

> **Note:** `manim-voiceover` requires a manual patch to work with Conda.
> In `<conda_envs>/manim/lib/python3.10/site-packages/manim_voiceover/__init__.py`,
> replace `import pkg_resources` with `import importlib.metadata as pkg_resources`.

---

### 3. LaTeX — Required for math rendering

#### macOS

```bash
brew install --cask mactex-no-gui
```

Add to `~/.zshrc`:
```bash
export PATH="/Library/TeX/texbin:$PATH"
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt install texlive-full
```

#### Windows

Download and install [MiKTeX](https://miktex.org/download) or [TeX Live](https://tug.org/texlive/windows.html).

---

### 4. Latin Modern Roman font — Required for proper text rendering

Latin Modern Roman is included with any full TeX installation. After installing LaTeX, register the fonts with your system:

#### macOS

```bash
# Copy fonts so Pango/Manim can detect them
find /usr/local/texlive -name "lmroman*.otf" 2>/dev/null | xargs -I{} cp {} ~/Library/Fonts/
fc-cache -fv
```

#### Linux

```bash
sudo apt install fonts-lmodern   # or: texlive-fonts-recommended
fc-cache -fv
```

#### Windows

Fonts are installed automatically with MiKTeX/TeX Live.  
If needed, copy `.otf` files from `C:\texlive\...\fonts\opentype\` to `C:\Windows\Fonts\`.

Verify detection on macOS/Linux:

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
├── render_part1.sh         # Render all Part 1 scenes (macOS/Linux)
├── render_part2.sh         # Render all Part 2 scenes (macOS/Linux)
├── render_part3.sh         # Render all Part 3 scenes (macOS/Linux)
└── requirements.txt
```

---

## 🎬 Rendering

Each render script accepts a quality flag: `-ql` (preview, 480p) or `-qh` (final, 1080p).

```bash
conda activate manim

# Preview quality
bash render_part1.sh -ql

# High quality (for final export)
bash render_part1.sh -qh
bash render_part2.sh -qh
```

**Windows** — run each scene manually:
```bash
manim -qh drivex_video/scenes/part1/01_intro.py TitleScene
```

Output: `media/videos/<scene_file>/1080p60/<SceneName>.mp4`

---

## 🎨 Design System

- **Font:** Latin Modern Roman (LaTeX standard serif)
- **Background:** `#1C1C1C`
- **Colors:** UCLA Blue `#2774AE` · UCLA Gold `#FFD100` · Sky Blue `#58C4DD`
- **Config:** `drivex_video/styles/theme.py`

---

## 📦 Part 3 Setup

Part 3 scenes require slide images extracted from `Part 3.pdf`:

```bash
# Place PDF at materials/slides/Part 3.pdf, then:
pip install pymupdf
python extract_part3_slides.py
bash render_part3.sh -qh
```

---

## 🛠 Troubleshooting

| Problem | Fix |
|---|---|
| `pdflatex not found` | Add TeX bin dir to PATH (see step 3) |
| `Latin Modern Roman` not detected | Run `fc-cache -fv`, restart terminal |
| `ModuleNotFoundError: pkg_resources` | Patch `manim_voiceover/__init__.py` (see step 2) |
| Broken letter spacing in small text | Increase `font_size` to ≥ 22 for Latin Modern Roman |
