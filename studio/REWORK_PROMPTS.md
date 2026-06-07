# Studio Rework Prompts — Beyond Self-Driving

Audience: a fresh Claude Code session working on `studio/`.

Read `studio/CLAUDE.md` first. It has render commands, ManimGL quirks, component
APIs, and layout zone constants.

Run all commands from `C:\Users\admin\Downloads\ML\Lab01_3B1B` with PYTHONPATH set:

```powershell
$env:PYTHONPATH = "C:\Users\admin\Downloads\ML\Lab01_3B1B"
$env:PATH = "C:\Users\admin\miniconda3\Scripts;C:\Users\admin\miniconda3\Library\bin;" + $env:PATH
```

## Phase overview

| Phase | Work | Priority |
|---|---|---|
| 0 | Audit: render representative scenes and identify visible failures | First |
| 1 | Quote fix: replace Unicode curly quotes in Text() string literals | Critical |
| 2 | Image placeholders: add `img_or_placeholder()` to paper and dataset scenes | High |
| 3 | Layout fixes: 2D scenes only — anchor positioning, FadeOut audit | Medium |
| 4 | Enhancements: thought bubbles, visual hierarchy, bridge wipes | Polish |
| 5 | Final render and merge | Final |

---

## Phase 0 — Audit (read-only)

Goal: render one scene from each part at low quality and identify visible failures.
Do not edit any file in this phase.

```powershell
# Smoke test: components
manimgl -w -l studio/scenes/_smoke_components.py SmokeComponents

# One scene per part
manimgl -w -l studio/scenes/intro/i01_title_card.py I01TitleCard
manimgl -w -l studio/scenes/part01/p01_s02a_genai_timeline.py P01S02AGenAITimeline
manimgl -w -l studio/scenes/part02/p02_s01_title.py P02S01Title
manimgl -w -l studio/scenes/part03/p03_s03_smart_intersection.py P03S03SmartIntersection
manimgl -w -l studio/scenes/part04/p04_s03_annotation_cost.py P04S03AnnotationCost
manimgl -w -l studio/scenes/part05/p05_s04a_compositional_quote.py P05S04ACompositionalQuote
```

For 3D scenes (these use Studio3DScene — no extra flag needed):

```powershell
manimgl -w -l studio/scenes/intro/i02_the_hook.py I02TheHook
manimgl -w -l studio/scenes/part02/p02_s05_radar_waves.py P02S05RadarWaves
```

**Do not touch i02_the_hook.py or p02_s05_radar_waves.py in any layout phase.**
Their 3D geometry is complex and should only be adjusted if a specific bug is reported.

Look for:
- Curly-quote characters (`"` / `"`) rendering as boxes or missing glyphs.
- Text rendered as white-on-white (invisible on BG_PAPER cream background).
- Content outside safe zone: x outside [-6.5, 6.5] or y outside [-3.8, 3.8].
- Data points or bars appearing before their axes.
- Text labels overlapping geometry or each other.
- Scene ending without FadeOut (content visible in last frame).

---

## Phase 1 — Quote fixes

**Problem:** Several scenes contain Unicode curly double-quote characters (U+201C `"`,
U+201D `"`) directly inside `Text()` string literals. ManimGL's Pango layer on Windows
can drop these silently, producing a missing glyph or a blank space where the quote mark
should be.

**Detection:**

```powershell
rg -n "[\x{201C}\x{201D}]" studio/scenes --glob "*.py"
```

**Fix pattern:**

```python
# Before — Pango may drop U+201C / U+201D silently
Text('"The world is compositional,', ...)
Text('or there is a god."', ...)

# After — use standard ASCII double quotes
Text('"The world is compositional,', ...)
Text('or there is a god."', ...)
```

If typographic open/close distinction is important to the scene, use explicit escapes:

```python
Text('\u201CThe world is compositional,', ...)   # U+201C open
Text('or there is a god.\u201D', ...)             # U+201D close
```

### 1-A  `studio/scenes/part05/p05_s04a_compositional_quote.py`

Lines 19–20: both `quote1` and `quote2` open/close with curly quotes.

```python
# Fix line 19
quote1 = Text('"The world is compositional,', font=FONT_PRIMARY, ...)

# Fix line 20
quote2 = Text('or there is a god."', font=FONT_PRIMARY, ...)
```

Render after fix:

```powershell
manimgl -w -l studio/scenes/part05/p05_s04a_compositional_quote.py P05S04ACompositionalQuote
```

Verify: opening `"` and closing `"` are clearly visible on the cream background as
distinct characters, not boxes or spaces.

### 1-B  `studio/scenes/part02/p02_s01_title.py`

Line 54: the quote text starts and ends with curly quotes.

```python
# Fix line 54
quote = Text('"A single agent, no matter how smart, is limited by its own line of sight."',
             font=FONT_PRIMARY, ...)
```

Render:

```powershell
manimgl -w -l studio/scenes/part02/p02_s01_title.py P02S01Title
```

### 1-C  Search and fix remaining scenes

After fixing 1-A and 1-B, run a broad scan and fix every `Text("...)` or `Text('...')` that
contains curly-quote bytes:

```powershell
rg -ln "[\x{201C}\x{201D}]" studio/scenes --glob "*.py"
```

For each file: open it, replace every occurrence of `"` with `"` and `"` with `"` inside
`Text()` string literals. Do not change occurrences that appear in Python comments or
in `SCRIPT = """..."""` blocks (those are never rendered).

---

## Phase 2 — Image placeholders

Goal: add image slots to scenes that reference real papers, datasets, or physical
systems. The placeholder renders as a labeled rectangle when the asset file is absent,
so the user can see exactly where to drop a real PNG later.

Add this helper near the top of each scene file that needs it (after imports):

```python
from pathlib import Path


def img_or_placeholder(path: str, width: float = 3.5, label: str = "") -> VGroup:
    """ImageMobject if asset exists, otherwise a labeled placeholder box."""
    if Path(path).exists():
        img = ImageMobject(path)
        img.scale_to_fit_width(width)
        return img
    box = RoundedRectangle(
        corner_radius=0.1,
        width=width,
        height=width * 0.625,
        fill_color=BG_CARD,
        fill_opacity=1.0,
        stroke_color=INK_LIGHT,
        stroke_width=1.5,
    )
    lbl = Text(
        label or Path(path).name,
        font=FONT_PRIMARY,
        font_size=SIZE_MICRO,
        color=INK_LIGHT,
    )
    lbl.move_to(box)
    return VGroup(box, lbl)
```

Asset path convention: `studio/assets/images/<scene_id>/<image_name>.png`

Placement rules:
- Use `next_to()` or `to_corner()` relative to existing mobs — never absolute `move_to`.
- Keep inside safe zone: x ∈ [-6.5, 6.5], y ∈ [-3.8, 3.8].
- Fade out before the next major layout beat or let `_close()` handle it.
- Scale one side with `scale_to_fit_width(W)` for real images.

### 2-A  VLA paper scenes — architecture thumbnails

Files:
- `studio/scenes/part01/p01_s07a_bevdriver.py` (class `P01S07ABEVDriver`)
- `studio/scenes/part01/p01_s07b_emma.py` (class `P01S07BEMMA`)
- `studio/scenes/part01/p01_s07c_drivevlm.py` (class `P01S07CDriveVLM`)
- `studio/scenes/part01/p01_s08a_autovla_switch.py` (class `P01S08AAutoVLASwitch`)

Each scene focuses on one VLA paper. After the main pipeline diagram is revealed,
add a paper thumbnail in the upper-right region:

```python
thumb = img_or_placeholder(
    "studio/assets/images/p01_s07a/bevdriver_arch.png",
    width=3.2,
    label="BEVDriver architecture",
)
thumb.to_corner(UR, buff=0.5)
self.play(FadeIn(thumb, run_time=0.35))
```

Asset names per scene:
| Scene | Asset path |
|---|---|
| `p01_s07a` | `studio/assets/images/p01_s07a/bevdriver_arch.png` |
| `p01_s07b` | `studio/assets/images/p01_s07b/emma_arch.png` |
| `p01_s07c` | `studio/assets/images/p01_s07c/drivevlm_arch.png` |
| `p01_s08a` | `studio/assets/images/p01_s08a/autovla_system.png` |

### 2-B  V2X dataset — real intersection photo

File: `studio/scenes/part02/p02_s10_v2xpnp_dataset.py`

After the dataset stats cards appear, add a real-scene photo beside the bar chart:

```python
scene_img = img_or_placeholder(
    "studio/assets/images/p02_s10/v2xpnp_scene.png",
    width=3.4,
    label="V2X-PnP intersection photo",
)
scene_img.next_to(bar_chart, RIGHT, buff=0.5)
self.play(FadeIn(scene_img, run_time=0.35))
```

### 2-C  Smart Intersection — testbed photo

File: `studio/scenes/part03/p03_s03_smart_intersection.py`

After RSU icons are revealed, add a real UCLA Smart Intersection photo in the top-right:

```python
testbed_img = img_or_placeholder(
    "studio/assets/images/p03_s03/ucla_intersection.png",
    width=3.6,
    label="UCLA Smart Intersection (real)",
)
testbed_img.to_corner(UR, buff=0.5)
self.play(FadeIn(testbed_img, run_time=0.40))
self.wait(1.5)
self.play(FadeOut(testbed_img, run_time=0.25))
```

### 2-D  CooperFuse — method diagram

File: `studio/scenes/part03/p03_s08_cooperfuse.py`

After the architecture pipeline is shown, add a results comparison image:

```python
result_img = img_or_placeholder(
    "studio/assets/images/p03_s08/cooperfuse_comparison.png",
    width=4.0,
    label="CooperFuse detection improvement",
)
result_img.to_edge(DOWN, buff=0.5)
self.play(FadeIn(result_img, run_time=0.35))
```

### 2-E  MetaUrban — generated environment

File: `studio/scenes/part05/p05_s04b_metaurban.py`

After the procedural generation demo, show a rendered MetaUrban environment:

```python
env_img = img_or_placeholder(
    "studio/assets/images/p05_s04b/metaurban_env.png",
    width=4.2,
    label="MetaUrban generated scene",
)
env_img.move_to(RIGHT * 3.0 + DOWN * 0.3)
self.play(FadeIn(env_img, run_time=0.4))
self.wait(2.0)
self.play(FadeOut(env_img, run_time=0.3))
```

### 2-F  CityWalker — trajectory visualization

File: `studio/scenes/part05/p05_s06a_citywalker.py`

After the dataset stats, add a CityWalker trajectory map:

```python
traj_img = img_or_placeholder(
    "studio/assets/images/p05_s06a/citywalker_trajectory.png",
    width=3.0,
    label="CityWalker trajectory sample",
)
traj_img.next_to(stats_group, RIGHT, buff=0.4)
self.play(FadeIn(traj_img, run_time=0.30))
```

### 2-G  Vid2Sim — real vs sim comparison

File: `studio/scenes/part05/p05_s08_vid2sim.py`

Add a side-by-side pair after the Gaussian Splatting animation:

```python
real_img = img_or_placeholder(
    "studio/assets/images/p05_s08/real_footage.png",
    width=3.0,
    label="Real city footage",
)
sim_img = img_or_placeholder(
    "studio/assets/images/p05_s08/gaussian_splatting.png",
    width=3.0,
    label="Gaussian Splatting output",
)
pair = VGroup(real_img, sim_img).arrange(RIGHT, buff=0.3)
pair.move_to(DOWN * 0.4)
self.play(FadeIn(pair, run_time=0.45))
```

---

## Phase 3 — Layout fixes (2D scenes only)

**Do not touch i02_the_hook.py or p02_s05_radar_waves.py in this phase.**

Render each scene before editing to see the exact problem. After editing, render again.

Canvas safe zone: x ∈ [-6.5, 6.5], y ∈ [-3.8, 3.8].

Layout helpers to prefer over raw `move_to`:
- `place_title(mob)` — centers at y = 3.2
- `place_left(mob, y=0)` — centers at x = -4.0
- `place_right(mob, y=0)` — centers at x = 4.0
- `place_footer(mob)` — centers at y = -3.5
- `content_row(*items, buff, y)` — horizontal row centered in content band
- `content_column(*items, buff, x, y)` — vertical stack
- `two_column(left, right, gap)` — side-by-side arrangement

### 3-A  FadeOut audit — all 2D body scenes

Every scene must end cleanly. `StudioScene._close()` handles this, but some
scenes that do not call `_close()` may leave orphan mobs.

Check: the last frame of each rendered MP4 should be blank (BG_PAPER cream), not
showing any content.

Scenes to audit:
- Any scene where `construct()` does not call `self._close()` at the end.
- Bridge scenes (i04, p01_s10, p02_s14, p03_s15, p04_s10) — these tend to be
  short and may skip the close.

Fix: add `self._close()` as the final line of `construct()`.

### 3-B  Roadmap strip label collisions — PartTitleCard scenes

`StudioScene._roadmap_strip()` alternates labels above/below dots:
```python
t.next_to(d, DOWN if i % 2 == 0 else UP, buff=0.12)
```

If the scene has content near y = -3.0 (bottom of content area), the UP-shifted
labels on odd dots (y ≈ -2.7) may collide with content. Fix: move the entire strip
lower by calling `dots.to_edge(DOWN, buff=0.22)` before adding labels, or remove
labels entirely (keep just dots) if collision cannot be resolved.

### 3-C  Axes-before-data rule

For every scene with a chart: confirm that `ShowCreation(axes)` (or `axes_deploy()`)
runs before any data lines, bars, or dots are added.

Common incorrect pattern to look for and fix:

```python
# WRONG — data before axes
self.add(data_group)
self.play(ShowCreation(axes))

# CORRECT
self.play(ShowCreation(axes))
self.play(LaggedStart(*(GrowFromCenter(d) for d in data_group), lag_ratio=0.05))
```

Affected scenes to check:
- `p01_s02a_genai_timeline.py` — timeline chart
- `p02_s02a_119m.py` — death counter + icon grid
- `p04_s03_annotation_cost.py` — bar chart
- `p04_s08_quantv2x.py` — size comparison chart
- Any scene using `axes_deploy()` from `charts.py`

### 3-D  Milestone label overlaps in timeline scenes

In `p01_s02a_genai_timeline.py` and similar: milestone dots at nearby x-positions
(e.g., GPT-3 2020 and CLIP 2021) can produce overlapping labels.

After building all milestone label mobs but before animating, run a one-pass
vertical de-collision:

```python
sorted_by_x = sorted(milestone_mobs, key=lambda m: m[1].get_center()[0])
for i in range(1, len(sorted_by_x)):
    dot_a, lbl_a = sorted_by_x[i - 1]
    dot_b, lbl_b = sorted_by_x[i]
    if lbl_b.get_left()[0] - lbl_a.get_right()[0] < 0.2:
        lbl_b.shift(UP * 0.5)   # push later label up
```

### 3-E  Right-column text overflow check

Several scenes place text in the right column near x = RIGHT_X = 4.0. Check that
no text mob extends past MAX_TEXT_X = 6.5:

```python
if mob.get_right()[0] > 6.2:
    mob.scale(6.2 / mob.get_right()[0])
```

Apply this check to long labels in part02 and part04 scenes that have right-column
annotation text.

---

## Phase 4 — Visual enhancements

Apply selectively. Each enhancement should improve clarity, not add noise.

### 4-A  Add thought_bubble for conceptual question moments

`thought_bubble(text, target)` from `annotations.py` creates a Pi-style thinking bubble
pointing up from a vehicle or agent icon.

Good candidates — scenes that pose the core "why" question without currently showing
a conceptual prompt:

- `p01_s04a_longtail_problem.py` — after showing the long-tail distribution, add a
  thought bubble above the ego vehicle: `"Corner cases: 0.001% of data, 80% of crashes"`
- `p02_s02a_119m.py` — after the 1.19M counter: `"Can tech close this gap?"`
- `p04_s03_annotation_cost.py` — after the cost bars: `"What if labels were free?"`

Placement pattern:

```python
from studio.components.annotations import thought_bubble

car = vehicle_icon(color=self.PART_COLOR).to_corner(DL, buff=0.5)
self.play(FadeIn(car, run_time=0.25))
bubble = thought_bubble("Corner cases:\n0.001% of data", car)
self.play(FadeIn(bubble, run_time=0.4))
self.wait(2.5)
self.play(FadeOut(bubble, run_time=0.3), FadeOut(car, run_time=0.2))
```

### 4-B  Add contribution_badge for paper highlights

`contribution_badge(label)` from `annotations.py` creates a gold rounded badge.
Use it when a paper is first named, before launching into the architecture detail.

Example in `p01_s07a_bevdriver.py`:

```python
from studio.components.annotations import contribution_badge

badge = contribution_badge("BEVDriver  ·  IROS 2023")
badge.to_corner(UL, buff=0.4)
self.play(FadeIn(badge, run_time=0.3))
```

### 4-C  Bridge scene wipe

The bridge scenes (i04, p01_s10, p02_s14, p03_s15, p04_s10) transition between
parts. Each should end with the upcoming part's accent color sweeping across the
canvas to signal a new topic.

Insert this block before `_close()` in each bridge scene:

```python
# Replace NEXT_ACCENT with the next part's accent color constant
wipe = Rectangle(
    width=15.0, height=9.0,
    fill_color=NEXT_ACCENT, fill_opacity=0.0, stroke_width=0,
)
self.add(wipe)
self.play(wipe.animate(run_time=0.5, rate_func=smooth).set_fill(opacity=0.85))
self.play(FadeOut(wipe, run_time=0.4))
```

Next-part accent per bridge:

| Bridge file | NEXT_ACCENT |
|---|---|
| `i04_bridge_to_p1.py` | `ACCENT_BLUE` |
| `p01_s10_bridge_to_p2.py` | `ACCENT_TEAL` |
| `p02_s14_bridge_to_p3.py` | `ACCENT_GREEN` |
| `p03_s15_bridge_to_p4.py` | `ACCENT_AMBER` |
| `p04_s10_bridge_to_p5.py` | `ACCENT_PINK` |

### 4-D  Chart baseline alignment

For any scene with multiple bar groups: ensure all bars share an aligned bottom edge
by using `arrange(RIGHT, aligned_edge=DOWN)`:

```python
bars = VGroup(bar1, bar2, bar3)
bars.arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
```

If bars are built with individual `move_to()` calls, verify they share the same
bottom y by checking `bar.get_bottom()[1]` — all should be equal.

### 4-E  `p05_s09_living_city.py` — camera pan return

If this scene uses `self.frame.animate.move_to(...)` or `self.frame.animate.scale(...)`,
the final frame must return to center before `_close()`:

```python
self.play(self.frame.animate(run_time=0.6).move_to(ORIGIN).set_height(8.0))
self._close()
```

---

## Phase 5 — Final render and merge

After all phases, render each part at low quality to verify no crashes:

```powershell
.\render_studio_all.ps1
```

For final 1080p output, re-render in sections (render_studio_all.ps1 only does `-l`):

```powershell
# Each scene individually at --hd
manimgl -w --hd studio/scenes/intro/i01_title_card.py I01TitleCard
# ... repeat for all scenes
```

Merge all MP4 files with ffmpeg (ensure ffmpeg is in PATH):

```powershell
$videos_dir = "C:\Users\admin\Downloads\ML\Lab01_3B1B\videos"
$all_mp4 = Get-ChildItem $videos_dir -Filter "*.mp4" | Sort-Object Name
$list_file = "$videos_dir\_concat.txt"
$all_mp4 | ForEach-Object { "file '$($_.FullName)'" } | Out-File $list_file -Encoding utf8
ffmpeg -y -f concat -safe 0 -i $list_file -c copy "$videos_dir\_FINAL_BeyondSelfDriving.mp4"
```

---

## Quick-reference scene index

| File | Class | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|---|---|---|---|---|---|
| `intro/i01_title_card.py` | I01TitleCard | — | — | FadeOut | — |
| `intro/i02_the_hook.py` | I02TheHook | — | — | **SKIP 3D** | — |
| `intro/i03_roadmap.py` | I03Roadmap | — | — | FadeOut | — |
| `intro/i04_bridge_to_p1.py` | I04BridgeToP1 | — | — | FadeOut | 4-C wipe |
| `part01/p01_s02a_genai_timeline.py` | P01S02AGenAITimeline | — | — | 3-C axes, 3-D labels | — |
| `part01/p01_s07a_bevdriver.py` | P01S07ABEVDriver | — | 2-A | — | 4-B badge |
| `part01/p01_s07b_emma.py` | P01S07BEMMA | — | 2-A | — | 4-B badge |
| `part01/p01_s07c_drivevlm.py` | P01S07CDriveVLM | — | 2-A | — | 4-B badge |
| `part01/p01_s08a_autovla_switch.py` | P01S08AAutoVLASwitch | — | 2-A | — | 4-B badge |
| `part01/p01_s10_bridge_to_p2.py` | P01S10BridgeToP2 | — | — | FadeOut | 4-C wipe |
| `part02/p02_s01_title.py` | P02S01Title | 1-B quote | — | — | — |
| `part02/p02_s02a_119m.py` | P02S02A119M | — | — | 3-C axes | 4-A bubble |
| `part02/p02_s05_radar_waves.py` | P02S05RadarWaves | — | — | **SKIP 3D** | — |
| `part02/p02_s10_v2xpnp_dataset.py` | P02S10V2XPnPDataset | — | 2-B | — | — |
| `part02/p02_s14_bridge_to_p3.py` | P02S14BridgeToP3 | — | — | FadeOut | 4-C wipe |
| `part03/p03_s03_smart_intersection.py` | P03S03SmartIntersection | — | 2-C | — | — |
| `part03/p03_s08_cooperfuse.py` | P03S08CooperFuse | — | 2-D | — | — |
| `part03/p03_s15_bridge_to_p4.py` | P03S15BridgeToP4 | — | — | FadeOut | 4-C wipe |
| `part04/p04_s03_annotation_cost.py` | P04S03AnnotationCost | — | — | 3-C axes | 4-A bubble |
| `part04/p04_s08_quantv2x.py` | P04S08QuantV2X | — | — | 3-C axes, 3-D | — |
| `part04/p04_s10_bridge_to_p5.py` | P04S10BridgeToP5 | — | — | FadeOut | 4-C wipe |
| `part05/p05_s04a_compositional_quote.py` | P05S04ACompositionalQuote | **1-A quote** | — | — | — |
| `part05/p05_s04b_metaurban.py` | P05S04BMetaUrban | — | 2-E | — | — |
| `part05/p05_s06a_citywalker.py` | P05S06ACityWalker | — | 2-F | — | — |
| `part05/p05_s08_vid2sim.py` | P05S08Vid2Sim | — | 2-G | — | — |
| `part05/p05_s09_living_city.py` | P05S09LivingCity | — | — | 4-E cam pan | — |
