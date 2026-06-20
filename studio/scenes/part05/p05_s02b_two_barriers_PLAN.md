# Animation Plan — P05S02BTwoBarriers ("Two Barriers")

Scene: [p05_s02b_two_barriers.py](p05_s02b_two_barriers.py). Goal: rebuild the animation so each
barrier carries **~15 s of motion that *tells* the script**, not ~4 s of fade-ins. Keep on-screen
**text minimal** — let visuals do the talking. Total target ≈ **35 s** (2 s intro + 15 + 15 + ~3 s
outro).

## Script being served (struck parts allowed as *visual* fuel, not as text)
- Intro: "…blocked by **two distinct barriers**."
- **Barrier 1 — No web-scale robot behavior data.** "Behavior cloning requires large quantities of
  demonstration data in the target environment. *(Collecting it at scale requires either an enormous
  fleet of physical robots or a simulation realistic enough that sim-to-real works.)*"
- **Barrier 2 — No human modeling in context.** "Robots in shared human spaces must predict and
  respond to human behavior to be safe. A robot that cannot model pedestrian intent cannot safely
  navigate a crosswalk. *(Pedestrian behavior is highly variable, context-dependent, subtle — hard to
  capture in existing datasets.)*"

## Hard constraints
- **Text budget — that's all that may appear on screen:**
  - Title `Two Barriers`; badges `1` / `2`; the two headings (`Data bottleneck` / `No web-scale robot
    behavior data`, `Human modeling gap` / `Simulation has people, but not behavior`).
  - Barrier 1: `robot behavior?` → `0` (web query), `one robot × one environment × one task`,
    `Data arrives as a trickle.`
  - Barrier 2: `no yielding`, `straight lines · no interaction`, `Safety needs human behavior.`
  - Outro: `Physical AI needs scalable simulation and human-centric modeling.`
  - **Everything else is icons/motion** (∅ stamps, gauges, ⚠, gaze cues, prediction fans). No
    paragraphs, no sentence-long captions mid-beat.
- Design rules from CLAUDE.md hold: `BG_PAPER`, colors from `colors.py`, end on `_close()`.

## Layout / staging strategy
Keep the final **two-column "Two Barriers"** composition as the payoff, but let each barrier **own the
stage during its 15 s**:
1. **Intro (2 s):** divider + both headings fade in (the skeleton). Right column stays dim.
2. **Barrier 1 (15 s):** plays in the **left 60%** of the canvas (it may borrow center space; right
   heading stays, right body dim).
3. **Hand-off:** Barrier 1 collapses to a compact summary cluster pinned in the left column.
4. **Barrier 2 (15 s):** plays in the **right 60%**; left column is now the settled summary.
5. **Outro (3 s):** both conclusions sit in their columns; bottom rule + synthesis line.

Reuse zone constants from `layout.py`; left action centered ~`LEFT*3.4`, right ~`RIGHT*3.4`, each
allowed to expand toward center during its own 15 s.

---

## BARRIER 1 — Data bottleneck (15 s)

Through-line: **the web is a firehose of text, but robot behavior isn't on the web — it has to be
*physically* collected, one slow run at a time, so it arrives as a trickle.** (Echo the firehose of
"Trillions of tokens" from the previous scene P05S02A for contrast.)

| # | t (s) | What happens (motion-first) | On-screen text | Components |
|---|------|------------------------------|----------------|-----------|
| B1.1 | 0–3.5 | A compact **web-corpus strip** (Books / Wiki / GitHub / Video tiles, reused from P05S02A) sits top-left. A **magnifier/crawler** sweeps across it carrying a query glyph; over each tile a small **∅** stamps in red and the tile dims. End on a red **`0`** counter. → "behavior can't be scraped." | `robot behavior?` (tiny, on the crawler) → `0` | corpus tiles; `Circle`+handle magnifier; `∅` = `Cross`/slashed circle; red count |
| B1.2 | 3.5–7.5 | Cut to the **three mini-worlds** (campus / curb / crosswalk). One **robot** drives each *slowly* (deliberate `smooth`, ~0.9 s/run) leaving a short `TracedPath`; each finished run **emits one log card** that drops into a small buffer. A tiny **odometer/clock** ticks up per run to stress the slowness. `one robot × one environment × one task` fades in beneath. | `one robot × one environment × one task` | `mini_world`, `robot_marker`, `data_card`, `TracedPath`, small tick counter |
| B1.3 | 7.5–11 | The buffer docks beside a **huge archive grid** ("web-scale coverage" = ~120 empty cells). The 3 logs fill exactly **3 cells**; a **fill-gauge** crawls to ≈0 %. Optional: a faint **ghost firehose** of tokens streams in from the left edge (the web) next to the **3 lonely drips** (the robot) — flood vs. trickle, side by side. | — (gauge is visual) | archive grid (`Square` lattice), progress gauge, faded token stream (`token_packet` ghosts) |
| B1.4 | 11–13 | From the robot, **two option branches** sprout: (a) a **fleet** of many small robot icons multiplying ($$$ / a stack), (b) a **sim screen** with a jagged **sim-to-real "crack"**. Both quickly **dim / stamp hard** (a small ⚠ or grey-out). → the two costly ways to scale. | — (icons only) | cloned `robot_marker` grid; small monitor rect + zig-zag crack; ⚠ |
| B1.5 | 13–15 | The 3 drips fall and coalesce into a single small drop; **`Data arrives as a trickle.`** writes in. Cluster shrinks to the left-column summary. | `Data arrives as a trickle.` | drop shape, text write |

Net Barrier 1 text on screen at rest: heading + `one robot × one environment × one task` +
`Data arrives as a trickle.` (the `robot behavior?/0` is transient).

---

## BARRIER 2 — Human modeling gap (15 s)

Through-line: **sim has *bodies* but not *behavior* — "zombies" on rails that don't react — so a robot
trained there can't predict pedestrian intent and isn't safe at a crosswalk.** Built as a **A/B
contrast**: zombie-sim vs. real reactive humans.

| # | t (s) | What happens (motion-first) | On-screen text | Components |
|---|------|------------------------------|----------------|-----------|
| B2.1 | 0–2 | The **intersection panel** builds: roads, crosswalk stripes, 4 corner blocks; a **robot** rolls toward the crosswalk; **2–3 pedestrians** appear, each with a small **heading arrow**. | — | `city` group (existing), `robot_marker`, `person_dot` |
| B2.2 | 2–6.5 | **Zombie sim.** Pedestrians and robot move in **perfectly straight, constant-velocity rails**. A pedestrian and the robot **cross the same point and clip *through* each other** (overlap/ghost, zero reaction); a second pair does the same. A red **⚠ `no yielding`** stamps at the clip point; the straight paths render as hard **rails**. → "straight lines, no interaction." | `no yielding` | `Line` rails, `MoveAlongPath` linear, overlap (no collision), ⚠ ring |
| B2.3 | 6.5–10.5 | **Replay, real behavior.** Same setup, faded zombie rails left as ghosts. Now the pedestrian shows a **gaze/attention cue** (a small eye or attention arc toward the robot), **slows and yields**; the robot **curves** to respond. A green **✓** at the safe pass. Contrast reads instantly: **grey straight rails (sim) vs. colored reactive curves (real).** | — (✓ only) | gaze arc/eye glyph, curved `CubicBezier` paths, green check |
| B2.4 | 10.5–14 | **Why it fails.** Zoom to the robot at the crosswalk facing one pedestrian. The robot casts a **prediction fan** (`sensor_cone`) but — trained on zombie sim — predicts a **single straight arrow**. The real pedestrian **diverges** off that arrow → **near-miss** flash ⚠ on the crosswalk. → "can't model intent → unsafe crosswalk." | — | `sensor_cone`, dashed predicted arrow, divergent real path, `Flash` ⚠ |
| B2.5 | 14–15 | The pedestrian briefly **splays into a fan of several dashed futures** (varied, context-dependent — too many to script). Settle; **`Safety needs human behavior.`** writes in. | `Safety needs human behavior.` | fan of `DashedLine`s, text write |

Net Barrier 2 text on screen at rest: heading + `no yielding` (transient) + `Safety needs human
behavior.` Optionally a single faded `straight lines · no interaction` tag during B2.2.

---

## Outro (≈3 s)
Both columns settle to their conclusion lines; draw `bottom_rule`; write
`Physical AI needs scalable simulation and human-centric modeling.` (color `scalable simulation` pink,
`human-centric modeling` red). `self.wait(1.5)` → `_close()`.

## Pacing check
- Intro 2 + Barrier 1 15 + Barrier 2 15 + Outro 3 ≈ **35 s**. Each barrier's beats already sum to ~15 s
  (trim the optional flood-ghost in B1.3 or the splay in B2.5 if long).
- Per-beat run_times are mostly 0.5–1.5 s with deliberate easing; the *slowness* in B1.2 and the
  *clip-through* in B2.2 are the emotional beats — give them room, don't rush.

## What to reuse vs. build
- **Reuse (already in this file):** `mini_world`, `data_card`, `robot_marker`, `person_dot`, `city`
  group, `barrier_heading`.
- **Reuse (other modules):** `vehicle_icon`, `pedestrian_icon` (`agents.py`); `sensor_cone`,
  `radar_shells_2d` (`signals.py`); corpus tiles / `token_packet` style from `p05_s02a` (copy a
  lightweight local version, don't import across scenes).
- **Build (small new helpers):** magnifier + `∅` stamp; archive grid + fill-gauge; fleet/sim option
  icons + sim-to-real crack; pedestrian **gaze/attention** cue; **prediction fan** (cone + single
  dashed arrow); **clip-through** (two mobjects sharing a point with no avoidance).

## Mapping beats → script (coverage check)
- "can't be scraped from the web" → **B1.1**
- "demonstration data in the target environment / one robot, one env, one task" → **B1.2**
- "web-scale needed but absent" → **B1.3**
- "enormous fleet OR realistic sim (sim-to-real)" → **B1.4**
- "data is a trickle" → **B1.5**
- "sim has people, not behavior / straight lines, no interaction" → **B2.2**
- "must predict and respond to human behavior" → **B2.3**
- "can't model pedestrian intent → unsafe crosswalk" → **B2.4**
- "behavior is variable / subtle / hard to capture" → **B2.5**
- synthesis → **Outro**

## One-line summary
Give each barrier a **15 s motion story** built on one strong contrast — Barrier 1: *web firehose vs.
robot trickle* (crawler finds nothing → one slow run = one log → near-empty web-scale archive);
Barrier 2: *zombie rails vs. reactive humans* (peds clip through on straight lines → real humans
yield/gaze → robot mispredicts intent at the crosswalk). Keep text to the heading + one scarcity line +
one conclusion per side; everything else is icons and movement.
