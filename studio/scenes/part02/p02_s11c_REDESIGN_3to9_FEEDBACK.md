# Comprehensive Redesign — P02S11CPlanningPivot (current ≈3/10 → target 9/10)

Scene: [p02_s11c_planning_pivot.py](p02_s11c_planning_pivot.py). Reviewed full render (frames
t ≈ 2.5 / 6 / 9 / 12 s). The badges got fixed — but the scene as a whole now reads as **flat
PowerPoint SmartArt**: two empty neon boxes, a clip-art stick figure, ghost-grey arrows, and a
clashing palette, with no depth or composition. This file is a top-to-bottom rebuild, not a patch.

---

## Why it's a 3/10 right now (root causes)

1. **Two big EMPTY neon-teal boxes.** Dropping the glyphs left the Perception/Prediction cards as
   large, saturated cyan rectangles with *nothing inside*. Empty boxes read as **unfinished /
   placeholder**, and `PASTEL_TEAL (#99F6E4)` is a cold near-neon that **fights the warm cream
   `BG_PAPER (#FFF9E6)`**. This is the single ugliest thing on screen.
2. **Palette clash & no system.** Neon teal pair + amber Planning card + cream BG = three unrelated
   temperatures. Nothing ties them together.
3. **Ghost arrows.** `LINE_ARROW` dimmed to 0.65 → pale grey arrows that look washed-out and
   accidental, not like "inputs flowing into planning."
4. **Clip-art stick figure.** `pedestrian_icon` is a thin orange stick man — childish next to the
   editorial serif title. It floats to the *right* of Planning, unmotivated and asymmetric.
5. **The "safe path" doesn't read.** The thin green squiggle near the stick figure has no legible
   relationship to it — you can't tell the path is *avoiding* a person. The emotional payoff
   ("stake a life on") lands on a stick figure + a wiggle.
6. **Flat & depthless.** No glow, shadow, ground, or hierarchy. The rest of the studio (loss
   landscapes, RiskMap) has gradients, glows, depth; this scene looks primitive beside them.
7. **Lopsided composition.** Top-heavy empty boxes in Beat 1; Planning + figure + hook crammed
   bottom-right in Beat 3. No balance, no focal hero.

---

## The redesign concept (one coherent picture)

> **"Two confident *understanding* tiles flow down into a single glowing *Planning* node — which
> opens onto a road where one human stands in the path. The plan must choose the trajectory that
> keeps them safe."**

Everything sits on a **faint road** that foreshadows RiskMap, so this bridge visually *becomes* the
next scene. Planning is the **hero** (glowing, warm, central); Perception/Prediction are calm,
solved, secondary. The human is a clean silhouette, centered in the path, with a deliberate safe
corridor curving around them.

---

## Element-by-element fixes

### 1. Palette — soften and unify (highest impact)
Stop using raw `PASTEL_TEAL` as a fill. Pull every tint toward the cream so cards sit *in* the world:

```python
def tint(base, amt=0.58):           # amt toward BG_PAPER
    return interpolate_color(base, BG_PAPER, amt)

TEAL_TILE  = tint(PASTEL_TEAL, 0.55)   # gentle pale teal, not neon
BLUE_HERO  = tint(PASTEL_BLUE, 0.30)   # warmer, brighter than the pair = hero
```

- Perception/Prediction: `fill=TEAL_TILE`, `stroke=ACCENT_TEAL` (width 2.5). Calm, recessive.
- Planning: `fill=BLUE_HERO` (or a soft amber `tint(PASTEL_AMBER,0.25)`), `stroke=ACCENT_BLUE`
  width 3.5 + a glow (below). It should be visibly *warmer/brighter* than the pair.

### 2. Cards must never be empty — put a refined glyph + label INSIDE
Empty tiles are the core problem. Two acceptable directions; pick one and execute it cleanly:

**(a) Compact labeled chips with a small icon** (simplest, very clean): shrink the cards, move the
label *inside* the card, and add one small refined icon above the label. No big empty area exists.

**(b) Proper glyphs** (more informative): keep larger cards but fill them with legible marks:

```python
# Perception: origin dot + outward fan + 2 detected blips (fan points UP/out, not a down-wedge)
def perception_glyph(c=ACCENT_TEAL):
    src = DOWN * 0.34
    fan = sensor_cone(src, color=c, spread=PI/2.2, length=0.85, n_levels=5)
    fan.rotate(PI/2, about_point=src)
    blips = VGroup(Square(0.13), Square(0.11)).set_fill(c,1).set_stroke(width=0)
    blips[0].move_to(UP*0.06+LEFT*0.24); blips[1].move_to(UP*0.20+RIGHT*0.22)
    return VGroup(fan, Dot(src, radius=0.05, color=c), blips)

# Prediction: now-dot -> solid curve -> dashed future -> ghost endpoint
def prediction_glyph(c=ACCENT_TEAL):
    pts = [LEFT*0.42+DOWN*0.10, LEFT*0.04+UP*0.12, RIGHT*0.42+UP*0.04]
    known  = VMobject().set_points_smoothly(pts[:2]).set_stroke(c, 3.5)
    future = DashedVMobject(VMobject().set_points_smoothly(pts[1:]), num_dashes=7).set_stroke(c,3.5)
    ghost  = Dot(pts[-1], radius=0.07, color=c, fill_opacity=0.35).set_stroke(c,1.5)
    return VGroup(known, future, Dot(pts[0], radius=0.06, color=c), ghost)
```

Size the glyphs to ~60% of the inner area so they read but don't crowd. **Recommend (a) for speed,
(b) if you want the cards to carry meaning.** Either way: no empty box ships.

### 3. Arrows — confident, colored, with flow
Replace pale grey ghosts with tapered arrows tinted from teal→blue, plus a one-shot flow pulse:

```python
arrow = Arrow(start, end, thickness=3.5, color=ACCENT_TEAL, buff=0)
arrow.set_opacity(0.9)
# flow pulse along it as it appears:
self.play(ShowCreation(arrow), ShowPassingFlash(
    arrow.copy().set_stroke(ACCENT_TEAL, 6, 1.0), time_width=0.5), run_time=0.9)
```

Do **not** dim them to 0.65 in Beat 2 — keep them ~0.8; only dim the *pair cards* to push them back.

### 4. Planning = the hero node (glow + scale)
Give it presence:

```python
glow = ambient_glow(planning[0], color=ACCENT_BLUE, radius=1.4)   # soft halo behind
self.add(glow); self.play(FadeIn(glow), FadeIn(planning))
```

Make it ~15% larger than the pair, `?` in `ACCENT_BLUE` (`SIZE_HERO`). Keep a *gentle* breathe
(amplitude 0.02, not 0.038 — current one is too jiggly).

### 5. Replace the stick figure with a clean silhouette
`pedestrian_icon` is the second-worst element. Use a filled, editorial human:

```python
def human_silhouette(color=INK_MID, h=0.95):
    head = Circle(radius=0.12*h).set_fill(color,1).set_stroke(width=0)
    body = Polygon(                      # tapered torso "bowling-pin"
        LEFT*0.16*h+DOWN*0.55*h, RIGHT*0.16*h+DOWN*0.55*h,
        RIGHT*0.10*h+UP*0.18*h, LEFT*0.10*h+UP*0.18*h
    ).round_corners(0.06).set_fill(color,1).set_stroke(width=0)
    head.next_to(body, UP, buff=0.02)
    return VGroup(body, head)
```

Render it in a warm, human tone (`GOLD_KEY` or `ORANGE_INFRA`) at a calm size, **standing in the
path**, centered, not floating to the side. Add one soft `ambient_glow` ring + a single slow pulse
on the hook line — restraint.

### 6. Make "safe" legible — a corridor that visibly bends around the human
A bare thin line doesn't say "safe." Borrow RiskMap's corridor (wide translucent band + crisp
center line) and route it **clearly clear of** the human, with a small danger ring on the human so
the avoidance is obvious:

```python
band   = VMobject().set_points_smoothly(path_pts).set_stroke(GREEN_FIX, 30, 0.16)
center = VMobject().set_points_smoothly(path_pts).set_stroke(GREEN_FIX, 4.0, 0.95)
hazard = Circle(radius=0.5, color=RED_ERROR).set_stroke(RED_ERROR, 2, 0.5).set_fill(RED_ERROR,0.06)
hazard.move_to(human.get_center())
```

The green corridor sweeping *around* a red hazard ring around the person = "the plan keeps them
safe" at a glance. This also pre-echoes RiskMap's exact visual language (green corridor + risk
rings) → a seamless handoff.

### 7. Ground everything on a faint road (cohesion + RiskMap rhyme)
Add `road_grid_2d(width=10, height=3)` at very low opacity beneath the Planning→human tableau, or a
single soft horizon line. It unifies the lower third and makes the cut into RiskMap feel like the
camera simply pushing into the same road.

### 8. Composition & depth
- **Center the Beat-3 tableau** (Planning node left-of-center, corridor sweeping right around the
  centered human). Kill the right-side float.
- Add a subtle **drop shadow** behind each card (a slightly offset, blurred dark rounded rect at
  ~8% opacity) for depth, or at least the glow on the hero.
- Consistent corner radius and stroke weights; labels tightly coupled to (or inside) their cards.

---

## Revised beat sequence

1. `self._open("From Understanding to Planning")`.
2. **Beat 1:** faint road fades in low. Perception + Prediction tiles (soft teal, glyph inside)
   `LaggedStart` in → solved badges *pop* (grow+overshoot). Calm, confident.
3. **Beat 2:** hero Planning node fades in with glow, `?` in blue, gentle breathe → two **colored
   flow arrows** pulse down into it → pair dims to push hero forward.
4. **Beat 3:** human silhouette stands on the road ahead; a **green corridor** sweeps from Planning
   *around* a red hazard ring on the human → chiseled hook (`GOLD_RICH` italic) → one slow pulse.
5. Hold → `self._close()` (optional: push the road/corridor toward frame bottom as a match-cut into
   RiskMap).

---

## Implementation checklist

- [ ] Add `tint()` helper; replace all `PASTEL_TEAL` fills with `TEAL_TILE`; hero uses `BLUE_HERO`.
- [ ] No empty cards — glyph-inside (option a or b); never ship a bare box.
- [ ] Colored, pulsed arrows; stop dimming them below ~0.8.
- [ ] `ambient_glow` behind Planning; gentler breathe (amp 0.02).
- [ ] Replace `pedestrian_icon` → `human_silhouette`; center it; warm tone.
- [ ] Green **corridor (band+center)** bending around a red **hazard ring** on the human.
- [ ] Faint `road_grid_2d` ground; centered Beat-3 tableau; add card shadow/glow for depth.
- [ ] Design rules: `BG_PAPER`, ends on `_close()`, English-only, colors imported, no curly quotes.

## Render & review
```bash
cd "/Users/phu-quynguyen-lam/o D/Beyond_SelfDriving"
PYTHONPATH="$PWD" /Users/phu-quynguyen-lam/miniforge3/envs/manim/bin/manimgl \
  -w -l studio/scenes/part02/p02_s11c_planning_pivot.py P02S11CPlanningPivot
```
9/10 bar: (a) no empty neon boxes — tiles read as finished, warm, glyphed; (b) Planning is the
obvious glowing hero; (c) the human is a clean silhouette with a green corridor visibly curving
around a red hazard ring; (d) everything sits on a faint road that flows into RiskMap.
