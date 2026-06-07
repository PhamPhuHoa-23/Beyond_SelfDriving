# OPUS 4.7 SUPER PLANNING PROMPT
## Beyond Self-Driving — Complete Source Rebuild from Zero

> Đây là prompt dành riêng cho Claude Opus 4.7 trong chế độ Plan Mode.
> Nhiệm vụ: đọc toàn bộ context, rồi lập kế hoạch chi tiết cho package Manim mới hoàn toàn.
> KHÔNG viết code trong session này. Chỉ plan. Code sẽ được implement trong các session riêng theo từng part.

---

## 0. NHIỆM VỤ TỔNG QUAN

Bạn cần lập kế hoạch xây dựng lại **toàn bộ package hoạt hình Manim** cho tutorial ICCV 2025 "Beyond Self-Driving" của UCLA Mobility Lab.

Package cũ là `beyond/` — dark theme, 56 scenes, text-heavy, nhiều scenes nhồi nhét quá nhiều concept. Package đó **KHÔNG** bị xóa — giữ làm reference.

Package mới sẽ là **`studio/`** — xây từ zero theo triết lý hoàn toàn khác.

Yêu cầu thay đổi căn bản của người dùng:
- **Nền sáng** (light background, gần white/paper), không còn dark theme
- **Màu pastel** — soft, breathing, không chói
- **Font LaTeX** (CMU Serif hoặc Latin Modern Roman) — đẹp, học thuật, 3B1B feel
- **MarkupText đa màu** — một dòng chữ có thể nhiều màu khác nhau
- **Nhiều scene hơn** — tách mỗi concept thành scene riêng, đừng nhét
- **Visual-first** — mỗi scene phải có diagram/animation chủ đạo, không phải text list
- **Bám sát slide gốc** — nội dung phải đúng với `materials/slides/` và `materials/scripts/`
- **Reuse từ `Source_manim_reference/`** — đây là rule MANDATORY, MẠNH NHẤT
- **Script mới** — viết lại script tiếng Anh sạch, concise, phù hợp với visual mới

---

## 1. ĐỌC BẮT BUỘC TRƯỚC KHI PLAN (theo thứ tự)

### 1A. Nội dung gốc — nguồn sự thật

```
materials/scripts/script_part1.md    # Script tiếng Việt/Anh Part 1
materials/scripts/script_part2.md    # Script Part 2
materials/scripts/script_part3.md    # Script Part 3
materials/scripts/script_part4.md    # Script Part 4
materials/scripts/script_part5.md    # Script Part 5
materials/chat_plan.md               # Brainstorm ban đầu
materials/drivex_tutorial.md         # Extended notes
```

Slides PDF nằm tại `materials/slides/` — xem tên file để biết structure.

### 1B. Kiến trúc và design đã có

```
5_PART_GUIDE.md                          # Kịch bản điện ảnh — ĐỌC KỸ NHẤT
BEYOND_SELFDRIVING_ANIMATION_GUIDE.md    # Animation masterclass guide
MICRO_ANIMATION_BIBLE.md                 # Micro-animation recipes
ENHANCEMENT_PROMPT.md                    # Enhancement history
SOURCE_MANIM_REFERENCE_AUDIT.md          # Audit đã làm sẵn — QUAN TRỌNG
plans/00_MASTER_PLAN.md
plans/01_DESIGN_SYSTEM.md
plans/03_NARRATIVE_AUDIT.md
plans/09_FIX_CHECKLIST.md
```

### 1C. Code hiện tại — reference và anti-patterns

```
beyond/config.py
beyond/components/colors_dark.py
beyond/components/base_scene.py
beyond/components/animations.py
beyond/components/pipeline_block.py
beyond/components/__init__.py
```

Đọc đủ để hiểu architecture, KHÔNG copy dark-theme logic vào `studio/`.

### 1D. Source reference — MANDATORY READ

```
SOURCE_MANIM_REFERENCE_AUDIT.md    # Đã audit sẵn — đọc hết bảng này
```

Sau khi đọc audit, inspect trực tiếp những file có High-Priority mark:
```
Source_manim_reference/welchlabs_videos/_2026/vla/p31_61_1.py   # VLA reference
Source_manim_reference/3b1b_videos/_2024/transformers/network_flow.py
Source_manim_reference/3b1b_videos/_2026/hairy_ball/model3d.py
Source_manim_reference/welchlabs_videos/once_useful_constructs/light.py
Source_manim_reference/3b1b_videos/custom/logo.py
Source_manim_reference/3b1b_videos/_2026/spheres_talk/volumes.py
```

### 1E. Manim CE documentation

```
materials/manim_docs/mobjects.md
materials/manim_docs/animations.md
materials/manim_docs/text.md          # Đặc biệt quan trọng — MarkupText
materials/manim_docs/graphing.md
materials/manim_docs/three_d.md
```

---

## 2. DESIGN SYSTEM MỚI — `studio/` Package

### 2A. Background

```python
BG_PAPER   = "#FAFAF8"   # Warm white — default mọi scene
BG_CARD    = "#F0EEE8"   # Slightly darker — info panels
BG_SECTION = "#F5F3EF"   # Section divider panels
```

Part title cards vẫn có thể dùng màu tối nhẹ để tạo contrast, nhưng body scenes phải sáng.

### 2B. Bảng màu Pastel + Vivid accent

Palette mới phải vừa pastel (background fills, panels) vừa có vivid accents (mũi tên, labels, data points):

```python
# ── Nền / Fill nhạt (Pastel) ──────────────────────────────────────
PASTEL_BLUE   = "#C8DCFA"   # P1 Foundation — fill panels, zones
PASTEL_TEAL   = "#B0E8DA"   # P2 Cooperation
PASTEL_GREEN  = "#C8EDD0"   # P3 Sim-to-Real
PASTEL_AMBER  = "#FAE3B0"   # P4 Efficiency
PASTEL_PINK   = "#F9C8D8"   # P5 Physical AI

# ── Accent vivid (borders, highlights, key data) ──────────────────
ACCENT_BLUE   = "#2563EB"   # P1 accent
ACCENT_TEAL   = "#0891B2"   # P2 accent
ACCENT_GREEN  = "#16A34A"   # P3 accent
ACCENT_AMBER  = "#D97706"   # P4 accent
ACCENT_PINK   = "#DB2777"   # P5 accent

# ── Chữ ──────────────────────────────────────────────────────────
INK_DARK      = "#1E293B"   # Chữ chính — slate dark, không pure black
INK_MID       = "#475569"   # Chữ phụ
INK_LIGHT     = "#94A3B8"   # Caption, footnote

# ── Functional ───────────────────────────────────────────────────
GOLD_RICH     = "#D97706"   # Số liệu, key insight
RED_ERROR     = "#DC2626"   # Failure, bottleneck, before-fix
GREEN_FIX     = "#16A34A"   # Success, after-fix, gain
PURPLE_MODEL  = "#7C3AED"   # Neural net, model internals
ORANGE_INFRA  = "#EA580C"   # RSU, infrastructure

# ── Lines ────────────────────────────────────────────────────────
LINE_GRID     = "#E2E8F0"   # Background grid lines
LINE_SEP      = "#CBD5E1"   # Separator
LINE_ARROW    = "#475569"   # Default arrow color
```

### 2C. Typography

**Font chính**: `CMU Serif` — xác nhận đã installed tại README.
- Nếu `CMU Serif` render lỗi, fallback: `Latin Modern Roman`.
- KHÔNG dùng `Times New Roman` cho `studio/` — quá generic.

**Font code/mono**: `Courier New` hoặc `CMU Typewriter Text`

**MarkupText rule**: Bất cứ khi nào một dòng chữ cần phân biệt màu concept → dùng `MarkupText` với Pango markup:

```python
# Ví dụ multi-color trong 1 dòng
MarkupText(
    'Camera sees <span color="#0891B2">features</span> → '
    'LLM reasons → <span color="#D97706">action</span>',
    font="CMU Serif", font_size=24
)
```

### 2D. Canvas và Layout zones

```
Canvas: 14.22u × 8.0u  (giữ nguyên Manim default)

Title zone:    y > 2.8u   — tiêu đề scene + separator line
Content zone: -3.2u < y < 2.7u  — toàn bộ animation
Footer zone:   y < -3.2u  — số liệu nhỏ, footnote, takeaway

Left panel:   x < -1.5u   (khi dùng left/right split)
Right panel:  x > +1.5u
Center zone: -1.5u < x < 1.5u
```

**Rule**: Không bao giờ đặt text edge tại x > 6.5 hoặc x < -6.5.

### 2E. Scene structure chuẩn

```python
class StudioScene(Scene):
    PART_COLOR: str = ACCENT_BLUE   # Màu accent của part
    PART_NUM:   int = 1

    def setup(self):
        self.camera.background_color = BG_PAPER

    def construct(self):
        title = self._open("Scene Title Here")
        # ... animation ...
        self._close()

    def _open(self, text: str) -> VGroup:
        """Title + separator + part dot indicator."""
        ...

    def _close(self) -> None:
        """FadeOut everything cleanly."""
        ...
```

---

## 3. FONT SETUP INSTRUCTIONS (ghi vào plan)

Plan cần include bước cài font:

```powershell
# Kiểm tra CMU Serif đã có chưa
fc-list | grep -i "CMU"

# Nếu chưa, cài từ CTAN:
# Download: https://www.ctan.org/pkg/cm-unicode
# Extract → copy .otf files → C:\Windows\Fonts\
# Hoặc dùng Latin Modern (đã confirmed installed):
# FONT_PRIMARY = "Latin Modern Roman"
```

Plan phải xác định rõ: nếu CMU Serif available → dùng CMU Serif. Nếu không → Latin Modern Roman. KHÔNG fallback về Times New Roman.

---

## 4. RULE REUSE SOURCE_MANIM_REFERENCE (MANDATORY, STRONGEST RULE)

Đây là rule quan trọng nhất trong toàn bộ rebuild:

**Trước khi viết BẤT KỲ animation nào cho một scene, bắt buộc phải:**

1. Tra bảng `SOURCE_MANIM_REFERENCE_AUDIT.md` → tìm "Target Scenes" column → xem scene đó có reference nào không
2. Nếu có → đọc file reference đó → extract pattern/idiom → implement bằng Manim CE API
3. Nếu không có → vẫn phải tra "Visual Motifs Worth Stealing Conceptually" → tìm motif nào phù hợp nhất
4. Document trong code comment: `# Pattern adapted from: Source_manim_reference/path/to/file.py:line`

**Ưu tiên reuse theo loại:**

| Loại | Rule |
|---|---|
| Tiny pure helpers (color math, vector math) | Copy trực tiếp nếu self-contained |
| Animation patterns (không phụ thuộc manimlib) | Port sang Manim CE — không copy API |
| Layout idioms (grid, embedding rows, token tiles) | Implement lại bằng VGroup/arrange |
| Visual motifs (shells, trails, attention arcs) | Lấy ý tưởng, implement độc lập |
| Asset-dependent scenes (SVG, texture paths) | Không copy asset, reuse structure only |
| 3B1B logo/characters | Không copy branding |

---

## 5. SCENE ARCHITECTURE MỚI

### 5A. Triết lý tách scene

**Quy tắc vàng**: Mỗi scene = một câu hỏi + một câu trả lời visual.

Nếu một scene hiện tại trả lời 3 câu hỏi → tách thành 3 scenes.

Ví dụ: `p01_s03_av_arch.py` hiện tách 3 kiến trúc vào 1 scene → tách thành:
- `p01_s03a_modular.py` — Modular pipeline: pipeline visual, error cascade
- `p01_s03b_e2e.py` — End-to-end: black box với inputs/outputs, single optimization
- `p01_s03c_hybrid.py` — Hybrid: best of both worlds, trade-off visual

### 5B. Scene types mới

Mỗi scene thuộc một trong các loại sau — và phải được xây đúng theo loại đó:

```
TYPE_PROBLEM_FIRST    Hiển thị failure/bottleneck trước → rồi solution sau
TYPE_BEFORE_AFTER     Hai cột: trước/sau, có arrow transform ở giữa
TYPE_PIPELINE_FLOW    Block diagram với moving packets chạy qua
TYPE_TIMELINE         Timeline evolution với nodes animate lần lượt
TYPE_CHART_REVEAL     Axes build → data appear → annotation
TYPE_AGENT_SIM        City/intersection/map với moving agents + signals
TYPE_GALLERY_CARDS    Method cards với mini mechanism bên trong
TYPE_BRIDGE_RECAP     Bridge scene: bullets recap + forward question
TYPE_TITLE_CINEMATIC  Title card với assembly animation
TYPE_MATH_REVEAL      Equations hoặc matrices animate vào
TYPE_UNCERTAINTY_CLOUD Probability distributions, uncertainty fields
```

### 5C. Scene count estimate

```
Intro:   I01 I02 I03 I04           = 4 scenes
Part 1:  P01S01..P01S14 (estimate) ≈ 14 scenes
Part 2:  P02S01..P02S15 (estimate) ≈ 15 scenes
Part 3:  P03S01..P03S16 (estimate) ≈ 16 scenes
Part 4:  P04S01..P04S12 (estimate) ≈ 12 scenes
Part 5:  P05S01..P05S12 (estimate) ≈ 12 scenes

Total estimate: ~73 scenes (tăng từ 56)
```

---

## 6. DELIVERABLE CỦA PLANNING SESSION NÀY

Opus 4.7 phải output một kế hoạch có cấu trúc sau:

### 6A. Design System Document

File: `studio/DESIGN_SYSTEM.md`

Gồm:
- Bảng màu đầy đủ với hex values
- Font decision (CMU Serif vs LMR) + fallback logic
- MarkupText usage examples cho từng pattern thường gặp
- Layout zones diagram (ASCII art)
- Scene type definitions
- Component API spec (functions cần implement trong `studio/components/`)

### 6B. Scene Inventory Table

Format:

```
Scene ID | New Name | Type | Slide Ref | Script Ref | Visual Core | Reference Source | MarkupText Usage | Est. Duration
```

Phải có ít nhất 70 rows. Mỗi row phải fill đủ tất cả columns.

Ví dụ một row:
```
P01-S04a | p01_s04a_longtail_problem | TYPE_PROBLEM_FIRST | slides/part1 slide 6 | script_part1.md#slide6 | Long-tail curve với failure icons dọc theo tail + red zone | generalization/p8_15.py:long-tail curve pattern | "1% scenarios <red>100% accidents</red>" | 35s
```

### 6C. Component Architecture

Spec đầy đủ cho `studio/components/`:

```
studio/
├── __init__.py
├── config.py              # BG_PAPER, FONTS, quality settings
├── components/
│   ├── __init__.py        # Re-exports
│   ├── colors.py          # Pastel palette + accent colors
│   ├── base_scene.py      # StudioScene base class
│   ├── typography.py      # Text helpers, MarkupText builders
│   ├── pipeline.py        # pipeline_block, pipeline_row, pipeline_flow (với packets)
│   ├── charts.py          # axes_deploy, bar_reveal, curve_trace
│   ├── agents.py          # Vehicle, Pedestrian, RSU visual objects
│   ├── signals.py         # Radar shells, sensor cones, V2X links
│   ├── annotations.py     # Callout, thought bubble, contribution card
│   ├── animations.py      # scene_open, scene_close, micro-animations
│   └── layout.py          # Grid helpers, panel builders, zone management
```

Với mỗi component, plan phải specify:
- Function signature
- Parameters
- Return type
- Animation behavior
- Reference source nếu adapted từ `Source_manim_reference/`

### 6D. Script Update Plan

Với mỗi part, plan phải note:
- Những đoạn script hiện tại đang "drift" khỏi slide gốc → fix thế nào
- Những số liệu trong slide gốc chưa được script đề cập → thêm vào đâu
- Script mới cần viết bằng tiếng Anh cho voiceover → format đề xuất

### 6E. Implementation Roadmap

Chia thành các session coding riêng:

```
Session 1: studio/components/ — toàn bộ component package
Session 2: intro/ + Part 1 scenes
Session 3: Part 2 scenes
Session 4: Part 3 scenes
Session 5: Part 4 scenes
Session 6: Part 5 + finale
Session 7: Render all → fix bugs → final QA
```

Với mỗi session, plan phải specify:
- Scenes sẽ được code
- Dependencies giữa scenes
- Reference sources cần đọc trong session đó
- Estimated complexity (S/M/L/XL)

---

## 7. CONSTRAINTS KỸ THUẬT

### 7A. Anti-patterns cần tránh hoàn toàn

```python
# WRONG — hai .animate trên cùng object
self.play(mob.animate.scale(1.2), mob.animate.set_color(RED))

# WRONG — unicode glyph không render
Text("✓ done")  →  MarkupText('[OK] done', ...)
                    hoặc: Text("[OK] done", ...)

# WRONG — interpolate_color với hex strings
interpolate_color("#FF0000", "#0000FF", t)
# RIGHT:
ManimColor("#FF0000").interpolate(ManimColor("#0000FF"), t)

# WRONG — set_y với vector
mob.set_y(DOWN * 1.5)  →  mob.set_y(-1.5)

# WRONG — font_size dưới SIZE_MICRO
Text("tiny", font_size=9)

# WRONG — hardcode hex trong scene files
fill_color="#2563EB"  →  từ  from studio.components.colors import ACCENT_BLUE

# WRONG — không FadeOut khi kết scene
# RIGHT: self._close() fade toàn bộ

# WRONG — data chart trước axes
# RIGHT: self.play(axes_deploy(...)) TRƯỚC self.play(Create(bars))
```

### 7B. MarkupText rules

```python
# Dùng khi: 1 dòng cần 2+ màu khác nhau
MarkupText(
    'Foundation Model <span color="#0891B2">generalizes</span> → '
    '<span color="#D97706">fine-tune</span> per task',
    font="CMU Serif",
    font_size=24,
    color=INK_DARK,
)

# KHÔNG dùng MarkupText khi: chỉ 1 màu → dùng Text() thường
# KHÔNG dùng MarkupText cho equations → dùng MathTex()
# Không mix MarkupText và MathTex trong 1 VGroup ngang hàng
```

### 7C. Render commands

```powershell
# Standard 2D scene
manim -ql --disable_caching "studio/scenes/part01/p01_s01.py" ClassName

# 3D scene
manim -ql --renderer=opengl --disable_caching "studio/scenes/intro/i02.py" ClassName

# Python env
C:\Users\admin\miniconda3\python.exe   # base conda, KHÔNG dùng manim_env
```

### 7D. Frame check protocol

```python
# Sau mỗi render:
cap = cv2.VideoCapture(r'media/videos/scene_folder/480p15/ClassName.mp4')
dur = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
for t in [0.35, 0.60, 0.85]:
    cap.set(cv2.CAP_PROP_POS_MSEC, dur * t * 1000)
    ret, frame = cap.read()
    if ret: cv2.imwrite(f'check_{int(t*100)}.png', frame)
cap.release()
```

---

## 8. SCENE-BY-SCENE PLANNING TEMPLATE

Với mỗi scene trong inventory, Opus phải output block sau:

```markdown
## [SCENE ID] — [Scene Name]

**Type**: TYPE_PROBLEM_FIRST
**Duration**: ~40s
**Slide reference**: materials/slides/part1/slide_06.png
**Script reference**: script_part1.md — [Slide 6 — Long-tail Problem]

### Visual Core
[Describe rõ ràng cái người xem NHÌN THẤY gì — từng beat animation]
- Beat 1 (0–8s): ...
- Beat 2 (8–20s): ...
- Beat 3 (20–35s): ...
- Closing (35–40s): ...

### Reference Reuse
[Liệt kê pattern nào từ SOURCE_MANIM_REFERENCE_AUDIT.md sẽ được dùng]
- `welchlabs_videos/_2025/generalization/p8_15.py` — long-tail curve pattern → port sang CE Axes

### MarkupText Usage
[Liệt kê những dòng chữ cần multi-color]
- Title annotation: "1% of scenarios → <red>100%</red> of accidents"

### Key Number
[Con số nổi bật nhất của scene — hiển thị rõ, font_size lớn, màu GOLD_RICH]
- "1% of scenarios = 100% of fatal accidents"

### Components Needed
[Liệt kê components từ studio/components/ sẽ dùng]
- `charts.curve_trace()` — long-tail curve
- `annotations.failure_icon()` — icons dọc tail
- `signals.highlight_zone()` — red zone overlay

### Script (EN, voiceover ready)
[1–3 câu tiếng Anh clean, phù hợp voiceover tương lai]
"Autonomous driving fails most in rare scenarios — and rare doesn't mean safe.
Just 1 percent of situations cause almost all fatal accidents.
Foundation models can reason about context. But can they learn from what they've never seen?"

### Dependencies
- Cần: P01-S03c (Hybrid arch conclusion) đã render trước
- Output: Introduces "why FMs matter" → feeds into P01-S05
```

---

## 9. SPECIFIC DIRECTION PER PART

### INTRO (I01–I04)

- **I01 Title Card**: Particle assembly của tên "BEYOND SELF-DRIVING". 200 hạt từ trung tâm nổ ra → settle thành chữ vàng. Ref: `3b1b_videos/custom/logo.py:192 LogoGenerationFlurry`.
- **I02 The Hook**: Giữ nguyên 3D structure (OpenGL). Cải thiện radar shells (ref: `model3d.py:260 RadioBroadcast`), thêm occlusion shadow realer. Text overlay dùng MarkupText.
- **I03 Roadmap**: Orbital roadmap (5 parts quay quanh "Beyond Self-Driving" center). Ref: `3b1b_videos/custom/logo.py:216 LogoGenerationFivefold` — adapt 5 parts lighting up theo thứ tự.
- **I04 Bridge**: Bridge scene TYPE_BRIDGE_RECAP — 3 bullets + 1 forward question.

### PART 1 — Foundation Models (~14 scenes)

Key splits:
- `p01_s02` → split thành `p01_s02a` (GenAI boom timeline) + `p01_s02b` (FM definition visual)
- `p01_s03` → split 3 kiến trúc thành 3 scenes riêng (3a modular, 3b e2e, 3c hybrid)
- `p01_s07` → split theo 3 VLA architectures: 7a EMMA, 7b DriveVLM, 7c UniAD

Ref chính: `Source_manim_reference/welchlabs_videos/_2026/vla/p31_61_1.py` — embedding rows, attention arcs, action expert.

### PART 2 — Cooperative Perception (~15 scenes)

Key splits:
- `p02_s04` → giữ 3D OpenGL, improve RSU towers (ref: `model3d.py:68 RadioTower`)
- `p02_s05` → timeline riêng cho mỗi method với mini-mechanism card
- `p02_s07` → V2XPnP attention arcs — ref: `network_flow.py:161 play_simple_attention_animation`

### PART 3 — Sim-to-Real (~16 scenes)

Key splits:
- `p03_s04` → split: 4a temporal calibration + 4b spatial calibration
- `p03_s05` → Kalman filter với uncertainty cloud animation — ref: `3b1b_videos/_2018/uncertainty.py`
- `p03_s06` → CooperFuse với weighted fusion fields — ref: `welchlabs_videos/once_useful_constructs/region.py`

### PART 4 — Efficiency (~12 scenes)

Key splits:
- `p04_s04` → TurboTrain gradient conflict — ref: `welchlabs_videos/_2025/backprop_3/geometry_while_learning_2.py`
- `p04_s05` → QuantV2X compression visual — ref: `network_flow.py` block stack + squeeze motif
- `p04_s07` → Latency chain với packet pulses — ref: `wave_machine.py`

### PART 5 — Physical AI (~12 scenes)

Key splits:
- `p05_s03` → MetaUrban: tiling city procedural + diversity curve
- `p05_s05` → CityWalker + PedGen: split stats scene + zombie transform scene riêng
- `p05_s07` → Living city: keep 3D OpenGL, cải thiện agent choreography + signal shells
- `p05_s08` → Final montage: 5 parts converge → "A safer world."

---

## 10. OUTPUT FORMAT YÊU CẦU

Khi Opus 4.7 hoàn thành planning, output phải có các sections sau (theo thứ tự):

```
# STUDIO REBUILD PLAN

## 0. Executive Summary (5–10 câu)

## 1. Design System
  1.1 Color palette (full table)
  1.2 Typography decision
  1.3 MarkupText patterns
  1.4 Layout zones
  1.5 Scene type taxonomy

## 2. Component Architecture
  2.1 File structure
  2.2 API spec per component file

## 3. Full Scene Inventory (70+ rows, table format)

## 4. Scene Detail Blocks (1 block per scene, dùng template từ Section 8)

## 5. Script Update Notes per Part

## 6. Reference Reuse Map
   Source → Target Scene → Adaptation Notes

## 7. Implementation Sessions
   Session N: scenes, dependencies, complexity

## 8. Risk Log
   Known technical risks + mitigation
```

---

## 11. GHI CHÚ CUỐI

- Đây là planning session. Chỉ output plan dưới dạng Markdown structured document.
- KHÔNG viết code trong session này.
- KHÔNG tạo file mới trong session này (chỉ output text plan trong response).
- Nếu cần clarify bất kỳ điểm nào từ slides/scripts — note rõ "NEEDS CLARIFICATION" thay vì đoán mò.
- Plan phải đủ chi tiết để người khác có thể implement từng scene mà không cần hỏi thêm.
- Ưu tiên visual clarity hơn completeness — nếu 1 scene quá phức tạp → tách ra, đừng nhét.
- Mỗi scene phải có ít nhất 1 "khoảnh khắc đẹp" — thứ khiến người xem phải dừng lại và nói "wow".

**Câu hỏi để Opus tự hỏi về mỗi scene trước khi plan:**
1. Khán giả sẽ nhìn thấy GÌ ở giây thứ 5?
2. Animation nào khiến họ hiểu ngay mà không cần đọc chữ?
3. Con số nào của scene này khiến họ impressed?
4. Khoảnh khắc "wow" là khoảnh khắc nào?
5. Reference nào trong `Source_manim_reference/` gần nhất với vibe này?
