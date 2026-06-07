# 09 — Fix Checklist (consolidated from 3 review rounds)

> One row per scene. Lists every reviewer-flagged issue across reviews 1, 2, 3 (in `spec_prompts/spec_review_*.md`), plus durable design-system fixes.
>
> Use this when you open a scene file. If a row says **STATUS: open**, do the listed fix.

---

## How to use

For the scene you're editing:
1. Find its row.
2. Apply every fix listed.
3. Render at `-ql`, eyeball.
4. If clean, mark `STATUS: closed` (or replace the row with a single `closed` line).
5. If new issues found, add a row labeled `R4` (round 4 — your own review pre-handoff).

Keys:
- **R1 / R2 / R3** = which review round flagged the issue
- **DS** = durable design-system rule (white BG, English-only, tight bubbles, etc.)

---

## Intro

| Scene | Issues |
|---|---|
| **I-01 Title Card** | R1: ok. **DS**: verify navy bg, white→navy→white transition. Use new `BG_PART_TITLE`. |
| **I-02 Hook** | R1: "I see." text overlaps `fm1` and `fm2` (GPT, VLM) — **fix: `FadeOut(fm1, fm2)` before `Write(i_see)`**. **DS**: thought bubble uses new `TightBubble`. **DS**: scene-end `FadeOut` of `divider` and `payoff` already exists; verify. |
| **I-03 Roadmap** | R1: ok. Whole canvas is dedicated to the roadmap, so labels are fine here. |

---

## Part 1

| Scene | Issues |
|---|---|
| **P01-S01 Opening** | R1: PI speaks Vietnamese — **change all on-screen text to English**. R1: text centered, PI overlapping center text — **lift text up, place PI lower-right**. R1: multiple bubble positions — **use ONE fixed bubble position; show/hide, no second bubble**. R2: PI too high, overlaps text — **PI position `DOWN*1.5+RIGHT*4` or further from text**. R3: same issue — bubble overlaps prior content. |
| **P01-S02 GenAI Boom** | R1: FM box too narrow vs text — **widen**. R1: arrow not straight — **use explicit `Arrow(start_point, end_point)`**. R2: PI bubble (top-right) overlaps FM box (bottom-left of FM diagram) — **after PI bubble, lift FM box up by 0.3u OR position PI further into corner**. |
| **P01-S03 AV Arch** | R1: ok. **DS**: white BG, uniform pipeline block heights. |
| **P01-S04 Long-Tail** | R1: axes appear AFTER distribution — **draw axes FIRST, then distribution**. R1: after 3 nodes squeeze to 1%, shrink chart UP, then mascots speak (don't speak while distribution is centered, causes overlap). R2: same issue — mascots talk before fading distribution. R3: same — axes BEFORE function. **THE most-flagged issue in the project — fix definitively.** |
| **P01-S05 FM Empower** | R1: scene has navy background — **switch to white BG**. R2: left-side 5 boxes too narrow for text (multimodal text overflows) — **widen to ≥ 2.4u, 2-line labels where needed**. |
| **P01-S06 VLA Roadmap** | R1: chain labels too close to nodes — **fade labels before next node, don't dim**. R2: same — text on roadmap close to line. R3: "language is at the core" box too narrow, text touches edges — **widen to ~8u**. R3: end-of-scene replays everything — **REMOVE the replay**, end with single FadeOut. |
| **P01-S07 VLA Arch** | R1: BEVDriver blocks not aligned horizontally — **use `arrange(RIGHT, buff=0.5)`, uniform block height**. R2: GPT-Driver arrows too short — **arrows from box edge to box edge with `buff=0.05`**. R2: BEVDriver still misaligned. R3: BEV map illustration disrupts row alignment — **redraw simplified or remove inline**. |
| **P01-S08 AutoVLA** | R1: "reasoning training" annotation overlaps Stage 1/2 — **lift Stage region UP**. R2: Stage region pulled down causes overlap with content — same fix. R3: scene end leaves "Stage 1" and "Stage 2" labels on screen — **explicit `FadeOut` of stage labels in cleanup**. |
| **P01-S09 Takeaways** | R1: takeaway cards too narrow — **width ≥ 4.5u, buff 0.6u**. |

---

## Part 2

| Scene | Issues |
|---|---|
| **P02-S01 Title** | R1: ok. **DS**: navy bg, transition cleanly to/from white. |
| **P02-S02 Background** | R1: 80% reduction box overlaps human-error grid — **shrink the grid + recolor (red→orange) + brace label, no separate box**. R2: same — box overlaps figure; place vertically along 94% text. R3: bottom note overlaps grid — **remove the note**. |
| **P02-S03 Evolution** | R1: in-scene roadmap zigzag overlaps content — **remove roadmap from body scenes (DS rule)**. R1: E2E advantages box overlaps roadmap — same fix. R1: mascot bubble overlaps roadmap — same fix. R3: end-of-scene replays — **REMOVE**. |
| **P02-S04 Occlusion** | R1: coverage gain area too small, red zones still visible — **`Transform` red region into green region** (not hide+show). R2: timing bug — when added cars come in, blind field fades before green appears. **Use `ReplacementTransform(red_zone, green_zone)`, simultaneous with car reveal**. R2: replace circle radar with **expanding ring sweep** (use `ValueTracker` updater). |
| **P02-S05 Related Works** | R1: chain text close to node, overlap on next reveal — **fade label before next**. R2: same; boxes too small — **widen to ≥ 1.6u**. R2: zigzag layout — **all labels on one side**. R2: red/green comparison lines overlap text — **move text up first, then plot lines**. |
| **P02-S06 Three Questions** | R2: forking into 3 arrows looks better than one arrow with 3 sub-labels — **3 separate arrows**. |
| **P02-S07 V2XPnP** | R1: text close to arrows, yellow box overlap — **remove yellow "n-frames" box**. R1: spatial-attn box close to temporal-feature, agent-2 — fixed by Review 2's serpentine layout. R1: arrows from features to spatial-attn point wrong — **straight arrows from each feature's right edge to spatial-attn's left edge**. R1: detection box not aligned with multi-agent representation — **explicit alignment**. R2 (verbatim, key fix): **shift pipeline UP, center spatial-attn between two feature blocks (vertical center alignment), wider horizontal spread, downward arrow from spatial-attn to multi-agent rep, serpentine flow for detection→prediction (left→right→down→left)**. |
| **P02-S08 Dataset** | R1: ok. |
| **P02-S09 TurboTrain** | R1: pipeline-stage right side overlaps chart annotation on left — **move chart annotations to be near the chart (left), not near the pipeline (right)**. R1: 4 horizontal arrows in Stage 2 unclear — **label them: 2 green "free", 2 red "suppress", alternating**. R2: nothing fixed yet — same issues. |
| **P02-S10 RiskMap** | R1: "RiskMap" text overlapped — **move x-axis ticks BELOW the line; shift module-blocks to RIGHT**. R2: nothing fixed yet. |
| **P02-S11 Summary** | R1: ok. |
| **P02-S12 Bridge** | R1: mascot bubble overlaps "reality" box — **fade box first, OR move bubble to a non-overlapping anchor**. **DS**: white→navy transition for next scene. |

---

## Part 3

| Scene | Issues |
|---|---|
| **P03-S01 Title** | R2: tagline ("Theory + Engineering" or similar) overlaps presenter — **move tagline below quote, not above presenter**. |
| **P03-S02 Four Pillars** | R1: 4-block pipeline overlap — **shift pipeline LEFT, or stack vertically**. R2: not fixed. |
| **P03-S03 Smart Intersection** | R1: missing "intersection at UCLA" caption — **add it**. R1: 2 annotations (infra node, connect) horizontal-row overlap with shrunk image — **stack vertically on LEFT**. R1: dialog bubble persists, overlaps next content — **`FadeOut` bubble after dialog**. R2: not fixed. |
| **P03-S04 Calibration Time** | R1: car/box dynamics confusing — **draw lane markings FIRST**. R2 (verbatim): one car drives to a position, stops; spawn ghost at same position; ghost moves +50ms further; brace = "1m". |
| **P03-S05 Calibration Space** | R1: only 2 points — **add multiple aligned point pairs** (~5 each). R1: when aligned, labels overlap — **color-code per sensor source**. R2: 4 mini coord systems overlap "without calibration" axes/text — **lift mini-axes UP, give space for ground-truth axes below**. |
| **P03-S06 Data Collection** | R1: ok. |
| **P03-S07 Localization Why** | R1: ok. |
| **P03-S08 Kalman Filter** | R1: ok. |
| **P03-S09 CooperFuse** | R1: NMS demo lacks motion — **add bbox rotation (or shift) animation in NMS to show orientation difference**. |
| **P03-S10 V2X-ReaLO** | R1: compression should look like compress→smaller block→onto balance scale (with wobble) — **redraw**. R1: arrows not straight — **use `Arrow(start, end)` not curved**. R2: gold dot offset right of center — **center it on the curve**. R2: scale too small — **make it bigger**. |
| **P03-S11 OpenCDA-ROS** | R1: arrows overlap — **spread vertically with `arrange(DOWN, buff=0.5)` or put on different y-coords**. |
| **P03-S12 SimBoost** | R1: ok. |
| **P03-S13 InfraX** | R1: ok. |
| **P03-S14 Bridge** | R1: CAR mascot box persists, overlaps next content — **`FadeOut(bubble)` before transition**. **DS**: white→navy at end. |

---

## Part 4

| Scene | Issues |
|---|---|
| **P04-S01 Title** | R2: 3 boxes (data/training/inference) overlap title and presenter — **REMOVE the boxes from title card; defer 3-bottleneck reveal to S02**. |
| **P04-S02 Why Efficiency** | R1: ok. |
| **P04-S03 Annotation Cost** | R1: distribution chart centered, "5x in 2 years" overlaps last bar — **shift chart LEFT, place "5×" annotation on RIGHT**. R1: bullets in chart area — **move bullets RIGHT-OF-CHART**. |
| **P04-S04 CooPre** | R2: grid map not centered between two source agents — **center horizontally on midpoint**. |
| **P04-S05 Multi-Task Conflict** | R1: gradient conflict diagram should be **3D coord with vectors on a plane** (not abstract). R3: multi-frame box too narrow at scene start — **widen, watch for arrow overlap**. |
| **P04-S06 TurboTrain** | R1: ok. |
| **P04-S07 Latency Chain** | R1: total time inline next to chain looks unbalanced — **move "total time" to a NEW LINE below chain**. R1: 3 chain blocks too close — **wider buff, arrows visible**. R1: 2 charts inconsistent (one horizontal, one vertical) — **make both vertical**. R1: lots of empty space below — **enlarge the charts to use it**. R2: not fixed. |
| **P04-S08 QuantV2X** | R1: INT8 overlaps FP32 (shrink animation lands on top of FP32 box) — **shrink animation must end SIDE-BY-SIDE, not on top**. R1: yellow text overlap red text — **explicit `next_to` with buff**. R2: 3 bullet points at top overlap FP32 box — **move bullets DOWN below FP32**. |
| **P04-S09 Summary** | R1: ok. |
| **P04-S10 Bridge** | R1: bullets not left-aligned (different x) — **align all to same x-coord**. R2: bullet ticks overlap small human figures — **move ticks LEFT, figures go RIGHT**. |

---

## Part 5

| Scene | Issues |
|---|---|
| **P05-S01 Title** | (No prior review yet — Part 5 was largely stubs.) **DS**: all 5 roadmap dots light gold simultaneously — first time in series. |
| **P05-S02 Physical AI Vision** | (Stub — implement to spec_part05.md) |
| **P05-S03 Micro-Mobility** | (Stub) |
| **P05-S04 MetaUrban** | (Stub) — **DS**: Stuart Geman quote weight; power-law chart with 3 curves clearly distinguishable. |
| **P05-S05 UrbanSim** | (Stub) — **DS**: CPU-GPU ping-pong is the visual metaphor; 180-days vs 3-hours bar disproportion must be felt. |
| **P05-S06 CityWalker + PedGen** | (Stub) — **DS**: zombie pedestrians literally walk through walls. |
| **P05-S07 Vid2Sim** | R3: 3DGS and Mesh rectangles too close vertically — **separate vertically**. R3: pulling them together later confuses layout — **either keep them apart, or move appearance label up to clear center**. R3: sim-to-real arrow shrinks, but sim/real boxes don't move — **either keep arrow size and move boxes closer, OR brace narrows**. R3: text too small — **bump up**. |
| **P05-S08 Finale** | (Stub) — **THE most important scene**. **DS**: all agent types from all 5 parts in final wide shot. **DS**: 3-second hold at end is intentional. |
| **P05-S09 Credits** | (Stub) — CAR mascot wave. |

---

## Universal cross-scene fixes (apply to ALL scenes)

These apply EVERYWHERE; check while editing each scene:

| ID | Rule | Source |
|---|---|---|
| U1 | White background unless this is a part-title card or deliberate emotional scene | DS |
| U2 | All on-screen text in English | R1 |
| U3 | Replace `ThoughtBubble`/`PIBubble`/`SpeechBubble` with new `TightBubble`-based versions | DS / [02_COMPONENTS.md](02_COMPONENTS.md) |
| U4 | One bubble visible per mascot at a time. Show → hold ≥ 1s → fade. Don't stack. | R1 |
| U5 | Scene end: `FadeOut` ALL transient mobjects. No leftovers. | R3 |
| U6 | Roadmap strip is for title cards only. Body scenes don't show it. | DS / R1 |
| U7 | Axes drawn BEFORE plotted data | R1, R2, R3 |
| U8 | Pipeline blocks: uniform height, `arrange(RIGHT, buff=...)`, no eyeball spacing | R1, R2 |
| U9 | Arrows: `Arrow(box_a.get_right(), box_b.get_left(), buff=0.05)`. Not `ArcBetweenPoints` for straight needs. | R1, R2 |
| U10 | When in doubt about overlap, fade the older mobject before showing the new one. Movement is the second-best fix. | R1, R2, R3 |
| U11 | Strip the mojibake `â”€` Unicode-mangled comments. Replace with `# ── ──` or just plain text. | DS |
| U12 | No `sys.path.insert(...)` clutter at top of scene files unless absolutely necessary | DS |
