# CODEX ENHANCEMENT PROMPTS — Beyond Self-Driving Studio

> Dùng file này làm context cho Codex để refine toàn bộ studio/ package.  
> Đọc **tất cả** Global Fixes trước, rồi làm từng Phase theo thứ tự.  
> Mỗi scene prompt chỉ sửa file đó — KHÔNG tạo file mới, KHÔNG xóa logic cũ, chỉ ENHANCE.

---

## ═══ GLOBAL FIXES (áp dụng cho MỌI scene) ═══

### G-1: Background → Pure White

**Vấn đề:** `BG_PAPER = "#FAFAF8"` có tint vàng kem. User muốn trắng thật sự.

**Fix trong `studio/components/colors.py`:**
```python
BG_PAPER: Final[str] = "#FFFFFF"   # pure white — was "#FAFAF8"
BG_CARD: Final[str] = "#F5F5F5"    # very light grey for card backgrounds
BG_SECTION: Final[str] = "#F0F0F0"
```

**Fix trong MỌI scene file** — thêm dòng đầu `construct()`:
```python
def construct(self):
    self.camera.background_color = "#FFFFFF"  # force pure white every time
    ...
```

**Fix trong `studio/components/base_scene.py`** — method `setup()`:
```python
def setup(self) -> None:
    super().setup()
    self.camera.background_color = "#FFFFFF"  # không dùng BG_PAPER constant nữa
    ...
```

---

### G-2: Vehicle Icon → Actual Top-Down Car

**Vấn đề:** `vehicle_icon()` hiện tại = rounded rect + triangle nhỏ → trông như máy quay camera.

**Fix trong `studio/components/agents.py`** — rewrite `vehicle_icon()` hoàn toàn:
```python
def vehicle_icon(*, color: str = ACCENT_BLUE, scale: float = 1.0) -> VGroup:
    """Proper top-down car: body + roof + 4 wheels + windshield line."""
    # Body (main body, elongated)
    body = RoundedRectangle(
        width=1.1, height=0.55, corner_radius=0.1,
        fill_color=color, fill_opacity=1.0,
        stroke_color=color, stroke_width=1.0,
    )
    # Roof (smaller, centered slightly forward)
    roof = RoundedRectangle(
        width=0.58, height=0.36, corner_radius=0.08,
        fill_color=interpolate_color(color, WHITE, 0.25), fill_opacity=0.9,
        stroke_width=0,
    )
    roof.move_to(body.get_center() + LEFT * 0.05)
    # Windshield line (front)
    windshield = Line(
        roof.get_corner(UR) + LEFT * 0.04,
        roof.get_corner(DR) + LEFT * 0.04,
        stroke_color=interpolate_color(color, WHITE, 0.6),
        stroke_width=1.5,
    )
    # 4 wheels (dark rounded squares at corners)
    wheel_color = interpolate_color(color, BLACK, 0.55)
    wheels = VGroup()
    for dx, dy in [(0.42, 0.22), (0.42, -0.22), (-0.42, 0.22), (-0.42, -0.22)]:
        w = RoundedRectangle(
            width=0.2, height=0.12, corner_radius=0.04,
            fill_color=wheel_color, fill_opacity=1.0, stroke_width=0,
        )
        w.move_to(body.get_center() + RIGHT * dx + UP * dy)
        wheels.add(w)
    icon = VGroup(body, wheels, roof, windshield)
    icon.scale(scale)
    return icon
```

---

### G-3: Radar Shells → Gravitational Wave Style

**Vấn đề:** Shells hiện tại = circles phẳng 2D. Cần trông như sóng hấp dẫn thật.

**Fix `radar_shells_2d()` trong `studio/components/signals.py`:**
```python
def radar_shells_2d(
    center: np.ndarray,
    *,
    color: str = CYAN_RADAR,
    n_shells: int = 5,
    max_radius: float = 3.0,
) -> tuple[VGroup, LaggedStart]:
    """Gravitational-wave style shells: uneven spacing, ellipse squish, trailing glow.
    Pattern adapted from: 5_PART_GUIDE P2-04 — shells gần ở tâm, thưa ra ngoài.
    """
    shells = VGroup()
    # Non-linear spacing: dense near center, sparse outside (gravitational wave style)
    radii = [max_radius * ((i + 1) / n_shells) ** 1.6 for i in range(n_shells)]
    for i, r in enumerate(radii):
        opacity = 0.85 * (1 - i / (n_shells + 1)) ** 0.8
        # Slightly elliptical (in 3D view these look more like actual waves)
        shell = Ellipse(
            width=r * 2, height=r * 1.45,  # squish vertically for isometric look
            stroke_color=color,
            stroke_width=max(1.0, 2.8 - i * 0.4),
            stroke_opacity=opacity,
            fill_opacity=0,
        )
        shell.move_to(center)
        shells.add(shell)
    anims = [ShowCreation(s, run_time=0.4 + i * 0.06) for i, s in enumerate(shells)]
    return shells, LaggedStart(*anims, lag_ratio=0.18)
```

**Fix `radar_shells_3d()` — dùng multi-plane rings:**
```python
def radar_shells_3d(
    center: np.ndarray,
    *,
    color: str = CYAN_RADAR,
    n_shells: int = 4,
    max_radius: float = 3.5,
) -> tuple[VGroup, LaggedStart]:
    """3D shells: horizontal ring + 2 tilted rings per radius = sphere feel.
    Pattern adapted from: Source_manim_reference/3b1b_videos/_2026/hairy_ball/model3d.py:260
    """
    shells = VGroup()
    radii = [max_radius * ((i + 1) / n_shells) ** 1.5 for i in range(n_shells)]
    tilt_axes = [OUT, RIGHT, UP + RIGHT * 0.5]  # 3 orthogonal-ish planes
    tilt_angles = [0, PI / 2, PI / 3]
    for i, r in enumerate(radii):
        opacity = 0.75 * (1 - i / (n_shells + 1)) ** 0.7
        width = max(1.2, 2.5 - i * 0.35)
        for axis, angle in zip(tilt_axes, tilt_angles):
            ring = Ellipse(width=r * 2, height=r * 1.5,
                           stroke_color=color, stroke_width=width,
                           stroke_opacity=opacity * (0.9 if angle == 0 else 0.55))
            ring.rotate(angle, axis=axis)
            ring.move_to(center)
            shells.add(ring)
    all_anims = [ShowCreation(s, run_time=0.5) for s in shells]
    return shells, LaggedStart(*all_anims, lag_ratio=0.06)
```

---

### G-4: Color Enhancement — Text trên nền trắng

**Vấn đề:** Màu `INK_DARK = "#1E293B"` và `INK_MID = "#475569"` đủ tối trên trắng. Nhưng một số màu pastel quá nhạt.

**Fix trong `studio/components/colors.py`:**
```python
# Tăng saturation của pastel fills để nổi hơn trên nền trắng
PASTEL_BLUE: Final[str]  = "#BFDBFE"   # was "#C8DCFA"
PASTEL_TEAL: Final[str]  = "#99F6E4"   # was "#B0E8DA"
PASTEL_GREEN: Final[str] = "#BBF7D0"   # was "#C8EDD0"
PASTEL_AMBER: Final[str] = "#FDE68A"   # was "#FAE3B0"
PASTEL_PINK: Final[str]  = "#FBCFE8"   # was "#F9C8D8"

# Title card background — deep ink blue (không phải đen tuyền)
BG_TITLECARD: Final[str] = "#0B1120"   # was "#0F1419" — deeper, richer

# Accent colors — slightly more vivid
GOLD_RICH: Final[str] = "#D97706"      # unchanged, good
GOLD_KEY: Final[str]  = "#F59E0B"      # was "#EAB308" — warmer
```

---

### G-5: StudioScene `_open()` — separator màu đẹp hơn

**Fix trong `studio/components/base_scene.py`:**
- Separator line dày hơn: `stroke_width=2.0` (was 1.5)
- Thêm subtle glow bằng cách vẽ 2 lines: một dày mờ + một mỏng sáng
- Màu separator = `self.PART_COLOR` với opacity gradient trái→phải

```python
def _open(self, title: str | None = None) -> VGroup:
    t = title or self.SCENE_TITLE
    title_mob = Text(t, font=FONT_PRIMARY, font_size=SIZE_TITLE, color=INK_DARK)
    title_mob.to_edge(UP, buff=0.35)
    # Glow separator: fat dim line + thin bright line
    sep_glow = Line(LEFT * 6.5, RIGHT * 6.5,
                    stroke_color=self.PART_COLOR, stroke_width=6, stroke_opacity=0.15)
    sep_glow.next_to(title_mob, DOWN, buff=0.12)
    sep = Line(LEFT * 6.5, RIGHT * 6.5,
               stroke_color=self.PART_COLOR, stroke_width=2.0, stroke_opacity=0.85)
    sep.move_to(sep_glow)
    dot = Dot(radius=0.07, color=self.PART_COLOR)
    dot.next_to(sep, RIGHT, buff=0.1)
    header = VGroup(title_mob, sep_glow, sep, dot)
    self.play(FadeIn(title_mob, shift=0.15 * DOWN, run_time=0.5))
    self.play(ShowCreation(sep, run_time=0.5), ShowCreation(sep_glow, run_time=0.5), FadeIn(dot, run_time=0.3))
    return header
```

---

## ═══ PHASE A — INTRO SCENES ═══

### A-1: `studio/scenes/intro/i01_title_card.py`
**Class:** `I01TitleCard`

**Vấn đề:**
- Background tối (BG_TITLECARD) — OK cho title card nhưng cần force
- `particle_assemble` cần hạt đẹp hơn: trail afterglow, màu gradient cyan→gold→blue
- Chữ "BEYOND SELF-DRIVING" cần forge animation tốt hơn: trắng nóng → vàng cool

**Enhancement prompt cho Codex:**
```
Rewrite I01TitleCard.construct():

1. BACKGROUND: self.camera.background_color = "#0B1120"  (deep ink)

2. PARTICLE BURST (0-3s):
   - 200 particles, mỗi particle là Dot(radius=0.035)
   - Màu: randomize từ [CYAN_RADAR, GOLD_RICH, ACCENT_BLUE, WHITE]
   - Trajectory: burst radially từ ORIGIN, mỗi particle có TracedPath trail
     trail fade trong 0.3s (dissipating_time=0.3)
   - Run_time=1.5s cho burst phase

3. WORDMARK FORGE (3-8s):
   - Tạo Text("BEYOND SELF-DRIVING", font=FONT_PRIMARY, font_size=80, weight=BOLD)
   - Màu: bắt đầu WHITE (white-hot), animate → GOLD_RICH
   - Dùng Write với per-character lag:
     self.play(Write(wordmark, run_time=3.0, lag_ratio=0.025))
   - Sau Write: animate color WHITE → GOLD_RICH:
     self.play(wordmark.animate.set_color(GOLD_RICH), run_time=0.8)

4. SUBTITLE (8-12s):
   - "ICCV 2025 Tutorial  ·  UCLA Mobility Lab"
   - font_size=SIZE_CAPS, color=INK_LIGHT="#94A3B8"
   - FadeIn shift=UP*0.2

5. RULE LINE: 
   - Line LEFT*4.5 → RIGHT*4.5, stroke_color=GOLD_RICH, stroke_width=0.8
   - ShowCreation run_time=0.6

6. SPEAKERS: 5 names in one Text, font_size=SIZE_LABEL, color="#64748B"

7. HOLD 1.5s

8. DISSOLVE: particles fly upward (shift=UP*1.5) with FadeOut, run_time=1.2
   VGroup(wordmark, subtitle, rule, speakers).animate.set_opacity(0)
```

---

### A-2: `studio/scenes/intro/i02_the_hook.py`
**Class:** `I02TheHook` — **CRITICAL 3D SCENE**

**Vấn đề:**
- Xe trông như máy quay (vehicle_icon cũ)
- Radar shells chỉ là flat circles
- Building drop không có drama
- Blind zone không đủ visual impact
- Quote không đủ cinematics

**Enhancement prompt cho Codex:**
```
Rewrite I02TheHook với full cinematic treatment per 5_PART_GUIDE:

1. GRID (0-0.5s): 
   - NumberPlane với background_line_style stroke_color="#06B6D4", opacity=0.12, width=0.5
   - Thêm road rectangles màu "#0F1A2E" (dark navy)
   - FadeIn run_time=0.8

2. HERO CAR (0.5-1.0s):
   - Dùng vehicle_icon() MỚI (G-2 fix) với color=CYAN_RADAR
   - Car DRIVES IN từ LEFT*7: car.animate.move_to([-1.75, -0.45, 0]) run_time=0.5, rate_func=smooth
   - Thêm TracedPath trail cho car: màu CYAN_RADAR, opacity fade 0.4s

3. RADAR SHELLS (1.0-4s):
   - Dùng radar_shells_2d() MỚI (G-3 fix) — gravitational wave spacing
   - 6 shells, max_radius=3.5
   - Shells có afterglow: sau ShowCreation, animate opacity từ 0.85 → 0.0 trong 1.5s
   - Loop: shells1 lần lượt fade ra rồi mới tạo shells2 mới (continuous pulsing feel)
   
4. BUILDING DROP (1.8s):
   - Prism hoặc RoundedRectangle(width=1.4, height=1.4) màu "#E5E7EB" (light grey, không phải trắng tinh)
   - Add shadow: Ellipse dưới building, màu "#00000022", fill_only
   - Drop animation: từ y=8 xuống, squish 1.15→1.0 khi chạm đất
   - Digital dust: 16 tiny dots fly outward với FadeOut

5. BLIND ZONE (2.2s):
   - AnnularSector với arc_center tại ORIGIN (hoặc tính theo offset từ building)
   - fill_color=RED_ERROR, fill_opacity=0.22
   - Đường viền đỏ mờ: stroke_color=RED_ERROR, stroke_width=1.5, stroke_opacity=0.5
   - Không dùng move_arc_center_to() — thay bằng: 
     sector = AnnularSector(..., arc_center=[x, y, 0])

6. DISTORTION WAVES (2.2-3.0s):
   - 3-4 Arc objects cong xung quanh corner của building
   - Màu CYAN_RADAR nhạt hơn (opacity=0.4), animate từ normal → distorted shape

7. TEXT OVERLAY (3.0s):
   - fix_in_frame=True để không bị ảnh hưởng bởi camera
   - Màu "#DC2626" với soft drop shadow (background rectangle mờ)

8. COOPERATION PHASE (3.8-5.5s):
   - Car 2 màu "#2563EB" (bright blue), Car 3 màu "#7C3AED" (purple)
   - Mỗi car dùng vehicle_icon() mới
   - Interference pattern: VGroup circles with additive opacity blending
     tạo vùng sáng hơn ở nơi 3 systems gặp nhau

9. PEDESTRIAN (6.0s):
   - pedestrian_icon() với color=GREEN_FIX
   - FadeIn run_time=1.5 — chậm, dramatic
   - Thêm ambient_glow xung quanh ped: color="#22C55E", radius=0.5

10. QUOTE (7.0-9.5s):
    - "Cooperation is a physics solution,\nnot an algorithm one."
    - font_size=SIZE_TITLE, color=GOLD_RICH, weight=BOLD
    - fix_in_frame()
    - write_chiseled(quote, run_time=3.0)
    - HOLD 2.5s sau khi viết xong

11. FADE OUT (9.5-10.5s):
    - FadeOut tất cả
    - self.wait(64) để pad đến 75s total
```

---

### A-3: `studio/scenes/intro/i03_roadmap.py`
**Class:** `I03Roadmap`

**Enhancement:**
```
1. Background: "#FFFFFF" (pure white)
2. Center star: thay Dot bằng Star(n=6) hoặc Polygon 6 cạnh màu GOLD_RICH
   Star pulsing: self.play(star.animate.scale(1.3).scale(1/1.3), run_time=0.4, rate_func=there_and_back)
3. Orbital nodes: 
   - Mỗi node = Circle(radius=0.28) + số + label
   - Khi FadeIn: scale từ 0.0 → 1.0 với path_arc=PI*0.6 (orbit feel)
   - Thêm small orbit trail: Arc connecting previous node
4. Lightning trace: 
   - Dùng ShowPassingFlash thay ShowCreation
   - color=GOLD_RICH, time_width=0.4, run_time=0.4 per segment
   - Afterglow: arc lines mờ màu "#FEF3C7" opacity=0.3 để lại
5. P1 node brighten: 
   - Flash(nodes[0], color=ACCENT_BLUE, line_length=0.25, num_lines=10)
   - nodes[0][0].animate.set_fill(ACCENT_BLUE, opacity=0.45).set_stroke(ACCENT_BLUE, 3.5)
```

---

### A-4: `studio/scenes/intro/i04_bridge_to_p1.py`
**Enhancement:**
```
1. Background: "#FFFFFF"
2. Recap chips: thêm icon emoji-style (text character) ở trái mỗi chip
   "→" + recap text
3. Forward question: font_size=SIZE_H1+4, color=GOLD_RICH
   Thêm subtle glow bên dưới text: Rectangle màu "#FEF3C7" opacity=0.15
4. P2 node dot at bottom: Circle(radius=0.2) blink 3 lần rồi settle
```

---

## ═══ PHASE B — PART 1 SCENES ═══

### B-1: ALL Part 1 scenes — Global Enhancement
```
Áp dụng cho tất cả p01_s*.py:

1. Background: self.camera.background_color = "#FFFFFF" đầu construct()
2. Header separator: theo G-5 fix (glow dual-line)
3. PART_COLOR = ACCENT_BLUE = "#2563EB"
4. Tất cả Text() trên nền trắng: color=INK_DARK="#1E293B" (đủ tối, không đen thuần)
5. Pipeline blocks: stroke_width=2.5 (was 2.0), corner_radius=0.18 (was 0.15)
6. Arrows: fill_color=INK_MID, thickness=3.0 (was 2.5)
```

### B-2: `p01_s02a_genai_timeline.py`
```
1. Timeline spine: thêm gradient stroke: trái nhạt → phải đậm (dùng set_stroke với opacity array)
2. Beads: thêm glow ring bên ngoài mỗi bead: Circle(radius=r+0.08, stroke_color=color, stroke_opacity=0.3)
3. ChatGPT/GPT-4 beads: thêm Flash khi xuất hiện
4. Under-curve fill: Rectangle hoặc ParametricCurve fill màu ACCENT_BLUE opacity=0.08
5. Question text: thêm subtle border rectangle màu "#FEF3C7" opacity=0.2 làm highlight box
```

### B-3: `p01_s03a_modular.py`
```
1. Module blocks: mỗi block có icon ở trái (chữ tắt: P = perception, L = loc, v.v.)
2. Noise particle: Dot(radius=0.12) màu RED_ERROR với Flash khi xuất hiện
3. Error cascade: thay vì blocks flash đỏ, animate arrows flash RED_ERROR với ShowPassingFlash
4. Car drift: TracedPath trail, car di chuyển off-lane curve (path_arc=PI/6)
5. Failure badges: thêm "✗" icon màu RED_ERROR trước mỗi line
```

### B-4: `p01_s04a_longtail_problem.py` — CRITICAL SCENE
```
1. Background: white
2. Three failure icon cards: add border với màu RED_ERROR, shadow effect
3. Power-law curve: 
   - Dày hơn: stroke_width=3.5
   - Head region fill: polygon dưới curve màu PASTEL_BLUE opacity=0.25
   - Tail region fill: polygon màu "#FEE2E2" opacity=0.35
   - Animated: curve traces từ trái qua phải (ShowCreation)
4. "1% scenarios" label: 
   - Thêm pulsing dot at tail position
   - Label trong box viền RED_ERROR
5. Failure icons: vẽ đẹp hơn — không đơn giản geometric mà có detail:
   - Phone pedestrian: stick figure + phone icon (Text "📵" hoặc SVG-like path)
   - Traffic light: 3 circles trong rectangle
   - Snow: zig-zag dots trên rectangle
6. Key number footer: font_size=SIZE_HERO, màu RED_ERROR, Flash khi xuất hiện
```

### B-5: `p01_s05_fm_empower.py`
```
1. Hub hexagon: RegularPolygon(n=6) thay Circle — đẹp hơn, tech feel
2. Hub pulsing: ValueTracker → glow radius oscillates 0.8→1.2→0.8 continuously
3. Source chips màu sắc: mỗi chip (VFM/LLM/MLLM) có màu riêng matching type
4. Packet flow: dùng ShowPassingFlash trên arrows thay vì manual Dot animation
   - Multiple flashes staggered: LaggedStart với lag=0.05
5. "Long-tail Generalization" footer: 
   - Lớn hơn font_size=SIZE_H1, weight=BOLD
   - Thêm underline trang trí
```

### B-6: `p01_s07b_emma.py`
```
1. Chain-of-thought lines: typewriter effect đúng — Write từng dòng với lag_ratio=0.0 
   (character by character) — tạo cảm giác xe đang "nghĩ to"
2. Final action line BOLD: "Brake. Yield." — font_size lớn hơn, weight=BOLD, màu GOLD_RICH
3. Gemini box: thêm neural network nodes bên trong (5-6 dots + lines) → animate
4. Output arrows: fan out từ gemini box → 3 output blocks với animation đẹp
5. Output blocks: mỗi màu khác nhau (trajectory=GOLD, bbox=CYAN, road=PURPLE)
```

### B-7: `p01_s08a_autovla_switch.py`
```
1. Chain-of-thought box: 
   - Không dùng Rectangle — dùng RoundedRectangle với dot pattern bên trong
   - Text animate word by word: Write với lag_ratio=0.04
2. Switch icon: thêm animated toggle — Circle di chuyển từ trái → phải
3. IROS badge: thêm star icon, màu GOLD_KEY gradient
4. Gold card border: dày hơn stroke_width=3.0, thêm corner star decorations
```

### B-8: `p01_s08b_autovla_results.py`
```
1. Bars: bar_reveal animation chậm hơn run_time=0.6 mỗi bar (was implicit)
2. Gold bars có glow top: thêm Dot hoặc Rectangle nhỏ ở đỉnh mỗi gold bar
3. Counter animation: ValueTracker → rolling text như đồng hồ
4. "+10.6%" text: font_size=SIZE_H1, weight=BOLD, Flash khi settle
5. IROS badge: vị trí bottom-right thay center-bottom
```

---

## ═══ PHASE C — PART 2 SCENES ═══

### C-1: `p02_s05_radar_waves.py` — **CRITICAL HERO SCENE**
```
Đây là cảnh đẹp nhất video — cần refine kỹ nhất.

1. GRID: 
   - NumberPlane stroke_color="#06B6D4", opacity=0.15
   - Road rectangles màu "#0D1B2A" (dark navy) không phải dark grey flat

2. HERO CAR (vehicle_icon mới):
   - color=CYAN_RADAR
   - Thêm headlights: 2 Dot nhỏ màu "#FEF08A" ở đầu xe
   - Thêm TracedPath trail khi xe lái vào

3. RADAR SHELLS (dùng radar_shells_2d() MỚI):
   - n_shells=7 cho hero
   - shells KHÔNG phải static — chúng disappear rồi respawn tạo continuous wave:
     ```python
     def pulse_waves(self, center, color, n_cycles=3):
         for _ in range(n_cycles):
             shells, anim = radar_shells_2d(center, color=color, n_shells=5)
             self.play(anim, run_time=1.2)
             self.play(FadeOut(shells, run_time=0.8))
     ```
   
4. BUILDING:
   - Dùng RoundedRectangle(width=1.3, height=1.3) thay Prism (nếu Prism không có)
   - Màu "#D1D5DB" với gradient stroke "#9CA3AF"
   - Drop shadow: Ellipse dưới, màu "#00000018", fill_opacity=1
   - Squish: scale(1.08) → scale(1/1.08) in 0.2s khi chạm đất
   - Digital dust: 12 tiny dots fly out với FadeOut

5. BLIND ZONE:
   - Polygon thay AnnularSector (tránh move_arc_center_to)
   - 5 vertices tạo hình wedge phía sau building
   - fill_color=RED_ERROR, fill_opacity=0.18
   - Thêm animated border: stroke pulse từ opacity 0 → 0.6 → 0

6. COOPERATION REVEAL:
   - Car 2, Car 3 (vehicle_icon mới) từ 2 hướng khác nhau
   - Mỗi car có color personality: blue, purple
   - 3 shell systems overlap: additive blending vùng overlap sáng hơn

7. INTERFERENCE PATTERN (quan trọng nhất):
   - KHÔNG chỉ là vòng tròn overlap
   - Tạo interference_pattern() với concentric_shells từ 3 centers
   - Vùng overlap: tạo thêm Dot cluster nhỏ màu WHITE opacity=0.15
     (simulate constructive interference)
   - Thêm AnimationGroup flashing ở các nút interference

8. PEDESTRIAN:
   - Fade từ opacity=0 → 1, run_time=2.0 (rất chậm = dramatic materializing)
   - Khi fully visible: Flash(ped, num_lines=8, line_length=0.2)
   - Thêm ambient_glow(ped, color=GREEN_FIX, radius=0.6)

9. QUOTE:
   - font_size=SIZE_TITLE=56, màu GOLD_RICH, weight=BOLD
   - fix_in_frame() 
   - write_chiseled(quote, run_time=3.5)  — chậm hơn
   - self.wait(2.5)  — PHẢI giữ đủ 2.5s

10. CAMERA TILT:
    - self.play(self.frame.animate.reorient(-15, 65), run_time=2.5) — smoother
```

### C-2: `p02_s02a_119m.py`
```
1. Counter: chạy chậm lúc đầu, accelerate về cuối (rate_func=smooth)
2. Màu counter: đổi dần từ INK_MID → RED_ERROR khi số tăng
3. Khi settle 1,190,000: Flash lớn + camera shake nhẹ
   self.play(ApplyFunction(lambda m: m.shift(0.05*RIGHT).shift(0.05*LEFT), num_mob))
4. Caption "94% due to human error": fade in chậm bên dưới
```

### C-3: `p02_s09_v2xpnp_arch.py`
```
1. 3-tier architecture: vẽ theo vertical flow (top → mid → bottom)
   Tier 1: 4 agents (2 cars + 2 RSU) arranged horizontally
   Tier 2: attention mechanism box (center, lớn)
   Tier 3: 3 output blocks horizontal
2. Agent icons: vehicle_icon() mới cho cars, rsu_icon() cho RSU
3. Packet swarm: Dots fly từ agents → attention → outputs (LaggedStart)
4. Attention arcs: ShowPassingFlash trên arcs, nhiều arcs staggered
5. SOTA stamps: contribution_badge ở góc mỗi output block
```

### C-4: `p02_s11b_turbotrain_solution.py`
```
1. Contour landscape: 5 Ellipse rings centered at optimum point
   Colors: từ RED_ERROR (outer) → ACCENT_AMBER → GREEN_FIX (center)
2. Gradient arrows TRƯỚC TurboTrain: 3 arrows tug từ starting point → 3 hướng khác nhau
   Animate: arrows jitter/conflict: small random rotate oscillation
3. WITHOUT path: zigzag VMobject với stroke_color=RED_ERROR opacity=0.7
4. WITH TurboTrain: smooth spiral VMobject, stroke_color=GREEN_FIX
   Spiral xuất hiện với ShowCreation run_time=3.0
5. Counter: "120 → 45 epochs" với roll animation
```

### C-5: `p02_s12_riskmap.py`
```
1. Road: Rectangle với lane markings (dashed white lines)
2. Heatmap: thay 1 solid zone bằng nhiều overlapping circles với varying opacity
   heat_blobs tại các vị trí nguy hiểm, radius từ 0.3 đến 1.2
3. Ego car: vehicle_icon() mới, TracedPath trail màu GOLD_RICH
4. Risk field dynamic: khi car khác swerve → heat_blob expand + pulsing
5. Ego trajectory: CubicBezier path "tránh" hot zones như nước chảy quanh đá
6. Quote: fix_in_frame() ở bottom
```

---

## ═══ PHASE D — PART 3 SCENES ═══

### D-1: `p03_s04b_space_calibration.py`
```
1. Point clouds: thêm color coding — vehicle cloud=ACCENT_BLUE, infra cloud=ACCENT_GREEN
   Mỗi dot có slight glow: glow ring bên ngoài opacity=0.2
2. Matrix: larger font trong matrix entries: R màu PURPLE, t màu GOLD_RICH
   Thêm bracket glow animation khi matrix flies in
3. Transform animation: 
   - Thay vì 2 arrows → 1 merged cloud
   - Animate cloud_v di chuyển transform (rotate+translate) vào merged position
   - Trực quan như LinearTransformation
4. Ghost object: thêm ✗ icon rõ ràng hơn, pulsing red
```

### D-2: `p03_s07_kalman_filter.py`
```
1. 3 streams visual:
   - GNSS: WIDE stream (nhiều dots hàng ngang) + periodic gaps (building blocks màu dark)
   - IMU: narrow fast stream + dots drift slightly off-axis khi đi từ trái → phải
   - LiDAR: isolated pulses (dot, pause, dot, pause) — không continuous
2. Confluence node:
   - Circle lớn hơn radius=0.4, stroke_color=GREEN_FIX, stroke_width=2.5
   - ValueTracker controlled glow: opacity oscillates
   - 3 arrows vào node từ 3 hướng animate
3. Output stream: WIDER, màu GREEN_FIX solid, denser dots
4. Label markup: dùng Text với <span> markup cho từng Hz label màu riêng
```

### D-3: `p03_s08_cooperfuse.py`
```
1. Gaussian ellipses: n_rings=6 (was 4), thêm inner ring opacity cao hơn
   Tạo feel như Gaussian distribution thật sự
2. NMS side: thêm confidence score labels (0.82, 0.73)
   Red X animation: Draw X từng line, không instant
3. CooperFuse side: 
   - Animate 2 ellipses MULTIPLY: scale nhỏ lại khi "nhân" với nhau
   - Result ellipse: animate từ 0 scale → full với bounce:
     self.play(GrowFromCenter(result, run_time=1.0, rate_func=overshoot))
4. Math annotation: "P(A∩B) ∝ P(A)·P(B)" dạng Tex bên cạnh
```

### D-4: `p03_s12_digital_twin.py`
```
1. Scan line effect: thicker Line + glow (2 parallel lines, outer dim outer bright)
   Vùng đã scan: tint overlay màu CYAN_RADAR opacity=0.08 trailing behind scanline
2. Real side icons: màu #94A3B8 (slate, "real world feel")
3. Twin side icons: wireframe style — stroke_only, no fill, màu CYAN_RADAR
4. Sync movement: animate cả 2 sides move đồng thời với same delta
5. "100ms lag" annotation: stopwatch icon (text "⏱") + số
```

---

## ═══ PHASE E — PART 4 SCENES ═══

### E-1: `p04_s04_coopre_masked.py` — HERO #1
```
1. BEV Grid (8×8):
   - Mỗi cell: Square với rounded corners (corner_radius=0.04)
   - Màu gradient: cells gần center sáng hơn cells ngoài rìa
   - Grid lines subtle: stroke opacity=0.4

2. Agents:
   - vehicle_icon() MỚI — top-down car đẹp
   - LiDAR beams: Line + DashedLine + animated pulse:
     LiDAR beam = ShowPassingFlash(Line(...), time_width=0.5, run_time=2.0, rate_func=linear)
     Repeat nhiều lần (n_cycles=3)

3. Masking (40% voxels):
   - LaggedStart với lag_ratio=0.04 (chậm hơn để puzzle feel)
   - Màu masked cells: từ ACCENT_BLUE → "#1E293B" (nearly dark), opacity=0.12
   - Thêm subtle pattern trên masked cells: dot in center màu tối

4. Reconstruction (HERO BEAT):
   - Particles = Dot(radius=0.05, color=ACCENT_TEAL)
   - Path = CubicBezier với mid-control points: mỗi particle có arc riêng
   - Khi particle arrive: voxel FLASH (Flash(cell, num_lines=6, line_length=0.08))
     rồi animate từ dark → PASTEL_TEAL → ACCENT_TEAL full opacity
   - Timing: mỗi reconstruction = 0.6s, stagger giữa các cell
   - TOTAL reconstruction block: ~3.5s để "puzzle complete" feel

5. Result bars: thêm value labels trên đỉnh mỗi bar
   "+4% AP" counter: số ROLL up, cuối Flash màu GOLD_RICH

6. Badges: contribution_badge với màu GOLD_KEY, animation: FadeIn scale từ 0.5→1.1→1.0
```

### E-2: `p04_s08_quantv2x.py` — HERO #2
```
1. Big FP32 blob:
   - RoundedRectangle(width=3.5, height=2.2) màu RED_ERROR opacity=0.15
   - Thêm animated noise texture: VGroup of small Dots flickering inside blob
   - Label "100 MB · FP32" Bold, màu RED_ERROR

2. V2X channel BLOCKED:
   - 2 parallel Lines như ống dẫn
   - Packets (Dots) cố đi qua nhưng "bounce back" khi gặp blob
     packet.animate.move_to(mid).move_to(start) — suggest blocked

3. 3-stage pipeline:
   - Animate từng stage BUILD DOWN: Stage1 → arrow → Stage2 → arrow → Stage3
   - Mỗi stage: thêm small icon ở góc (code symbol, book, ?)

4. SQUEEZE ANIMATION (CLIMAX):
   - Blob animate: scale 0.1 trong x và y, đồng thời
     self.play(
         blob.animate(run_time=2.5, rate_func=smooth)
              .stretch(0.1, 0).stretch(0.1, 1)
              .set_fill(GREEN_FIX, 0.8)
              .set_stroke(GREEN_FIX, 2)
     )
   - Màu transition: interpolate từ RED_ERROR → GREEN_FIX
   - Particles flying off blob khi squeeze: small bits fly outward, fade

5. Channel OPENS:
   - Animate channel lines từ RED_ERROR → GREEN_FIX (color change)
   - Packets flow: 6 packets fly through smoothly, MoveAlongPath

6. "300×" counter:
   - font_size=96, weight=BOLD, màu GOLD_RICH
   - Roll up từ 0→300 với tracker
   - Final Flash(kn, num_lines=16, line_length=0.5)

7. Pad to 65s: active beats ~12s, self.wait(53) at end
```

### E-3: `p04_s05_turbotrain_landscape.py`
```
1. Contour rings: 5 Ellipse, màu gradient từ pale → saturated về center
   OUTER: stroke_color="#FCA5A5" (pale red)
   MIDDLE: stroke_color=ACCENT_AMBER
   CENTER: stroke_color=GREEN_FIX
2. Gold star at optimum: star polygon (RegularPolygon n=5 rotated), màu GOLD_RICH
   Pulsing glow: Flash(star, ...) repeat 2×
3. Gradient conflict arrows: 3 Arrows màu riêng, jitter animation:
   self.play(Rotate(arr, 10*DEGREES, about_point=origin, rate_func=there_and_back), run_time=0.3)
   Repeat 3× để thấy conflict
4. Smooth spiral: stroke_color=GREEN_FIX, stroke_width=3.0
   ShowCreation run_time=3.5 để trajectory slow enough to follow
5. Counter "120 → 45": thêm animated strikethrough trên "120" khi "45" xuất hiện
```

---

## ═══ PHASE F — PART 5 + FINALE ═══

### F-1: `p05_s07_zombie_to_alive.py` — EMOTIONAL MOMENT
```
1. Zombie squares: thêm zombie motion — slight random wobble trong khi moving:
   z.animate.shift(dir).rotate(rng.uniform(-5, 5)*DEGREES)
2. Pass-through: khi 2 squares overlap → briefly highlight collision point màu RED_ERROR
3. FREEZE: camera subtle zoom in (frame.animate.set_height(7), run_time=0.5)
   Dim overlay: màu "#00000088" không phải "#00000045"
4. TRANSFORM (climax):
   - Mỗi Square → pedestrian_icon mới: animate với Flash khi transform
   - Màu transition: gray → ACCENT_PINK qua interpolate
   - 1 second delay giữa các transforms (LaggedStart lag=0.08)
5. Organic movement:
   - Paths không straight line — CubicBezier với random control points
   - 2 pedestrians có avoidance: khi trajectories gần nhau, curve away
6. Final state: pedestrians arranged dạng cluster groups (2-3 người) 
   — simulate natural pedestrian social grouping
7. "Human-Centric Physical AI" text: font_size=SIZE_H1, màu GREEN_FIX
   write_chiseled(lbl, run_time=1.5)
   self.wait(2) — giữ đủ 2s
```

### F-2: `p05_s09_living_city.py` — **VISUAL CLIMAX**
```
Đây là cảnh đỉnh điểm của cả video.

1. CITY GRID:
   - Thêm road intersections rõ ràng hơn: 2 crossed Rectangle (dark navy)
   - Block buildings: VGroup of small squares scattered quanh intersections
     màu "#374151" opacity=0.6 — suggest urban context
   - Grid lines: thin, CYAN_RADAR opacity=0.12

2. PHASE 1 — 6 AGENT TYPES (t=0→15s):
   Mỗi type có distinct visual personality:
   
   CARS (t=1s): vehicle_icon() mới, color=ACCENT_BLUE
     - 6 cars (not 4), positioned trên roads
     - Thêm tiny headlight dots màu "#FEF08A"
   
   ROBOTS (t=3s): vehicle_icon() scale=0.55, color="#10B981" (green smaller cars)
     - 4 robots, trên sidewalk areas
   
   WHEELCHAIRS (t=5s): pedestrian_icon scale=0.85, color=ACCENT_PINK
     - Thêm small circle "wheel" dưới pedestrian icon
     - 3 wheelchairs
   
   PEDESTRIANS (t=7s): pedestrian_icon scale=0.8, color=GOLD_KEY
     - 6 pedestrians, các vị trí khác nhau
     - Random very slight oscillation (subtle walking animation)
   
   RSUs (t=9s): rsu_icon scale=1.2, color=ORANGE_INFRA
     - Flash khi xuất hiện (Flash(rsu, num_lines=12))
     - ambient_glow(rsu, color=ORANGE_INFRA, radius=0.8)
   
   DRONES (t=11s): drone_icon scale=1.0, color="#F1F5F9" (light)
     - FadeIn từ trên xuống (shift=DOWN*0.4)

3. PHASE 2 — V2X WEB (t=15→30s):
   - Links: LaggedStart lag_ratio=0.008 (rất chậm = web building feel)
   - Link opacity=0.3 (không quá dày)
   - Thêm packet pulses: ShowPassingFlash trên các links
     LaggedStart(*(ShowPassingFlash(l.copy()...) for l in links), lag_ratio=0.02)
   
   RADAR SHELLS (parallel):
   - Từ mỗi RSU: pulse_waves() continuous (3 cycles)
   - Interference: ở nơi 3 RSU coverage overlap → thêm bright spot
     Dot(radius=0.12, color=CYAN_RADAR, opacity=0.4) tại các giao điểm

4. CAMERA ORBIT:
   - self.play(self.frame.animate.reorient(5, 60, 0), run_time=15, rate_func=linear)
   - Add ambient rotation: self.frame.add_ambient_rotation(0.3 * DEG) for smoother

5. PHASE 3 — PULLBACK (t=30→50s):
   - self.play(self.frame.animate.set_height(16), run_time=10, rate_func=smooth)
   - City không fade — stays alive in background
   - Camera rests on wide isometric view showing full city
   - self.wait(8) — city breathing
   - FULL FADEOUT: run_time=2.0

6. PERFORMANCE: nếu render > 10 phút:
   - Giảm links xuống: chỉ connect RSU → nearby agents (3 RSU × 8 agents = 24 links)
   - Giảm pulse cycles: n_cycles=2 thay 3
   - Radar shells: n_shells=3 thay 4 per RSU
```

### F-3: `p05_s11_final_frame.py` — CLOSING
```
1. Background dots: nhiều hơn (60 dots), kích thước đa dạng 0.03-0.07
   Animate subtle drift: dots slowly drift upward during entire scene
   self.play(bg_dots.animate(run_time=45, rate_func=linear).shift(UP * 0.8))

2. THREE LINES timing QUAN TRỌNG:
   Line 1: "Beyond Self-Driving." 
     - font_size=SIZE_TITLE, weight=BOLD, color=GOLD_RICH
     - write_chiseled(l1, run_time=2.5)
     - self.wait(1.0)  ← 1 giây đúng
   Line 2: "Not just smarter cars."
     - font_size=SIZE_TITLE, color=GOLD_RICH  
     - write_chiseled(l2, run_time=2.0)
     - self.wait(1.0)  ← 1 giây đúng
   Line 3: "A safer world."
     - font_size=SIZE_TITLE, color=GOLD_RICH, weight=BOLD
     - write_chiseled(l3, run_time=1.5)
     - self.wait(2.0)  ← 2 giây đúng

3. ROADMAP STRIP (all gold):
   - 5 dots flash in sequence: LaggedStart lag=0.08
   - Gold connector line draw L→R
   - Flash ALL 5 dots simultaneously

4. UCLA BADGE:
   - RoundedRectangle background nhạt màu "#FAFAFA" stroke="#E2E8F0"
   - Text "UCLA Mobility Lab  ·  ICCV 2025" bên trong

5. CONVERGE ENDING:
   - 100 particles (bigger n), paths có path_arc đa dạng hơn
   - Center dot: radius=0.25, pulse 2× (scale 1.5→1.0, Flash)
   - Final: self.play(FadeOut(center_dot, scale=3), run_time=0.8)
   - self.wait(1.0) — black silence at end
```

---

## ═══ PHASE G — COMPONENTS UPGRADE ═══

### G-COMPONENTS: Fixes cần apply TRƯỚC khi render lại

**Priority 1 (phải làm):**
1. `colors.py`: BG_PAPER → "#FFFFFF" (G-1)
2. `agents.py`: vehicle_icon() → proper car (G-2)
3. `signals.py`: radar_shells_2d() và radar_shells_3d() (G-3)
4. `base_scene.py`: _open() glow separator (G-5), setup() force white

**Priority 2 (quan trọng):**
5. `agents.py`: pedestrian_icon() → thêm detail (head bigger, proper arm/leg angles)
6. `agents.py`: rsu_icon() → thêm antenna glow animation
7. `signals.py`: sensor_cone() → fix move_arc_center_to bug → dùng arc_center= param
8. `annotations.py`: contribution_badge() → thêm subtle gradient fill
9. `pipeline.py`: pipeline_block() → stroke_width=2.5, add subtle shadow
10. `animations.py`: forge_text() → sửa để dùng Write + color change thay Succession

**Priority 3 (nice-to-have):**
11. `typography.py`: thêm helper `bold_text()` và `italic_text()`
12. `charts.py`: bar_reveal() → thêm value label trên đỉnh mỗi bar
13. `charts.py`: axes_deploy() → thicker tick marks

---

## ═══ RENDER ORDER ═══

Sau khi apply global fixes, render theo thứ tự này:
```
1. Render components smoke test trước: studio/scenes/_smoke_components.py
2. Intro: I-01, I-02, I-03, I-04
3. Part 1: P01-S01 → P01-S10 (các subfiles theo order)
4. Part 2: P02-S01 → P02-S14 (S05 render riêng cuối)
5. Part 3: P03-S01 → P03-S15
6. Part 4: P04-S01 → P04-S10 (S04, S08 render riêng)
7. Part 5: P05-S01 → P05-S11 (S09, S11 render riêng)
```

Render command:
```powershell
$env:PYTHONPATH = "C:\Users\admin\Downloads\ML\Lab01_3B1B"
manimgl -w -l studio/scenes/<part>/<file>.py <ClassName>
```

---

## ═══ QUICK REFERENCE — Common API Fixes ═══

```python
# BACKGROUND (phải set ở ĐẦU construct, không dựa vào setup())
self.camera.background_color = "#FFFFFF"

# VEHICLE (dùng version mới sau G-2 fix)
car = vehicle_icon(color=ACCENT_BLUE, scale=1.0)

# RADAR SHELLS (gravitational wave style sau G-3 fix)
shells, anim = radar_shells_2d(center, color=CYAN_RADAR, n_shells=6, max_radius=3.5)

# 3D CAMERA TILT (không dùng set_camera_orientation hay move_camera)
self.frame.reorient(theta_deg, phi_deg, 0)  # setup
self.play(self.frame.animate.reorient(-15, 65), run_time=2.5)  # animated

# ANNULARSECTOR (không có move_arc_center_to → dùng arc_center param)
sector = AnnularSector(
    inner_radius=0.5, outer_radius=2.5,
    start_angle=-PI/5, angle=PI/2.5,
    arc_center=np.array([x, y, 0]),  # ← thay vì move_arc_center_to
    fill_color=RED_ERROR, fill_opacity=0.2, stroke_width=0,
)

# WRITE-CHISELED cho quote moments
from studio.components import write_chiseled
self.play(write_chiseled(text_mob, run_time=3.0))
self.wait(2.5)  # PHẢI giữ hold

# FIX VGroup(*self.mobjects) bug
from manimlib import VMobject
mobs = [m for m in self.mobjects if isinstance(m, VMobject)]
self.play(*[FadeOut(m) for m in mobs])

# DOUBLE ARROW (không có DoubleArrow trong manimgl)
# Thay bằng:
gap = Arrow(start, end, fill_color=RED_ERROR, thickness=2.5, buff=0.06)

# SET_STYLE (không có trong manimgl)
# Thay bằng: truyền slant/weight vào Text() constructor
text = Text("Hello", font=..., slant=ITALIC, weight=BOLD)
```
