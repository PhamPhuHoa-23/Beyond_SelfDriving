# Feedback (adversarial) — P05S06ACityWalker after Gemini's implementation

Scene: [p05_s06a_citywalker.py](p05_s06a_citywalker.py) (595 lines). Reviewed the full 23.1 s render
frame-by-frame at t ≈ 1.5 / 3 / 4.5 / 6 / 7.5 / 9 / 10.5 / 12 / 13.5 / 15 / 16.5 / 18 / 19.5 / 22 s.
Adversarial pass — listing everything, worst first. The plan's *structure* came through (6 beats,
props, count-up, PedGen bridge), but the *execution* has one scene-wide bug and several broken beats.

---

## CRITICAL — visible in (almost) every frame

### C1. A stray green box is welded to the left edge for the entire scene
In **every** frame from t≈1.5 s to the end there's a green rounded box half-clipped off the **left
canvas edge**. Root cause is exact:

```python
# Beat 0 — the "simulation solved ✓" card is shoved off-screen but never removed
sim_group.animate.shift(LEFT * 8),     # line 232
```

`sim_group` (a `PASTEL_GREEN` card, [lines 212–217](p05_s06a_citywalker.py#L212-L217)) is *translated*
8 units left — landing at x ≈ −7, just past the safe edge (−6.5) — and is **never faded or removed**,
so it parks there, clipped, for all 23 s. It's the single most unprofessional thing on screen.
**Fix:** `FadeOut(sim_group, shift=LEFT*0.5)` (or add `sim_group` to a later FadeOut / `self.remove`),
not an off-canvas shift.

---

## MAJOR — broken or empty beats

### M1. Beat 2 "reveal" plays to an empty panel
At t≈10.5 the caption `real pedestrian trajectories in context` is up, but the panel is **empty** —
no trajectories, just a stray dark blob + the car. The context-aware paths (the entire payoff of this
beat, and the contrast against Beat 1) don't appear until ~13 s. So the "reveal" reveals nothing for
~2 s. **Fix:** start the trajectory `TracedPath` growth *with* the caption; never hold an empty panel
under a "here are the trajectories" title.

### M2. An unexplained dark rounded rectangle sits on the road through Beats 2–4
A tall dark rounded rect (looks like a phone/obstacle) sits mid-panel on the road from t≈7.5 through
t≈16.5 with **no label and no explanation**. The Beat-1 mocap figure is faded at
[lines 356–360](p05_s06a_citywalker.py#L356-L360), so this is either a leftover or an unlabeled
obstacle. Either way it reads as a stray blob. **Fix:** if it's an obstacle a ped should avoid, style
+ label it as one; if it's a leftover, remove it.

### M3. Beat 1's void is grossly unbalanced
At t≈3 the "isolated mocap" void is a **huge dark navy panel** with a **tiny** skeleton tucked in the
**bottom-left corner**, while the right ~60 % of the canvas is empty cream (plus the C1 green box).
The figure is lost; the dark mass dominates nothing. **Fix:** shrink the void (or enlarge/center the
mocap figure), and balance the frame — the figure walking in a featureless void is the point, so make
*it* the focal element, not a corner detail.

### M4. Beat 4 numbers are washed-out / low-contrast
At t≈16.5 the count-up values (`6.5h`, `25,377`, `3,403`, `47` mid-count) render **pale and barely
legible** on the cards. This is very likely the same class of bug as the earlier MetaUrban `SEED`
chip: a live-updating number (`ValueTracker`/`DecimalNumber`, often via `always_redraw`) bypasses
`StudioScene._force_text_contrast` and gets the ManimGL white-on-cream treatment. **Fix:** force the
number's fill each update — `.set_fill(<accent>, opacity=1).set_stroke(width=0)` — or call
`_force_text_contrast` on the rebuilt number; verify the final values read at full contrast.

---

## MODERATE — composition & polish

### P1. Beats 4–5 leave huge dead space
In Beat 5 the `training signal → PedGen` bridge sits in the **lower third** (`DOWN*0.5`,
[lines 546–574](p05_s06a_citywalker.py#L546-L574)) with the **entire top two-thirds empty** (t≈22).
Centre the bridge vertically (or frame it) so the final hand-off doesn't look like it slid to the
bottom of an empty page.

### P2. The Beat-3 → Beat-4 panel shuffle is abrupt
Going from the full-width panel (Beat 3) to the shrunk-and-shifted panel + metric stack (Beat 4),
the panel jumps in scale/position. Verify it eases smoothly rather than popping.

### P3. Beat 1 warnings overlap
At t≈7.5 two red `⚠` triangles stack on/near the mocap figure — busy and ambiguous. Space them at the
actual violation points (wall hit, obstacle clip, jaywalk) so each ⚠ reads as one specific failure.

### P4. Minor reads
- The mocap "skeleton" (dots around a stick figure) reads as a dot cluster, not clearly *motion
  capture*; consider a clearer skeleton or a "recording in a void" cue.
- The building blocks are empty pale rectangles — fine, but they don't clearly say "buildings."
- Behavior props (stroller/camera/phone/speech) in Beat 3 actually land well — keep them.

---

## What works (keep)
- Beat 3 (diversity) is the strongest: pedestrians with **stroller / camera / phone / speech** props +
  staggered tags reads clearly.
- The PedGen bridge **does** complete by t≈22 (`training signal → PedGen / Behavior Model`) — good
  hand-off, just mistimed/low in the frame (P1) and the screenshot at 19.5 caught it mid-build.
- Count-up metrics with per-card motifs (play / dots / scenes / globe) is the right idea once the
  contrast (M4) is fixed.

## Priority order
1. **C1** — stop shifting the "simulation solved" card off-canvas; fade it (one line). Fixes every
   frame.
2. **M2** — remove/clarify the stray dark rectangle on the road.
3. **M1** — sync Beat 2's trajectory reveal to its caption (no empty panel).
4. **M4** — force contrast on the count-up numbers.
5. **M3 / P1** — rebalance Beat 1's void and centre the Beat 5 bridge.

## One-line summary
The plan landed but the build is buggy: a **"simulation solved" card is shoved off-screen-left and
never removed, so a clipped green box haunts all 23 s** (one-line fix); the **Beat-2 reveal shows an
empty panel** because the trajectories come ~2 s late; a **stray dark blob** lingers on the road; the
**Beat-4 numbers are washed out** (the `always_redraw`/contrast quirk again); and **Beat 1's void and
Beat 5's bridge are badly unbalanced**. Fix C1 first, then resync Beat 2 and de-clutter the road.
