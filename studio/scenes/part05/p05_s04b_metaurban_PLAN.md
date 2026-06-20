# Animation Plan — P05S04BMetaUrban ("MetaUrban Generator")

Scene: [p05_s04b_metaurban.py](p05_s04b_metaurban.py). Two goals: (1) grow the animation from the
current ~7 s of fade-ins to **~20 s that actually tells the script**, and (2) **redesign the
"procedural engine"**, which currently reads as a cluttered cyan asterisk, not a generator.

## Script being served
> "MetaUrban, published as an **ICLR 2025 Spotlight**, is a **compositional** simulation platform for
> urban environments. Instead of designing specific scenes, MetaUrban uses **description scripts** to
> procedurally generate environments: the number of **city blocks**, **intersection types**, **lane
> widths**, **sidewalk configurations**, **vegetation density**, and the **placement and density of
> objects**. Varying these parameters across **different distributions** generates an **effectively
> infinite variety** of unique training environments."

Three ideas must land: **(a) script → procedural engine → scene**, **(b) the scene is *composed*
layer-by-layer from the named parameters**, **(c) varying the parameter *distributions* yields
*infinite, unique* scenes.** Today only (a) is shown, weakly.

## Current problems
- **Too short / monotonous (~7 s):** terminal fade → chips fade → 4 packets cross → gear spins → 3
  scenes swap → punch. Each step is a single fade; no build, no payoff for "infinite."
- **The engine is ugly:** `gear()` is a 0.46 cyan disc + a 0.67 ring + **10 thin teeth** + **6 amber
  inner dots** ([lines 89–130](p05_s04b_metaurban.py#L89-L130)). The thin teeth + inner dot ring read
  as a **sun/asterisk**, the rotation is barely legible at that tooth size, and cyan+amber clash with
  the Part-5 pink identity.
- **"Compositional" is never shown** — scenes just `ReplacementTransform` into each other; the viewer
  never sees a scene *assembled from parts*.
- **"Infinite variety" is a text label** (`scene 1 → 2 → 3 → … → infinite`) rather than a visual.

---

## Redesign: the "procedural engine"

Replace the asterisk with a clean, legible **generator module** that says *procedural + compositional*:

**Build:**
- A **rounded-hex housing** (or a squircle) in Part-5 pink/teal, ~1.3 units, with a soft fill and a
  crisp 2px stroke — a solid "machine," not a thin ring.
- **One clean gear** inside: ~8 **chunky trapezoidal teeth** (not 10 thin sticks) + a glowing **core
  dot**; rotation is obvious because the teeth are big.
- A **seed / RNG badge** on top: a small **die** (or a tiny distribution curve) that **rolls/ticks**
  on each generate — this is what makes it read as *procedural*, not just "a gear."
- An **input funnel** (left) where parameter tokens enter, and an **emitter slot** (right) where the
  assembled scene exits.
- Clean label `procedural engine` at `SIZE_CAPS` (legible), or replace with a ⚙+die glyph.

**Motion:** gear rotates continuously while active; on each "generate," the **core pulses** and the
**seed rolls**; tokens visibly **drop into** the funnel and a scene **emerges** from the emitter.

**Alternative (if you want extra flair):** a "3-D printer" engine that builds the scene **layer by
layer** on its output bed (ties perfectly to the compositional beat below). Pick one; don't do both.

---

## 20 s storyboard

Layout keeps the **script (left) → engine (center) → scene (right)** flow. Engine and scene get more
room; the parameter chips become the spine of the compositional build.

| # | t (s) | What happens (motion-first) | On-screen text | Components |
|---|------|------------------------------|----------------|-----------|
| 1 | 0–2.5 | **Establish.** Title + a small **`ICLR 2025 Spotlight`** ribbon badge. The terminal **types** the description script line-by-line (typewriter, blinking cursor), not an instant fade. | terminal code (it *is* the "description script"); `ICLR 2025 Spotlight` | `terminal()`, `contribution_badge`, `AddTextLetterByLetter`/cursor |
| 2 | 2.5–4.5 | **Engine powers on & ingests the script.** The redesigned engine fades in, gear starts turning, seed badge lights. The 5 **parameter chips** (`layout · lanes · sidewalks · vegetation · objects`) light up under the terminal and **stream as colored tokens into the engine's funnel**. Input arrow draws. | 5 chip labels | new `engine()`, chips (extend to 5), token `MoveAlongPath` |
| 3 | 4.5–8.5 | **Compositional assembly (the key beat).** The engine emits ONE scene that **builds up layer by layer**, each layer fired by its chip pulsing: **blocks** → plot grid; **intersection** → roads connect (T per script); **lane_width** → lane markings; **sidewalks** → sidewalk borders; **vegetation** → trees pop; **objects** → benches placed. Each chip glows as its layer lands. | — (chips already labeled) | layered `scene_tile` rebuilt as separately-animatable layers; `LaggedStart` |
| 4 | 8.5–13 | **Vary the distributions.** The chips flip to show **tiny distributions** (mini-histograms / sliders / a die). A **reroll**: die tumbles, sliders jitter, samples fire → engine spins (seed rolls, core pulses) → a **visibly different** scene assembles (different block count, intersection becomes `+` then a roundabout, denser objects). Do this **2×**, fast, each clearly distinct. | — | mini-histogram helper, more `scene_tile` variants (X/+/Y/roundabout, density levels) |
| 5 | 13–17.5 | **Effectively infinite variety.** Each new scene **shrinks and flies into a growing gallery wall** on the right; the engine keeps emitting, faster and faster, until a **grid of dozens of unique tiles** fills the space and cascades. A `∞` punctuates the `scene 1 → 2 → 3 → … → ∞` counter as the wall completes. | `scene 1 → 2 → 3 → … → ∞` | scaled `scene_tile` clones, `grid_4`/lattice, accelerating `LaggedStart` |
| 6 | 17.5–20 | **Payoff & settle.** Wall settles; punch line lands (`Diversity > Quantity`, or `∞ unique environments`); brief hold → `_close()`. | `Diversity > Quantity` | existing `punch`, `_close` |

Beats sum to ~20 s. If long, trim the second reroll in Beat 4 or the cascade tail in Beat 5.

## Text budget (keep it light)
On screen at rest: title + `ICLR 2025 Spotlight` badge; the terminal code block; 5 chip labels; the
`scene … → ∞` counter; one punch line. The reroll distributions, the layer build, and the gallery wall
are **all visual** — no sentences mid-beat.

## Coverage map (beat → script)
- "ICLR 2025 Spotlight / compositional platform" → **Beat 1**
- "uses description scripts to procedurally generate" → **Beats 1–2**
- "blocks, intersections, lane widths, sidewalks, vegetation, objects" → **Beat 3** (each is a layer)
- "varying these parameters across different distributions" → **Beat 4** (distributions + reroll)
- "effectively infinite variety of unique environments" → **Beat 5** (gallery wall + ∞)

## Reuse vs. build
- **Reuse:** `terminal()` (add typewriter), `scene_tile()` (refactor into animatable layers + add
  intersection/density variants), `chips`, `punch`, `counter`, `contribution_badge` for the spotlight
  ribbon.
- **Build:** the new **`engine()`** (hex housing + chunky gear + seed die + funnel/emitter);
  **mini-distribution** chips (histogram/slider/die); a **layered scene builder** so Beat 3 can stage
  blocks→roads→lanes→sidewalks→trees→objects; the **gallery-wall** accumulator for Beat 5.

## Implementation notes
- Make `scene_tile` return its layers as named sub-VGroups (`plots`, `roads`, `lanes`, `sidewalks`,
  `vegetation`, `objects`) so Beat 3 can `LaggedStart` them and Beats 4–5 can recolor/rebuild cheaply.
- Keep the gear rotation `rate_func=linear` and *continuous* during active beats; pulse the core via a
  brief `Indicate`/scale on each generate so "it's working" reads.
- Part-5 identity: lead with `ACCENT_PINK`/`PASTEL_PINK` for the engine and output accents; reserve
  amber/teal for the parameter chips so the colors mean "parameters," not decoration.

## One-line summary
Turn a 7 s fade-reel into a 20 s story: **type the script → a clean redesigned engine ingests the
parameters → it visibly *composes* one scene layer-by-layer (blocks→roads→lanes→sidewalks→trees→
objects) → rerolling the parameter *distributions* spits out different scenes → they pile into an
infinite gallery wall (→ ∞).** Replace the asterisk-gear with a hex engine + chunky gear + a rolling
seed die so it reads as a *procedural generator*, and keep text to the badge, chip labels, and the
∞ counter.
