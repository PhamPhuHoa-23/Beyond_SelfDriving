# BEYOND SELF-DRIVING — ANIMATION MASTERCLASS GUIDE
### ICCV 2025 Tutorial · Manim Production · 16:9 · 4K

> Đây là tài liệu hướng dẫn sáng tạo đầy đủ cho toàn bộ video. Mọi quyết định về aesthetic, animation, layout, và màu sắc đều ghi ở đây. Khi implement, đây là nguồn sự thật duy nhất.

---

## 0. QUYẾT ĐỊNH NỀN TẢNG

### 0.1 Background — DARK THEME (quyết định thay đổi hoàn toàn)

**Chọn: Nền tối `#090E1A` (Space Navy — gần đen nhưng có hint blue)**

Lý do không dùng white theme của bản draft cũ:
- Content nói về radar, LiDAR, sensor waves — những thứ này PHẢI phát sáng trên nền tối
- Hiệu ứng gravitational wave, particle system, glowing BEV grid — không thể làm đẹp trên nền trắng
- Welch Labs reference (`background_color: '#000000'`) — bạn muốn theo hướng đó
- Dark theme tạo cảm giác "kỹ thuật cao, nghiêm túc" phù hợp với audience CV/robotics

**Config Manim:**
```yaml
# custom_config.yml
camera:
  resolution: (3840, 2160)       # 4K
  background_color: '#090E1A'    # Space Navy
  fps: 30
  background_opacity: 1.0
file_writer:
  saturation: 1.4                # Boost saturation nhẹ cho glowing effects
```

**Part title cards:** Chuyển từ navy sang `#030508` (gần pure black) — tạo contrast mạnh hơn với body scenes

---

## 1. BẢNG MÀU (Color Palette) — Dark Theme Edition

```python
# colors_dark.py — THAY TOÀN BỘ colors.py

# ─── Backgrounds ─────────────────────────────────────────────────
BG_SPACE          = "#090E1A"   # Body scene background (default)
BG_VOID           = "#030508"   # Part title card (darkest)
BG_GRID_LINE      = "#0D1829"   # Grid/road surface tone
BG_PANEL          = "#0F1A2E"   # Info box fill background

# ─── Primary Text ────────────────────────────────────────────────
TEXT_WHITE        = "#E8EDF4"   # Main body text (không dùng pure white — quá chói)
TEXT_DIM          = "#6B7A99"   # Secondary / caption text
TEXT_GHOST        = "#2A3550"   # Background label, subtitle dim

# ─── Brand Accents ───────────────────────────────────────────────
GOLD              = "#FFD100"   # UCLA Gold — key emphasis, title highlights
GOLD_GLOW         = "#FFE566"   # Lighter gold cho glow effect
CYAN_NEON         = "#00E5FF"   # LiDAR beams, radar waves, sensor data
CYAN_DIM          = "#0097A7"   # Dimmed sensor / secondary signal
BLUE_ELECTRIC     = "#4D9FFF"   # Communication links, V2X arrows
BLUE_SOFT         = "#1565C0"   # Fill for agent boxes
GREEN_SIGNAL      = "#00E676"   # Successful detection, ✓ marks, AP gain
GREEN_DIM         = "#00796B"   # Background success fill
RED_ALERT         = "#FF1744"   # Error, miss, danger zone
RED_DIM           = "#B71C1C"   # Background danger fill
ORANGE_INFRA      = "#FF6D00"   # RSU / Infrastructure nodes
PURPLE_MODEL      = "#CE93D8"   # Neural net / model blocks
PURPLE_DEEP       = "#4A148C"   # Model fill background

# ─── Part-Specific ───────────────────────────────────────────────
P1_FOUNDATION     = "#7986CB"   # Indigo — Foundation Models
P2_COOP           = "#00BCD4"   # Teal — Cooperative Perception  
P3_SIM            = "#4CAF50"   # Green — Sim-to-Real
P4_EFFICIENT      = "#FFC107"   # Amber — Efficiency / Quantization
P5_PHYSICAL       = "#F06292"   # Pink — Physical AI / Pedestrians

# ─── Special Effects ─────────────────────────────────────────────
WAVE_CORE         = "#00E5FF"   # Center of radar/gravitational wave
WAVE_MID          = "#00607A"   # Mid-ring of wave
WAVE_EDGE         = "#003344"   # Outer ring (fades out)
GRID_LINE         = "#112233"   # BEV map grid lines
VOXEL_MASKED      = "#1A237E"   # Masked voxel (dark blue)
VOXEL_ACTIVE      = "#82B1FF"   # Active/visible voxel
LIDAR_BEAM        = "#80DEEA"   # LiDAR scan beam
COMM_LINK         = "#40C4FF"   # Vehicle-to-vehicle link color
FP32_HEAVY        = "#FF5252"   # Full precision — expensive, heavy
INT8_LIGHT        = "#69F0AE"   # Quantized — fast, light
```

---

## 2. TYPOGRAPHY

```python
FONT_PRIMARY = "CMU Serif"      # Welch Labs default — elegant, mathematical
FONT_MONO    = "JetBrains Mono" # Code / numbers / bit-level display
FONT_LABEL   = "CMU Sans Serif" # Axis labels, captions

# Sizes (Manim units ≈ pixels/48)
SIZE_HERO    = 52   # Title cards — part names
SIZE_TITLE   = 38   # Scene headers
SIZE_BODY    = 26   # Main explanation text
SIZE_LABEL   = 20   # Diagram labels, axis ticks
SIZE_CAPTION = 16   # Footnotes, citations
SIZE_MICRO   = 13   # Background text, citations in corners
```

**Rules:**
- Title cards: `GOLD` text trên `BG_VOID`
- Scene titles: `TEXT_WHITE` bold
- Body text: `TEXT_WHITE`  
- Emphasis: `GOLD` hoặc `CYAN_NEON`
- Dim labels: `TEXT_DIM`
- Không dùng plain white `#FFFFFF` — dùng `TEXT_WHITE = "#E8EDF4"` để tránh quá chói

---

## 3. HIỆU ỨNG SIGNATURE — PHẢI CÓ TRONG VIDEO

### 3.1 🌊 RADAR AS GRAVITATIONAL WAVE (Cảnh đặc trưng Part 2)

Đây là **hiệu ứng iconic** của toàn video — phải làm đẹp nhất.

**Concept:** Khi xe phát signal, sóng tỏa ra như gravitational waves từ LIGO:
- Không phải circle 2D đơn giản
- Là **concentric ellipsoid shells** tỏa ra từ điểm xe trong không gian 3D, nhìn từ góc BEV isometric (camera tilt ~60°)
- Mỗi shell: neon cyan, fade ra từ `WAVE_CORE → WAVE_MID → WAVE_EDGE → transparent`
- Khoảng cách giữa các shells không đều — gần nhau ở gốc, thưa dần ra ngoài (như gravitational wave thực)
- Khi gặp vật cản: wave bị "bóp méo" (distort) xung quanh obstacle, không xuyên qua — tạo shadow/blind zone tự nhiên

**Layout 3D camera:**
```python
# Dùng ThreeDScene với camera angle cố định
self.set_camera_orientation(phi=65*DEGREES, theta=-45*DEGREES, gamma=0)
self.camera.frame_width = 10

# Xe là cylinder thấp, neon-bordered
car = Cylinder(height=0.3, radius=0.4, 
               fill_color=BLUE_SOFT, fill_opacity=0.9,
               stroke_color=CYAN_NEON, stroke_width=2)

# Radar wave = series of Sphere shells với increasing radius
def make_wave_ring(t, max_radius=5.0, base_color=CYAN_NEON):
    r = t * max_radius
    opacity = max(0, 1.0 - t) * 0.6  # Fade ra ngoài
    ring = Circle3D(radius=r, color=base_color).set_opacity(opacity)
    return ring
```

**Animation flow radar:**
1. `t=0`: Xe đứng yên, pulse nhỏ từ antenna
2. `t=0.5`: Wave ring đầu bắt đầu tỏa ra, 4-5 rings cách nhau
3. `t=1.5`: Wave gặp building → distortion effect (dùng `ParametricSurface` bị "dented")
4. `t=2.0`: Blind zone sau building sáng đỏ `RED_DIM`
5. `t=2.5`: Xe thứ 2 xuất hiện, phát wave riêng → 2 wave systems
6. `t=3.5`: **INTERFERENCE PATTERN** — nơi 2 waves gặp nhau, vùng sáng/tối xen kẽ như diffraction grating
7. `t=4.5`: Blind zone chuyển từ đỏ sang xanh — hợp tác giải quyết occlusion

### 3.2 🔵 BEV HOLOGRAPHIC GRID (Dùng xuyên suốt Parts 2-4)

Bird's Eye View map không phải lưới tẻ nhạt — mà là **holographic projection**:

```python
# BEV grid với glow effect
def create_bev_grid(rows=20, cols=20, cell_size=0.4):
    grid = VGroup()
    for i in range(-rows//2, rows//2 + 1):
        line_h = Line(
            [-cols/2 * cell_size, i * cell_size, 0],
            [cols/2 * cell_size, i * cell_size, 0],
            stroke_color=GRID_LINE,
            stroke_width=0.8
        )
        grid.add(line_h)
    for j in range(-cols//2, cols//2 + 1):
        line_v = Line(
            [j * cell_size, -rows/2 * cell_size, 0],
            [j * cell_size, rows/2 * cell_size, 0],
            stroke_color=GRID_LINE, stroke_width=0.8
        )
        grid.add(line_v)
    return grid

# Overlay: glowing scan line sweeping across grid
scan_line = Line(
    start=[-cols/2 * cell_size, 0, 0],
    end=[cols/2 * cell_size, 0, 0],
    stroke_color=CYAN_NEON, stroke_width=2.5,
    stroke_opacity=0.7
)
# Animate: scan_line moves từ bottom lên top, mỗi row sáng lên khi scan qua
```

### 3.3 ⚡ QUANTIZATION BIT COMPRESSION (Part 4 — QuantV2X)

**Concept:** FP32 = 32 glowing dots xếp thành 4×8 matrix. Khi quantize về INT8 = 8 dots còn lại. Animation:

1. 32 dots sáng full brightness `FP32_HEAVY`
2. Compression animation: dots merge/fade theo group
3. 8 dots còn lại, sáng hơn, xanh hơn `INT8_LIGHT`
4. Một bên: full BEV feature (large, heavy, red glow)
5. Bên kia: codebook entry (tiny, bright green, fast)
6. Arrow "300× smaller" animate xuất hiện

```python
# FP32 representation — 32 dots
fp32_dots = VGroup(*[
    Dot(radius=0.06, color=FP32_HEAVY, 
        fill_opacity=0.9).move_to(
        [i*0.2 - 3.1, j*0.2 - 0.7, 0])
    for i in range(8) for j in range(4)
])

# INT8 — chỉ còn 8 dots, sáng hơn
int8_dots = VGroup(*[
    Dot(radius=0.10, color=INT8_LIGHT,
        fill_opacity=1.0).move_to(
        [i*0.5 - 1.75, 0, 0])
    for i in range(8)
])

# Animation: LaggedStart(FadeOut) cho 24 dots, Transform 8 còn lại
self.play(
    LaggedStart(*[
        Succession(
            FadeOut(fp32_dots[i], scale=0.3),
        )
        for i in range(24)
    ], lag_ratio=0.05),
    *[Transform(fp32_dots[24+i], int8_dots[i]) 
      for i in range(8)],
    run_time=2.0
)
```

### 3.4 🏙️ ZOMBIE CITY → ALIVE CITY (Part 5)

**Concept:** Contrast giữa simulation không có human model (zombie city) và simulation với PedGen:

**Zombie city (trước):**
- Pedestrians = hình vuông nhỏ, di chuyển straight line, đi xuyên qua nhau
- Màu: `TEXT_DIM` (gray)
- No collision avoidance, robotic movement
- Text overlay: `"Zombie City"` in flashing `RED_ALERT`

**Alive city (sau PedGen):**
- Pedestrians = hình người nhỏ (stick figure đơn giản, Manim polygon), di chuyển với acceleration, deceleration, avoidance
- Màu: `P5_PHYSICAL` (pink) — con người nổi bật
- Các agent khác: delivery robots `P3_SIM`, cars `BLUE_ELECTRIC`, infrastructure `ORANGE_INFRA`
- Animation: smooth bezier curves thay straight lines
- Communication web: thin lines connecting nearby agents, pulsing

**Transform animation:**
```python
# Zombie to alive transition
self.play(
    *[mob.animate.set_color(P5_PHYSICAL) 
      for mob in ped_group],
    # Straight paths → curved paths
    *[Transform(zombie_path[i], alive_path[i]) 
      for i in range(n_peds)],
    # Text transform
    ReplacementTransform(zombie_label, alive_label),
    run_time=2.5,
    rate_func=smooth
)
```

---

## 4. LAYOUT RULES — ANTI-OVERLAP BIBLE

Đây là nguyên nhân số 1 gây lỗi trong bản draft cũ. **Đọc kỹ trước khi code bất cứ scene nào.**

### 4.1 Safe Zones (16:9 aspect ratio, Manim units)

```
Canvas: width = 14.22u,  height = 8.0u
Origin: (0, 0) = center

Safe zones:
┌──────────────────────────────────────────┐  y = +4.0
│  [TITLE STRIP]  top 0.8u                │  y = +3.2 ← TITLE BASELINE
│  ─────────────────────────────────────  │
│                                          │
│  [CONTENT AREA]  6.6u tall × 12.0u wide │  y = -3.4 ← CONTENT BOTTOM
│                                          │
│  ─────────────────────────────────────  │
│  [FOOTNOTE STRIP]  bottom 0.6u          │  y = -4.0
└──────────────────────────────────────────┘  
         x = -7.11                   x = +7.11

Left margin:  x = -6.5u (absolute min content edge)
Right margin: x = +6.5u
```

### 4.2 Title Strip Rules

```python
scene_title = Text("Scene Name", font_size=SIZE_TITLE, 
                   color=TEXT_WHITE, font=FONT_PRIMARY)
scene_title.to_edge(UP, buff=0.25)  # Always: buff=0.25 minimum
# KHÔNG bao giờ đặt nội dung y > 2.8u — reserve cho title
```

### 4.3 Pipeline Block Standard

**Tất cả pipeline boxes PHẢI dùng cùng một helper function:**

```python
def pipeline_block(text, width=2.4, height=0.85, 
                   border_color=CYAN_NEON, fill_color=BG_PANEL,
                   font_size=SIZE_LABEL, text_color=TEXT_WHITE,
                   corner_radius=0.12):
    """
    Standard dark-theme pipeline block.
    Không tự ý thay đổi width/height ngoài helper này.
    """
    rect = RoundedRectangle(
        corner_radius=corner_radius,
        width=width, height=height,
        fill_color=fill_color, fill_opacity=1.0,
        stroke_color=border_color, stroke_width=1.8
    )
    label = Text(text, font_size=font_size, 
                 color=text_color, font=FONT_PRIMARY)
    label.move_to(rect.get_center())
    # KIỂM TRA: nếu label rộng hơn rect, giảm font_size
    if label.width > width - 0.3:
        label.set(font_size=font_size - 3)
        label.move_to(rect.get_center())
    return VGroup(rect, label)

def pipeline_arrow(from_mob, to_mob, color=BLUE_ELECTRIC, 
                   buff=0.08, tip_length=0.18):
    return Arrow(
        from_mob.get_right(), to_mob.get_left(),
        buff=buff, color=color,
        stroke_width=2.0, tip_length=tip_length
    )
```

**Arrange rules:**
```python
# LUÔN dùng arrange() — KHÔNG eyeball position
row = VGroup(block_a, block_b, block_c, block_d)
row.arrange(RIGHT, buff=0.55)
row.move_to(ORIGIN)  # hoặc specific position

# Kiểm tra không overflow:
assert row.width < 12.0, f"Pipeline quá rộng: {row.width:.2f}u"
```

### 4.4 Roadmap Strip

Chỉ xuất hiện trong PART TITLE CARDS (nền `BG_VOID`). Không bao giờ đặt trong body scenes.

```python
def roadmap_strip(current_part: int, total=5) -> VGroup:
    """
    5 dots, connected by line. current_part highlighted gold.
    Luôn đặt ở y = -3.0 (bottom of title card).
    KHÔNG có text labels — chỉ dots.
    """
    dots = VGroup()
    line = Line([-2.0, 0, 0], [2.0, 0, 0], 
                stroke_color=TEXT_GHOST, stroke_width=1.5)
    spacing = 1.0
    for i in range(total):
        x = -2.0 + i * spacing
        is_current = (i + 1 == current_part)
        d = Circle(radius=0.12,
                   fill_color=GOLD if is_current else TEXT_GHOST,
                   fill_opacity=1.0,
                   stroke_color=GOLD if is_current else TEXT_DIM,
                   stroke_width=1.5).move_to([x, 0, 0])
        dots.add(d)
    strip = VGroup(line, dots)
    strip.move_to([0, -3.0, 0])
    return strip
```

### 4.5 Bubble (Mascot Speech)

```python
# CHỈ 1 bubble tại 1 thời điểm. Position: TOP-RIGHT corner, cố định cho cả scene
BUBBLE_ANCHOR = [4.5, 2.5, 0]  # Fixed position — không di chuyển

# Bubble phải fade out trước khi hiện bubble mới
self.play(FadeIn(bubble_1, shift=DOWN*0.1))
self.wait(1.2)
self.play(FadeOut(bubble_1))
self.wait(0.2)
self.play(FadeIn(bubble_2, shift=DOWN*0.1))
```

**Dark theme bubble:**
```python
def dark_bubble(text, target_mob, color=CYAN_NEON, fill="#071222"):
    label = Text(text, font_size=SIZE_LABEL, color=TEXT_WHITE)
    rect = RoundedRectangle(
        corner_radius=0.15,
        width=label.width + 0.5,
        height=label.height + 0.3,
        fill_color=fill, fill_opacity=0.95,
        stroke_color=color, stroke_width=1.5
    )
    label.move_to(rect)
    return VGroup(rect, label).move_to(BUBBLE_ANCHOR)
```

### 4.6 Chart Layout — No Overlap Rule

```python
# LUÔN: axes first, then data
# Axes chiếm LEFT 60% của canvas → room cho annotation ở RIGHT 35%
axes = Axes(
    x_range=[0, 10, 2],
    y_range=[0, 100, 20],
    x_length=7.5,   # Không dùng 12 — cần margin
    y_length=4.5,
    axis_config={"color": TEXT_DIM, "stroke_width": 1.5,
                 "include_tip": True},
).shift(LEFT * 1.5)  # Shift left để có space cho annotations

# Annotations phải ở RIGHT of axes
annotation = Text("Key insight", font_size=SIZE_LABEL, color=GOLD)
annotation.next_to(axes, RIGHT, buff=0.5)

# KIỂM TRA: annotation không overlap axes
assert annotation.get_left()[0] > axes.get_right()[0], "Annotation overlaps axes!"
```

### 4.7 3D Camera Conventions

Cho tất cả scenes dùng 3D (radar waves, BEV isometric):

```python
class ThreeDSceneBase(ThreeDScene):
    def setup(self):
        # Standard isometric view cho V2X scenes
        self.set_camera_orientation(
            phi=65*DEGREES,    # Tilt
            theta=-45*DEGREES, # Rotation  
            gamma=0
        )
        self.camera.frame_width = 12
        
        # Ground plane: BEV grid
        self.ground = self.create_ground()
        self.add(self.ground)
    
    def create_ground(self):
        grid = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            background_line_style={
                "stroke_color": GRID_LINE,
                "stroke_width": 0.8,
                "stroke_opacity": 0.7
            },
            axis_config={"stroke_opacity": 0}
        )
        return grid
```

---

## 5. INTRO SCENES (I01–I03)

### I01 — Title Card

**Background:** `BG_VOID` (near-black)

**Animation flow (enhanced):**
1. `t=0`: Background `#090E1A` → `BG_VOID` fade in (0.4s)
2. `t=0.4`: Particle burst từ center — 80 tiny cyan dots `CYAN_NEON` tỏa ra rồi fade out trong 1s (particle system: `always_redraw` + `ValueTracker`)
3. `t=1.0`: Logo UCLA `FadeIn` top-left (placeholder SVG rectangle)
4. `t=1.4`: Title `"Beyond Self-Driving"` — `Write` animation, font size 52, `GOLD`
5. `t=2.8`: Subtitle `"ICCV 2025 Tutorial"` — `FadeIn(shift=UP*0.1)`, `TEXT_WHITE`, size 24
6. `t=3.3`: Divider line `Create` left→right, `GOLD`, opacity 0.6
7. `t=3.7`: Presenter info `FadeIn`, `P2_COOP`, size 20
8. `t=4.2`: Hold 1.5s → `FadeOut` all (0.6s)

**Layout:**
```
y=+2.5: [UCLA logo]          "Beyond Self-Driving"     <- GOLD bold 52
y=+1.5:                      "ICCV 2025 Tutorial"      <- WHITE 24
y=+0.9:                      "Team Summary"
y=+0.4: ──────────────────── divider ─────────────────
y= 0.0:                     UCLA Mobility Lab           <- CYAN 20
y=-0.5:           contact: mobility.cs.ucla.edu
y=-3.5: [roadmap: all 5 dots dim, will light in I03]
```

**KHÔNG có mascot ở title card** — mascots debut ở I02.

---

### I02 — The Hook (SCENE ĐẶC BIỆT NHẤT)

**Background:** `BG_VOID` → midway switch to `BG_SPACE`  
**Duration:** ~75s  
**3D:** Yes — dùng `ThreeDScene`

**Act A — One Smart Car:**
1. Camera: `phi=70°, theta=-30°` — nhìn hơi nghiêng
2. Road surface: 2 làn đường, vạch kẻ `TEXT_GHOST`
3. Hero car xuất hiện (cyan-bordered rectangle): `GrowFromCenter`
4. **FM icons** float bên trên xe: 3 hexagon nhỏ (GPT-4, CLIP, DINO) kết nối bằng wire
5. Radar waves bắt đầu (xem section 3.1) — đây là lần đầu tiên hiệu ứng xuất hiện

**Act B — The Wall:**
1. Building block `Create` từ trên xuống (drop in) — màu `BG_PANEL` với edge `TEXT_DIM`
2. Radar waves hit building: **wave distortion effect** — wave ring deforms quanh building
3. Red polygon `"blind zone"` fill behind building: `FadeIn` với `fill_opacity=0.3`, `RED_DIM`
4. FM icons `FadeOut` — xe dù thông minh đến đâu cũng mù
5. Text overlay: `"Even the smartest single agent..."` → `"...cannot see around corners."` (chữ xuất hiện từng từ)

**Act C — Cooperation Reveals:**
1. **FadeOut(fm_icons)** — CRITICAL — giải quyết bug cũ (text overlap)
2. 2 xe thêm `FadeIn` từ góc trái phải
3. Mỗi xe có wave riêng, màu khác nhau: xe 1 `CYAN_NEON`, xe 2 `P1_FOUNDATION`, xe 3 `GREEN_SIGNAL`
4. **Interference pattern**: nơi 3 wave hệ gặp nhau, ánh sáng combined (dùng `opacity add`)
5. Hidden pedestrian behind building: silhouette xuất hiện dần `FadeIn`
6. Red blind zone → `Transform → GREEN_SIGNAL zone`: "Cooperation fills the gap"
7. Text: `"So we taught them to cooperate."` — Write chậm, `GOLD`, italic, size 30

**End:** Tất cả fade → logo transition → I03

---

### I03 — 5-Part Roadmap

**Background:** `BG_SPACE`  
**Không dùng boring horizontal dot list** — dùng **orbital diagram**:

5 parts = 5 nodes trên các quỹ đạo ellipse, centered on "Beyond Self-Driving" core:

```
                    [★ Beyond Self-Driving]
                           |
          ╭────────────────┼────────────────╮
    [P1]──┤                |                ├──[P5]
          │          [P2]──┤──[P4]           │
          ╰────────────────┼────────────────╯
                         [P3]
```

**Animation:**
1. Core node `GrowFromCenter` — pulsing glow
2. Orbit paths `Create` (ellipses, `TEXT_GHOST`)
3. P1 node xuất hiện, color `P1_FOUNDATION`, label `"Foundation Models"` 
4. Lần lượt P2→P5, mỗi node có màu riêng, label nhỏ bên dưới
5. P1 node sáng nhất (gold ring) — "We start here"
6. Arrow animate từ P1→P2→P3→P4→P5 nhanh — show chain of causality
7. Hold → zoom into P1 node → transition to Part 1

---

## 6. PART 1 — Foundation Models for AV

**Part color:** `P1_FOUNDATION = "#7986CB"` (Indigo)

### P01-S01 — Title Card

**Layout:**
```
y=+2.0: "Part 01"              <- TEXT_DIM size 18 (supertitle)
y=+1.0: "Foundation Models"    <- GOLD size 44
y= 0.2: "for Autonomous Driving"  <- GOLD size 44
y=-0.5: "Dr. Zhiyu Huang · UCLA"  <- P1_FOUNDATION size 20
y=-1.2: [italic] "Why, in 2025, can AI..."  <- TEXT_WHITE size 20
y=-3.0: [roadmap strip: dot 1 highlighted GOLD]
```

**Enhancement:** Khi title xuất hiện, background có **very subtle neural network pattern** — tiny nodes và edges, `TEXT_GHOST` opacity 0.08, animated nhẹ (like moving screen-saver)

---

### P01-S02 — GenAI Boom

**Concept:** Timeline không phải flat line — mà là **upward rocket trajectory**

**Layout:**
- Trục X: time (2020 → 2025)
- Trục Y: "AI Capability"
- Curve: exponential, màu `P1_FOUNDATION` với gradient fill bên dưới

**Milestones xuất hiện lần lượt dọc curve:**
```
2020: GPT-3     [dot + label FadeIn]
2021: CLIP      [dot + label FadeIn]  
2022: ChatGPT   [dot + label FadeIn, bigger pulse]
2023: GPT-4     [dot + label FadeIn, GOLD color — turning point]
2024: Gemma/Qwen [multiple dots]
2025: ???       [dot ở đỉnh, blink]
```

**Foundation Model definition box:** 
Xuất hiện bên phải chart, **không overlap** (chart ở left 55%, definition ở right 40%):
```
┌─ Foundation Model ──────────────┐
│ • Train on diverse large data   │
│ • Self-supervised               │
│ • Adapt to downstream tasks     │
│ [Stanford CRFM, 2021]           │
└─────────────────────────────────┘
```
Box có `border_color=P1_FOUNDATION`, `fill_color=BG_PANEL`

**Transition câu hỏi:**
Text xuất hiện ở bottom: `"So... why not apply this to self-driving?"` → text sáng `GOLD`, câu hỏi đặt ra scene tiếp theo

---

### P01-S03 — Ba Kiến Trúc AV

**Concept:** 3 pipeline architectures side-by-side, mỗi cái reveal lần lượt

**Layout (horizontal thirds):**
```
LEFT THIRD:           CENTER:             RIGHT THIRD:
[MODULAR]            [HYBRID]            [E2E]
━━━━━━━━━           ━━━━━━━━━           ━━━━━━━━━
Perc→Loc             ML Perc             sensor
  ↓                   + Planning           ↓
Pred→Plan             + Trad.             raw net
  ↓                   Control             ↓
Control                                  action

Error ❌             Balanced ✓          Black box ⚠️
accumulation
```

**Enhance: Error Cascade Animation (MODULAR):**
1. Perception box có tiny noise particle
2. Arrow to Prediction: noise amplifies (wave-like effect)
3. Arrow to Planning: even bigger noise
4. Control: wrong turn action — car goes wrong way
5. Red `"×"` badges cascade down the pipeline

**E2E box** đặc biệt: toàn bộ pipeline là một **neural net visualization** (layered dots, twinkling)

---

### P01-S04 — Long-Tail Problem

**CẢNH VISUAL ĐẸP NHẤT CỦA PART 1**

**Power-law curve:**
```python
axes = Axes(
    x_range=[0, 100, 20],
    y_range=[0, 1, 0.2],
    x_length=7.0, y_length=4.5,
).shift(LEFT * 2)

# Power law: y = x^(-1.5) normalized
curve = axes.plot(
    lambda x: min(1.0, 2.0 * (x + 1) ** (-1.2)),
    color=P1_FOUNDATION,
    stroke_width=3
)

# Gradient fill: BLUE_SOFT → transparent
# (common scenarios: left side, tall)
# (edge cases: right side, tiny bar)
```

**3 photos:** Vì dark theme, không dùng actual photos — thay bằng **icon illustrations**:
1. Person on road: stick figure + road lines + question mark above
2. Traffic lights on truck: truck icon + 3 upside-down circles
3. Snow-covered road: road shape với white dots (snow particle effect)

**Edge cases animation:**
- Zoom vào đuôi distribution (right side)
- Text: `"99% of driving is routine"`
- Đuôi sáng lên đỏ: `"1% contains all the accidents"`
- Tiny spark particles appear along tail — each spark = one edge case

---

### P01-S05 — FM Empower AV

**Concept:** Hub-and-spoke diagram, nhưng **animated data flowing**

**Center hub:** "Foundation Models" — pulsing hexagon `P1_FOUNDATION`

**Left spokes (sources):**
- VFM (SAM, DINO, CLIP)
- VGM (Wan, NVIDIA Cosmos)
- LLM
- MLLM (Gemma3, Qwen3-VL)

**Right spokes (AV needs):**
- Auto-labeling
- Scenario generation
- Sensor simulation
- Vehicle interface
- E2E Driving Stack ← highlight GOLD (key target)

**Flow animation:** Tiny data packets (dots) travel from left sources → hub → right targets:
```python
# Data packet along path
def data_flow(start, end, color, n_packets=5, duration=1.5):
    for i in range(n_packets):
        dot = Dot(radius=0.05, color=color)
        dot.move_to(start)
        self.play(
            dot.animate.move_to(end),
            FadeOut(dot, run_time=0.2),
            run_time=duration / n_packets,
            lag_ratio=0
        )
```

---

### P01-S06 → S09 — VLA Roadmap + Architectures

**VLA Architecture gallery:**

4 architectures xếp theo timeline (2021→2024):

| Year | Model | Color accent | Key visual |
|------|-------|-------------|------------|
| 2021 | BEVDriver | `CYAN_DIM` | BEV bird-eye view compress box |
| 2022 | EMMA | `BLUE_ELECTRIC` | Chain-of-thought arrows looping |
| 2023 | DriveVLM | `P1_FOUNDATION` | Dual-track (fast/slow) parallel |
| 2024 | AutoVLA | `GOLD` | Toggle switch between modes |

**AutoVLA (UCLA — CLIMAX của Part 1):**
Đây là cảnh QUAN TRỌNG NHẤT Part 1, dành nhiều screen time nhất.

```
Input image/lidar
      ↓
[Scene Complexity Analyzer]  ←  neon border, pulsing
      ↓
    ┌─────────────────────────────┐
    │  Simple scene?              │
    │  → Fast mode (traditional)  │  ← GREEN path
    │                             │
    │  Complex/ambiguous scene?   │
    │  → VLA reasoning mode       │  ← GOLD path with "thinking" animation
    └─────────────────────────────┘
      ↓
   Action output
```

**"Thinking" animation cho VLA mode:**
Chain-of-thought text xuất hiện như typewriter, sau đó decisions emerge:
```
"There is a person waving on the road..."
"They appear to be trying to flag down the vehicle..."
"Safe action: slow down and assess..."
→ [Steering + Speed decision]
```

---

## 7. PART 2 — Cooperative Perception

**Part color:** `P2_COOP = "#00BCD4"` (Teal)  
**Signature effect:** RADAR GRAVITATIONAL WAVES (see section 3.1)

### P02-S02 — Background (Why 1.19M deaths)

**Opening counter animation:**
```python
# Death toll counter
counter = Integer(0, color=RED_ALERT, font_size=60)
counter.move_to(ORIGIN + UP)
self.play(
    ChangeDecimalPlace(counter, 1190000, 
                       run_time=2.5, rate_func=smooth)
)
# Label appears: "traffic deaths per year worldwide"
```

**94% human error visualization:**
```python
# Grid of 100 car icons (10×10)
# 94 của chúng highlight RED_DIM
# 6 còn lại: GREEN_SIGNAL (non-human error)
# Animate: LaggedStart highlight từng icon
```

**Waymo 80% reduction:**
- Bar chart đơn giản: "Before Waymo" vs "After"
- KHÔNG pop-up box overlap — dùng `BraceLabel` phía bên phải
- Bar 2 thu nhỏ còn 20%, màu chuyển `RED_ALERT → ORANGE_INFRA`

---

### P02-S04 — Occlusion (RADAR WAVE MAIN SCENE)

**Đây là cảnh radar gravitational waves đặc trưng — implement đầy đủ hiệu ứng section 3.1**

**Sequence:**
1. `[0s]` BEV ground grid xuất hiện, `BG_SPACE` background
2. `[0.5s]` Car A (hero car) appears center-left
3. `[1.0s]` Radar waves bắt đầu tỏa ra — first 3 rings
4. `[1.5s]` Building block xuất hiện center
5. `[2.0s]` Waves hit building — shadow zone hình thành
6. `[2.5s]` Text: `"Single agent: blind to occlusions"`, `RED_ALERT`
7. `[3.5s]` Two more cars appear (B và C)
8. `[4.0s]` Each car starts own wave system — 3 colors
9. `[5.0s]` **COVERAGE MERGE**: regions combine, shadow zone fills green
10. `[6.0s]` Pedestrian behind building materializes `P5_PHYSICAL` 
11. `[7.0s]` Quote: `"Cooperation is a physics solution, not an algorithm."` `GOLD italic`

**Camera movement trong scene này:**
- Start: static overhead BEV (phi=90°)
- Khi waves tỏa ra: slow camera tilt to phi=65° — 3D depth revealed
- Khi cooperation happens: camera slowly rotate theta 15° — cinematic feel

---

### P02-S05 — Related Works Chain

**4 methods như 4 stages của "evolution" — DNA helix metaphor:**

```
TIMELINE: 2020──────2022──────2022──────2024
            │          │          │          │
         V2VNet    V2X-ViT    Where2comm  CodeFilling
           │          │          │          │
        "Can we     "Better   "What do    "How small
         fuse?"      math?"    we send?"   can we go?"
           │          │          │          │
        solved↓    solved↓    solved↓    solved↓
        "how"      "quality"  "volume"   "size"
```

**Animation:** Mỗi method xuất hiện như một bead trên timeline:
1. Timeline line draws left to right
2. V2VNet: bead drops, label appears above (NOT on timeline)
3. Arrow đến V2X-ViT với label "addresses: fusion quality"
4. Tiếp tục đến hết
5. Sau cùng: "But all 4 miss multi-frame multi-task" → PI bubble xuất hiện

**KHÔNG cho labels zigzag trên/dưới** — tất cả labels ở TRÊN timeline, đủ khoảng cách

---

### P02-S07 → S09 — V2XPnP + TurboTrain

**V2XPnP Framework (UCLA contribution):**
3D pipeline diagram với clear vertical zones:

```
ZONE 1 (top): Multi-agent inputs
  Car A ─────────────────────────────┐
  Car B ─────────── [FUSION CORE] ───┼─→ [Tasks]
  Car C ─────────────────────────────┘
  
ZONE 2 (middle): Fusion + Temporal
  [BEV features] → [4D attention] → [temporal aggregation]
  
ZONE 3 (bottom): Output tasks
  Detection │ Prediction │ Planning
```

**TurboTrain (ICCV 2025 — UCLA):**
Biểu đồ "training stability" đặc biệt:

```python
# Unstable training (old method) — jagged orange line
unstable = ParametricFunction(
    lambda t: axes.c2p(t, 0.3 + 0.4*np.sin(5*t)*np.exp(-t*0.3) + 0.05*np.random.randn()),
    t_range=[0, 8],
    color=ORANGE_INFRA
)

# TurboTrain — smooth convergence, blue
stable = ParametricFunction(
    lambda t: axes.c2p(t, 0.85 * (1 - np.exp(-t*0.8))),
    t_range=[0, 8],
    color=P2_COOP
)

# Animation: draw unstable first, then stable appear on same axes
```

---

### P02-S10 — RiskMap

**Risk field visualization** — đây là cảnh đẹp tự nhiên:

```python
# Top-down road view
# Risk map = color heatmap overlaid on road
# High risk zones: RED_ALERT glow
# Safe zones: transparent/GREEN

def risk_function(x, y, obstacle_positions):
    # Gaussian risk fields around each obstacle
    risk = sum(np.exp(-((x-ox)**2 + (y-oy)**2) / (2*0.8**2))
               for ox, oy in obstacle_positions)
    return min(1.0, risk)

# Animate risk map updating as car moves:
# Old risk: fade out
# New risk based on new position: fade in
```

---

## 8. PART 3 — Bridging Simulation and Reality in V2X

**Part color:** `P3_SIM = "#4CAF50"` (Green)

### P03-S02 — Simulation Gap

**ICONIC VISUAL: Split-world reveal**

Screen chia đôi bởi một vertical "fracture line" pulsing:

```
LEFT HALF (Simulation):          RIGHT HALF (Reality):
─────────────────────            ─────────────────────
Clean grid roads                 Messy real streets
Perfect boxy cars                Varied vehicle shapes  
Uniform lighting                 Shadows, glare
No noise                         LiDAR noise artifacts
P3_SIM border glow               ORANGE_INFRA border glow

"Sim Domain"                     "Real Domain"
```

**Gap animation:**
1. Fracture line `Create` từ top đến bottom — lightning bolt shape, not straight line
2. LEFT side: phát sinh từ LEFT, clean geometry
3. RIGHT side: phát sinh từ RIGHT, messy/noisy
4. Arrow từ sim→real với text `"Sim-to-Real Gap"`, `RED_ALERT`
5. Arrow shrinks khi video progresses (gap được giải quyết)

---

### P03-S04 — V2X Hardware Setup

**Isometric city view** với hardware components labeled:

```
        [RSU Tower]
       /   (ORANGE)
      /
  [Car A] ─── V2X signal ──→ [Car B]
  (CYAN)      (COMM_LINK)    (CYAN)
      \
       \─── signal ──→ [Infrastructure sensor]
                        (ORANGE_INFRA)
```

**Signal animation:** Packets flowing between nodes:
- V2X packets: small hexagons traveling along path `BLUE_ELECTRIC`
- LiDAR beams: scan fan animation từ sensor `LIDAR_BEAM`
- GPS signal: downward arrow từ top `P1_FOUNDATION`

---

### P03-S08 — Kalman Filter Fusion

**THREE RIVERS METAPHOR:**

```
River 1: GNSS          River 2: IMU+Wheel      River 3: LiDAR
Width: wide            Width: medium            Width: narrow
Color: BLUE_ELECTRIC   Color: ORANGE_INFRA      Color: CYAN_NEON  
Speed: slow (5Hz)      Speed: fast (100Hz)      Speed: very slow (1Hz)
Character: "absolute   Character: "drifts       Character: "precise
 but blocked"           over time"               but slow"
     │                       │                       │
     └───────────────────────┴───────────────────────┘
                             │
                    [KALMAN FILTER]
                    (pulsing neural node)
                             │
                    Clean output stream
                    100Hz, lane-level precision
                    Color: GREEN_SIGNAL
```

**Animation:** Ba dòng sông text/particles hợp lưu, kết hợp vào center node, output stream smooth và sáng

---

### P03-S09 → S12 — Digital Twin + CooperFuse

**Digital Twin reveal:**
1. Real-world scene (camera scan effect — horizontal scan line sweeping)
2. Scene "scans" → particles detach và reorganize vào grid
3. Digital twin version xuất hiện bên cạnh: identical but "clean/grid" aesthetic
4. Twin synchronizes với real-time updates: when real car moves, twin moves

**CooperFuse pipeline:**
```
Agent A LiDAR → [3D Encoder]  ─┐
Agent B LiDAR → [3D Encoder]  ─┤→ [Attention Fusion] → [Detection]
Agent C LiDAR → [3D Encoder]  ─┘         │
                                   [Alignment Module]
                                   (chống localization error)
```

---

## 9. PART 4 — Pre-Training to Post-Training: Efficient V2X

**Part color:** `P4_EFFICIENT = "#FFC107"` (Amber)

### P04-S03 — Annotation Cost Explosion

**BAR CHART với explosion metaphor:**

```python
# Chart ở LEFT HALF (x: -7 đến -0.5)
# Annotations ở RIGHT HALF (x: +0.5 đến +7)

# Bars: grow bottom-up với counter animation
data = [
    ("V2V4Real\n2022", 240_000, BLUE_ELECTRIC),
    ("DAIR-V2X\n2023", 460_000, P4_EFFICIENT),
    ("V2X-Real\n2024", 1_200_000, GREEN_SIGNAL),
]

# "5× in 2 years" label: arrow from V2V4Real to V2X-Real
# Placed RIGHT của chart, không overlap
annotation_5x = VGroup(
    Text("5× in 2 years", color=GOLD, font_size=24),
    Arrow(start=RIGHT*0.3, end=RIGHT*0.3+UP*1.5, color=GOLD)
).next_to(chart, RIGHT, buff=0.8)

# Bullet points: RIGHT side, below 5× annotation
bullets = VGroup(
    Text("• Annotators: specialized + expensive", font_size=SIZE_LABEL),
    Text("• Toolkits: complex multi-pass", font_size=SIZE_LABEL),
    Text("• QC: multi-layer checking", font_size=SIZE_LABEL),
).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
bullets.next_to(annotation_5x, DOWN, buff=0.4)
```

---

### P04-S04 — CooPre (IROS 2025 Best Paper)

**MASKED VOXEL PUZZLE ANIMATION:**

Đây là cảnh "wow" của Part 4.

1. BEV grid hiện ra với point cloud từ Agent A và B
2. **Random masking:** Một số voxels fade thành `VOXEL_MASKED` (dark blue)  
   - Animation: mỗi voxel tắt dần như pixel dropout
3. **"The question":** Text floats up `"Can you fill in what you can't see?"`
4. **Reconstruction:** masked voxels từ từ reconstruct:
   - Particles from Agent B move across → land on masked positions
   - Masked voxels reignite `VOXEL_ACTIVE`
   - Success sound visual (glow pulse)
5. **Results reveal:**

```
                    ┌──────────────────────────────────┐
                    │        CooPre Results            │
50% labels →        │  ████████████░░░░░░░░░░░░░░░░░  │  = 100% baseline
100% labels →       │  ████████████████████████████+  │  +4% AP
                    └──────────────────────────────────┘
```

Hai bars animate grow từ 0, counter số animate.

---

### P04-S05 — TurboTrain (ICCV 2025)

**"Gradient Conflict" visualization:**

Dùng vector field diagram:
- Detection gradient: arrow pointing NORTHEAST `BLUE_ELECTRIC`
- Prediction gradient: arrow pointing SOUTHEAST `ORANGE_INFRA`  
- Planning gradient: arrow pointing WEST `P1_FOUNDATION`
- Combined gradient without TurboTrain: chaotic zigzag path
- TurboTrain: smooth path to optimum

```
         WEIGHT SPACE
    ────────────────────────
    │    ↗ Detection       │
    │   ↙ Prediction       │
    │  ← Planning          │
    │                      │
    │  Without TurboTrain: │  ← zigzag path in RED
    │  ↗↙←↗↙←... crash    │
    │                      │
    │  With TurboTrain:    │  ← smooth spiral in GREEN
    │  → → → ✓ Optimum    │
    ────────────────────────
```

**2620 FPS claim:**
```
Traditional V2X training: [||||||||||||||||] 180 GPU-days
TurboTrain:               [||] 3 hours

Ratio: 1440× faster
```
Bar chart với dramatic difference, text animate: `"2620 FPS at inference"`

---

### P04-S06 → S08 — QuantV2X Pipeline

**QuantV2X 3-Stage Pipeline (CẢNH ICON NHẤT Part 4):**

```
STAGE 1                    STAGE 2                    STAGE 3
Full-Precision             Codebook                   Post-Training
Pretraining                Learning                   Quantization
──────────                 ──────────                 ──────────
FP32 weights               Learn discrete             FP32 → INT8
All layers                 token vocab                 Smart calibration
                           for features
[Deep blue glow]           [Gold codebook]            [Green efficiency]
```

**Animation sequence:**
1. Three boxes fade in left-to-right `LaggedStart`
2. Between S1→S2: weights flowing → "condensing" into codebook
3. Between S2→S3: codebook entries quantizing → tiny efficient tokens

**COMMUNICATION COMPRESSION REVEAL (Part 4 climax):**

```
BEFORE QuantV2X:
BEV Feature: [===================] 100 MB per frame
FP32 tensor: 32 bits per value
Bandwidth: 🔴 TOO HEAVY for V2X

AFTER QuantV2X:
Codebook entry: [=] 0.33 MB per frame
4-bit code: just 4 bits per value
Bandwidth: 🟢 300× SMALLER
```

Hiệu ứng compression: large data packet (big glowing blob) → shrinks dramatically → tiny bright dot `INT8_LIGHT`

Dùng `ValueTracker` để animate số từ "100 MB" → "0.33 MB" while blob shrinks.

---

## 10. PART 5 — Scalable, Human-Centric Physical AI

**Part color:** `P5_PHYSICAL = "#F06292"` (Pink)

### P05-S01 — Title Card (SPECIAL)

"All 5 roadmap dots light up gold simultaneously" — đây là khoảnh khắc emotional:

```python
# Dots xuất hiện lần lượt, mỗi dot có burst effect
for i, dot in enumerate(roadmap_dots):
    self.play(
        dot.animate.set_fill(GOLD).set_stroke(GOLD),
        Flash(dot, color=GOLD, flash_radius=0.3, num_lines=8),
        run_time=0.3
    )

# Sau khi tất cả lit up: shared glow giữa 5 dots
# Animation: faint glow line connecting all 5
self.play(
    Create(connecting_glow_line),
    run_time=0.8
)
```

**Bổ sung: quote từ Wayne Wu:**
`"Beyond cars — to any agent, any space."`
Xuất hiện sau khi dots light up, `GOLD italic`, hold 2s

---

### P05-S02 — Physical AI Vision + 2 Barriers

**Web-scale data contrast:**

```
LLMs ← INTERNET DATA:
[Books][Wikipedia][GitHub][Reddit][...][...]  → Trillion tokens
      Arrows flowing into one model
      → GPT-4, Gemma, Claude — knows everything

Physical AI ← ROBOT DATA:
[1 robot][another][expensive][manual]  → Millions actions
      Trickle of data
      → Can't scale this way ❌
```

**2 Barriers:**
```
BARRIER 1: No web-scale robot data
  ─────────────────────────────────
  Internet:   [██████████████████████] Unlimited
  Robot data: [█] Hard to collect

BARRIER 2: No human modeling
  ─────────────────────────────────
  [Robot path] ─────────────── ─── →
  [Human] ??? — modeled poorly → unpredictable
  Result: ZOMBIE CITY
```

Zombie city visual: pedestrians di chuyển thẳng, không interact, xuyên qua nhau (brief 3-second animated clip)

---

### P05-S03 — MetaUrban (ICLR 2025 Spotlight)

**"THE WORLD IS COMPOSITIONAL" — Stuart Geman quote:**

```python
# Quote card: gold italic, centered, hold 2s
quote = Text('"The world is compositional, or there is a god."',
             font="CMU Serif", slant=ITALIC, 
             font_size=28, color=GOLD)
quote.move_to(ORIGIN)
self.play(Write(quote, run_time=1.5))
self.wait(2.0)
# Attribution appears below
attr = Text("— Stuart Geman", font_size=18, color=TEXT_DIM)
attr.next_to(quote, DOWN, buff=0.3)
self.play(FadeIn(attr))
self.wait(1.5)
self.play(FadeOut(quote), FadeOut(attr))
```

**Procedural Generation Animation:**

```
Description Script:
  blocks: 4
  intersections: T-shaped  
  lane_width: 3.2m
  objects: [bench, tree, lamp]
  density: medium
         ↓
[GENERATOR ENGINE]  ← spinning gear animation
         ↓
  [Scene 1] → [Scene 2] → [Scene 3] → ... → [∞ scenes]
  (all different, animate morphing)
```

**Power-law scaling chart:**

```python
# X: number of unique training layouts
# Y: performance on unseen test environments
# Curve: power-law (steeper than linear at start, then sustained growth)

power_law = axes.plot(lambda x: 0.9 * x**0.4 if x > 0 else 0, 
                     x_range=[1, 100], color=P5_PHYSICAL)
linear = axes.plot(lambda x: 0.5 * x/50, 
                  x_range=[1, 100], color=TEXT_DIM)

# Label: "Diversity > Quantity"
```

---

### P05-S05 — UrbanSim (CVPR 2025 Highlight)

**Training efficiency: 180 GPU-days vs 3 hours:**

```python
# Timeline visual
old_bar = Rectangle(width=9.0, height=0.7, 
                   fill_color=FP32_HEAVY, fill_opacity=0.8)
new_bar = Rectangle(width=0.15, height=0.7,
                   fill_color=INT8_LIGHT, fill_opacity=0.9)

# Labels
old_label = Text("Traditional: 180 GPU-days", color=FP32_HEAVY)
new_label = Text("UrbanSim: 3 hours", color=INT8_LIGHT)
```

**GPU-native rendering explanation:**
- Old pipeline: scene → CPU render → GPU train → loop (slow)
- UrbanSim: everything stays on GPU, no CPU transfer
- Visual: data pipeline với bottleneck "CPU transfer" highlighted then removed

---

### P05-S06 — CityWalker (Diversity in Pedestrian Data)

**227 cities visualization:**

World map outline (simple), dots appearing on cities with `LaggedStart`:
- Each dot = 1 of 227 cities
- Size proportional to number of scenes from that city
- Color: `P5_PHYSICAL` (pink)

**Statistics:**
```
30.8h video  |  120,914 pedestrians  |  16,215 scenes
    ↓                ↓                      ↓
"more than    "human diversity    "more training
 any prior     captured"          scenarios than
 dataset"                         any prior work"
```

**Diversity examples (stick figure animations):**
- Person pushing stroller
- Person taking selfie
- Person with luggage
- Person on phone
- Each appears, does action, fades

---

### P05-S07 — PedGen (Diffusion Model)

**3 Inputs + 3 Losses architecture:**

```
3 INPUTS:
──────────────────────────────────────────────────────
[Scene Context]     [Body Context]      [Goal]
  Voxel grid          SMPL skeleton       Destination
  of environment      of person           waypoint
     │                    │                  │
     └────────────────────┴──────────────────┘
                          │
                  [DIFFUSION MODEL]
                  (pulsing noise → clean)
                          │
            ┌─────────────┴─────────────┐
            │                           │
     [Generated trajectory]    [Generated pose]
     
3 LOSSES:
─────────────────────────────────────────────────────
L_rec (Reconstruction) | L_traj (Trajectory) | L_geo (Geometry)
```

**Diffusion animation:**
- Start: pure noise (random colored pixels in skeleton shape)
- Step-by-step: noise reduces, skeleton emerges
- Final: clean walking pedestrian animation

---

### P05-S08 — Grand Finale (CLIMAX của TOÀN BỘ VIDEO)

**Đây là cảnh WOW nhất của toàn bộ video. Render time không giới hạn.**

**Sequence (3 phases):**

**PHASE 1 — City at Night (0-15s):**
City view từ trên cao (isometric 3D), `BG_VOID` background:
- Roads: `GRID_LINE` với faint glow
- Buildings: dark rectangles với window lights (tiny yellow dots)
- Slowly: các agent types FADE IN một sau một, mỗi agent có màu riêng:
  ```
  Cars:          BLUE_ELECTRIC    — smooth bezier paths
  Delivery robots: GREEN_SIGNAL   — grid-snapping movement
  Wheelchairs:    P5_PHYSICAL     — slower, careful paths
  Pedestrians:    GOLD            — organic walking patterns
  RSU towers:     ORANGE_INFRA    — static, pulsing signal
  ```

**PHASE 2 — Communication Web Lights Up (15-30s):**
- Communication links between nearby agents: thin lines `COMM_LINK`
- Lines appear one by one: `LaggedStart(Create(...), lag_ratio=0.02)`
- After all links drawn: the whole city is a **glowing network**
- Radar waves dari all agents simultaneously — gravitational wave effect
- Web "breathes" — opacity oscillating gently

**PHASE 3 — Chain of Solutions Montage (30-50s):**
5 small vignette panels appear (one for each part):
```
┌─P1: Foundation─┐  ┌─P2: Cooperate─┐  ┌─P3: Real World─┐
│ FM → reasoning │  │ Radar waves   │  │ Sim → Real     │
│                │  │ coverage↑     │  │ gap shrinks    │
└────────────────┘  └───────────────┘  └────────────────┘
                                        
         ┌─P4: Efficient─┐  ┌─P5: Physical AI─┐
         │ FP32 → INT8   │  │ Human + Robot   │
         │ 300× smaller  │  │ City thriving   │
         └───────────────┘  └─────────────────┘
```

Each panel: tiny replay of that part's iconic animation

**FINAL FRAME:**
All 5 panels fade, back to full city view:
```
"Beyond Self-Driving.
 Not just smarter cars.
 A safer world."
```
Text: `GOLD`, Write animation, center screen, hold 3s.

Then: roadmap strip with all 5 dots glowing, UCLA logo, `FadeOut`.

---

## 11. TRANSITION RULES BETWEEN SCENES

### Between Parts (Navy → Space transition)
```python
def part_transition():
    # Current scene fades to black
    self.play(FadeToColor(self.camera.background, BG_VOID, run_time=0.5))
    # Part title card plays on BG_VOID
    # After title: fade back to BG_SPACE
    self.play(FadeToColor(self.camera.background, BG_SPACE, run_time=0.5))
```

### Between Scenes within a Part
```python
# Simple: all mobjects fade, new ones appear
def scene_transition(outgoing_group, run_time=0.4):
    self.play(
        FadeOut(VGroup(*[m for m in self.mobjects if m is not self.background]),
                run_time=run_time)
    )
    self.wait(0.1)
```

### Special: "Zoom into concept" transition
```python
# When going from overview → detail
# Zoom in on the relevant node/block before cutting
target_mob.generate_target()
target_mob.target.scale(20).set_opacity(0)
self.play(MoveToTarget(target_mob), run_time=0.8)
# Then new scene starts with that concept at full size
```

---

## 12. ANTI-OVERLAP CHECKLIST (Run trước khi render)

Sau khi viết xong mỗi scene, chạy mental check này:

```python
# Quick overlap test helper
def check_overlaps(mobjects_list, scene_name):
    for i, m1 in enumerate(mobjects_list):
        for j, m2 in enumerate(mobjects_list[i+1:], i+1):
            if m1.get_bounding_box().overlaps(m2.get_bounding_box()):
                print(f"WARNING [{scene_name}]: {type(m1).__name__}[{i}] "
                      f"overlaps {type(m2).__name__}[{j}]")
```

**Checklist per scene:**
- [ ] Scene title nằm trong TITLE STRIP (y > 2.6u)
- [ ] Content nằm trong CONTENT AREA (-3.4u < y < 2.5u)  
- [ ] Citation/footnote nằm trong FOOTNOTE STRIP (y < -3.3u)
- [ ] Pipeline rows không overflow sang margin (|x| < 6.5u)
- [ ] Không có text nằm trên chart area
- [ ] Annotations ở side KHÁC với chart
- [ ] Bubble ở BUBBLE_ANCHOR = [4.5, 2.5, 0], không overlap content
- [ ] Roadmap strip CHỈ trong title cards, không trong body scenes
- [ ] `FadeOut(all_mobs)` ở cuối mỗi scene

---

## 13. CUSTOM ANIMATION RECIPES (Tái sử dụng)

### Glowing pulse (cho bất kỳ node/icon nào)
```python
def glow_pulse(mob, color, n_pulses=2, scale=1.3, run_time=0.4):
    anims = []
    for _ in range(n_pulses):
        ring = mob.copy().set_fill(opacity=0).set_stroke(color, width=3)
        anims.append(
            Succession(
                GrowFromCenter(ring, run_time=run_time),
                ring.animate(run_time=run_time*0.5).set_stroke(opacity=0)
            )
        )
    return LaggedStart(*anims, lag_ratio=0.5)
```

### Data packet flowing along path
```python
def data_packet_flow(path: VMobject, color=COMM_LINK, 
                     n=5, speed=2.0):
    packets = VGroup(*[
        Dot(radius=0.05, color=color).move_to(path.get_start())
        for _ in range(n)
    ])
    return LaggedStart(*[
        MoveAlongPath(p, path, run_time=speed)
        for p in packets
    ], lag_ratio=1.0/n)
```

### Typewriter effect với cursor
```python
def typewriter(text_mob, run_time=1.5):
    cursor = Rectangle(width=0.03, height=text_mob.height,
                      fill_color=CYAN_NEON, fill_opacity=1,
                      stroke_width=0)
    def update_cursor(c):
        c.move_to(text_mob[-1].get_right() + RIGHT*0.05)
    cursor.add_updater(update_cursor)
    return AnimationGroup(
        AddTextLetterByLetter(text_mob, run_time=run_time),
        FadeIn(cursor),
    )
```

### BEV scan sweep
```python
def bev_scan_sweep(grid_mob, direction=UP, color=CYAN_NEON, 
                   run_time=1.5):
    scan_line = Line(
        grid_mob.get_left(), grid_mob.get_right(),
        stroke_color=color, stroke_width=2.0, stroke_opacity=0.8
    )
    scan_line.move_to(grid_mob.get_bottom())
    trail = scan_line.copy().set_stroke(opacity=0.2)
    return AnimationGroup(
        scan_line.animate(run_time=run_time, 
                         rate_func=linear).move_to(grid_mob.get_top()),
        UpdateFromFunc(trail, lambda t: t.become(scan_line.copy()
                                                  .set_stroke(opacity=0.15)))
    )
```

### Voxel reconstruction (CooPre)
```python
def voxel_reconstruct(masked_voxels: VGroup, 
                      source_particles: VGroup,
                      run_time=2.0):
    anims = []
    for i, voxel in enumerate(masked_voxels):
        # Pick random source particle
        src = source_particles[i % len(source_particles)]
        particle = Dot(radius=0.04, color=VOXEL_ACTIVE).move_to(src)
        anims.append(
            Succession(
                FadeIn(particle, run_time=0.1),
                particle.animate(run_time=0.4).move_to(voxel),
                Transform(voxel, voxel.copy().set_fill(VOXEL_ACTIVE, 1.0),
                          run_time=0.2),
                FadeOut(particle, run_time=0.1)
            )
        )
    return LaggedStart(*anims, lag_ratio=0.15)
```

---

## 14. RENDER SETTINGS VÀ FILE STRUCTURE

### Manim config đề xuất
```yaml
# custom_config_dark.yml
camera:
  resolution: (3840, 2160)   # 4K, 16:9
  background_color: '#090E1A'
  fps: 30
  background_opacity: 1.0
file_writer:
  saturation: 1.4
  movie_file_extension: '.mp4'
  h264_crf: 18               # High quality
text:
  font: "CMU Serif"
```

### Recommended render command
```bash
# Quick preview (720p)
manim -ql scene_file.py SceneClass

# Full quality 4K
manim -qk scene_file.py SceneClass

# With output to specific folder  
manim -qk --media_dir ./output scene_file.py SceneClass
```

### File structure
```
drivex/
├── components/
│   ├── colors_dark.py          ← NEW - dark palette
│   ├── pipeline_block.py       ← NEW - standardized blocks
│   ├── radar_wave.py           ← NEW - gravitational wave effect
│   ├── bev_grid.py             ← NEW - holographic grid
│   └── mascots.py              ← UPDATE for dark theme
├── scenes/
│   ├── intro/
│   ├── part01/
│   ├── part02/
│   ├── part03/
│   ├── part04/
│   └── part05/
└── custom_config_dark.yml      ← NEW
```

---

## 15. VÀI LƯU Ý QUAN TRỌNG CUỐI

1. **Không code bất cứ thứ gì khi chưa đọc xong guide này** — nhiều scene depend vào conventions ở các section trên

2. **ThreeDScene cho radar waves** — phải dùng `ThreeDScene`, không thể simulate 3D tốt bằng `Scene` thường

3. **`always_redraw`** — dùng cho scan lines, wave rings, particle systems — không tạo từng frame thủ công

4. **Glow effects** thực sự trong Manim dùng:
   ```python
   # Fake glow: nhiều circles với opacity giảm dần
   def create_glow(center, color, radius=0.5, n_rings=5):
       rings = VGroup()
       for i in range(n_rings):
           r = radius * (i+1)/n_rings
           op = 0.3 * (1 - i/n_rings)
           rings.add(Circle(radius=r, color=color, 
                           stroke_opacity=op, stroke_width=2/(i+1)))
       return rings.move_to(center)
   ```

5. **Camera animation trong 3D scenes** — dùng `move_camera` thay vì `self.camera.animate`:
   ```python
   self.move_camera(phi=65*DEGREES, theta=-45*DEGREES, run_time=1.5)
   ```

6. **Scene timing** — với 4K render, mỗi giây tốn thời gian render. Tránh `self.wait(5)` không cần thiết. Nhưng `wait(1.5)` sau key insights là BẮT BUỘC.

7. **Grand Finale (P05-S08)** — dành nhiều thời gian nhất. Đây là cảnh mà viewer nhớ nhất. Không rush.

---

*Guide này được tạo cho dự án ICCV 2025 "Beyond Self-Driving" tutorial video. Mọi thay đổi lớn về aesthetic hoặc convention phải update file này trước.*
