# Feedback — "Inductive Bias for Cooperative Perception" beat in P04S04CooPReMasked

Scene: [p04_s04_coopre_masked.py](p04_s04_coopre_masked.py), section **`FRAME 1.5`**, lines **481–658**.

> **Status.** Round 1 was applied — the panels are now mirrored, labels read `EGO — OCCLUDED VIEW` /
> `CAV — COMPLEMENTARY VIEW`, masked cells carry `?`, there's a `COOPERATIVE SHARING (CAV → EGO)`
> lane, an amber reconstruction column, and a `= COOPERATIVE DETECTION` payoff. Good progress. This
> document is **Round 2**: a full review of the *revised* render, reviewed from frames at
> t ≈ 17.5 / 18.6 / 19.4 / 22 / 23.5 s of `videos/P04S04CooPReMasked.mp4` (re-rendered 12:02).

The beat still has to land one idea in a glance: **EGO has a hole → CAV sees that exact region →
CAV's data flows in and fills the hole → now EGO detects the car it couldn't see.** Below: the two
issues you flagged (with root causes), then everything else I found, then concrete fixes.

---

## The two you flagged

### A. The packets are white and invisible on the cream background — **it's a real bug, not a perception issue**

The transmission dots ([lines 593–607](p04_s04_coopre_masked.py#L593-L607)) are built as:

```python
packet = Dot(radius=0.09, color=ACCENT_AMBER)   # line 599
```

In this ManimGL build, the `color=` **constructor kwarg on `Dot` is not reliably applied** — the
dots fall back to near-white fill (you can see them as soft white blobs in the lane at t≈19.4, and
on the cream `BG_PAPER` they vanish). Proof it's the construction, not the color choice: amber is
clearly visible elsewhere (the `COOPERATIVE SHARING` label is amber and reads fine), and the
**Beat-2 packets** in the 8×8 grid render as crisp teal dots because they set color *explicitly*:

```python
# lines 448–450 — THIS pattern works
packet = Dot(radius=0.055)
packet.set_fill(ACCENT_TEAL, opacity=1.0)
packet.set_stroke(ACCENT_TEAL, width=0.8, opacity=1.0)
```

**Fix** — use the explicit pattern here too, and give the dot a darker halo so it survives on cream:

```python
packet = Dot(radius=0.09)
packet.set_fill(ACCENT_AMBER, opacity=1.0)
packet.set_stroke(GOLD_RICH, width=1.6, opacity=1.0)   # gold rim → reads on light BG
```

While you're in there: this is the **hero motion** of the whole beat, so make it unmistakable —
add a fading trail (`TracedPath` per packet, or a short comet tail), and bump the arc so the *flow*
reads, not just the endpoints. Right now even if they were amber they'd be small and quick.

### B. The dashed ghost car looks like a stray scribble before the reveal

The ghost ([lines 557–563](p04_s04_coopre_masked.py#L557-L563)) is two nested **dashed rounded
rectangles** at `set_opacity(0.45)`, dropped into `frame_bias_base` and faded in at the very start
([line 576](p04_s04_coopre_masked.py#L576)). So from second 0 of the beat there's a dashed double-box
sitting in the occluded column, *on top of* the `?` glyphs and the grey shadow. At scale 0.35 it
doesn't read as a vehicle — it reads as a dashed smudge / leftover guide, exactly the "kì" (off)
look you noticed. Three things are stacked in that one column: grey masked cells + `?` + shadow +
ghost. It's overcrowded and the ghost is the weakest of the four.

**Fix — pick one of:**
- **(recommended) Don't show the ghost during setup at all.** During the occluded beat the column is
  simply unknown (`?`). Only *after* the packets land does the object resolve: cross-fade the `?`
  column → amber fill → the detected car appears. The "unknown becomes known" story is cleaner with
  nothing-then-something than with a permanent ghost.
- **Or** keep a hint, but make it unambiguous and quiet: a single faint **solid** car silhouette
  (not dashed, `opacity≈0.25`, INK_LIGHT) *with no `?` overlapping it* — move the `?` glyphs to the
  empty masked cells and reserve the object's cell for the silhouette. And build it from
  `vehicle_icon(...)` so it's clearly a car, not a generic dashed box.

---

## Everything else (Round 2)

### 1. **Conceptual bug: CAV has the same occluding building, so it doesn't look "complementary."**
`building_cav` ([lines 551–554](p04_s04_coopre_masked.py#L551-L554)) mirrors `building_ego` — an
identical dark block over CAV's grid. But CAV is the panel that's supposed to **see what EGO can't**.
Putting the same occluder on both panels makes them look *equally blocked*, which contradicts the
whole message. CAV's inner column should read as **clear / fully sensed** (it already gets the darker
teal highlight — good), with **no building over it**. Either drop `building_cav`, or place CAV's
building somewhere that *doesn't* occlude the shared column — so the viewer sees: same region, EGO
blocked, CAV clear.

### 2. **The EGO building occludes the wrong cells.**
`building_ego` is at `LEFT*3.0` ([line 545](p04_s04_coopre_masked.py#L545)) ≈ grid **column 2**, but
the masked/amber column is **column 4** (`idx 3,7,11,15`), and `shadow_ego` is at `LEFT*2.36`
([line 549](p04_s04_coopre_masked.py#L549)) = column 4. So the building sits two columns to the left
of the shadow it supposedly casts — they're disconnected, and the building covers cells that are
*not* the masked ones. Visually it reads as **two separate dark problems** (a black blob mid-grid +
a masked column on the right). Move the building to the **inner edge**, immediately adjacent to the
masked column, so building → shadow → masked column is one continuous cause-and-effect.

### 3. **The building sits *on* the voxel grid, breaking the BEV metaphor.**
A solid dark rounded-rect overlapping cells reads as "deleted voxels," not "a building in the scene."
If the grid is a BEV occupancy map, an occluder should be either a clearly-iconified object resting
*above* the plane, or rendered as dark *footprint cells* — not a floating block that erases the grid.
Right now (t≈22) the EGO grid shows blue cells + a black block + an orange column + a red box: four
strong values fighting in one small panel.

### 4. **The amber reconstruction column is heavy and pre-baked-looking.**
`set_fill(ACCENT_AMBER, opacity=0.70)` ([lines 617–620](p04_s04_coopre_masked.py#L617-L620)) on a
full column lands as a saturated orange bar that competes with the building and box. Two
improvements: (a) lower it to ~0.5 or use `PASTEL_AMBER` fill + `ACCENT_AMBER` stroke so it's clearly
"filled" without shouting; (b) animate it **cell-by-cell synced to packet arrival** (each packet that
lands flips one cell to amber) so it reads as *reconstructed by the incoming data*, not as an orange
column that was always there.

### 5. **`= COOPERATIVE DETECTION` tag is tiny and cramped.**
`size=8`, `next_to(card_ego, DOWN, 0.12)` ([lines 630–631](p04_s04_coopre_masked.py#L630-L631)) — it
collides with the card's bottom edge and the caption band, and is barely legible (see t≈23.5). Bump
to `SIZE_CAPS`, center it under the EGO panel with more buffer, and consider a thin connector from
the box to the tag so the equation (box = cooperative detection) reads.

### 6. **Lane label + lane bar are under-powered.**
`lbl_lane` is `size=8` ([line 504](p04_s04_coopre_masked.py#L504)) and the lane fill is `opacity=0.1`
([lines 500–503](p04_s04_coopre_masked.py#L500-L503)) — both nearly disappear. This lane is the
"pipe" the cooperation flows through; make the label `SIZE_CAPS` and add a faint directional cue in
the lane (a few `→` chevrons, or a subtle gradient) so direction reads *before* the packets fly.

### 7. **CAV panel has a redundant second car.**
`cav_car` (rotated, bottom — [lines 537–539](p04_s04_coopre_masked.py#L537-L539)) plus `target_cav`
in the complementary column ([lines 565–567](p04_s04_coopre_masked.py#L565-L567)) gives CAV two teal
cars with unclear distinct roles. Mirror EGO's structure instead: **one observer car + one target
object** per panel. The target object on CAV (solid teal) is the same physical car that's a ghost on
EGO — make that pairing explicit (same shape/size, mirrored position) so "CAV sees the car EGO can't"
is obvious.

### 8. **Radar waves add noise, not signal.**
`waves_ego` / `waves_cav` ([lines 580–582](p04_s04_coopre_masked.py#L580-L582)) are faint expanding
rings that, at this scale and against everything else, mostly read as low-contrast clutter and don't
advance the idea. Either drop them, or repurpose them as a single clean "sensing" pulse on the
*observer* cars only.

### 9. **Value/colour overload + leftover empty space.**
The EGO panel carries blue, near-black, orange, red, grey across a small area while the cards still
have empty bands top and bottom. Net it out: fewer hues (let amber = the one payoff colour),
slightly larger grids to use the vertical space, and the occluder reduced to a quiet footprint so
the **amber fill + detection box** are the only things that pop.

---

## Suggested order of operations
1. **Packets → explicit `set_fill`/`set_stroke` + gold rim + trail** (Fix A) — biggest single win,
   makes the hero motion visible.
2. **Drop/relocate `building_cav`** so CAV reads as complementary (Issue 1) — fixes the core message.
3. **Re-anchor `building_ego` to the inner edge** next to its shadow + masked column (Issue 2).
4. **Remove the setup ghost; resolve the car only on reconstruction** (Fix B / Issue 7).
5. **Animate the amber fill cell-by-cell with packet arrival** (Issue 4).
6. Polish: lane label + detection tag sizes (Issues 5–6), trim the second CAV car and radar waves
   (Issues 7–8), reduce the colour count (Issue 9).

---

## Round 3 — "what is that thing in the middle?" (the transmission lane)

Reviewed from the t≈18 s frame (pre-packets). The thing in the centre is `lane_bg` +
`lane_arrows` ([lines 499–513](p04_s04_coopre_masked.py#L499-L513)) — a faint grey band with three
small `←` glyphs. It reads as weird/unfinished, for concrete reasons:

1. **It's a big empty grey bar with almost nothing in it.** Before the packets fly (which is most of
   the beat) the lane is just a 4.8-wide grey rectangle holding three tiny arrows. With no content,
   it looks like a placeholder / a UI element that failed to load — not a deliberate part of the
   diagram.

2. **The arrows contradict the label sitting right above them.** The label says
   `COOPERATIVE SHARING (CAV ➔ EGO)` — a **right**-pointing `➔` — and 0.1 units below it the lane
   shows three **left**-pointing `←`. Both are technically correct (the label's arrow is a "from→to"
   separator; the lane arrows point right-to-left because CAV is on the right). But stacking a `➔`
   directly over a `←` is visually self-contradictory and is the main "kì" trigger: the eye sees two
   opposite arrows and can't tell which way anything goes.

3. **They're text glyphs, not flow chevrons.** `text_label("←", size=14)` at `opacity=0.35` renders
   as three thin, faded serif characters floating far apart (1.5 units each). They don't tile into a
   continuous "flow," don't touch anything, and look like stray typed characters rather than a
   directional channel.

### Fix — pick one

- **(recommended) Delete the static lane and arrows entirely; let motion carry direction.** Once the
  packets are visible (Round 2, Fix A) and have a trail, the *movement* of amber dots from CAV to
  EGO shows the direction far better than static chevrons ever will. Keep just the
  `COOPERATIVE SHARING` label above the gap (drop its `➔` too, or keep only that one arrow). Removes
  the empty grey bar and the contradiction in one move.

- **Or, keep a channel but make it a real directed one.** Replace the three text `←` with actual
  geometry — a row of evenly tiled `Triangle`/`ArrowTip` chevrons all pointing toward EGO, full
  opacity, touching edge-to-edge so they read as one arrow lane — and **remove the `➔` from the
  label** so only one direction is on screen. Optionally animate the chevrons sliding toward EGO so
  the lane itself flows. (Still more work than Option A for the same payoff.)

Either way: **don't have two opposite-pointing arrows on screen at once.** That's the core of why the
middle looks off.

## Round 3b — "why does box 2 (CAV) have two cars?"

They're two *different roles*, but nothing on screen tells you that, so it reads as a duplicate:

- The car **outside the grid on the right** is `cav_car`
  ([lines 539–541](p04_s04_coopre_masked.py#L539-L541)) — the **CAV sensor vehicle** (the agent
  doing the sensing), at `RIGHT*5.0`, rotated `PI` to face its own grid.
- The car **inside the grid, in the left/complementary column** is `target_cav`
  ([lines 548–549](p04_s04_coopre_masked.py#L548-L549)) — the **object being detected**: the same
  physical car that EGO can't see but CAV can.

Why it looks weird:

1. **Both are the same teal, similar size, unlabeled.** Agent and target are rendered identically,
   so the eye sees "two of the same car" instead of "a sensor + the thing it senses."
2. **The panels aren't symmetric, so the count jumps out.** During setup the EGO panel shows **one**
   car (`ego_car`, the observer) — the target ghost was removed — while CAV shows **two**. The mirror
   the layout promises is broken: EGO = 1 car, CAV = 2.
3. **The same object changes colour.** `target_cav` is teal, but when EGO finally detects it the new
   `detected_car` is **blue** (`ACCENT_BLUE`). One physical car shouldn't be two colours — it breaks
   the "this is the *same* car CAV saw and EGO recovered" link.

The underlying idea is actually right (CAV sees the car from the start; EGO only after cooperation),
it's just illegible. **Fix:**

- **Give the target its own identity, distinct from the agents.** The agents are blue (EGO) / teal
  (CAV); make the *target* a neutral third colour (e.g. `INK_MID`/grey) so "two teal cars" becomes
  "the teal CAV + the grey car it detected." Use that same target colour on both sides.
- **Restore symmetry: put the target on EGO too.** Show the same car as a faint grey **silhouette**
  in EGO's masked `?` column (EGO suspects it but can't confirm), mirroring the solid grey target in
  CAV's column. Now each panel has *observer + target*, the 2-vs-1 imbalance disappears, and when the
  packets land the EGO silhouette resolves into the detected car — the payoff finally pays off.
- **Keep one identity colour for that car** through ghost → detected, so the viewer tracks it as one
  object across both panels.

(This supersedes Round 2, Issue 7 — same topic, with the exact roles identified.)

## Round 3c — the `COOPERATIVE SHARING` label got shoved up to the header row

**Why it moved.** `lbl_lane.move_to(UP * 1.1)` ([lines 500–501](p04_s04_coopre_masked.py#L500-L501))
puts the label at exactly the same height as the two card titles (`lbl_card_ego` / `lbl_card_cav`,
both at `UP * 1.1`). The code comment even says "aligned with card headers" — but that's the
problem, not the goal. At header height the usable gap is narrow and the right card's title
(`CAV — COMPLEMENTARY VIEW`) starts right there, so the amber label collides with it and looks
cramped/floating at the top.

**It's also semantically in the wrong place.** The label describes the *cross-panel transfer*, which
happens at **grid mid-height** (the packets fly through the middle of the gap, y ≈ −0.4). Parking the
label up at y = 1.1 divorces it from the thing it names.

**Fix — drop it into the centre of the gap, at the transmission line:**

```python
lbl_lane = text_label("COOPERATIVE SHARING", size=SIZE_CAPS - 4, color=ACCENT_AMBER, weight=BOLD)
lbl_lane.move_to(ORIGIN + DOWN * 0.4)        # x=0 (gap centre), y=-0.4 (grid mid-line)
```

Geometry check: the grids' inner edges are at x ≈ ±2.44 (grid centres ±3.4, half-width 0.96), so the
gap between them is ~4.9 wide — plenty of room for a centred label. The target cars sit at x ≈ ±2.68
and the packets **arc upward** (peak ≈ +1.0), so a label at y = −0.4 sits cleanly *below* the arcs and
*between* the grids — it reads as the channel label, exactly where the sharing happens.

Two refinements:
- **Shorten to `COOPERATIVE SHARING`** (drop the `(CAV TO EGO)`). Direction is already carried by the
  moving amber packets (Round 3 logic); the parenthetical only adds width that risks touching the
  grids. If you want the direction in text, keep it but stack it on a second line so it stays narrow.
- If mid-gap feels too "buried," the next-best spot is **just above the grids but below the card
  titles** — `move_to(UP * 0.78)` — centred at x=0. Still clear of the `UP*1.1` header row and clear
  of the grid tops (≈ +0.56). Either works; mid-line is the cleaner of the two.

Whatever you pick: **don't share the y of the card headers** — that's what makes it look shoved up
and cramped.

## One-line summary
The redesign's bones are right (mirrored panels, lane, payoff), but the **hero transmission renders
white/invisible** (a `Dot(color=…)` bug — use explicit `set_fill`/`set_stroke` like Beat 2), the
**setup ghost looks like a stray dashed smudge**, and the **occluding building is mirrored onto CAV
and detached from the column it occludes**, which quietly breaks the "EGO blocked / CAV complementary"
story. Fix those three and tidy the value/label sizes, and the beat will read as a deliberate
diagram.
