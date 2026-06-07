# EXECUTION PROMPTS — Beyond Self-Driving

> Paste each PROMPT block into a fresh Claude session.
> Each prompt is self-contained. Do NOT paste multiple at once.
> Working directory for all prompts: `drivex_v2/` (start from scratch).
> Source material: `materials/scripts/` (narrative) · `materials/images/` (slide images).
> Render check: `manim -ql drivex_v2\scenes\<file>.py <ClassName>`

---

## GLOBAL DESIGN RULES (embedded in every prompt)

These apply to every scene in `drivex_v2/`:
- **Background**: white `#FFFFFF` for body scenes; navy `#0F172A` for part-title cards only
- **Text**: English only on screen; `COL_NAVY = "#334155"` for body text; minimum font size 22
- **Bubbles**: tight-fit (width = text + 0.30u pad each side); light fill; thin 1.5pt border; ONE bubble per mascot at a time (show → wait 1s → fade)
- **Pipeline blocks**: uniform height 0.9u; `arrange(RIGHT, buff=0.5)`; all arrows `Arrow(a.get_right(), b.get_left(), buff=0.05)`
- **Charts**: axes drawn BEFORE data, always
- **Scene end**: `FadeOut` ALL transient mobjects before scene ends — no leftovers
- **No overlap**: if two elements would overlap, fade the older one first

---

## PROMPT 0 — Project setup + all components

```
Project: Beyond Self-Driving (Manim, 3B1B style, ICCV 2025 tutorial)
Task: Create drivex_v2/ from scratch with complete component library.

Working directory: c:\Users\admin\Downloads\ML\Lab01_3B1B\
Create: drivex_v2/ with subdirs components/, scenes/intro/, scenes/part01/ ... scenes/part05/, render/
Manim env: base conda (run `manim` directly, NOT conda activate manim_env)

==== CREATE drivex_v2/__init__.py (empty) ====

==== CREATE drivex_v2/components/__init__.py ====
from .colors import *
from .mascots import create_car_mascot, create_pi_mascot, idle_bounce, wave_animation
from .thought_bubble import TightBubble, PIBubble, SpeechBubble, ThoughtBubble
from .roadmap import RoadmapStrip
from .title_card import make_part_title_card
from .slide_helper import SlideImage

==== CREATE drivex_v2/components/colors.py ====
BG_DARK = "#FFFFFF"
BG_PART_TITLE = "#0F172A"  # navy for part title cards only
COL_NAVY = "#334155"
COL_BLUE = "#3B82F6"
COL_GOLD = "#F59E0B"
COL_LIGHT_BLUE = "#BFDBFE"
COL_WHITE = "#334155"   # alias — old code uses COL_WHITE for text
COL_RED = "#EF5350"
COL_GREEN = "#4ADE80"
COL_GREEN_DARK = "#16A34A"   # text-on-white green
COL_PURPLE = "#A78BFA"
COL_INFRA_ORANGE = "#FB923C"
COL_ROAD_GRAY = "#94A3B8"
COL_SENSOR_CYAN = "#06B6D4"
COL_INT8_GREEN = "#34D399"
COL_FP32_RED = "#F87171"
COL_ENERGY_YELLOW = "#FBBF24"
COL_DEEP_PURPLE = "#E9D5FF"
COL_DEEP_GREEN = "#DCFCE7"
COL_DEEP_BLUE = "#DBEAFE"
COL_GRAY_FILL = "#F1F5F9"
COL_DANGER_FILL = "#FECACA"
COL_SOFT_PURPLE = "#C4B5FD"
COL_BUBBLE_PI_FILL = "#DBEAFE"
COL_BUBBLE_CAR_FILL = "#FEF3C7"
COL_PEDESTRIAN = "#F39C12"
COL_ROBOT_TEAL = "#1ABC9C"
COL_SIM_PURPLE = "#9B59B6"
COL_MESH_GRAY = "#7F8C8D"
UCLA_BLUE = "#2774AE"
UCLA_GOLD = "#FFD100"

==== CREATE drivex_v2/components/thought_bubble.py ====
# TightBubble: fits text tightly, light fill, thin border, triangular tail.
# Width = text.width + 2*pad_x (no minimum clamp).
# PIBubble = blue border, light-blue fill.
# SpeechBubble = gold border, light-gold fill.
# ThoughtBubble = alias for TightBubble (back-compat).
#
# get_pop_animation() returns LaggedStart(tail, bubble, text).
#
# Implement using RoundedRectangle + Text + Polygon tail.
# Tail: small triangle pointing from bubble corner toward target.
# pad default: pad_x=0.30, pad_y=0.18, corner_radius=0.18, stroke_width=1.5

==== CREATE drivex_v2/components/mascots.py ====
# CarMascot: side-view car. body_color="#2774AE", stroke COL_NAVY 2pt.
#   Wheels dark fill with COL_NAVY stroke (not WHITE — invisible on white BG).
# PiMascot: circle body. color="#BFDBFE" (light blue), stroke COL_NAVY.
#   Eyes, smile, pi-symbol all COL_NAVY.
# idle_bounce(mascot, amplitude=0.08, run_time=0.8): subtle up-down once.
# wave_animation(mascot, run_time=1.0): slight tilt+bounce.
# Both try SVG from assets/ first, fall back to geometric.
# Assets dir relative to this file: ../assets/

==== CREATE drivex_v2/components/roadmap.py ====
# RoadmapStrip(current_part=0, mini=False, spine_width=10.5)
# Full mode (mini=False): spine + 5 nodes + labels (zigzag above/below).
# Mini mode (mini=True): spine + 5 dots ONLY — no labels.
#   Use mini=True for title cards. Labels only in the dedicated I-03 scene.
# current_part node fills COL_GOLD; others COL_NAVY outline.
# build_animation() returns LaggedStart drawing spine then nodes.

==== CREATE drivex_v2/components/slide_helper.py ====
# SlideImage(rel_path, width=5, height=3):
#   Looks in drivex_v2/assets/ and materials/images/.
#   If file not found, returns labeled RoundedRectangle placeholder
#   (fill COL_GRAY_FILL, stroke COL_NAVY, text = rel_path, font 14).

==== CREATE drivex_v2/components/title_card.py ====
# make_part_title_card(part_num, title, speaker, quote) → Scene subclass.
# Background: BG_PART_TITLE (navy).
# Layout: "Part NN" supertitle (GOLD small), main title (GOLD bold 32),
#   speaker line (LIGHT_BLUE 18), quote (italic GOLD 20), mini roadmap strip bottom.
# Fade in from white, fade out to white.

==== CREATE drivex_v2/scenes/__init__.py (empty) ====
(repeat for each part subdir)

==== SMOKE TEST: CREATE drivex_v2/scenes/_smoke_test.py ====
Class SmokeTest(Scene):
- White BG
- Header text
- PI mascot left + PIBubble "Why tight bubbles?" (UP+RIGHT)
- CAR mascot right + SpeechBubble "Padding fits text." (UP+LEFT)  
- Mini RoadmapStrip at bottom, current_part=2
- Verify: no overlap, readable on white, bubbles hug text
- FadeOut all at end

Run: manim -ql drivex_v2\scenes\_smoke_test.py SmokeTest
Pass = bubbles clearly fit their text tightly, no dark fills.
```

---

## PROMPT 1 — Intro scenes (I-01, I-02, I-03)

```
Project: Beyond Self-Driving Manim tutorial, drivex_v2/
All components exist in drivex_v2/components/ (white theme, TightBubble etc.)
Render check: manim -ql drivex_v2\scenes\intro\<file>.py <Class>

DESIGN RULES (all scenes):
- White BG except I-02 (navy ok for emotional hook)
- English on screen; min font 22; COL_NAVY text
- TightBubble for mascot speech; one bubble at a time
- FadeOut everything at scene end

==== I-01: drivex_v2/scenes/intro/i01_title_card.py ====
Class I01TitleCard(Scene) — duration ~30s
BG: navy (part card feel for the series opener)
Layout (top→bottom):
  "Beyond Self-Driving" — GOLD bold 52, center
  "ICCV 2025 Tutorial — Team Summary" — COL_WHITE 24
  "[Presenter Name] · UCLA" — LIGHT_BLUE 20
  "UCLA Mobility Lab" — COL_WHITE 18 opacity 0.7
  horizontal divider line — COL_BLUE
  "For questions: contact UCLA Mobility Lab" — COL_WHITE 15 opacity 0.6
  CAR mascot bottom-right, idle_bounce
Animation: Write title → FadeIn subtitle → FadeIn names → Create divider → FadeIn contact → FadeIn CAR
End: FadeOut all.

==== I-02: drivex_v2/scenes/intro/i02_hook.py ====
Class I02Hook(Scene) — duration ~75s
BG: navy (emotional scene)
Three sub-scenes:
  A) Single car center-left, radar sweep arcs (3 expanding arcs), 5 detection dots,
     GPT+VLM small labels near car, TightBubble "There is a human over there. → Turn left."
  B) Wall slides in right; radar arcs truncated; red blind-zone polygon
     FadeOut detection dots, GPT/VLM labels, thought bubble BEFORE wall appears
  C) FadeOut blind zone+blocked radar; 2 green cars appear;
     comm arcs between cars (ArcBetweenPoints); wall fades to opacity 0.2;
     hidden green dot appears; Text "I see." near original car
Payoff: FadeOut scene objects → gold divider + "So we taught them to cooperate." (GOLD bold 36)
KEY FIX: FadeOut fm1(GPT) and fm2(VLM) labels before writing "I see." — they overlap.
End: FadeOut divider+payoff.

==== I-03: drivex_v2/scenes/intro/i03_roadmap.py ====
Class I03Roadmap(Scene) — duration ~30s
BG: WHITE (first body scene)
Header "The 5-Part Journey" — COL_NAVY bold 30
Full RoadmapStrip (mini=False, spine_width=10.5) — centered, shifted DOWN 0.3
Labels (zigzag) allowed here since whole canvas is dedicated.
Part titles:
  1: "Foundation\nModels"
  2: "Cooperative\nV2X"
  3: "Sim-to-Real"
  4: "Efficiency\n& V2X"
  5: "Physical AI"
Animation: header → build_animation() → all 5 nodes pulse → node 1 turns GOLD
End: FadeOut all.
```

---

## PROMPT 2 — Part 1 scenes A (P01-S01 to P01-S04)

```
Project: Beyond Self-Driving Manim tutorial, drivex_v2/
Components done. Intro done.
Source narrative: materials/scripts/script_part1.md (slides 1–6)
Render check: manim -ql drivex_v2\scenes\part01\<file>.py <Class>

DESIGN RULES: white BG, English, COL_NAVY text, TightBubble, axes before data, clean end.

==== P01-S01: p01_s01_opening.py — Class P01S01Opening (~30s) ====
White BG. Header area (top 40% of canvas):
  "In 2025, AI can write code," — COL_NAVY 28
  "draw pictures, answer everything…" — COL_NAVY 28
  "Why can't self-driving cars drive everywhere yet?" — COL_GOLD 30 bold
PI mascot bottom-right (height=1.0), shifted DOWN enough so bubble doesn't hit text.
PIBubble position=UP+LEFT, text: "That's our question for the next 10 minutes."
ONE bubble, ONE position. No second bubble.
Animation: Write line1 → Write line2 → Write emphasis → FadeIn PI → pop bubble →
  wait 1.5s → FadeOut all.

==== P01-S02: p01_s02_genai_boom.py — Class P01S02GenAIBoom (~75s) ====
White BG. Two acts.
ACT 1 — GenAI explosion:
  Header "GenAI is everywhere"
  5 capability cards in a row (arrange RIGHT buff=0.5), each width=2.2 height=0.9:
    "Code", "Images", "Video", "Reasoning", "Multimodal"
  Each card: COL_DEEP_BLUE fill, COL_BLUE stroke 1.5pt, COL_NAVY text 18
  "What do they have in common?" — italic COL_NAVY below cards
  FadeOut Act 1.
ACT 2 — Foundation Models:
  Header "Foundation Models" — COL_GOLD bold 28
  Quote (italic): '"trained on broad data, adaptable to many downstream tasks" — Stanford CRFM'
  Diagram (horizontal): [data: text/images/speech/3D] → Arrow → [FOUNDATION MODEL box] → Arrow → [tasks column]
  Arrows must be straight Arrow(box.get_right(), next.get_left(), buff=0.05)
  Arrows AFTER boxes appear (not before)
  PI bubble top-right corner: "Why not for autonomous driving?" — pop, wait 1.5s, fade
  KEY FIX: PI bubble must not overlap the diagram. Position PI at RIGHT*5+DOWN*2 (corner).
  FadeOut all.

==== P01-S03: p01_s03_av_arch.py — Class P01S03AVArch (~75s) ====
White BG. Header "Three AV Architectures"
Three rows (each reveals sequentially, then brief caption appears and fades):
  Modular: [Perception]→[Localize]→[Predict]→[Plan]→[Control]
    Caption: "Error accumulates; each module frozen"
  End-to-End: [Sensors] ──────────────────→ [Action]
    Caption: "Joint optimization; black-box safety"
  Hybrid: [Perception ML]→[Planning ML]→[Control classical]
    Caption: "Most deployed; pragmatic balance"
After all 3: "All three share one weakness Foundation Models will expose." — COL_GOLD italic
Use _block() helper for uniform width=1.6 height=0.9 blocks.
FadeOut all.

==== P01-S04: p01_s04_longtail.py — Class P01S04LongTail (~80s) ====
White BG. Header "The Long-Tail Problem"
CRITICAL ORDER:
  1. Create Axes (x="driving situations", y="frequency") FIRST
  2. Plot long-tail distribution curve on axes (power-law decay, left-peak)
  3. Add "99%" label on left hump; "1%" label far right tail
  4. 3 hero images (SlideImage placeholders if no file):
       "phone-in-road person", "traffic-light truck", "snowy road"
     below the chart, 3 columns
  5. Distribution group (axes+curve+labels) .animate.scale(0.55).to_edge(UP) — shrink UP
  6. Wait for shrink to finish
  7. PI mascot bottom-left, CAR mascot bottom-right appear
  8. PI bubble: "How do humans handle this?"
  9. Wait 1.2s, FadeOut PI bubble
  10. CAR bubble: "Common-sense reasoning."
  11. Wait 1.2s, FadeOut CAR bubble
  12. Write "We need common-sense and generalist experience." — COL_GOLD
  13. FadeOut all
DO NOT show mascots while distribution is centered. DO NOT draw axes after distribution.
```

---

## PROMPT 3 — Part 1 scenes B (P01-S05 to P01-S09)

```
Project: Beyond Self-Driving Manim tutorial, drivex_v2/
Source narrative: materials/scripts/script_part1.md (slides 7–23)
Render check: manim -ql drivex_v2\scenes\part01\<file>.py <Class>

DESIGN RULES: white BG, English, COL_NAVY text, TightBubble, clean end.

==== P01-S05: p01_s05_fm_empower.py — Class P01S05FMEmpower (~70s) ====
White BG (FIX: old version had navy BG — must be white).
Header "Foundation Models empower Autonomous Driving"
Left column (5 boxes, arrange DOWN buff=0.25, width=2.6 min):
  "Vision FM\n(SAM / DINO / CLIP)"
  "Video Gen\n(Cosmos / Wan)"
  "Vector Space\n(MotionLM)"
  "LLM\n(GPT etc.)"
  "Multimodal LM\n(Gemma3 / QwenVL)"  ← must be wide enough for this text
Right column (6 boxes, width=2.4):
  "Auto-Labeling", "Scenario Gen", "Sensor Sim", "Vehicle Interface", "Reasoning", "E2E Stacks"
Center: Arrow LEFT→RIGHT labeled "Empower" — COL_BLUE bold
Bottom: "Goal: Long-tail Generalization & Generalist Experience" — COL_GOLD bold
FadeIn left col → FadeIn right col → GrowArrow center → Write bottom goal.
FadeOut all.

==== P01-S06: p01_s06_vla_roadmap.py — Class P01S06VLARoadmap (~80s) ====
White BG. Two acts.
ACT 1 — 4 strategies (arrange DOWN):
  "Text Action output — e.g. GPT-Driver"
  "Numerical Action output — e.g. DriveGPT4"
  "Explicit Guidance — e.g. DriveLM graph"
  "Implicit Transfer — latent representations"
FadeOut Act 1.
ACT 2 — Quote + DriveLM chain + datasets:
  Quote (italic, COL_GOLD, width=8u RoundedRect box, LIGHT_BLUE fill):
    "Language is not just input — it is the interface for contextual understanding and reasoning."
  Quote box appears → hold 1.5s → shifts UP smaller
  DriveLM chain — 4 nodes horizontal:
    "I see…" → "I predict…" → "I should…" → "trajectory"
  Nodes: each appears with label BELOW (buff=0.45), hold 0.8s, label FADES before next node
  3 dataset cards below chain: "DriveLM / graph QA", "CoVLA / 80h video", "Impromptu VLA / 80K clips"
END CLEANUP: FadeOut EVERYTHING — no replay. Common bug in old version: things reappear at end.

==== P01-S07: p01_s07_vla_arch.py — Class P01S07VLAArch (~120s) ====
White BG. Header "Four VLA Architectures"
Use _block(text, w=1.8, h=0.9) helper for ALL pipeline blocks.
GPT-Driver row: [Text desc] → [GPT-3.5] → [Action]
  arrows must reach box edges (buff=0.05), not short
BEVDriver row: [LiDAR+Cam] → [BEV] → [Q-Former] → [LLM] → [Waypoints]
  ALL blocks same height — arrange(RIGHT, buff=0.5) — no inline BEV image
EMMA row: [Camera] → [Gemini] → [CoT+Traj+Perception+RoadGraph]
DriveVLM row (dual): Two parallel sub-rows:
  top: [VLM — slow, scene+plan] ─┐
  bottom: [3D Perception — fast] ─┴→ [merge] → output
After all 4: "Language at the center of every architecture." — COL_GOLD italic
FadeOut all.

==== P01-S08: p01_s08_autovla.py — Class P01S08AutoVLA (~110s) ====
White BG. Header "AutoVLA — UCLA"
ACT A — Architecture (keep in UPPER half of canvas):
  "Simple scene → [VLM] → Fast: action only"
  "Complex scene → [VLM] → Slow: CoT + action"
  Switch-logic box: "scene complexity → mode choice"
  Keep all of Act A in y > 0 (upper screen).
ACT B — Training (LOWER half, clearly separated):
  Stage 1 box left: "SFT — teach both modes"
  Arrow →
  Stage 2 box right: "RFT (GRPO) — verified rewards"
  Result line: "+10.6% planning · −66.8% runtime" — COL_GOLD bold
END CLEANUP: FadeOut EVERY mobject — including stage1 label, stage2 label, result line.
Old bug: stage labels remained on screen at end.

==== P01-S09: p01_s09_takeaways.py — Class P01S09Takeaways (~60s) ====
White BG. Header "Part 1 Takeaways"
4 takeaway cards in 2×2 grid, each width=4.5 height=1.8, buff=0.6:
  "Long-tail generalization — FMs unlock edge-case reasoning"
  "MLLMs scale AV — out-of-domain generalization"
  "Diverse architectures — dual-system, E2E, BEV, RL fine-tuning"
  "Open issues — safety, latency, data scarcity"
Hold 2s → FadeOut cards.
4 future direction bullets:
  "• Post-training with RL + simulation"
  "• Unified multimodal backbone"
  "• Efficient VLA for low-latency control"
  "• Continual learning from real-world"
Bridge line: "Single-agent, even with FMs, has one blind spot…" — COL_GOLD italic
FadeOut all.
```

---

## PROMPT 4 — Part 2 scenes A (P02-S01 to P02-S06)

```
Project: Beyond Self-Driving Manim tutorial, drivex_v2/
Source narrative: materials/scripts/script_part2.md
Render check: manim -ql drivex_v2\scenes\part02\<file>.py <Class>

DESIGN RULES: white BG (except S01 which is navy title card), English, clean end, no overlap.

==== P02-S01: p02_s01_title.py — Class P02S01Title (~30s) ====
BG: BG_PART_TITLE (navy). White→navy transition at start; navy→white at end.
"Part 02" supertitle — GOLD small 20
"Towards End-to-End\nCooperative Automation" — GOLD bold 32
"Zewei Zhou, UCLA Mobility Lab" — LIGHT_BLUE 18
Quote: "Single agent, no matter how smart, is limited by its own line of sight." — italic GOLD 20
Mini RoadmapStrip (mini=True, dots only), current_part=2, node 2 = GOLD.
FadeOut all → white BG.

==== P02-S02: p02_s02_background.py — Class P02S02Background (~50s) ====
White BG.
Counter: "1,190,000 deaths / year worldwide" — animate ValueTracker 0→1190000
"94% from human error" — COL_RED bold
Human-error grid: ~94% red squares, 6% gold squares (use small Squares in VGroup)
Waymo reduction animation:
  Grid stays visible. Animate grid.animate.scale(0.2) + .set_color(ORANGE)
  Brace(small_grid, direction=RIGHT) with label "80% reduction" to the RIGHT of grid
  DO NOT add a separate box that overlaps the grid.
  DO NOT add a bottom note under the grid.
Delivery robots: "Robots are reshaping delivery too" + 3 small icon labels
FadeOut all.

==== P02-S03: p02_s03_evolution.py — Class P02S03Evolution (~50s) ====
White BG. Header "From Modular to End-to-End"
Brief modular→E2E comparison (2 mini rows), then FadeOut.
Timeline: horizontal Line, 4 year markers (2020, 2022, 2023, 2024)
4 milestones, each:
  Dot on timeline → Name (above or below, NOT zigzag — all above) → sub-label BELOW name
  Sub-label holds 1s then FADES before next dot appears
  PnPNet: "CNN+LSTM, joint perc+pred"
  GameFormer: "interactive prediction in planning"
  UniAD: "query-based, joint optimization"
  DiffusionDrive: "anchored diffusion trajectory"
After 4: "Each added what the previous lacked." — italic
NO in-scene roadmap strip (body scene rule).
END: explicit FadeOut all. No replay (old bug).

==== P02-S04: p02_s04_occlusion.py — Class P02S04Occlusion (~60s) ====
White BG. Header "The Limit: Occlusion"
Single car center. LiDAR sweep: use always_redraw updater with expanding ring
  (Circle radius driven by ValueTracker 0→2.0, run_time=1.5)
Static obstacles (2 Rectangles) block parts of sweep.
Red shaded polygons = blind zones behind obstacles.
PI bubble: "Why is this red?" → hold 1.2s → FadeOut bubble.
Two extra cars FadeIn from sides.
Their sweeps expand similarly.
FIX: use ReplacementTransform(red_zone_group, green_zone_group) — same shapes, green fill.
  Do NOT hide red and then show green separately (timing bug in old version).
"Cooperation is a physics solution, not an algorithm one." — COL_GOLD
FadeOut all.

==== P02-S05: p02_s05_related_works.py — Class P02S05RelatedWorks (~70s) ====
White BG. Header "Cooperative Perception — Chain of Progress"
4 method boxes arrange(RIGHT, buff=0.6), each width=1.8 height=1.2 (taller for 2-line label):
  "V2VNet\n(GNN fusion)" · "V2X-ViT\n(Transformer)" · "Where2comm\n(sparse comm)" · "CodeFilling\n(codebook)"
Reveal ONE at a time:
  FadeIn box → Write name → Write what-it-adds sub-label (BELOW box, buff=0.4) → hold 0.8s → FadeOut sub-label → GrowArrow to next
After 4: "Each addressed what the previous one missed." — italic below
Labels ALL above the boxes OR all below — NOT zigzag.
Dataset row (clearly separated, below chain, buff=0.8):
  "OPV2V (sim, ECCV 2022)" → Arrow → "V2X-Real (real-world, ECCV 2024)"
FadeOut all.

==== P02-S06: p02_s06_three_questions.py — Class P02S06ThreeQuestions (~30s) ====
White BG. Header "Three Research Questions"
Center-left: single agent icon (simple car VGroup)
Three SEPARATE arrows forking RIGHT from agent:
  Arrow 1 (UP-RIGHT): "What to transmit?"
  Arrow 2 (RIGHT): "When to transmit?"
  Arrow 3 (DOWN-RIGHT): "How to fuse?"
All three arrows → converge label: "→ V2XPnP answers these"
LaggedStart(GrowArrow x3, lag_ratio=0.3)
FadeOut all.
```

---

## PROMPT 5 — Part 2 scenes B (P02-S07 to P02-S12)

```
Project: Beyond Self-Driving Manim tutorial, drivex_v2/
Source narrative: materials/scripts/script_part2.md (slides 10–28)
Render check: manim -ql drivex_v2\scenes\part02\<file>.py <Class>

DESIGN RULES: white BG, English, clean end, no overlap.

==== P02-S07: p02_s07_v2xpnp.py — Class P02S07V2XPnP (~120s) ====
White BG. Header "V2XPnP — What / When / How"
ACT 1 "What": 3 fusion strategies briefly shown (3 small cards):
  "Early fusion (raw LiDAR)" · "Intermediate (BEV features)" · "Late (bboxes)"
  All have temporal dimension → small clock icon or "+time" badge on each
FadeOut Act 1.
ACT 2 "When": Vehicle-distance illustration. "One-step: transmit full history when close."
  Temporal attention box compresses history → small output.
FadeOut Act 2.
ACT 3 "How" — SERPENTINE LAYOUT (key fix):
  Row 1 (top): [Agent1 history] → [Temporal Attn 1]
               [Agent2 history] → [Temporal Attn 2]
  Both Temporal Attn outputs → [Spatial Attn] (centered between them horizontally)
  Spatial Attn center_x = (temporal1.get_x() + temporal2.get_x()) / 2
  Arrow from Spatial Attn goes DOWN (not right) to:
  [Multi-agent Spatio-temporal Representation]
  From that box: arrow DOWN-LEFT → [Detection], arrow DOWN-RIGHT → [Prediction]
  All arrows: Arrow(a.get_right()/get_bottom(), b.get_left()/get_top(), buff=0.05)
Result: "Spatio-temporal fusion — one end-to-end framework"
Mention: V2XPnP-Seq dataset (one line only; detail in next scene)
FadeOut all.

==== P02-S08: p02_s08_dataset.py — Class P02S08Dataset (~30s) ====
White BG. Header "V2XPnP-Seq Dataset"
4 stat cards (2×2 grid), each animate a counter:
  "2 vehicles + 2 infra nodes" · "40,000 LiDAR frames"
  "208,000 camera frames" · "All V2X modes: V2V, V2I, V2X, I2I"
"HD maps + trajectories included" badge below.
"First real-world dataset covering all collaboration modes." — COL_GOLD italic
FadeOut all.

==== P02-S09: p02_s09_turbotrain.py — Class P02S09TurboTrain (~70s) ====
White BG. Header "TurboTrain — Efficient Multi-task Training"
LEFT side (60% width): Axes chart
  x="AP@0.5 (detection)", y="EPA (prediction)"
  Draw axes FIRST.
  Orange dots cluster low-left: "One-time training (fail)" — label near dots cluster, NOT near pipeline
  Blue dots progression upper-right: "Manual 4-stage (120 epochs)" — label near dots
  Green star top-right: "TurboTrain (45 epochs)" — highlighted
RIGHT side (40% width): 2-stage pipeline
  Stage 1 box: "Pretrain\nMasked LiDAR recon\n→ task-agnostic 4D repr"
  Arrow DOWN
  Stage 2 box: "Hybrid training\n[green arrow] Free gradient\n[red arrow] Conflict-suppress\n(alternating)"
  Stage 2 internal: show 2 green arrows (free) then 2 red arrows (suppress) explicitly labeled
Result below pipeline: "120 → 45 epochs · No manual stage-switching"
FadeOut all.

==== P02-S10: p02_s10_riskmap.py — Class P02S10RiskMap (~70s) ====
White BG. Header "RiskMap — Interpretable Planning"
Three paradigm rows (each revealed, captioned briefly, caption fades):
  (a) Modular: [Perc]→[Loc]→[Pred]→[Plan]→[Ctrl]  "error accumulates"
  (b) E2E: [Sensors]→[black box]→[Action]  "uninterpretable"
  (c) Proposed: [Sensors]→[Perception]→[Risk Map]→[MPC]→[Trajectory]
      Sub-label for Risk Map: "explicit spatiotemporal risk distribution"
      Sub-label for MPC: "verifiable, constrainable"
Axis ticks for any chart: BELOW the axis line (not above — old bug).
Module blocks: shifted RIGHT to avoid text overlap.
"RiskMap outperforms SOTA on detection, prediction, and planning." — COL_GOLD
FadeOut all.

==== P02-S11: p02_s11_summary.py — Class P02S11Summary (~30s) ====
White BG. Header "Part 2 Summary"
3 rows with arrows:
  "Build framework + dataset" → "V2XPnP"
  "Train efficiently" → "TurboTrain"
  "Plan interpretably" → "RiskMap"
Subtitle: "Cooperative perception, end-to-end." — COL_GOLD
FadeOut all.

==== P02-S12: p02_s12_bridge.py — Class P02S12Bridge (~30s) ====
White BG → navy at end.
Two boxes side by side:
  Left "Theory" box (COL_DEEP_BLUE fill): V2XPnP, TurboTrain, RiskMap
  Right "Reality" box (COL_DEEP_GREEN fill): Hardware, Calibration, Real data
Arrow left→right.
PI mascot bottom. PIBubble: "Where does the data come from?" — pop, hold 1.5s, FADE bubble.
Right "Reality" box gets gold border highlight.
FadeOut all elements → BG transitions to navy (for next Part 3 title card).
```

---

## PROMPT 6 — Part 3 scenes (P03-S01 to P03-S07)

```
Project: Beyond Self-Driving Manim tutorial, drivex_v2/
Source narrative: materials/scripts/script_part3.md
Render check: manim -ql drivex_v2\scenes\part03\<file>.py <Class>

DESIGN RULES: white BG (except S01 navy), English, clean end, no overlap.

==== P03-S01: p03_s01_title.py — Class P03S01Title (~30s) ====
BG: navy. Layout:
  "Part 03" — GOLD small
  "Bridging Simulation\nand Reality in V2X" — GOLD bold 32
  "Zhaoliang Zheng, UCLA Mobility Lab" — LIGHT_BLUE 18
  Quote: "Hardware, calibration, and a real intersection." — italic GOLD 20
  Tagline "Theory → Engineering" — GOLD 16, position BELOW the quote (not above presenter line)
  Mini roadmap strip (mini=True), node 3 = GOLD.
FadeOut → white.

==== P03-S02: p03_s02_four_pillars.py — Class P03S02FourPillars (~50s) ====
White BG. Header "Part 3 — Four Pillars"
4 pillar cards stacked VERTICALLY (arrange DOWN, buff=0.4), shifted LEFT (to_edge LEFT buff=0.5):
  "① Hardware & Data Collection"
  "② Mapping & Localization"
  "③ Late & Intermediate Fusion"
  "④ Digital Twin"
Each card: width=6, height=0.9, COL_DEEP_BLUE fill, COL_BLUE stroke.
Tagline RIGHT of cards: "Built in order — bottom up."
LaggedStart(FadeIn each card), then tagline.
FadeOut all.

==== P03-S03: p03_s03_smart_intersection.py — Class P03S03SmartIntersection (~70s) ====
White BG. Header "UCLA Smart Intersection"
Sub-header: "Charles E. Young Dr & Westwood Plaza, UCLA" — COL_NAVY 18 italic
Top-down map (simplified rectangles for roads + corner nodes):
  NW corner: yellow dot labeled "Infra Node NW"
  SE corner: yellow dot labeled "Infra Node SE"
  2 CAV dots on road: blue, labeled "CAV 1" "CAV 2"
Annotations VERTICALLY STACKED on LEFT side (not horizontal — old bug):
  "Infra nodes: LiDAR + cameras + radar/C-V2X"
  "CAVs: 4 stereo cams + LiDAR-128 + GNSS/IMU"
PI bubble: "Why so many sensors?" → pop, hold, FADE before next content.
Answer reveals: "Each fails in different conditions — redundancy is safety."
Sensor failure examples (brief, 3 small labels): camera/LiDAR/GNSS with their limits.
FadeOut all.

==== P03-S04: p03_s04_calibration_time.py — Class P03S04CalibrationTime (~60s) ====
White BG. Header "Time Calibration — Sync Across Agents"
Step 1: Draw road with lane markings (dashed lines) FIRST before car appears.
Step 2: Car drives in from left, stops at center.
Step 3: Ghost car (same shape, opacity 0.4) spawns at same position → moves RIGHT by 1u.
Step 4: Brace(ghost_car, original_car, direction=DOWN) + label "~1m"
Sub-label: "At 60 km/h, a 50 ms desync = ~83 cm position error"
Solution box (appears below): "GPS time reference + hardware trigger (not software)"
Note: software trigger → jitter.
FadeOut all.

==== P03-S05: p03_s05_calibration_space.py — Class P03S05CalibrationSpace (~70s) ====
White BG. Header "Space Calibration — Shared World Frame"
4 mini coordinate systems (each with 2 colored axes + 1 labeled point):
  Arrange in a row at TOP of canvas (y > 1.5), buff=1.0
"Extrinsic calibration" label + arrow pointing DOWN to:
Common world frame axes (larger, center-bottom of canvas).
5 aligned point pairs on world frame:
  For each pair: point_A (COL_BLUE) and point_B (COL_GREEN) slightly offset but visible
  "without calibration" → show misaligned (point_B shifts ~0.5u right)
  "with calibration" → Transform to aligned
Label: "Without calibration → ghost objects (same thing detected twice)"
Mini grid axes must NOT overlap "without calibration" text — mini axes at TOP is key fix.
FadeOut all.

==== P03-S06: p03_s06_data_collection.py — Class P03S06DataCollection (~50s) ====
White BG. Header "Data Collection — Systematic Routes"
Basic routes row (4 icons using Arrows/curves to show path shape):
  L-turn · Straight · R-turn · U-turn
  Label below each.
Combined route example: chain of 3 → animated path with MoveAlongPath
Time-of-day icons (4 small): Day · Dusk · Night · Rain
Datasets badge: "→ V2X-Real (ECCV 2024) · V2XPnP-Seq"
FadeOut all.

==== P03-S07: p03_s07_localization_why.py — Class P03S07LocalizationWhy (~50s) ====
White BG. Header "Why Localization Matters for Cooperation"
Three boxes converge on HD Map node (center):
  "Data Acquisition" (left-top) → Arrow → HD Map
  "Localization" (left-mid) → Arrow → HD Map
  "Digital Twin" (left-bot) → Arrow → HD Map
Failure mode illustration (below):
  Agent A sees object at (5,2): blue dot
  Agent B sees SAME object but bad localization puts it at (5.5,2): red dot
  Fused result = average between two → shown as gray dot between them, labeled "wrong"
  Caption: "Bad localization → fused result WORSE than single-agent"
FadeOut all.
```

---

## PROMPT 7 — Part 3 scenes B (P03-S08 to P03-S14)

```
Project: Beyond Self-Driving Manim tutorial, drivex_v2/
Source narrative: materials/scripts/script_part3.md (slides 29–end)
Render check: manim -ql drivex_v2\scenes\part03\<file>.py <Class>

DESIGN RULES: white BG, English, clean end, no overlap.

==== P03-S08: p03_s08_kalman_filter.py — Class P03S08KalmanFilter (~60s) ====
White BG. Header "Multi-rate Kalman Filter"
3 sensor source boxes on LEFT (arrange DOWN, buff=0.4):
  "GNSS — 5 Hz · absolute · blocked by buildings" (stroke COL_RED)
  "IMU + wheel speed — 100 Hz · drifts" (stroke COL_BLUE)
  "LiDAR map-match — 1 Hz · accurate · slow" (stroke COL_GREEN_DARK)
All three → Arrows → center KF box "Multi-rate Error-state KF\n(handles measurement delays)"
KF → Arrow → output box RIGHT: "100 Hz · lane-level pose"
FadeOut all.

==== P03-S09: p03_s09_cooper_fuse.py — Class P03S09CooperFuse (~70s) ====
White BG. Header "CooperFuse — Late Fusion Done Right"
Two agent detect-then-share flow briefly shown (simple).
NMS DEMO:
  Show bbox A (high confidence, wrong orientation — rotate it 30° from expected)
  Show bbox B (low confidence, correct orientation)
  NMS label: "picks A (higher confidence)" → red X on A's bbox
  ANIMATION FIX: bbox A visibly ROTATES 30° in wrong direction before NMS label appears.
    Use: bbox_a.animate.rotate(30*DEGREES)
CooperFuse panel: "Fuse using temporal BBX features (position, orientation, scale history)"
  Result: B's orientation wins.
"First real-time cooperative late fusion for V2X — IV 2024" — COL_GOLD
FadeOut all.

==== P03-S10: p03_s10_v2x_realo.py — Class P03S10V2XReaLO (~70s) ====
White BG. Header "V2X-ReaLO — Intermediate Fusion in Real V2X"
BEV feature grid (small 3×3 grid of colored squares) on LEFT.
Compress animation: grid.animate.scale(0.25) → small square (COL_BLUE filled block)
Compressed block moves UP onto center of a LARGE balance scale (VGroup of horizontal bar + two pans).
Scale wobbles (rotate(5*DEGREES) there_and_back, 2 cycles) then settles.
Label on scale: "0.5 MB / msg · 32× compression"
Trade-off chart (RIGHT of scale):
  Axes: x="bandwidth", y="accuracy" — axes FIRST
  Curve drawn (slightly concave down, showing diminishing returns)
  Gold dot at center of curve (NOT offset right — old bug)
  All arrows straight: Arrow(start, end, buff=0.05)
"First online intermediate fusion in real V2X — T-PAMI submission"
FadeOut all.

==== P03-S11: p03_s11_opencda_ros.py — Class P03S11OpenCDAROS (~50s) ====
White BG. Header "OpenCDA-ROS — Bridging Sim and Real"
Two columns (LEFT: Simulation, RIGHT: Real Vehicle), each has:
  Environment box (CARLA or UCLA intersection icon/placeholder)
  Arrow DOWN to ROS Bridge box
Two-headed arrow between ROS bridges (horizontal) labeled "same code"
Below both: "V2X comm · multi-agent sync · data streaming"
Arrows between columns must be on SEPARATE y-levels (arrange DOWN buff=0.5) — old bug was all arrows at same height.
"Code written for the vehicle runs in simulation without rewriting." — COL_GOLD italic
FadeOut all.

==== P03-S12: p03_s12_simboost.py — Class P03S12SimBoost (~60s) ====
White BG. Header "CDA-SimBoost — Closed Digital-Twin Loop"
4-node loop drawn clockwise:
  "Real Data (ROS)" → "Digital Twin (CARLA)" → "Challenging Scenarios" → "Train & Benchmark"
  Arrow from Train & Benchmark back to Real Data (completing the loop).
Each arrow: GrowArrow in sequence.
Center label inside loop: "Modular — swap any component"
"Expose model to edge cases not present in real data." — italic below
FadeOut all.

==== P03-S13: p03_s13_infrax.py — Class P03S13InfraX (~30s) ====
White BG. Header "OpenCDA-InfraX — Data Generation Platform"
4 feature bullets (LaggedStart FadeIn):
  "✓ Flexible sensor configuration"
  "✓ Multi-modality (LiDAR, camera, radar)"
  "✓ Weather variation (rain, fog, night, snow)"
  "✓ Vector maps included"
Tagline: "All-in-one for downstream model training." — COL_GOLD
FadeOut all.

==== P03-S14: p03_s14_bridge.py — Class P03S14Bridge (~30s) ====
White BG → navy at end.
3 bottleneck cards (FadeIn):
  "Data: annotation cost" · "Training: multi-task complexity" · "Inference: edge latency"
CAR mascot enters bottom. SpeechBubble: "Can we make this efficient enough to scale?"
  Hold 1.5s. FadeOut bubble FIRST.
Then FadeOut cards and mascot.
BG transitions to navy (for Part 4 title card).
```

---

## PROMPT 8 — Part 4 scenes (P04-S01 to P04-S10)

```
Project: Beyond Self-Driving Manim tutorial, drivex_v2/
Source narrative: materials/scripts/script_part4.md
Render check: manim -ql drivex_v2\scenes\part04\<file>.py <Class>

DESIGN RULES: white BG (except S01 navy), English, clean end, no overlap.

==== P04-S01: p04_s01_title.py — Class P04S01Title (~30s) ====
BG: navy. NO "data/training/inference" boxes on title card (old bug: overlapped everything).
Layout: "Part 04" · "From Pre-Training to Post-Training:\nBuilding Efficient V2X" · speaker · quote · mini roadmap node 4 GOLD.
FadeOut → white.

==== P04-S02: p04_s02_why_efficiency.py — Class P04S02WhyEfficiency (~40s) ====
White BG. Header "Three Efficiency Bottlenecks"
3 cards (arrange DOWN, each width=8, height=0.9):
  "Data: annotation costs scale with dataset size"
  "Training: multi-agent multi-task is unstable and slow"
  "Inference: edge devices have strict memory and latency budgets"
Mention US DoT smart intersection partnership (one italic line below).
FadeOut all.

==== P04-S03: p04_s03_annotation_cost.py — Class P04S03AnnotationCost (~45s) ====
White BG. Header "Annotation Cost Explosion"
Bar chart on LEFT (60% of canvas width):
  Axes FIRST: x=["V2V4Real", "DAIR-V2X", "V2X-Real"], y=annotations count
  3 bars grow up: 240K · 460K · 1,200,000
  Bars labeled with values (above each bar)
"5× in 2 years" annotation on RIGHT of chart (not overlapping bars).
Bullet points below annotation (RIGHT side):
  "• 3D annotation software complex"
  "• Trained annotators expensive"
  "• Multi-pass quality checks"
FadeOut all.

==== P04-S04: p04_s04_coopre.py — Class P04S04CooPre (~80s) ====
White BG. Header "CooPre — Self-Supervised Pretraining for V2X"
Agent A LiDAR cluster (dots) LEFT. Agent B LiDAR cluster RIGHT.
Arrows from both converge to BEV grid CENTERED between them:
  grid_map.move_to([(agent_a.get_x() + agent_b.get_x())/2, grid_map_y, 0])
30% of voxels randomly masked (gray squares overlaid on grid).
Reconstruction box below grid: "Fill in what I can't see using other agents' data"
"This teaches: when I can't see something, ask a neighbor." — italic
Result stat cards (3):
  "50% labels → matches 100% baseline performance"
  "+4% AP at full 100% data"
  "Cross-domain transfer works"
FadeOut all.

==== P04-S05: p04_s05_multi_task_conflict.py — Class P04S05MultiTaskConflict (~60s) ====
White BG. Header "Why Multi-task Training is Hard"
Problem 1 box (width=8 — wider than old version):
  "Multi-frame + Multi-agent + Multi-task → complex architecture → init-sensitive"
3D coordinate gradient visualization (isometric 2D or ThreeDAxes):
  Draw 3 axes
  Draw a tilted plane (Polygon representing weight space region)
  Two arrow vectors ON the plane pointing in nearly OPPOSITE directions:
    Arrow 1 (COL_BLUE): labeled "Detection ∇"
    Arrow 2 (COL_GREEN): labeled "Prediction ∇" — pointing ~120° from Arrow 1
  Caption: "Gradient conflict: improving one task degrades another"
FadeOut all.

==== P04-S06: p04_s06_turbotrain.py — Class P04S06TurboTrain (~70s) ====
White BG. Header "TurboTrain — Solving Training Cost"
Vertical pipeline (top to bottom):
  Stage 1 box (width=7, COL_DEEP_BLUE fill):
    "Stage 1 — Pretrain\nMasked LiDAR reconstruction (multi-agent, multi-frame)\n→ Task-agnostic 4D representation"
  Arrow DOWN
  Stage 2 box (width=7):
    "Stage 2 — Hybrid Training\nFree gradient steps ↔ Conflict-suppress steps"
    Show 2 small green arrows + 2 red arrows alternating inside box
Result: "120 → 45 epochs · No human stage-switching needed" — COL_GOLD bold
FadeOut all.

==== P04-S07: p04_s07_latency_chain.py — Class P04S07LatencyChain (~70s) ====
White BG. Header "Inference Latency Chain"
ACT 1 — Latency chain:
  3 blocks arrange(RIGHT, buff=1.2) — wider spacing so arrows visible:
    "Local inference\n80 ms" · "V2X comm\n50 ms" · "Fusion inference\n40 ms"
  Total time on NEW LINE below chain:
    "Total: ~170 ms budget"  ← NOT inline with blocks
ACT 2 — Cost comparison (replace Act 1):
  Two VERTICAL bar charts side by side (consistent orientation — old bug was mixed):
    Chart 1: "Arithmetic: FP32 multiplication" — tall red bar vs short green bar (INT8)
    Chart 2: "Memory: DRAM 640 pJ vs SRAM 5 pJ" — tall red vs short green
  Charts drawn at bottom half — use the empty lower space, make them taller.
FadeOut all.

==== P04-S08: p04_s08_quantv2x.py — Class P04S08QuantV2X (~70s) ====
White BG. Header "QuantV2X — Fully Quantized V2X"
3 bullet points at TOP-LEFT (y=2.5, x=-5):  ← positioned to NOT overlap mid-canvas
  "✓ Model-level: FP32 → INT8 (4× memory reduction)"
  "✓ Communication-level: BEV features → codebook (300× smaller)"
  "✓ First fully-quantized end-to-end V2X system"
Model section LEFT half:
  FP32 box (COL_FP32_RED fill, width=2.2) on LEFT
  INT8 box (COL_INT8_GREEN fill, width=1.1) appears to the RIGHT of FP32 — NOT on top
  Arrow FP32→INT8 with label "shrink 4×"
Communication section RIGHT half:
  FP32 features bar (tall, red) LEFT
  Codebook bar (tiny, green, 300× smaller) RIGHT — extreme visual disproportion
"First to quantize BOTH model AND communication simultaneously." — COL_GOLD italic
FadeOut all.

==== P04-S09: p04_s09_efficiency_summary.py — Class P04S09EfficiencySummary (~30s) ====
White BG. Header "Efficiency — Three Solutions"
3 rows:
  "Data bottleneck" → "CooPre (50% labels = 100% performance)"
  "Training bottleneck" → "TurboTrain (120 → 45 epochs)"
  "Inference bottleneck" → "QuantV2X (FP32+comm → INT8+codebook)"
Tagline: "Cooperative perception, ready for real deployment." — COL_GOLD
FadeOut all.

==== P04-S10: p04_s10_bridge.py — Class P04S10Bridge (~30s) ====
White BG → navy at end.
"Cars: solved." — COL_GREEN_DARK bold
4 bullet ticks aligned to SAME LEFT x-coord (x=-4):  ← all at same x
  "✓ Delivery robots"
  "✓ Quadrupeds & humanoids"
  "✓ Electric scooters & wheelchairs"
  "✓ Pedestrians (unpredictable)"
Small figure icons on RIGHT side (x=+2): 4 simple stick/geometric icons — NOT overlapping tick marks.
PI bubble: "What about everyone else?" — pop, hold 1.5s, fade.
FadeOut all → navy BG.
```

---

## PROMPT 9 — Part 5 scenes (P05-S01 to P05-S09)

```
Project: Beyond Self-Driving Manim tutorial, drivex_v2/
Source narrative: materials/scripts/script_part5.md
Reference spec: spec_prompts/spec_part05.md (detailed timing + visual IDs)
Render check: manim -ql drivex_v2\scenes\part05\<file>.py <Class>

DESIGN RULES: white BG (S01 navy, S08 ends navy), English, clean end, no overlap.

==== P05-S01: p05_s01_title.py — Class P05S01Title (~30s) ====
BG: navy. "Part 05" · "Building Scalable,\nHuman-Centric Physical AI" · "Wayne Wu, UCLA"
Quote: "Beyond cars — to any agent, any space." — italic GOLD
Mini roadmap: ALL 5 nodes light up GOLD simultaneously (first time in series).
  Animate: LaggedStart([node.animate.set_fill(GOLD) for node in nodes], lag_ratio=0.15)
FadeOut → white.

==== P05-S02: p05_s02_physai_vision.py — Class P05S02PhysAIVision (~70s) ====
White BG. Header "Physical AI — The Vision"
2×2 environment collage (4 RoundedRectangle placeholders):
  "Urban street" · "Indoor corridor" · "Campus path" · "Rough terrain"
LLM comparison (LEFT): "Internet (web-scale)" → LLM → "Language tasks"
Physical AI (RIGHT, PARALLEL): "???" → PhysAI → "Physical tasks"
Label above Physical AI input: "No equivalent data exists" — COL_RED
PI bubble: "Why can't we just do the same?" — pop, hold, fade.
Two barrier cards (COL_DANGER_FILL, COL_RED stroke):
  "Barrier 1: No web-scale robot behavior data"
  "Barrier 2: No human modeling in context"
Recipe box (COL_DEEP_GREEN, COL_GREEN_DARK stroke):
  "✓ Scene Simulation → Scalable"
  "✓ Human Modeling → Human-Centric"
FadeOut all.

==== P05-S03: p05_s03_micromobility.py — Class P05S03MicroMobility (~40s) ====
White BG. Header "60% of US Trips < 5 Miles"
Pie chart (AnnularSector): 60% COL_GOLD, 40% COL_GRAY_FILL.
"Micro-Mobility" label.
4 agent type icons (simple geometric shapes with labels):
  Delivery robot (rectangle on wheels) · Wheelchair (chair shape) · Scooter (simplified) · Humanoid (stick figure)
Top-down urban scene (roads + sidewalk rectangles as backdrop).
COCO Robotics card: "UCLA partner — real urban deployment"
Quote: "Not a test track. A real city." — COL_GOLD italic
FadeOut all.

==== P05-S04: p05_s04_metaurban.py — Class P05S04MetaUrban (~80s) ====
White BG. Three sub-acts.
ACT A — Quote + Procedural Gen:
  Write quote large, italic, COL_GOLD:
    '"The world is compositional, or there is a god." — Stuart Geman'
  Hold ≥ 1.5s — let it breathe.
  Quote shifts TOP-LEFT smaller.
  Description script box (monospace-style, COL_DEEP_BLUE fill):
    "blocks: 35  lanes: 6  sidewalk: wide  density: 0.4"
  Arrow → 3 generated mini-scene rectangles (different colored grid patterns)
  "∞ unique environments" — COL_GOLD
ACT B — Power-law chart:
  Axes FIRST (x="Number of unique layouts", y="Performance")
  Gray dashed linear reference line.
  Blue dashed logarithmic reference.
  COL_GOLD power-law curve (steep, dominant).
  Gold dot (100 diverse) HIGH on curve. Red dot (1000 repetitive) LOWER on linear line.
  "Diversity > Quantity" callout box (COL_DEEP_GREEN fill).
ACT C — UrbanVerse:
  [city-tour video placeholder] → Arrow "reconstruct" → [isometric 3D scene placeholder]
  "Realistic asset distribution — no human-design bias." — italic
FadeOut all.

==== P05-S05: p05_s05_urbansim.py — Class P05S05UrbanSim (~75s) ====
White BG. Three sub-acts.
ACT A — Bottleneck:
  "180 GPU days" — COL_FP32_RED size 36 bold
  CPU box LEFT ↔ GPU box RIGHT: 3 cycles of arrows going back and forth (GrowArrow → FadeOut × 3)
  Latency fill bar grows slowly across bottom: "GPU waits more than it computes"
ACT B — Solution:
  Single large GPU box (6u × 4u, COL_INT8_GREEN stroke)
  3 internal modules (smaller boxes inside): physics sim, observation, NN inference
  All connected with small green arrows INSIDE the box
  "No CPU-GPU transfer" badge outside box
  4×4 mini-tile grid (16 tiles, different colors): "256 async environments"
ACT C — Results:
  Speed stat: "2,620 FPS · 256 environments · 11.2 GB VRAM (<25%)"
  Time comparison bars (both vertical, same scale):
    "180 GPU days" bar → extends far RIGHT with ">>" label (almost off screen)
    "3 hours" bar → tiny sliver
  Deploy line: "PPO-UrbanVerse outperforms S2E, CityWalker, NoMaD" — COL_GOLD
FadeOut all.

==== P05-S06: p05_s06_citywalker.py — Class P05S06CityWalker (~100s) ====
White BG. Three sub-acts.
ACT A — Zombie city:
  "Zombie City" — COL_RED bold 28
  Top-down street layout.
  5 stick-figure pedestrians: all move in straight lines (MoveAlongPath with Line paths)
  One figure walks through a Rectangle wall — no collision response.
  "No context awareness" label.
  AMASS reference: "Motion capture: studio isolation, no environment." — small italic
ACT B — CityWalker stats:
  "CityWalker" — COL_GOLD bold 26
  4 stat cards (counter-up): 30.8h · 120,914 ped · 16,215 scenes · 227 cities
  Behavior icons: phone user · stroller · looking sideways · pausing
  "Real behavior. Real context." — COL_INT8_GREEN italic
ACT C — PedGen:
  "PedGen — Diffusion Model for Pedestrian Motion"
  Central skeleton figure (connected Lines as stick figure).
  3 input arrows:
    Scene context (voxel grid VGroup) → left arrow into skeleton
    Body context (SMPL outline simplified) → top-left arrow
    Goal (Dot + dashed path) → top-right arrow
  Output: curved ParametricFunction path navigating AROUND a Rectangle obstacle.
  3 loss cards horizontal (MathTex): L_rec · L_traj · L_geo
    With sub-labels: "anatomical" · "path direction" · "joints 3D"
  Comparison: left panel (without context, path through wall) vs right panel (with, path around).
FadeOut all.

==== P05-S07: p05_s07_vid2sim.py — Class P05S07Vid2Sim (~55s) ====
White BG. Header "Vid2Sim — Reality into Simulation"
Input: "Real World Video" placeholder Rectangle LEFT.
Arrow "convert →".
Output region RIGHT: two layers VERTICALLY SEPARATED (not overlapping):
  Top: "3D Gaussian Splatting" rectangle (COL_BLUE stroke) — y = +0.8
    Label "Photorealistic appearance" — above this rectangle
  Bottom: "Mesh Reconstruction" rectangle (COL_MESH_GRAY stroke) — y = -0.8
    Label "Physical interaction geometry" — below this rectangle
  Labels positioned ABOVE/BELOW their respective rectangles, not in center.
Combined label: "Appearance + Physics = Realistic Sim" — appears to side, NOT in center.
Sim-to-real gap:
  "Sim" box LEFT, "Real" box RIGHT, fixed positions.
  BEFORE: DoubleArrow between them (large gap — COL_FP32_RED)
  AFTER: same boxes but DoubleArrow transforms to much shorter one (COL_INT8_GREEN)
  Boxes MOVE CLOSER to each other during the transform.
  Text sizes: all ≥ 22pt.
FadeOut all.

==== P05-S08: p05_s08_finale.py — Class P05S08Finale (~75s) ====
★ Most important scene in the series ★
White BG → navy at end.
ACT A — 5-part recap:
  "Five parts. One story." — COL_NAVY bold
  5 mini-cards LaggedStart:
    "Part 1 · Foundation Models · long-tail generalization"
    "Part 2 · V2X Cooperation · spatiotemporal fusion"
    "Part 3 · Sim-to-Real · hardware + digital twin"
    "Part 4 · Efficiency · data, training, inference"
    "Part 5 · Physical AI · scalable + human-centric"
  4 arrows between cards. All 5 pulse once.
ACT B — Causal chain:
  Horizontal spine with 5 dots.
  4 curved arcs above spine connecting consecutive dots.
  Labels below arcs (LaggedStart): "long-tail→ cooperate" · "cooperate→ real data" · "real data→ efficient" · "efficient→ physical AI"
ACT C — Grand finale (navy BG):
  BG transitions to navy.
  Write "Beyond Self-Driving" — GOLD bold size 44, center.
  Gold divider line.
  "Building the full ecosystem for Physical AI" — GOLD italic 22.
  Populated city wide-shot — ALL agent types from all 5 parts:
    Cars (blue) · Infra nodes (yellow dots) · Delivery robots (teal) · Pedestrians (orange)
    Quadruped (teal, different shape) · Scooter (simplified) · Wheelchair
    Arrange in a believable top-down city layout — not random scatter.
  Communication web: CurvedArrow x6+ connecting agent types (dashed, COL_BLUE)
    Each agent type connected to ≥ 2 others.
  wait(3.0) ← INTENTIONAL. Let the audience breathe after 55 minutes.

==== P05-S09: p05_s09_credits.py — Class P05S09Credits (~20s) ====
BG: navy.
UCLA Mobility Lab (text header).
"ICCV 2025 Tutorial"
Speakers list (5 names, COL_WHITE 15):
  Dr. Zhiyu Huang · Zewei Zhou · Zhaoliang Zheng · Seth Z. Zhao · Wayne Wu
"Summary by [Team Name]" — COL_WHITE 16
"Made with Manim" — COL_WHITE opacity 0.5, bottom corner, 12pt
CAR mascot bottom-right: wave_animation().
Hold 3s. Fade to black.
```

---

## PROMPT 10 — Render scripts + final check

```
Project: Beyond Self-Driving Manim tutorial, drivex_v2/
All scenes implemented. Now create render scripts and do a final consistency pass.

==== CREATE drivex_v2/render/render_intro.ps1 ====
$scenes = @(
  @{file="scenes\intro\i01_title_card.py"; class="I01TitleCard"},
  @{file="scenes\intro\i02_hook.py"; class="I02Hook"},
  @{file="scenes\intro\i03_roadmap.py"; class="I03Roadmap"}
)
foreach ($s in $scenes) {
  manim -ql $s.file $s.class
}

==== Create similarly for render_part01.ps1 through render_part05.ps1 ====
(9 scenes for P01, 12 for P02, 14 for P03, 10 for P04, 9 for P05)

==== CREATE drivex_v2/render/render_all_final.ps1 ====
Runs all parts at -qh (1080p). Only run after user signs off on -ql.

==== CONSISTENCY CHECKLIST (run through every scene file) ====
For each .py in drivex_v2/scenes/:
  [ ] self.camera.background_color set correctly (white or navy)
  [ ] No hardcoded hex strings — all use constants from colors.py
  [ ] No sys.path.insert boilerplate
  [ ] Scene ends with FadeOut of all transient mobjects + wait(0.2)
  [ ] All Text uses font_size ≥ 22
  [ ] No COL_WHITE usage for fill on white BG (it now = #334155 = navy text color)
  [ ] All charts: axes created before data plotted
  [ ] No roadmap strip in body scenes (only in title cards and I-03)
  [ ] All bubble usages use TightBubble/PIBubble/SpeechBubble from components

Run: manim -ql drivex_v2\scenes\_smoke_test.py SmokeTest
     (should still pass — sanity check components not broken)

Deliver: list of any scene that needed more than 2 render iterations to pass visual check.
```
