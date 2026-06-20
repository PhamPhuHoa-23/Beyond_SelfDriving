# Feedback — the redesigned "generator" in P05S04BMetaUrban

Scene: [p05_s04b_metaurban.py](p05_s04b_metaurban.py), `engine()` [lines 99–141](p05_s04b_metaurban.py#L99-L141)
and its `seed_label` [lines 320–335](p05_s04b_metaurban.py#L320-L335). Reviewed from frames t ≈ 5 / 8 s
of `videos/P05S04BMetaUrban.mp4` (22 s), plus a zoom of the centre node.

**Verdict:** the "make it more academic" swap **over-corrected** — it replaced a *generator* with a
literal *textbook probability plot*. A lone Gaussian bell curve in a near-invisible box does not read
as "a machine that turns a script into a city," which is the whole job of that center node. It looks
like a statistics figure was pasted into the middle of a `script → engine → scene` pipeline.

---

## Concrete defects

### 1. The housing is a ghost — the hero node is the faintest thing on screen
`housing` is `fill_opacity=0.08` with a `LINE_SEP` (light-grey) stroke
([lines 100–108](p05_s04b_metaurban.py#L100-L108)). On cream it's barely there. So the **center of the
pipeline** — which should dominate — is a pale, small (1.6×1.6) box that the teal/pink arrows point at
as if it were empty. Hierarchy is inverted: the terminal (left) and the scene tile (right) both read as
solid, the *generator* reads as nothing.

### 2. It reads as a stats diagram, not a generator
The box contains only a **Gaussian PDF curve + x/y axes** ([lines 116–123](p05_s04b_metaurban.py#L116-L123)).
There's no mechanism, no transformation, no sense of *generation*. A bell curve says "here is a
distribution," not "I ingest parameters and emit a scene." For a tutorial audience it's an abstract
motif with no visible link to city blocks / intersections / sidewalks.

### 3. The `SEED:` readout renders white / invisible — and it's a known-cause bug
`seed_label` is declared `color=INK_DARK` but shows up **white** (a pale smudge at the top of the box —
see the zoom). Cause: it's wrapped in `always_redraw(...)` ([lines 321–324](p05_s04b_metaurban.py#L321-L324)),
which **recreates the `Text` every frame**, so `StudioScene._force_text_contrast` (which only runs on
`add()`/`play()`) never touches the regenerated text — exactly the ManimGL "white text on BG_PAPER"
quirk that CLAUDE.md warns about. **Fixes (any one):**
- Don't use `always_redraw` for this. Keep a single `Text`, update only the characters via
  `seed_label.become(make_seed(self.seed_val))` inside an updater **and** call
  `self._force_text_contrast(seed_label)` after building it; or
- Inside the lambda, set the fill explicitly after creation:
  `Text(...).set_fill(INK_DARK, opacity=1).set_stroke(width=0)`; or
- Drop the live hex ticker entirely (it's noise — see below) and show the seed as one static chip.

### 4. The math label is tiny and cryptic
`x ~ p(X | θ)` at `font_size=11` ([lines 130–132](p05_s04b_metaurban.py#L130-L132)) is illegible and
over-mathy. The idea (sample a scene from a parameterized distribution) is *correct*, but as a tiny
formula it explains nothing to a general viewer and clutters the box.

### 5. Nothing actually "generates"
The `laser` sampling line ([lines 125–128](p05_s04b_metaurban.py#L125-L128)) sweeping a static curve is
a weak cue — even animated, a line over a bell curve doesn't show *a scene being produced*. The node
can't visibly transform the script into the output; it just sits there.

### 6. Two competing "random" signals, both weak
A live-ticking hex `SEED: 0x5BE1` **and** a `p(X|θ)` curve both gesture at "randomness," redundantly,
while neither shows generation. The flickering hex in particular reads as a fake-techy ticker, not
information.

---

## Direction: keep "academic," but make it a *generator*

Academic and legible aren't in conflict. The node must visibly **take parameters in and put a scene
out**. Recommended rebuild (this also matches the engine spec already in
[p05_s04b_metaurban_PLAN.md](p05_s04b_metaurban_PLAN.md)):

- **Solid housing.** Real presence: `PASTEL_PINK` fill at ~0.5–0.7 (or a soft card), `ACCENT_PINK`
  stroke ~2px, ~1.8 units. Make it the biggest, most defined node in the row.
- **Show sampling as production, not as a plot.** Keep one small distribution *if you want the academic
  nod*, but make it **do** something: a sample **dot drops from the curve**, slides to the emitter, and
  **becomes the output scene**. Each "generate" → the curve flashes, a new sample drops, a new scene
  exits. That's "sampling from p(X|θ)" shown as *generation*.
- **One readable seed/θ chip**, static per generate (e.g. `θ = seed 0x5BE1`), updated once when a new
  scene is produced — not a per-frame hex flicker. Fix the contrast (above) so it's actually visible.
- **If you prefer the mechanical read:** a clean **engine module** — chunky 8-tooth gear + a rolling
  **seed die** + funnel/emitter (per the PLAN). Pick *one* metaphor (sampler **or** machine); don't
  stack both.
- **Drop or enlarge** the `x ~ p(X|θ)` formula. If kept, make it `SIZE_CAPS`, place it under the box as
  a caption, and let the dropping-sample animation be what explains it.

The test: freeze any frame mid-run and a viewer should think **"that box is building the city on the
right,"** not "that's a graph."

---

## Priority
1. **Fix the white `SEED` text** (the `always_redraw` contrast bug) — it's the most obviously broken
   thing on screen.
2. **Solidify + enlarge the housing** so the generator stops being a ghost.
3. **Make the box visibly produce the scene** (sample-drop → scene), instead of displaying a static
   curve.
4. Replace the flickering hex with one static seed/θ chip; drop or enlarge the tiny formula.

## One-line summary
Gemini turned the generator into a **faint box with a textbook Gaussian** — it doesn't read as a
generator, the **`SEED` text is white/invisible** (an `always_redraw` contrast bug), and the formula is
tiny and cryptic. Make the housing solid and dominant, show **sampling as a dot that drops and becomes
the output scene**, and replace the flickering hex with one readable seed chip — keep the academic
nod, but it has to *generate*, not just *plot*.

---

# Round 2 — the rebuilt generator (solid housing, θ chip, sampling)

The redesign landed well: **solid pink housing**, a readable **`θ = …` chip**, a clean curve, the
`x ~ p(X | θ)` caption, and a sample-drop. The Round-1 problems are fixed. Three new bugs remain,
reviewed from frames t ≈ 15–18 s (the reroll beats).

## Bug 1 (main) — after a reroll, the curve detaches from its axes
The first (centered) curve is perfect: peak on the y-axis, baseline on the x-axis. But the moment the
distribution **rerolls**, the bell sits **below the x-axis with the axis slicing through its middle**,
and looks broken (this is the "bị gì" frame).

**Root cause — wrong origin for the reroll curves.** The axes are built inside `engine()` relative to
the **housing** centre (`chart_origin = DOWN*0.25`, [lines 159–172](p05_s04b_metaurban.py#L159-L172)).
But the reroll curves use:

```python
engine_center = engine.get_center()                 # line 487  ← bounding-box centre
chart_origin_abs = engine_center + DOWN * 0.25      # lines 562, 606
```

`engine.get_center()` is the **bounding box** of the whole VGroup — which includes the
`"Probabilistic Generator"` **label hanging below the housing**, so the box centre is pulled *downward*
from the housing centre. The reroll curves are therefore drawn **lower than the axes**. (The axes don't
move, so the original curve stays aligned and only the rerolls break.)

**Fix — one line.** Anchor the reroll origin to the **housing** (index 0), not the group:

```python
engine_center = engine[0].get_center()              # line 487: housing, not the whole group
```

This corrects `chart_origin_abs` for **both** reroll curves *and* the sample-drop start points
(`start_pt1`, `start_pt2`, which also derive from it). Equivalent alternative:
`chart_origin_abs = engine[1][0].get_center()` (the x-axis line's centre *is* the chart origin).

> Note: the remaining **rightward shift** of the peak in reroll 2 (`narrow_skew`, mean = 0.12,
> [line 605](p05_s04b_metaurban.py#L605)) is the *intended* skew, not a bug. But if an off-axis peak
> reads as "misaligned," either keep the means near 0 and vary the **width** instead, or slide the
> y-axis to the new mean on each reroll.

## Bug 2 — the bimodal curve renders as a jagged, overshooting mess
The `double_peak` reroll ([lines 560–567](p05_s04b_metaurban.py#L560-L567)) is two **sharp narrow**
Gaussians (σ ≈ 0.07–0.08) sampled at only **40 points** and fed to `set_points_smoothly`. Through sharp
peaks that few samples, the smooth Bézier **overshoots** — extra wiggles/spikes and a weird valley — so
it reads as broken rather than as a clean two-hump distribution (the user's second image).

**Fix — pick one:**
- **Simplest:** make reroll 1 a clean **unimodal** with a different mean/width (like reroll 2, which
  renders fine). "Different distribution → different scene" still reads; you don't need bimodality.
- **If you want the two humps:** widen σ to ≥ 0.12 **and** raise the sample count to ~100–120 so the
  smoothing doesn't overshoot; optionally `np.clip(y_val, 0, None)` so it can't dip below baseline.

## Bug 3 — the `θ = 0x…` text garbles during the morph
Mid-transition the chip shows a mashed blob (e.g. `0x?C?B`, t≈18). Cause:
`ReplacementTransform(self.seed_chip, new_chip)` ([lines 577, 618](p05_s04b_metaurban.py#L577))
morphs the **old hex glyphs into different new hex glyphs**, which always interpolates into overlapping
garbage for a few frames.

**Fix — don't morph text-to-text.** Keep the chip **box** static and swap only the **label** with a
clean crossfade:

```python
# keep the box; crossfade the text
self.play(FadeOut(old_text, run_time=0.2), FadeIn(new_text, run_time=0.2))
# or, in one shot:
self.play(FadeTransform(self.seed_chip, new_chip))   # softer than ReplacementTransform for text
```

`FadeTransform`/`FadeOut+FadeIn` cross-dissolves instead of letter-morphing, so no garbled frames.

## Priority
1. **Bug 1** — `engine[0].get_center()` (one line) fixes the misalignment that prompted this review.
2. **Bug 3** — crossfade the seed text instead of `ReplacementTransform`.
3. **Bug 2** — drop the bimodal or widen+resample it.

## Round-2 one-line summary
The generator looks right now; the breakage is **the reroll curves using `engine.get_center()`** (the
group box, dragged down by the label) instead of the **housing** centre, so they fall below the axes —
fix with `engine[0].get_center()`. Also de-jag the bimodal curve and crossfade (don't morph) the
`θ` hex text.
