# Beyond Self-Driving — Production Spec
## Session 5 of 5: Part 05 — Building Scalable, Human-Centric Physical AI Systems

> **Original speaker:** Wayne Wu, Research Associate, UCLA
> **Reference slides:** (no PDF uploaded — work from script)
> **Estimated duration:** ~12 min
> **Tone note:** Part 05 is the widest in scope. The narrative deliberately zooms out from "cars" to "any physical AI in any environment with humans." Visuals should feel expansive — more populated scenes, more agent types, more human presence. This is also the emotional conclusion of the entire tutorial, so the final scene carries extra weight.

---

## Quick Reference

Same conventions as Sessions 1–4.

**Part 05 additional colors:**

| Name | Hex | Used for |
|---|---|---|
| `PEDESTRIAN` | `#F39C12` | Human figures in scenes |
| `ROBOT_TEAL` | `#1ABC9C` | Non-car robot agents (delivery robots, quadrupeds) |
| `SIM_PURPLE` | `#9B59B6` | Simulation environments (MetaUrban, UrbanSim) |
| `MESH_GRAY` | `#7F8C8D` | Physical mesh / collision geometry |

---
---

## SCENE 5-01 — Title & Scope Expansion

> **Duration:** ~30s

### [NARRATION]

```
[NARRATOR]

"Part 5. Building Scalable, Human-Centric
Physical AI Systems.
Speaker: Wayne Wu, UCLA.

Four parts built a complete stack for autonomous vehicles —
foundation model reasoning, V2X cooperation,
real-world deployment, efficient inference.

This part steps out of the car entirely.

The question is no longer
'how do we make self-driving better?'

The question is:
'how does AI operate safely
in any physical environment —
alongside humans?'

This is Physical AI
in the broadest sense of the term."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| T01 | Background | `Rectangle` | Fill `NAVY` |
| T02 | Part number "05" watermark | `Text` | Font size 72, `GOLD`, opacity 0.15 |
| T03 | Title text | `Text` | Font size 30, `WHITE`, bold, center |
| T04 | Speaker label | `Text` | Font size 18, `LIGHT_BLUE` |
| T05 | Divider | `Line` | `BLUE`, 8u wide |
| T06 | Scope transition visual | `VGroup` | Car icon shrinks left → surrounding scene expands: robots, pedestrians, scooters, wheelchairs |
| T07 | "Physical AI" label (large) | `Text` | `GOLD`, size 36, bold, fades in center |
| T08 | Roadmap strip | `VGroup` (reused) | Bottom, Part 05 node highlighted `GOLD` — all 5 nodes now lit |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(T01, T02)` | 0.4s |
| 2 | 0.4s | `Write(T03)` | 1s |
| 3 | 1.4s | `FadeIn(T04)` | 0.3s |
| 4 | 1.7s | `Create(T05)` | 0.3s |
| 5 | 2s | `FadeIn(T06)` — car icon alone, then scene expands around it | 1.2s, each new agent type pops in 0.2s apart |
| 6 | 3.5s | `Write(T07)` — "Physical AI" | 0.8s, wide reveal |
| 7 | 4.5s | `FadeIn(T08)` — roadmap, all nodes light up sequentially | 0.8s |
| 8 | 5.5s | `[HOLD]` | 1s |

### [NOTES]
- T06 is the visual transition that marks Part 05's scope. The car should be centered first, then robots, pedestrians, and scooters fade in around it, then the car itself shrinks and moves to equal footing with the others. Nobody is the main character anymore.
- T08: for the first time in the series, all 5 roadmap nodes light up `GOLD` simultaneously — signaling we've reached the final chapter. This should feel like a satisfying reveal.

---

## SCENE 5-02 — The Physical AI Vision

> **Duration:** ~45s

### [NARRATION]

```
[NARRATOR]

"Imagine a general-purpose Physical AI.
An agent that operates in any environment,
performs any task,
adapts to any condition.

This sounds like science fiction.
But look at what large language models
have done with language.

LLMs work because of one specific reason:
web-scale data.
The entire internet — trillions of tokens —
as training signal.
From that, they learned world knowledge,
reasoning, and common sense.

Why can't we do the same
for physical intelligence?"

[PI mascot]

[PI]
"Tại sao không thể làm tương tự?"

[NARRATOR]
"Because Physical AI faces two barriers
that language never had.

First: there is no web-scale robot behavior data.
Robot-generated behavior data doesn't exist
on the internet at any meaningful scale.
Every byte of it has to be actively collected —
one robot, one environment, one task at a time.
That doesn't scale.

Second: robots operate around people.
And if you can't model human behavior,
you can't guarantee safety.

The recipe for both:
scalable scene simulation,
and genuine human modeling."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| PV01 | Background | `Rectangle` | Fill `#0A0A0A` |
| PV02 | "General-Purpose Physical AI" label | `Text` | `GOLD`, size 28, bold |
| PV03 | Multi-environment collage | `VGroup` of 4 `Rectangle` | 2×2 grid, each showing a different environment type: urban street, indoor corridor, campus path, rough terrain |
| PV04 | LLM comparison diagram | `VGroup` | Left: "Internet (web-scale)" → "LLM" → "Language tasks"; compact horizontal |
| PV05 | Physical AI comparison (parallel) | `VGroup` | Left: "???" (question marks) → "Physical AI" → "Physical tasks"; same layout but left side empty |
| PV06 | "Web-scale data" label on PV04 | `Text` | `LIGHT_BLUE`, size 16 |
| PV07 | "No equivalent exists" label on PV05 | `Text` | `RED_MUTED`, size 16 |
| PV08 | Barrier 1 card | `RoundedRectangle` | Fill `#2A1A1A`, stroke `RED_MUTED`, 4u×2u |
| PV09 | "No web-scale robot data" | `Text` | `RED_MUTED`, size 17, inside PV08 |
| PV10 | Barrier 2 card | Same style | |
| PV11 | "No human modeling in context" | `Text` | `RED_MUTED`, size 17, inside PV10 |
| PV12 | Recipe box | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN` |
| PV13 | Recipe line 1 "Scene Simulation → Scalable" | `Text` | `GREEN`, size 17 |
| PV14 | Recipe line 2 "Human Modeling → Human-Centric" | `Text` | `GREEN`, size 17 |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(PV01)`, `Write(PV02)` | 0.6s |
| 2 | 0.6s | `FadeIn(PV03)` — environment collage | 0.6s, cells pop in 2×2 |
| 3 | 1.8s | `FadeIn(PV04)` — LLM comparison | 0.5s |
| 4 | 2.3s | `FadeIn(PV05, PV07)` — Physical AI gap | 0.5s |
| 5 | 3s | `FadeIn(PI)` with question bubble | 0.4s |
| 6 | 3.8s | PI fades, `FadeIn(PV08, PV09)` — Barrier 1 | 0.4s |
| 7 | 4.4s | `FadeIn(PV10, PV11)` — Barrier 2 | 0.4s |
| 8 | 5.2s | `FadeIn(PV12, PV13, PV14)` — recipe | 0.5s |
| 9 | 6.5s | `[HOLD]` | 1.5s |

---

## SCENE 5-03 — Micro-Mobility: The Real Testbed

> **Duration:** ~35s

### [NARRATION]

```
[NARRATOR]

"Before the contributions —
the testbed.

60% of trips in the United States
are shorter than 5 miles.

That's the domain of micro-mobility:
delivery robots, AI-powered electric wheelchairs,
intelligent scooters, and increasingly,
humanoid robots navigating
alongside people on sidewalks.

This is not highway driving.
This is dense urban navigation —
pedestrians appearing from any direction,
curbs, uneven terrain,
and a continuous stream of unpredictable human behavior.

UCLA's research partner is COCO Robotics —
a real deployment of wheeled delivery robots
in campus and urban environments.
Not a test track. A real city."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| MM01 | Background | `Rectangle` | Fill `#0F172A` |
| MM02 | "60% of US trips < 5 miles" stat | `Text` | `GOLD`, size 28, bold |
| MM03 | Pie chart showing 60% / 40% | `AnnularSector` x2 | `GOLD` for 60%, `#2A2A2A` for 40% |
| MM04 | "Micro-Mobility" label | `Text` | `WHITE`, size 22, italic |
| MM05 | Agent icons (4 types) | `VGroup` | Delivery robot, wheelchair, scooter, humanoid — spaced evenly |
| MM06 | Agent labels | `Text` x4 | `LIGHT_BLUE`, size 14, below each icon |
| MM07 | Urban scene backdrop | `VGroup` | Simplified top-down street with sidewalk, buildings, pedestrian dots |
| MM08 | COCO Robotics reference | `RoundedRectangle` | Fill `#1E3A5F`, stroke `BLUE` |
| MM09 | "COCO Robotics — real urban deployment" | `Text` | `WHITE`, size 15 inside MM08 |
| MM10 | "Not a test track" note | `Text` | `GOLD`, size 14, italic |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(MM01)` | 0.3s |
| 2 | 0.3s | `Write(MM02)` | 0.5s |
| 3 | 0.8s | `Create(MM03)` — pie chart | 0.6s, sectors sweep |
| 4 | 1.5s | `FadeIn(MM04)` | 0.3s |
| 5 | 2s | `FadeIn(MM05, MM06)` — agent icons, staggered 0.2s | 0.8s |
| 6 | 3s | `FadeIn(MM07)` — urban scene | 0.5s |
| 7 | 4s | `FadeIn(MM08, MM09, MM10)` | 0.4s |
| 8 | 5s | `[HOLD]` | 1.5s |

---

## SCENE 5-04 — MetaUrban: Compositional Scene Generation

> **Duration:** ~80s

### [NARRATION]

```
[NARRATOR]

"The first pillar: scalable scene simulation.

If you can't collect enough real-world data,
you need simulation environments diverse enough
to substitute.

But a single hand-crafted simulation environment
doesn't scale.
You need infinite variety.

MetaUrban's answer is compositional generation —
building from a quote that appears in the original paper:

'The world is compositional, or there is a god.'
— Stuart Geman

Instead of designing each scene manually,
MetaUrban uses description scripts
to procedurally generate urban environments.
The script specifies:
number of city blocks, intersection type,
lane width, sidewalk configuration,
object density and placement distribution.

Combine those parameters under different distributions
and you get an infinite space of unique environments.
No two training scenes are identical."

--- POWER-LAW FINDING ---

[NARRATOR]
"And here is the most important empirical finding
from MetaUrban.

There is a power-law scaling relationship
between scene diversity and agent performance.

As the number of unique training layouts increases,
performance on unseen test environments
increases following a power law —
not linear, not logarithmic. Power law.

What this means in practice:
100 diverse, unique scene layouts
is worth more than 1000 scenes
that all share the same underlying structure.

Diversity beats quantity.

This is the same insight
that drove web-scale pretraining for language —
except now it applies to physical environments."

--- URBANVERSE ---

[NARRATOR]
"UrbanVerse complements MetaUrban
by reconstructing real-world scenes
from city-tour videos into simulation environments.

This adds realistic asset distribution
that doesn't carry the biases
of human-designed scenes."
```

### [VISUAL SPEC]

**Section A — Procedural Generation Concept**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| MU01 | Background | `Rectangle` | Fill `#0F172A` |
| MU02 | Quote text (full) | `Text` | Font size 22, `GOLD`, italic, center |
| MU03 | Quote attribution "— Stuart Geman" | `Text` | `WHITE`, size 16 |
| MU04 | Description script box | `RoundedRectangle` | Fill `#1A1A2E`, stroke `SIM_PURPLE`, font monospace |
| MU05 | Script content lines | `Text` | `LIGHT_BLUE`, size 14, monospace — e.g. "blocks: 35", "lanes: 6", "sidewalk: wide", "density: 0.4" |
| MU06 | Arrow "Generate →" | `Arrow` | `WHITE` |
| MU07 | Generated scene 1 (grid-style) | `VGroup` | Top-down road grid, varied layout |
| MU08 | Generated scene 2 | Same style | Different layout |
| MU09 | Generated scene 3 | Same style | Another layout |
| MU10 | "∞ unique environments" label | `Text` | `GOLD`, size 20 |

**Section B — Power-law chart**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| PL01 | Axes | `Axes` | `WHITE`, x="Number of unique layouts", y="Performance" |
| PL02 | Power-law curve | `ParametricFunction` | `GOLD`, concave-up, steeply rising |
| PL03 | Linear reference line (faint) | `Line` | `WHITE`, opacity 0.3, dashed |
| PL04 | Logarithmic reference (faint) | `ParametricFunction` | `BLUE`, opacity 0.3, dashed |
| PL05 | Power-law label | `Text` | `GOLD`, size 16, alongside PL02 |
| PL06 | Annotation "100 diverse > 1000 repetitive" | `Text` | `WHITE`, size 16, italic |
| PL07 | Point A marker (100 diverse) | `Dot` | `GOLD`, on PL02 |
| PL08 | Point B marker (1000 repetitive) | `Dot` | `RED_MUTED`, below PL07 on PL03 |
| PL09 | "Diversity > Quantity" callout | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN` |

**Section C — UrbanVerse**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| UV01 | "UrbanVerse" label | `Text` | `WHITE`, size 20, bold |
| UV02 | City-tour video frame placeholder | `Rectangle` | Fill `#2A2A2A`, stroke `WHITE` |
| UV03 | Arrow "reconstruct →" | `Arrow` | `WHITE` |
| UV04 | 3D environment output (stylized) | `VGroup` | Isometric grid with colored blocks for buildings |
| UV05 | "Realistic asset distribution" note | `Text` | `LIGHT_BLUE`, size 15, italic |

### [ANIMATION]

**Section A (0–30s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(MU01)` | 0.3s |
| 2 | 0.3s | `Write(MU02)` — quote, letter by letter | 1.5s |
| 3 | 1.8s | `FadeIn(MU03)` — attribution | 0.3s |
| 4 | 2.5s | `[HOLD]` | 0.8s |
| 5 | 3.3s | Quote fades to top-left, smaller. `FadeIn(MU04, MU05)` — script | 0.6s |
| 6 | 4s | `GrowArrow(MU06)` | 0.3s |
| 7 | 4.3s | `FadeIn(MU07)` — scene 1 | 0.3s |
| 8 | 4.6s | `FadeIn(MU08)` — scene 2 | 0.3s |
| 9 | 4.9s | `FadeIn(MU09)` — scene 3 | 0.3s |
| 10 | 5.5s | `Write(MU10)` — "∞ unique environments" | 0.5s |
| 11 | 6.5s | `[HOLD]` | 1s |

**Section B (0–25s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `Create(PL01)` — axes | 0.5s |
| 2 | 0.5s | `Create(PL03)` — linear ref (dashed) | 0.3s |
| 3 | 0.8s | `Create(PL04)` — log ref (dashed) | 0.3s |
| 4 | 1.1s | `Create(PL02)` — power-law curve draws | 1s, `rate_func=smooth` |
| 5 | 2.2s | `FadeIn(PL05)` — label | 0.3s |
| 6 | 2.8s | `FadeIn(PL07, PL08)` — A and B markers | 0.3s each |
| 7 | 3.5s | `Write(PL06)` — "100 diverse > 1000 repetitive" | 0.5s |
| 8 | 4.3s | `FadeIn(PL09)` — callout box | 0.4s |
| 9 | 5.5s | `[HOLD]` | 1.5s |

**Section C (0–15s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(UV01, UV02)` | 0.4s |
| 2 | 0.4s | `GrowArrow(UV03)` | 0.3s |
| 3 | 0.7s | `FadeIn(UV04)` — 3D environment | 0.5s, builds from ground up |
| 4 | 1.5s | `Write(UV05)` | 0.4s |
| 5 | 2.5s | `[HOLD]` | 1s |

### [NOTES]
- MU02 quote: center it prominently and let it breathe before the technical content follows. This is one of the few moments in the tutorial that uses a philosophical quote as a structural argument — give it the weight it deserves.
- PL07 and PL08 markers: PL07 (100 diverse) should be higher on the y-axis than PL08 (1000 repetitive on linear), even though PL08 has more data. The visual should make it unmistakable that the gold dot (diverse) beats the red dot (repetitive) despite fewer samples.

---

## SCENE 5-05 — UrbanSim: GPU-Native Training

> **Duration:** ~75s

### [NARRATION]

```
[NARRATOR]

"Scene diversity is only useful
if you can actually train on it quickly.

The problem: training a single RL agent
in a traditional simulation platform —
MetaUrban, iGibson, CARLA —
takes up to 180 GPU days to reach
a 95% success rate.

That's not a research bottleneck.
That's a research blocker."

--- BOTTLENECK ---

[NARRATOR]
"The root cause is the architecture
of traditional simulation platforms.

Physics simulation runs on CPU.
Observation computation runs on CPU.
Then data gets transferred to GPU
for the neural network forward pass.
Then actions go back from GPU to CPU.

Every CPU-GPU transfer is a latency hit.
With hundreds of parallel environments,
those hits accumulate.
The GPU spends more time waiting
than computing."

--- URBANSIM SOLUTION ---

[NARRATOR]
"UrbanSim, built on NVIDIA Omniverse,
eliminates that transfer entirely.

Physics simulation: GPU.
Observation computation: GPU.
Neural network inference: GPU.
Everything lives on the same device.
No data crosses the CPU-GPU boundary
in the training hot loop.

Combined with asynchronous scene sampling —
where each parallel environment gets
its own heterogeneous configuration
instead of sharing the same scene layout —
training throughput increases dramatically.

The result:
2,620 frames per second
across 256 parallel environments,
using only 11.2 gigabytes of GPU memory —
less than 25% of a single GPU's capacity.

180 GPU days becomes 3 hours of wall-clock time."

--- REAL-WORLD VALIDATION ---

[NARRATOR]
"And it transfers.

PPO-UrbanVerse — an agent trained
in UrbanVerse reconstructed real-world environments —
outperforms every state-of-the-art
navigation model on real deployments:
S2E, CityWalker, NoMaD —
on both crosswalk and sidewalk scenarios,
using COCO wheeled delivery robots
and Unitree Go2 quadruped robots."
```

### [VISUAL SPEC]

**Section A — Traditional platform bottleneck**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| US01 | Background | `Rectangle` | Fill `#0A0A0A` |
| US02 | "180 GPU days" stat | `Text` | `RED_MUTED`, size 36, bold |
| US03 | Sub-label "to reach 95% success rate" | `Text` | `WHITE`, size 18 |
| US04 | Traditional pipeline diagram | `VGroup` | CPU box left, GPU box right, arrows back-and-forth |
| US05 | CPU box | `RoundedRectangle` | Fill `#2A2A2A`, stroke `RED_MUTED`, label "CPU" |
| US06 | GPU box | `RoundedRectangle` | Fill `#1E3A5F`, stroke `BLUE`, label "GPU" |
| US07 | Transfer arrows (bidirectional) | `Arrow` x2 | `RED_MUTED`, one each way |
| US08 | Transfer labels | `Text` x2 | "data →", "← actions", `RED_MUTED`, size 14 |
| US09 | Latency accumulation indicator | `Rectangle` (progress fill) | Fill `RED_MUTED`, fills slowly — represents wasted time |
| US10 | "GPU waits more than it computes" label | `Text` | `RED_MUTED`, size 15, italic |

**Section B — UrbanSim GPU-native**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| UG01 | Single GPU box | `RoundedRectangle` | Fill `#1E3A5F`, stroke `INT8_GREEN`, large — 6u×4u |
| UG02 | Physics sim module inside box | `RoundedRectangle` | Fill `#1B4332`, small, inside UG01 |
| UG03 | Observation module inside | Same | |
| UG04 | Neural net module inside | Same | |
| UG05 | Internal arrows (all inside GPU) | `Arrow` x3 | `INT8_GREEN`, small, connecting the 3 modules |
| UG06 | "No CPU-GPU transfer" badge | `RoundedRectangle` | Fill `NAVY`, stroke `INT8_GREEN`, outside UG01 |
| UG07 | "Async scene sampling" label | `Text` | `LIGHT_BLUE`, size 15 |
| UG08 | 256 mini-environment tiles | `Rectangle` x16 (4×4 grid, representing 256) | `SIM_PURPLE`, tiny, each slightly different layout |

**Section C — Results**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| UR01 | Speed stat box | `RoundedRectangle` | Fill `#1B4332`, stroke `INT8_GREEN` |
| UR02 | "2,620 FPS" | `Text` | `INT8_GREEN`, size 32, bold |
| UR03 | "256 environments" | `Text` | `WHITE`, size 18 |
| UR04 | "11.2 GB VRAM (<25%)" | `Text` | `WHITE`, size 18 |
| UR05 | Time comparison | `VGroup` — two bars | `RED_MUTED` bar labeled "180 GPU days", `INT8_GREEN` bar "3 hours" |
| UR06 | Real-world deployment photos placeholder | `Rectangle` x2 | Fill `#2A2A2A`, one COCO robot, one Unitree Go2 |
| UR07 | "PPO-UrbanVerse > SOTA" badge | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN` |
| UR08 | Beaten models list "S2E, CityWalker, NoMaD" | `Text` | `WHITE`, size 14, strikethrough style |

### [ANIMATION]

**Section A (0–20s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(US01)` | 0.3s |
| 2 | 0.3s | `Write(US02)` — "180 GPU days" | 0.8s |
| 3 | 1.1s | `FadeIn(US03)` | 0.3s |
| 4 | 2s | `FadeIn(US04–US08)` — pipeline diagram | 0.6s |
| 5 | 3s | US07 arrows animate back-and-forth: `GrowArrow` → `FadeOut` → repeat | 1.2s, 3 cycles — emphasizes the ping-pong |
| 6 | 4.5s | `FadeIn(US09)` — latency fill creeps across | 0.8s, slow `rate_func=linear` |
| 7 | 5.5s | `Write(US10)` | 0.4s |
| 8 | 6.5s | `[HOLD]` | 0.8s |

**Section B (0–20s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(UG01)` — big GPU box | 0.5s |
| 2 | 0.5s | `FadeIn(UG02, UG03, UG04)` — modules inside, staggered | 0.4s |
| 3 | 1s | `GrowArrow(UG05)` x3 — internal arrows | 0.4s |
| 4 | 1.6s | `FadeIn(UG06)` — "No CPU-GPU transfer" badge | 0.4s |
| 5 | 2.2s | `FadeIn(UG07, UG08)` — async sampling + mini tiles | 0.5s |
| 6 | 3.5s | `[HOLD]` | 1s |

**Section C (0–25s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(UR01)` | 0.3s |
| 2 | 0.3s | `Write(UR02)` — "2,620 FPS" | 0.5s |
| 3 | 0.8s | `FadeIn(UR03, UR04)` | 0.3s each |
| 4 | 1.8s | `FadeIn(UR05)` — time comparison bars | 0.6s, bars grow from same baseline |
| 5 | 3s | `FadeIn(UR06)` — robot photos | 0.4s |
| 6 | 3.7s | `FadeIn(UR07, UR08)` | 0.4s |
| 7 | 5s | `[HOLD]` | 1.5s |

### [NOTES]
- US07 ping-pong animation: this is the visual metaphor for the bottleneck. Arrows going back and forth between CPU and GPU should feel repetitive and wasteful. Make the arrow grow and shrink 3 cycles before the latency bar (US09) begins filling.
- UR05 comparison bars: the "180 GPU days" bar should extend far to the right — almost off-screen with a ">>" arrow — while the "3 hours" bar is a tiny sliver. The disproportion must be felt visually, not just read.

---

## SCENE 5-06 — CityWalker Dataset & The Zombie City Problem

> **Duration:** ~55s

### [NARRATION]

```
[NARRATOR]

"Even with scalable simulation and fast training,
there is still a second barrier:
if the simulated world has no realistic humans,
the agent learns to navigate a zombie city.

Real pedestrians don't follow straight paths.
They check their phone and slow down.
They drift toward a shop window.
They stop to talk.
They step off a curb at the last second.

Existing motion datasets like AMASS
capture human movement in studio isolation —
no environment, no context, no destination.
Generating pedestrians from those datasets
produces ghosts that walk through walls
and ignore everything around them.

CityWalker is the dataset built to fix this.

30.8 hours of high-quality video.
120,914 pedestrians.
16,215 scenes.
227 cities.

And crucially: diverse, context-embedded behavior.
Not actors in a lab.
People in real environments doing real things —
pushing strollers, taking photos,
turning around unexpectedly,
stopping to look at something."
```

### [VISUAL SPEC]

**Section A — Zombie City Problem**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| ZC01 | Background | `Rectangle` | Fill `#0A0A0A` |
| ZC02 | "Zombie City" label | `Text` | `RED_MUTED`, size 28, bold |
| ZC03 | Simulated scene (top-down) | `VGroup` | Road, sidewalk grid |
| ZC04 | Zombie pedestrian icons | `VGroup` x5 | Simple stick figures, `WHITE`, moving in perfectly straight lines |
| ZC05 | Wall collision illustration | — | One stick figure walks through a wall `Rectangle` without stopping |
| ZC06 | "No context awareness" label | `Text` | `RED_MUTED`, size 16, italic |
| ZC07 | AMASS dataset reference | `RoundedRectangle` | Fill `#1E1A1A`, stroke `RED_MUTED` |
| ZC08 | "Motion capture: no environment, no context" | `Text` | `WHITE`, size 14 inside ZC07 |

**Section B — CityWalker Stats**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| CW01 | "CityWalker" title | `Text` | `GOLD`, size 26, bold |
| CW02 | Stats grid (2×2) | `VGroup` | Four stat cards |
| CW03 | "30.8 hours" stat | `Text` | `GOLD`, size 24, bold — with label "video footage" |
| CW04 | "120,914 pedestrians" stat | `Text` | `GOLD`, size 24, bold |
| CW05 | "16,215 scenes" stat | `Text` | `GOLD`, size 24, bold |
| CW06 | "227 cities" stat | `Text` | `GOLD`, size 24, bold |
| CW07 | Behavior diversity illustration | `VGroup` | Small icons: person with phone, person with stroller, person looking sideways |
| CW08 | "Real behavior, real context" label | `Text` | `INT8_GREEN`, size 16, italic |

### [ANIMATION]

**Section A (0–20s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(ZC01, ZC02)` | 0.4s |
| 2 | 0.4s | `FadeIn(ZC03, ZC04)` — zombie pedestrians on scene | 0.5s |
| 3 | 1s | ZC04 pedestrians move in perfectly straight lines | 1s, `MoveAlongPath` — mechanically linear |
| 4 | 2s | One ZC04 figure walks through ZC05 wall — no collision | 0.5s |
| 5 | 2.5s | `Write(ZC06)` | 0.4s |
| 6 | 3.2s | `FadeIn(ZC07, ZC08)` | 0.4s |
| 7 | 4s | `[HOLD]` | 0.8s |

**Section B (0–25s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `Write(CW01)` | 0.5s |
| 2 | 0.5s | Stat cards pop in one by one, staggered 0.25s | 1s total |
| 3 | 1.5s | Numbers count up: `CountAnimation` on each | 1s |
| 4 | 3s | `FadeIn(CW07)` — behavior diversity icons | 0.5s |
| 5 | 3.7s | `Write(CW08)` | 0.4s |
| 6 | 4.5s | `[HOLD]` | 1.5s |

### [NOTES]
- ZC04 straight-line movement: animate with `MoveAlongPath` using literal straight lines — the robotic uniformity is the point. Every pedestrian moves identically: same speed, same direction, no variation. This sets up the contrast with PedGen.
- ZC05 wall collision: draw a solid `Rectangle` across the path of one ZC04 figure. Animate the figure moving through it without stopping. This is the "ghost" behavior that makes zombie cities unsafe for robot training.

---

## SCENE 5-07 — PedGen: Context-Aware Human Motion

> **Duration:** ~65s

### [NARRATION]

```
[NARRATOR]

"From CityWalker, PedGen was developed —
a diffusion model for pedestrian motion generation
conditioned on scene context.

Three conditioning inputs."

--- THREE INPUTS ---

[NARRATOR]
"First: Scene Context.
A 3D voxel representation of the surrounding environment.
Walls, furniture, obstacles, parked vehicles —
all encoded into the input.
The model knows where it can and cannot go
before it starts moving.

Second: Body Context.
SMPL body shape parameters —
the physical dimensions of this specific person.
Motion generated for a tall, heavy person
should look different from a child.
The model accounts for that.

Third: Goal.
The destination.
Where is this person heading?

With these three inputs, the model generates
motion that is coherent with the environment,
consistent with the body,
and directed toward the goal."

--- LOSS FUNCTION ---

[NARRATOR]
"The loss function has three components.

Reconstruction loss ensures
body poses stay anatomically realistic.

Trajectory loss ensures
the integrated path actually leads
toward the goal direction.

Geometry loss via forward kinematics
keeps every joint in its correct
3D spatial position."

--- RESULT ---

[NARRATOR]
"The result is not subtle.

Without scene context conditioning,
pedestrians walk through objects,
take unrealistic paths,
ignore everything around them.

With context:
they navigate around obstacles,
adjust speed, pause naturally,
and behave the way a real person would.

This is the difference between
a training environment full of ghosts
and one full of genuine human agents."
```

### [VISUAL SPEC]

**Section A — Three conditioning inputs**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| PG01 | Background | `Rectangle` | Fill `#0F172A` |
| PG02 | "PedGen" title | `Text` | `GOLD`, size 26, bold |
| PG03 | "Diffusion model for pedestrian motion" subtitle | `Text` | `WHITE`, size 16 |
| PG04 | Central skeleton figure | `VGroup` of connected `Line` | `WHITE`, simplified human skeleton, center |
| PG05 | Input arrow 1 "Scene Context" | `Arrow` | `BLUE`, from left |
| PG06 | Scene context icon | `VGroup` of tiny voxel cubes | `BLUE`, 3D grid representation |
| PG07 | Input arrow 2 "Body Context" | `Arrow` | `PEDESTRIAN`, from top-left |
| PG08 | Body shape icon | Silhouette | `PEDESTRIAN`, human outline |
| PG09 | Input arrow 3 "Goal" | `Arrow` | `INT8_GREEN`, from top-right |
| PG10 | Goal marker | `Dot` + dashed path | `INT8_GREEN`, destination point |
| PG11 | Output arrow from skeleton | `Arrow` | `WHITE`, downward |
| PG12 | Output: realistic motion path | `ParametricFunction` (curved path) | `INT8_GREEN`, natural curve avoiding obstacles |

**Section B — Loss function**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| LF01 | Three loss cards | `RoundedRectangle` x3 | Fill `#1E3A5F`, stroke `BLUE`, horizontal row |
| LF02 | "$L_{rec}$" label | `Text` (LaTeX) | `WHITE`, size 18 |
| LF03 | "Reconstruction — anatomical realism" | `Text` | `LIGHT_BLUE`, size 14 |
| LF04 | "$L_{traj}$" label | `Text` (LaTeX) | `WHITE`, size 18 |
| LF05 | "Trajectory — path toward goal" | `Text` | `LIGHT_BLUE`, size 14 |
| LF06 | "$L_{geo}$" label | `Text` (LaTeX) | `WHITE`, size 18 |
| LF07 | "Geometry — joints in 3D space" | `Text` | `LIGHT_BLUE`, size 14 |

**Section C — Context vs No-context comparison**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| CO01 | Left panel "Without context" | `RoundedRectangle` | Fill `#1A1A1A`, stroke `RED_MUTED` |
| CO02 | Zombie path (straight through wall) | `Line` + wall `Rectangle` | `RED_MUTED`, path goes through wall |
| CO03 | Label "Unrealistic — ignores environment" | `Text` | `RED_MUTED`, size 14 |
| CO04 | Right panel "With context" | `RoundedRectangle` | Fill `#1B4332`, stroke `INT8_GREEN` |
| CO05 | Realistic path (curves around obstacle) | `ParametricFunction` | `INT8_GREEN`, bends naturally around obstacle |
| CO06 | Obstacle object on right panel | `Rectangle` | `MESH_GRAY` |
| CO07 | Label "Coherent — navigates environment" | `Text` | `INT8_GREEN`, size 14 |

### [ANIMATION]

**Section A (0–30s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(PG01)`, `Write(PG02, PG03)` | 0.6s |
| 2 | 0.6s | `FadeIn(PG04)` — skeleton | 0.4s |
| 3 | 1s | `GrowArrow(PG05)` + `FadeIn(PG06)` — Scene Context | 0.4s |
| 4 | 1.5s | `GrowArrow(PG07)` + `FadeIn(PG08)` — Body Context | 0.4s |
| 5 | 2s | `GrowArrow(PG09)` + `FadeIn(PG10)` — Goal | 0.4s |
| 6 | 2.8s | `GrowArrow(PG11)` + `Create(PG12)` — output path | 0.6s |
| 7 | 4s | `[HOLD]` | 1s |

**Section B (0–15s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(LF01[0], LF02, LF03)` — Lrec | 0.4s |
| 2 | 0.4s | `FadeIn(LF01[1], LF04, LF05)` — Ltraj | 0.4s |
| 3 | 0.8s | `FadeIn(LF01[2], LF06, LF07)` — Lgeo | 0.4s |
| 4 | 2s | `[HOLD]` | 1s |

**Section C (0–20s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(CO01, CO02, CO03)` — left panel | 0.5s |
| 2 | 0.5s | CO02 path animates through wall | 0.5s — the ghost violation |
| 3 | 1.2s | `FadeIn(CO04, CO05, CO06, CO07)` — right panel | 0.6s |
| 4 | 1.8s | CO05 path animates curving around CO06 | 0.6s — natural navigation |
| 5 | 3s | `[HOLD]` | 1.5s |

### [NOTES]
- LF02, LF04, LF06 use LaTeX math: `$L_{rec}$`, `$L_{traj}$`, `$L_{geo}$`. In Manim, render using `MathTex("L_{rec}")` etc. Keep font size readable (at least 24pt in Manim units).
- CO05 "curves around obstacle": draw using `ParametricFunction` with a path that clearly bends around CO06's position — not just a straight dodge, but a smooth, human-like arc. This is the visual payoff for the entire scene.

---

## SCENE 5-08 — Vid2Sim: Reality into Simulation

> **Duration:** ~55s

### [NARRATION]

```
[NARRATOR]

"The final piece: Vid2Sim.

Everything so far assumed
you have a simulation environment to train in.
But building a realistic 3D simulation
of a specific real-world location is expensive —
manual modeling, asset placement,
physics tuning.

Vid2Sim removes that cost.

Give it a video of any real-world space.
It automatically converts it
into an interactive 3D simulation environment.

The pipeline combines two techniques.

First: 3D Gaussian Splatting.
Reconstruct scene geometry and appearance
from multi-view images.
The output is photorealistic —
the agent sees exactly what the real space looks like,
from any viewpoint.

Second: mesh reconstruction.
Physical interaction requires geometry
the robot can collide with, stand on,
and push against.
Gaussian Splatting gives appearance.
Mesh gives physics.

Combine both layers:
the agent sees a photorealistic world,
and every physical interaction is correct.

The sim-to-real gap shrinks dramatically —
not because simulation looks 'good enough,'
but because it looks and behaves
almost exactly like the real space."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| VS01 | Background | `Rectangle` | Fill `#0A0A0A` |
| VS02 | "Vid2Sim" title | `Text` | `GOLD`, size 26, bold |
| VS03 | Video frame input placeholder | `Rectangle` | Fill `#1A1A1A`, stroke `WHITE`, 3u×2u, labeled "Real World Video" |
| VS04 | Arrow "convert →" | `Arrow` | `WHITE` |
| VS05 | Output: two-layer illustration | `VGroup` | |
| VS06 | Layer 1 — Gaussian Splatting | `Rectangle` | Fill `#1A2A3A`, stroke `BLUE`, semi-transparent grid overlaid with color — "photorealistic" |
| VS07 | "3D Gaussian Splatting" label | `Text` | `BLUE`, size 15 |
| VS08 | "Photorealistic appearance" sub-label | `Text` | `LIGHT_BLUE`, size 13, italic |
| VS09 | Layer 2 — Mesh | `Rectangle` | Fill `#1A1A1A`, stroke `MESH_GRAY`, wireframe grid pattern |
| VS10 | "Mesh Reconstruction" label | `Text` | `MESH_GRAY`, size 15 |
| VS11 | "Physical interaction geometry" sub-label | `Text` | `WHITE`, size 13, italic |
| VS12 | Combined output label | `Text` | `GOLD`, size 18, bold — "Appearance + Physics = Realistic Sim" |
| VS13 | Sim-to-real gap indicator (before) | `DoubleArrow` | `RED_MUTED`, large gap between sim and real panels |
| VS14 | Sim-to-real gap indicator (after Vid2Sim) | `DoubleArrow` | `INT8_GREEN`, very small gap |
| VS15 | "Sim-to-real gap ↓ dramatically" | `Text` | `INT8_GREEN`, size 18, bold |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(VS01)`, `Write(VS02)` | 0.5s |
| 2 | 0.5s | `FadeIn(VS03)` — video input | 0.4s |
| 3 | 0.9s | `GrowArrow(VS04)` | 0.3s |
| 4 | 1.2s | `FadeIn(VS06, VS07, VS08)` — Layer 1 | 0.5s |
| 5 | 1.7s | `FadeIn(VS09, VS10, VS11)` — Layer 2 | 0.5s |
| 6 | 2.3s | VS06 and VS09 animate together — overlap to show combination | 0.5s, `Transform` layers to combined view |
| 7 | 3s | `Write(VS12)` — combined label | 0.5s |
| 8 | 4s | `FadeIn(VS13)` — large gap indicator | 0.4s |
| 9 | 4.6s | `Transform(VS13, VS14)` — gap shrinks | 0.6s, arrow visibly collapses |
| 10 | 5.5s | `Write(VS15)` | 0.4s |
| 11 | 6.5s | `[HOLD]` | 1.5s |

### [NOTES]
- VS13 → VS14 gap shrinking: this is the visual summary of why simulation matters. Animate the double arrow collapsing inward — from a wide span to a near-zero gap. The motion should be smooth and satisfying, `rate_func=smooth`.

---

## SCENE 5-09 — Grand Finale: The Full Picture

> **Duration:** ~75s

### [NARRATION]

```
[NARRATOR]

"Let's step back and look at the full picture."

[Each part's title card briefly recalled]

[NARRATOR]
"Part 1: Foundation models gave individual vehicles
the ability to reason beyond their training data —
long-tail generalization through common sense.

Part 2: V2X cooperation connected agents
in space and time — seeing together
what none of them could see alone.

Part 3: Real-world grounding — hardware, calibration,
localization, data collection, digital twin —
turned theory into deployable systems.

Part 4: Efficiency — data, training, inference —
made those systems viable at scale,
on the hardware that actually exists in vehicles.

Part 5: Physical AI — scalable simulation,
human modeling, and sim-to-real pipelines —
extended the entire framework beyond cars,
to any agent operating in any space with humans."

[NARRATOR — final beat, slower]

"These aren't five separate topics.

Each part solved the bottleneck
the previous one created.
And each solution opened a question
that the next part had to answer.

That chain of necessity
is the actual argument of this tutorial.

Beyond self-driving doesn't mean
better autonomous vehicles.

It means building the full ecosystem —
the data pipelines, the simulation infrastructure,
the cooperative architectures, the efficiency tools,
the human modeling —
so that physical AI can operate safely and usefully
in the same world as the rest of us."
```

### [VISUAL SPEC]

**Section A — Five-part callback sequence**

Each Part gets a 6-second condensed visual recap, playing sequentially.

| ID | Object | Manim Class | Style |
|---|---|---|---|
| GF01 | Background | `Rectangle` | Fill `#0A0A0A` |
| GF02 | Part 1 mini-card | `RoundedRectangle` | Fill `NAVY`, stroke `GOLD`, 2.5u×1.5u |
| GF03 | P1 label "Foundation Models" | `Text` | `WHITE`, size 15 |
| GF04 | P1 key result "Long-tail generalization" | `Text` | `GOLD`, size 13, italic |
| GF05–GF08 | Part 2 mini-card, same structure | Same | "V2X Cooperation" / "Spatiotemporal fusion" |
| GF09–GF12 | Part 3 mini-card | Same | "Sim-to-Real Grounding" / "Hardware + Digital Twin" |
| GF13–GF16 | Part 4 mini-card | Same | "Efficiency" / "Data, Training, Inference" |
| GF17–GF20 | Part 5 mini-card | Same | "Physical AI" / "Scalable + Human-Centric" |
| GF21 | Chain arrows between cards | `Arrow` x4 | `BLUE`, connecting all 5 |

**Section B — The causal chain visualization**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| CC01 | Spine line (horizontal) | `Line` | `WHITE`, full width |
| CC02 | Five nodes on spine | `Dot` x5 | `GOLD`, 0.15u |
| CC03 | "Bottleneck → Solution → New Question" label per link | `Text` x4 | `LIGHT_BLUE`, size 13, below each arrow |
| CC04 | Cause-effect arrows | `CurvedArrow` x4 | `BLUE`, looping forward |

**Section C — Final payoff text**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| FT01 | Background fade to `NAVY` | `Rectangle` | Fill `NAVY`, fades in over `#0A0A0A` |
| FT02 | "Beyond Self-Driving" | `Text` | Font size 44, `WHITE`, bold, center |
| FT03 | em-dash separator | `Line` | `GOLD`, 4u |
| FT04 | "Building the full ecosystem for Physical AI" | `Text` | Font size 22, `GOLD`, italic, below FT02 |
| FT05 | Populated city scene (final wide shot) | `VGroup` | Cars, robots, pedestrians, scooters, infrastructure nodes — all coexisting on the same street grid |
| FT06 | All agents communicating (comm arc lines) | `CurvedArrow` x6 (many-to-many) | `BLUE`, dashed, connecting every agent type |

### [ANIMATION]

**Section A (0–35s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(GF01)` | 0.3s |
| 2 | 0.3s | `FadeIn(GF02–GF04)` — Part 1 card | 0.4s |
| 3 | 1s | `GrowArrow(GF21[0])` | 0.2s |
| 4 | 1.2s | `FadeIn(GF05–GF08)` — Part 2 card | 0.4s |
| 5 | 1.8s | `GrowArrow(GF21[1])` | 0.2s |
| 6 | 2s | `FadeIn(GF09–GF12)` — Part 3 card | 0.4s |
| 7 | 2.6s | `GrowArrow(GF21[2])` | 0.2s |
| 8 | 2.8s | `FadeIn(GF13–GF16)` — Part 4 card | 0.4s |
| 9 | 3.4s | `GrowArrow(GF21[3])` | 0.2s |
| 10 | 3.6s | `FadeIn(GF17–GF20)` — Part 5 card | 0.4s |
| 11 | 4.5s | All 5 cards pulse simultaneously | 0.4s |
| 12 | 5.5s | `[HOLD]` | 1s |

**Section B (0–20s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `Create(CC01)` | 0.4s |
| 2 | 0.4s | `FadeIn(CC02)` x5, staggered | 0.4s |
| 3 | 1s | `Create(CC04)` x4, staggered — cause-effect arcs | 0.4s each |
| 4 | 2.8s | `FadeIn(CC03)` — labels, staggered | 0.3s each |
| 5 | 4.5s | `[HOLD]` | 1s |

**Section C (0–30s):**

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(FT01)` — navy background transition | 0.8s |
| 2 | 0.8s | `Write(FT02)` — "Beyond Self-Driving" | 1.2s |
| 3 | 2s | `Create(FT03)` — gold divider | 0.4s |
| 4 | 2.4s | `FadeIn(FT04)` — subtitle | 0.6s |
| 5 | 3.5s | `[HOLD]` | 1s |
| 6 | 4.5s | `FadeIn(FT05)` — city wide shot, agents appear one by one | 2s, stagger each agent type 0.3s |
| 7 | 6.5s | `Create(FT06)` — comm arcs between all agents | 1s, arcs draw simultaneously |
| 8 | 7.5s | `[HOLD]` — full scene, all agents connected | 3s — let it breathe |

### [NOTES]
- FT05 is the emotional conclusion of the entire 5-part series. Every agent type introduced across all 5 parts should appear: cars, infrastructure nodes, delivery robots, pedestrians, quadruped robots, scooters, wheelchairs. Pack the scene but keep it readable — use distinct colors per type and leave enough spacing that each is identifiable.
- FT06 comm arcs: unlike earlier scenes where arcs connected a few agents, here they should create a dense web of communication — every agent type connected to at least 2 others. This visualizes the core thesis: not smart agents, but a connected ecosystem.
- The 3-second hold at the end (step 8) is intentional. After 5 parts and ~55 minutes of content, the audience deserves a moment of stillness with the full picture visible.

---

## SCENE 5-10 — Credits & Closing

> **Duration:** ~20s

### [NARRATION]

```
[NARRATOR]

"This tutorial was originally presented at ICCV 2025
by the UCLA Mobility Lab.

This summary video was produced by [Team Name]
as a lab assignment.

We'd love to make it public —
we've reached out to the organizers.
Thank you for watching."

[CAR mascot gives a small wave]
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| CR01 | Background | `Rectangle` | Fill `NAVY` |
| CR02 | UCLA logo | `SVGMobject` | `WHITE`, top-center |
| CR03 | "ICCV 2025 Tutorial" label | `Text` | `LIGHT_BLUE`, size 18 |
| CR04 | Speakers list | `Text` | `WHITE`, size 15, 4 names with affiliations |
| CR05 | Team credit | `Text` | `WHITE`, size 16 — "Summary by [Team Name]" |
| CR06 | "Made with Manim" small badge | `Text` | `WHITE`, opacity 0.5, size 12, bottom corner |
| CR07 | `CAR` mascot | `SVGMobject` | Bottom-right, wave animation |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(CR01, CR02)` | 0.5s |
| 2 | 0.5s | `FadeIn(CR03, CR04)` | 0.5s |
| 3 | 1.2s | `FadeIn(CR05)` | 0.3s |
| 4 | 2s | `FadeIn(CR06)` | 0.3s |
| 5 | 2.5s | `FadeIn(CR07)` — CAR mascot waves | 0.5s |
| 6 | 3.5s | `[HOLD]` | 3s — full credits visible |
| 7 | 6.5s | Fade to black | 1s |

---

## End of Session 5 — Full Series Complete

> **Sessions produced:**
> - `spec_intro_part01.md` — Introduction + Part 01
> - `spec_part02.md` — Part 02
> - `spec_part03.md` — Part 03
> - `spec_part04.md` — Part 04
> - `spec_part05.md` — Part 05 ← this file
>
> **Total estimated runtime:** ~55 minutes
> **Total scenes across all sessions:** ~60 scenes

---

## Cross-Session Consistency Checklist

Use this when reviewing all five files together before production begins.

| Item | Check |
|---|---|
| `CAR` and `PI` mascots appear in all 5 parts with consistent visual style | ☐ |
| Roadmap strip (5 nodes) is shown at every Part title card | ☐ |
| Color palette is consistent (`NAVY`, `GOLD`, `BLUE`, `INT8_GREEN`, `RED_MUTED`) | ☐ |
| Each Part's bridge scene correctly names the next Part | ☐ |
| LaTeX math strings (`$L_{rec}$`, `$L_{traj}$`, `$L_{geo}$`) render correctly in Manim | ☐ |
| Scene numbering is sequential within each file (no gaps) | ☐ |
| FP32/INT8 color coding (`FP32_RED` vs `INT8_GREEN`) is consistent in Parts 04 and 05 | ☐ |
| Final scene (5-09, Section C) includes all agent types from all 5 parts | ☐ |

---

*Production note: Scene 5-09 (Grand Finale) is the most important scene of the entire series. It should receive disproportionate polish — the populated city wide shot, the communication web, and the 3-second hold are what the audience takes away. If production time is limited, compress earlier scenes before touching 5-09.*
