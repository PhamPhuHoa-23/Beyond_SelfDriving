# Visual Improvement Plan — P01S03CHybrid ("Hybrid Systems")

Scene file: [p01_s03c_hybrid.py](p01_s03c_hybrid.py)
Narration (target): *"Hybrid architectures occupy the middle ground. Machine learning handles
perception and high-level planning where it excels. Classical, verifiable control modules handle
the actuators where reliability matters most. Many leading companies are converging on this design
because it balances learning-based adaptability with engineering-grade hardware guarantees. But all
three architectures share a common weakness. Foundation models will make that weakness visible."*

This is the third of the three architecture scenes (modular → end-to-end → hybrid). Its job is to
(1) make the **ML-where-it-excels / classical-where-reliability-matters** split instantly legible,
and (2) land the closing hook that all three share a weakness foundation models will expose.

---

## Problems in the current frame

1. **Cryptic per-row tags.** The `ML` / `Cls` bands left of every block (`_kind_tag`) are small,
   abbreviated ("Cls" is not self-explanatory), and create a ragged left edge. They duplicate
   information the color coding + legend already carry, adding noise instead of clarity.
2. **Legend reads like a bug.** Two rows are both titled **"Classical"** — at a glance this looks
   like a copy-paste error rather than an intentional distinction (estimation vs. control).
3. **Weak color story.** The ML vs. classical split is the whole point, but the pastels
   (`#EDE9FE` lavender vs. `PASTEL_BLUE` vs. `PASTEL_AMBER`) are low-contrast and hard to group at a
   glance. The two ML blocks (Perception, Planning) — the narrative's hero — do not pop.
4. **Dead bottom half.** The stack + legend float in the upper-middle; the lower ~40% of the canvas
   is empty, and the composition sits high and slightly left-heavy.
5. **Punchline is buried.** The closing weakness line is rendered as small, **dimmed** red footer
   text (`place_footer` at `FOOTER_Y = -3.5`) — it looks washed out and cut off, not like a payoff.
6. **Script mismatch.** Code says *"...share one weakness: the long tail."* The new narration drops
   the named "long tail" and instead teases that **foundation models will make the weakness
   visible.** On-screen text should match.
7. **"All three" is unsupported on screen.** The narration says *all three* architectures, but only
   the hybrid stack is shown — nothing recalls modular + end-to-end, so the claim has no visual hook.

---

## Design goals

> **Guiding principle: minimal text.** Let color, position, and motion carry the meaning. Words on
> screen are a last resort — the narration does the talking. Every label below is the *shortest*
> form that still reads, and most are one word or a color swatch.

- The ML/classical split should be readable in **under one second** from color alone.
- The two ML modules are the protagonists — make them visually dominant.
- Balance the composition vertically; use the bottom space for the payoff beat.
- The closing hook is one short line at most — ideally a *visual* cue, not a sentence.

---

## Concrete changes

### 1. Drop the per-row `ML`/`Cls` bands; encode kind in the block itself
Remove `_kind_tag` and the left-of-block tags entirely (kills 5 text labels). Carry "kind" purely
through the block's appearance:

- **ML blocks (Perception, Planning):** stronger purple identity — `PURPLE_MODEL` stroke at
  `stroke_width≈3.5`, lavender `#EDE9FE` fill, plus a subtle outer glow (reuse `ambient_glow` from
  `signals.py`) so they read as "the learning parts."
- **Classical blocks (Localization, Prediction, Control):** keep `PASTEL_BLUE` / `PASTEL_AMBER`
  fills but at thinner, calmer `INK_MID` strokes so they recede relative to the ML blocks.

Color does the grouping; no abbreviations needed. The left edge becomes clean and the eye catches
the two highlighted ML rows immediately.

### 2. Shrink the legend to a compact color key (fewer words)
The current legend is the most text-heavy element and repeats "Classical." Cut it down:

- **Three swatches, one short word each:** purple = **Learning**, blue = **Estimation**,
  amber = **Control**. Drop the second descriptive sub-line entirely (no "Localization · Prediction"
  etc.) — the block names already say which module is which, so the sub-lines are redundant.
- This turns ~9 lines of legend text into 3 words beside 3 swatches, and removes the duplicate
  "Classical" that read like a bug.

> Even lighter option: drop the legend's words too and let the three swatches sit as a bare color
> key — the matching block colors make the mapping obvious. Keep 3 words only if a quick render
> shows the mapping isn't instantly clear.

### 3. No thesis subtitle / no extra captions
Skip any explanatory subtitle under the title. The "learning where it helps, control where it must"
idea is the narration's job, not the frame's. Keep the title (`Hybrid Systems`) as the only header
text.

### 4. Recenter and use the vertical space
- Reduce inter-row `buff` slightly (`0.24 → 0.20`) so the stack is more compact, then center the
  **stack + color key group** vertically in the content zone rather than pinning to the header.
- Reserve the lower third for the payoff beat (see #5).

### 5. Make the payoff visual, not a paragraph
Replace the two-line dimmed footer with **one short beat**:

- After the key lands, **dim the whole stack** (extend the existing `dim` group to all blocks +
  arrows + key, not just `b[0]`) to push it back.
- Bring up a single small `RED_ERROR` mark — prefer a **visual cue over a sentence**: e.g. a thin
  crack/fault line drawn across the dimmed stack, or a small pulsing warning dot, paired with **at
  most three words**: **"One shared weakness."**
- That's the whole payoff. The follow-up idea ("foundation models will make it visible") stays in
  the *narration* and is paid off by the next scene — no second on-screen line needed.

  (If a render shows the beat feels empty without it, add the second line; default is to leave it
  out. Note: drop the old "long tail" wording — the current narration doesn't say it.)

### 6. "All three" — keep it visual and wordless (optional)
If "all three" needs an on-screen referent, use three tiny color chips (no labels) recalling
modular / end-to-end / hybrid — two greyed, one lit — rather than text chips. Optional; skip if it
adds clutter.

---

## Suggested animation sequence

1. `_open("Hybrid Systems")` — title only, no subtitle.
2. `LaggedStart(FadeIn)` the five blocks (no tags). ML blocks fade in **last/brighter** so the eye
   lands on Perception + Planning.
3. `ShowCreation` the vertical arrows.
4. `FadeIn` the compact color key (3 swatches, ≤3 words).
5. Dim stack + arrows + key (`set_opacity(0.42)`).
6. `FadeIn` the payoff: visual mark + "One shared weakness."
7. `self.wait(2)` → `self._close()`.

---

## Implementation checklist

- [ ] Delete `_kind_tag`; remove tag construction from the row loop (−5 labels).
- [ ] Add ML-block emphasis (stroke weight + `ambient_glow`); soften classical strokes.
- [ ] Collapse legend → 3 swatches + ≤3 words; remove duplicate "Classical" and the sub-lines.
- [ ] No subtitle / no extra captions.
- [ ] Recompute layout: center stack+key vertically, reserve bottom third.
- [ ] Replace footer `weakness` Text with a visual mark + ≤3-word line.
- [ ] Extend `dim` group to include all blocks, arrows, and key.
- [ ] (optional, wordless) three color recall chips.
- [ ] Verify against design rules: `BG_PAPER`, no curly quotes, colors imported, ends on `_close()`.

## Render & review

```bash
cd "/Users/phu-quynguyen-lam/o D/Beyond_SelfDriving"
PYTHONPATH="$PWD" /Users/phu-quynguyen-lam/miniforge3/envs/manim/bin/manimgl \
  -w -l studio/scenes/part01/p01_s03c_hybrid.py P01S03CHybrid
# then extract the final-stack frame and the payoff frame to check both beats
ffmpeg -y -loglevel error -ss <t> -i videos/P01S03CHybrid.mp4 -frames:v 1 videos/check.png
```

After the change, update the matching section in `studio_scripts/script_part1.md` if the on-screen
weakness wording changed.
