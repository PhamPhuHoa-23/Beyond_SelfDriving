# 04 — Per-Scene Plan: Intro + Part 1

> Read [00_MASTER_PLAN.md](00_MASTER_PLAN.md), [01_DESIGN_SYSTEM.md](01_DESIGN_SYSTEM.md), [03_NARRATIVE_AUDIT.md](03_NARRATIVE_AUDIT.md), and the [Part 1 fix list](09_FIX_CHECKLIST.md#part-1) before editing.

Scene IDs map to files at `drivex/scenes/intro/` and `drivex/scenes/part01/`.

For each scene:
- **What**: short summary
- **Source**: original script + slide reference
- **Visual blueprint**: the on-screen layout
- **Animation flow**: ordered beats
- **Mascot use**: where PI / CAR appears, what they say (English on-screen)
- **End state**: what must fade out before next scene

---

## I-01 — Title Card

**File:** `drivex/scenes/intro/i01_title_card.py`
**Class:** `I01TitleCard`
**Duration:** ~30s

### What
Welcome card. Tutorial name, ICCV 2025 marker, that this is a student summary, contact note for organizers, mascot first appearance.

### Source
[script_part1.md](../materials/scripts/script_part1.md) — slide 1; [spec_intro_part01.md §I-01](../spec_prompts/spec_intro_part01.md).

### Visual blueprint (NAVY background — deliberate exception)
```
┌──────────────────────────────────────────────────┐
│  [UCLA logo]        Beyond Self-Driving         │  ← title GOLD bold 52
│                                                  │
│              ICCV 2025 Tutorial                  │  ← subtitle WHITE 24
│                  Team Summary                    │
│                                                  │
│           [Presenter Name] · UCLA                │  ← LIGHT_BLUE 20
│            UCLA Mobility Lab                     │
│        ────────────────────────                  │  ← divider line
│  For questions about the original material:      │
│         contact UCLA Mobility Lab                │
│                                          [CAR]   │  ← mascot bottom-right
└──────────────────────────────────────────────────┘
```

### Animation flow
1. `t=0` — `bg` navy fades in (0.3s)
2. `t=0.3` — Title `Write` (1.2s)
3. `t=1.5` — Subtitle `FadeIn(shift=UP*0.15)` (0.5s)
4. `t=2.0` — UCLA logo (placeholder) `FadeIn` (0.4s)
5. `t=2.5` — Presenter + Org `FadeIn` (0.5s)
6. `t=3.0` — Divider `Create` left-to-right (0.4s)
7. `t=3.4` — Contact `FadeIn` (0.4s)
8. `t=3.8` — CAR mascot `FadeIn(shift=LEFT*0.3)` (0.6s) + `idle_bounce`
9. `wait(1.5)` then `FadeOut(everything)` (0.6s)

### End state
Screen empty (next scene I-02 starts on its own bg).

---

## I-02 — The Hook

**File:** `drivex/scenes/intro/i02_hook.py`
**Class:** `I02Hook`
**Duration:** ~75s

### What
The emotional thesis, told as a 3-act visual essay:
- A: One smart car (FMs + radar) — sees, reasons, acts.
- B: Wall blocks the view — even smart car blind to what's behind.
- C: Two more cars share their views — cooperation reveals the hidden.

Then payoff quote: *"So we taught them to cooperate."*

### Source
[script_part1.md](../materials/scripts/script_part1.md) (the bridge concept) and [spec_intro_part01.md §I-02](../spec_prompts/spec_intro_part01.md).

### Background
Navy is acceptable here for emotional weight — but consider also doing the whole hook on white with deliberate dim grey "wall" — discuss with user. **Default: navy.** This is the only intro scene that gets navy.

### Known issue from review #1
> "I02 Hook: chữ i see còn đè lên 2 chữ gpt và vlm"

Translation: the "I see." text overlaps the GPT and VLM labels from sub-scene A.

**Fix**: in sub-scene C, before placing `i_see` text, the small `fm1` and `fm2` labels (GPT, VLM) must be `FadeOut`d. Currently the scene only fades the wall, blocked radar, and detection dots; it leaves `fm1, fm2` on screen.

### Animation flow (verified against existing implementation)
- Quote 4 lines write in
- Quote fades, sub-scene A: car + radar + GPT/VLM icons + thought bubble
- Sub-scene B: wall slides in, radar arcs blocked, blind zone red polygon
- Sub-scene C: 2 more cars, comm arcs, wall fades to opacity 0.2, hidden human visible, "I see." text
- Payoff quote: divider + "So we taught them to cooperate."

### Edits required
1. Add `FadeOut(fm1, fm2)` between sub-scenes B and C, or before placing `i_see`.
2. The thought bubble's text "There is a human / over there. / → Turn left." should use the new `TightBubble`.
3. End-of-scene `FadeOut(VGroup(divider, payoff))` already exists — confirm.

### End state
Screen black/navy, ready for I-03.

---

## I-03 — The 5-Part Roadmap

**File:** `drivex/scenes/intro/i03_roadmap.py`
**Class:** `I03Roadmap`
**Duration:** ~30s

### What
Show 5-node journey, each node labeled with the part name. Pulse all nodes. Highlight Part 1 in gold (we start here).

### Source
[spec_intro_part01.md §I-03](../spec_prompts/spec_intro_part01.md).

### Background
**WHITE.** This is the first body scene; sets the tone going into Part 1.

### Visual blueprint
```
                The 5-Part Journey                ← header NAVY 30
┌──────────────────────────────────────────────────┐
│                                                  │
│   ●─────●─────●─────●─────●                      │  ← spine + 5 nodes
│   1     2     3     4     5                      │
│ Found.  Coop  Sim-  Eff.  Phys.                  │  ← labels (zigzag OK in this scene)
│ Models  V2X   Real  V2X    AI                    │
│                                                  │
└──────────────────────────────────────────────────┘
```

### Animation flow
1. Header `FadeIn` (0.4s)
2. Roadmap spine + nodes draw via `roadmap.build_animation()`
3. All 5 nodes pulse (`scale(1.2)` rate-back-and-forth) staggered 0.12s
4. Part 1 node turns gold (0.4s)
5. `wait(1.2)`, then fade everything

### Edit required
- Verify `RoadmapStrip(current_part=0, mini=False)` shows labels properly without overlap. If labels overlap with each other (long names), wrap each label to 2 lines (already done in `PART_TITLES_LONG`).
- This scene **may keep zigzag labels** because the whole canvas is dedicated to it — no conflicting body content.

### End state
Empty white screen.

---

## P01-S01 — Opening Question

**File:** `drivex/scenes/part01/p01_s01_opening.py`
**Class:** `P01S01Opening`
**Duration:** ~30s

### What
PI asks the question that launches Part 1: *"Why, in 2025 — with AI writing code, drawing pictures, answering everything — can self-driving cars not yet drive everywhere?"*

### Source
[script_part1.md](../materials/scripts/script_part1.md) — slide 1 narration.

### Reviews to fix
- Review 1: "P01S01: Pi đang nói tiếng việt, đổi hết thành tiếng anh, chữ ở chính giữa và Pi nói chuyện bị dính vào chính giữa, có thể nâng text lên trên và thay vì hiện box của pi theo sequence và lần lượt nhiều vị trí khác nhau thì chỉnh cho nó 1 vị trí box thôi, chỉ là ẩn hiện."
- Review 2: "vị trí linh vật quá cao, làm overlap chữ, hạ thấp linh vật xuống."
- Review 3: "Mascot Pi ở vị trí hơi cao, làm cho cái box nói chuyện của nó bị overlap lên box chữ trước đó."

### Background
WHITE.

### Visual blueprint
```
┌──────────────────────────────────────────────────┐
│                                                  │
│  In 2025, AI can write code,                     │  ← line 1, NAVY 28, top
│  draw pictures, answer everything…               │  ← line 2, NAVY 28
│                                                  │
│  Why can't self-driving cars                     │  ← emphasis line, GOLD 30
│  drive everywhere yet?                           │
│                                                  │
│                                       [PI]       │  ← PI bottom-right
│                                                  │
│                  ┌── single bubble position ──┐  │
│                  │  "That's a great question…"│  │
│                  │  Or one short bubble.      │  │
│                  └────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

### Animation flow
1. `Write(line1)` (1.0s)
2. `Write(line2)` (0.8s)
3. `wait(0.5)`
4. `Write(emphasis_line)` golden, slightly larger (1.2s)
5. `wait(0.7)`
6. PI mascot `FadeIn(shift=LEFT*0.3)` at bottom-right (0.5s)
7. `PIBubble(pi, "That's our question for the next 10 minutes.", position=UP+LEFT)` — `get_pop_animation` (0.8s)
8. `wait(1.5)`
9. End: `FadeOut(VGroup(line1, line2, emphasis_line, pi, bubble))` (0.6s)

### Mascot rule
**One bubble, one position.** Position fixed at `pi UP+LEFT`. If you want a follow-up, do `Transform(bubble, new_bubble)` — don't add a second bubble.

PI sits **lower than the text** — at least 2.5u below the bottom of `emphasis_line`. The bubble extends `UP+LEFT` from PI; verify it doesn't overlap the text by adjusting PI's position to `DOWN*1.5` or further.

### English-only on screen
On-screen text is English. Vietnamese narration is for voiceover only.

### End state
Empty white screen.

---

## P01-S02 — GenAI Boom + Foundation Models

**File:** `drivex/scenes/part01/p01_s02_genai_boom.py`
**Class:** `P01S02GenAIBoom`
**Duration:** ~75s

### What
Two-act scene:
- Act 1: showcase recent GenAI capabilities (image gen, code, video gen, reasoning, multimodal). 5 mini-cards.
- Act 2: zoom out — they're all *foundation models*. Show Stanford's definition. Diagram: data → core model → many downstream tasks.

### Source
[script_part1.md](../materials/scripts/script_part1.md) — slides 3–4.

### Reviews to fix
- Review 1: "box foundation models còn hơi sát với chữ, mở rộng chiều rộng sẽ ok, phần fms là gì thì mũi tên đang chưa thẳng tắp."
- Review 2: "box của linh vật góc trên phải overlap với góc dưới trái của box fms, có thể là sau khi hiển thị thì nâng cao box FMs lên một xíu."

### Background
WHITE.

### Visual blueprint — Act 1
```
┌──────────────────────────────────────────────────┐
│   GenAI is everywhere                            │  ← header
│                                                  │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐│
│  │ Code │  │Image │  │Video │  │Reason│  │ MM   ││  ← 5 capability cards
│  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘│
│                                                  │
│            What do they have in common?          │  ← bridge text
└──────────────────────────────────────────────────┘
```

### Visual blueprint — Act 2
```
┌──────────────────────────────────────────────────┐
│   Foundation Models                              │  ← header GOLD bold
│                                                  │
│  "trained on broad data, adaptable to many       │  ← Stanford CRFM quote
│   downstream tasks"                              │
│        — Stanford CRFM                           │
│                                                  │
│  ┌─text──┐                  ┌─Q&A───┐            │
│  │ images│                  │class. │            │
│  │ speech│ → [FOUNDATION]→  │image  │            │
│  │ 3D    │     MODEL        │ cap.  │            │
│  └───────┘                  │recon. │            │
│   data                      └───────┘            │
│                              tasks               │
└──────────────────────────────────────────────────┘
```

### Animation flow
**Act 1 (~25s):**
1. Header `Write`
2. 5 capability cards `LaggedStart(FadeIn, lag_ratio=0.15)` — left to right
3. `wait(2)`
4. Bridge text `Write`
5. `wait(0.7)`

**Transition:** All Act 1 mobjects `FadeOut`. New header.

**Act 2 (~50s):**
6. Header "Foundation Models" `Write`
7. CRFM quote `FadeIn` slowly (1.5s) — center, italic
8. `wait(1)`
9. Quote shifts up to make room
10. Data column (left): `FadeIn` 4 small labels stacked vertically
11. Foundation Model box (center) `GrowFromCenter`
12. Downstream task column (right): `LaggedStart(FadeIn, lag_ratio=0.1)` 4 labels
13. `Arrow(data, fm)` and `Arrow(fm, tasks)` — `Create` together
14. PI bubble (top-right corner of canvas) "Why not for cars?" — pop, hold, fade
15. End — fade Act 2

### Bubble fix
The PI bubble in Act 2 must NOT overlap the FM diagram. Position PI in the **upper-right corner** with bubble extending `UP+LEFT` (small bubble — single short question). Or, after PI bubble fades, animate the FM diagram up by `0.3u` if needed.

### End state
Empty white screen.

---

## P01-S03 — AV Architectures

**File:** `drivex/scenes/part01/p01_s03_av_arch.py`
**Class:** `P01S03AVArch`
**Duration:** ~75s

### What
Three architecture paradigms:
- **Modular**: perception → loc → prediction → planning → control. Most deployed but error accumulates.
- **End-to-End**: sensors → NN → action. No info loss but black box.
- **Hybrid**: ML for perception/planning, classical control. Pragmatic compromise.

Then: *"All three share one weakness FMs will expose."*

### Source
[script_part1.md](../materials/scripts/script_part1.md) — slide 5.

### Reviews
- Review 1: "P01S03: AV Arch: ok"

### Background
WHITE.

### Visual blueprint
```
┌──────────────────────────────────────────────────┐
│   Three architectures for AVs                    │
│                                                  │
│   Modular:                                       │
│   [Perception]→[Loc]→[Pred]→[Plan]→[Control]    │
│                                                  │
│   End-to-End:                                    │
│   [Sensors] ──────────→ [Action]                 │
│                                                  │
│   Hybrid:                                        │
│   [Perception ML]→[Planning ML]→[Control class.]│
│                                                  │
│   ────────────────────────────────────────       │
│   All three share ONE weakness…                  │
└──────────────────────────────────────────────────┘
```

### Animation flow
1. Header `Write`
2. Modular row: 5 boxes `arrange(RIGHT)`, `LaggedStart(FadeIn)`, then 4 arrows `LaggedStart(GrowArrow)`
3. Pause; subtitle "error accumulates" appears under modular row, then fades
4. End-to-End row: 2 boxes + arrow, faster reveal
5. Subtitle "no error accumulation, but black-box" appears + fades
6. Hybrid row: 3 boxes
7. Subtitle "best of both — most companies' choice" appears + fades
8. Bridge line: "All three share ONE weakness…" — `Write`, hold ~1s
9. End — fade everything

### End state
Empty white screen.

---

## P01-S04 — Long-Tail Problem

**File:** `drivex/scenes/part01/p01_s04_longtail.py`
**Class:** `P01S04LongTail`
**Duration:** ~80s

### What
The long-tail distribution. 99% normal driving, 1% edge cases (3 hero images: phone-on-road person, traffic-light truck, snow-covered road). Then: humans handle these via *common-sense reasoning* — which we need to teach to AVs.

### Source
[script_part1.md](../materials/scripts/script_part1.md) — slide 6.

### Reviews
- Review 1: "cái trục của distribution xuất hiện sau khi nói chuyện (nó sai), nó nên xuất hiện đồng thời với phân phối, sau khi 3 cái node vào 1% thì nên thu nhỏ nó lên trên, sau đó cho 2 mascot nói chuyện chứ không nó overlap"
- Review 2: "vấn đang hiện 2 cái trục sau khi hiện phân phối. đúng ra 2 linh vật noi chuyện với nhau sau khi ẩn phân phối đi"
- Review 3: "Còn lỗi vẽ trục sau khi đã hiển thị phân phối, 99 và 1, đúng ra nó phải là vẽ trục rồi mới vẽ mấy cái hàm chứ"

### Critical fix order

**Axes BEFORE distribution.** This is the most-flagged bug in the project. Pseudocode:

```python
# WRONG (current):
distribution = ParametricFunction(lambda t: ..., color=COL_BLUE)
self.play(Create(distribution))
axes = Axes(...)
self.play(Create(axes))   # ← appears AFTER, looks wrong

# RIGHT (do this):
axes = Axes(x_range=[0, 10], y_range=[0, 1], ...)
self.play(Create(axes), run_time=0.6)
self.play(Create(axes.x_label, axes.y_label))
distribution = axes.plot(lambda x: ..., color=COL_BLUE)
self.play(Create(distribution), run_time=1.2)
```

### Background
WHITE.

### Visual blueprint
```
┌──────────────────────────────────────────────────┐
│   The Long-Tail Problem                          │
│                                                  │
│   ┃                                              │
│   ┃     ●                                        │
│   ┃   ●     ●                                    │
│   ┃ ●         ●  ●                               │
│   ┃●            ●  ●  ●  ●  ●                    │
│   └─────────────────────────────────────►        │
│   common                  rare = 1%              │
│                                                  │
│   [phone person]  [traffic-light truck]  [snow]  │  ← 3 hero images
│                                                  │
│        ↓ humans handle these via                 │
│        common-sense reasoning                    │
│                                                  │
│   [PI]  ↔  [CAR] discussing                      │
└──────────────────────────────────────────────────┘
```

### Animation flow
1. Header `Write`
2. Axes `Create` (0.6s)
3. Distribution curve `Create` left-to-right (1.2s)
4. 99% / 1% labels `FadeIn` at appropriate x positions
5. 3 hero images (use `SlideImage` with placeholders if no real images) — `LaggedStart(FadeIn)`
6. Each image labeled below with one-line caption
7. **Distribution chart shrinks UP** (smaller scale, top of canvas) — `self.play(distribution_group.animate.scale(0.5).to_edge(UP))`
8. PI appears bottom-left, asks: "How do humans handle this?"
9. CAR appears bottom-right, answers: "Common-sense reasoning."
10. Final line `Write`: "We need common-sense and generalist experience."
11. End: fade all

### Mascot positioning
Both mascots **below the shrunk distribution**, with bubbles extending toward the empty canvas (PI's bubble → UP+RIGHT; CAR's bubble → UP+LEFT). Verify no overlap with the distribution-up-top.

### End state
Empty white screen.

---

## P01-S05 — FMs Empower AV

**File:** `drivex/scenes/part01/p01_s05_fm_empower.py`
**Class:** `P01S05FMEmpower`
**Duration:** ~70s

### What
Diagram: 5 categories of foundation models (left) → 6 AV needs (right). Center arrow labeled "Empower". Below: target = "Long-tail Generalization & Generalist Experience".

### Source
[script_part1.md](../materials/scripts/script_part1.md) — slide 7. Slide image `materials/images/part1/p1_s07_foundation_models_empower_av_*.png`.

### Reviews
- Review 1: "P01S05: ổn nhưng không hiểu sao nền xanh"
- Review 2: "P01S05FMEmpower: tăng chiều rộng cho box bên trái, tăng chung 5 cái vì cái cuối chữ multimodal overlap với clip/llava/blip"

### Critical fix
- Background must be WHITE (not navy/blue).
- Left-side 5 boxes: increase width so multi-line labels don't overflow.

### Background
WHITE (fix the bug).

### Visual blueprint
```
┌──────────────────────────────────────────────────┐
│   Foundation Models empower AV                   │
│                                                  │
│  ┌─VFM────┐                  ┌─AutoLabel─┐       │
│  │SAM/CLIP│                  │           │       │
│  │  DINO  │                  └───────────┘       │
│  └────────┘                  ┌─Sim───────┐       │
│  ┌─VGM────┐                  │           │       │
│  │Cosmos  │      Empower     └───────────┘       │
│  │  Wan   │   ──────────►    ┌─Vehicle───┐       │
│  └────────┘                  │ Interface │       │
│  ┌─VSM────┐                  └───────────┘       │
│  │MotionLM│                  ┌─Reasoning─┐       │
│  └────────┘                  │           │       │
│  ┌─LLM────┐                  └───────────┘       │
│  │GPT/etc │                  ┌─E2E────────┐      │
│  └────────┘                  │  Stacks    │      │
│  ┌─MLLM───┐                  └────────────┘      │
│  │Gemma3  │                                      │
│  │QwenVL  │                                      │
│  └────────┘                                      │
│                                                  │
│       Long-tail Generalization & Experience      │  ← target gold
└──────────────────────────────────────────────────┘
```

### Animation flow
1. Header `Write`
2. Left column: 5 boxes `arrange(DOWN, buff=0.25)`, `LaggedStart(FadeIn)` (each box width ≥ 2.4u so text fits)
3. Right column: 6 boxes `arrange(DOWN)`, `LaggedStart(FadeIn)`
4. Center "Empower" arrow `GrowArrow` with label
5. Bottom target text `Write` (gold)
6. End: fade all

### Box width fix
Make every box `width=2.4` minimum. Multimodal box label may need 2 lines: `"MLLM\nGemma3 / QwenVL"`.

### End state
Empty white screen.

---

## P01-S06 — VLA Roadmap & Datasets

**File:** `drivex/scenes/part01/p01_s06_vla_roadmap.py`
**Class:** `P01S06VLARoadmap`
**Duration:** ~80s

### What
Two acts:
- Act 1: VLA approach roadmap — 4 strategies (text action / numerical action / explicit guidance / implicit transfer).
- Act 2: Quote about language interface + datasets (DriveLM, CoVLA, Impromptu VLA). DriveLM's graph chain visualized: "I see X" → "I predict Y" → "I will do Z" → "trajectory".

### Source
[script_part1.md](../materials/scripts/script_part1.md) — slides 9–11.

### Reviews
- Review 1: "trong cái chain thì cái chữ gần cái node quá, đừng chỉ làm mờ, bạn move nó vào giữa nó overlap hết, fadeout luôn hoặc thu nhỏ hoặc move lên trên head 1 cách có tổ chức"
- Review 2: "vẫn là text trên roadmap quá gần line, không đọc được"
- Review 3: "Làm cho cái box language is at the core bự hơn về chiều rộng một xíu tại vì hiện tại chữ đang dính với box ở 2 phía trái phải. Tự nhiên cuối scene nó hiện tất cả mọi thứ lên lại nó kỳ cục nên bỏ giúp tôi nhé"

### Critical fixes
1. **DriveLM chain text-near-node**: when nodes are placed, labels collide with nodes. Either:
   - Place labels far enough below/above with explicit `buff=0.4`+, OR
   - Show label, hold, then `FadeOut` label before next node. Don't just dim.
2. **"Language is at the core" box** too narrow — increase width.
3. **End-of-scene replay bug**: scene currently re-plays all elements at the end. Remove the replay; just fade out cleanly.

### Background
WHITE.

### Visual blueprint — Act 1 (4 strategies)
```
       VLA Strategies for AV
   ┌──────────────────────────┐
   │  Text Action             │  → e.g., GPT-Driver
   │  Numerical Action        │  → e.g., DriveGPT4
   │  Explicit Guidance       │  → e.g., DriveLM
   │  Implicit Transfer       │  → e.g., latent representations
   └──────────────────────────┘
```

### Visual blueprint — Act 2 (DriveLM chain)
```
   "Language is at the core of contextual
    understanding and reasoning."

   [I see…] → [I predict…] → [I should…] → [trajectory]
        each node ~1.4u wide; arrow between; label BELOW node
        with buff = 0.45u

   Datasets:  DriveLM     CoVLA     Impromptu VLA
              graph QA   80h video  80K clips
```

### Animation flow
**Act 1:**
1. Header `Write`
2. 4 row stack `LaggedStart(FadeIn)` each row showing strategy name + example label

**Transition:** Fade Act 1.

**Act 2:**
3. Quote `FadeIn` slowly (1.5s)
4. Quote shifts up slightly
5. DriveLM chain — 4 nodes drawn left-to-right with `Create`, then 3 arrows
6. Each node label: appear → hold 1s → fade BEFORE next node (per review #1: "fadeout luôn")
7. Datasets row: 3 dataset cards stagger in
8. **DO NOT** play "FadeIn(everything_again)" — review #3 explicitly bans this
9. End: `FadeOut` everything, clean

### "Language is at the core" box
If you draw it as a `RoundedRectangle`, set `width=8` (was probably 6 — too narrow for the text). Add 0.4u padding.

### End state
Empty white screen.

---

## P01-S07 — VLA Architectures (4 examples)

**File:** `drivex/scenes/part01/p01_s07_vla_arch.py`
**Class:** `P01S07VLAArch`
**Duration:** ~120s (longest scene in Part 1)

### What
Four VLA architectures, each with a mini-pipeline diagram:
1. **GPT-Driver** — GPT-3.5 as zero-shot planner. Text in → action.
2. **BEVDriver** — LiDAR + camera → BEV → Q-Former → LLM → waypoints.
3. **EMMA (Waymo)** — camera → Gemini → CoT + perception + road graph + trajectory.
4. **DriveVLM (Tsinghua)** — dual-system: VLM (slow, high-level) ‖ traditional 3D (fast, low-level).

### Source
[script_part1.md](../materials/scripts/script_part1.md) — slides 12–16.

### Reviews
- Review 1: "BEVDriver mấy cái module không thẳng hàng, mũi tên thì thẳng rồi nhưng align giữa các block chưa đẹp"
- Review 2: "mũi tên ở gptdriver ngắn quá, bevdriver, vẫn chưa căn chỉnh chính giữa 1 dòng cho các block phía sau"
- Review 3: "Cái BEV Map có cái hình gì hay sao mà không align thẳng hàng vậy, nếu bạn muốn vẽ thì cụ thể hoặc không thì bỏ đi tại vì flow đang khá align và thẳng cái BEV nó bị tụt xuống dưới"

### Critical fixes
1. **BEVDriver row blocks not horizontally aligned** → use `VGroup(*blocks).arrange(RIGHT, buff=0.5)`. All blocks must be `height=0.9` (uniform).
2. **GPT-Driver arrows too short** → arrows from box edge to box edge with `buff=0.05`.
3. **BEV map illustration** disrupting alignment → either render the BEV as a separate small icon ABOVE the row (not inline), OR remove the illustration entirely and keep the row uniform.

### Background
WHITE.

### Visual blueprint
```
     Four VLA architectures

GPT-Driver:    [Text] → [GPT-3.5] → [Action]    ← row 1 (uniform height)
BEVDriver:     [LiDAR+Cam] → [BEV] → [Q-Former] → [LLM] → [Waypoints]
EMMA:          [Camera] → [Gemini] → [CoT+Perc+RG+Traj]
DriveVLM:      ┌─[VLM (slow, scene+plan)]────────────┐
               │                                      ├→ [merge]
               └─[3D Perception (fast, traj)]────────┘
```

### Animation flow
For each of the 4 architectures:
1. Title label `Write`
2. Pipeline blocks `LaggedStart(FadeIn)` along a horizontal line
3. Arrows `LaggedStart(GrowArrow)`
4. 1-line caption appears, holds 1s, fades

After all 4:
5. Bridge line: "Language at the center of every one." `Write`
6. End: fade all

### Layout enforcement helper
Add at top of file:
```python
def _pipeline_block(text, w=1.8, h=0.9, color=COL_NAVY):
    box = RoundedRectangle(corner_radius=0.1, width=w, height=h,
                           fill_color=COL_DEEP_BLUE, fill_opacity=1,
                           stroke_color=color, stroke_width=1.5)
    label = Text(text, font_size=18, color=color).move_to(box)
    return VGroup(box, label)
```
Use this for every block. All blocks come out the same size.

### End state
Empty white screen.

---

## P01-S08 — AutoVLA

**File:** `drivex/scenes/part01/p01_s08_autovla.py`
**Class:** `P01S08AutoVLA`
**Duration:** ~110s

### What
UCLA's flagship Part 1 contribution. Two halves:
- A: Architecture — single VLM with **dual fast/slow modes**, chosen based on scene complexity.
- B: Training — Stage 1 (SFT for dual-thinking) → Stage 2 (RFT with GRPO for verified rewards). Result: +10.6% planning, −66.8% runtime.

### Source
[script_part1.md](../materials/scripts/script_part1.md) — slides 17–20.

### Reviews
- Review 1: "Nâng những block đầu lên cao một xíu, vì khi hiển thị reasoning training gì đó thì nó overlap vào block stage 1 stage 2"
- Review 2: "chỉnh sao mà kéo cái region stage xuống dưới làm overlap với các block nội dung liên quan"
- Review 3: "Chỉnh lại ending tại vì tụi mình còn merge video (lỗi hơi kiểu kiểu P01S06VLARoadmap nhưng nó hơi ngược là nó ẩn đi hết và tự nhiên để 2 cái text stage 1 với stage 2 lại)"

### Critical fixes
1. **Layered overlap**: when "Reasoning training" annotation appears, it lands on top of the Stage 1/Stage 2 boxes. Move Stage 1/2 region UP by 0.5u OR keep annotation entirely below the canvas-vertical-mid.
2. **End-of-scene leftover**: at scene end, "Stage 1" and "Stage 2" text remain on screen. Add explicit `FadeOut(stage1_label, stage2_label)` to the final cleanup.

### Background
WHITE.

### Visual blueprint — Act A (architecture)
```
   AutoVLA — one model, two thinking modes

   Simple road →  [VLM] → [Fast: action only]
   Complex int. → [VLM] → [Slow: chain-of-thought + action]

   ┌─Switch logic─┐
   │ scene complexity → mode  │
   └──────────────────────────┘
```

### Visual blueprint — Act B (training)
```
   ┌── Stage 1: SFT ──────────┐  ┌── Stage 2: RFT (GRPO) ──────┐
   │ supervised dual-thinking │  │ verified-reward alignment   │
   └──────────────────────────┘  └─────────────────────────────┘

      Result: +10.6% planning · −66.8% runtime
```

### Animation flow
**Act A:**
1. Title + subtitle
2. Two parallel rows reveal sequentially:
   - Row 1: simple scene → fast mode
   - Row 2: complex scene → slow mode
3. Switch box appears between rows
4. Hold

**Act B:**
5. Acts A elements shrink/move UP to give room (or fade entirely)
6. Stage 1 box `FadeIn` left
7. Stage 2 box `FadeIn` right
8. Arrow Stage 1 → Stage 2 `GrowArrow`
9. Result line `Write` (gold, bold)
10. **End cleanup** — explicit `FadeOut` of EVERY mobject including stage labels, result text, arrows

### End state
Empty white screen — verified by checking `self.mobjects` is `[bg]` only.

---

## P01-S09 — Takeaways + Future Directions

**File:** `drivex/scenes/part01/p01_s09_takeaways.py`
**Class:** `P01S09Takeaways`
**Duration:** ~60s

### What
4-point recap of Part 1, then 4 future directions, then bridge to Part 2.

### Source
[script_part1.md](../materials/scripts/script_part1.md) — slides 22–24.

### Reviews
- Review 1: "ok ổn, nhưng sẽ ổn hơn nếu tăng chiều rộng, và chỉnh lại khoảng cách giữa các box"

### Background
WHITE.

### Visual blueprint
```
       Part 1 Takeaways

   ┌──────────────┐  ┌──────────────┐
   │ Long-tail    │  │ MLLMs scale  │
   │ generalization│  │ AV reasoning │
   └──────────────┘  └──────────────┘
   ┌──────────────┐  ┌──────────────┐
   │ Diverse      │  │ Open issues: │
   │ architectures│  │ safety, lat, │
   │              │  │ data         │
   └──────────────┘  └──────────────┘
```

### Animation flow
1. Header `Write`
2. 2×2 grid of takeaway cards `LaggedStart(FadeIn)` — each card width ≥ 4.0u
3. Hold 2s
4. Cards fade
5. New header "What's next?" — 4 future-direction lines as bullets
6. Bridge line: "Single-agent has a limit even FMs can't break — let's see what comes next."
7. End: fade all

### Box width fix (review #1)
Each takeaway card: `width=4.5` (was probably 3.5). Buff between cards: `0.6u`.

### End state
Empty white screen.

---

## End-of-part summary checkbox

For Sonnet 4.6 to track progress per scene:

- [ ] I-01 Title Card
- [ ] I-02 Hook (fix `fm1, fm2` overlap with `i_see`)
- [ ] I-03 Roadmap
- [ ] P01-S01 Opening (fix PI position; English only; one bubble)
- [ ] P01-S02 GenAI Boom (fix FM box width, arrow alignment, PI overlap)
- [ ] P01-S03 AV Arch (was OK in review — verify still good)
- [ ] P01-S04 Long-tail (axes BEFORE distribution; shrink chart up before mascots talk)
- [ ] P01-S05 FM Empower (white BG, widen left boxes)
- [ ] P01-S06 VLA Roadmap (fade chain labels; widen "language at core" box; remove end-replay)
- [ ] P01-S07 VLA Arch (uniform block height; longer arrows; remove inline BEV illustration)
- [ ] P01-S08 AutoVLA (move Stage region up; explicit FadeOut at end including stage labels)
- [ ] P01-S09 Takeaways (widen cards to 4.5u, increase buff)
