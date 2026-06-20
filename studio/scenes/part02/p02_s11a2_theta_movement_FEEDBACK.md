# Feedback #2 — the θ "movement" (thrash-in-place) in Beat 2

Scene: [p02_s11a2_root_causes.py](p02_s11a2_root_causes.py), lines **369–403** (the zigzag trail +
park). The earlier rebuild (θ at center, gradients from θ, tip-to-tail ghost chain, red
"net step ≈ 0") landed well. The remaining weird part is exactly the bit the user flagged: **the
moment θ moves.** Reviewed by extracting frames t ≈ 20.3 → 23.0 s.

---

## What the movement actually draws (and why it looks wrong)

The trail steps cycle det → pred → plan **in the same order, same directions, every loop**:

```python
det_vec  = (1.0, 1.4);  pred_vec = (1.1, -1.2);  plan_vec = (-1.8, -0.1)
p1 = p0 + det*0.5;  p2 = p1 + pred*0.5;  p3 = p2 + plan*0.5      # cycle 1
p4 = p3 + det*0.45; p5 = p4 + pred*0.45; p6 = p5 + plan*0.45     # cycle 2
p7 = p6 + det*0.35; p8 = p7 + pred*0.35; p9 = p8 + plan*0.35     # cycle 3
```

Because `det + pred + plan = (0.3, 0.1)` (≈0), each cycle **returns near its start**, and since the
three directions never change, the path is a **clean, regular triangle traced three times**,
shrinking slightly each loop (step 0.5 → 0.45 → 0.35). Frames 22.1–22.7 show exactly this: a tidy
black triangle, not a scribble.

That produces four problems:

1. **A neat triangle reads as the *opposite* of "stuck."** The point of this beat is *SGD flails and
   makes no progress*. A clean, repeating triangle looks like deliberate, elegant periodic motion —
   it looks *intentional and under control*, not chaotic or futile. The visual says the wrong thing.

2. **It's the same triangle the viewer just saw.** The tip-to-tail ghost chain (det→pred→plan,
   lines 308–339) already drew this exact triangle to demonstrate "sum ≈ 0." The trail now redraws
   the same shape. The viewer thinks "why is it tracing that triangle again?" — redundant, and it
   muddies the two distinct ideas (cancellation vs. no-progress-over-time).

3. **Scale mismatch — the trail shoots outside the cluster.** By line 369 the gradient arrows have
   been shrunk to 0.35 stubs (lines 360–363), but the trail still uses full-size `det_vec*0.5`
   (~0.85 units/step). So the triangle is ~2.4× larger than the stubs and juts far up-right, visually
   detached from θ (frames 22.1–22.7). Then line 401 scales the whole group by 0.62, so the giant
   triangle suddenly snaps smaller — a second jarring scale jump.

4. **θ renders as a white/uncolored dot while moving** (frames 21.8–22.7 show a white blob at the
   moving tip, not an `INK_DARK` dot). Looks like a stray glyph / missing fill.

---

## Recommended fix

The deeper issue is that **the trail duplicates the ghost chain and a tidy triangle can't express
"no progress."** Two clean ways out — pick one:

### Option A (preferred): cut the literal trail; show "no progress" as jitter + a step counter
The tip-to-tail chain + red "net step ≈ 0" stub already prove the gradients cancel. To express
"…and this keeps happening, step after step, going nowhere," don't re-trace geometry — show *time
passing with no descent*:

- Keep the 3 gradient stubs + red net stub parked at θ.
- Make θ **jitter in a tiny region** around its start (small random `shift`s, amplitude ≈ stub
  length × 0.3, ~12–16 quick steps), leaving a faint short scribble that **never leaves the
  cluster**. Crucially keep amplitude *small* and the order *shuffled* so it reads as restless
  noise, not a shape.
- Overlay a ticking counter, e.g. `steps: 50 … 200 … 800` (`SIZE_CAPS`, `INK_MID`) that climbs while
  θ stays put. The contrast "counter goes up, θ goes nowhere" *is* the message, and it doesn't
  redraw the triangle.

### Option B: keep a trail, but make it a genuine tangle at stub scale
If you want to keep a visible path:

- **Shuffle the order and add noise** so it's not a regular triangle: each step picks det/pred/plan
  in randomized order with a small random magnitude (e.g. `base * np.random.uniform(0.25, 0.6)`),
  ~15–20 steps. The result is a self-crossing knot, not a polygon.
- **Match scale:** draw the trail *after* the stubs are shrunk, using step sizes relative to the
  **stub** length (≈0.35× vec), so the knot stays inside the θ cluster and never juts out.
- **Don't rescale afterward:** build Beat 2 already at its parked size/position from the start (set
  `theta_center` to the final parked spot and size the vecs for that), then drop the line-401
  `.scale(0.62)` entirely. One scale, no snap.
- Ensure net displacement ≈ 0 (knot ends where it began) so the green chip's "no progress" reads.

### Either option, also fix:
- **θ color:** rebuild/repin θ as an `INK_DARK` dot for the move (it's rendering white). If it's the
  white-contrast quirk, route it through `self.add`/`self._force_text_contrast` or re-`set_fill`
  after the move. Verify it stays dark in the parked frame.
- **Avoid the double scale jump:** prefer building Beat 2 at final scale (Option B bullet) so there's
  no full-size→0.62 snap at line 401 regardless of which option you choose.

---

## Concrete sketch (Option A, minimal change)

Replace lines 369–396 with something like:

```python
# θ jitters but never descends — many steps, no net motion
rng = np.random.default_rng(2)
trail = VMobject(stroke_color=INK_LIGHT, stroke_width=2.0)
trail.set_points_as_corners([theta_center])
cur = theta_center.copy()
amp = 0.18  # small: stays inside the stub cluster
counter = _txt("steps: 50", size=SIZE_CAPS, color=INK_MID)
counter.next_to(theta, DOWN, buff=0.5)
self.add(trail); self.play(FadeIn(counter), run_time=0.3)
for k, n in enumerate([50, 120, 250, 480, 800]):
    nxt = theta_center + rng.uniform(-amp, amp, size=3) * np.array([1, 1, 0])
    seg = Line(cur, nxt, stroke_color=INK_LIGHT, stroke_width=2.0)
    new_counter = _txt(f"steps: {n}", size=SIZE_CAPS, color=INK_MID).move_to(counter)
    self.play(theta.animate.move_to(nxt), ShowCreation(seg),
              Transform(counter, new_counter), run_time=0.3, rate_func=linear)
    trail.add(seg); cur = nxt
self.play(theta.animate.move_to(theta_center), run_time=0.25)  # ends where it started
self.wait(0.4)
```

Then keep θ visibly `INK_DARK`, fold `counter` into the park/closing fade, and drop the redundant
triangle entirely. (If you keep the park scale at line 401, add `counter` to `beat2_group` or fade
it first.)

## Re-render & check
```bash
cd "/Users/phu-quynguyen-lam/o D/Beyond_SelfDriving"
PYTHONPATH="$PWD" /Users/phu-quynguyen-lam/miniforge3/envs/manim/bin/manimgl \
  -w -l studio/scenes/part02/p02_s11a2_root_causes.py P02S11A2RootCauses
```
Check the move specifically: (a) θ stays a dark dot; (b) its path stays *inside* the gradient
cluster and does **not** form a clean triangle; (c) no sudden scale snap when it parks; (d) the
"no progress" idea is legible without narration.
