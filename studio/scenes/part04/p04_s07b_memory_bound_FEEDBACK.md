# Feedback — P04S07BMemoryBound ("memory-bound, not compute-bound" + 4× INT8)

Scene: [p04_s07b_memory_bound.py](p04_s07b_memory_bound.py), full `construct`, lines **73–332**.
Reviewed by extracting frames at t ≈ 2.5 / 5 / 7.5 / 9.5 / 11.5 / 14.5 s from
`videos/P04S07BMemoryBound.mp4` (15.2 s, rendered 15:35), plus zoomed crops of the DRAM box and the
MAC core.

Narration this scene serves:

> "…inference on edge hardware is **memory-bound, not compute-bound**… Reducing the bit-width of
> weights from 32-bit float to 8-bit integer **cuts the memory footprint by 4×**, **replaces
> multiplications with cheaper integer additions**…"

The content is all there — DRAM→funnel→starving core (memory-bound), a 32-vs-8 cell strip (4×), and a
×-vs-+ arithmetic row. The **idea is sound and on-script**; the problems are execution: two real bugs
and several legibility issues that make it look unfinished. Below: bugs first (with root causes),
then layout, then composition.

---

## Bugs (must fix — these are why it looks broken)

### Bug 1 — a green block is stranded on top of the "DRAM (off-chip)" label

In every frame from t≈9.5 s on, "DRAM (off-chip)" reads `DRAM▮ff-chip)` — a small green block sits
permanently on the label (confirmed in the DRAM crop). Root cause:

```python
# line 235 — Transform pulls blk2 to green_blocks[0]'s position…
Transform(fp32_blocks[2], green_blocks[0]),
```

`green_blocks[0]` is created at `dram_box.get_center()` ([line 231](p04_s07b_memory_bound.py#L231)),
so this Transform yanks `fp32_blocks[2]` **back up to the DRAM box** (a weird backwards motion), turns
it into a small green block, and then **never moves or fades it again** — the later animations
([lines 246–282](p04_s07b_memory_bound.py#L246-L282)) only touch `green_blocks[0..3]`, not
`fp32_blocks[2]`. So it's stranded on the label forever.

**Fix** — don't Transform the leftover red block onto DRAM. Fade it out and bring the four green
blocks in **at the neck**, where the fast INT8 flow is supposed to start:

```python
# spawn green blocks near the neck, not at DRAM centre
for i in range(4):
    g_blk = RoundedRectangle(width=0.22, height=0.16, corner_radius=0.03)
    g_blk.set_fill(GREEN_FIX, opacity=0.9).set_stroke(GREEN_FIX, width=0)
    g_blk.move_to([left_center_x, 0.7, 0])      # at the funnel mouth, not [dram]
    green_blocks.add(g_blk)

self.play(
    FadeOut(fp32_blocks[2], scale=0.6),          # retire the last red block cleanly
    *(FadeIn(g, scale=0.6) for g in green_blocks),
    run_time=0.5,
)
```

### Bug 2 — the MAC core's text turns muddy green and goes low-contrast

After the core "activates," `MAC` / `compute core` render as a muddy green smudge (see core crop).
Root cause:

```python
# line 261 — set_stroke on the whole VGroup hits the text too
core.animate.set_stroke(GREEN_FIX, width=2.4),
```

`core` is `VGroup(pins, body, copy)` ([line 66](p04_s07b_memory_bound.py#L66)), so `set_stroke` on it
strokes the **title and subtitle text** green as well as the body — that's what muddies "MAC compute
core." Target only the body rectangle:

```python
core_body = core[1]                              # VGroup(pins, body, copy) → body is index 1
self.play(core_body.animate.set_stroke(GREEN_FIX, width=2.4), ...)
```

(Same applies anywhere you recolor `core` — only touch `core[1]`.)

---

## Layout / legibility

### 3. Red blocks collide with the "MEMORY BANDWIDTH" label

During the FP32 beat the queued blocks sit at y = 0.7 / 1.2
([lines 144–145](p04_s07b_memory_bound.py#L144-L145)) while `funnel_lbl` is at y = 1.1
([line 112](p04_s07b_memory_bound.py#L112)) — so the blocks pass straight through the text (at t≈2.5
it reads "MEMORY ▮ DWIDTH"). Move the label **out of the flow path**: either above the funnel mouth
(y ≈ 1.95, beside DRAM) or rotated 90° and set along one funnel wall as an axis label. The flow
column (x = left_center_x) must stay clear.

### 4. Blocks spawn on top of the DRAM label

`blk.move_to(dram_box.get_center())` ([lines 137, 231](p04_s07b_memory_bound.py#L137)) starts every
block on "DRAM (off-chip)". Spawn them at the box's bottom edge so they emerge *from* DRAM rather than
over its text: `blk.move_to(dram_box.get_bottom() + DOWN * 0.12)`.

### 5. The funnel doesn't read as a funnel / bottleneck — the core metaphor is the faintest thing on screen

The whole left-column point is "a **narrow bandwidth neck** starves a fast core." But:
- The walls are `LINE_SEP` (very light grey) at width 2.4 ([line 110](p04_s07b_memory_bound.py#L110))
  — they nearly vanish on the cream background. The neck (the bottleneck!) carries no emphasis.
- The walls **end at y = −1.2** ([lines 101, 107](p04_s07b_memory_bound.py#L101)) but the core is at
  y = −2.1 ([line 116](p04_s07b_memory_bound.py#L116)), so blocks travel ~0.9 units through empty
  space below the neck — the channel visually disconnects from the core.

**Fix:** give the **neck** a stronger, warmer stroke (e.g. `ACCENT_AMBER` or `INK_MID`, width ~3),
extend the neck walls down to the core's top edge so the channel is continuous, and tag the neck with
a small `BANDWIDTH LIMIT` / `← narrow →` cue so the constriction *is* the message. Optionally widen
the funnel mouth vs. neck ratio so the pinch is obvious.

---

## Composition / storytelling

### 6. The left column dies after its beat
Once INT8 kicks in, the left is frozen (ACTIVE core + the Bug-1 stray block) while the right keeps
building the arithmetic row. The funnel's payoff — green blocks streaming *fast* through the neck — is
over in a flash. Either keep a subtle looping green flow through the neck during the right-column
beats, or resolve the left to a clean "solved" state (green neck, calm core, **no** stray block) so it
reads as finished, not abandoned.

### 7. "memory-bound vs compute-bound" is only shown as half the contrast
The script's hook is "memory-bound, **not** compute-bound." The visual nails *memory-bound* (starving
core) but never says what compute-bound would look like, so the "not" half is implicit. A one-beat cue
helps: e.g. the core briefly shows "compute: ready/fast" while the neck throttles it — "the core isn't
the problem, the pipe is."

### 8. The two halves (funnel ↔ bit-strips) are only loosely linked
The left "red block shrinks to 4 green blocks" and the right "FP32 strip → INT8 strip (4× shorter)"
are the *same* fact shown twice. Sync them: trigger the right-column INT8 strip reveal **at the same
moment** the left blocks shrink to green, so the viewer reads "8-bit = smaller = flows faster" as one
event instead of two separate animations.

### 9. Minor
- The multiply glyph is a lowercase `x` in a circle ([line 292](p04_s07b_memory_bound.py#L292)) — use
  `×` (`×`) so it reads as "multiply," not the letter x.
- "FP32: Multiplications / INT8: Additions" is faithful to the narration but is a simplification
  (INT8 still multiply-accumulates; it's just cheaper integer math). Fine to keep for the script, but
  if you want to be defensible, "INT8: cheap integer ops" avoids overclaiming. (Low priority.)
- Right column has a tall empty gap between WEIGHT PRECISION (top) and ARITHMETIC SIMPLIFICATION
  (lower third). Tighten the vertical rhythm or raise the arithmetic block so the column reads as one
  unit.

---

## What's already good (keep)
- The DRAM → bandwidth neck → compute-core metaphor is the right mental model for memory-bound.
- The **32-cell vs 8-cell** strip with a 4× length difference is an accurate, instantly-readable "4×
  footprint" visual, and the `4x smaller memory footprint` note is well placed.
- Red = slow/expensive → green = fast/cheap is consistent across blocks, strips, ops, and the
  IDLE→ACTIVE status flip — good semantic coding.

## Priority order
1. **Bug 1** (stray DRAM block) and **Bug 2** (green core text) — both are one-line fixes and both are
   the things that make the frame look broken.
2. Move the two labels out of the flow path (Issues 3–4).
3. Make the funnel neck actually read as a bottleneck and connect it to the core (Issue 5).
4. Polish: sync left/right INT8 reveal, keep the left alive, `×` glyph, vertical rhythm (Issues 6–9).

## One-line summary
On-script and well-conceived, but a **stray green block is welded to the DRAM label** and the
**MAC text is accidentally stroked green** (both one-line bugs), the **flow runs through two text
labels**, and the **bandwidth neck — the actual metaphor — is the faintest, most disconnected element
on screen**. Fix the two bugs, clear the flow lane, and make the neck read as a real bottleneck, and
this becomes a clean, convincing memory-bound explainer.
