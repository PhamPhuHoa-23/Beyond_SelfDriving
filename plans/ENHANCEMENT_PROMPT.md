# PROMPT — Beyond Self-Driving: Scene Enhancement Pass

> Paste toàn bộ block này vào đầu phiên làm việc tiếp theo.
> Claude sẽ không có context — đây là tất cả những gì cần biết.

---

## 0. BỐI CẢNH DỰ ÁN

Bạn đang làm việc trên dự án **"Beyond Self-Driving"** — một animated tutorial video
theo phong cách 3Blue1Brown, tóm tắt 5 bài nói tại **ICCV 2025** của UCLA Mobility Lab.

**Working directory:** `c:\Users\admin\Downloads\ML\Lab01_3B1B\`

**Package chính:** `beyond/` — dark-theme Manim production package (đã commit lên git).

**Môi trường:**
- Manim Community v0.20.1
- Python: `C:\Users\admin\miniconda3\python.exe` (base conda — KHÔNG activate env khác)
- Shell: PowerShell (Windows 11)
- Render preview: `manim -ql "beyond/scenes/..." ClassName`
- Render final: `manim -qh ...` hoặc `python beyond/render_all.py -q qh`

---

## 1. ĐỌC TRƯỚC KHI LÀM BẤT CỨ THỨ GÌ

Đọc theo thứ tự này:

1. **`beyond/config.py`** — THEME = "dark", font config
2. **`beyond/components/colors_dark.py`** — bảng màu đầy đủ
3. **`beyond/components/animations.py`** — 30+ micro-animation recipes
4. **`beyond/components/base_scene.py`** — BeyondScene, PartTitleCard
5. **`5_PART_GUIDE.md`** — kịch bản sáng tạo đầy đủ (QUAN TRỌNG NHẤT)
6. **`BEYOND_SELFDRIVING_ANIMATION_GUIDE.md`** — spec kỹ thuật: màu sắc, 3D scenes, hiệu ứng
7. **`MICRO_ANIMATION_BIBLE.md`** — từng loại element phải animate như thế nào
8. **`materials/slides/`** — slide PDF gốc (dùng để cross-check nội dung)
9. **`materials/scripts/script_part*.md`** — transcript tiếng Việt của presenter

Không đọc code cũ trong `drivex/` — đó là bản reject.

---

## 2. TRẠNG THÁI HIỆN TẠI

Package `beyond/` đã có:
- **61 scene files** trải từ Intro (I01–I03) đến Part 5 (P5-S08)
- Dark theme (`BG_SPACE = "#090E1A"`)
- Tất cả import clean, render OK ở 480p15
- `beyond/render_all.py` — render toàn bộ + ffmpeg merge

Những gì đã tốt:
- Cấu trúc component sạch (colors, animations, base_scene)
- Timing hold times cơ bản đúng per guide
- Quote reveals dùng Write() thay FadeIn
- Mandatory hold times (3.0s cho "A safer world.", v.v.)

**Những gì CÒN YẾU và là mục tiêu của session này** — xem Section 3 bên dưới.

---

## 3. ENHANCEMENT OBJECTIVES — ĐÂY LÀ NHIỆM VỤ CHÍNH

### 3.1 FONT — Ngay bây giờ dùng "Latin Modern Roman"

Mục tiêu: Đổi sang **"CMU Serif"** cho tất cả các scene (đẹp hơn, gần 3B1B hơn).

Trước khi đổi: kiểm tra CMU Serif có được cài chưa bằng cách test render 1 scene nhỏ.
Nếu chưa có: hướng dẫn user install hoặc dùng fallback "DejaVu Serif".

File cần sửa: `beyond/config.py` → `FONT_PRIMARY = "CMU Serif"` (hoặc font tốt nhất có sẵn).
Sau đó verify `beyond/scenes/_smoke_test.py SmokeTest` render OK.

### 3.2 3D SCENES — Các cảnh phải dùng ThreeDScene

Theo `BEYOND_SELFDRIVING_ANIMATION_GUIDE.md §3.1`, các cảnh sau PHẢI dùng 3D:

**I-02 The Hook** (`beyond/scenes/intro/i02_the_hook.py`):
- Hiện tại: 2D BEV với circle rings
- Cần: `ThreeDScene`, phi=65°, theta=-45°, radar waves là **ellipsoid shells** thực sự 3D
- Camera tilt animation khi waves tỏa ra (dùng `self.move_camera(phi=65*DEGREES)`)
- Building drop trong 3D space

**P2-04 Occlusion** (`beyond/scenes/part02/p02_s04_occlusion.py`):
- Hiện tại: 2D BEV với _RadarSystem updater
- Cần: ThreeDScene, camera phi=70° → tilt xuống phi=65° khi radar waves tỏa ra
- Building là 3D Prism, không phải 2D Rectangle

**P5-07 Living City** (`beyond/scenes/part05/p05_s07_living_city.py`):
- Hiện tại: 2D top-down với circles
- Cần: isometric 3D city view, buildings là 3D prisms với window lights
- Agents di chuyển trên mặt đất 3D

**I-03 Roadmap** (`beyond/scenes/intro/i03_roadmap.py`):
- Hiện tại: dùng `MovingCameraScene`, nodes là circles phẳng
- Cần: Camera zoom giữ nguyên, nhưng thêm depth: nodes có drop shadow, orbits có tilt nhẹ

### 3.3 BRIDGE SCENES — Thêm khi cần nối nội dung

Đọc `5_PART_GUIDE.md` và `materials/scripts/` để check tính liên mạch.

Những chỗ cần bridge scene mới:
- **Giữa I-03 và P1-01**: Hiện tại zoom vào P1 node rồi cut — cần 1 scene ngắn (~10s)
  "What makes foundation models special for AV?" — dùng 2-3 bullet points + PI mascot hỏi
- **Giữa P1-09 và P2-01**: Bridge takeaway đã có nhưng thiếu visual — thêm animation
  1 xe đơn độc đang run thành công NHƯNG gặp tòa nhà → dẫn vào Part 2
- **Giữa P2-12 và P3-01**: "Chúng ta có model tốt, nhưng deploy ở đâu?" → bridge
- **Giữa P4-09 và P5-01**: "Cars sorted. What about everything else?" → thêm visual

Template bridge scene (nhanh ~15s):
```python
class BridgeXtoY(BeyondScene):
    PART_COLOR = PX_COLOR
    def construct(self):
        # 1. Brief summary of what was solved (1-2 icons, ~3s)
        # 2. "But..." transition moment (key_insight_reveal, ~4s)
        # 3. Question that Part Y answers (Write, ~5s)
        # 4. Close
```

### 3.4 TIMING & LAYOUT — Fix tất cả overlap và timing lệch

Khi làm từng scene, bắt buộc chạy `manim -ql` và xem video. Check:

**Spacing rules** (từ `BEYOND_SELFDRIVING_ANIMATION_GUIDE.md §4.1`):
```
Canvas: 14.22u wide × 8.0u tall
Title strip: y > 3.2u
Content area: -3.4u < y < 2.5u
Footnote: y < -3.3u
Left/Right safe margin: |x| < 6.5u
```

**Checklist mỗi scene:**
- [ ] Title text ở đúng y > 2.6u
- [ ] Không có gì overflow sang margin
- [ ] Pipeline blocks dùng `.arrange(RIGHT, buff=0.55)` — không eyeball
- [ ] Axes vẽ TRƯỚC data (luật U7 tuyệt đối)
- [ ] FadeOut sạch cuối scene
- [ ] Wait(0.3-0.5) minimum giữa các bước reveal
- [ ] Key insights: hold tối thiểu 1.5s sau key_insight_reveal
- [ ] Bubbles: chỉ 1 bubble visible tại 1 thời điểm

### 3.5 CONTENT DEPTH — Đọc slide để thêm chi tiết

Hiện tại nhiều scenes chỉ show tên paper mà không explain WHY.

Quy trình:
1. Mở `materials/slides/` (slide PDF gốc)
2. Mở `materials/scripts/script_partX.md` (transcript tiếng Việt)
3. Với mỗi paper/method được đề cập: thêm 1-2 bullet point giải thích
   - Tại sao paper này quan trọng?
   - Con số cụ thể là gì? (AP improvement, speedup, v.v.)
   - Vấn đề nó giải quyết?

Ví dụ P2-07 V2XPnP:
- HIỆN TẠI: chỉ show 3-layer architecture
- PHẢI THÊM: SOTA numbers (detection AP +X%, prediction EPA +Y%)
- Badge: "ICCV 2025 Best Paper" nếu applicable

### 3.6 VISUAL POLISH — Mỗi scene phải thở

Áp dụng **MICRO_ANIMATION_BIBLE.md** triệt để:

**Scene opening (G1):** Mỗi body scene BẮT BUỘC có 3-beat opening:
1. BG flash (0.04 opacity, 0.15s)
2. Title scan line (0.6s)
3. Separator line (0.35s)
→ Hiện tại `BeyondScene.open()` đã làm việc này — verify nó được gọi đúng

**Micro-detail per part (Section H):**
- Part 1: `neural_spark()` mỗi khi model "processes" data
- Part 2: `signal_ping()` mỗi khi V2X data received
- Part 3: scan-to-twin effect khi show Digital Twin
- Part 4: `compression_squeeze()` khi show INT8
- Part 5: `human_awareness()` khi robot nhận ra human

**Ambient backgrounds (F1/F2):**
- Body scenes: 22 particle drift (đã có qua `SHOW_AMBIENT = True`)
- Part 1 scenes: thêm `setup_p1_ambient()` — faint neural net
- Part 2 scenes: thêm `setup_p2_ambient()` — faint radar rings

**Transitions:**
- Giữa scenes trong cùng 1 part: brief `part_color flash` (G2 scene close)
- Giữa các parts: `FullScreenRectangle` wipe

---

## 4. QUY TRÌNH LÀM VIỆC — THEO THỨ TỰ NÀY

```
Với mỗi scene (theo thứ tự SCENE ORDER bên dưới):

1. Read file hiện tại
2. Read phần tương ứng trong 5_PART_GUIDE.md
3. Xem slide gốc (materials/slides/) để check content accuracy
4. Identify: layout bugs, timing issues, missing content, missing 3D
5. Rewrite/enhance với full effort
6. Render: manim -ql "beyond/scenes/xxx/yyy.py" ClassName
7. Nếu render OK → next scene
8. Nếu render fail → fix bug trước khi tiếp tục
```

**KHÔNG bỏ qua bước 6.** Mỗi scene phải render clean trước khi tiếp.

**Với 3D scenes:** Phải dùng `ThreeDScene` và test đặc biệt cẩn thận vì 3D có nhiều edge cases.

---

## 5. SCENE ORDER — THỨ TỰ XỬ LÝ

Làm theo thứ tự này. Đánh dấu [DONE] khi xong.

```
PRIORITY 1 — Iconic scenes (phải làm đẹp nhất):
  [ ] i02_the_hook.py         → I02Hook         (3D radar waves)
  [ ] p02_s04_occlusion.py    → P02S04Occlusion  (3D BEV + pedestrian)
  [ ] p01_s04_longtail.py     → P01S04LongTail   (power-law visual)
  [ ] p05_s07_living_city.py  → P05S07LivingCity (3D city finale)
  [ ] p04_s03_coopre.py       → P04S03CooPre     (voxel puzzle)

PRIORITY 2 — Title cards (cần consistent high quality):
  [ ] i01_title_card.py       → I01TitleCard
  [ ] p01_s01_title.py        → P01S01Title
  [ ] p02_s01_title.py        → P02S01Title
  [ ] p03_s01_title.py        → P03S01Title
  [ ] p04_s01_title.py        → P04S01Title
  [ ] p05_s01_title.py        → P05S01Title

PRIORITY 3 — Key body scenes per part:
  [ ] p01_s02_genai_boom.py   → timeline chart
  [ ] p01_s03_av_arch.py      → 3 architectures
  [ ] p01_s06_vla_gallery.py  → VLA cards
  [ ] p01_s08_autovla.py      → AutoVLA climax
  [ ] p02_s02_background.py   → 1.19M counter
  [ ] p02_s05_related_works.py → evolution timeline
  [ ] p02_s07_v2xpnp.py       → V2XPnP framework
  [ ] p03_s02_sim_gap.py       → split world
  [ ] p03_s05_kalman.py        → three rivers
  [ ] p04_s05_quantv2x.py      → compression reveal
  [ ] p05_s03_metaurban.py     → compositional quote
  [ ] p05_s05_citywalker_pedgen.py → zombie→alive

PRIORITY 4 — Bridge và summary scenes:
  [ ] Tất cả _bridge.py và _summary.py
  [ ] i03_roadmap.py
  [ ] p01_s09_takeaways.py
  [ ] Thêm bridge scenes mới nếu cần (Section 3.3)

PRIORITY 5 — Các scene còn lại
  [ ] Tất cả p03_s*, p04_s* còn lại
```

---

## 6. KỸ THUẬT 3D TRONG MANIM

Khi implement ThreeDScene:

```python
from manim import *

class MyScene(ThreeDScene):
    def setup(self):
        self.camera.background_color = "#090E1A"

    def construct(self):
        # Set camera angle
        self.set_camera_orientation(phi=65*DEGREES, theta=-45*DEGREES)
        self.camera.frame_width = 12

        # Di chuyển camera (animate)
        self.move_camera(phi=60*DEGREES, theta=-30*DEGREES, run_time=1.5)

        # Thêm 3D objects
        prism = Prism(dimensions=[1, 0.8, 2])   # building
        sphere = Sphere(radius=0.3)              # agent
        cylinder = Cylinder(radius=0.3, height=0.2)  # car top-down

        # Ground plane
        ground = Square(side_length=12).rotate(PI/2, RIGHT)

        # LỬU Ý: Text trong 3D dùng Text3D hoặc flat Text với add_fixed_in_frame_mobjects
        label = Text("Label", font_size=24)
        self.add_fixed_in_frame_mobjects(label)  # ← stays flat on screen
```

**Radar waves trong 3D (từ BEYOND_SELFDRIVING_ANIMATION_GUIDE §3.1):**
```python
# Dùng concentric Circle3D hoặc Annulus trong 3D space
def radar_ring_3d(center, radius, color, opacity):
    ring = Circle(radius=radius, color=color,
                  stroke_opacity=opacity, fill_opacity=0)
    ring.rotate(PI/2, RIGHT)  # lay flat on ground
    ring.move_to(center)
    return ring
```

**BEV (Bird's Eye View) isometric:**
```python
self.set_camera_orientation(phi=65*DEGREES, theta=-45*DEGREES, gamma=0)
# Ground = XY plane, Z = up
# Road lines: Line([x1, y1, 0], [x2, y2, 0]) → flat on ground
```

---

## 7. FONT SETUP

Test font trước khi dùng:
```python
# Test scene để verify font
from manim import *
class FontTest(Scene):
    def construct(self):
        for font in ["CMU Serif", "CMU Sans Serif", "DejaVu Serif",
                     "Latin Modern Roman", "Times New Roman"]:
            try:
                t = Text(font, font=font, font_size=28)
                self.add(t)
                self.remove(t)
                print(f"OK: {font}")
            except:
                print(f"MISSING: {font}")
```

Priority font order: CMU Serif > DejaVu Serif > Latin Modern Roman > default

Sau khi chọn font: sửa `beyond/config.py`:
```python
FONT_PRIMARY = "CMU Serif"    # hoặc font tốt nhất có sẵn
FONT_MONO    = "JetBrains Mono"  # hoặc "Courier New"
```

---

## 8. CONTENT STANDARDS — Mỗi scene phải đảm bảo

### Về nội dung:
- Mỗi paper/method được đề cập PHẢI có:
  - 1 sentence giải thích contribution
  - Ít nhất 1 con số cụ thể (AP, FPS, latency, v.v.)
  - Tại sao nó quan trọng với bức tranh tổng thể
- Cross-check với slide gốc trong `materials/slides/`
- Transcript trong `materials/scripts/` là nguồn content authority

### Về visual:
- Title text: SIZE_HERO = 52, GOLD, forge effect
- Body text: SIZE_BODY = 26, TEXT_WHITE, không nhỏ hơn 22
- Labels: SIZE_LABEL = 20
- Captions/footnotes: SIZE_MICRO = 13
- Charts LUÔN có axis labels (kể cả ngắn)
- Pipeline blocks: consistent height 0.80-0.90u

### Về animation:
- KHÔNG có scene nào chỉ dùng FadeIn flat cho quote/key text
- KHÔNG có scene nào thiếu FadeOut cuối
- Key insight moments: dim overlay + centered text + 2.0-3.0s hold
- Mỗi part có signature micro-animation (xem MICRO_ANIMATION_BIBLE §H)

---

## 9. FILES QUAN TRỌNG — ĐỌC TRỰC TIẾP

```
beyond/config.py                     ← theme, font config
beyond/components/colors_dark.py     ← bảng màu đầy đủ (GOLD, CYAN_NEON, v.v.)
beyond/components/animations.py      ← scene_open, scene_close, key_insight_reveal,
                                        bullet_reveal, evolution_timeline, v.v.
beyond/components/base_scene.py      ← BeyondScene class, PartTitleCard
beyond/render_all.py                 ← render + merge script

5_PART_GUIDE.md                      ← kịch bản từng cảnh (SOURCE OF TRUTH)
BEYOND_SELFDRIVING_ANIMATION_GUIDE.md ← spec kỹ thuật 3D + màu sắc
MICRO_ANIMATION_BIBLE.md             ← mọi element animate như thế nào
materials/slides/                    ← slide PDF gốc (Part 1-5)
materials/scripts/script_part*.md   ← transcript tiếng Việt
plans/09_FIX_CHECKLIST.md           ← bug history từ 3 rounds review
```

---

## 10. QUALITY BAR — THẾ NÀO LÀ "XONG"

Một scene được coi là hoàn thành khi:
- [ ] Render clean (không error, không crash)
- [ ] Xem video: không có element nào overlap
- [ ] Timing: viewer có đủ thời gian đọc mỗi text element
- [ ] Content: số liệu, paper names khớp với slide gốc
- [ ] 3D (nếu applicable): camera angle đúng spec, không z-fighting
- [ ] Font: nhất quán với config
- [ ] Scene end: FadeOut sạch, không có leftover objects
- [ ] Emotional arc: scene có HIGH POINT rõ ràng, không flat từ đầu đến cuối

---

## 11. LỜI NHẮC CUỐI

- **Cứ 3-4 scenes, render một lần.** Đừng viết 10 scenes rồi mới render — bugs tích lũy.
- **3D scenes cần thêm thời gian.** ThreeDScene có nhiều edge cases — test sớm.
- **Font mới có thể làm thay đổi layout.** Sau khi đổi font, phải check lại tất cả title cards.
- **Bridge scenes ngắn thôi.** 10-20s, đừng biến thành full scene.
- **Đọc slide trước khi viết.** Presenter original nêu ra reason for everything — đừng simplify.
- **Creativity > compliance.** Guide là khung — innovation trong từng animation là điều user muốn.
