# Animation Plan — P02S11A2RootCauses ("Two Root Causes")

New scene file: `studio/scenes/part02/p02_s11a2_root_causes.py`
Class: `P02S11A2RootCauses(StudioScene)` — **2D scene** (the 3D landscape belongs to the next
scene; keep this one flat and cheap).

Position in the cut: **between** [p02_s11a_turbotrain_problem.py](p02_s11a_turbotrain_problem.py)
(empirical scatter — "one-shot runs collapse") and
[p02_s11b_turbotrain_solution.py](p02_s11b_turbotrain_solution.py) (3D loss landscape — the
"TurboTrain Solution" frame).

Narration (target, from `studio_scripts/script_part2.md` §P02S11A — this scene takes over the
second half of that section):

> *"Two root causes. **Initialization sensitivity**: a complex architecture with temporal,
> multi-agent, and multi-task dimensions converges to a bad local minimum when trained from random
> initialization. **Gradient conflict**: detection, prediction, and planning objectives pull the
> model's weights in contradictory directions. Standard SGD has no mechanism to resolve this."*

The scene's job: make both **mechanisms** legible visually — not as bullet text. S11a already
showed the *symptom* (collapsed runs); this scene shows *why*; s11b shows the *fix*. The narration
is ~22 s, so budget ~10 s per cause + ~3 s for the closing beat.

---

## Why a dedicated scene (not a rework of s11a)

- s11a's scatter chart is evidence, and it works; cramming a mechanism diagram into it would
  bury both.
- s11b *assumes* the viewer already pictures a rugged landscape and conflicting gradients — its
  Stage 1/Stage 2 beats land much harder if this scene has planted exactly those two pictures.
- The narration sentence literally enumerates two causes; a scene with two visual beats maps 1:1.

---

## Design goals

> **Guiding principle: minimal text** (same as all studio scenes). The mechanism is carried by
> *shape morphing* (cause 1) and *vector geometry* (cause 2). On-screen words: arrow tags
> ("det" / "pred" / "plan"), three dimension chips, and two ≤3-word cause labels. Nothing else.

- Cause 1 must answer *"why does complexity → bad minima?"* — show the landscape **getting
  rugged as dimensions are added**, then show random starts falling into the new sharp pits.
- Cause 2 must answer *"why can't SGD fix it?"* — show gradients **cancelling** and the weight
  point **going nowhere**, not just three arrows pointing apart.
- End-frame plants the visual vocabulary of s11b: rugged landscape ↔ Stage 1 (GOLD_RICH),
  conflicting gradients ↔ Stage 2 (GREEN_FIX). Reuse those exact colors on the closing chips.
- Layout: each beat builds at ~full content width for clarity, then **shrinks and parks** into
  its half (left = cause 1, right = cause 2) so the final frame is a side-by-side summary.

---

## Beat 1 — Initialization sensitivity (~10 s)

**Visual: a 1D loss curve that grows local minima as complexity chips are added, then balls
dropped from random inits get trapped.**

1. `axes_deploy` a wide flat axes block (no ticks/labels — abstract loss-vs-θ), centered,
   width ≈ 9.5, height ≈ 3.4, parked around `UP * 0.4`. Play the deploy anim **before** any
   curve (design rule).
2. Draw the **simple** loss curve first: a single smooth wide bowl
   (`curve_trace` or `VMobject.set_points_smoothly` over `f0(x) = 0.18·(x−c)²`),
   stroke `ACCENT_TEAL` (part-2 accent), width ≈ 4.
3. Three small chips appear one by one above the axes (use `pipeline_block` or plain rounded
   rects, `BG_CARD` fill, `INK_MID` stroke): **temporal**, **multi-agent**, **multi-task**.
   As each chip lands, `Transform` the curve into a progressively more rugged version:
   - `f1 = f0 + bump A` (one shallow dip)
   - `f2 = f1 + bumps B,C` (two more, sharper)
   - `f3 = f2 + high-freq ripple` (final rugged curve: 1 wide deep global basin on the right,
     3 sharp shallow local minima left/center)
   Implementation: precompute the four curves as Gaussian-bump sums
   (`f(x) = bowl − Σ aᵢ·exp(−(x−bᵢ)²/wᵢ)`), sample ~120 points each with identical point count
   so `Transform` interpolates cleanly.
   *(Optional continuity touch: shape `f3` to roughly match a 1D slice of s11b's `_loss` —
   eyeball it, don't import.)*
4. **Drop the inits.** 4 dots (`Dot`, radius 0.09, `INK_LIGHT` fill) fade in at random x
   positions on the curve's upper slopes. Tag the group once with a tiny caption "random init"
   (`SIZE_CAPS`, `INK_MID`) that fades after the drop starts.
5. Animate descent: for each ball, precompute a gradient-descent path on `f3`
   (30–40 GD iterations, step ~0.08, project onto the curve) → `set_points_smoothly` →
   `MoveAlongPath` (same pattern as s11b's `bad_dot`). Run all four with `LaggedStart`,
   lag ≈ 0.15, run_time ≈ 2.2.
6. **3 of 4 get trapped** in the sharp minima: on arrival each trapped dot snaps to `RED_ERROR`
   and does one small `Indicate`-style pulse; the 1 lucky ball reaches the wide basin and turns
   `GREEN_FIX` *briefly*, then dims to `INK_LIGHT` (it's the exception, not the story).
7. Park the beat: scale the whole group to ≈ 0.62 and slide to `LEFT_X`; a cause chip
   **"init sensitivity"** (`GOLD_RICH` text on `BG_CARD`, bold, `SIZE_LABEL`) settles under it.
   GOLD_RICH is deliberate — it pre-echoes s11b's Stage 1 label color.

## Beat 2 — Gradient conflict (~9 s)

**Visual: weight-space plane, three task gradients at obtuse angles, a near-zero resultant,
and a θ that zigzags in place while the true minimum sits unreached.**

1. On the (now clear) right-of-center area, fade in a minimal weight-space frame: two thin
   `LINE_ARROW` axes arrows (no ticks), ~3.6 × 3.6, plus a small ring marker `★`-less target —
   a `Circle` (radius 0.12, `GREEN_FIX` stroke, dashed feel via low opacity fill) at the lower
   right = the joint minimum, with a `DashedLine` from θ to it (stroke_opacity ≈ 0.45).
2. Place θ: `Dot` (radius 0.1, `INK_DARK`) center-left of the frame.
3. Grow three gradient arrows out of θ (`Arrow`, stroke_width ≈ 5, tip small), pairwise angles
   > 90°:
   - **det** — `ACCENT_BLUE`, pointing up-right
   - **pred** — `GOLD_RICH`, pointing down-right
   - **plan** — `ACCENT_PINK` (or `PURPLE_MODEL` if pink reads too part-5), pointing left
   Each gets a one-word `SIZE_CAPS` tag at its tip. Stagger with `LaggedStart(GrowArrow…)`.
4. **Show the conflict explicitly:** draw a red `Arc` between det and plan (the most obtuse
   pair), `RED_ERROR`, with nothing but the arc — the obtuse angle *is* the statement.
   Then draw the **resultant**: a stubby `DashedLine`/small arrow from θ, `INK_MID`,
   length ≈ 15 % of the task arrows — the sum nearly cancels. One short pulse on it.
5. **SGD goes nowhere:** animate 5–6 alternating steps — θ moves a small step along det's
   direction, then pred's, then plan's, leaving a thin jittery `TracedPath`-style trail
   (`VMobject` polyline, `INK_LIGHT`, width 2). The trail crosses itself; net displacement
   toward the green target ≈ 0. Keep the dashed line to the target visible the whole time —
   the gap never closes. (Precompute the zigzag points; ~1.8 s total.)
6. Park the beat at `RIGHT_X` at the same scale as beat 1; cause chip **"gradient conflict"**
   (`GREEN_FIX` text on `BG_CARD`) settles under it — pre-echoing s11b's Stage 2 color.

## Closing beat (~3 s)

- Both parked panels dim to opacity ≈ 0.5; the two cause chips stay at full strength.
- One short center-bottom line, `SIZE_LABEL`, `INK_DARK`, bold: **"SGD cannot fix either."**
  (5 words max — it's the bridge into the TurboTrain frame. If it feels crowded on render,
  drop it; the chips alone may carry it.)
- `self.wait(0.8)` → `self._close()`.

---

## Animation sequence summary

1. `self._open("Two Root Causes")`.
2. Beat 1: axes deploy → smooth bowl → 3 chips, 3 curve morphs → 4 inits drop → 3 trapped red,
   1 escapes → shrink-park left + GOLD chip.
3. Beat 2: weight frame + target → θ → 3 task arrows w/ tags → red obtuse arc → tiny resultant →
   zigzag trail, gap to target never closes → park right + GREEN chip.
4. Dim both, closing line, `_close()`.

Target duration ≈ 22–24 s, matching the narration block.

---

## Implementation notes

- `StudioScene`, `PART_NUM = 2` (`ACCENT_TEAL` / `PASTEL_TEAL` available as `self.PART_COLOR` /
  `self.PART_PASTEL`).
- All colors imported from `studio/components/colors.py`; never hex literals.
- Curve morphs: build all curve variants with the **same number of sampled points** so
  `Transform` doesn't sliver. Helper: `def _curve(axes, bumps): …` returning `VMobject`.
- Descent paths: pure precompute (no updaters) — mirror s11b's `bad_path` / `MoveAlongPath`
  pattern.
- Text built outside `self.play`/`self.add` paths must go through `self._force_text_contrast`
  (or just rely on the overridden `add`/`play`). No curly quotes.
- `SCRIPT` constant: `"Two root causes: rugged landscape from random init, and task gradients
  that cancel."`

## Integration checklist

- [ ] Create `p02_s11a2_root_causes.py` with class `P02S11A2RootCauses` (the `a2` infix keeps
      s11a/s11b filenames stable; no renames in the render script beyond one added line).
- [ ] Add the scene to `render_studio_all.ps1` between s11a and s11b.
- [ ] Split `studio_scripts/script_part2.md` §P02S11ATurboTrainProblem: keep the "why is
      one-time training so hard" lead-in under s11a; move the "Two root causes…" paragraph into
      a new `## [P02S11A2RootCauses — "Two Root Causes"]` section. Mirror in
      `studio_scripts/latex/main.tex` if that file is being kept in sync.
- [ ] Verify design rules: BG_PAPER, axes before data, ends on `_close()`, English-only on
      screen.

## Render & review

```bash
cd "/Users/phu-quynguyen-lam/o D/Beyond_SelfDriving"
# iterate
PYTHONPATH="$PWD" /Users/phu-quynguyen-lam/miniforge3/envs/manim/bin/manimgl \
  -w -l studio/scenes/part02/p02_s11a2_root_causes.py P02S11A2RootCauses
# final (required)
PYTHONPATH="$PWD" /Users/phu-quynguyen-lam/miniforge3/envs/manim/bin/manimgl \
  -w --hd studio/scenes/part02/p02_s11a2_root_causes.py P02S11A2RootCauses
```

Frames to spot-check: (a) final rugged curve with 3 trapped red balls; (b) the obtuse-arc +
tiny-resultant moment; (c) the parked side-by-side end frame with both chips.
