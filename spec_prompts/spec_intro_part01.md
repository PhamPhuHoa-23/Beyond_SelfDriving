# Beyond Self-Driving — Production Spec
## Session 1 of 5: Introduction + Part 01

> **How to read this document**
> Each scene block contains four sections:
> - `[NARRATION]` — full script, line by line, with speaker tag
> - `[VISUAL SPEC]` — every on-screen object with ID, Manim class, and style
> - `[ANIMATION]` — ordered steps with timing and Manim method
> - `[NOTES]` — design intent, open decisions, references

---

## Document Conventions

| Tag | Meaning |
|---|---|
| `CAR` | The main mascot — car-shaped character, acts as guide/responder |
| `PI` | The curious mascot — small round character, asks questions |
| `t=0s` | Time offset from scene start |
| `FadeIn`, `Write`, `Create`, `MoveAlongPath` | Manim animation methods |
| `[HOLD]` | Pause before next animation step |

**Color palette (use consistently):**
| Name | Hex | Used for |
|---|---|---|
| `NAVY` | `#1F3864` | Backgrounds, headers |
| `BLUE` | `#2E75B6` | Accent, arrows, highlights |
| `GOLD` | `#E8A838` | Quote text, emphasis |
| `LIGHT_BLUE` | `#EAF4FB` | Info boxes |
| `WHITE` | `#FFFFFF` | Text on dark backgrounds |
| `RED_MUTED` | `#C0392B` | Warnings, X marks |
| `GREEN` | `#27AE60` | Checkmarks, positive outcomes |

---
---

# INTRODUCTION

> **Estimated duration:** ~3 min
> **Objective:** Establish context, introduce the team and the tutorial, deliver the hook, reveal the 5-part roadmap.

---

## SCENE I-01 — Title Card & Team Introduction

> **Duration:** ~45s

### [NARRATION]

```
[NARRATOR — warm, welcoming tone]

"Hi everyone, and welcome to Beyond Self-Driving —
a tutorial originally presented at ICCV 2025.

My name is [Presenter Name], and I'm a member of [Lab Name] at UCLA.
This video was put together by our student group
as a summary of the tutorial — in our own words,
for a lab assignment.

If you're the organizer and you're watching this —
we'd love to make it public. We sent you an email. 😊

The original tutorial was presented by researchers
from the UCLA Mobility Lab.
For questions about the original material,
you can reach out to the organizers directly."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| V01 | Background | `Rectangle` | Fill `NAVY`, full screen |
| V02 | UCLA Logo | `SVGMobject` | White, top-left, w=1.5u |
| V03 | Title text "Beyond Self-Driving" | `Text` | Font size 52, `GOLD`, center |
| V04 | Subtitle "ICCV 2025 Tutorial — Team Summary" | `Text` | Font size 24, `WHITE`, below V03, gap 0.3u |
| V05 | Presenter name tag | `Text` | Font size 20, `LIGHT_BLUE`, below V04 |
| V06 | Org name + lab name | `Text` | Font size 18, `WHITE`, opacity 0.7 |
| V07 | Mascot `CAR` | `SVGMobject` | Bottom-right, idle animation |
| V08 | Divider line | `Line` | `BLUE`, width=8u, below V06 |
| V09 | Contact note | `Text` | Font size 16, `WHITE`, opacity 0.6 |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(V01)` — background | 0.3s |
| 2 | 0.3s | `Write(V03)` — title | 1.2s, typewriter feel |
| 3 | 1.5s | `FadeIn(V04)` — subtitle | 0.5s, slide up from below |
| 4 | 2s | `FadeIn(V02)` — UCLA logo | 0.4s |
| 5 | 2.5s | `FadeIn(V05, V06)` — names | 0.5s together |
| 6 | 3s | `Create(V08)` — divider | 0.4s, draw left-to-right |
| 7 | 3.5s | `FadeIn(V09)` — contact | 0.4s |
| 8 | 4s | `FadeIn(V07)` — CAR mascot, idle loop | persistent |

### [NOTES]
- If mascot (`CAR`) is not finalized, use a placeholder car icon with a subtle bounce loop (`rate_func=there_and_back`, repeat).
- The team discussed having a 2D cute mascot designed — this card is where it first appears. **Design decision still open.**
- UCLA logo: check licensing for reuse in public video.

---

## SCENE I-02 — The Hook

> **Duration:** ~40s
> **Quote delivery:** This is the emotional centerpiece of the intro. Animate it slowly and deliberately.

### [NARRATION]

```
[NARRATOR]

"Before we dive in, here's the one idea
this entire tutorial is built around."

[PAUSE — quote appears on screen]

"We gave cars eyes to see,
and Foundation Models to reason —
but even the smartest agent
cannot see through walls.

So we taught them to cooperate."

[PAUSE 1s]

"That's what this tutorial is about."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| V10 | Background | `Rectangle` | Fill `#0D0D0D` (near-black), full screen |
| V11 | Quote line 1 "We gave cars eyes to see," | `Text` | Font size 32, `WHITE`, center-left |
| V12 | Quote line 2 "and Foundation Models to reason —" | `Text` | Font size 32, `WHITE`, below V11 |
| V13 | Quote line 3 "but even the smartest agent" | `Text` | Font size 28, `WHITE`, opacity 0.85 |
| V14 | Quote line 4 "cannot see through walls." | `Text` | Font size 28, `WHITE`, bold |
| V15 | Spacer line | `Line` | `GOLD`, short, 2u, centered |
| V16 | Quote line 5 "So we taught them to cooperate." | `Text` | Font size 36, `GOLD`, bold |

**Hook Animation Sequence (embedded in scene):**

Sub-scene A — Single car with radar:

| ID | Object | Manim Class | Style |
|---|---|---|---|
| A01 | Car object | `SVGMobject` or `VGroup` of shapes | Centered-left, 1.2u |
| A02 | Radar sweep arcs | `Arc` x3, animated | Color `BLUE`, opacity fading out at edge |
| A03 | Detection dots (pedestrians, objects) | `Dot` x5 | Color `GREEN`, appear as radar passes |
| A04 | GPT/FM logo icons | `SVGMobject` x2 | Small, 0.4u, appear near car |
| A05 | Thought bubble | `SVGMobject` or hand-drawn `VMobject` | White fill, above car |
| A06 | Thought text line 1 | `Text` inside bubble | "There is a human over there." size 16 |
| A07 | Thought text line 2 | `Text` inside bubble | "→ Turn left." size 16, `BLUE` |

Sub-scene B — Wall blocking:

| ID | Object | Manim Class | Style |
|---|---|---|---|
| B01 | Wall rectangle | `Rectangle` | Fill `#555555`, stroke `WHITE`, 0.8u × 2u |
| B02 | Radar arcs (blocked) | `Arc` | Same as A02 but `clip` or terminate at B01 |
| B03 | Shadow/blind zone indicator | `Polygon` | Fill `RED_MUTED`, opacity 0.15 |

Sub-scene C — Multi-agent cooperation:

| ID | Object | Manim Class | Style |
|---|---|---|---|
| C01 | Car 2 | `SVGMobject` | Top-right of scene |
| C02 | Car 3 | `SVGMobject` | Bottom-right of scene |
| C03 | 3D communication arcs | `CurvedArrow` or `ParametricFunction` | Color `BLUE`, dashed, 3D curve feel |
| C04 | Wall (now transparent) | `Rectangle` | Same size as B01, fill transparent, stroke `WHITE` opacity 0.3 |
| C05 | Detected human (behind wall) | `Dot` or small `SVGMobject` | `GREEN`, visible now |
| C06 | "I see." text near Car | `Text` | Font size 18, `GREEN` |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(V10)` — dark background | 0.3s |
| 2 | 0.3s | `Write(V11)` — line 1 of quote | 1s, letter by letter |
| 3 | 1.5s | `Write(V12)` — line 2 | 1s |
| 4 | 2.5s | `Write(V13, V14)` — lines 3–4 | 1.2s |
| 5 | 3.7s | `[HOLD]` | 0.5s |
| 6 | 4.2s | All quote lines `FadeOut`, then `FadeIn(A01)` — single car appears | 0.8s |
| 7 | 5s | `Create(A02)` — radar sweep, rotate 360° | 1.5s, looping 1× |
| 8 | 5.5s | `FadeIn(A03)` — detection dots appear as sweep passes | staggered 0.1s each |
| 9 | 7s | `FadeIn(A04)` — FM logos appear near car | 0.4s |
| 10 | 7.5s | `FadeIn(A05, A06)` — thought bubble with text 1 | 0.6s |
| 11 | 8.2s | `Transform(A06, A07)` — thought updates to "Turn left" | 0.4s |
| 12 | 9s | `FadeIn(B01)` — wall appears, blocking path | 0.5s slide-in from right |
| 13 | 9.5s | `Create(B02)` — radar sweeps, arcs terminate at wall | 1.2s |
| 14 | 9.8s | `FadeIn(B03)` — blind zone fills in red | 0.5s |
| 15 | 11s | `FadeIn(C01, C02)` — 2 more cars appear | 0.6s |
| 16 | 11.6s | `Create(C03)` x2 — 3D curved comm lines between cars | 1s, draw simultaneously |
| 17 | 12.6s | `FadeOut(B01)`, `FadeIn(C04)` — wall becomes transparent | 0.8s |
| 18 | 13.4s | `FadeIn(C05)` — human behind wall now visible | 0.4s |
| 19 | 13.8s | `Write(C06)` — "I see." | 0.5s |
| 20 | 14.3s | Entire scene `FadeOut`, then `FadeIn(V15, V16)` — payoff quote | 1s |
| 21 | 15.5s | `[HOLD]` | 1.5s |

### [NOTES]
- The 2D → 3D transition (step 16) is the visual centerpiece. The 3D curve arcs should feel like wireless signals arcing through space, not just flat lines. Use `ParametricFunction` with a z-component, or fake it with a thick arc + shadow.
- Wall transparency (step 17): use `set_opacity(0.2)` on the wall rectangle rather than full FadeOut — the wall still exists physically, they just "see through" it with cooperation.

---

## SCENE I-03 — The 5-Part Journey (Roadmap)

> **Duration:** ~30s

### [NARRATION]

```
[NARRATOR]

"This tutorial is structured as a five-part journey.

Part 1: How Foundation Models give individual cars
the ability to reason about the world.

Part 2: How multiple agents cooperate —
V2X, collective intelligence.

Part 3: The bridge between simulation and reality.

Part 4: Making all of this efficient enough
to actually run on real hardware.

And Part 5: Scaling up to a full human-centric
Physical AI ecosystem.

Let's begin."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| R01 | Background | `Rectangle` | Fill `NAVY` |
| R02 | Central spine line | `Line` | `WHITE`, horizontal, full width |
| R03–R07 | 5 arc nodes (semicircle alternating up/down) | `Arc` x5 | Radius 0.4u, alternating above/below spine, `BLUE` fill |
| R08–R12 | Node labels (Part 01–05 numbers) | `Text` inside arcs | Font size 18, `WHITE` |
| R13–R17 | Part titles (short) | `Text` | Font size 16, below/above arc, `WHITE` |
| R18 | Connecting tick marks | `Line` x4 | `WHITE`, short, on spine between nodes |

**Part titles (short versions for roadmap):**
1. Individual Reasoning (FMs)
2. Collective Intelligence (V2X)
3. Sim-to-Real Bridge
4. Efficiency & Adaptation
5. Scalable Physical AI

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(R01)` | 0.3s |
| 2 | 0.3s | `Create(R02)` — spine draws left to right | 0.8s |
| 3 | 1.1s | `Create(R03)` + `FadeIn(R08, R13)` — Part 1 node | 0.4s |
| 4 | 1.5s | `Create(R04)` + `FadeIn(R09, R14)` — Part 2 node | 0.4s |
| 5 | 1.9s | `Create(R05)` + `FadeIn(R10, R15)` — Part 3 node | 0.4s |
| 6 | 2.3s | `Create(R06)` + `FadeIn(R11, R16)` — Part 4 node | 0.4s |
| 7 | 2.7s | `Create(R07)` + `FadeIn(R12, R17)` — Part 5 node | 0.4s |
| 8 | 3.1s | All nodes pulse briefly (`scale(1.15)` → `scale(1.0)`) | 0.3s each, staggered 0.1s |
| 9 | 4s | `[HOLD]` — full roadmap visible | 1s |
| 10 | 5s | Node R03 (Part 1) highlights: fill `GOLD`, label bold | 0.4s — signals we start here |

### [NOTES]
- Alternating arc direction (up/down) comes from the idea sketch. Even-numbered parts arc below the spine, odd-numbered arc above.
- Keep the roadmap on screen as a small persistent element (bottom strip) throughout Part 01 if layout allows.

---
---

# PART 01 — Foundation Models for Autonomous Driving

> **Estimated duration:** ~10 min
> **Original speaker:** Dr. Zhiyu Huang, Postdoctoral Researcher, UCLA
> **Reference slides:** Slides 1–24, Part_1.pdf

---

## SCENE 1-01 — Opening Question

> **Duration:** ~30s

### [NARRATION]

```
[NARRATOR]

"Let's start with a question that sounds simple
but is surprisingly hard to answer:

Why, in 2025 — with everything AI can do —
write code, generate videos, answer any question —
why can't self-driving cars just... work everywhere?"

[PI mascot appears, looking curious]

[PI]
"AI đang ở đâu?"
"And — AV đang ở đâu?"

[NARRATOR]
"To answer that, we need to understand
where AI actually is right now,
and where the autonomous vehicle industry stands.
Those are the two things we'll look at first."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| S01 | Background | `Rectangle` | Fill `NAVY` |
| S02 | Question text (large) | `Text` | Font size 36, `WHITE`, center, max width 11u |
| S03 | `PI` mascot | `SVGMobject` | Left side, 1u, idle |
| S04 | Speech bubble 1 | `RoundedRectangle` | Fill `WHITE`, stroke `BLUE` |
| S05 | Bubble text 1 | `Text` | "AI đang ở đâu?" size 20, `NAVY` |
| S06 | Speech bubble 2 | `RoundedRectangle` | Same style as S04 |
| S07 | Bubble text 2 | `Text` | "AV đang ở đâu?" size 20, `NAVY` |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(S01)` | 0.3s |
| 2 | 0.3s | `Write(S02)` — question | 1.5s |
| 3 | 2s | `FadeIn(S03)` — PI appears, bounce in | 0.5s |
| 4 | 2.5s | `FadeIn(S04, S05)` — bubble 1 | 0.4s |
| 5 | 3.5s | `FadeIn(S06, S07)` — bubble 2 | 0.4s |
| 6 | 4.5s | `[HOLD]` | 1s |
| 7 | 5.5s | `FadeOut` all except background | 0.5s |

---

## SCENE 1-02 — Generative AI Boom

> **Duration:** ~60s

### [NARRATION]

```
[NARRATOR]

"Since 2023, generative AI has exploded
in ways we genuinely didn't predict.

Coding assistants, complex reasoning,
image generation, video synthesis,
3D scene understanding —
all of it, within two years.

Every single one of these systems
shares a common DNA.
They are what researchers call
Foundation Models."

[PI mascot pops up]

[PI]
"Foundation Model là gì vậy?"

[NARRATOR]
"According to the Stanford Center for Research on Foundation Models —
a foundation model is any model trained on diverse, large-scale data —
usually through self-supervised learning,
meaning it learns without human-labeled examples —
and can then be adapted to a huge variety of downstream tasks.

Think of it like this:
instead of building a separate AI for each problem,
you build one model that understands the world —
then fine-tune it for whatever you need.

GPT-4, CLIP, DINO — all foundation models."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| G01 | Background | `Rectangle` | Fill `#111827` (dark blue-gray) |
| G02 | Year label "2023 →" | `Text` | Font size 22, `GOLD`, top-left |
| G03–G06 | 4 capability icons (coding, reasoning, image, video) | `SVGMobject` or `VGroup` | Grid 2×2, centered, each 1.2u |
| G07 | Capability labels under each icon | `Text` x4 | Font size 16, `WHITE` |
| G08 | Converging arrows toward center | `Arrow` x4 | `BLUE`, pointing inward |
| G09 | "Foundation Models" label box | `RoundedRectangle` + `Text` | Fill `BLUE`, text `WHITE`, size 28 bold |
| G10 | Pipeline diagram (left: data → center: model → right: tasks) | `VGroup` of shapes | See sub-spec below |

**Pipeline sub-spec (G10):**

| Sub-ID | Object | Manim Class | Notes |
|---|---|---|---|
| G10a | "Data" column — 5 stacked rects | `Rectangle` x5 | Colors: text=gray, image=blue, speech=green, 3D=purple, video=orange |
| G10b | Arrow "Training" | `Arrow` | `WHITE`, left-to-right |
| G10c | Core model box | `RoundedRectangle` | Fill `NAVY`, stroke `GOLD`, label "Foundation Model" |
| G10d | Arrow "Adaptation" | `Arrow` | `WHITE`, left-to-right |
| G10e | Tasks column — 6 stacked rects | `Rectangle` x6 | Each labeled: Info Extraction, Object Recognition, Image Captioning, QA, etc. |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(G01, G02)` | 0.4s |
| 2 | 0.4s | `FadeIn(G03)` — coding icon | 0.3s |
| 3 | 0.7s | `FadeIn(G04)` — reasoning icon | 0.3s |
| 4 | 1.0s | `FadeIn(G05)` — image icon | 0.3s |
| 5 | 1.3s | `FadeIn(G06)` — video icon | 0.3s |
| 6 | 2s | All icons animate toward center: `G03–G06.animate.move_to(center)` | 0.6s converge |
| 7 | 2.6s | Icons fade, `G09` replaces them: `FadeIn(G09)` | 0.5s |
| 8 | 3.2s | `PI` appears with question bubble | 0.4s |
| 9 | 4s | PI fades, `FadeIn(G10)` — full pipeline diagram | 0.8s, draw left to right |
| 10 | 4.8s | `G10a` animates in column by column | 0.5s each column |
| 11 | 5.8s | `Create(G10b)` — arrow draws | 0.4s |
| 12 | 6.2s | `FadeIn(G10c)` — core model | 0.5s |
| 13 | 6.7s | `Create(G10d)` — arrow draws | 0.4s |
| 14 | 7.1s | `G10e` animates in | 0.6s, staggered 0.1s per task |
| 15 | 8s | `[HOLD]` | 1.5s |

### [NOTES]
- 4 capability icons can be simple geometric symbols if no SVG is ready: gear (coding), lightbulb (reasoning), frame (image), play triangle (video).
- The pipeline diagram is meant to be re-used — it will appear briefly as a reference in later scenes. Build it as a `VGroup` so it can be scaled down and repositioned.

---

## SCENE 1-03 — AV Industry: Three Architectures

> **Duration:** ~90s

### [NARRATION]

```
[NARRATOR]

"Now let's look at where autonomous driving stands.

There are three dominant architectures
used in the industry today."

[Architecture 1 appears]

"The first is the Modular system —
the most commercially deployed architecture right now.
The pipeline is split into sequential modules:
perception, localization, prediction, planning, control.
Each module can be debugged and updated independently —
which is exactly why companies like it.

But it has three core weaknesses.
First: error accumulation.
If perception is slightly off,
prediction gets worse, planning gets worse,
and the final action can be dangerously wrong.
Second: there's no joint optimization —
each module is trained independently,
so they don't actually agree with each other.
Third: once trained, modular systems
generally don't continue learning from experience."

[Architecture 2 appears]

"End-to-end systems solve that
by replacing the entire pipeline
with a single neural network.
One input — sensor data.
One output — action.
No information lost between steps.
Joint optimization across everything.

The cost: when something goes wrong,
you have no idea why.
Safety verification becomes nearly impossible."

[Architecture 3 appears]

"Hybrid systems try to balance both.
Machine learning handles perception and planning,
while a classical control module handles execution.
It's the approach most large companies are taking
because it combines adaptability with reliability.

But all three share one fundamental weakness."
```

### [VISUAL SPEC]

Three columns layout, each column = one architecture.

| ID | Object | Manim Class | Style |
|---|---|---|---|
| AV01 | Background | `Rectangle` | Fill `#0F172A` |
| AV02 | Column header "Modular" | `Text` | Font size 22, `WHITE`, bold, top of col 1 |
| AV03 | Column header "End-to-End" | `Text` | Same, top of col 2 |
| AV04 | Column header "Hybrid" | `Text` | Same, top of col 3 |

**Modular column (col 1):**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| M01 | "Sensor" box | `RoundedRectangle` | Fill `#1E3A5F`, stroke `BLUE`, label white |
| M02 | Arrow → | `Arrow` | `BLUE` |
| M03 | "Perception" box | Same style | |
| M04 | Arrow → | | |
| M05 | "Localization" box | Same | |
| M06 | Arrow → | | |
| M07 | "Prediction" box | Same | |
| M08 | Arrow → | | |
| M09 | "Planning" box | Same | |
| M10 | Arrow → | | |
| M11 | "Control" box | Same | |
| M12 | Arrow → | | |
| M13 | "Action" box | Fill `GREEN` | |
| M14 | ✗ Label "Error Accumulation" | `Text` | `RED_MUTED`, size 16, below col |
| M15 | ✗ Label "No Joint Opt." | `Text` | Same |
| M16 | ✗ Label "No Continual Learning" | `Text` | Same |

**E2E column (col 2):**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| E01 | "Sensor" box | Same style as M01 | |
| E02 | Arrow → | | |
| E03 | "Neural Network" box | `RoundedRectangle` | Fill `#2D1B69`, stroke `#7C3AED`, taller |
| E04 | Arrow → | | |
| E05 | "Action" box | Fill `GREEN` | |
| E06 | ✗ Label "Safety Verification Impossible" | `Text` | `RED_MUTED`, size 16 |

**Hybrid column (col 3):**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| H01 | "Sensor" box | Same | |
| H02 | Arrow → | | |
| H03 | "ML (Perception + Planning)" box | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN` |
| H04 | Arrow → | | |
| H05 | "Control Module" box | `RoundedRectangle` | Fill `#1E3A5F`, stroke `BLUE` |
| H06 | Arrow → | | |
| H07 | "Action" box | Fill `GREEN` | |
| H08 | ✓ Label "Balanced" | `Text` | `GREEN`, size 16 |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(AV01)` | 0.3s |
| 2 | 0.3s | **Col 1 builds:** `Write(AV02)` then `Create(M01–M13)` sequentially | 0.2s per box, 0.15s per arrow |
| 3 | 3s | `FadeIn(M14, M15, M16)` — weakness labels appear with ✗ | 0.2s staggered |
| 4 | 3.8s | **Col 2 builds:** `Write(AV03)` then `Create(E01–E05)` | 0.8s total |
| 5 | 4.6s | `FadeIn(E06)` — ✗ label | 0.2s |
| 6 | 5s | **Col 3 builds:** `Write(AV04)` then `Create(H01–H07)` | 0.8s total |
| 7 | 5.8s | `FadeIn(H08)` — ✓ label | 0.2s |
| 8 | 6.5s | `[HOLD]` — all three visible | 1s |
| 9 | 7.5s | Columns scale slightly to make room for next text | 0.5s |

### [NOTES]
- The three columns should fit horizontally with roughly equal spacing. At 16:9 aspect, allocate ~4.5u per column with 0.3u gap.
- The ✗ / ✓ symbols should use proper unicode (`\u2717` / `\u2713`) or draw them as `VMobject` for cleaner look.
- Consider highlighting the currently-narrated column with a subtle `set_stroke(GOLD, width=3)` pulse.

---

## SCENE 1-04 — Long-Tail Problem

> **Duration:** ~75s

### [NARRATION]

```
[NARRATOR]

"But all three architectures share
one fundamental weakness."

[Three ✗ marks converge onto shared label]

"The long-tail problem.

99% of the time, a self-driving car
drives completely normally —
standard intersections, clear weather,
predictable behavior.

But in the remaining 1% —
that's where everything breaks.

Look at these three situations."

[Photo 1 appears]
"A person standing in the middle of the road,
holding a phone, completely still.
Is this a pedestrian who's about to move?
Are they safe? Do they see the car?

[Photo 2 appears]
A truck carrying three traffic lights —
upside down, facing the wrong way, not lit.
How does a perception system classify that?

[Photo 3 appears]
A road completely buried under snow.
No lane markings. No reference points.
Lane detection is completely blind."

[Photos shrink, distribution appears]

"These situations live in the tail
of the probability distribution.
Rare. But that's exactly where accidents happen.

Now — why can humans handle these?"

[PI mascot appears]

[PI]
"Tại sao con người xử lý được?"

[CAR mascot appears]

[CAR]
"Because we have contextual reasoning —
built from a lifetime of experiencing the world.
We understand other people's intentions.
We understand the physics of the environment.
We know that traffic lights on a truck aren't real signals.

That's common sense.
And that's what's missing."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| L01 | Background | `Rectangle` | Fill `#0F172A` |
| L02 | Shared ✗ label: "Long-Tail Problem" | `Text` | Font size 36, `RED_MUTED`, bold, center |
| L03 | Photo placeholder 1 (person in road) | `Rectangle` + label | Fill `#2A2A2A`, stroke `WHITE`, 3.5u×2u |
| L04 | Photo placeholder 2 (traffic lights on truck) | Same | |
| L05 | Photo placeholder 3 (snowy road) | Same | |
| L06 | Chi-square distribution curve | `ParametricFunction` | Color `BLUE`, fill under curve |
| L07 | "99%" fill region | Fill under left of curve | Fill `BLUE` opacity 0.3 |
| L08 | "1%" fill region | Fill under right tail | Fill `RED_MUTED` opacity 0.5 |
| L09 | "99%" label | `Text` | Font size 20, `WHITE` |
| L10 | "1%" label with callout | `Text` + `Arrow` | `RED_MUTED`, arrow pointing to tail |
| L11 | Three dots from photos → tail | `Dot` x3 | `RED_MUTED`, animate from photo positions to tail |
| L12 | `PI` mascot | `SVGMobject` | Left, 0.8u |
| L13 | `CAR` mascot | `SVGMobject` | Right, 0.8u |
| L14 | Speech bubble + "Common Sense" emphasis | `RoundedRectangle` + `Text` | Text `GOLD`, size 28, bold |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | Previous scene fades out. `FadeIn(L01)` | 0.4s |
| 2 | 0.4s | `Write(L02)` — "Long-Tail Problem" | 0.8s |
| 3 | 1.5s | `FadeIn(L03)` — photo 1 | 0.4s |
| 4 | 2s | `FadeIn(L04)` — photo 2 | 0.4s |
| 5 | 2.5s | `FadeIn(L05)` — photo 3 | 0.4s |
| 6 | 4s | `L03–L05.animate.scale(0.5).shift(UP*1.5)` — photos shrink upward | 0.6s |
| 7 | 4.6s | `Create(L06)` — distribution curve draws | 1s |
| 8 | 5.6s | `FadeIn(L07)` — 99% region fills | 0.5s |
| 9 | 6.1s | `FadeIn(L08)` — 1% tail fills red | 0.5s |
| 10 | 6.6s | `FadeIn(L09, L10)` — labels | 0.3s |
| 11 | 7s | `L11` dots travel from photo positions → 1% tail | 0.8s, `MoveAlongPath` |
| 12 | 8s | `[HOLD]` | 1s |
| 13 | 9s | `FadeIn(L12)` — PI with question bubble | 0.4s |
| 14 | 9.8s | `FadeIn(L13)` — CAR mascot | 0.4s |
| 15 | 10.5s | `Write(L14)` — "Common Sense" emphasis | 0.5s, flash `GOLD` |
| 16 | 11.5s | `[HOLD]` | 1s |

### [NOTES]
- Photos L03–L05 are from the original slides. If the video goes public, verify whether these can be used or need replacement visuals.
- The chi-square distribution is approximate. Use `ParametricFunction` to draw a right-skewed curve (not a true chi-square) — the shape matters more than mathematical accuracy here.

---

## SCENE 1-05 — Foundation Models Empower AV

> **Duration:** ~60s

### [NARRATION]

```
[NARRATOR]

"And this is exactly why foundation models
matter for autonomous driving.

Look at this diagram.
On the left — the full foundation model ecosystem.
On the right — what autonomous driving needs.

The arrow in the middle says 'Empower.'
Not 'Replace.'

Foundation models don't replace the AV stack.
They give it superpowers:
automatic data labeling,
rich scenario generation,
sensor and traffic simulation —
and most importantly,
they bring language reasoning
into the decision-making process.

All of this points toward one goal:
Long-tail generalization and generalist experience."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| FM01 | Background | `Rectangle` | Fill `NAVY` |
| FM02 | Left column header "Foundation Models" | `Text` | `WHITE`, size 20, bold |
| FM03–FM07 | 5 FM category rows (Vision, Video, Vector, LLM, Multimodal) | `RoundedRectangle` + label | Fill `#1E3A5F`, stroke `BLUE` |
| FM08 | Sub-labels per row (e.g., SAM/DINO, Wan/Cosmos…) | `Text` | `LIGHT_BLUE`, size 14 |
| FM09 | Center arrow "Empower" | `Arrow` | `GOLD`, thick, left→right |
| FM10 | Right column header "Autonomous Driving" | `Text` | `WHITE`, size 20, bold |
| FM11–FM16 | 6 AD requirement rows | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN` |
| FM17 | Bottom goal text "Long-tail Generalization and Generalist Experience" | `Text` | `GOLD`, size 20, bold, centered at bottom |
| FM18 | Highlight box around FM17 | `RoundedRectangle` | Stroke `GOLD`, no fill |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(FM01)` | 0.3s |
| 2 | 0.3s | `Write(FM02)` — left header | 0.4s |
| 3 | 0.7s | `FadeIn(FM03–FM07)` — staggered 0.15s each | 0.75s total |
| 4 | 1.5s | `FadeIn(FM08)` — sub-labels appear | 0.4s |
| 5 | 2s | `Write(FM10)` — right header | 0.4s |
| 6 | 2.4s | `FadeIn(FM11–FM16)` — staggered 0.15s | 0.9s total |
| 7 | 3.5s | `GrowArrow(FM09)` — "Empower" arrow grows | 0.8s |
| 8 | 4.5s | FM09 pulses: `scale(1.1) → scale(1.0)` | 0.3s |
| 9 | 5s | `Write(FM17)` — goal text | 0.8s |
| 10 | 5.8s | `Create(FM18)` — highlight box | 0.4s |
| 11 | 6.5s | `[HOLD]` | 1.5s |

---

## SCENE 1-06 — Roadmap VLA for AV & Datasets

> **Duration:** ~60s

### [NARRATION]

```
[NARRATOR]

"Since 2023, both academia and industry
have been exploring how to use
LLMs and Vision-Language Models for driving —
in four main directions.

First: generating text-based actions —
describing what the car should do in language.

Second: generating numerical actions directly —
waypoints, steering angles, velocities.

Third: providing explicit guidance —
using language to constrain or direct
a separate planning module.

And fourth: implicit representation transfer —
using the internal representations of language models
to enrich the car's understanding of the scene.

Language matters in every single one of these approaches.
It forces the model to explain its reasoning,
not just produce a fuzzy mapping from pixels to actions.
And that inductive bias — the requirement to articulate —
is what drives better generalization.

To train these models, researchers needed new data.
DriveLM built a structured chain:
'What do I see?' →
'What do I predict?' →
'What should I do?' →
'What is the exact trajectory?'

Each step linked by language."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| RM01 | Background | `Rectangle` | Fill `#0F172A` |
| RM02 | Timeline spine | `Line` | `WHITE`, horizontal, full width |
| RM03–RM20 | Model logos/icons on timeline | `SVGMobject` or `RoundedRectangle` | 2 rows (upper/lower), color-coded by approach type |
| RM21–RM24 | 4 approach category labels (right side) | `Text` + colored bar | Textual Action=blue, Numerical=green, Explicit=orange, Implicit=purple |
| RM25 | "Language" emphasis box | `RoundedRectangle` + `Text` | `GOLD` border, bold |
| RM26 | DriveLM chain diagram | `VGroup` of 4 boxes + 3 arrows | Fill `#1E3A5F`, arrows `BLUE` |
| RM27–RM30 | DriveLM step labels | `Text` | "See" / "Predict" / "Do" / "Trajectory" |
| RM31 | Sample annotation image placeholder | `Rectangle` | Fill `#2A2A2A`, 3u×2u, right side |
| RM32 | Annotation boxes overlay on image | `Rectangle` x3 | Stroke `GOLD`, labeled |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(RM01)` | 0.3s |
| 2 | 0.3s | `Create(RM02)` — timeline | 0.6s |
| 3 | 0.9s | Model icons appear chronologically left→right, staggered 0.1s | 2s total |
| 4 | 3s | `FadeIn(RM21–RM24)` — 4 category labels | 0.2s staggered |
| 5 | 4s | `FadeIn(RM25)` — "Language" box emphasis | 0.5s |
| 6 | 5s | Timeline fades to 30% opacity | 0.4s |
| 7 | 5.4s | `FadeIn(RM26)` — DriveLM chain | 0.4s |
| 8 | 5.8s | `FadeIn(RM27–RM30)` — step labels, staggered | 0.2s each |
| 9 | 7s | `FadeIn(RM31)` — sample annotation image | 0.4s |
| 10 | 7.5s | `Create(RM32)` — annotation boxes appear one by one | 0.3s each |
| 11 | 8.5s | `[HOLD]` | 1.5s |

---

## SCENE 1-07 — Four VLA Architectures

> **Duration:** ~120s

### [NARRATION]

```
[NARRATOR]

"Let's look at four specific systems
that show how different teams
are combining language models with autonomous driving."

--- GPT-DRIVER ---

[NARRATOR]
"First: GPT-Driver.
The idea is almost beautifully naive —
take GPT-3.5, describe the driving situation in text,
and just ask it what to do.
No fine-tuning. Zero-shot.

And it actually works at a basic level —
because GPT-3.5 already absorbed
enormous amounts of common-sense knowledge
about traffic and driving from the internet."

--- BEVDriver ---

[NARRATOR]
"BEVDriver goes further.
It encodes LiDAR and camera data
into a BEV map —
a Bird's Eye View, meaning the scene is seen from above —
and then projects that spatial representation
into an LLM to predict waypoints.
3D spatial understanding meets language reasoning."

--- EMMA ---

[NARRATOR]
"EMMA, from Waymo, is one of the most ambitious.
Built on Gemini, it's fully end-to-end.
Raw camera frames go in.
Out comes: chain-of-thought reasoning,
trajectory prediction, perception bounding boxes,
and a road graph.

The car doesn't directly output a steering angle.
It thinks out loud first.
This is how a new driver thinks —
narrating their decisions before executing them."

--- DriveVLM ---

[NARRATOR]
"DriveVLM from Tsinghua uses a dual-system approach.
A VLM handles scene understanding
and high-level planning at low frequency —
it's the slow, thoughtful brain.
A separate 3D perception and trajectory module
runs at high frequency —
the fast, reactive layer.

Combining both gives you the best of both worlds.
At the cost of significant engineering complexity.

The common thread across all four:
language is no longer an add-on.
It's at the core of the architecture."
```

### [VISUAL SPEC]

The scene is split into four sequential sub-scenes (one per architecture). Each occupies the full screen, then transitions to the next.

---

**Sub-scene A: GPT-Driver**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| GA01 | Section label "GPT-Driver" | `Text` | `GOLD`, size 24, top-left |
| GA02 | Input box "Language Description of Scene" | `RoundedRectangle` | Fill `#1E3A5F`, text `WHITE` |
| GA03 | GPT logo icon | `SVGMobject` | Centered, 0.8u |
| GA04 | Arrow input→GPT | `Arrow` | `BLUE` |
| GA05 | Output box "Motion Planning Result" | `RoundedRectangle` | Fill `#1B4332` |
| GA06 | Arrow GPT→output | `Arrow` | `GREEN` |
| GA07 | Sample output text (waypoints) | `Text` inside GA05 | size 14, `WHITE` |
| GA08 | "Zero-shot" label badge | `RoundedRectangle` | Fill `GOLD`, text `NAVY`, size 14 |

**Sub-scene B: BEVDriver**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| GB01 | Section label "BEVDriver" | `Text` | `GOLD`, size 24 |
| GB02 | LiDAR sensor icon + camera icon | `SVGMobject` x2 | Top-left |
| GB03 | BEV map visualization | `Grid` or `Rectangle` with grid pattern | Fill `#1E293B`, stroke `BLUE` |
| GB04 | Arrow sensors→BEV | `Arrow` | `BLUE` |
| GB05 | LLM box | `RoundedRectangle` | Fill `#2D1B69`, stroke `#7C3AED` |
| GB06 | Arrow BEV→LLM | `Arrow` | `BLUE` |
| GB07 | Waypoints output | `Dot` x5 connected by `Line` | `GREEN` dots on map |
| GB08 | Label "3D Spatial + Language" | `Text` | `LIGHT_BLUE`, size 16 |

**Sub-scene C: EMMA (Waymo)**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| GC01 | Section label "EMMA (Waymo)" | `Text` | `GOLD`, size 24 |
| GC02 | Input stack: camera frames + text instruction | `VGroup` | Left side |
| GC03 | EMMA core (Gemini) box | `RoundedRectangle` | Fill `#1A1A2E`, stroke `GOLD`, "thinking…" label |
| GC04 | Arrow input→EMMA | `Arrow` | `BLUE` |
| GC05 | Output 1: "Chain-of-Thought" | `RoundedRectangle` | `BLUE` |
| GC06 | Output 2: "Trajectory" | `RoundedRectangle` | `GREEN` |
| GC07 | Output 3: "Perception BBoxes" | `RoundedRectangle` | `#E8A838` |
| GC08 | Output 4: "Road Graph" | `RoundedRectangle` | `#9B59B6` |
| GC09–GC12 | Arrows EMMA→each output | `Arrow` x4 | |
| GC13 | Quote "THINK FIRST, THEN ACT" | `Text` | `GOLD`, bold, size 20 |

**Sub-scene D: DriveVLM**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| GD01 | Section label "DriveVLM" | `Text` | `GOLD`, size 24 |
| GD02 | Sensor input block | `VGroup` | Left |
| GD03 | Branch arrow 1 (to VLM) | `Arrow` | `BLUE` |
| GD04 | Branch arrow 2 (to 3D pipeline) | `Arrow` | `GREEN` |
| GD05 | VLM box "Low Frequency: Scene Understanding, Planning" | `RoundedRectangle` | Fill `#2D1B69`, stroke `#7C3AED` |
| GD06 | 3D pipeline "High Frequency: Perception + Trajectory" | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN` |
| GD07 | Frequency label on VLM | `Text` | "~1 Hz", `LIGHT_BLUE` |
| GD08 | Frequency label on 3D | `Text` | "~10 Hz", `GREEN` |
| GD09 | Loop animation on GD06 | — | The 3D block flashes 2× while VLM flashes 1× |
| GD10 | Summary: "Language = Core Architecture" | `Text` | `GOLD`, size 22, bold |

### [ANIMATION]

Each sub-scene follows the same structure: **label appears → input appears → processing box appears with arrows → output appears → [HOLD 1.5s] → FadeOut → next sub-scene**.

Key timing notes:
- GPT-Driver: 20s total
- BEVDriver: 25s total
- EMMA: 35s total (most complex outputs)
- DriveVLM: 30s total

For DriveVLM (GD09 loop):
- `GD06.animate` flashes 2× while `GD05` flashes 1× using `Succession` with `rate_func=there_and_back`

For EMMA thinking animation (GC03):
- Animate "thinking…" with `Write` + `FadeOut` in a loop 2× before outputs appear

### [NOTES]
- These four sub-scenes should feel visually consistent — same background color, same label placement, same arrow style. The only variation is the fill colors of the boxes.
- Consider a brief transition slide between sub-scenes: a dark flash (0.2s) with the name of the next architecture fading in.

---

## SCENE 1-08 — AutoVLA

> **Duration:** ~75s

### [NARRATION]

```
[NARRATOR]

"Now let's look at what the UCLA lab contributed —
a model called AutoVLA.

Previous VLA systems had two problems.
First: generated actions weren't always
physically feasible.
Second: the model always used chain-of-thought reasoning,
even for trivially simple situations —
wasting time and compute.

AutoVLA introduces dual thinking modes.

Fast mode: when the situation is simple —
clear road, known conditions —
the model outputs an action directly.
No reasoning chain needed.

Slow mode: when the situation is complex —
unexpected obstacle, bad weather,
ambiguous scene —
chain-of-thought reasoning kicks in.

This mirrors how human cognition works.
Driving on a familiar highway? Automatic.
Navigating an unfamiliar intersection in fog?
You slow down and think deliberately."

[Training diagram appears]

"Training uses two stages.
SFT — Supervised Fine-Tuning — teaches the model
both fast and slow modes simultaneously.

Then RFT — Reinforcement Fine-Tuning,
specifically using GRPO —
aligns the model with rewards
that can be verified from the environment.
Did we stay in lane? Did we avoid the collision?

The results are striking.
Across all four metrics on nuPlan and nuScenes —
reasoning training always outperforms action-only training.
Teaching the model to think better
makes it act better.

RFT improved planning score by 10.6%.
And reduced runtime by 66.8%."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| AV01 | Background | `Rectangle` | Fill `#0F172A` |
| AV02 | Title "AutoVLA" | `Text` | `GOLD`, size 28, top-left |
| AV03 | "Dual Thinking Modes" label | `Text` | `WHITE`, size 22 |
| AV04 | Center decision diamond | `Polygon` (4 sides) | Fill `#1E3A5F`, stroke `BLUE` |
| AV05 | Diamond label "Situation?" | `Text` | `WHITE`, size 16 |
| AV06 | Arrow left → "Simple" | `Arrow` | `GREEN` |
| AV07 | Arrow right → "Complex" | `Arrow` | `RED_MUTED` |
| AV08 | "Fast Mode" box | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN` |
| AV09 | Fast mode label "Direct Action Output" | `Text` | `GREEN`, size 16 |
| AV10 | "Slow Mode" box | `RoundedRectangle` | Fill `#3D1A1A`, stroke `RED_MUTED` |
| AV11 | Slow mode label "Chain-of-Thought → Action" | `Text` | `RED_MUTED`, size 16 |
| AV12 | Training section divider | `Line` | `WHITE` opacity 0.3 |
| AV13 | "SFT" box | `RoundedRectangle` | Fill `#1E3A5F` |
| AV14 | SFT label "Teaches both modes" | `Text` | `LIGHT_BLUE`, size 14 |
| AV15 | "RFT (GRPO)" box | `RoundedRectangle` | Fill `#2D1B69` |
| AV16 | RFT label "Aligns with verified rewards" | `Text` | `#A78BFA`, size 14 |
| AV17 | Arrow SFT → RFT | `Arrow` | `WHITE` |
| AV18 | Results box "10.6% ↑ Planning" | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN` |
| AV19 | Results box "66.8% ↓ Runtime" | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN` |
| AV20 | Quote highlight "Reasoning training > Action-only" | `Text` | `GOLD`, size 20, bold |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(AV01)`, `Write(AV02)` | 0.6s |
| 2 | 0.8s | `Write(AV03)` | 0.4s |
| 3 | 1.2s | `FadeIn(AV04, AV05)` — decision diamond | 0.5s |
| 4 | 1.7s | `GrowArrow(AV06)` → `FadeIn(AV08, AV09)` | 0.5s |
| 5 | 2.5s | `GrowArrow(AV07)` → `FadeIn(AV10, AV11)` | 0.5s |
| 6 | 3.5s | `[HOLD]` — dual mode diagram | 1s |
| 7 | 4.5s | `FadeIn(AV12)` — divider | 0.3s |
| 8 | 4.8s | `FadeIn(AV13, AV14)` — SFT | 0.4s |
| 9 | 5.3s | `GrowArrow(AV17)` | 0.3s |
| 10 | 5.6s | `FadeIn(AV15, AV16)` — RFT | 0.4s |
| 11 | 6.5s | `Write(AV20)` — reasoning quote | 0.6s, flash |
| 12 | 7.5s | `FadeIn(AV18, AV19)` — results boxes | 0.3s each |
| 13 | 8.5s | Numbers in AV18 and AV19 `CountAnimation` (0→10.6, 0→66.8) | 1s |
| 14 | 10s | `[HOLD]` | 1.5s |

---

## SCENE 1-09 — Key Takeaways

> **Duration:** ~60s

### [NARRATION]

```
[NARRATOR]

"Four things to take away from this part.

One: foundation models unlock long-tail generalization —
the thing traditional architectures simply can't do,
because they encode rules instead of understanding.

Two: multimodal language models —
MLLMs —
are emerging as the most promising path
toward scalable autonomous driving.
They bring out-of-domain generalization
and internet-scale world knowledge.

Three: the field is still wide open.
Dual-system, unified E2E, BEV inputs, RL fine-tuning —
there is no dominant paradigm yet.
This is active exploration.

Four — and this is the honest one:
foundation models are not magic.
Safety, interpretability, and verification
are still unsolved.
Compute and latency are still barriers to deployment.
And in academia, the biggest bottleneck right now
is simply the lack of high-quality open-source data."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| K01 | Background | `Rectangle` | Fill `NAVY` |
| K02 | Takeaway 1 box | `RoundedRectangle` | Fill `#1E3A5F`, stroke `BLUE` |
| K03 | Takeaway 2 box | Same | |
| K04 | Takeaway 3 box | Same | |
| K05 | Takeaway 4 box | `RoundedRectangle` | Fill `#2A1A1A`, stroke `RED_MUTED` — different to signal the honest caveat |
| K06–K09 | Number labels "01" "02" "03" "04" | `Text` | `GOLD`, size 32, bold |
| K10–K13 | Takeaway body text | `Text` | `WHITE`, size 18 |
| K14 | "Not magic." emphasis inside K05 | `Text` | `RED_MUTED`, size 20, bold |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(K01)` | 0.3s |
| 2 | 0.3s | `FadeIn(K02, K06, K10)` — Takeaway 1 | 0.5s |
| 3 | 1.5s | `FadeIn(K03, K07, K11)` — Takeaway 2 | 0.5s |
| 4 | 3s | `FadeIn(K04, K08, K12)` — Takeaway 3 | 0.5s |
| 5 | 4.5s | `FadeIn(K05, K09, K13)` — Takeaway 4, different style | 0.5s |
| 6 | 5.5s | `Write(K14)` — "Not magic." | 0.4s, slight pulse |
| 7 | 6.5s | `[HOLD]` | 2s |

---

## SCENE 1-10 — Future Directions

> **Duration:** ~45s

### [NARRATION]

```
[NARRATOR]

"The field is converging on four directions.

Post-training for VLA alignment:
using RL and simulation to better connect
language reasoning with actual driving actions.

Unified multimodal backbone:
fusing 2D, 3D, and spatial representations
through a single backbone,
with language as the shared interface.

Efficient VLA models:
optimizing inference for low-latency,
closed-loop, real-world deployment —
because none of this matters if it can't run in real-time.

And continual learning:
models that keep learning from feedback in the world,
adapting to new regions, weather,
and traffic cultures."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| FD01 | Background | `Rectangle` | Fill `#0F172A` |
| FD02 | 2×2 grid of direction cards | `VGroup` of `RoundedRectangle` x4 | Each 4u×2.5u |
| FD03–FD06 | Direction icons (simple geometric symbols) | `SVGMobject` or `VGroup` | Top of each card, 0.8u |
| FD07–FD10 | Direction titles | `Text` | `GOLD`, size 18, bold |
| FD11–FD14 | Direction descriptions | `Text` | `WHITE`, size 14, wrapped |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(FD01)` | 0.3s |
| 2 | 0.3s | Cards appear one by one, 0.3s apart | 1.2s total |
| 3 | 1.5s | Icons and titles fade in per card | 0.2s per card |
| 4 | 2.5s | Descriptions fade in per card | 0.2s per card |
| 5 | 4s | `[HOLD]` | 1.5s |

---

## SCENE 1-11 — Bridge to Part 02

> **Duration:** ~25s

### [NARRATION]

```
[CAR mascot]

"So foundation models can help vehicles
reason better, see more, generalize further.

But there is one thing
no foundation model can fix."

[PAUSE]

"A single agent — no matter how intelligent —
is still limited by its own field of view.

If there's a car blocking the line of sight,
if there's a pedestrian behind a corner —
no amount of reasoning helps.

That's why Part 2 is about something different:
not making one agent smarter —
but making many agents cooperate."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| BR01 | Background | `Rectangle` | Fill `NAVY` |
| BR02 | Single car icon, alone | `SVGMobject` | Center, with FOV cone |
| BR03 | FOV cone | `Triangle` or `Sector` | Fill `BLUE`, opacity 0.2 |
| BR04 | Obstacle blocking FOV | `Rectangle` | Fill `#555555` |
| BR05 | Blind zone behind obstacle | `Polygon` | Fill `RED_MUTED`, opacity 0.15 |
| BR06 | Text "Single agent limit" | `Text` | `WHITE`, size 20 |
| BR07 | Fade: multiple cars appear | `SVGMobject` x2 | Like Scene I-02 hook ending |
| BR08 | "Part 02: Collective Intelligence" | `Text` | `GOLD`, size 26, bold |
| BR09 | Part 02 node from roadmap | — | Pull from roadmap (Scene I-03), scale up briefly |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(BR01, BR02, BR03)` | 0.5s |
| 2 | 0.5s | `FadeIn(BR04)` — obstacle appears | 0.4s |
| 3 | 0.9s | `FadeIn(BR05)` — blind zone | 0.3s |
| 4 | 1.5s | `Write(BR06)` | 0.4s |
| 5 | 2.5s | `[HOLD]` | 1s |
| 6 | 3.5s | `FadeIn(BR07)` — more cars appear, comm lines | 0.8s |
| 7 | 4.3s | `Write(BR08)` | 0.6s |
| 8 | 5s | `[HOLD]` | 1s |
| 9 | 6s | Transition to Part 02 title card | 0.5s fade |

---

## End of Session 1 (Introduction + Part 01)

> **Next file:** `spec_part02.md`
> **Scenes covered:** I-01, I-02, I-03, 1-01 through 1-11
> **Total estimated duration:** ~13 min

---

*Production note: All mascot animations assume SVG files with at least 2–3 keyframe states (idle, speaking, reacting). If not ready, substitute with simple colored circles with label text — the spec structure remains the same.*
