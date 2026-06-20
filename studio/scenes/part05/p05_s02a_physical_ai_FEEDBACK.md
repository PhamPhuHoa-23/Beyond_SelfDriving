# Feedback — Physical AI (right) panel of P05S02ALLMVsRobot ("Web Data vs. Robot Experience")

Scene: [p05_s02a_llm_vs_robot.py](p05_s02a_llm_vs_robot.py). Focus: the **right / Physical AI** column
and its robot-through-waypoints sequence. Reviewed from frames t ≈ 33 / 36 / 38 / 40 / 42 / 45 / 48 s
of `videos/P05S02ALLMVsRobot.mp4` (54.5 s), with right-panel crops.

The metaphor is good (a robot must physically drive a route to *create* experience, vs. the web where
text already exists). The execution of the **waypoint sequence** is where it falls apart — exactly the
"chạy tới mấy cái mốc xong biến hoá gớm, nhiều thứ overlap" you flagged. Concretely:

---

## The "ugly morph" at each waypoint — root causes

### 1. The log card spawns **on top of the robot**, so the robot looks like it mutates into a card
At each checkpoint the code does ([lines 915–922](p05_s02a_llm_vs_robot.py#L915-L922)):

```python
log.move_to(robot.get_center() + UP * 0.25)   # right on the robot
self.play(FadeIn(log, scale=0.6), ...)         # a card materialises over it
self.play(log.animate.move_to(log_targets[idx]), ...)
```

So a `log 0x` card fades in *scaled-up from the robot's centre*, covering the robot body, the route
line, and the checkpoint (clearly visible at t≈36 — "log 02" sits squarely on the robot). That
fade-in-on-the-robot is read as the robot "biến hoá" into something. **Fix:** never spawn the card on
the robot. Grow it from the **checkpoint dot** (the thing that was just logged), offset clear of the
robot, e.g.:

```python
log.move_to(checkpoint.get_center() + UP * 0.55)   # above the waypoint, not on the robot
log.scale(0.0)
self.play(GrowFromPoint(log, checkpoint.get_center()), ...)
```

### 2. The log cards fly **outside the world panel**, into the bottom-right corner
`log_targets` are at x ≈ 5.95, y ∈ [−0.66, −1.64] ([lines 700–712](p05_s02a_llm_vs_robot.py#L700-L712)),
but the world panel's right edge is ≈ 5.9 and its bottom is ≈ −0.53 (panel centre `RIGHT*3.48+UP*0.32`,
4.84×1.7). So all three cards land **past the panel, in the empty bottom-right margin** (spanning out
to x≈6.29, almost the 6.5 safe edge). They look detached — like they're spilling off-screen — and
nothing frames them as "the robot's collected experience." **Fix:** give them a real home: a small
labeled container ("logged runs" / "experience buffer") docked in the right margin with a border, cards
stacked tidily inside it and aligned, not free-floating. Or collapse the three cards into one growing
stack with a counter (`×3`), which is calmer and still says "few, hard-won runs."

### 3. Four effects fire at once on a tiny area → noise
Per checkpoint ([lines 893–913](p05_s02a_llm_vs_robot.py#L893-L913)) you play **simultaneously**: a
`sensor_cone` (5 levels), `radar_shells_2d` (3 shells), a `ShowPassingFlash` ray, **and** a `Flash` on
the checkpoint — all on top of the robot + route + checkpoint + pedestrian, which already share that
spot. It reads as a flickery burst, not a clean "sensor ping." **Fix:** pick **one** signature beat per
waypoint — e.g. a single radar ping + the colored ray to the checkpoint — and drop the cone and/or the
8-line Flash. Calm and legible beats busy.

### 4. The robot parks on top of the checkpoint and flag at the end
The route ends at the flag (`target.move_to(route.get_end() + UP*0.25)`,
[line 354](p05_s02a_llm_vs_robot.py#L354)) and the robot drives to t=1.0
([line 927](p05_s02a_llm_vs_robot.py#L927)), so it finishes overlapping the last (amber) checkpoint and
crowding the flag (t≈40–48). **Fix:** stop the robot at ~t=0.94, or push the flag up/right so the robot
ends with clear space around it.

---

## Overcrowding — the right column is doing too much at once

By the end of the sequence the lower-right packs, in roughly the same band, all of:
`factor_chips` (1 ROBOT × 1 WORLD × 1 TASK), **3 log cards**, the `annotation_pipeline`, the
`campus_absence_card`, `expensive`, `robot_caption`, and the `data_gap_meter`. Several share the
y ∈ [−1.1, −2.5] strip in the right x-band and are introduced back-to-back, so the panel never gets to
breathe — that's the "nhiều thứ overlap, gớm òm" feeling.

- **The `annotation_pipeline` glyphs are cryptic** ([lines 510–524](p05_s02a_llm_vs_robot.py#L510-L524)).
  The three mini-icons render as `)` (an arc+dot), `∅` (a line through a circle), and `✓`. Nobody reads
  that as "record → label → verify." Either replace them with unmistakable icons + a one-word caption
  under each card, or cut the pipeline — the story (experience is expensive to create) doesn't need it.
- **Decide what this beat is actually about.** The narration is "experience must be created, one run at
  a time, expensive." That needs: the robot driving the route (creating data) + the `1 ROBOT × 1 WORLD
  × 1 TASK` scarcity chips + *one* "expensive/slow" cue. The log cards, annotation pipeline, campus
  card, and gap meter are four *additional* ideas competing for the same corner. Keep the 1–2 that land
  hardest; stage the rest as separate, fully-cleared beats or cut them.
- **Match the left's density.** The web side resolves cleanly to "ABUNDANT / Trillions of tokens." The
  right should resolve just as cleanly (e.g. "EXPENSIVE / one run at a time") instead of a pile of
  cards. Right now the two halves are visually unbalanced — left calm, right cluttered.

---

## Suggested rework of the waypoint loop (shape, not final code)
1. Robot drives segment → arrives at checkpoint.
2. **One** clean ping: radar ring + colored ray to the checkpoint (no cone, no extra Flash).
3. A log card **grows from the checkpoint** (not the robot), then docks into a **framed "experience
   buffer"** in the right margin — tidy stack, aligned, inside the safe zone.
4. After the third waypoint, robot stops short of the flag; reveal `1 ROBOT × 1 WORLD × 1 TASK` with a
   single accent flash.
5. Resolve to one strong line — "EXPENSIVE · one run at a time" — and stop. Drop or defer the
   annotation pipeline / campus card / gap meter so the ending is clean.

## What's good (keep)
- The world panel (road + curved route + colored checkpoints + flag) is a clear, attractive "go drive
  the real world" metaphor, and the pink `TracedPath` showing the robot's actual path is a nice touch.
- `1 ROBOT × 1 WORLD × 1 TASK` is a strong, instantly-readable statement of why physical data is scarce.
- The left/right "data exists vs. experience must be created" framing is excellent — the fix is making
  the right side as disciplined as the left.

## Priority
1. Stop spawning log cards on the robot — grow them from the checkpoint (Issue 1). This removes the
   "morph" outright.
2. Dock the log cards in a framed container inside the panel's margin, not the bottom-right void
   (Issue 2).
3. Reduce the per-waypoint effect stack to one clean ping (Issue 3).
4. Thin out the lower-right: cut/defer annotation pipeline + campus + gap meter; fix the cryptic glyphs
   (Overcrowding).
5. Stop the robot short of the flag (Issue 4).

## One-line summary
The right panel's idea is right but the waypoint loop is the problem: **log cards fade in on top of the
robot (the "morph"), then fly out into the empty bottom-right corner, while four sensor effects flash at
once and four more cards pile into the same band.** Grow the logs from the checkpoints into a tidy framed
buffer, cut each ping to one clean effect, and thin the lower-right to one strong "expensive" payoff —
then the right will read as cleanly as the left.
