# Studio Scene Fix Plan
# Generated after visual audit — session 2026-05-30

Read `studio/CLAUDE.md` first for render commands, component APIs, and layout constants.

## How to render + check a scene

```powershell
$env:PYTHONPATH = "C:\Users\admin\Downloads\ML\Lab01_3B1B"
$env:PATH = "C:\Users\admin\miniconda3\Scripts;C:\Users\admin\miniconda3\Library\bin;" + $env:PATH
Set-Location "C:\Users\admin\Downloads\ML\Lab01_3B1B"

manimgl -w -l studio/scenes/part03/p03_s06_localization_role.py P03S06LocalizationRole

# Extract a mid-scene frame to inspect
$env:PATH = "C:\Users\admin\miniconda3\Scripts;C:\Users\admin\miniconda3\Library\bin;" + $env:PATH
ffmpeg -i videos/P03S06LocalizationRole.mp4 -vf "select='eq(n\,90)'" -vsync 0 videos/_check.png -y
```

---

## Already fixed this session (do not redo)

| Scene | Fix applied |
|---|---|
| `p04_s03_annotation_cost.py` | `bar_reveal()` unpack bug; chart centered; Y-axis labels via `chart_mount` + `next_to(tick_labels, LEFT)`; key_number moved to `to_corner(DR)` |
| `p05_s09_living_city.py` | VMobject filter removed — now fades all `self.mobjects` |
| `p05_s11_final_frame.py` | Added `self._close()` safety net |

---

## Batch A — Invisible content (fix first, most critical)

### A1 · `p03_s04b_space_calibration.py` — white point cloud dots

**Problem:** Point cloud dots are white (`WHITE`) on cream BG_PAPER → invisible.

**Fix:** In the point-cloud generation loops, replace dot colors:
- Vehicle point cloud → `ACCENT_BLUE`
- Infrastructure point cloud → `ACCENT_GREEN`
- Any "merged" cloud → `ACCENT_AMBER`

Look for `Dot(radius=..., color=WHITE)` or `color=WHITE` in the point-cloud helper and swap colors.

**Verify:** Dots should be clearly visible as two distinct colored clusters.

---

### A2 · `p03_s06_localization_role.py` — white dots + unclear animation

**Problem:** Point cloud dots are white → invisible. The bad-vs-good localization contrast is hard to read.

**Fix:**
1. Bad localization side: dots = `RED_ERROR` (lộn xộn / misaligned)
2. Good localization side: dots = `ACCENT_GREEN` (aligned grid)
3. After the two clouds appear, add a brief annotation:
   - Bad side: `error_callout("Misaligned — object lost", target, side="right")` in red
   - Good side: `callout("Aligned — fusion succeeds", target, side="right")` in green
4. Fade callouts before `_close()`

**Verify:** Two clearly different colored clouds with contrast labels.

---

### A3 · `p03_s07_kalman_filter.py` — labels cropped + white stream dots

**Problem:** "GNSS" / "IMU" / "LiDAR" labels at `to_edge(LEFT)` are cut off by the canvas edge. Stream dots are white → invisible.

**Fix:**
1. Shift the entire layout RIGHT by ~1.5u: change the left anchor from `LEFT_X` / `to_edge(LEFT)` to `LEFT * 3.0` or use `place_left(mob, y=...)` with appropriate y offsets.
2. Stream dot colors:
   - GNSS (5 Hz) → `ACCENT_BLUE`
   - IMU (100 Hz) → `ACCENT_AMBER`
   - LiDAR (1 Hz) → `ACCENT_GREEN`
3. Increase dot radius slightly (0.06 → 0.10) for visibility.

**Verify:** All three stream labels fully visible; dots clearly colored; Kalman box in center.

---

### A4 · `p05_s04a_compositional_quote.py` — quote text white

**Problem:** The two quote lines (`quote1`, `quote2`) render as white on the BG_TITLECARD cream background. Only "— Stuart Geman" (dark) is readable. ManimGL white-text bug not caught because the text is stored in a VGroup and animated via `LaggedStart(Restore(...))` — the `_force_text_contrast` override doesn't apply to pre-saved states.

**Fix:** After creating `quote1` and `quote2`, and BEFORE calling `save_state()`, explicitly set color:
```python
quote1 = Text('"The world is compositional,', font=FONT_PRIMARY, font_size=SIZE_H1, color=GOLD_RICH)
quote2 = Text('or there is a god."', font=FONT_PRIMARY, font_size=SIZE_H1, color=GOLD_RICH)
# Force color before save_state so Restore() brings back the correct color
for mob in [quote1, quote2]:
    mob.set_color(GOLD_RICH)
    for sub in mob.family_members_with_points():
        sub.set_color(GOLD_RICH)
```
Then proceed with `save_state()` / scatter / `Restore()` as before.

**Verify:** Quote text visible as gold on cream background.

---

### A5 · `p05_s06a_citywalker.py` — world map dots white

**Problem:** City dots on the world map ellipse are white → invisible on light gray oval on cream background.

**Fix:**
1. Dot colors: cycle through `[ACCENT_PINK, ACCENT_AMBER, ACCENT_BLUE, ACCENT_GREEN]` based on index
2. Increase dot radius: 0.04 → 0.08
3. Increase dot opacity to 0.9
4. The world ellipse fill: use `BG_CARD` (slightly darker cream) at opacity 0.6 so it reads as a shape

**Verify:** World map visible; city dots clearly distinguishable from background.

---

## Batch B — Chart / pipeline layout (left-heavy)

### B1 · `p01_s08b_autovla_results.py` — chart left-heavy + Y-label overlap

**Problem:** Same chart layout issues as the fixed `p04_s03`: Y-axis "Score" label overlaps tick numbers; chart in left 40% of canvas.

**Fix pattern** (same as p04_s03 fix):
```python
axes, axes_anim = axes_deploy(x_range, y_range)
tick_labels = chart_mount(axes, position=RIGHT * 0.4 + UP * 0.1, scale=0.85)
y_lbl = Text("Score", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_MID, weight=BOLD)
y_lbl.rotate(90 * DEGREES)
y_lbl.next_to(tick_labels, LEFT, buff=0.35)  # next_to LABELS GROUP not y_axis
```
Also add dataset labels below X-axis (nuPlan / nuScenes) centered under their bar groups using `x_step = (x1-x0)/n_bars` formula.

Key numbers ("+10.6% planning", "-66.8% runtime") → `to_corner(DR, buff=0.5)` or two stacked `key_number` mobs on the right.

---

### B2 · `p02_s11a_turbotrain_problem.py` — chart left-heavy, dots small

**Problem:** Axes in left ~45% of canvas; scatter dots barely visible.

**Fix:**
```python
tick_labels = chart_mount(axes, position=RIGHT * 0.3 + DOWN * 0.2, scale=0.85,
                          x_label="AP@0.5", y_label="EPA")
```
Increase scatter dot radius: 0.08 → 0.14. Add a legend (failure zone label, manual solution label) in the top-right area of the content band.

---

### B3 · `p03_s09_v2x_realo.py` — left-heavy pipeline

**Problem:** Blob + compressor box occupying left half; output blob and key_number appear late.

**Fix:**
- Position input blob at `LEFT * 4.0`
- Compressor box at `ORIGIN`
- Output blob at `RIGHT * 3.5`
- Add `Arrow(compressor.get_right(), output.get_left())` visible from start
- `key_number("32x", "compression ratio", color=GOLD_RICH).to_corner(DR, buff=0.5)`

---

### B4 · `p04_s08_quantv2x.py` — pipeline review + timing

**Problem:** 51-second wait at end is padding. Need to verify full pipeline flow is readable.

**Fix:**
1. Reduce `self.wait(51)` to `self.wait(2)`
2. Check that the 3-stage pipeline labels are visible: font size ≥ SIZE_LABEL, color = INK_DARK
3. Ensure blob shrink animation (FP32 → INT8) shows the size labels clearly: "100 MB FP32" → "0.33 MB INT8"
4. `key_number("300x", "size reduction", color=GOLD_RICH).to_corner(DR, buff=0.5)`

---

## Batch C — Label / margin / overflow

### C1 · `p01_s07c_drivevlm.py` — "Fast/Slow" labels overlap

**Problem:** "Fast / 10 Hz" and "Slow / 2 Hz" labels are stacked on top of the "Driving scene" input block, overlapping text.

**Fix:** Move speed labels to the RIGHT of each lane's first block (above/below the lane line), not floating over the input:
```python
fast_lbl.next_to(fast_lane[0], UP, buff=0.15)   # above Perception block
slow_lbl.next_to(slow_lane[0], DOWN, buff=0.15)  # below Vision block
```
Add a shared "Driving scene" input column on the LEFT, separate from the speed labels, with arrow forks splitting into the two rows.

---

### C2 · `p05_s10_chain_of_solutions.py` — text overflow in panels

**Problem:** Keyword labels (e.g., "Foundation Models AutoVLA") overflow the panel borders. "PedGon alive" is clipped at right edge.

**Fix:**
1. Reduce keyword text to `SIZE_MICRO` (14pt)
2. Wrap long keywords: split at natural break ("Foundation Models\nAutoVLA")
3. Keep panel text inside using `.scale_to_fit_width(panel.width - 0.3)` after creation
4. Shift the rightmost panel (Part 5) LEFT by 0.2u so it doesn't clip the canvas edge

---

## Batch D — Design redesign

### D1 · `p04_s05_turbotrain_landscape.py` — redesign as axes-based scatter

**User request:** "làm giống p02s11" (make it like p02_s11a TurboTrain Problem scatter plot)

**Current:** Bare ellipse contours (no axes, no labels, faint gray on cream).

**New design:**
1. Use `axes_deploy` with x_range and y_range representing two task losses
2. Draw gradient contour ellipses ON the axes (color from RED_ERROR outer → GOLD_RICH inner)
3. Conflict point (orange dot) at a specific data coordinate
4. Three gradient arrows from that point in different directions (task1, task2, task3)
5. Path 1 (without TurboTrain): zigzag red path drifting away
6. Path 2 (with TurboTrain): smooth spiral converging to optimum (gold star at axes minimum)

```python
axes, axes_anim = axes_deploy((0, 10, 2), (0, 10, 2),
                               x_label="Task 1 Loss", y_label="Task 2 Loss")
tick_labels = chart_mount(axes, position=DOWN * 0.2, scale=0.85,
                           x_label="Task 1 Loss", y_label="Task 2 Loss")
```
Match the visual style of `p02_s11a` exactly: same axis style, same dot sizes, similar color choices.

---

### D2 · `p03_s08_cooperfuse.py` — clearer two-stage visualization

**User request:** "cần đọc và visualize lại dễ hiểu hơn"

**Current:** Two overlapping Gaussian ellipses, left side only.

**New design — two explicit stages side by side:**

**Stage 1 (LEFT half) — NMS baseline:**
- Two Gaussian ellipses overlapping (blue = vehicle, green = infra)
- NMS discards the smaller one: animate `FadeOut(infra_ellipse)` + red X mark
- Label: `Text("NMS: discards weak detection", SIZE_LABEL, RED_ERROR)`
- Result: only one ellipse remains, wider uncertainty

**Stage 2 (RIGHT half) — CooperFuse:**
- Same two Gaussian ellipses
- Fuse: animate both shrinking into a single tighter ellipse (GOLD_RICH)
- Label: `Text("CooperFuse: tighter fusion", SIZE_LABEL, ACCENT_GREEN)`
- Result: smaller uncertainty ellipse

Use a vertical divider `Line(UP*2.5, DOWN*2.5, stroke_color=INK_LIGHT, stroke_width=1)` between stages.

```python
# Gaussian ellipse helper
def gaussian_ellipse(cx, cy, rx, ry, color, alpha=0.3):
    e = Ellipse(width=rx*2, height=ry*2, fill_color=color, fill_opacity=alpha,
                stroke_color=color, stroke_width=2)
    e.move_to([cx, cy, 0])
    return e
```

---

### D3 · `p03_s02_sim_real_gap.py` — add actual visual content

**Problem:** Both columns are mostly empty — just "Simulation" / "Reality" labels on a cream canvas.

**Fix — add visual content to each column:**

LEFT (Simulation):
- Clean straight road (two `Line` objects, teal/uniform)
- One `vehicle_icon(ACCENT_BLUE)` driving perfectly centered
- Label: `Text("Clean  ·  Predictable  ·  Unlimited", SIZE_CAPS, ACCENT_TEAL)`

RIGHT (Reality):
- Noisy road (wavy `VMobject` path, slightly irregular)
- One `vehicle_icon(ACCENT_AMBER)` on it
- Random noise dots scattered (small, ACCENT_AMBER, low opacity)
- Label: `Text("Noisy  ·  Unpredictable  ·  Expensive", SIZE_CAPS, ACCENT_AMBER)`

Gap label at the bottom center: `Text("Sim-to-Real Gap", SIZE_H1, RED_ERROR)` with arrow pointing at the divider.

---

## Batch E — Enhancement / spacing

### E1 · `p03_s04a_time_calibration.py` — more spacing, clearer labels

**User request:** "làm dễ hiểu hơn, tăng spacing"

**Fix:**
1. Move the vehicle start position from left-center to `LEFT * 4.5`
2. Move the ghost/delayed observation position to `LEFT * 1.5` (gap = 3u instead of ~1.5u)
3. The offset error arrow: `DoubleArrow` between the two, labeled `Text("83 cm offset", SIZE_LABEL, RED_ERROR)` above it
4. Add a horizontal ruler/timeline below the road: small tick marks at every 0.5u with "0ms", "50ms" labels
5. Add `Text("Infrastructure sees 50ms behind", SIZE_LABEL, INK_MID)` as a caption below the arrow

---

### E2 · `p04_s06_latency_chain.py` — bold ending

**User request:** "đoạn cuối, bold cái gì lên ấy"

**Fix:** After the three pipeline blocks + time labels are shown, add a finale beat:
```python
# Show total vs budget
total_lbl = Text("Total: 150ms+", font=FONT_PRIMARY, font_size=SIZE_H1,
                  color=RED_ERROR, weight=BOLD)
budget_lbl = Text("Budget: < 100ms", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                   color=INK_MID)
total_lbl.to_edge(DOWN, buff=0.8)
budget_lbl.next_to(total_lbl, UP, buff=0.2)
self.play(FadeIn(budget_lbl))
self.play(FadeIn(total_lbl, scale=1.15))
# Flash the Fusion Inference block red
self.play(fusion_block.animate(run_time=0.3).set_fill(RED_ERROR, opacity=0.25))
self.wait(2)
```

---

### E3 · `p01_s07b_emma.py` — improve canvas utilization

**Fix:** Restructure layout so CoT panel and output blocks appear in right half simultaneously with VLM reveal:
- Left column (x ≈ -3.5): Camera → VLM (stacked vertically)  
- Right column (x ≈ 2.5): CoT panel (top) + Output blocks (bottom)
- Use `two_column(left_group, right_group, gap=1.5)` from layout.py

---

### E4 · `p02_s02b_waymo_reduce.py` — scale up icon grid

**Fix:**
1. Scale icon grid so it spans LEFT half (x ∈ [-6, -0.5])
2. Increase icon size: currently too small to read at video resolution
3. Bar chart for injury reduction: RIGHT half (same pattern as p04_s03 fix)
4. Both left grid and right chart should be visible simultaneously for comparison

---

### E5 · `p05_s02a_llm_vs_robot.py` — balance layout

**Fix:** True two-column layout:
- LEFT col: data sources list + LLM box + "Trillions of tokens" (build sequentially)
- RIGHT col: robot icon(s) + "~10 hours each" + stark contrast label ("vs. Trillions")
- A `DoubleArrow` or `vs.` text in the CENTER dividing the two columns
- `key_number("1000x", "data gap", color=RED_ERROR).to_edge(DOWN, buff=0.4)`

---

### E6 · `p05_s02b_two_barriers.py` — scale zombie city

**Fix:**
1. Scale zombie squares from current size to 0.25u × 0.25u per square
2. Use `INK_MID` color (dark) instead of gray
3. Arrange in a 6×4 grid (not random scatter)
4. Each square moves in a straight line (zombie behavior) with `always_redraw` or repeated `MoveAlongPath`
5. Add `Text("No personality. No interaction. No life.", SIZE_LABEL, INK_LIGHT)` below

---

### E7 · `p05_s04b_metaurban.py` — connect generator to outputs

**Fix:**
1. Add `Arrow` from generator circle RIGHT edge → output scene box
2. When cycling scenes (Urban Scene 1 → 2 → 3…), do a quick fade-swap with scale pulse
3. Add `key_number("∞", "generated environments", color=ACCENT_PINK).to_corner(DR, buff=0.5)`

---

### E8 · `p05_s05a_urbansim_bottleneck.py` — center + add cost

**Fix:**
1. Center CPU–GPU diagram at ORIGIN (currently left-heavy)
2. After the transfer bottleneck flash, reveal cost in right area:
   ```python
   cost = key_number("180", "GPU-days to train", color=RED_ERROR)
   cost.to_corner(DR, buff=0.5)
   self.play(FadeIn(cost))
   ```
3. Remove dead code on line 22 (`if False else ...`)

---

## Batch F — 3D enhancement

### F1 · `p05_s09_living_city.py` — upgrade 2D agents to 3D

**User request:** "làm 3d dùm"

**Context:** Scene already uses `Studio3DScene`. Currently all agents (`vehicle_icon`, `pedestrian_icon`, `rsu_icon`, `drone_icon`) are 2D VGroup mobs placed in 3D space — they look flat.

**Fix:**

Replace 2D icon calls with 3D equivalents from `agents.py`:
```python
# Before
c = vehicle_icon(color=ACCENT_BLUE, scale=0.75)

# After
from studio.components import vehicle_icon_3d, rsu_tower_3d
c = vehicle_icon_3d(color=ACCENT_BLUE, scale=0.75)
c.apply_depth_test()
```

Add extruded building blocks for city feel:
```python
def city_block(w, h, d, color=INK_LIGHT):
    b = Prism(dimensions=[w, h, d])
    b.set_fill(color, opacity=0.4)
    b.set_stroke(color, width=0.8, opacity=0.6)
    b.apply_depth_test()
    return b
```
Place 6–8 building blocks at fixed positions BEFORE agents spawn (Phase 0).

For pedestrians (no 3D version in agents.py): use a `Cylinder(radius=0.05, height=0.3)` with a `Sphere(radius=0.07)` head. Keep `fix_in_frame()=False` so they're truly 3D.

RSU towers: `rsu_tower_3d(color=ORANGE_INFRA, height=0.8)` from `agents.py`.

Camera default angle: keep `default_frame_orientation = (-25, 60)`.

---

## Execution checklist

For each scene:
1. Read the existing file carefully
2. Apply the fix from this plan
3. Render: `manimgl -w -l <file> <Class>`
4. Extract frame: `ffmpeg -i videos/<Class>.mp4 -vf "select='eq(n\,90)'" -vsync 0 videos/_check.png -y`
5. View `_check.png` — confirm no invisible content, no overflow, no cropped labels
6. If OK, mark done below

## Progress tracker

| Batch | Scene | Status |
|---|---|---|
| A1 | p03_s04b SpaceCalibration | ✅ |
| A2 | p03_s06 LocalizationRole | ✅ |
| A3 | p03_s07 KalmanFilter | ✅ redesigned: flowing lanes + diagonal convergence lines |
| A4 | p05_s04a CompositionalQuote | ✅ |
| A5 | p05_s06a CityWalker | ✅ |
| B1 | p01_s08b AutoVLAResults | ✅ chart centered; "3× faster" replaces "-66.8%" |
| B2 | p02_s11a TurboTrainProblem | ✅ blue dots set_fill fix; radius 0.075→0.12 |
| B3 | p03_s09 V2XReaLO | ✅ layout OK; pipeline + 32x kn visible |
| B4 | p04_s08 QuantV2X | ✅ wait(51)→wait(2); packet dot color fixed |
| C1 | p01_s07c DriveVLM | ✅ shared input fork; Action moved to right-side horizontal merge |
| C2 | p05_s10 ChainOfSolutions | ✅ wrapped/clamped panel keywords; even panel spacing |
| D1 | p04_s05 TurboTrainLandscape | ✅ copied p02_s11b-style 3D loss surface + bad/good paths |
| D2 | p03_s08 CooperFuse | ✅ two-stage NMS vs CooperFuse visualization |
| D3 | p03_s02 SimRealGap | ✅ simulation/reality visual content + gap arrow |
| E1 | p03_s04a TimeCalibration | ✅ wider spacing + timeline + 83cm offset callout |
| E2 | p04_s06 LatencyChain | ✅ bold total/budget ending + fusion flash |
| E3 | p01_s07b EMMA | ✅ two-column layout with CoT + outputs visible |
| E4 | p02_s02b WaymoReduce | ✅ larger icon grid + right-side bar chart |
| E5 | p05_s02a LLMVsRobot | ✅ balanced two-column data-gap layout |
| E6 | p05_s02b TwoBarriers | ✅ 6x4 zombie grid + behavior caption |
| E7 | p05_s04b MetaUrban | ✅ generator-to-output arrows + scene swaps + key number |
| E8 | p05_s05a UrbanSimBottleneck | ✅ centered CPU-GPU bottleneck + 180 GPU-days cost |
| F1 | p05_s09 LivingCity (3D) | ⬜ |
