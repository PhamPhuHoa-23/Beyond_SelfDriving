# Animation Plan — P02S11CPlanningPivot ("From Understanding to Planning")

New scene file: `studio/scenes/part02/p02_s11c_planning_pivot.py`
Class: `P02S11CPlanningPivot(StudioScene)` — **2D scene**, light and short (~13–15 s).

Position in the cut: **between** [p02_s11b_turbotrain_solution.py](p02_s11b_turbotrain_solution.py)
(training solved) and [p02_s12_riskmap.py](p02_s12_riskmap.py) (safe, interpretable planning).
The `s11c` infix sorts the file right after `s11b` and before `s12` in `ls` / the render script —
no existing file needs renaming.

Narration (target — the lead-in the user supplied):

> *"The system can now perceive and predict reliably. The remaining question is: what do we do with
> that understanding? Perception and prediction are inputs to planning — and planning must be safe
> enough to stake a life on."*

This is a **pivot beat**: Part 2 has spent V2XPnP + TurboTrain building reliable *perception and
prediction*; this frame turns the camera toward the one capability still open — *planning* — and
loads it with stakes, so RiskMap arrives as the answer to a question the viewer now feels.

> **Note on overlap:** RiskMap's own opening line ("Perception and prediction enable the vehicle to
> understand the scene. Planning requires using that understanding to make safe decisions…") covers
> the same ground. If this scene ships, trim RiskMap's intro to start at *"And this is where
> interpretability becomes critical"* so the two don't restate each other. Flagged in the checklist.

---

## Design goals

> **Guiding principle: minimal text** (house rule). The whole idea is a 3-node pipeline plus one
> emotional hook. On-screen words: three node labels (**Perception / Prediction / Planning**), and
> the single chiseled hook line. Nothing else — the narration carries the rhetoric.

- The "perception + prediction are *done*" idea reads from a calm, checked, part-2-teal pair.
- "…are inputs to planning" reads as **flow**: two arrows converge into a third node that is visibly
  the *open* one (it's the only node not yet "solved").
- "safe enough to stake a life on" is the payoff — give it a **human** referent and the house-style
  chiseled hook line; do not let it be just text.
- Palette discipline: Part 2 accent `ACCENT_TEAL` for the solved pair, `GREEN_FIX` for the
  solved-checks, `ACCENT_BLUE` for the Planning node (rhymes with RiskMap's ego vehicle so the
  handoff feels continuous), `GOLD_RICH` italic for the hook line (matches the s14 bridge style).

---

## Beat 1 — Perception + Prediction, solved (~4 s)

Narration: *"The system can now perceive and predict reliably."*

- Two `pipeline_block` / `stage_panel` cards side by side, upper-center: **Perception** and
  **Prediction**, `ACCENT_TEAL` stroke on `BG_CARD`. Optionally a tiny glyph inside each (a small
  sensor-cone for Perception, a 2–3-point forecast polyline for Prediction) — keep it ≤ a few
  strokes; labels alone are acceptable if glyphs add clutter.
- After both land, **stamp a `GREEN_FIX` check** on each (a short two-segment `VMobject` drawn with
  `ShowCreation`, or `contribution_badge`-style), with a small `Flash`. This is the "reliably" beat:
  the two upstream capabilities are confidently closed.
- `LaggedStart(FadeIn(perception), FadeIn(prediction))` → then the two checks together.

## Beat 2 — They are inputs to planning (~5 s)

Narration: *"The remaining question is: what do we do with that understanding? Perception and
prediction are inputs to planning."*

- Introduce the third node **Planning** below-center (or right), as the pipeline's sink. Render it
  **differently from the solved pair** so the eye knows it's the open one:
  - `ACCENT_BLUE` stroke, *no* green check, and a single `?` or a hollow/under-construction feel
    (e.g. a dashed inner outline, or it fades in slightly larger and "breathing").
- Draw two `pipeline_arrow` / `h_arrow` flows: Perception → Planning and Prediction → Planning,
  converging. Animate with `ShowCreation`, `LINE_ARROW`/`INK_MID`, so "inputs to planning" is
  literally the picture.
- As the arrows land, **dim the solved pair slightly** (`set_opacity(~0.7)`) and let Planning hold
  full strength + a soft pulse — the question has moved downstream. The "?" sells *"what do we do
  with that understanding?"*

## Beat 3 — Safe enough to stake a life on (~5 s)

Narration: *"…and planning must be safe enough to stake a life on."*

This is the hook; give it a human and weight.

- A small `pedestrian_icon()` (it defaults to `GOLD_KEY`) appears just ahead of / beside the
  Planning node — the thing the plan must not endanger. Keep it small and quiet, not cartoonish.
- The Planning node emits **one** short forward trajectory stub (a green `VMobject` curve) that
  bends safely clear of the pedestrian — a one-line promise of "safe," without pre-drawing RiskMap's
  whole risk-field (leave that for s12).
- Land the chiseled hook line, `write_chiseled`, `GOLD_RICH`, italic, lower-center — same treatment
  as the s14 bridge forward-line:
  **"safe enough to stake a life on."**
  (Verbatim is strong; if it crowds, shorten to *"stake a life on it."* — default to verbatim.)
- Optional single life motif: one slow `Flash`/pulse on the pedestrian (a heartbeat beat) as the
  line finishes. One pulse only — restraint.

## Handoff to RiskMap (~1 s)

- End on the chiseled line + Planning node + pedestrian held briefly, then `self._close()` (blank
  `BG_PAPER`, house rule). RiskMap opens on its road grid; because Planning was `ACCENT_BLUE` and
  the safe stub was `GREEN_FIX`, s12's blue ego + green corridor read as a direct continuation.
- *(Optional, nicer)* instead of a plain close, have the Planning node briefly **expand toward the
  bottom of frame** as if opening into the road space, then close — a soft match-cut into RiskMap.
  Skip if it adds time/complexity; the plain `_close()` is fine.

---

## Animation sequence summary

1. `self._open("From Understanding to Planning")`.
2. Beat 1: FadeIn Perception + Prediction (teal) → green checks + Flash.
3. Beat 2: FadeIn Planning (blue, "?", breathing) → two converging arrows → dim solved pair.
4. Beat 3: pedestrian in → safe trajectory stub bends clear → `write_chiseled` hook (gold italic) →
   one pedestrian pulse.
5. Brief hold → `self._close()` (or optional expand-into-road match-cut).

Target ≈ 13–15 s, matching the narration.

---

## Implementation notes

- `StudioScene`, `PART_NUM = 2` (`ACCENT_TEAL` / `PASTEL_TEAL` as `self.PART_COLOR` /
  `self.PART_PASTEL`).
- Reuse: `pipeline_block` / `stage_panel` and `pipeline_arrow` / `h_arrow` from
  `studio/components/pipeline.py`; `pedestrian_icon` from `agents.py`; `write_chiseled` from
  `animations.py`; `contribution_badge` from `annotations.py` if you want a ready-made check/badge.
- All colors imported from `colors.py`; no hex literals. No curly quotes — write the hook with ASCII
  apostrophe-free wording ("stake a life on") to avoid any Pango quirk.
- Text built outside `self.play`/`self.add` relies on the overridden `add`/`play` for contrast;
  if you assemble a `VGroup` separately, call `self._force_text_contrast(group)` first.
- `SCRIPT` constant: `"Perception and prediction are inputs to planning; planning must be safe
  enough to stake a life on."`

## Integration checklist

- [ ] Create `p02_s11c_planning_pivot.py` with class `P02S11CPlanningPivot`.
- [ ] Add the scene to `render_studio_all.ps1` between `P02S11BTurboTrainSolution` and
      `P02S12RiskMap`.
- [ ] Add a new `### [P02S11CPlanningPivot — "From Understanding to Planning"]` section to
      `studio_scripts/script_part2.md` (place it between the TurboTrain Solution and RiskMap
      sections) with the narration above; mirror in `studio_scripts/latex/main.tex` if kept in sync.
- [ ] Trim the RiskMap intro narration so it doesn't restate "perception and prediction →
      understanding → planning" (start RiskMap at the interpretability sentence).
- [ ] Verify design rules: `BG_PAPER`, ends on `_close()`, English-only on screen, colors imported,
      axes-before-data not applicable (no chart here).

## Render & review

```bash
cd "/Users/phu-quynguyen-lam/o D/Beyond_SelfDriving"
# iterate
PYTHONPATH="$PWD" /Users/phu-quynguyen-lam/miniforge3/envs/manim/bin/manimgl \
  -w -l studio/scenes/part02/p02_s11c_planning_pivot.py P02S11CPlanningPivot
# final HD (required before done)
PYTHONPATH="$PWD" /Users/phu-quynguyen-lam/miniforge3/envs/manim/bin/manimgl \
  -w --hd studio/scenes/part02/p02_s11c_planning_pivot.py P02S11CPlanningPivot
```

Frames to spot-check: (a) the solved teal pair with green checks; (b) the converging arrows into the
blue "?" Planning node with the pair dimmed; (c) the hook line + pedestrian + safe stub end frame —
it should read "planning, with a life at stake" on its own.
