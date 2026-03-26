# Beyond Self-Driving — Production Spec
## Session 4 of 5: Part 04 — From Pre-Training to Post-Training: Building an Efficient V2X System

> **Original speaker:** Seth Z. Zhao, PhD Candidate, UCLA Mobility Lab
> **Reference slides:** Part 4 (no PDF uploaded — work from script)
> **Estimated duration:** ~10 min
> **Tone note:** Part 04 is the most quantitative part of the tutorial. Narration is precise and number-driven. Visuals lean heavily on comparison charts, before/after diagrams, and pipeline flows. Fewer mascot appearances — the material is dense enough to carry itself.

---

## Quick Reference

Same conventions as Sessions 1–3.

**Part 04 additional colors:**

| Name | Hex | Used for |
|---|---|---|
| `ORANGE` | `#E67E22` | Failed baseline results (scatter plot) |
| `INT8_GREEN` | `#2ECC71` | Quantized / efficient representations |
| `FP32_RED` | `#E74C3C` | Heavy FP32 cost indicators |
| `ENERGY_YELLOW` | `#F1C40F` | Energy / power cost annotations |

---
---

## SCENE 4-01 — Title & Efficiency Framing

> **Duration:** ~30s

### [NARRATION]

```
[NARRATOR]

"Part 4. Building an Efficient V2X
Cooperative Perception System.
Speaker: Seth Z. Zhao, UCLA Mobility Lab.

Parts 1 through 3 built a system
that works in the real world.

But 'works' is not enough.

This part asks a harder question:
can this system survive the real world?

Survive means:
learning when labeled data is scarce,
training without months of GPU compute,
and running on the edge hardware
inside an actual vehicle.

Three bottlenecks.
Three solutions.
In order."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| T01 | Background | `Rectangle` | Fill `NAVY` |
| T02 | Part number "04" watermark | `Text` | Font size 72, `GOLD`, opacity 0.15 |
| T03 | Title text | `Text` | Font size 30, `WHITE`, bold, center |
| T04 | Speaker label | `Text` | Font size 18, `LIGHT_BLUE` |
| T05 | Divider | `Line` | `BLUE`, 8u wide |
| T06 | Three bottleneck labels in a row | `VGroup` of 3 `RoundedRectangle` | Fill `#2A1A1A`, stroke `RED_MUTED`, each 3u×1.2u |
| T07 | Bottleneck 1 label "Data" | `Text` | `RED_MUTED`, size 20, bold |
| T08 | Bottleneck 2 label "Training" | `Text` | Same |
| T09 | Bottleneck 3 label "Inference" | `Text` | Same |
| T10 | "In order" arrow connecting T06 boxes | `Arrow` x2 | `WHITE`, left→right |
| T11 | Roadmap strip | `VGroup` (reused) | Bottom, Part 04 node highlighted `GOLD` |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(T01, T02)` | 0.4s |
| 2 | 0.4s | `Write(T03)` | 1s |
| 3 | 1.4s | `FadeIn(T04)` | 0.3s |
| 4 | 1.7s | `Create(T05)` | 0.3s |
| 5 | 2s | `FadeIn(T06[0], T07)` — Data box | 0.3s |
| 6 | 2.3s | `GrowArrow(T10[0])` | 0.2s |
| 7 | 2.5s | `FadeIn(T06[1], T08)` — Training box | 0.3s |
| 8 | 2.8s | `GrowArrow(T10[1])` | 0.2s |
| 9 | 3s | `FadeIn(T06[2], T09)` — Inference box | 0.3s |
| 10 | 3.8s | `FadeIn(T11)` — roadmap strip | 0.4s |
| 11 | 4.5s | `[HOLD]` | 1s |

---

## SCENE 4-02 — Why Efficiency Matters in V2X

> **Duration:** ~40s

### [NARRATION]

```
[NARRATOR]

"V2X — Vehicle-to-Everything —
is the paradigm that lets agents share perception
and 'borrow eyes' from each other.
The occlusion problem from Part 2 in practice.

This is attracting serious attention
beyond just academia.
The US Department of Transportation
is investing in smart intersection deployments
specifically for pedestrian safety.

But here's the reality gap:
building a V2X system that works in a lab
is very different from building one
that scales to millions of intersections.

Three unanswered questions remain.

One: how do you get good performance
when annotated data is limited?
Annotation is expensive — it doesn't scale.

Two: how do you train a multi-task,
multi-agent framework without months of compute?

Three: how do you run inference in real-time
on an edge device in a moving vehicle,
where memory and power budgets are tight?

These three questions are the three parts of this section."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| WH01 | Background | `Rectangle` | Fill `#0F172A` |
| WH02 | "V2X = Borrowing Eyes" diagram | `VGroup` | Two cars + INF node, dashed communication lines, small LiDAR sweeps |
| WH03 | US DoT reference badge | `RoundedRectangle` | Fill `#1E3A5F`, stroke `BLUE`, "US DoT — Smart Intersections" |
| WH04 | Three question cards (stacked vertically) | `RoundedRectangle` x3 | Fill `#1E3A5F`, stroke `BLUE`, each 8u×1.2u |
| WH05 | Q1 "Data: annotation doesn't scale" | `Text` | `WHITE`, size 17 |
| WH06 | Q2 "Training: months of compute" | `Text` | `WHITE`, size 17 |
| WH07 | Q3 "Inference: edge hardware limits" | `Text` | `WHITE`, size 17 |
| WH08 | Number labels "01" "02" "03" | `Text` | `GOLD`, size 22, bold, left of each card |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(WH01, WH02)` | 0.5s |
| 2 | 0.5s | `FadeIn(WH03)` | 0.4s |
| 3 | 1.5s | `[HOLD]` | 0.5s |
| 4 | 2s | WH02 and WH03 scale down to top | 0.4s |
| 5 | 2.4s | `FadeIn(WH08[0], WH04[0], WH05)` — Q1 | 0.4s |
| 6 | 2.8s | `FadeIn(WH08[1], WH04[1], WH06)` — Q2 | 0.4s |
| 7 | 3.2s | `FadeIn(WH08[2], WH04[2], WH07)` — Q3 | 0.4s |
| 8 | 4.5s | `[HOLD]` | 1s |

---

## SCENE 4-03 — Data Bottleneck: The Annotation Cost Problem

> **Duration:** ~45s

### [NARRATION]

```
[NARRATOR]

"Start with data.

V2X datasets have grown fast.
V2V4Real: 240 thousand annotations.
DAIR-V2X: 460 thousand.
UCLA's V2X-Real: 1.2 million.

Five times the scale in two years.

But annotation cost scales exactly the same way.

3D LiDAR annotation isn't a click-and-drag task.
It requires specialized software toolkits,
annotators trained specifically for point cloud data,
and multi-layer quality checking.

You cannot scale annotation
by just hiring more people and throwing money at it.
The complexity doesn't compress.

The question is fundamental:
how do you make a model learn well
when labeled data is limited?"
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| AN01 | Background | `Rectangle` | Fill `#0A0A0A` |
| AN02 | Bar chart — dataset growth | `BarChart` or `VGroup` of `Rectangle` x3 | X-axis: dataset names, Y-axis: annotation count |
| AN03 | Bar 1 "V2V4Real 240K" | `Rectangle` | Fill `BLUE`, height proportional |
| AN04 | Bar 2 "DAIR-V2X 460K" | `Rectangle` | Fill `BLUE`, taller |
| AN05 | Bar 3 "V2X-Real 1.2M" | `Rectangle` | Fill `GOLD`, tallest |
| AN06 | Scale growth label "5× in 2 years" | `Text` | `GOLD`, size 18, bold, above bar chart |
| AN07 | Annotation cost bar (parallel, red) | `Rectangle` x3 | Fill `RED_MUTED`, same heights — "cost grows same rate" |
| AN08 | Cost label "Annotation cost ↑ equally" | `Text` | `RED_MUTED`, size 16 |
| AN09 | Annotation complexity breakdown | `VGroup` of 3 bullet cards | Fill `#1E3A5F`, right of chart |
| AN10 | Bullet 1 "Specialized 3D toolkit" | `Text` | `WHITE`, size 15 |
| AN11 | Bullet 2 "Trained annotators" | `Text` | `WHITE`, size 15 |
| AN12 | Bullet 3 "Multi-layer QC" | `Text` | `WHITE`, size 15 |
| AN13 | Key question box | `RoundedRectangle` | Fill `#2A1A1A`, stroke `RED_MUTED`, bottom |
| AN14 | "How to learn with limited labels?" | `Text` | `RED_MUTED`, size 20, bold |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(AN01)` | 0.3s |
| 2 | 0.3s | Bars AN03, AN04, AN05 grow up from zero, staggered 0.3s | 1s total, `rate_func=smooth` |
| 3 | 1.3s | `Write(AN06)` — 5× label | 0.4s |
| 4 | 2s | `FadeIn(AN07)` — cost bars overlay or appear beside | 0.5s |
| 5 | 2.5s | `Write(AN08)` — cost label | 0.4s |
| 6 | 3.2s | `FadeIn(AN09–AN12)` — bullets, staggered 0.2s | 0.6s |
| 7 | 4.5s | `FadeIn(AN13, AN14)` — question box | 0.5s |
| 8 | 5.5s | `[HOLD]` | 1.5s |

### [NOTES]
- AN03–AN05 bars: normalize heights so V2V4Real = 2u, DAIR-V2X = ~3.8u, V2X-Real = 10u (1.2M is ~5× V2V4Real). The visual gap should feel dramatic.
- AN07 cost bars: draw them immediately next to or behind the dataset bars in a contrasting color. The point is that they're the same height — cost didn't get cheaper as data grew.

---

## SCENE 4-04 — CooPre: Cooperative Pretraining

> **Duration:** ~100s

### [NARRATION]

```
[NARRATOR]

"The answer is CooPre —
Cooperative Pretraining for V2X Perception.
Published at IROS 2025.

The first self-supervised pretraining method
designed specifically for multi-agent cooperative perception.
Zero annotations required."

--- MECHANISM ---

[NARRATOR]
"The core mechanism:
multi-agent masked reconstruction.

During pretraining, the model receives
LiDAR point clouds from multiple agents.
It randomly masks a set of voxels
on the BEV plane —
Bird's Eye View, the top-down feature space.

Then it's asked to reconstruct
the masked regions.

This sounds simple.
But to do it well, the model must learn
the 3D geometric structure of the environment —
and more importantly,
learn how to use information from other agents
to fill in what it can't see from its own position.

Think about what that means.
When Agent 1 has a voxel masked —
a region it can't see —
the only way to reconstruct it
is to use Agent 2's observation of that same region.

That inductive bias is exactly
what cooperative perception needs.
The model is being forced to learn
'when I can't see something, I ask someone else.'
No annotation required to teach that behavior."

--- RESULTS ---

[NARRATOR]
"The results validate this directly.

With only 50% of the labeled training data,
CooPre matches the performance of a model
trained from scratch on 100% of the data.

With the full 100% of labeled data,
CooPre improves AP by an additional 4%
over the baseline.

And pretraining cross-domain —
training on one dataset and transferring to another —
outperforms single-domain pretraining.
The representation CooPre learns
is genuinely transferable across environments."
```

### [VISUAL SPEC]

**Section A — Mechanism diagram**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| CP01 | Background | `Rectangle` | Fill `#0F172A` |
| CP02 | "CooPre" title | `Text` | `GOLD`, size 26, bold |
| CP03 | "Zero annotations" badge | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN`, text `GREEN` bold |
| CP04 | Agent 1 LiDAR block | `VGroup` stacked rects | `#1E3A5F`, N-frame depth effect |
| CP05 | Agent 2 LiDAR block | Same | Right of CP04 |
| CP06 | BEV plane visualization | `Grid` 8×8 | Fill `#0F172A`, stroke `BLUE` opacity 0.4 |
| CP07 | Masked voxels on BEV | `Square` x6 (scattered) | Fill `RED_MUTED`, opacity 0.8 — the hidden regions |
| CP08 | Arrow agents → BEV | `Arrow` x2 | `BLUE` |
| CP09 | Reconstruction output BEV | Same `Grid` | But masked cells now filled `GREEN` |
| CP10 | "Reconstruct masked regions" label | `Text` | `WHITE`, size 16, italic |
| CP11 | Inductive bias callout | `RoundedRectangle` | Fill `NAVY`, stroke `GOLD` |
| CP12 | Callout text | `Text` | `GOLD`, size 17 — "When I can't see — I ask someone else." |
| CP13 | Agent 2 helping arrow | `CurvedArrow` | `GREEN`, dashed, from CP05 toward masked voxels |

**Section B — Results chart**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| CR01 | Axes | `Axes` | `WHITE`, x="% labeled data (50% / 100%)", y="AP" |
| CR02 | Baseline bar at 100% | `Rectangle` | Fill `BLUE`, label "Baseline 100%" |
| CR03 | CooPre bar at 50% | `Rectangle` | Fill `INT8_GREEN`, same height as CR02 — "matches with half the data" |
| CR04 | CooPre bar at 100% | `Rectangle` | Fill `INT8_GREEN`, taller than CR02 by ~4% |
| CR05 | "50% data = 100% baseline" annotation | `DoubleArrow` + label | `GOLD`, horizontal, between CR02 and CR03 |
| CR06 | "+4% AP" annotation | `DoubleArrow` + label | `GREEN`, vertical, on CR04 |
| CR07 | Cross-domain result badge | `RoundedRectangle` | Fill `#1E3A5F`, stroke `BLUE` |
| CR08 | Cross-domain label | `Text` | `LIGHT_BLUE`, size 15 — "Cross-domain pretraining > single-domain" |

### [ANIMATION]

**Section A (0–45s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(CP01)`, `Write(CP02)`, `FadeIn(CP03)` | 0.6s |
| 2 | 0.6s | `FadeIn(CP04, CP05)` — agent blocks | 0.5s |
| 3 | 1.1s | `GrowArrow(CP08[0], CP08[1])` | 0.4s |
| 4 | 1.5s | `FadeIn(CP06)` — BEV grid | 0.4s |
| 5 | 1.9s | `FadeIn(CP07)` — masked voxels appear | 0.5s, each square pops individually staggered 0.08s |
| 6 | 2.5s | `Write(CP10)` — label | 0.4s |
| 7 | 3.5s | `[HOLD]` | 0.8s |
| 8 | 4.3s | `Create(CP13)` — Agent 2 helping arrow | 0.5s |
| 9 | 4.8s | `Transform(CP07, CP09_masked_cells)` — masked cells fill green | 0.6s, `rate_func=smooth` |
| 10 | 5.8s | `FadeIn(CP11, CP12)` — callout | 0.5s |
| 11 | 7s | `[HOLD]` | 1.5s |

**Section B (0–30s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `Create(CR01)` — axes | 0.5s |
| 2 | 0.5s | `CR02` grows up from zero | 0.5s — baseline |
| 3 | 1s | `CR03` grows up to same height | 0.5s, `GOLD` label "50% data = same performance" |
| 4 | 2s | `FadeIn(CR05)` — double arrow with annotation | 0.4s |
| 5 | 2.8s | `CR04` grows slightly taller than CR02 | 0.4s |
| 6 | 3.2s | `FadeIn(CR06)` — "+4% AP" | 0.4s |
| 7 | 4s | `FadeIn(CR07, CR08)` — cross-domain badge | 0.4s |
| 8 | 5s | `[HOLD]` | 1.5s |

### [NOTES]
- CP07 masked voxels: scatter them non-uniformly across the grid — some near the edge, some in the middle — to feel more realistic than a regular pattern.
- CP13 helping arrow: draw as a dashed `CurvedArrow` arcing from Agent 2's block over the BEV to land on one of the masked squares. This is the single most important visual in this scene — it makes the cooperative inductive bias tangible.
- CR03 and CR02 being exactly the same height is visually striking. Make sure they align at the same y-coordinate precisely.

---

## SCENE 4-05 — Training Bottleneck: The Multi-Task Conflict Problem

> **Duration:** ~50s

### [NARRATION]

```
[NARRATOR]

"The second bottleneck: training.

Part 2 introduced TurboTrain.
Here we go deeper into why the problem exists
before showing how it's solved.

When you take single-frame cooperative perception
and extend it to multi-frame and multi-task —
temporal dimension, multiple agents,
detection, prediction, and planning simultaneously —
the architecture becomes complex
across many dimensions at once.

That complexity creates two specific problems."

--- PROBLEM 1: INITIALIZATION SENSITIVITY ---

[NARRATOR]
"First: initialization sensitivity.

A complex model like this is very sensitive
to its starting point.
One-time training — random initialization,
one full training run —
frequently leads to instability
or convergence to a bad local minimum.

Look at those orange dots on the chart.
Models with strong individual components —
failing completely in one-time training."

--- PROBLEM 2: GRADIENT CONFLICT ---

[NARRATOR]
"Second: gradient conflict.

Different tasks pull the model
in different directions in weight space.

Detection wants one thing.
Prediction wants another.
Planning sometimes wants a third.

When tasks conflict heavily,
improving one task actively degrades another.
The optimizer has no principled way
to balance them
without explicit intervention."
```

### [VISUAL SPEC]

**Section A — Architecture complexity visualization**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| TC01 | Background | `Rectangle` | Fill `#0A0A0A` |
| TC02 | "Single-frame" label + simple diagram | `VGroup` | Left: one agent → one box → detect |
| TC03 | Arrow "extend →" | `Arrow` | `WHITE` |
| TC04 | "Multi-frame + Multi-agent + Multi-task" label | `VGroup` | Right: multiple agents, N-frame stacks, 3 output branches |
| TC05 | Complexity annotation "Many dimensions at once" | `Text` | `RED_MUTED`, size 16, below TC04 |

**Section B — Orange dot scatter plot (initialization failure)**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| TG01 | Axes | `Axes` | `WHITE`, x="AP@0.5", y="EPA" |
| TG02 | Orange dots x8 (one-time training failures) | `Dot` x8 | `ORANGE`, r=0.09u, clustered low-left area |
| TG03 | "One-time training" legend entry | `Dot` + label | `ORANGE` |
| TG04 | Failure zone shading | `Polygon` | Fill `ORANGE`, opacity 0.08, around TG02 cluster |
| TG05 | Label "Strong models — fail one-time" | `Text` | `ORANGE`, size 15, italic |

**Section C — Gradient conflict diagram**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| GC01 | Center model weight space node | `Circle` | Fill `#1E3A5F`, r=0.4u, label "Model" |
| GC02 | Detection gradient arrow | `Arrow` | `BLUE`, pointing one direction |
| GC03 | Prediction gradient arrow | `Arrow` | `GREEN`, pointing different direction |
| GC04 | Planning gradient arrow | `Arrow` | `PURPLE`, pointing third direction |
| GC05 | Conflict zone at node | — | `GC01.set_stroke(RED_MUTED, width=4)` pulse |
| GC06 | Label "Gradients pull in different directions" | `Text` | `WHITE`, size 16 |
| GC07 | ✗ "Improve Detection → Prediction degrades" | `Text` | `RED_MUTED`, size 14, italic |

### [ANIMATION]

**Section A (0–15s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(TC01, TC02)` | 0.4s |
| 2 | 0.5s | `GrowArrow(TC03)` | 0.3s |
| 3 | 0.8s | `FadeIn(TC04)` | 0.6s, complexity diagram assembles with staggered parts |
| 4 | 1.8s | `Write(TC05)` | 0.4s |

**Section B (0–20s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `Create(TG01)` — axes | 0.5s |
| 2 | 0.5s | `FadeIn(TG04)` — failure zone shading | 0.3s |
| 3 | 0.8s | `FadeIn(TG02)` — orange dots pop in, staggered 0.07s | 0.56s total |
| 4 | 1.4s | `FadeIn(TG03, TG05)` — legend + label | 0.4s |
| 5 | 2.5s | `[HOLD]` | 1s |

**Section C (0–20s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(GC01)` — model node | 0.3s |
| 2 | 0.3s | `GrowArrow(GC02)` — detection gradient | 0.4s |
| 3 | 0.7s | `GrowArrow(GC03)` — prediction gradient, different direction | 0.4s |
| 4 | 1.1s | `GrowArrow(GC04)` — planning gradient, third direction | 0.4s |
| 5 | 1.8s | `GC01` stroke pulses `RED_MUTED` — conflict signal | 0.5s, `there_and_back` |
| 6 | 2.5s | `Write(GC06, GC07)` | 0.5s |
| 7 | 3.5s | `[HOLD]` | 1s |

### [NOTES]
- GC02, GC03, GC04 gradient arrows should point in clearly different directions — roughly 120° apart — so the conflict is geometrically obvious.

---

## SCENE 4-06 — TurboTrain: The 2-Stage Solution

> **Duration:** ~70s

### [NARRATION]

```
[NARRATOR]

"TurboTrain solves both problems
with a two-stage pipeline."

--- STAGE 1: PRETRAIN ---

[NARRATOR]
"Stage 1 — Pretrain.

The model learns a task-agnostic 4D representation.
4D: three spatial dimensions plus time.

It does this by reconstructing masked LiDAR
across multi-agent, multi-frame data —
the same masked reconstruction mechanism as CooPre,
but now applied to the full temporal stack.

No annotations. No task-specific objective.
Just: learn the spatiotemporal structure
of what the environment looks like.

This gives the model a stable initialization
before any task-specific training begins —
solving the initialization sensitivity problem."

--- STAGE 2: BALANCE ---

[NARRATOR]
"Stage 2 — Balance.

Fine-tune with a hybrid training strategy
that alternates between two types of steps.

Free gradient steps:
all tasks learn simultaneously, no interference.
The model explores freely.

Conflict-suppressing steps:
when the optimizer detects that tasks
are pulling against each other,
it applies a correction.
The conflicting gradients are projected
to reduce mutual interference.

This directly solves the gradient conflict problem."

--- RESULT ---

[NARRATOR]
"The outcome on the chart:

TurboTrain reaches the highest combined
detection and prediction performance
in approximately 45 epochs.

Compare: manual 4-stage pipeline needed 120 epochs.

Less than half the compute.
Higher performance.
And no human expertise needed
to decide when to transition between stages."
```

### [VISUAL SPEC]

**Section A — 2-Stage Pipeline Diagram**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| TB01 | Background | `Rectangle` | Fill `#0F172A` |
| TB02 | "TurboTrain" header | `Text` | `GOLD`, size 26, bold |
| TB03 | "2 stages vs 4 manual stages" sub-label | `Text` | `WHITE`, size 16, italic |
| TB04 | Stage 1 box "Pretrain" | `RoundedRectangle` | Fill `#1E3A5F`, stroke `BLUE`, 5u×2.5u |
| TB05 | Stage 1 sub-label "Task-agnostic 4D representation" | `Text` | `LIGHT_BLUE`, size 15 |
| TB06 | Stage 1 mechanism label "Masked LiDAR reconstruction — multi-agent, multi-frame" | `Text` | `WHITE`, size 14, italic |
| TB07 | Stage 1 solves badge | `RoundedRectangle` | Fill `NAVY`, stroke `GREEN`, "Solves: initialization sensitivity" |
| TB08 | Arrow Stage 1 → Stage 2 | `Arrow` | `WHITE`, thick |
| TB09 | Stage 2 box "Balance" | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN`, 5u×2.5u |
| TB10 | Stage 2 sub-label "Hybrid gradient strategy" | `Text` | `INT8_GREEN`, size 15 |
| TB11 | Free gradient step indicator | `Arrow` | `BLUE`, labeled "Free steps" |
| TB12 | Conflict-suppressing step indicator | `Arrow` | `GREEN`, labeled "Conflict-suppressing steps" |
| TB13 | Alternating symbol between TB11 and TB12 | `Text` "↔" | `WHITE`, size 22 |
| TB14 | Stage 2 solves badge | `RoundedRectangle` | Fill `NAVY`, stroke `GREEN`, "Solves: gradient conflict" |

**Section B — Result chart (extends scatter plot from Scene 4-05)**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| TR01 | Scatter plot (reuse TG01 axes + TG02 orange dots) | Reused `VGroup` | Same as Section B from Scene 4-05 |
| TR02 | Blue dots x5 (manual 4-stage, 120 epochs) | `Dot` x5 | `BLUE`, mid-range performance |
| TR03 | Gold star — TurboTrain (45 epochs) | `Star` or `Dot` | `GOLD`, r=0.13u, top-right quadrant |
| TR04 | "120 epochs" label near TR02 cluster | `Text` | `BLUE`, size 14 |
| TR05 | "~45 epochs" label near TR03 | `Text` | `GOLD`, size 14 |
| TR06 | "Best performance" annotation arrow | `Arrow` | `GOLD`, pointing to TR03 |
| TR07 | Epoch comparison callout | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN` |
| TR08 | "45 vs 120 epochs — less than half" | `Text` | `GREEN`, size 18, bold |
| TR09 | "No human expertise needed" | `Text` | `WHITE`, size 15 |

### [ANIMATION]

**Section A (0–35s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(TB01)`, `Write(TB02, TB03)` | 0.6s |
| 2 | 0.6s | `FadeIn(TB04, TB05, TB06)` — Stage 1 | 0.6s |
| 3 | 1.5s | `FadeIn(TB07)` — "Solves" badge | 0.3s |
| 4 | 2s | `GrowArrow(TB08)` | 0.3s |
| 5 | 2.3s | `FadeIn(TB09, TB10)` — Stage 2 | 0.5s |
| 6 | 3s | `GrowArrow(TB11)` — free steps | 0.3s |
| 7 | 3.3s | `FadeIn(TB13)` — alternating symbol | 0.2s |
| 8 | 3.5s | `GrowArrow(TB12)` — conflict steps | 0.3s |
| 9 | 4s | TB11 → TB12 → TB11 alternating flash: `set_color(GOLD)` → `set_color(original)` | 1s, 2 cycles — simulates the alternating strategy |
| 10 | 5.2s | `FadeIn(TB14)` — "Solves" badge | 0.3s |
| 11 | 6s | `[HOLD]` | 1s |

**Section B (0–25s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(TR01)` — scatter plot reappears | 0.4s |
| 2 | 0.5s | `FadeIn(TR02)` — blue dots, staggered | 0.5s |
| 3 | 1.2s | `FadeIn(TR04)` — 120 epochs label | 0.3s |
| 4 | 2s | `FadeIn(TR03)` — gold star pops in | 0.4s, slight scale bounce `scale(1.3)→scale(1.0)` |
| 5 | 2.5s | `FadeIn(TR05, TR06)` — label + arrow | 0.4s |
| 6 | 3.2s | `FadeIn(TR07, TR08, TR09)` — callout | 0.5s |
| 7 | 4.5s | `[HOLD]` | 2s |

---

## SCENE 4-07 — Inference Bottleneck: The Latency Chain

> **Duration:** ~50s

### [NARRATION]

```
[NARRATOR]

"The third bottleneck: inference.

This is the one most often skipped in research papers —
and the one that determines whether
a system actually deploys.

In a V2X pipeline, inference isn't a single step.
It's a chain.

Each agent runs local inference on its own sensors.
Then communication latency —
transmitting features to other agents.
Then fusion inference —
integrating information from all agents together.

Every step in that chain takes time.
And the total must be small enough
for the vehicle to make real-time decisions.

The underlying problem is arithmetic cost.

Neural networks use FP32 —
32-bit floating point numbers.
Floating point multiplication is expensive.
And it scales quadratically —
double the precision, roughly four times the cost.

The memory access problem is worse.
Reading 32-bit data from DRAM —
main memory —
costs around 640 picojoules per access.
From SRAM, just 5 picojoules.
With millions of parameters
that need to be loaded for every forward pass,
on edge hardware with limited memory bandwidth —
this compounds fast."
```

### [VISUAL SPEC]

**Section A — Latency chain**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| LC01 | Background | `Rectangle` | Fill `#0A0A0A` |
| LC02 | Progress bar / pipeline | `VGroup` of 3 blocks + arrows | Horizontal, full width |
| LC03 | Block 1 "Local Inference" | `RoundedRectangle` | Fill `#1E3A5F`, stroke `BLUE` |
| LC04 | Block 2 "Communication" | `RoundedRectangle` | Fill `#3D1A00`, stroke `INFRA_ORANGE` |
| LC05 | Block 3 "Fusion Inference" | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN` |
| LC06 | Arrows between blocks | `Arrow` x2 | `WHITE` |
| LC07 | "Time budget" bar above pipeline | `Rectangle` | Fill `RED_MUTED`, limited width — "total budget is fixed" |
| LC08 | Clock icon (countdown) | `SVGMobject` or `VGroup` | `RED_MUTED`, right end |
| LC09 | "Real-time requirement" label | `Text` | `RED_MUTED`, size 16 |

**Section B — Arithmetic cost breakdown**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| AC01 | "FP32 Multiplication" label | `Text` | `FP32_RED`, size 20, bold |
| AC02 | Power consumption bar | `Rectangle` | Fill `FP32_RED`, tall |
| AC03 | "FP32 Add" comparison bar | `Rectangle` | Fill `BLUE`, shorter |
| AC04 | "Quadratic scaling" annotation | `Text` + upward arrow | `FP32_RED`, "double precision → 4× cost" |
| AC05 | Memory access comparison table | `VGroup` of 2 rows | |
| AC06 | Row 1 "DRAM: 640 pJ per access" | `Rectangle` + `Text` | Fill `FP32_RED`, wide |
| AC07 | Row 2 "SRAM: 5 pJ per access" | `Rectangle` + `Text` | Fill `INT8_GREEN`, narrow — 128× smaller |
| AC08 | Scale label "128× more expensive" | `Text` | `FP32_RED`, size 16, between rows |
| AC09 | "Millions of params × DRAM cost = problem" | `Text` | `WHITE`, size 16, italic |

### [ANIMATION]

**Section A (0–20s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(LC01)` | 0.3s |
| 2 | 0.3s | `FadeIn(LC03)` + label | 0.3s |
| 3 | 0.6s | `GrowArrow(LC06[0])` | 0.2s |
| 4 | 0.8s | `FadeIn(LC04)` + label | 0.3s |
| 5 | 1.1s | `GrowArrow(LC06[1])` | 0.2s |
| 6 | 1.3s | `FadeIn(LC05)` + label | 0.3s |
| 7 | 2s | `FadeIn(LC07)` — time budget bar appears above | 0.4s, draws left to right, stops at a "tight" point |
| 8 | 2.5s | `FadeIn(LC08, LC09)` | 0.3s |
| 9 | 3.5s | `[HOLD]` | 0.8s |

**Section B (0–25s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(AC01)` | 0.3s |
| 2 | 0.3s | `AC02` grows up: FP32 mult bar | 0.5s |
| 3 | 0.8s | `AC03` grows up: FP32 add bar (shorter) | 0.4s |
| 4 | 1.5s | `Write(AC04)` — quadratic annotation | 0.4s |
| 5 | 2.5s | `FadeIn(AC06)` — DRAM row | 0.4s, bar drawn left to right |
| 6 | 3s | `FadeIn(AC07)` — SRAM row | 0.3s, much shorter bar |
| 7 | 3.5s | `Write(AC08)` — "128× more expensive" | 0.4s |
| 8 | 4.2s | `Write(AC09)` — conclusion | 0.4s |
| 9 | 5.5s | `[HOLD]` | 1.5s |

### [NOTES]
- AC06 and AC07 bars: draw as horizontal bars with lengths proportional to cost (640 vs 5). At a reasonable scale where AC07 = 0.5u wide, AC06 = 64u — obviously too wide. Scale to max screen width so AC06 extends off-screen with an arrow, emphasizing the disproportion. Or: cap AC06 at screen edge with "640 pJ →" label. Either approach makes the 128× difference visceral.

---

## SCENE 4-08 — QuantV2X: Full-Pipeline Quantization

> **Duration:** ~80s

### [NARRATION]

```
[NARRATOR]

"The solution is quantization —
reducing the bit-width of weights and activations
throughout the network."

--- WHAT QUANTIZATION DOES ---

[NARRATOR]
"Moving from FP32 to INT8.
32-bit floats become 8-bit integers.

The impact:
floating point multiplication becomes integer addition —
far cheaper in hardware.
Memory footprint drops by a factor of four.
And many edge chips have dedicated
INT8 inference hardware with much higher throughput
than their FP32 counterparts."

--- THE V2X CHALLENGE ---

[NARRATOR]
"But quantization in V2X is not the same
as quantization in a single-agent model.

In standard quantization,
you worry about outlier activations —
values far from the mean that get clipped or distorted
when you compress the number range.

In V2X, you receive features
transmitted by other agents.
Those features may have very different
statistical distributions than your own.
They contain different outlier patterns —
and naively quantizing them
loses precisely the complementary information
that multi-agent cooperation provides.

QuantV2X solves this in two layers."

--- TWO LAYERS ---

[NARRATOR]
"Layer 1 — model-level quantization.
The full neural network: FP32 to INT8.
Standard quantization, applied carefully
to preserve inter-agent feature quality.

Layer 2 — communication-level quantization.
Instead of transmitting FP32 BEV features,
QuantV2X compresses them
into a low-bit codebook representation.
The result: communication payload
is 300 times smaller than uncompressed.

That's not a rounding difference.
That is the difference between
a message that fits in real-world V2X bandwidth
and one that doesn't.

QuantV2X proves that a fully quantized
cooperative perception pipeline —
model and communication both —
is viable for deployment,
with acceptable performance drop."
```

### [VISUAL SPEC]

**Section A — Quantization concept**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| QV01 | Background | `Rectangle` | Fill `#0F172A` |
| QV02 | FP32 representation visual | `VGroup` of 32 tiny `Square` | All `FP32_RED`, each 0.08u — "32 bits" |
| QV03 | "FP32" label | `Text` | `FP32_RED`, size 20, bold |
| QV04 | Arrow "→ quantize" | `Arrow` | `WHITE` |
| QV05 | INT8 representation visual | `VGroup` of 8 tiny `Square` | `INT8_GREEN`, same size — "8 bits" |
| QV06 | "INT8" label | `Text` | `INT8_GREEN`, size 20, bold |
| QV07 | Impact row 1 "FP multiply → INT add" | `Text` | `WHITE`, size 16 — with ✓ `GREEN` |
| QV08 | Impact row 2 "Memory: 4× smaller" | `Text` | `WHITE`, size 16 — with ✓ |
| QV09 | Impact row 3 "Edge hardware INT8 throughput" | `Text` | `WHITE`, size 16 — with ✓ |

**Section B — V2X-specific challenge**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| VC01 | "Single-agent quantization" label | `Text` | `WHITE`, size 18 |
| VC02 | Normal distribution curve (activations) | `ParametricFunction` | `BLUE`, standard bell curve |
| VC03 | "V2X quantization" label | `Text` | `WHITE`, size 18 |
| VC04 | Agent 1 distribution | `ParametricFunction` | `BLUE`, bell curve |
| VC05 | Agent 2 distribution (different shape) | `ParametricFunction` | `INFRA_ORANGE`, shifted/wider |
| VC06 | Naive quantization clip zone | `Rectangle` | Fill `RED_MUTED`, opacity 0.3, covers outlier tail |
| VC07 | "Loses complementary information" label | `Text` | `RED_MUTED`, size 15, italic |

**Section C — QuantV2X two-layer diagram**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| QL01 | Agent block with neural network | `VGroup` | Left |
| QL02 | "Layer 1: Model Quantization FP32→INT8" | `RoundedRectangle` | Fill `#1E3A5F`, stroke `INT8_GREEN` |
| QL03 | Communication pathway | `Arrow` | `BLUE`, center |
| QL04 | BEV feature (uncompressed, big) | `Rectangle` | Fill `FP32_RED`, wide — 3u |
| QL05 | "Layer 2: Codebook Compression" | `RoundedRectangle` | Fill `#1B4332`, stroke `INT8_GREEN` |
| QL06 | Compressed representation | `Rectangle` | Fill `INT8_GREEN`, narrow — 0.01u (300× smaller) |
| QL07 | "300× smaller" annotation | `DoubleArrow` + label | `GOLD`, between QL04 and QL06 |
| QL08 | "Fits V2X bandwidth" badge | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN`, `GREEN` text |
| QL09 | "Acceptable performance drop" note | `Text` | `WHITE`, size 15, italic |
| QL10 | "QuantV2X" badge | `RoundedRectangle` | Fill `#1E3A5F`, stroke `GOLD` |

### [ANIMATION]

**Section A (0–20s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(QV01, QV02, QV03)` | 0.5s |
| 2 | 0.5s | `GrowArrow(QV04)` | 0.3s |
| 3 | 0.8s | `FadeIn(QV05, QV06)` | 0.4s |
| 4 | 1.5s | QV02 boxes collapse into QV05 count: `Transform` | 0.6s, 32 → 8 boxes |
| 5 | 2.3s | `FadeIn(QV07, QV08, QV09)` — impact rows, staggered 0.2s | 0.6s |
| 6 | 3.5s | `[HOLD]` | 1s |

**Section B (0–20s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(VC01, VC02)` — single-agent case | 0.5s |
| 2 | 0.8s | `FadeIn(VC03, VC04, VC05)` — V2X case, two different distributions | 0.5s |
| 3 | 1.5s | `FadeIn(VC06)` — clip zone | 0.4s |
| 4 | 2s | `Write(VC07)` — "loses complementary info" | 0.4s |
| 5 | 3s | `[HOLD]` | 1s |

**Section C (0–30s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(QL01, QL02)` — agent + Layer 1 | 0.5s |
| 2 | 0.6s | `FadeIn(QL04)` — big BEV feature | 0.4s, label "uncompressed" |
| 3 | 1.2s | `FadeIn(QL05)` — Layer 2 module | 0.5s |
| 4 | 1.7s | `Transform(QL04, QL06)` — BEV compresses 300× | 0.8s, rectangle visibly shrinks |
| 5 | 2.5s | `FadeIn(QL07)` — "300× smaller" double arrow | 0.4s |
| 6 | 3.2s | `GrowArrow(QL03)` — communication pathway | 0.4s |
| 7 | 3.8s | `FadeIn(QL08)` — bandwidth badge | 0.3s |
| 8 | 4.5s | `FadeIn(QL09, QL10)` — performance note + QuantV2X badge | 0.4s |
| 9 | 5.5s | `[HOLD]` | 2s |

### [NOTES]
- Step 4 in Section C (`Transform(QL04, QL06)`): this is the visual climax of the scene. QL04 should be drawn noticeably wide (representing a large tensor) and QL06 should be barely visible — the compression is 300×, so even if QL04 is 3u wide, QL06 should be 0.01u — essentially a thin sliver. Add a `brace` with "300×" between them.
- VC05 (Agent 2's distribution): shift it ~0.5u to the right and make it slightly wider/flatter than VC04. This visually communicates that two agents have different feature statistics even when observing the same scene.

---

## SCENE 4-09 — Efficiency Summary: Three Solutions

> **Duration:** ~35s

### [NARRATION]

```
[NARRATOR]

"Three bottlenecks. Three solutions. One stack.

CooPre solves the data problem:
50% of labeled data achieves 100% performance,
through multi-agent masked reconstruction pretraining.

TurboTrain solves the training problem:
45 epochs instead of 120,
through task-agnostic pretraining
and conflict-suppressing fine-tuning.

QuantV2X solves the inference problem:
full-pipeline INT8 quantization,
communication payload 300× smaller,
edge-deployable cooperative perception."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| ES01 | Background | `Rectangle` | Fill `NAVY` |
| ES02 | Three cards, horizontal | `RoundedRectangle` x3 | Each 3.8u×4u, Fill `#1E3A5F`, stroke `BLUE` |
| ES03 | Card 1 header "CooPre" | `Text` | `GOLD`, size 22, bold |
| ES04 | Card 1 icon | Simple `VGroup` | Masked grid with green fill — mini version |
| ES05 | Card 1 result "50% data = 100% perf" | `Text` | `INT8_GREEN`, size 16, bold |
| ES06 | Card 2 header "TurboTrain" | `Text` | `GOLD`, size 22, bold |
| ES07 | Card 2 icon | Simple `VGroup` | Two-stage pipeline arrow |
| ES08 | Card 2 result "45 vs 120 epochs" | `Text` | `INT8_GREEN`, size 16, bold |
| ES09 | Card 3 header "QuantV2X" | `Text` | `GOLD`, size 22, bold |
| ES10 | Card 3 icon | Simple `VGroup` | 32→8 bit shrink |
| ES11 | Card 3 result "300× comm compression" | `Text` | `INT8_GREEN`, size 16, bold |
| ES12 | Connecting arrows | `Arrow` x2 | `BLUE`, card1→card2→card3 |
| ES13 | Bottom label "Edge-deployable V2X stack" | `Text` | `GOLD`, size 20, italic |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(ES01)` | 0.3s |
| 2 | 0.3s | `FadeIn(ES02[0], ES03, ES04, ES05)` — CooPre | 0.5s |
| 3 | 1s | `GrowArrow(ES12[0])` | 0.2s |
| 4 | 1.2s | `FadeIn(ES02[1], ES06, ES07, ES08)` — TurboTrain | 0.5s |
| 5 | 1.9s | `GrowArrow(ES12[1])` | 0.2s |
| 6 | 2.1s | `FadeIn(ES02[2], ES09, ES10, ES11)` — QuantV2X | 0.5s |
| 7 | 3s | `Write(ES13)` | 0.5s |
| 8 | 4s | All three cards pulse once simultaneously | 0.4s |
| 9 | 5s | `[HOLD]` | 1.5s |

---

## SCENE 4-10 — Bridge to Part 05

> **Duration:** ~25s

### [NARRATION]

```
[NARRATOR]

"Three bottlenecks solved.

The system can now learn from limited data,
train without months of compute,
and run on edge hardware.

But every part of this tutorial —
Parts 2, 3, and 4 —
has been focused on one thing:
cars and infrastructure.

The physical world is much larger than that.

Delivery robots. Humanoid robots.
Electric wheelchairs. Autonomous scooters.
All of them operating in the same space —
and all of them operating around people."

[CAR mascot transforms into a robot silhouette]

[CAR/ROBOT]
"The hardest variable in the equation
is not the sensor.
Not the model.
Not the hardware.

It's the human.

Part 5."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| BR01 | Background | `Rectangle` | Fill `NAVY` |
| BR02 | "✓ Data" label | `Text` | `INT8_GREEN`, size 20, bold |
| BR03 | "✓ Training" label | `Text` | Same |
| BR04 | "✓ Inference" label | `Text` | Same |
| BR05 | Checkmarks appear left-to-right | — | Stagger 0.3s |
| BR06 | "Cars + Infrastructure" label | `Text` | `LIGHT_BLUE`, size 18, center |
| BR07 | Expanding scene — more agent types | `VGroup` | Car → + robot + wheelchair + scooter icons, spread out |
| BR08 | Human figure icons | `SVGMobject` or simple `VGroup` | `WHITE`, scattered around BR07 |
| BR09 | "The hardest variable: the human" | `Text` | `GOLD`, size 22, bold |
| BR10 | CAR mascot → robot silhouette transition | `Transform` | `CAR` morphs to a generic robot shape |
| BR11 | "Part 05" reveal | `Text` | `GOLD`, size 28, bold |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(BR01)` | 0.3s |
| 2 | 0.3s | `Write(BR02)` | 0.3s |
| 3 | 0.6s | `Write(BR03)` | 0.3s |
| 4 | 0.9s | `Write(BR04)` | 0.3s |
| 5 | 1.5s | `[HOLD]` | 0.5s |
| 6 | 2s | `FadeIn(BR06)` — "Cars + Infrastructure" | 0.4s |
| 7 | 2.7s | `FadeIn(BR07)` — more agent types spread out | 0.6s, icons pop in one by one |
| 8 | 3.5s | `FadeIn(BR08)` — human figures | 0.4s, scattered around agents |
| 9 | 4.2s | `Write(BR09)` — "hardest variable" | 0.5s |
| 10 | 5s | `Transform(BR10)` — CAR → robot | 0.8s |
| 11 | 6s | `Write(BR11)` — "Part 05" | 0.4s |
| 12 | 7s | `[HOLD]` | 1s |
| 13 | 8s | Transition fade to Part 05 | 0.5s |

---

## End of Session 4 (Part 04)

> **Next file:** `spec_part05.md`
> **Scenes covered:** 4-01 through 4-10
> **Total estimated duration:** ~10 min

---

*Production note: Part 04 is the most number-driven section. Three scenes carry disproportionate weight: Scene 4-04 (CooPre mechanism — especially the CP13 helping arrow), Scene 4-06 (TurboTrain result on scatter plot — the gold star reveal), and Scene 4-08 (QuantV2X Layer 2 compression — the 300× shrink Transform). If cuts are needed, Scenes 4-05 and 4-07 can be compressed significantly — they set up problems that are already established by the context, and a shorter version can reference Part 2/3 rather than rebuilding from scratch.*
