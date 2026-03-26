# Beyond Self-Driving — Production Spec
## Session 3 of 5: Part 03 — Bridging Simulation and Reality in Cooperative V2X Systems

> **Original speaker:** Zhaoliang Zheng, PhD Candidate, UCLA Mobility Lab
> **Reference slides:** Part_3.pdf
> **Estimated duration:** ~12 min
> **Character note:** This is the most engineering-heavy part of the tutorial. Tone shifts from "conceptual" to "grounded" — narration is more concrete, visuals lean on system diagrams and real sensor setups rather than abstract arrows.

---

## Quick Reference

Same conventions as Session 1 & 2. Additional tags for Part 03:

| Tag | Meaning |
|---|---|
| `INF` | Infrastructure node (fixed, roadside unit) |
| `CAV` | Connected Automated Vehicle (moving agent) |
| `LIDAR_SWEEP` | Animated rotating arc simulating LiDAR scan |

**Part 03 additional colors:**

| Name | Hex | Used for |
|---|---|---|
| `INFRA_ORANGE` | `#E67E22` | Infrastructure nodes on maps |
| `ROAD_GRAY` | `#4A4A4A` | Road/map elements |
| `SENSOR_CYAN` | `#00BCD4` | Sensor beams, calibration lines |

---
---

## SCENE 3-01 — Title & Context Handoff

> **Duration:** ~25s

### [NARRATION]

```
[NARRATOR]

"Part 3. Bridging Simulation and Reality
in Cooperative V2X Systems.
Speaker: Zhaoliang Zheng, UCLA Mobility Lab.

Parts 1 and 2 gave us theory:
cooperative fusion, spatio-temporal reasoning,
interpretable planning.

But theory doesn't drive.

This part is the engineering layer —
where does real data come from,
what happens when you bolt sensors onto a real intersection,
and how do you make all of it
actually run in the physical world?"
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| T01 | Background | `Rectangle` | Fill `NAVY` |
| T02 | Part number "03" watermark | `Text` | Font size 72, `GOLD`, opacity 0.15 |
| T03 | Title text | `Text` | Font size 30, `WHITE`, bold, center |
| T04 | Speaker label | `Text` | Font size 18, `LIGHT_BLUE` |
| T05 | Divider | `Line` | `BLUE`, 8u |
| T06 | "Theory → Engineering" visual bridge | `VGroup`: two labels + arrow | Left: "Theory" `PURPLE`, right: "Engineering" `GREEN`, arrow `GOLD` between |
| T07 | Roadmap strip | `VGroup` (reused) | Bottom, Part 03 node highlighted `GOLD` |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(T01, T02)` | 0.4s |
| 2 | 0.4s | `Write(T03)` | 1s |
| 3 | 1.4s | `FadeIn(T04)` | 0.3s |
| 4 | 1.7s | `Create(T05)` | 0.3s |
| 5 | 2s | `FadeIn(T06)` — bridge visual | 0.6s, arrow draws left→right |
| 6 | 2.6s | `FadeIn(T07)` | 0.4s |
| 7 | 3.5s | `[HOLD]` | 1s |

---

## SCENE 3-02 — Four Pillars Overview

> **Duration:** ~30s

### [NARRATION]

```
[NARRATOR]

"The content here breaks into four pillars —
and they have to be built in this exact order.

You cannot localize before you have hardware.
You cannot fuse before you can localize.
You cannot simulate reality before you understand it.

First: Hardware and Data Collection.
Second: Mapping and Localization.
Third: Late and Intermediate Fusion in the real world.
Fourth: Digital Twin — closing the loop
between simulation and reality.

These four address three core challenges:
solving the blind-spot problem through cooperation,
making data trustworthy enough to learn from,
and ensuring safety at dangerous urban intersections."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| OV01 | Background | `Rectangle` | Fill `#0F172A` |
| OV02 | Vertical timeline / roadmap (4 stations) | `Line` + `Dot` x4 | `WHITE` vertical line, left side |
| OV03 | Station 1 "Hardware + Data Collection" | `RoundedRectangle` | Fill `#1E3A5F`, stroke `BLUE`, right of OV02 |
| OV04 | Station 2 "Mapping + Localization" | Same | |
| OV05 | Station 3 "Late + Intermediate Fusion" | Same | |
| OV06 | Station 4 "Digital Twin" | Same | |
| OV07–OV10 | Station icons (hardware bolt, map pin, network node, twin) | Simple `VGroup` | Left of each station label |
| OV11 | Dependency arrows between stations | `Arrow` x3 | `BLUE`, station→station, downward |
| OV12 | Three challenge badges (right side) | `RoundedRectangle` x3 | Fill `#2A1A1A`, stroke `RED_MUTED` |
| OV13–OV15 | Challenge texts | `Text` | `WHITE`, size 15 |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(OV01)` | 0.3s |
| 2 | 0.3s | `Create(OV02)` — spine draws downward | 0.6s |
| 3 | 0.9s | Stations appear top→bottom, staggered 0.3s each | 1.2s total |
| 4 | 2.1s | Station icons fade in | 0.2s per icon |
| 5 | 3s | `GrowArrow(OV11)` x3, staggered 0.2s | 0.6s total |
| 6 | 4s | `FadeIn(OV12–OV15)` — challenge badges | 0.5s |
| 7 | 5s | `[HOLD]` | 1s |

### [NOTES]
- Station 1 should be pre-highlighted (stroke `GOLD`) to signal "this is where we start." The highlight will transfer to each subsequent station as the part progresses — a subtle progress indicator.

---

## SCENE 3-03 — UCLA Smart Intersection

> **Duration:** ~60s

### [NARRATION]

```
[NARRATOR]

"Here's the actual deployment site —
the intersection of Charles E. Young Drive
and Westwood Plaza, on the UCLA campus.

This is not a test track.
Not a closed course.
A live, active intersection
with real traffic and real pedestrians.

The system consists of two infrastructure nodes
and two connected automated vehicles."

[Infrastructure nodes]

[NARRATOR]
"Infrastructure node at the Northwest corner:
a 128-line LiDAR, two cameras, and one radar.

Infrastructure node at the Southeast corner:
a 64-line LiDAR, two cameras,
and a C-V2X communication unit."

[Vehicles]

[NARRATOR]
"Each connected vehicle:
four stereo cameras for wide-angle coverage,
a LiDAR RoboSense Ruby Plus 128-line,
and GNSS plus IMU for position and orientation."

[PI mascot appears]

[PI]
"Tại sao cần nhiều sensor đến vậy?
Không phải overkill à?"

[CAR mascot]

[CAR]
"Every sensor type has its own blind spot.
Camera fails in backlight or darkness.
LiDAR degrades in heavy rain.
GNSS loses accuracy between tall buildings.

Redundancy isn't overkill.
It's the minimum condition
for a reliable system outside a lab."
```

### [VISUAL SPEC]

**Section A — Intersection Map**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| IS01 | Background | `Rectangle` | Fill `#0A0A0A` |
| IS02 | Top-down map of intersection | `VGroup` | Road: `ROAD_GRAY` rectangles; sidewalks: darker gray |
| IS03 | Road lane markings | `DashedLine` x4 | `WHITE`, opacity 0.6 |
| IS04 | NW infrastructure node marker | `Square` | Fill `INFRA_ORANGE`, 0.2u, rotated 45° (diamond shape) |
| IS05 | SE infrastructure node marker | Same as IS04 | |
| IS06 | Label "NW Node" | `Text` | `INFRA_ORANGE`, size 14 |
| IS07 | Label "SE Node" | `Text` | `INFRA_ORANGE`, size 14 |
| IS08 | CAV 1 icon | `SVGMobject` or `VGroup` | `BLUE`, 0.3u |
| IS09 | CAV 2 icon | Same | |
| IS10 | "Charles E. Young Dr & Westwood Plaza" label | `Text` | `WHITE`, size 14, italic, bottom |
| IS11 | "UCLA Campus — Live Intersection" badge | `RoundedRectangle` | Fill `RED_MUTED`, text `WHITE`, top-right corner |

**Section B — Sensor Breakdown**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| SB01 | Sensor table: 2 columns (INF Nodes / CAVs) | `Table`-style `VGroup` | Side by side |
| SB02 | INF column header | `Text` | `INFRA_ORANGE`, bold |
| SB03–SB05 | INF sensor rows | `Text` | `WHITE`, size 15 |
| SB06 | CAV column header | `Text` | `BLUE`, bold |
| SB07–SB09 | CAV sensor rows | `Text` | `WHITE`, size 15 |

**Section C — Sensor Failure Illustration**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| SF01 | Camera icon | `SVGMobject` | Center |
| SF02 | "Backlight / Night" failure overlay | `Rectangle` | Fill `#000000`, opacity 0.8, covers SF01 |
| SF03 | LiDAR icon | `SVGMobject` | |
| SF04 | Rain noise overlay | `Dot` x20 scattered | `WHITE`, random positions, opacity 0.3 — simulates LiDAR noise |
| SF05 | GNSS icon | `SVGMobject` | |
| SF06 | Building occlusion overlay | `Rectangle` | Fill `ROAD_GRAY`, tall, placed next to SF05 |
| SF07 | "Redundancy = Reliability" label | `Text` | `GOLD`, size 22, bold |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(IS01, IS02, IS03)` — map | 0.6s |
| 2 | 0.6s | `FadeIn(IS04, IS06)` — NW node | 0.3s |
| 3 | 0.9s | `FadeIn(IS05, IS07)` — SE node | 0.3s |
| 4 | 1.2s | `FadeIn(IS08, IS09)` — CAVs | 0.3s |
| 5 | 1.5s | `FadeIn(IS10, IS11)` — labels | 0.3s |
| 6 | 2.5s | `[HOLD]` | 0.8s |
| 7 | 3.3s | Map scales down to left half, `FadeIn(SB01–SB09)` — sensor table on right | 0.8s |
| 8 | 5s | `[HOLD]` | 0.8s |
| 9 | 5.8s | Sensor table fades, SF icons appear centered, 3 across | 0.5s |
| 10 | 6.3s | `FadeIn(SF02)` — camera blacks out | 0.4s |
| 11 | 6.7s | `FadeIn(SF04)` — LiDAR noise appears | 0.4s, dots scatter randomly |
| 12 | 7.1s | `FadeIn(SF06)` — GNSS blocked | 0.4s |
| 13 | 7.8s | `FadeIn(PI)` with question bubble | 0.4s |
| 14 | 8.5s | `FadeIn(CAR)` with response | 0.4s |
| 15 | 9.5s | `Write(SF07)` — "Redundancy = Reliability" | 0.5s |
| 16 | 10.5s | `[HOLD]` | 1s |

---

## SCENE 3-04 — Sensor Calibration: Time

> **Duration:** ~50s

### [NARRATION]

```
[NARRATOR]

"With multiple agents and multiple sensors running
at the same time, a problem appears immediately:
how do you synchronize everything?

Start with time.

A vehicle moving at 60 kilometers per hour —
that's roughly 17 meters per second.
If an infrastructure node sends an observation
with a 50-millisecond delay,
that object will appear almost one meter
away from where it actually is.

One meter.
At an intersection where decisions happen
in fractions of a second.

The solution: use GPS as a shared time reference
across all agents simultaneously.
And use hardware triggers — not software — to fire the sensors.
Software triggers have jitter.
A hardware trigger fires every sensor
at exactly the same clock tick."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| TC01 | Background | `Rectangle` | Fill `#0F172A` |
| TC02 | Road (horizontal line) | `Line` | `WHITE`, 12u wide |
| TC03 | Moving car icon | `VGroup` | `BLUE`, small |
| TC04 | Ghost car (50ms-lagged position) | Same style as TC03 | `RED_MUTED`, opacity 0.5 |
| TC05 | "~1m" distance indicator | `DoubleArrow` between TC03 and TC04 | `RED_MUTED` |
| TC06 | "50ms delay" label above distance | `Text` | `RED_MUTED`, size 18, bold |
| TC07 | Speed label | `Text` | `WHITE`, size 14 — "60 km/h" |
| TC08 | Solution box (right half) | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN` |
| TC09 | Solution item 1 "GPS shared time reference" | `Text` with `SENSOR_CYAN` dot | Size 16, `WHITE` |
| TC10 | Solution item 2 "Hardware Trigger (not software)" | `Text` with `GREEN` dot | Size 16, `WHITE` |
| TC11 | ✗ "Software: has jitter" sub-note | `Text` | `RED_MUTED`, size 13, italic |
| TC12 | ✓ "Hardware: exact clock tick" sub-note | `Text` | `GREEN`, size 13 |
| TC13 | GPS satellite icon (simplified) | `VGroup` | `GOLD`, top of scene, lines down to TC03 and INF node icon |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(TC01, TC02)` | 0.3s |
| 2 | 0.3s | `FadeIn(TC03)` — car appears on road | 0.3s |
| 3 | 0.6s | `TC03.animate.shift(RIGHT*3)` — car moves | 1s |
| 4 | 1.6s | `FadeIn(TC04)` at lagged position | 0.4s — ghost appears where car was 50ms ago |
| 5 | 2s | `FadeIn(TC05, TC06)` — gap indicator | 0.4s |
| 6 | 2.6s | `Write(TC07)` — speed label | 0.3s |
| 7 | 3.5s | `FadeIn(TC08, TC09, TC10)` — solution box | 0.6s |
| 8 | 4.2s | `FadeIn(TC11, TC12)` — sub-notes | 0.3s |
| 9 | 5s | `FadeIn(TC13)` — GPS satellite, signal lines draw down | 0.5s |
| 10 | 6s | `[HOLD]` | 1.5s |

---

## SCENE 3-05 — Sensor Calibration: Space

> **Duration:** ~45s

### [NARRATION]

```
[NARRATOR]

"Now space.

Every sensor lives in its own coordinate frame.
A camera sees the world from its lens position.
A LiDAR has its own origin point.
The vehicle has a body frame.
And then there's the world frame — the ground truth.

Intrinsic calibration defines a camera's
focal length and lens distortion —
how it sees.

Extrinsic calibration defines the transform
between coordinate frames:
camera to LiDAR, LiDAR to vehicle body,
vehicle body to world frame.

If extrinsic calibration is wrong,
two point clouds from different sources —
when fused together —
will appear to show objects that don't exist.
Ghost objects.
You're fusing two misaligned realities.

These calibration tools are released open-source
through PJLab's SensorsCalibration on GitHub."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| SC01 | Background | `Rectangle` | Fill `#0A0A0A` |
| SC02 | Camera frame axes (XYZ) | `ThreeDAxes` or `VGroup` of 3 `Arrow` | `SENSOR_CYAN`, small, top-left |
| SC03 | LiDAR frame axes | Same | `GOLD`, center |
| SC04 | Vehicle body frame axes | Same | `BLUE`, larger |
| SC05 | World frame axes | Same | `WHITE`, largest, bottom-right |
| SC06 | Transform arrows between frames | `CurvedArrow` x3 | Dashed, `WHITE` opacity 0.6 |
| SC07 | Frame labels | `Text` x4 | Match each axis color, size 14 |
| SC08 | Ghost object demo (left half) | `VGroup` | Two point clouds drawn offset |
| SC09 | Point cloud A | `Dot` x12, cluster | `BLUE`, clustered to form a car shape |
| SC10 | Point cloud B (misaligned) | `Dot` x12, cluster | `RED_MUTED`, same shape but offset 0.5u |
| SC11 | "Ghost Object" label with arrow | `Text` + `Arrow` | `RED_MUTED`, pointing to overlap zone |
| SC12 | ✓ Aligned demo (right half) | Same cloud setup | Both `GREEN`, perfectly overlapping |
| SC13 | "Correct Calibration" label | `Text` | `GREEN`, size 16 |
| SC14 | GitHub / open-source badge | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN`, "PJLab SensorsCalibration" |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(SC01)` | 0.3s |
| 2 | 0.3s | `FadeIn(SC02, SC03, SC04, SC05)` — all frames | 0.6s, staggered 0.15s |
| 3 | 1s | `FadeIn(SC06)` — transform arrows between frames | 0.5s, each arrow draws sequentially |
| 4 | 1.5s | `FadeIn(SC07)` — labels | 0.3s |
| 5 | 2.5s | Frame diagram shrinks to right half | 0.4s |
| 6 | 2.9s | `FadeIn(SC08, SC09, SC10)` — misaligned demo | 0.5s |
| 7 | 3.4s | `Write(SC11)` — "Ghost Object" | 0.4s |
| 8 | 4.2s | `FadeOut(SC09, SC10, SC11)` | 0.3s |
| 9 | 4.5s | `FadeIn(SC12, SC13)` — correct alignment | 0.5s, clouds snap together |
| 10 | 5.5s | `FadeIn(SC14)` — open source badge | 0.4s |
| 11 | 6.5s | `[HOLD]` | 1s |

### [NOTES]
- SC09 and SC10 misalignment: draw both point cloud clusters with a visible offset (~0.4u) so the "ghost" car shape is obvious. The two clusters should be recognizable as the same object, just shifted.
- SC12 "snap together": animate by `Transform(SC10, SC09.copy())` — the red cluster moves to overlap the blue one, then both turn `GREEN`.

---

## SCENE 3-06 — Data Collection Strategy

> **Duration:** ~35s

### [NARRATION]

```
[NARRATOR]

"With hardware calibrated, it's time to collect data.

This isn't just driving around randomly.
The team designed specific routes —
right turns, left turns, straight-through —
and then combined them systematically.

Each combination gives a different angle
and overlap pattern between infrastructure sensors
and vehicle sensors.

Data was also collected at different times of day —
capturing varied lighting conditions,
traffic density, and weather.

The result:
two datasets — V2X-Real published at ECCV 2024,
and V2XPnP-Seq referenced in Part 2.
This intersection is where they were born."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| DC01 | Background | `Rectangle` | Fill `#0F172A` |
| DC02 | Intersection top-down view (reuse IS02 style) | `VGroup` | Center |
| DC03 | Basic route 1 — right turn | `Arc` | `BLUE`, arrow at end |
| DC04 | Basic route 2 — left turn | `Arc` | `GREEN`, arrow at end |
| DC05 | Basic route 3 — straight | `Line` | `GOLD`, arrow at end |
| DC06 | Combined routes overlay | Multiple `Arc` + `Line` | All three colors, denser |
| DC07 | Time-of-day strip (right side) | `VGroup` of 3 bands | Morning (yellow-orange), Afternoon (bright), Night (dark blue) |
| DC08 | Time labels | `Text` | `WHITE`, size 14 |
| DC09 | Dataset result badges | `RoundedRectangle` x2 | `#1B4332`, stroke `GREEN` |
| DC10 | "V2X-Real — ECCV 2024" | `Text` | `GREEN`, size 16 |
| DC11 | "V2XPnP-Seq" | `Text` | `GREEN`, size 16 |
| DC12 | Link arrow "from Part 2" | `Text` + `Arrow` | `LIGHT_BLUE`, small, italic — "referenced in Part 2" |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(DC01, DC02)` | 0.4s |
| 2 | 0.4s | `Create(DC03)` — right turn route | 0.4s |
| 3 | 0.8s | `Create(DC04)` — left turn | 0.4s |
| 4 | 1.2s | `Create(DC05)` — straight | 0.4s |
| 5 | 2s | `FadeIn(DC06)` — combined overlay | 0.5s, overlay fades in over basic routes |
| 6 | 3s | `FadeIn(DC07, DC08)` — time strip | 0.5s |
| 7 | 4s | `FadeIn(DC09, DC10, DC11, DC12)` — dataset badges | 0.5s |
| 8 | 5s | `[HOLD]` | 1.5s |

---

## SCENE 3-07 — Mapping & Localization: Why It's a Prerequisite

> **Duration:** ~60s

### [NARRATION]

```
[NARRATOR]

"Mapping and localization is the backbone.
Not a nice-to-have. Not an add-on.
A prerequisite for everything else.

HD Map serves three roles in this system:
the data acquisition platform needs it to geo-tag sensor data.
The localization module needs it to know exactly
where each vehicle is.
The digital twin needs it as an environment scaffold.

But for cooperative perception,
localization has one additional critical meaning."

[Illustration appears]

[NARRATOR]
"Imagine an infrastructure node and a vehicle
are both observing the same pedestrian —
from different angles.

To fuse those two observations,
both agents need to know their exact position
in the same world coordinate frame.

If they don't —
the same pedestrian will appear as two different objects.
One from each agent's local coordinate system,
with no way to resolve them.

And it gets worse.
With incorrect localization,
fused result is not just less accurate
than each agent individually —
it's actively worse than single-agent.
Wrong information injected in makes things worse."

[PI mascot]

[PI]
"Vậy giải pháp là gì?"
```

### [VISUAL SPEC]

**Section A — HD Map roles**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| ML01 | Background | `Rectangle` | Fill `NAVY` |
| ML02 | "HD Map" center node | `Circle` | Fill `GOLD`, r=0.5u, label `NAVY` bold |
| ML03 | Role 1 arm "Data Acquisition" | `Arrow` + label | `BLUE` |
| ML04 | Role 2 arm "Localization" | `Arrow` + label | `GREEN` |
| ML05 | Role 3 arm "Digital Twin" | `Arrow` + label | `PURPLE` |

**Section B — Fusion failure without localization**

| ID | Object | Manim Class | Style |
|---|---|---|---|
| FL01 | Top-down intersection view (mini, center) | `VGroup` | Same style as DC02 |
| FL02 | Infrastructure node (fixed) | `Square` diamond | `INFRA_ORANGE` |
| FL03 | Vehicle agent | `VGroup` car | `BLUE` |
| FL04 | Shared pedestrian (ground truth) | `Dot` | `GREEN`, 0.15u |
| FL05 | INF observation of pedestrian | `Dot` | `INFRA_ORANGE`, dashed circle around it |
| FL06 | CAV observation of pedestrian | `Dot` | `BLUE`, dashed circle |
| FL07 | "Same object?" label with ✗ | `Text` | `RED_MUTED`, size 18 |
| FL08 | Two perceived objects (post-fusion without calib) | `Dot` x2 | `RED_MUTED`, slightly offset from FL04 |
| FL09 | "Ghost duplication" label | `Text` | `RED_MUTED`, size 15, italic |
| FL10 | "Worse than single-agent" warning box | `RoundedRectangle` | Fill `#2A1A1A`, stroke `RED_MUTED` |
| FL11 | Warning text | `Text` | `RED_MUTED`, size 16 |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(ML01, ML02)` | 0.4s |
| 2 | 0.4s | `GrowArrow(ML03)` + label | 0.4s |
| 3 | 0.8s | `GrowArrow(ML04)` + label | 0.4s |
| 4 | 1.2s | `GrowArrow(ML05)` + label | 0.4s |
| 5 | 2.5s | HD Map diagram shrinks, `FadeIn(FL01–FL06)` | 0.6s |
| 6 | 3.2s | `FadeIn(FL07)` — "Same object?" | 0.4s |
| 7 | 4s | `FadeIn(FL08, FL09)` — ghost duplication | 0.5s, FL08 dots pop in at wrong positions |
| 8 | 5s | `FadeIn(FL10, FL11)` — warning box | 0.5s |
| 9 | 6s | Warning box pulses once | 0.3s |
| 10 | 7s | `FadeIn(PI)` with question bubble | 0.4s |
| 11 | 8s | `[HOLD]` | 1s |

---

## SCENE 3-08 — Multi-Rate Kalman Filter

> **Duration:** ~55s

### [NARRATION]

```
[NARRATOR]

"The solution is a multi-rate error-state Kalman Filter.

Three sensor streams, each running
at a different frequency.

GNSS provides absolute position —
you know where you are on Earth.
But it only updates at 5 Hz,
and it's blocked by tall buildings.

IMU and wheel speed sensors provide
high-frequency updates at 100 Hz —
every 10 milliseconds.
But they accumulate drift over time.
They're fast, but they wander.

LiDAR map-matching compares the current scan
against a pre-built HD map to correct pose.
Very accurate, but computationally expensive —
only runs at 1 Hz.

The Kalman Filter fuses all three.
It handles the measurement delays from time synchronization.
It corrects for drift using the slower but more accurate sources.
The output: continuous pose at 100 Hz —
fast enough for real-time driving,
accurate to lane level."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| KF01 | Background | `Rectangle` | Fill `#0A0A0A` |
| KF02 | Funnel / pipeline shape (center) | `VGroup` converging to one output | Three input lanes merging into one output |
| KF03 | Input lane 1 — "GNSS" | `Arrow` | `SENSOR_CYAN`, labeled |
| KF04 | Input lane 2 — "IMU / Wheel Speed" | `Arrow` | `GOLD`, labeled |
| KF05 | Input lane 3 — "LiDAR Map-Matching" | `Arrow` | `PURPLE`, labeled |
| KF06 | Frequency badge on KF03 | `RoundedRectangle` | Fill `SENSOR_CYAN`, text `NAVY` — "5 Hz" |
| KF07 | Frequency badge on KF04 | `RoundedRectangle` | Fill `GOLD`, text `NAVY` — "100 Hz" |
| KF08 | Frequency badge on KF05 | `RoundedRectangle` | Fill `PURPLE`, text `WHITE` — "1 Hz" |
| KF09 | Limitation note on KF03 | `Text` | `WHITE`, size 13, italic — "blocked by buildings" |
| KF10 | Limitation note on KF04 | `Text` | `WHITE`, size 13, italic — "drifts over time" |
| KF11 | Limitation note on KF05 | `Text` | `WHITE`, size 13, italic — "heavy compute" |
| KF12 | "Multi-Rate Error-State Kalman Filter" box | `RoundedRectangle` | Fill `#1E3A5F`, stroke `BLUE`, center-bottom |
| KF13 | Output arrow from KF12 | `Arrow` | `GREEN` |
| KF14 | Output label "100 Hz — Lane-Level Accuracy" | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN` |
| KF15 | Animated flow dots | `Dot` x3, one per lane | Each dot color matches lane, travels down lane into KF12 |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(KF01)` | 0.3s |
| 2 | 0.3s | `GrowArrow(KF03)` + `FadeIn(KF06, KF09)` — GNSS lane | 0.5s |
| 3 | 0.8s | `GrowArrow(KF04)` + `FadeIn(KF07, KF10)` — IMU lane | 0.5s |
| 4 | 1.3s | `GrowArrow(KF05)` + `FadeIn(KF08, KF11)` — LiDAR lane | 0.5s |
| 5 | 2.2s | `FadeIn(KF12)` — Kalman Filter box | 0.5s |
| 6 | 2.7s | KF15 flow dots travel down their lanes into KF12 | 1.5s, looping 2× with `Succession` |
| 7 | 4.5s | `GrowArrow(KF13)` + `FadeIn(KF14)` — output | 0.5s |
| 8 | 5.5s | `[HOLD]` | 1.5s |

### [NOTES]
- KF02 "funnel shape": construct as a `VGroup` of `Line` objects that converge — three lines from top-left, top-center, top-right meeting at a single point above KF12. Simple and clear.
- KF15 flow animation: use `MoveAlongPath` with the corresponding arrow as the path. Stagger the three dots by 0.3s so they don't all arrive at once.

---

## SCENE 3-09 — Late Fusion: CooperFuse

> **Duration:** ~55s

### [NARRATION]

```
[NARRATOR]

"Now the fusion systems themselves —
first starting with late fusion.

CooperFuse is the first real-time cooperative
late fusion system for V2X,
presented at IV 2024.

Late fusion means:
each agent runs detection independently,
generates bounding boxes,
and then shares those boxes with other agents.
Lightweight. Bandwidth-friendly.
No raw data or intermediate features need to be transmitted.

But fusing bounding boxes from multiple agents
has a specific technical problem.

The traditional approach is NMS —
Non-Maximum Suppression.
You receive multiple bounding boxes
for the same object.
NMS picks the one with the highest confidence score.

The problem: confidence score only says
'how sure am I that there's an object here?'
It says nothing about the physical quality
of that bounding box —
its position, its orientation, its scale.

An infrastructure node at an elevated vantage point
might have lower confidence
but a more accurate orientation angle
because it sees the vehicle from above
rather than from the side.

NMS throws that away.

CooperFuse's insight:
instead of fusing by confidence score,
fuse using the temporal bounding box features —
position, heading, and size over multiple frames.
This captures the physical quality of each detection,
not just the detector's confidence."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| CF01 | Background | `Rectangle` | Fill `#0F172A` |
| CF02 | "Late Fusion" flow diagram (left side) | `VGroup` | Agent 1 → detect → bbox; Agent 2 → detect → bbox; both → fuse → output |
| CF03 | Agent 1 pipeline | `RoundedRectangle` chain | Compact, horizontal |
| CF04 | Agent 2 pipeline | Same | |
| CF05 | "Bounding Boxes" shared zone | `RoundedRectangle` | Fill `#1E3A5F`, dashed border |
| CF06 | NMS comparison (right side, top) | `VGroup` | |
| CF07 | Two overlapping bounding boxes | `Rectangle` x2 | `BLUE` and `INFRA_ORANGE`, overlapping |
| CF08 | Confidence score labels | `Text` x2 | "0.91" `BLUE`, "0.74" `INFRA_ORANGE` |
| CF09 | NMS result: picks blue box | `Rectangle` | `BLUE`, green checkmark |
| CF10 | ✗ Label "Ignores orientation quality" | `Text` | `RED_MUTED`, size 14 |
| CF11 | CooperFuse comparison (right side, bottom) | `VGroup` | |
| CF12 | Same two boxes as CF07 | `Rectangle` x2 | Same colors |
| CF13 | Temporal feature bars (position, heading, size) | `Rectangle` x3 per box | Tiny bar charts below each box |
| CF14 | Fusion result: weighted blend | `Rectangle` | `GREEN`, better orientation angle than CF09 |
| CF15 | ✓ Label "Physical quality captured" | `Text` | `GREEN`, size 14 |
| CF16 | "CooperFuse — IV 2024" badge | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN` |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(CF01, CF02, CF03, CF04)` — pipeline | 0.6s |
| 2 | 0.6s | `FadeIn(CF05)` — shared bbox zone | 0.4s |
| 3 | 1.5s | `[HOLD]` — let the pipeline register | 0.5s |
| 4 | 2s | `FadeIn(CF06, CF07, CF08)` — two overlapping boxes | 0.5s |
| 5 | 2.5s | `FadeIn(CF09)` — NMS picks blue | 0.4s, blue box scales slightly |
| 6 | 3s | `Write(CF10)` — ✗ label | 0.4s |
| 7 | 4s | `FadeIn(CF11, CF12, CF13)` — CooperFuse version | 0.6s |
| 8 | 4.8s | `FadeIn(CF14)` — better fusion result | 0.4s |
| 9 | 5.3s | `Write(CF15)` — ✓ label | 0.3s |
| 10 | 6s | `FadeIn(CF16)` — paper badge | 0.3s |
| 11 | 7s | `[HOLD]` | 1.5s |

### [NOTES]
- CF07 two overlapping bounding boxes: one should be clearly rotated (incorrect heading), the other at the correct angle. The rotation difference is the visual crux of the NMS-vs-CooperFuse comparison.
- CF13 bar charts: three tiny `Rectangle` objects below each bounding box, labeled "pos", "hdg", "size". Heights differ to show different quality per agent.

---

## SCENE 3-10 — Intermediate Fusion: V2X-ReaLO

> **Duration:** ~50s

### [NARRATION]

```
[NARRATOR]

"If late fusion trades accuracy for low bandwidth,
intermediate fusion goes the other direction —
share richer BEV features
to preserve more information,
but control latency tightly.

V2X-ReaLO is the first online intermediate fusion
system for V2X in the real world,
submitted to T-PAMI.

BEV — Bird's Eye View — is a top-down feature map.
Each cell in that map encodes information
about its position:
static elements like roads and sidewalks,
dynamic elements like vehicles and pedestrians —
all in one shared representation.

This is what gets compressed and transmitted.

The trade-off is direct:
larger message size → higher accuracy, higher latency.
Smaller message size → lower latency, less information.

And in V2X, latency is the hard constraint.
A moving vehicle cannot wait.

The team found the working point:
0.5 megabytes per message.
That's a 32× compression of the raw BEV feature.
Enough accuracy retained.
Fits inside real-world V2X bandwidth."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| RL01 | Background | `Rectangle` | Fill `#0A0A0A` |
| RL02 | "BEV Feature" visualization | `Grid` | 8×8 cells, each colored by feature type — `ROAD_GRAY` for static, `BLUE`/`GREEN` for dynamic |
| RL03 | BEV label | `Text` | `WHITE`, size 16 |
| RL04 | BEV size label "32× uncompressed" | `Text` | `RED_MUTED`, size 14 — shown before compression |
| RL05 | Compression animation | `RL02.animate.scale(1/4)` direction | BEV grid shrinks |
| RL06 | Compressed BEV label "0.5 MB" | `Text` | `GREEN`, size 18, bold |
| RL07 | Trade-off scale diagram | `VGroup` | Classic balance scale |
| RL08 | Left weight "Accuracy" | `Circle` + label | `BLUE`, heavier |
| RL09 | Right weight "Latency" | `Circle` + label | `RED_MUTED`, heavier on other side |
| RL10 | Scale in balance | — | After working point: scale levels |
| RL11 | Working point marker "0.5 MB" | `Dot` + label | `GOLD`, on scale bar |
| RL12 | "V2X-ReaLO — T-PAMI" badge | `RoundedRectangle` | Fill `#1B4332`, stroke `GREEN` |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(RL01, RL02, RL03, RL04)` — BEV full size | 0.6s |
| 2 | 1s | `RL02.animate.scale(0.25)` — BEV compresses | 0.8s |
| 3 | 1.8s | `FadeOut(RL04)`, `Write(RL06)` — "0.5 MB" | 0.4s |
| 4 | 2.8s | `FadeIn(RL07, RL08, RL09)` — unbalanced scale | 0.5s, scale tips toward Latency |
| 5 | 3.5s | Scale tips toward Accuracy | 0.4s |
| 6 | 4.2s | `FadeIn(RL11)` — working point appears on scale | 0.3s |
| 7 | 4.5s | Scale levels: `RL10` — both sides balanced | 0.5s |
| 8 | 5.5s | `FadeIn(RL12)` — paper badge | 0.3s |
| 9 | 6.5s | `[HOLD]` | 1.5s |

### [NOTES]
- RL07 balance scale: build as a `VGroup` of: a center post (`Line`), a horizontal beam (`Line`), and two hanging "pans" (`Arc` or `RoundedRectangle`). Animate beam rotation with `.animate.rotate(angle)` to show it tipping side to side before settling.

---

## SCENE 3-11 — Digital Twin: OpenCDA-ROS

> **Duration:** ~50s

### [NARRATION]

```
[NARRATOR]

"The final piece — closing the loop
between simulation and reality.

The fundamental problem it solves:
the code that runs on a real vehicle
should also run, unchanged, in simulation.

OpenCDA-ROS is the bridge.

ROS — Robot Operating System —
is the standard middleware in robotics.
It handles communication between
different software modules running on different hardware.

OpenCDA-ROS connects a simulation environment —
specifically CARLA — to real-world data flow through ROS.
It handles V2X communication modules,
multi-agent time synchronization,
and sensor data streaming.

The result: write code once, run it anywhere.
Real vehicle, or simulated vehicle —
the same stack, no rewrites."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| OR01 | Background | `Rectangle` | Fill `#0F172A` |
| OR02 | Left panel "Real World" | `RoundedRectangle` | Fill `#1A1A1A`, stroke `GREEN`, 4.5u×5u |
| OR03 | Real world contents | `VGroup` | CAV icon + INF node icon + sensor icons |
| OR04 | Real world label | `Text` | `GREEN`, size 16 |
| OR05 | Right panel "Simulation (CARLA)" | `RoundedRectangle` | Fill `#1A2A3A`, stroke `BLUE`, 4.5u×5u |
| OR06 | Simulation contents | `VGroup` | Stylized CARLA scene: grid roads, colored blocks for buildings |
| OR07 | Simulation label | `Text` | `BLUE`, size 16 |
| OR08 | Center bridge "OpenCDA-ROS" | `RoundedRectangle` | Fill `#1B4332`, stroke `GOLD`, 2u×5u, center |
| OR09 | Bridge label | `Text` | `GOLD`, size 18, bold, vertical or horizontal |
| OR10 | Data flow arrows (real → bridge → sim) | `Arrow` x4 | `WHITE`, bidirectional (both panels ↔ bridge) |
| OR11 | Module labels inside bridge | `Text` x3 | Size 13, `LIGHT_BLUE` — "V2X Comm", "Time Sync", "Data Streaming" |
| OR12 | "Write once, run anywhere" tagline | `Text` | `GOLD`, size 20, italic, below the diagram |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(OR01)` | 0.3s |
| 2 | 0.3s | `FadeIn(OR02, OR03, OR04)` — real world panel | 0.5s |
| 3 | 0.8s | `FadeIn(OR05, OR06, OR07)` — sim panel | 0.5s |
| 4 | 1.8s | `FadeIn(OR08, OR09)` — bridge slides in from bottom | 0.6s |
| 5 | 2.4s | `FadeIn(OR11)` — module labels | 0.4s, staggered |
| 6 | 3s | `GrowArrow(OR10)` x4 — bidirectional arrows | 0.3s each |
| 7 | 4.5s | `Write(OR12)` — tagline | 0.5s |
| 8 | 5.5s | `[HOLD]` | 1.5s |

---

## SCENE 3-12 — Digital Twin: CDA-SimBoost & Why Simulation Matters

> **Duration:** ~55s

### [NARRATION]

```
[NARRATOR]

"CDA-SimBoost completes the full loop.

Step 1: import real-world sensor data through ROS.
Step 2: build a digital twin of that environment in CARLA —
a precise replica of the intersection.
Step 3: generate challenging scenarios
from the digital twin.
Step 4: train and benchmark models in simulation.
Step 5: validate on real hardware.

The design is modular —
any component can be swapped independently.

Now — why generate scenarios
instead of just replaying real data?

Because real data is mostly boring.
Clear weather. Smooth traffic flow.
Nobody cutting across lanes.

A model trained only on real data
never encounters the situations that actually cause accidents:
limited visibility in heavy rain,
a pedestrian stepping out from behind a parked truck,
partial sensor failure.

Digital twin lets you manufacture those edge cases —
in controlled conditions, at whatever volume you need,
with perfect ground truth labels.

That's why simulation is not a substitute for reality.
It's a complement — generating the parts
that reality can't give you enough of."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| SB01 | Background | `Rectangle` | Fill `#0A0A0A` |
| SB02 | 5-step loop diagram | `VGroup` of 5 nodes in a circle + connecting arrows | Circular layout, each step a `RoundedRectangle` |
| SB03 | Step 1 "Import Real Data (ROS)" | `RoundedRectangle` | Fill `#1E3A5F`, stroke `BLUE` |
| SB04 | Step 2 "Build Digital Twin (CARLA)" | Same | |
| SB05 | Step 3 "Generate Scenarios" | Same | |
| SB06 | Step 4 "Train & Benchmark" | Same | |
| SB07 | Step 5 "Validate on Real HW" | Same | |
| SB08 | Arrows between steps | `Arrow` x5 | `BLUE`, follow circle |
| SB09 | Edge case examples panel (right) | `VGroup` | Three small scenario illustrations |
| SB10 | Scenario 1: rain + limited visibility | `Rectangle` | Fill `#1A1A2A`, rain dots overlaid |
| SB11 | Scenario 2: sudden pedestrian | `Rectangle` | Fill `#1A1A2A`, pedestrian icon mid-road |
| SB12 | Scenario 3: partial sensor failure | `Rectangle` | Fill `#1A1A2A`, one sensor icon with ✗ |
| SB13 | "Real data: mostly normal" vs "Simulation: edge cases" comparison | Two-column `VGroup` | Left normal, right edge cases |
| SB14 | Distribution curve (as in Scene 1-04) | `ParametricFunction` | `BLUE` with `GREEN` tail — sim generates the tail |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(SB01)` | 0.3s |
| 2 | 0.3s | Loop steps appear one by one: `FadeIn(SB03)` → arrow → `FadeIn(SB04)` → ... | 0.4s per step + 0.2s per arrow |
| 3 | 3s | All steps visible, loop arrows complete the circle | 0.4s |
| 4 | 4s | `[HOLD]` — full loop visible | 0.8s |
| 5 | 4.8s | Loop scales down to left half | 0.4s |
| 6 | 5.2s | `FadeIn(SB09–SB12)` — scenario examples | 0.5s, staggered |
| 7 | 6.5s | `FadeIn(SB14)` — distribution, sim fills the tail | 0.6s |
| 8 | 7.5s | `[HOLD]` | 1.5s |

### [NOTES]
- SB02 circular layout: 5 nodes evenly distributed around a circle of radius ~2.5u. Each node's center is at angle 90°, 162°, 234°, 306°, 18° (starting from top, going clockwise). This is the standard "process loop" visual.
- SB14 reuses the chi-square distribution concept from Scene 1-04. Mark the tail region with a `GREEN` fill labeled "Simulation generates these" — inverting the red/dangerous framing from Part 1 to show that simulation turns a weakness into a strength.

---

## SCENE 3-13 — OpenCDA-InfraX

> **Duration:** ~25s

### [NARRATION]

```
[NARRATOR]

"Finally, OpenCDA-InfraX —
a data generation platform
that ties the whole simulation layer together.

Flexible sensor configuration.
Multi-modal — camera, LiDAR, radar.
Controllable weather variation.
Vector maps for downstream task support.

Everything needed to generate training data
for any perception or prediction model
in this stack."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| IX01 | Background | `Rectangle` | Fill `#0F172A` |
| IX02 | "OpenCDA-InfraX" title | `Text` | `GOLD`, size 24, bold |
| IX03 | Feature card grid (2×2) | `RoundedRectangle` x4 | Fill `#1E3A5F`, stroke `BLUE` |
| IX04 | Card 1 "Flexible Sensor Config" | `Text` + sensor icon | `WHITE`, size 15 |
| IX05 | Card 2 "Multi-Modal" | `Text` + modal icons | `WHITE`, size 15 |
| IX06 | Card 3 "Weather Variation" | `Text` + weather icon | `WHITE`, size 15 |
| IX07 | Card 4 "Vector Maps" | `Text` + map icon | `WHITE`, size 15 |
| IX08 | Arrow → "Training Data" | `Arrow` + label | `GREEN`, below card grid |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(IX01)`, `Write(IX02)` | 0.5s |
| 2 | 0.5s | Cards appear 2×2, staggered 0.2s | 0.8s total |
| 3 | 1.4s | `FadeIn(IX04–IX07)` — card contents | 0.2s each |
| 4 | 2.5s | `GrowArrow(IX08)` | 0.4s |
| 5 | 3.5s | `[HOLD]` | 1s |

---

## SCENE 3-14 — Bridge to Part 04

> **Duration:** ~25s

### [NARRATION]

```
[NARRATOR]

"From hardware installation to real-world deployment,
we now have the complete infrastructure layer for V2X.

But three hard problems remain unsolved."

[PI mascot]

[PI]
"Annotation là cực kỳ tốn kém."
"Training framework phức tạp — khó converge."
"Deploy lên edge hardware thì compute budget rất hạn chế."

[CAR mascot]

[CAR]
"Đúng.
Data efficiency. Training efficiency. Inference efficiency.

That's what Part 4 is about."
```

### [VISUAL SPEC]

| ID | Object | Manim Class | Style |
|---|---|---|---|
| BR01 | Background | `Rectangle` | Fill `NAVY` |
| BR02 | "Infrastructure layer: complete ✓" | `Text` | `GREEN`, size 20 |
| BR03 | Three bottleneck cards | `RoundedRectangle` x3 | Fill `#2A1A1A`, stroke `RED_MUTED` |
| BR04 | Card 1 "Data Efficiency" | `Text` | `RED_MUTED`, size 18 |
| BR05 | Card 2 "Training Efficiency" | `Text` | `RED_MUTED`, size 18 |
| BR06 | Card 3 "Inference Efficiency" | `Text` | `RED_MUTED`, size 18 |
| BR07 | `PI` mascot | `SVGMobject` | Left |
| BR08 | `CAR` mascot | `SVGMobject` | Right |
| BR09 | "Part 04: Efficiency" label | `Text` | `GOLD`, size 24, bold |

### [ANIMATION]

| # | t= | Action | Duration / Notes |
|---|---|---|---|
| 1 | 0s | `FadeIn(BR01, BR02)` | 0.4s |
| 2 | 0.5s | `FadeIn(BR07)` — PI appears | 0.3s |
| 3 | 0.8s | PI speech bubble 1 "Annotation tốn kém" | 0.3s |
| 4 | 1.2s | PI speech bubble 2 "Training khó converge" | 0.3s |
| 5 | 1.6s | PI speech bubble 3 "Compute budget hạn chế" | 0.3s |
| 6 | 2.3s | `FadeIn(BR03–BR06)` — three bottleneck cards, staggered 0.2s | 0.6s total |
| 7 | 3.2s | `FadeIn(BR08)` — CAR responds | 0.3s |
| 8 | 4s | `Write(BR09)` — Part 04 reveal | 0.5s |
| 9 | 5s | `[HOLD]` | 1s |
| 10 | 6s | Transition fade to Part 04 | 0.5s |

---

## End of Session 3 (Part 03)

> **Next file:** `spec_part04.md`
> **Scenes covered:** 3-01 through 3-14
> **Total estimated duration:** ~12 min

---

*Production note: Part 03 is the most engineering-grounded section. The visual language shifts here — fewer abstract arrows, more concrete system diagrams with labeled components. Scenes 3-04 (Time Calibration), 3-07 (Localization), and 3-11 (OpenCDA-ROS) carry the most weight and should be prioritized if cuts are needed. Scene 3-08 (Kalman Filter) is technically dense — if screen real estate is tight, the funnel diagram can be simplified to just the three input arrows + filter box + output.*
