# Feedback — Beat 1 glyphs & "solved" checks in P02S11CPlanningPivot

Scene: [p02_s11c_planning_pivot.py](p02_s11c_planning_pivot.py), lines **75–134**.
Reviewed by extracting frames t ≈ 3.5 / 4.5 s. Two things look off, exactly as flagged: the
Perception/Prediction **glyphs** are ambiguous, and the green **checkmarks** read as crude / like a
folded page corner. The rest of the scene (planning "?", arrows, hook) is fine.

---

## Problem 1 — the glyphs don't say "perception" / "prediction"

**Perception** (lines 76–78): `sensor_cone(...)` is a frustum that fans *outward from a source*.
You rotate it `PI/2` and shrink it to `length=0.55`, so it collapses into a small **solid downward
wedge with a top-to-bottom opacity gradient** — it reads as a faded funnel / down-triangle, not
"sensing." A sensor cone only reads as sensing when it **fans outward from a point toward things it
detects**; a lone shrunk wedge loses that.

**Prediction** (lines 81–91): a 3-corner polyline with `radius=0.045` dots. At card size the dots
vanish and you're left with a thin **caret `∧`** — looks like a roof/chevron, not a trajectory
forecast. A forecast reads when it shows *now → future*: a curve with a fading/dashed tail and a
ghost endpoint, or a forward arrow.

At this tile size (inner panel ≈ 1.8 × 1.0) both are too small to carry meaning, and the labels
**"Perception" / "Prediction" already say it**. So:

### Option A (cleanest, recommended): drop the glyphs
The plan explicitly allowed "labels alone are acceptable if glyphs add clutter." Two clean labeled
teal cards + a proper solved-badge is calmer and reads instantly. Pass `None`/empty content to
`stage_panel` (or just the label). This also removes the muddy nested-panel + gradient look.

### Option B: keep glyphs, but make each legible and self-explanatory
If you want the glyphs, rebuild them so they're unambiguous and bigger:

```python
# Perception: sensor origin + outward fan + two detected blips
def perception_glyph(color=ACCENT_TEAL):
    src = ORIGIN + DOWN * 0.35
    fan = sensor_cone(src, color=color, spread=PI / 2.2, length=0.9, n_levels=5)
    fan.rotate(PI / 2, about_point=src)          # fan points UP (outward), not down
    blips = VGroup(
        Square(0.12).set_fill(color, 1).set_stroke(width=0).move_to(UP * 0.05 + LEFT * 0.22),
        Square(0.10).set_fill(color, 1).set_stroke(width=0).move_to(UP * 0.18 + RIGHT * 0.20),
    )
    src_dot = Dot(src, radius=0.05, color=color)
    return VGroup(fan, blips, src_dot)

# Prediction: present dot -> solid curve -> dashed future -> ghost endpoint
def prediction_glyph(color=ACCENT_TEAL):
    pts = [LEFT * 0.45 + DOWN * 0.1, LEFT * 0.05 + UP * 0.12, RIGHT * 0.45 + UP * 0.05]
    known = VMobject().set_points_smoothly(pts[:2]).set_stroke(color, 3.5)
    future = DashedVMobject(
        VMobject().set_points_smoothly(pts[1:]), num_dashes=7
    ).set_stroke(color, 3.5)
    now = Dot(pts[0], radius=0.06, color=color)
    ghost = Dot(pts[-1], radius=0.07, color=color, fill_opacity=0.35).set_stroke(color, 1.5)
    return VGroup(known, future, now, ghost)
```

The fan-up + blips says "I see objects around me"; the solid→dashed curve with a ghost endpoint
says "I forecast where things go." Make the inner panel a bit larger (or the glyphs ~1.3×) so they
don't shrink into ambiguity.

> Default to **Option A** unless a quick render shows the cards feel too bare. Glyphs are optional;
> clarity isn't.

---

## Problem 2 — the checkmark is crude and reads as a dog-ear

`make_checkmark` (lines 30–40) builds a thin open "V" whose two arms are almost equal length
(`LEFT*0.45+UP*0.1 → LEFT*0.1+DOWN*0.3 → RIGHT*0.5+UP*0.45`), then you park it **straddling the
card's rounded top-right corner** (lines 121–126). A thin green V tracing the corner looks like a
**folded page corner / stray triangle**, not a check. Three issues:

1. **Proportions** — a real check has a *short* down-left arm and a *long* up-right arm at a sharp
   angle (~2:1). Yours is near-symmetric, so it reads as a wide V.
2. **Placement** — an open stroke laid over the corner line merges with the border. Checks read as
   "done" when they sit in a **filled badge**, not as a bare stroke on an edge.
3. **Animation** — `ShowCreation` + `Flash` of a thin stroke looks flimsy; a badge that pops in
   reads as a stamp.

### Fix: a filled "solved" badge (disc + white check), popped in

```python
def solved_badge(r: float = 0.20) -> VGroup:
    disc = Circle(radius=r, fill_color=GREEN_FIX, fill_opacity=1.0, stroke_width=0)
    chk = VMobject().set_points_as_corners([
        LEFT * 0.10, DOWN * 0.06, RIGHT * 0.13 + UP * 0.10,   # short arm, long arm, sharp angle
    ])
    chk.set_stroke(BG_PAPER, width=3.2)   # cream check on green disc — crisp, not white-on-cream
    chk.set_fill(opacity=0)
    badge = VGroup(disc, chk)
    badge.set_stroke(behind=False)
    return badge
```

Place it cleanly at the corner and **pop** it in (no Flash needed):

```python
badge_p = solved_badge().move_to(perception[0].get_corner(UR))
badge_pr = solved_badge().move_to(prediction[0].get_corner(UR))
self.play(
    GrowFromCenter(badge_p), GrowFromCenter(badge_pr),
    rate_func=overshoot, run_time=0.5,   # a small overshoot "stamp" feel
)
```

- Filled green disc + a crisp cream/white check = the universal "verified/done" affordance; it
  reads in a glance and won't be mistaken for a fold.
- Use round caps/joins if available (`chk.set_stroke(..., )` + ManimGL `flat_stroke=False`) for a
  softer tick; the proportion fix matters more than caps.
- Keep `set_opacity(0.65)` dimming in Beat 2 — just dim the whole badge `VGroup`, not a bare stroke.

> Optional nicety: a tiny `Flash` *inside* the disc color is fine, but the grow-stamp alone already
> looks finished. Drop the big external `Flash(line_length=0.25)` that currently fires on the thin V.

---

## Minor

- The nested look (bright `ACCENT_TEAL` outer card + `PASTEL_TEAL` inner panel + glyph gradient)
  is a touch muddy. If you drop the glyphs (Option A), consider a single flat `PASTEL_TEAL` fill so
  the cards read as clean tiles.
- After these fixes, dimming in Beat 2 should target the badge `VGroup`s (rename `chk_perc/chk_pred`
  → `badge_p/badge_pr`) at lines 180–181 and the `_close()` extras at line 240.

## Re-render & check
```bash
cd "/Users/phu-quynguyen-lam/o D/Beyond_SelfDriving"
PYTHONPATH="$PWD" /Users/phu-quynguyen-lam/miniforge3/envs/manim/bin/manimgl \
  -w -l studio/scenes/part02/p02_s11c_planning_pivot.py P02S11CPlanningPivot
```
Spot-check the Beat 1 frame (~3.5 s): the two cards should read clearly as Perception/Prediction
(label-only or with legible glyphs), and each badge should look like a filled green "done" stamp —
**not** a folded corner.
