# Beyond Self-Driving — Production Spec
## Session 2 of 5: Part 02 — Towards End-to-End Cooperative Automation

> **Original speaker:** Zewei Zhou, PhD Candidate, UCLA Mobility Lab
> **Reference slides:** Part 2 (no PDF uploaded — work from script)
> **Estimated duration:** ~10 min
> **Depends on:** `spec_intro_part01.md` for color palette, mascot definitions, and convention table

---

## Quick Reference (same as Session 1)

| Tag | Meaning |
|---|---|
| `CAR` | Main mascot — guide/responder |
| `PI` | Curious mascot — question-asker |
| `t=0s` | Time offset from scene start |
| `[HOLD]` | Pause before next step |

**Color palette** — identical to Session 1:

| Name | Hex | Used for |
|---|---|---|
| `NAVY` | `#1F3864` | Backgrounds, headers |
| `BLUE` | `#2E75B6` | Accent, arrows, highlights |
| `GOLD` | `#E8A838` | Quote text, emphasis |
| `LIGHT_BLUE` | `#EAF4FB` | Info boxes |
| `WHITE` | `#FFFFFF` | Text on dark backgrounds |
| `RED_MUTED` | `#C0392B` | Warnings, X marks |
| `GREEN` | `#27AE60` | Checkmarks, positive outcomes |
| `PURPLE` | `#7C3AED` | Neural network components |

---
---

## SCENE 2-01 — Title & Handoff from Part 01

> **Duration:** ~25s

### [NARRATION]

```
[NARRATOR]

"Part 2. Towards End-to-End Cooperative Automation.
Speaker: Zewei Zhou, UCLA Mobility Lab.

In Part 1, we saw how foundation models
give individual vehicles the ability to reason.
The conclusion was this:

A single agent — no matter how intelligent —
is still limited by its own field of view.

Part 2 asks a different question:
what if agents stopped working alone
and started working together?"
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| T01 | Background | `Rectangle` | Fill `NAVY` |
| T02 | Part number "02" | `Text` | Font size 72, `GOLD`, opacity 0.15, background watermark |
| T03 | Title "Towards End-to-End Cooperative Automation" | `Text` | Font size 32, `WHITE`, bold, center |
| T04 | Speaker label | `Text` | Font size 18, `LIGHT_BLUE`, below T03 |
| T05 | Callback quote "Single agent is limited by its own FOV" | `Text` | Font size 20, `WHITE`, italic, opacity 0.8 |
| T06 | Divider line | `Line` | `BLUE`, 8u wide |
| T07 | Roadmap strip (from Scene I-03, scaled down) | `VGroup` | Bottom of screen, Part 02 node highlighted `GOLD` |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(T01, T02)` — background + watermark | 0.4s |
| 2 | 0.4s | `Write(T03)` — title | 1s |
| 3 | 1.4s | `FadeIn(T04)` — speaker | 0.4s |
| 4 | 2s | `Create(T06)` — divider | 0.4s |
| 5 | 2.4s | `FadeIn(T05)` — callback quote, italic | 0.5s |
| 6 | 3s | `FadeIn(T07)` — roadmap strip, Part 02 node pulses `GOLD` | 0.5s |
| 7 | 4s | `[HOLD]` | 1s |

### [NOTES]
- T07 reuses the roadmap `VGroup` from Scene I-03. Scale it to ~15% of screen height and anchor to bottom center. This strip should persist through all Part 02 scenes if layout allows.

---

## SCENE 2-02 — Background: Why This Problem Matters

> **Duration:** ~50s

### [NARRATION]

```
[NARRATOR]

"Before we go into the technical work,
let's anchor why any of this matters.

Every year, 1.19 million people die
in road traffic accidents worldwide.

94% of those deaths are caused by human error.

Waymo recently published data showing
their autonomous vehicles reduce
injury-causing accidents by 80%
compared to human drivers.

And the scope is growing.
Delivery robots are replacing humans
in last-mile logistics —
from Amazon's sidewalk robots
to COCO's campus delivery fleet.

AI agents are reshaping
how we move and how we ship things.

This is why getting multi-agent systems right
is not an academic exercise.
It's a safety problem at scale."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| BG01 | Background | `Rectangle` | Fill `#0A0A0A` (near-black) — signals gravity |
| BG02 | Crowd of human icons (grid 10×5) | `SVGMobject` or `VGroup` of `Dot` | Each icon ~0.3u, `WHITE` |
| BG03 | "1.19 million" counter | `Text` | Font size 44, `RED_MUTED`, bold |
| BG04 | Label "deaths per year" | `Text` | Font size 20, `WHITE` |
| BG05 | "94%" fill overlay on crowd | `Rectangle` covering 94% of BG02 | Fill `RED_MUTED`, opacity 0.55 |
| BG06 | "94% human error" label | `Text` | Font size 22, `RED_MUTED`, bold |
| BG07 | "6%" remaining crowd (un-filled) | Visual leftover from BG02 | `WHITE`, opacity unchanged |
| BG08 | Waymo stat box | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN` |
| BG09 | "80% reduction" text inside BG08 | `Text` | `GREEN`, size 32, bold |
| BG10 | Waymo label | `Text` | `WHITE`, size 14, below BG09 |
| BG11 | Delivery robot icon (COCO) | `SVGMobject` or simple `VGroup` | Right half of screen |
| BG12 | Amazon robot icon | `SVGMobject` or simple `VGroup` | Left of BG11 |
| BG13 | Arrow between robots | `Arrow` | `BLUE`, suggesting movement |
| BG14 | Label "AI reshaping logistics" | `Text` | `WHITE`, size 18, italic |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(BG01)` | 0.3s |
| 2 | 0.3s | `FadeIn(BG02)` — crowd appears | 0.6s, icons pop in row by row |
| 3 | 1s | `CountAnimation` BG03: 0 → 1,190,000 | 1.5s |
| 4 | 2.5s | `FadeIn(BG04)` | 0.3s |
| 5 | 3s | `FadeIn(BG05)` — red overlay sweeps across 94% of crowd | 0.8s, left→right |
| 6 | 3.8s | `Write(BG06)` — "94% human error" | 0.5s |
| 7 | 5s | `FadeIn(BG08, BG09, BG10)` — Waymo stat box slides in from right | 0.6s |
| 8 | 6s | `[HOLD]` | 1s |
| 9 | 7s | Crowd + stat boxes `FadeOut` | 0.4s |
| 10 | 7.4s | `FadeIn(BG11, BG12, BG13, BG14)` — robot section | 0.6s |
| 11 | 8.5s | `[HOLD]` | 1s |

### [NOTES]
- BG02 crowd can be simplified to a 10×5 grid of `Dot` objects if human SVG icons are not available. The visual intent is "a lot of people."
- The 94% fill sweep (BG05) is the emotional peak of this scene. Animate it slowly — ~0.8s — so the proportion registers visually.

---

## SCENE 2-03 — Single-Agent Evolution: Modular → End-to-End

> **Duration:** ~60s

### [NARRATION]

```
[NARRATOR]

"Before talking about multi-agent,
we need to look at the trajectory
of single-agent systems.

There's a clear trend over the past few years:
from modular pipelines toward end-to-end architectures.

Here are the milestones.

PnPNet — 2020 — CNN plus LSTM
for joint perception and prediction.

GameFormer — 2023 — brings interactive prediction
into the planning loop.

UniAD — 2023 — the first system to optimize
the entire pipeline end-to-end simultaneously,
using a query-based design.

DiffusionDrive — 2025 — generates trajectory
using a diffusion model with anchored distribution.

End-to-end has three clear advantages over modular:
no error accumulation between modules,
no information loss at stage boundaries,
and joint optimization — the whole system
learns toward one shared goal.

So — has end-to-end solved everything?"

[PI pops up]

[PI]
"E2E đã giải quyết mọi thứ chưa?"

[NARRATOR]
"Not yet. And the reason is fundamental."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| EV01 | Background | `Rectangle` | Fill `#0F172A` |
| EV02 | Timeline spine | `Line` | `WHITE`, horizontal, 12u wide |
| EV03 | Milestone 1 — "PnPNet \| CVPR'20" | `VGroup`: dot + label + image placeholder | Dot `BLUE` 0.12u, label `WHITE` size 16 |
| EV04 | Milestone 2 — "GameFormer \| ICCV'23" | Same | |
| EV05 | Milestone 3 — "UniAD \| CVPR'23" | Same | |
| EV06 | Milestone 4 — "VAD \| ICCV'23" | Same | |
| EV07 | Milestone 5 — "DiffusionDrive \| CVPR'25" | Same | |
| EV08–EV12 | Sub-labels under each milestone | `Text` | Font size 13, `LIGHT_BLUE`, 2-line max |
| EV13 | "Modular" era bracket | `Brace` or `Line` with label | Left portion of timeline, `RED_MUTED` |
| EV14 | "End-to-End" era bracket | `Brace` or `Line` with label | Right portion, `GREEN` |
| EV15 | Advantages box (3 bullet points) | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN`, bottom-right |
| EV16–EV18 | Advantage lines | `Text` | `WHITE`, size 16, inside EV15 |
| EV19 | `PI` mascot | `SVGMobject` | Bottom-left, question bubble |
| EV20 | Pie chart (Modular vs E2E usage over time) | `AnnularSector` x2 or `PieChart` | Left: modular shrinks, right: E2E grows |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(EV01)` | 0.3s |
| 2 | 0.3s | `Create(EV02)` — spine | 0.6s |
| 3 | 0.9s | `FadeIn(EV03)` — PnPNet node | 0.4s |
| 4 | 1.3s | `FadeIn(EV04)` — GameFormer | 0.4s |
| 5 | 1.7s | `FadeIn(EV05)` — UniAD | 0.4s |
| 6 | 2.1s | `FadeIn(EV06)` — VAD | 0.4s |
| 7 | 2.5s | `FadeIn(EV07)` — DiffusionDrive | 0.4s |
| 8 | 3s | `FadeIn(EV08–EV12)` — sub-labels, staggered | 0.15s each |
| 9 | 4s | `Create(EV13)` — modular era bracket | 0.4s |
| 10 | 4.4s | `Create(EV14)` — e2e era bracket | 0.4s |
| 11 | 5s | `FadeIn(EV15)` — advantages box | 0.4s |
| 12 | 5.4s | `FadeIn(EV16, EV17, EV18)` — bullet points, staggered 0.2s | 0.6s total |
| 13 | 6.5s | `FadeIn(EV19)` — PI with question | 0.4s |
| 14 | 7.5s | `[HOLD]` | 1s |

### [NOTES]
- EV20 (pie chart) is optional — include only if time/complexity permits. The timeline + brackets already tell the modular→E2E story. Pie chart would reinforce it visually.
- Milestone image placeholders: small `Rectangle` 1.5u×1u above each dot, fill `#2A2A2A`, with milestone name as label. Replace with actual slide crops if available.

---

## SCENE 2-04 — The Physics Limit: Occlusion

> **Duration:** ~50s

### [NARRATION]

```
[NARRATOR]

"Look at these two LiDAR scan images
of the same intersection.

Top row: single-agent.
LiDAR scanning from one fixed point.
Large dark regions everywhere —
those are the blind spots.
Occlusions caused by parked vehicles,
buildings, and other obstacles.

Bottom row: same intersection,
but now with a second agent.
The blind spots are dramatically reduced.
What one agent can't see,
the other can — and shares.

This is a physics problem, not a software problem.
No foundation model can see through a truck.
No neural network can perceive
what's behind a corner.

The only solution is
complementary information sharing —
agents sharing what each uniquely sees.

This is where multi-agent systems begin."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| OC01 | Background | `Rectangle` | Fill `#0F172A` |
| OC02 | Label "Single Agent" | `Text` | `WHITE`, size 20, bold, top-left |
| OC03 | LiDAR scan visualization — single agent | `VGroup` | Stylized top-down view: `Circle` for agent, `Arc` sweep, dark `Polygon` for blind zones |
| OC04 | Blind zone fills | `Polygon` x4 | Fill `RED_MUTED`, opacity 0.4 |
| OC05 | Label "Multiple Dark Regions" | `Text` | `RED_MUTED`, size 16, arrow pointing to OC04 |
| OC06 | Divider | `Line` | `WHITE`, opacity 0.3, horizontal |
| OC07 | Label "Multi-Agent" | `Text` | `WHITE`, size 20, bold |
| OC08 | LiDAR scan visualization — multi agent | `VGroup` | Same intersection, 2 `Circle` agents, reduced blind zones |
| OC09 | Reduced blind zones | `Polygon` x2 | Same style as OC04 but smaller |
| OC10 | Coverage gain fill | `Polygon` | Fill `GREEN`, opacity 0.25 — the newly visible area |
| OC11 | Comm link between agents | `DashedLine` | `BLUE`, dashed |
| OC12 | Emphasis text "Physics problem — not algorithm" | `Text` | `GOLD`, size 22, bold |
| OC13 | Conclusion label "Complementary Information Sharing" | `RoundedRectangle` + `Text` | Fill `#1E3A5F`, stroke `BLUE`, size 20 |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(OC01, OC02)` | 0.4s |
| 2 | 0.4s | `Create(OC03)` — single agent scan builds | 1s, sweep arc rotates |
| 3 | 1.4s | `FadeIn(OC04)` — blind zones fill in | 0.5s |
| 4 | 2s | `FadeIn(OC05)` — label with arrow | 0.3s |
| 5 | 2.8s | `Create(OC06)` — divider | 0.3s |
| 6 | 3.1s | `FadeIn(OC07)` — multi-agent label | 0.3s |
| 7 | 3.4s | `Create(OC08)` — second scan view, second agent appears | 0.8s |
| 8 | 4.2s | `FadeIn(OC09)` — smaller blind zones | 0.4s |
| 9 | 4.6s | `FadeIn(OC10)` — green coverage gain | 0.5s, fills slowly |
| 10 | 5.1s | `Create(OC11)` — comm link draws | 0.4s, dashed line grows |
| 11 | 6s | `Write(OC12)` — "Physics problem" | 0.5s, flash |
| 12 | 7s | `FadeIn(OC13)` — conclusion box | 0.5s |
| 13 | 8s | `[HOLD]` | 1.5s |

### [NOTES]
- OC03 and OC08 are stylized, not actual LiDAR screenshots. Build them as `VGroup` of: a `Circle` (agent), several `Arc` objects (scan sweep), and `Polygon` objects (blind zones). Keep it abstract but recognizable.
- OC10 (green fill) is the visual payoff. Animate it with `FadeIn` + slight `rate_func=smooth` so it feels like light filling the scene.

---

## SCENE 2-05 — Related Works & Research Gaps

> **Duration:** ~60s

### [NARRATION]

```
[NARRATOR]

"The research community has been active here.

V2VNet used simple graph neural networks.
V2X-ViT brought transformer-based attention.
Where2comm introduced sparse communication —
only send features that are most relevant.
CodeFilling uses a shared codebook
for efficient feature compression.

Datasets followed a similar arc:
from simulation — OPV2V in 2022 —
to real-world: V2X-Real in 2024.

But two critical gaps remain unaddressed
across all of this work.

The first gap is in the models.
Every single one of these systems
only does cooperative perception —
detect objects, then stop.
How to benefit prediction and planning
from cooperation is still open.
And — all of them are single-frame.
They ignore temporal context entirely.
Without knowing how an object has been moving,
your prediction of where it's going is severely limited.

The second gap is in the data.
Existing datasets lack sequential data
and HD maps needed for downstream tasks.
Most only support V2V or V2I separately —
no dataset covers all V2X collaboration modes together.

These two gaps are exactly what this part addresses."
```

### [VISUAL SPEC]

**Section A: Related Works Timeline**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| RW01 | Background | `Rectangle` | Fill `#0F172A` |
| RW02 | Timeline spine | `Line` | `WHITE`, horizontal |
| RW03–RW09 | 7 paper nodes on timeline | `Dot` + label above/below | Alternating above/below, `BLUE` dots |
| RW10–RW16 | Node labels (paper name + venue + year) | `Text` | Font size 14, `WHITE` |
| RW17–RW20 | Method category tags | `RoundedRectangle` | Color-coded: GNN=`BLUE`, Attn=`PURPLE`, Sparse=`GREEN`, Codebook=`GOLD` |
| RW21 | "Simulation Data" bracket | `Brace` | Left side of timeline, `RED_MUTED` |
| RW22 | "Real-World Data" bracket | `Brace` | Right side, `GREEN` |

**Section B: Gap Cards**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| GA01 | Gap card 1 | `RoundedRectangle` | Fill `#2A1A1A`, stroke `RED_MUTED`, 4u×3u |
| GA02 | Gap 1 header "Model Gap" | `Text` | `RED_MUTED`, size 20, bold |
| GA03 | Gap 1 bullet 1 | `Text` | `WHITE`, size 16 — "Only cooperative perception, not prediction/planning" |
| GA04 | Gap 1 bullet 2 | `Text` | `WHITE`, size 16 — "Single-frame only — no temporal context" |
| GA05 | Gap card 2 | `RoundedRectangle` | Same style, right of GA01 |
| GA06 | Gap 2 header "Data Gap" | `Text` | `RED_MUTED`, size 20, bold |
| GA07 | Gap 2 bullet 1 | `Text` | `WHITE`, size 16 — "No sequential data / HD maps" |
| GA08 | Gap 2 bullet 2 | `Text` | `WHITE`, size 16 — "Only V2V or V2I, never all modes together" |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(RW01)` | 0.3s |
| 2 | 0.3s | `Create(RW02)` | 0.5s |
| 3 | 0.8s | Nodes + labels appear left→right, staggered 0.2s | 1.4s total |
| 4 | 2.2s | `FadeIn(RW17–RW20)` — category tags appear | 0.3s each |
| 5 | 3s | `Create(RW21, RW22)` — brackets | 0.4s each |
| 6 | 4s | `[HOLD]` | 0.8s |
| 7 | 4.8s | Timeline `FadeOut` | 0.4s |
| 8 | 5.2s | `FadeIn(GA01, GA02)` — gap card 1 | 0.5s |
| 9 | 5.7s | `FadeIn(GA03, GA04)` — bullets, staggered 0.2s | 0.4s |
| 10 | 6.5s | `FadeIn(GA05, GA06)` — gap card 2 | 0.5s |
| 11 | 7s | `FadeIn(GA07, GA08)` — bullets | 0.4s |
| 12 | 8s | Both gap cards pulse once: `scale(1.05) → scale(1.0)` | 0.4s |
| 13 | 9s | `[HOLD]` | 1.5s |

---

## SCENE 2-06 — The Three Core Questions

> **Duration:** ~30s

### [NARRATION]

```
[NARRATOR]

"When you introduce temporal dimension
into a multi-agent system,
three fundamental questions arise.

What to transmit?
When to transmit?
How to fuse?

These are the questions V2XPnP was built to answer."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| Q01 | Background | `Rectangle` | Fill `NAVY` |
| Q02 | "Multi-Agent" label | `Text` | `WHITE`, size 22 |
| Q03 | "+" | `Text` | `WHITE` |
| Q04 | "Multi-Frame" label | `Text` | `WHITE`, size 22 |
| Q05 | "+" | `Text` | `WHITE` |
| Q06 | "Multi-Task" label | `Text` | `WHITE`, size 22 |
| Q07 | Arrow down from label group | `Arrow` | `BLUE` |
| Q08 | Three question boxes in a row | `RoundedRectangle` x3 | Fill `#1E3A5F`, stroke `BLUE`, each 3u×1.5u |
| Q09 | "What to transmit?" | `Text` inside Q08[0] | `GOLD`, size 20, bold |
| Q10 | "When to transmit?" | `Text` inside Q08[1] | `GOLD`, size 20, bold |
| Q11 | "How to fuse?" | `Text` inside Q08[2] | `GOLD`, size 20, bold |
| Q12 | "→ V2XPnP" answer label | `Text` | `WHITE`, size 18, below Q08 |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(Q01)` | 0.3s |
| 2 | 0.3s | `Write(Q02, Q03, Q04, Q05, Q06)` — left to right, staggered | 0.8s total |
| 3 | 1.1s | `GrowArrow(Q07)` | 0.3s |
| 4 | 1.4s | `FadeIn(Q08[0], Q09)` — "What" | 0.3s |
| 5 | 1.7s | `FadeIn(Q08[1], Q10)` — "When" | 0.3s |
| 6 | 2.0s | `FadeIn(Q08[2], Q11)` — "How" | 0.3s |
| 7 | 3s | `Write(Q12)` — answer label | 0.4s |
| 8 | 4s | `[HOLD]` | 1s |

---

## SCENE 2-07 — V2XPnP: Research Problem 1

> **Duration:** ~120s

### [NARRATION]

```
[NARRATOR]

"V2XPnP — Vehicle-to-Everything
Perception and Prediction —
is the UCLA lab's answer to Research Problem 1.

Let's go through the three questions."

--- WHAT TO TRANSMIT ---

[NARRATOR]
"What to transmit?

V2XPnP considers all three fusion strategies.

Early fusion: agents share raw LiDAR point clouds —
maximum information, maximum bandwidth cost.

Intermediate fusion: agents share BEV feature maps —
processed representations, more compact.

Late fusion: agents share detected bounding boxes —
minimal data, but information has already been filtered.

The key difference from all prior work:
in V2XPnP, all three variants include temporal dimension —
each agent doesn't share one frame,
but a compressed history across multiple frames."

--- WHEN TO TRANSMIT ---

[NARRATOR]
"When to transmit?

The naive approach: transmit frame by frame
as long as agents are in communication range.
Multi-step communication.

The problem: two vehicles are not always close to each other.
When the distance is small enough to communicate —
that is the only window of opportunity.
Once the other vehicle drives away, the window closes.

V2XPnP's solution: one-step communication.
When agents are within range,
transmit the entire history at once.
All N frames, in one message.

Of course, sending N raw frames would be expensive.
So temporal attention compresses
the full history into a single-frame-sized representation
before transmission — preserving the temporal context
at the cost of a single message."

--- HOW TO FUSE ---

[NARRATOR]
"How to fuse?

Two attention modules, applied in sequence.

First: temporal attention.
Processes each agent's own movement history independently.
Produces a temporally-aware feature for each agent.

Second: spatial attention.
Fuses information across all agents at the same time step.
Combines what each agent individually understood
into one shared multi-agent spatio-temporal representation.

That representation feeds directly
into detection and prediction simultaneously."
```

### [VISUAL SPEC]

This scene is split into three sub-scenes, one per question.

---

**Sub-scene A: What to Transmit**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| W01 | Section label "Q1: What to Transmit?" | `Text` | `GOLD`, size 22, top-left |
| W02 | Agent 1 box | `RoundedRectangle` | Fill `#1E3A5F`, label "Agent 1" |
| W03 | Agent 2 box | `RoundedRectangle` | Same, "Agent 2", right side |
| W04 | Three transmission arrows (stacked vertically) | `Arrow` x3 | Between W02 and W03 |
| W05 | Arrow label 1 "Early: Raw LiDAR" | `Text` | `RED_MUTED`, size 15 |
| W06 | Arrow label 2 "Intermediate: BEV Features" | `Text` | `BLUE`, size 15 |
| W07 | Arrow label 3 "Late: Bounding Boxes" | `Text` | `GREEN`, size 15 |
| W08 | Temporal dimension badge on each arrow | `RoundedRectangle` | Fill `GOLD`, text "+ N frames", size 13 |
| W09 | "Key: all 3 include temporal dimension" note | `Text` | `GOLD`, italic, size 16, bottom |

**Sub-scene B: When to Transmit**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| WT01 | Section label "Q2: When to Transmit?" | `Text` | `GOLD`, size 22 |
| WT02 | Road/path visualization | `Line` | `WHITE`, long horizontal |
| WT03 | Car A icon | `SVGMobject` or `VGroup` | Left, moving right |
| WT04 | Car B icon | `SVGMobject` or `VGroup` | Right, moving left |
| WT05 | "Communication window" zone | `Rectangle` | Fill `GREEN`, opacity 0.2, narrow vertical band at center |
| WT06 | Window label "Only chance to communicate" | `Text` | `GREEN`, size 16, above WT05 |
| WT07 | ✗ "Multi-step" option | `RoundedRectangle` | Fill `#2A1A1A`, stroke `RED_MUTED` |
| WT08 | Multi-step label | `Text` | `RED_MUTED`, size 16 — "Unstable — cars move apart" |
| WT09 | ✓ "One-step" option | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN` |
| WT10 | One-step label | `Text` | `GREEN`, size 16 — "Transmit all N frames at once" |
| WT11 | Compression note | `Text` | `LIGHT_BLUE`, size 14 — "Temporal attention compresses N frames → 1" |

**Sub-scene C: How to Fuse**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| HF01 | Section label "Q3: How to Fuse?" | `Text` | `GOLD`, size 22 |
| HF02 | Agent block with N-frame history | `VGroup` of stacked `Rectangle` | Depth effect, each rect slightly offset, `NAVY` |
| HF03 | "Temporal Attention" module | `RoundedRectangle` | Fill `#2D1B69`, stroke `PURPLE`, label |
| HF04 | Arrow HF02 → HF03 | `Arrow` | `BLUE` |
| HF05 | Per-agent temporal feature | `Rectangle` | Fill `#1E3A5F`, slimmer, output of HF03 |
| HF06 | "Spatial Attention" module | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN`, label |
| HF07 | Arrow HF05 → HF06 (multiple agents converging) | `Arrow` x2 | `GREEN` |
| HF08 | "Multi-Agent Spatio-Temporal Representation" output | `RoundedRectangle` | Fill `GOLD`, text `NAVY`, bold |
| HF09 | Fork arrows to Detection + Prediction | `Arrow` x2 | `WHITE` |
| HF10 | "Detection" output box | `RoundedRectangle` | Fill `#1E3A5F` |
| HF11 | "Prediction" output box | `RoundedRectangle` | Fill `#1E3A5F` |

### [ANIMATION]

**Sub-scene A (0–25s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(W01, W02, W03)` | 0.5s |
| 2 | 0.5s | `GrowArrow(W04[0])` + `FadeIn(W05)` — Early fusion | 0.4s |
| 3 | 1s | `GrowArrow(W04[1])` + `FadeIn(W06)` — Intermediate | 0.4s |
| 4 | 1.5s | `GrowArrow(W04[2])` + `FadeIn(W07)` — Late | 0.4s |
| 5 | 2.2s | `FadeIn(W08)` x3 — temporal badges appear | 0.3s |
| 6 | 3s | `Write(W09)` — note | 0.4s |
| 7 | 4s | `[HOLD]` | 1s |

**Sub-scene B (0–30s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(WT01, WT02)` | 0.4s |
| 2 | 0.4s | Cars WT03, WT04 animate toward each other | 1.5s, `MoveAlongPath` |
| 3 | 1.9s | `FadeIn(WT05, WT06)` — window zone appears | 0.4s |
| 4 | 2.5s | `FadeIn(WT07, WT08)` — multi-step option with ✗ | 0.4s |
| 5 | 3.2s | `FadeIn(WT09, WT10)` — one-step option with ✓ | 0.4s |
| 6 | 4s | `Write(WT11)` — compression note | 0.4s |
| 7 | 5s | `[HOLD]` | 1.5s |

**Sub-scene C (0–35s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(HF01)` | 0.3s |
| 2 | 0.3s | `FadeIn(HF02)` — N-frame stack | 0.5s, frames appear staggered top→bottom |
| 3 | 0.8s | `GrowArrow(HF04)` + `FadeIn(HF03)` — temporal attention | 0.5s |
| 4 | 1.5s | `FadeIn(HF05)` — compressed per-agent feature | 0.4s |
| 5 | 2s | `GrowArrow(HF07)` + `FadeIn(HF06)` — spatial attention, 2nd agent converges | 0.6s |
| 6 | 3s | `FadeIn(HF08)` — final representation | 0.5s, slight glow effect `set_stroke(GOLD, width=4)` |
| 7 | 3.8s | `GrowArrow(HF09[0])` + `FadeIn(HF10)` — detection | 0.4s |
| 8 | 4.2s | `GrowArrow(HF09[1])` + `FadeIn(HF11)` — prediction | 0.4s |
| 9 | 5s | `[HOLD]` | 1.5s |

### [NOTES]
- HF02 (N-frame stack): simulate depth by drawing 3–4 rectangles slightly offset in both x and y (+0.1u each). This is a common 3D-stack effect in Manim using `VGroup`.
- The three sub-scenes should each occupy full screen. Use a brief 0.2s dark flash between sub-scenes as a separator.

---

## SCENE 2-08 — V2XPnP-Seq Dataset

> **Duration:** ~35s

### [NARRATION]

```
[NARRATOR]

"Alongside the framework,
the team built V2XPnP-Seq —
the first large-scale real-world dataset
supporting all V2X collaboration modes
simultaneously: V2V, V2I, and I2I.

Two connected vehicles.
Two infrastructure nodes.
40,000 LiDAR frames.
208,000 camera frames.
HD maps and trajectory annotations included.

Previously, researchers had to choose
between simulation data or real-world data,
and between V2V or V2I.
V2XPnP-Seq removes those constraints."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| DS01 | Background | `Rectangle` | Fill `#0F172A` |
| DS02 | Dataset name | `Text` | `GOLD`, size 26, bold |
| DS03 | "First real-world V2X sequential dataset" | `Text` | `WHITE`, size 18 |
| DS04 | Map top-down view placeholder | `Rectangle` | 4u×3u, Fill `#1A2A3A`, stroke `BLUE` — simulated map |
| DS05 | Road lines on map | `Line` x4 | `WHITE`, opacity 0.5 |
| DS06 | Vehicle icons on map (x2) | `SVGMobject` or colored `Dot` | `BLUE` |
| DS07 | Infrastructure node icons (x2) | `SVGMobject` or `Square` | `GOLD` |
| DS08 | Communication lines V2V, V2I, I2I | `DashedLine` x3 | Color-coded: `BLUE`, `GREEN`, `GOLD` |
| DS09 | Stats box | `VGroup` of `RoundedRectangle` + `Text` | Right side, 4 stat items |
| DS10 | Stat: "40K LiDAR frames" | `Text` | `WHITE`, size 16 |
| DS11 | Stat: "208K camera frames" | `Text` | `WHITE`, size 16 |
| DS12 | Stat: "HD maps + trajectories" | `Text` | `WHITE`, size 16 |
| DS13 | Stat: "All V2X modes" | `Text` | `GREEN`, size 16, bold |
| DS14 | Comparison timeline strip | Small `VGroup` | Bottom — prior datasets labeled "Sim only" / "V2V only" vs DS02 "All modes" |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(DS01)`, `Write(DS02, DS03)` | 0.6s |
| 2 | 0.6s | `FadeIn(DS04, DS05)` — map | 0.5s |
| 3 | 1.1s | `FadeIn(DS06, DS07)` — agents | 0.4s |
| 4 | 1.5s | `Create(DS08)` x3 — comm lines draw | 0.4s each, staggered |
| 5 | 2.5s | `FadeIn(DS09–DS13)` — stats, staggered 0.2s | 0.8s total |
| 6 | 4s | `FadeIn(DS14)` — comparison strip | 0.4s |
| 7 | 5s | `[HOLD]` | 1.5s |

---

## SCENE 2-09 — TurboTrain: Research Problem 2

> **Duration:** ~90s

### [NARRATION]

```
[NARRATOR]

"Research Problem 2:
how do you train this kind of complex framework
efficiently with limited data?

Look at this scatter plot.
X-axis: AP at 0.5 — detection accuracy.
Y-axis: EPA — prediction accuracy.

The orange dots are one-time training attempts.
Random initialization. Single run.
Performance is low — or fails completely.

The blue dots are the manual 4-stage approach:
Stage 1 — single-agent detection.
Stage 2 — temporal prediction.
Stage 3 — joint tuning.
Stage 4 — multi-agent fusion.
Each stage is a separate training run.
120 epochs total.

Two reasons why this system is hard to train.

First: the architecture is complex
across many dimensions simultaneously.
This makes the model extremely sensitive to initialization.
A bad starting point and training collapses — orange dots.

Second: gradient conflict.
Different tasks pull the model in opposite directions
in weight space.
Improve detection — prediction degrades.
Improve prediction — detection drops.
Without a balancing mechanism,
multi-task learning is unstable.

TurboTrain solves both with a 2-stage pipeline —
replacing all four manual stages."

--- STAGE 1 ---

[NARRATOR]
"Stage 1: Pretrain.

The model learns a task-agnostic 4D representation —
4D because it covers 3D space plus time —
by reconstructing masked LiDAR point clouds.

No annotations needed.
No task-specific objective.
Just: learn the spatiotemporal structure of the environment.
This gives the model a stable initialization
before any task-specific training begins."

--- STAGE 2 ---

[NARRATOR]
"Stage 2: Balance.

Fine-tuning with a hybrid training strategy
that alternates between two types of gradient steps.

Free gradient steps: all tasks learn simultaneously,
with no interference.

Conflict-suppressing steps: the optimizer detects
when tasks are pulling against each other
and applies a correction to reduce that conflict.

The result on the chart:
TurboTrain achieves the highest combined performance
in roughly 45 epochs —
less than half the compute of the manual 4-stage approach.
And no human expertise needed to decide when to switch stages."
```

### [VISUAL SPEC]

**Section A: Scatter Plot**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| TT01 | Background | `Rectangle` | Fill `#0A0A0A` |
| TT02 | Scatter plot axes | `Axes` | `WHITE`, x="AP@0.5", y="EPA" |
| TT03 | Orange dots (failed one-time runs) | `Dot` x8 | `#E8A838`, radius 0.08u, clustered low-left |
| TT04 | Blue dots (manual 4-stage) | `Dot` x5 | `BLUE`, radius 0.08u, mid-range |
| TT05 | Gold star (TurboTrain result) | `Star` or `Dot` | `GOLD`, radius 0.12u, top-right |
| TT06 | Legend box | `VGroup` | Top-left corner |
| TT07 | Epoch label near TT05 "~45 epochs" | `Text` | `GOLD`, size 14 |
| TT08 | Epoch label near TT04 "~120 epochs" | `Text` | `BLUE`, size 14 |

**Section B: TurboTrain Pipeline**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| TP01 | Header "TurboTrain" | `Text` | `GOLD`, size 26, bold |
| TP02 | "Stage 1: Pretrain" box | `RoundedRectangle` | Fill `#1E3A5F`, stroke `BLUE`, 5u×2u |
| TP03 | Stage 1 label detail | `Text` | `WHITE`, size 15 — "Masked LiDAR reconstruction" |
| TP04 | "Task-agnostic 4D representation" tag | `RoundedRectangle` | Fill `BLUE`, text `WHITE`, size 13 |
| TP05 | Arrow Stage 1 → Stage 2 | `Arrow` | `WHITE` |
| TP06 | "Stage 2: Balance" box | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN`, 5u×2u |
| TP07 | Stage 2 label detail | `Text` | `WHITE`, size 15 — "Hybrid gradient strategy" |
| TP08 | Sub-label A "Free gradient steps" | `Text` | `LIGHT_BLUE`, size 13 |
| TP09 | Sub-label B "Conflict-suppressing steps" | `Text` | `GREEN`, size 13 |
| TP10 | Alternating gradient animation | Two `Arrow` objects | `BLUE` and `GREEN`, alternating |
| TP11 | Comparison summary box | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN` |
| TP12 | "45 epochs vs 120 epochs" | `Text` | `GREEN`, size 20, bold, inside TP11 |
| TP13 | "No human expertise needed" | `Text` | `WHITE`, size 16, inside TP11 |

### [ANIMATION]

**Scatter plot (0–30s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `Create(TT02)` — axes | 0.6s |
| 2 | 0.6s | `FadeIn(TT03)` — orange dots, staggered | 0.8s, pop in randomly |
| 3 | 1.4s | `FadeIn(TT04)` — blue dots, staggered | 0.6s |
| 4 | 2s | `FadeIn(TT06)` — legend | 0.3s |
| 5 | 3s | `FadeIn(TT07, TT08)` — epoch labels | 0.3s each |
| 6 | 4s | `[HOLD]` | 1s (let the visual sink in) |

**TurboTrain pipeline (0–40s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `Write(TP01)` | 0.5s |
| 2 | 0.5s | `FadeIn(TP02, TP03, TP04)` — Stage 1 | 0.6s |
| 3 | 2s | `GrowArrow(TP05)` | 0.3s |
| 4 | 2.3s | `FadeIn(TP06, TP07)` — Stage 2 | 0.6s |
| 5 | 3s | `FadeIn(TP08, TP09)` — sub-labels | 0.3s each |
| 6 | 3.8s | `TP10` alternating arrow animation: blue arrow → green arrow → blue → green | 1.5s, 2 cycles |
| 7 | 5.5s | `FadeIn(TT05)` — TurboTrain star on scatter plot | 0.5s, pop with slight scale effect |
| 8 | 6.2s | `FadeIn(TP11, TP12, TP13)` — result box | 0.6s |
| 9 | 7.5s | `[HOLD]` | 2s |

### [NOTES]
- TT05 (gold star) should be introduced on the scatter plot after the pipeline explanation, not before. The reveal order matters: show the problem → explain the solution → then show it works.
- TP10 alternating arrows: build as a `Succession` of two `GrowArrow` → `FadeOut` animations to simulate the alternating strategy.

---

## SCENE 2-10 — RiskMap: Research Problem 3

> **Duration:** ~75s

### [NARRATION]

```
[NARRATOR]

"Research Problem 3:
how do you extend spatio-temporal fusion
from perception and prediction
all the way to planning?

Three paradigms. Look at them."

[Diagram appears]

[NARRATOR]
"(a) Modular.
Error accumulation across stages.
Limited perception range.
Known problems — we've been over this.

(b) Conventional end-to-end.
Sensors go in. Actions come out. Black box.
When it goes wrong — and it will —
you have no idea why.
Safety verification is nearly impossible.

(c) The proposed approach — RiskMap.

Instead of letting the model decide in a black box,
introduce a Risk Map as explicit middleware.

A Risk Map is a spatiotemporal risk distribution —
a map that encodes the probability of danger
at each location, at each future time step.

Then a learning-based MPC module —
Model Predictive Control —
takes that Risk Map and computes a safe trajectory.

Why does the intermediate Risk Map matter?
Because it separates two very different questions.

'Where is this environment dangerous?'
That's a perception and prediction question. AI is good at this.

'Given those dangers, what path should I take?'
That's a planning question. It can be verified,
interpreted, and constrained for safety.

RiskMap outperforms all state-of-the-art
fusion methods and planning models
on detection, prediction, and planning simultaneously."
```

### [VISUAL SPEC]

Three-row diagram layout (paradigm a, b, c).

| ID | Object | Manim Class | Style |
|---|---|---|---|
| RM01 | Background | `Rectangle` | Fill `#0A0A0A` |
| RM02 | Row label "(a) Modular" | `Text` | `WHITE`, size 18 |
| RM03 | Modular pipeline row | `VGroup` of boxes + arrows | Compact, same style as Scene 1-03 — small scale |
| RM04 | ✗ Badge | `Text` + circle | `RED_MUTED` |
| RM05 | Row label "(b) Conv. E2E" | `Text` | `WHITE`, size 18 |
| RM06 | Sensor box | `RoundedRectangle` | `#1E3A5F` |
| RM07 | Arrow → Black Box | `Arrow` | `BLUE` |
| RM08 | Black Box | `RoundedRectangle` | Fill `#111111`, stroke `RED_MUTED`, label "Black Box" |
| RM09 | Arrow → Action | `Arrow` | `BLUE` |
| RM10 | Action box | `RoundedRectangle` | Fill `#1B4332` |
| RM11 | ✗ Badge "Safety Verification Impossible" | `Text` | `RED_MUTED`, size 14 |
| RM12 | Row label "(c) RiskMap" | `Text` | `GOLD`, size 18, bold |
| RM13 | Multi-agent sensor block | `VGroup` | Left, multiple agents indicated |
| RM14 | Arrow → | `Arrow` | `BLUE` |
| RM15 | "Risk Map" box | `RoundedRectangle` | Fill `#3D1A00`, stroke `GOLD`, label "Risk Map\n(spatiotemporal risk)" |
| RM16 | Arrow → | `Arrow` | `GOLD` |
| RM17 | "Learning-based MPC" box | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN` |
| RM18 | Arrow → | `Arrow` | `GREEN` |
| RM19 | Trajectory output | `RoundedRectangle` | Fill `GREEN`, label "Safe Trajectory" |
| RM20 | ✓ Badge "Interpretable + Safe" | `Text` | `GREEN`, size 14 |
| RM21 | Annotation: "Where is it dangerous?" | `Text` | `LIGHT_BLUE`, curved arrow to RM15 |
| RM22 | Annotation: "What path to take?" | `Text` | `GREEN`, curved arrow to RM17 |
| RM23 | Result bar: "Best on detection + prediction + planning" | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN`, bottom |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(RM01)` | 0.3s |
| 2 | 0.3s | `FadeIn(RM02, RM03, RM04)` — row (a) | 0.6s |
| 3 | 1.2s | `FadeIn(RM05, RM06, RM07, RM08, RM09, RM10, RM11)` — row (b) | 0.6s |
| 4 | 2s | `[HOLD]` — pause on the two bad paradigms | 0.8s |
| 5 | 2.8s | `Write(RM12)` — "(c) RiskMap" in gold | 0.5s |
| 6 | 3.3s | `FadeIn(RM13, RM14)` | 0.4s |
| 7 | 3.7s | `FadeIn(RM15)` — Risk Map box | 0.5s, slight glow |
| 8 | 4.2s | `GrowArrow(RM16)` + `FadeIn(RM17)` | 0.5s |
| 9 | 4.7s | `GrowArrow(RM18)` + `FadeIn(RM19)` | 0.5s |
| 10 | 5.5s | `FadeIn(RM20)` — ✓ badge | 0.3s |
| 11 | 6s | `FadeIn(RM21)` — annotation 1 | 0.3s |
| 12 | 6.4s | `FadeIn(RM22)` — annotation 2 | 0.3s |
| 13 | 7.2s | `FadeIn(RM23)` — result bar | 0.5s |
| 14 | 8.5s | `[HOLD]` | 2s |

### [NOTES]
- RM15 glow: use `set_stroke(GOLD, width=6)` with a brief `rate_func=there_and_back` scale to draw attention. The Risk Map is the conceptual novelty of the whole paradigm.
- The split between RM21/RM22 annotations is the key insight — spend ~1s of narration time on each. Don't rush it.

---

## SCENE 2-11 — Summary: Three Problems, Three Solutions

> **Duration:** ~35s

### [NARRATION]

```
[NARRATOR]

"Three problems — three solutions —
one coherent stack.

V2XPnP builds the foundation:
a real-world dataset and a framework
that answers what, when, and how
for spatio-temporal fusion.

TurboTrain makes it trainable:
2-stage pretrain-then-balance,
replacing manual 4-stage pipelines
with less than half the compute.

RiskMap extends it to planning:
making the output interpretable,
verifiable, and safety-constrained.

Together, they form the first cooperative
end-to-end autonomous driving stack
that works from raw sensors to safe trajectory."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| SU01 | Background | `Rectangle` | Fill `NAVY` |
| SU02 | Three cards laid out horizontally | `RoundedRectangle` x3 | Each 3.5u×4u |
| SU03 | Card 1 header "V2XPnP" | `Text` | `GOLD`, size 22, bold |
| SU04 | Card 1 body | `Text` | `WHITE`, size 15 — "Dataset + What/When/How framework" |
| SU05 | Card 1 icon | Simple `VGroup` | Two agents connected by arc |
| SU06 | Card 2 header "TurboTrain" | `Text` | `GOLD`, size 22, bold |
| SU07 | Card 2 body | `Text` | `WHITE`, size 15 — "2-stage: Pretrain + Balance" |
| SU08 | Card 2 icon | Simple `VGroup` | Two-step pipeline arrow |
| SU09 | Card 3 header "RiskMap" | `Text` | `GOLD`, size 22, bold |
| SU10 | Card 3 body | `Text` | `WHITE`, size 15 — "Interpretable planning via Risk Map middleware" |
| SU11 | Card 3 icon | Simple `VGroup` | Risk Map heatmap sketch |
| SU12 | Connecting arrows between cards | `Arrow` x2 | `BLUE`, card1→card2→card3 |
| SU13 | Bottom label "Cooperative E2E AD Stack" | `Text` | `GOLD`, size 20, italic |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(SU01)` | 0.3s |
| 2 | 0.3s | `FadeIn(SU02[0], SU03, SU04, SU05)` — V2XPnP card | 0.5s |
| 3 | 1s | `GrowArrow(SU12[0])` | 0.3s |
| 4 | 1.3s | `FadeIn(SU02[1], SU06, SU07, SU08)` — TurboTrain card | 0.5s |
| 5 | 2s | `GrowArrow(SU12[1])` | 0.3s |
| 6 | 2.3s | `FadeIn(SU02[2], SU09, SU10, SU11)` — RiskMap card | 0.5s |
| 7 | 3.5s | `Write(SU13)` — bottom label | 0.5s |
| 8 | 4.5s | All three cards pulse simultaneously | 0.4s |
| 9 | 5.5s | `[HOLD]` | 1.5s |

---

## SCENE 2-12 — Bridge to Part 03

> **Duration:** ~25s

### [NARRATION]

```
[NARRATOR]

"We now have a complete cooperative stack —
from multi-agent perception
through to interpretable planning.

But there's a prerequisite we haven't touched.

To train a model that actually runs in the real world,
you need two things:
real sensor data collected on real roads,
and a simulation environment good enough
to generate enough training scenarios.

The gap between simulation and reality
is where a lot of this breaks down in practice.

That gap — and how to bridge it —
is exactly what Part 3 is about."

[CAR mascot]
"Sim-to-Real. Let's go."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| BR01 | Background | `Rectangle` | Fill `NAVY` |
| BR02 | Left panel: Simulation world | `RoundedRectangle` | Fill `#1A2A3A`, stroke `BLUE`, 4u×3u |
| BR03 | "Simulation" label | `Text` | `BLUE`, size 18 |
| BR04 | Simulated scene elements | Simple `VGroup` | Grid roads, boxes for buildings |
| BR05 | Right panel: Real world | `RoundedRectangle` | Fill `#1A1A1A`, stroke `GREEN`, 4u×3u |
| BR06 | "Reality" label | `Text` | `GREEN`, size 18 |
| BR07 | Real scene placeholder | `Rectangle` | Fill `#2A2A2A` — image placeholder |
| BR08 | Bridge arc between panels | `ArcBetweenPoints` | `GOLD`, thick |
| BR09 | Gap indicator | `Text` | `RED_MUTED`, size 18 — "GAP" with double arrow |
| BR10 | "Part 03: Bridging Sim and Reality" | `Text` | `GOLD`, size 24, bold |
| BR11 | `CAR` mascot | `SVGMobject` | Bottom-right, speech bubble "Let's go." |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(BR01)` | 0.3s |
| 2 | 0.3s | `FadeIn(BR02, BR03, BR04)` — sim panel | 0.5s |
| 3 | 0.8s | `FadeIn(BR05, BR06, BR07)` — real panel | 0.5s |
| 4 | 1.5s | `Create(BR08)` — bridge arc | 0.6s |
| 5 | 2.1s | `FadeIn(BR09)` — "GAP" | 0.3s |
| 6 | 3s | `Write(BR10)` — Part 03 title | 0.6s |
| 7 | 4s | `FadeIn(BR11)` — CAR mascot with speech | 0.4s |
| 8 | 5s | `[HOLD]` | 1s |
| 9 | 6s | Transition fade to Part 03 title card | 0.5s |

---

## End of Session 2 (Part 02)

> **Next file:** `spec_part03.md`
> **Scenes covered:** 2-01 through 2-12
> **Total estimated duration:** ~10 min

---

*Production note: Part 02 has three technical "deep dive" scenes (2-07, 2-09, 2-10). These are the densest in terms of visual elements. If the full spec is too heavy for a first pass, prioritize the architecture diagrams in 2-07 (Sub-scene C: How to Fuse) and 2-10 (RiskMap paradigm rows) — they carry the most conceptual weight.*
