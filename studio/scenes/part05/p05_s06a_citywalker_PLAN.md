# Animation Plan — P05S06ACityWalker ("CityWalker Dataset")

Scene: [p05_s06a_citywalker.py](p05_s06a_citywalker.py). Goal: grow from the current ~6 s of fade-ins
to **~20 s** that tells the whole script, and lift the visual to professional polish. Keep on-screen
**text minimal**.

## Script being served
> "The simulation bottleneck is resolved. **Now for the human modeling problem.** Existing human
> motion datasets record human movement **in isolation**. Motion from these datasets **walks through
> walls, ignores obstacles, and produces spatially incoherent trajectories.** **CityWalker** is the
> first dataset designed to capture pedestrian behavior **in the context of real urban environments**:
> 30.8 h egocentric video, 120,914 pedestrians, 16,215 scene segments, 227 cities. The diversity
> captures **pushing strollers, looking at phones, stopping for photos, gesturing to companions** — the
> full spectrum of real urban pedestrian behavior. CityWalker is the **training signal**… the model
> that learns from it is **PedGen**."

Five ideas: **(a)** pivot from sim → human-modeling problem; **(b)** the *problem* — isolated mocap
walks through walls / ignores obstacles; **(c)** CityWalker fixes it — behavior *in context*; **(d)**
the *diversity* of behaviors; **(e)** the *scale* (the stats) and the bridge to **PedGen**.

## Current problems
- **~6 s total**, all single fades; no room to breathe, far short of 20 s.
- **The script's opening contrast is missing entirely.** The scene never shows "isolated mocap walks
  through walls / ignores obstacles" — which is the whole *reason* CityWalker matters. The current
  bottom caption ("not motion-capture in isolation…") *states* it in a long sentence instead of
  *showing* it.
- **Trajectories are a tangle** of 4 colored Béziers crossing the crosswalk with floating tags; the
  "diversity" (strollers, phones, photos) is reduced to 3 text tags, not shown.
- **Stats are static fade-ins** — no count-up, no weight for "120,914 / 227 cities worldwide."
- **No bridge** to PedGen (the next scene), which the script explicitly sets up.

---

## 20 s storyboard

Layout keeps **city panel (left) + metric stack (right)**; the problem beat reuses the same panel so
the *isolated-vs-context* contrast happens in one place.

| # | t (s) | What happens (motion-first) | On-screen text | Components |
|---|------|------------------------------|----------------|-----------|
| 0 | 0–1.5 | **Pivot.** A small "sim solved ✓" token (carryover from MetaUrban) slides off; a **human figure with a `?`** slides in — "now the human problem." | — | icon swap, `pedestrian_icon` |
| 1 | 1.5–5.5 | **The problem: isolated mocap.** A figure walks on a **blank void / mocap stage** (dark tile, skeleton dots, no environment). That isolated path is then **dropped into the city** where it goes **straight through a building**, **across the road ignoring the crosswalk**, and **clips an obstacle** — red **⚠** flashes at each violation; the trajectory renders as a hard, scene-blind straight line. → "walks through walls, ignores obstacles, incoherent." | — (⚠ only) | void tile, straight `Line` path, `Flash` ⚠ at wall/obstacle |
| 2 | 5.5–8.5 | **CityWalker reveal.** Wipe the bad path. Panel caption `real pedestrian trajectories in context` writes in. The **same scene** now grows **context-aware** trajectories (`TracedPath`) that **follow sidewalks, use the crosswalk, curve around obstacles**. The contrast with Beat 1 is the payoff. | `real pedestrian trajectories in context` | `city_view` panel, `CubicBezier` paths that respect geometry, `TracedPath` |
| 3 | 8.5–12.5 | **Diversity of behaviors.** As peds move, each performs a **distinct behavior with a prop + tag**: **stroller** (cart), **phone** (head-down + phone glyph), **photo stop** (pause + camera glyph), **gesture** (two peds + speech glyph). Tags pop as each behavior happens, not all at once. | `stroller` · `phone` · `photo stop` · `gesture` | prop glyphs, `pedestrian_icon` variants, staggered tags |
| 4 | 12.5–17 | **The scale.** The four metric cards slide in and **count up** (`0 → 30.8h`, `0 → 120,914`, `0 → 16,215`, `0 → 227`), each with a tiny motif: a **play icon** (video), **multiplying dots** (pedestrians), **scene thumbnails** (scenes), a **mini-globe with scattered dots** (227 cities worldwide). | `30.8h video` · `120,914 pedestrians` · `16,215 scenes` · `227 cities` | `metric` cards + `ChangingDecimal`/count-up, mini-globe |
| 5 | 17–20 | **Bridge to PedGen.** The whole dataset **collapses into a "training signal" token**; an arrow → a model box labeled **`PedGen`** teases the next scene. Hold → `_close()`. | `training signal → PedGen` | token shrink, `Arrow`, model box |

Beats sum to ~20 s. If long, trim Beat 0 to 1 s or the globe motif in Beat 4.

## Text budget (keep light)
Scene title + `real pedestrian trajectories in context` + four behavior tags + four stat
number/labels + `training signal → PedGen`. The problem (Beat 1), the diversity props, and the
count-ups are **visual** — drop the long bottom sentence entirely; the contrast *shows* it.

## Coverage map (beat → script)
- "now for the human modeling problem" → **Beat 0**
- "record movement in isolation / walks through walls, ignores obstacles, incoherent" → **Beat 1**
- "first dataset … in the context of real urban environments" → **Beat 2**
- "strollers, phones, photos, gesturing — full spectrum" → **Beat 3**
- "30.8h, 120,914, 16,215, 227 cities worldwide" → **Beat 4**
- "training signal … the model is PedGen" → **Beat 5**

## Visual upgrades (the "make it professional" part)
1. **Add the isolated-vs-context contrast** (Beats 1–2) — the single biggest improvement; it's the
   script's thesis and it's currently absent.
2. **Show behaviors with props**, not floating tags (Beat 3): a stroller cart, a phone glyph, a camera,
   a speech/gesture mark make "diversity" legible.
3. **Count the stats up** (Beat 4) so 120,914 and 227 *land*; add a mini-globe for "227 cities
   worldwide."
4. **De-tangle the trajectories**: stagger them, tie each curve to one behavior, and make them visibly
   respect sidewalks/crosswalk/obstacles (this is the whole point — context-aware paths).
5. **End on the PedGen bridge** so the scene hands off instead of just stopping.

## Reuse vs. build
- **Reuse:** `city_view` (panel/road/sidewalks/crosswalk/blocks/car), `pedestrian_icon`,
  `vehicle_icon`, `metric`, `TracedPath`.
- **Build:** a **void/mocap tile** + scene-blind straight path with wall/obstacle ⚠ for Beat 1;
  **behavior props** (stroller cart, phone, camera, speech glyph); **count-up** numbers
  (`ChangingDecimal`/`Integer` + updater); a **mini-globe** with city dots; the **PedGen bridge** token
  + box.

## One-line summary
Turn a 6 s fade-reel into a 20 s story built on the script's own contrast: **isolated mocap walks
through walls (Beat 1) → CityWalker trajectories follow the real scene (Beat 2) → diverse behaviors
shown with props (Beat 3) → the stats count up with a 227-cities globe (Beat 4) → collapse to a
"training signal" that hands off to PedGen (Beat 5).** Keep text to the caption, behavior tags, stat
labels, and the PedGen bridge; everything else is motion.
