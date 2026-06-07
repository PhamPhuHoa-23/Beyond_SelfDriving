# STUDIO BUILD — PHASED PROMPTS
## Beyond Self-Driving · `studio/` package rebuild

> Mỗi phase là một prompt độc lập, copy-paste vào session Claude Code mới.
> Đọc context một lần, làm xong phase, render verify, đóng session.
> Mỗi prompt assume Claude đọc `OPUS_PLAN.md` và `CLAUDE.md` trước khi bắt đầu.

---

## INDEX

| Phase | Tên | Mục tiêu | Output | Est. effort |
|---|---|---|---|---|
| **0** | Discovery & Font Check | Kiểm tra font, audit references, sweep slides | `studio/PHASE0_REPORT.md` | 1 session ngắn |
| **1** | Components Foundation | Build `studio/components/` + smoke test | 10 component files render OK | 1 session lớn |
| **2** | Intro + Part 1 | I01-I04 + P01-S01..S10 | 14 scenes render -ql | 1-2 sessions |
| **3** | Part 2 (Cooperation) | P02-S01..S14, S05 là hero 3D | 14 scenes render -ql | 1 session lớn |
| **4** | Part 3 (Sim-to-Real) | P03-S01..S15 | 15 scenes render -ql | 1 session lớn |
| **5** | Part 4 (Efficiency) | P04-S01..S10 | 10 scenes render -ql | 1 session vừa |
| **6** | Part 5 + Finale | P05-S01..S11, S09 là hero 3D | 11 scenes render -ql | 1 session lớn |
| **7** | Full Render + QA | Render -qh, frame check, concat | 1 file MP4 50-60 phút | 1 session dài |
| **8** | Polish & Voiceover hooks | TTS prep, transition tuning, color grading | Voiceover-ready scenes | optional |

---

## PHASE 0 — DISCOVERY & FONT CHECK

> Mục đích: **kiếm thử duyệt thử** — verify môi trường, font, render path, reference availability TRƯỚC khi viết code thật.
> Đầu ra: một file report ngắn `studio/PHASE0_REPORT.md`, KHÔNG tạo code khác.

```
Bạn đang start một rebuild lớn cho project Manim "Beyond Self-Driving" (ICCV 2025
tutorial). Plan đầy đủ đã có ở [OPUS_PLAN.md](OPUS_PLAN.md). Đọc plan đó trước,
đặc biệt Section 1 (Design System) và Section 2 (Component Architecture).

NHIỆM VỤ PHASE 0: discovery & verification. KHÔNG viết code production trong session
này. Chỉ verify environment và viết một report.

Cụ thể, kiểm tra:

1. FONT AVAILABILITY
   - Chạy PowerShell command để liệt kê fonts có trên Windows:
     `[System.Drawing.FontFamily]::Families | Where-Object { $_.Name -match "CMU|Latin Modern|Computer Modern" }`
   - Nếu CMU Serif KHÔNG có: ghi vào report instructions để cài (CTAN cm-unicode).
   - Nếu Latin Modern Roman có: confirm fallback chain hoạt động.
   - Render một file Manim test 5 dòng (italic, bold, regular, MarkupText, MathTex)
     bằng font detected. Save kết quả vào `studio/_phase0_font_test/`.

2. MANIM ENV SANITY
   - Confirm manim version: `manim --version` (kỳ vọng 0.20.1).
   - Confirm `C:\Users\admin\miniconda3\Scripts\manim.exe` is the active binary.
   - Render scene rỗng (Scene class với 1 dot fadein) ở -ql và -qh để đo time.

3. REFERENCE FILE AUDIT
   - Confirm tồn tại các file mentioned trong SOURCE_MANIM_REFERENCE_AUDIT.md:
     * Source_manim_reference/3b1b_videos/custom/logo.py
     * Source_manim_reference/3b1b_videos/_2024/transformers/network_flow.py
     * Source_manim_reference/3b1b_videos/_2026/hairy_ball/model3d.py
     * Source_manim_reference/welchlabs_videos/once_useful_constructs/light.py
     * Source_manim_reference/welchlabs_videos/_2026/vla/p31_61_1.py
     * Source_manim_reference/welchlabs_videos/_2025/generalization/p8_15.py
   - Cho mỗi file: confirm exists, đọc 20 dòng đầu, log line count.
   - Nếu thiếu file nào: ghi vào risk section của report.

4. SLIDES SANITY
   - Confirm materials/slides/Part 1.pdf .. Part 5.pdf tồn tại.
   - Confirm materials/scripts/script_part1..5.md tồn tại.
   - Không cần đọc nội dung — chỉ verify.

5. OPENGL 3D RENDER CHECK (quan trọng cho I-02, P02-S05, P05-S09)
   - Render một ThreeDScene đơn giản (Sphere + camera move) với --renderer=opengl
     ở -ql.
   - Confirm output MP4 sinh ra ở media/videos/.../*.mp4.
   - Nếu OpenGL renderer crash: ghi vào risk và đề xuất fallback (cairo
     ThreeDScene).

6. WRITE REPORT
   - Path: studio/PHASE0_REPORT.md
   - Sections: Font status / Manim env / References available / Slides / OpenGL /
     Decisions (gồm: dùng font nào, OpenGL OK chưa, gì cần cài thêm).
   - Cuối file: "READY FOR PHASE 1: YES/NO" + lý do.

CONSTRAINTS:
- KHÔNG tạo studio/__init__.py hay component files trong phase này.
- KHÔNG modify beyond/ package.
- Chỉ tạo studio/PHASE0_REPORT.md và studio/_phase0_font_test/ (test artifacts).
- Nếu phát hiện issue blocker → STOP và hỏi user trước khi tiếp tục.
```

---

## PHASE 1 — COMPONENTS FOUNDATION

> Mục đích: build toàn bộ `studio/components/` package. Một session lớn, một lần.

```
Đọc trước:
- OPUS_PLAN.md Section 2 (Component Architecture) — toàn bộ API specs
- OPUS_PLAN.md Section 1 (Design System) cho color/font constants
- studio/PHASE0_REPORT.md cho font decision + OpenGL status
- SOURCE_MANIM_REFERENCE_AUDIT.md cho reference table
- Reference files cụ thể:
  * Source_manim_reference/3b1b_videos/_2024/transformers/network_flow.py (lines 5-260)
  * Source_manim_reference/3b1b_videos/_2026/hairy_ball/model3d.py (lines 68-310)
  * Source_manim_reference/welchlabs_videos/once_useful_constructs/light.py (lines 32-220)
  * Source_manim_reference/welchlabs_videos/_2026/vla/p31_61_1.py (line 214 make_embedding_row)

NHIỆM VỤ PHASE 1: Build toàn bộ studio/components/ + studio/config.py.

FILE STRUCTURE TO CREATE:
  studio/
  ├── __init__.py                  (empty)
  ├── config.py                    (BG_PAPER default, FONT decision logic, quality)
  └── components/
      ├── __init__.py              (re-export everything)
      ├── colors.py                (Section 1.1 palette as Final[str] constants)
      ├── typography.py            (detect_primary_font, FONT_PRIMARY, sizes, text/markup/math helpers)
      ├── base_scene.py            (StudioScene + Studio3DScene with _open/_close/_roadmap_strip)
      ├── pipeline.py              (pipeline_block, pipeline_row, pipeline_arrow, pipeline_flow)
      ├── charts.py                (axes_deploy, bar_reveal, curve_trace, scatter_rain)
      ├── agents.py                (vehicle_icon, pedestrian_icon, rsu_icon, rsu_tower_3d, drone_icon, agent_trail)
      ├── signals.py               (radar_shells_2d, radar_shells_3d, sensor_cone, v2x_link, ambient_glow, interference_pattern)
      ├── annotations.py           (callout, thought_bubble, contribution_badge, key_number, failure_icon)
      ├── animations.py            (forge_text, particle_assemble, fivefold_assemble, scan_reveal, dust_dissolve, write_chiseled)
      └── layout.py                (zone helpers + two_column, three_column, grid_4)

Theo từng module:
- Đúng signature như OPUS_PLAN.md Section 2.2 quy định.
- KHÔNG hardcode hex literals trong components khác colors.py.
- Mỗi function adapted từ reference: thêm comment `# Pattern adapted from: <path>:<line>`.
- Mỗi function có 1 line docstring tối đa. KHÔNG multi-paragraph.
- Type hints đầy đủ.

SMOKE TEST:
- Create studio/scenes/_smoke_components.py với 1 Scene class hiển thị:
  * Title text qua typography.text()
  * Multi-color MarkupText qua typography.markup()
  * 1 pipeline_block + 1 pipeline_arrow
  * 1 axes_deploy + 1 curve_trace
  * 1 vehicle_icon + 1 pedestrian_icon + 1 rsu_icon
  * 1 radar_shells_2d animation
  * 1 ambient_glow
  * 1 callout với leader line
  * 1 forge_text
  * 1 contribution_badge
- Render: manim -ql studio/scenes/_smoke_components.py SmokeComponents
- Output phải show mọi component trong 1 frame mosaic, không error.

OPENGL SMOKE TEST (nếu Phase 0 confirm OpenGL OK):
- studio/scenes/_smoke_3d.py: Studio3DScene với 1 rsu_tower_3d + radar_shells_3d.
- Render: manim -ql --renderer=opengl studio/scenes/_smoke_3d.py Smoke3D

CONSTRAINTS:
- KHÔNG viết scene production nào (intro / parts đợi Phase 2+).
- KHÔNG modify beyond/.
- Mọi color hex chỉ tồn tại trong colors.py.
- Test smoke render PHẢI pass trước khi đóng session.
- Sau khi smoke pass: log "PHASE 1 DONE — components ready" trong commit message
  hoặc final response.
```

---

## PHASE 2 — INTRO + PART 1

> 14 scenes. Đây là phase "đầu tiên có lửa" — first 3D hero (I-02) + first gallery cards (P01-S07a/b/c) + first chart reveal (P01-S04a).

```
Đọc trước:
- OPUS_PLAN.md Section 3 (rows I-01 → P01-S10) và Section 4 (detail blocks tương ứng)
- materials/scripts/script_part1.md (full)
- 5_PART_GUIDE.md sections I-01, I-02, I-03, P1-01 đến P1-08
- studio/components/ (đã build ở Phase 1)
- References:
  * Source_manim_reference/3b1b_videos/custom/logo.py (toàn bộ — particle assembly)
  * Source_manim_reference/3b1b_videos/_2026/hairy_ball/model3d.py (3D shells)
  * Source_manim_reference/welchlabs_videos/_2026/vla/p31_61_1.py (VLA architectures)
  * Source_manim_reference/welchlabs_videos/_2025/generalization/p8_15.py (long-tail curve)

NHIỆM VỤ PHASE 2: Implement 14 scenes:
  studio/scenes/intro/
    ├── __init__.py
    ├── i01_title_card.py            (I-01)
    ├── i02_the_hook.py              (I-02 — 3D hero, OpenGL, 75s)
    ├── i03_roadmap.py               (I-03)
    └── i04_bridge_to_p1.py          (I-04)
  studio/scenes/part01/
    ├── __init__.py
    ├── p01_s01_title.py             (P01-S01)
    ├── p01_s02a_genai_timeline.py   (P01-S02a)
    ├── p01_s02b_fm_definition.py    (P01-S02b)
    ├── p01_s03a_modular.py          (P01-S03a)
    ├── p01_s03b_e2e.py              (P01-S03b)
    ├── p01_s03c_hybrid.py           (P01-S03c)
    ├── p01_s04a_longtail_problem.py (P01-S04a)
    ├── p01_s04b_longtail_insight.py (P01-S04b)
    ├── p01_s05_fm_empower.py        (P01-S05)
    ├── p01_s06_vla_roadmap.py       (P01-S06)
    ├── p01_s07a_bevdriver.py        (P01-S07a)
    ├── p01_s07b_emma.py             (P01-S07b)
    ├── p01_s07c_drivevlm.py         (P01-S07c)
    ├── p01_s08a_autovla_switch.py   (P01-S08a)
    ├── p01_s08b_autovla_results.py  (P01-S08b)
    ├── p01_s09_takeaways.py         (P01-S09)
    └── p01_s10_bridge_to_p2.py      (P01-S10)

THỨ TỰ ƯU TIÊN (làm I-02 SỚM để confirm 3D pipeline):
  1. I-01, I-03, I-04 (2D title cards, đơn giản)
  2. I-02 (3D hero) — nếu fail, fallback sang cairo ThreeDScene đơn giản hơn
  3. P01-S01, S02a, S02b
  4. P01-S03a/b/c (3 architectures — đảm bảo split rõ ràng)
  5. P01-S04a/b (long-tail — phải có "wow moment")
  6. P01-S05, S06
  7. P01-S07a/b/c (VLA gallery — đọc p31_61_1.py kỹ)
  8. P01-S08a/b (AutoVLA climax)
  9. P01-S09, S10 (recap + bridge)

PER-SCENE STRUCTURE:
  - Top of file: SCRIPT = """<EN voiceover từ Section 4>"""
  - Class name: PascalCase tương ứng filename (e.g., I01TitleCard, P01S04ALongtailProblem)
  - Inherit StudioScene hoặc Studio3DScene
  - PART_NUM = 0 (intro) hoặc 1 (Part 1)
  - PART_COLOR = ACCENT_BLUE, PART_PASTEL = PASTEL_BLUE cho Part 1
  - SCENE_TITLE = title viết hoa thường, ngắn
  - construct() gọi self._open(self.SCENE_TITLE) đầu, self._close() cuối
  - Mỗi animation beat tách bằng comment ngắn 1 dòng (KHÔNG block comments)
  - Imports luôn từ studio.components, KHÔNG từ manim trực tiếp với màu/font

RENDER VERIFICATION:
  - Sau mỗi scene: render -ql, check output MP4 sinh ra, không error
  - Sau cả phase: render frame check tại 35/60/85% cho I-02, P01-S04a, P01-S08a
    (3 hero scenes của phase)
  - Save check frames vào studio/_phase2_check_frames/

CONSTRAINTS:
- KHÔNG modify studio/components/ (đã frozen sau Phase 1). Nếu cần thêm helper → ghi
  vào TODO note ở cuối session, xử lý ở Phase 7.
- KHÔNG copy code từ beyond/ — chỉ tham khảo nội dung (text, key numbers).
- KHÔNG quote 3B1B logo/character branding.
- Mỗi reference adaptation phải có comment `# Pattern adapted from: ...`.
- Hold timings (3s quote, 2.5s insight) PHẢI tôn trọng — không rút ngắn.

DONE WHEN:
- Tất cả 18 file scene + 2 __init__ tạo xong
- manim -ql từng scene chạy không error
- 3 hero frame-check frames trông đúng theo Section 4 detail blocks
- Final response log "PHASE 2 DONE — Intro + Part 1, 18 scenes"
```

---

## PHASE 3 — PART 2 (COOPERATIVE PERCEPTION)

> 14 scenes. **P02-S05 là cảnh wow nhất video** — full 3D radar gravitational waves, 75s, không được làm tệ.

```
Đọc trước:
- OPUS_PLAN.md rows P02-S01 → P02-S14 và detail blocks tương ứng
- materials/scripts/script_part2.md (full)
- 5_PART_GUIDE.md sections P2-01 đến P2-09 (đặc biệt P2-04 — radar waves)
- References:
  * Source_manim_reference/3b1b_videos/_2026/hairy_ball/model3d.py:260 RadioBroadcast
    (xem :275 update_shells)
  * Source_manim_reference/3b1b_videos/_2023/optics_puzzles/adding_waves.py
    (interference pattern)
  * Source_manim_reference/welchlabs_videos/once_useful_constructs/light.py:95 Spotlight
  * Source_manim_reference/3b1b_videos/_2024/transformers/network_flow.py:161
    play_simple_attention_animation
  * Source_manim_reference/welchlabs_videos/_2025/backprop_3/geometry_while_learning_2.py
  * Source_manim_reference/welchlabs_videos/once_useful_constructs/region.py:50

NHIỆM VỤ PHASE 3: 14 scenes trong studio/scenes/part02/.
  p02_s01_title.py
  p02_s02a_119m.py
  p02_s02b_waymo_reduce.py
  p02_s03_e2e_evolution.py
  p02_s04a_occlusion_problem.py
  p02_s05_radar_waves.py             ← THE HERO. 3D OpenGL. 75s. Special care.
  p02_s06_related_works.py
  p02_s07_research_gaps.py
  p02_s08_three_questions.py
  p02_s09_v2xpnp_arch.py
  p02_s10_v2xpnp_dataset.py
  p02_s11a_turbotrain_problem.py
  p02_s11b_turbotrain_solution.py
  p02_s12_riskmap.py
  p02_s13_summary.py
  p02_s14_bridge_to_p3.py

THỨ TỰ:
  1. P02-S01 title + S02a/b counter scenes (warm up)
  2. P02-S03 timeline + S04a problem (set up the climax)
  3. **P02-S05 RADAR WAVES** — làm KỸ. Đọc lại 5_PART_GUIDE.md section P2-04 (chứa
     timing per second). Render -ql nhiều lần, frame-check tại 1.0/2.2/4.3/6.0/7.0s
     để verify từng beat. Pattern adapted from model3d.py:260 — port shells qua CE
     bằng ValueTracker + LaggedStart(*[FadeIn(Circle(radius=r)) for r in radii]).
     Quote write-chiseled GOLD italic hold 2.5s — KHÔNG rút ngắn.
  4. P02-S06 related works chain
  5. P02-S07 research gaps
  6. P02-S08 three questions card layout
  7. P02-S09 V2XPnP architecture — attention arcs adapted from network_flow.py:161
  8. P02-S10 dataset stats
  9. P02-S11a/b TurboTrain — landscape adapted from backprop_3
  10. P02-S12 RiskMap heatmap — region.py:50 plane_partition
  11. P02-S13/14 recap + bridge

PHẦN P02-S05 (RADAR WAVES) DETAIL:
  - Studio3DScene phi=70°, theta=-30° initial
  - 3 shell systems (cyan / blue / purple), không đồng thời mà delayed
  - Building drop với squish (scale 1.1→1.0 + dust particle helper)
  - Blind zone = AnnularSector hoặc Polygon với fill_opacity 0.3 RED_ERROR
  - Interference: tại 4.3s, KHÔNG triệt tiêu mà show 3 shell families overlap với
    additive opacity (use VGroup of shell sets, opacity blending)
  - Pedestrian silhouette: agents.pedestrian_icon, fade in từ 0 → 1 trong 1.5s
  - Camera tilt: self.move_camera(phi=65°, theta=-15°, run_time=2.0)
  - Quote: animations.write_chiseled, GOLD_RICH italic, font_size=SIZE_TITLE
  - End: FadeOut tất cả, KHÔNG để leak vào P02-S06

CONSTRAINTS:
- Như Phase 2 (không modify components, không copy beyond/, comment reference per adaptation)
- P02-S05 nếu render -qh > 5 phút cho 75s output: optimize trước khi đóng session
  (giảm shell count, dùng cached Circle thay Sphere nếu cần)
- KHÔNG bỏ qua hero quote moment — đó là khoảnh khắc cảm xúc của Part 2

DONE WHEN:
- 14 scenes render -ql không error
- P02-S05 frame check tại 1.0s/2.2s/4.3s/6.0s/7.0s — save vào _phase3_hero_check/
- Final response log "PHASE 3 DONE — Part 2, 14 scenes incl. radar-waves hero"
```

---

## PHASE 4 — PART 3 (SIM-TO-REAL)

> 15 scenes. Phase engineering nặng nhất — calibration matrix, Kalman filter, CooperFuse Gaussian beauty.

```
Đọc trước:
- OPUS_PLAN.md rows P03-S01 → P03-S15 và detail blocks
- materials/scripts/script_part3.md (full)
- References:
  * Source_manim_reference/welchlabs_videos/once_useful_constructs/vector_space_scene.py:204
    LinearTransformationScene
  * Source_manim_reference/welchlabs_videos/once_useful_constructs/linear_algebra.py:32
    vector_coordinate_label
  * Source_manim_reference/3b1b_videos/_2018/uncertainty.py (Kalman / Gaussian)
  * Source_manim_reference/welchlabs_videos/once_useful_constructs/region.py
  * Source_manim_reference/3b1b_videos/_2026/hairy_ball/model3d.py:68 RadioTower
  * Source_manim_reference/welchlabs_videos/once_useful_constructs/graph_theory.py:56
  * Source_manim_reference/3b1b_videos/_2023/optics_puzzles/wave_machine.py

NHIỆM VỤ PHASE 4: 15 scenes trong studio/scenes/part03/.
  (xem OPUS_PLAN.md Section 3 cho danh sách đầy đủ)

THỨ TỰ:
  1. P03-S01 title + S02 sim-real gap (split-world với lightning crack)
  2. P03-S03 smart intersection — UCLA campus map + all sensors light up
  3. P03-S04a time calibration (50ms→83cm)
  4. P03-S04b space calibration — matrix-fly-in MATH_REVEAL — adapted from
     LinearTransformationScene
  5. P03-S05 data collection routes
  6. P03-S06 localization role (no-loc → worse than single)
  7. P03-S07 Kalman three rivers — UNCERTAINTY_CLOUD — adapted from uncertainty.py
  8. P03-S08 CooperFuse Gaussian beauty — math elegance, không rút gọn
  9. P03-S09 V2X-ReaLO compression
  10. P03-S10 OpenCDA-ROS bridge
  11. P03-S11 SimBoost loop
  12. P03-S12 digital twin scan reveal
  13. P03-S13 InfraX cards
  14. P03-S14/15 recap + bridge

PHẦN P03-S07 (KALMAN THREE RIVERS) DETAIL:
  - 3 rivers = 3 ParametricFunction streams entering từ left/top/bottom
  - GNSS (BLUE_ELECTRIC, 5Hz): wide stream, periodic blocks bằng small building icons
  - IMU (AMBER, 100Hz): narrow fast stream, gradually tilt off-axis
  - LiDAR (GREEN, 1Hz): pulsing dots not continuous
  - Confluence at center node — ambient_glow + ValueTracker pulse
  - Output single stream rightward, GREEN_FIX smooth 100Hz

PHẦN P03-S08 (COOPERFUSE) DETAIL:
  - 2 bounding boxes offset
  - 2 Gaussian ellipses (use Ellipse với fill_opacity gradient hoặc ParametricSurface)
  - Left side: NMS discards smaller-confidence — fadeout với red X
  - Right side: Gaussian multiply visualization — overlay two ellipses, intersection
    Region tinted GREEN_FIX, new tighter Ellipse crystallizes
  - Tham khảo uncertainty.py cho idiom Gaussian fade

CONSTRAINTS:
- Math scenes (S04b, S07, S08) KHÔNG đơn giản hóa — math beauty là điểm bán hàng
- Components nào thiếu (Gaussian helper, point-cloud helper) → tạo scene-local
  helper trong file scene đó. Đừng modify studio/components/.
- TODO list các helpers cần promote lên components/ → ghi vào response cuối session,
  xử lý Phase 7

DONE WHEN:
- 15 scenes render -ql không error
- Frame check P03-S04b (matrix), S07 (kalman), S08 (Gaussian) — save vào
  _phase4_math_check/
- Final response log "PHASE 4 DONE — Part 3, 15 scenes"
```

---

## PHASE 5 — PART 4 (EFFICIENCY)

> 10 scenes. Tone amber/gold. P04-S04 CooPre voxel puzzle + P04-S08 QuantV2X compression là 2 hero scenes.

```
Đọc trước:
- OPUS_PLAN.md rows P04-S01 → P04-S10 và detail blocks
- materials/scripts/script_part4.md (full)
- References:
  * Source_manim_reference/3b1b_videos/_2026/spheres_talk/volumes.py:53 VolumeGrid
  * Source_manim_reference/welchlabs_videos/_2025/backprop_3/geometry_while_learning_2.py
  * Source_manim_reference/welchlabs_videos/_2025/backprop_3/decision_boundary_utils.py
  * Source_manim_reference/3b1b_videos/_2024/transformers/network_flow.py:55 get_block
  * Source_manim_reference/3b1b_videos/_2023/optics_puzzles/wave_machine.py

NHIỆM VỤ PHASE 5: 10 scenes trong studio/scenes/part04/.
  p04_s01_title.py
  p04_s02_v2x_overview.py
  p04_s03_annotation_cost.py
  p04_s04_coopre_masked.py            ← HERO #1. Voxel puzzle. 75s.
  p04_s05_turbotrain_landscape.py
  p04_s06_latency_chain.py
  p04_s07_arithmetic_cost.py
  p04_s08_quantv2x.py                 ← HERO #2. Compression squeeze. 65s.
  p04_s09_efficiency_summary.py
  p04_s10_bridge_to_p5.py

PHẦN P04-S04 (COOPRE) DETAIL:
  - BEV grid 8×8 voxels (Square mob trong VGroup grid)
  - 2 agents corners shooting LiDAR beams (Line + glow)
  - Masking: random 40% voxels fade to 30% opacity, LaggedStart lag_ratio=0.05
  - Reconstruction beat: particles from Agent B fly along Bezier curves to masked
    voxels, on arrival each voxel pulses và restore opacity 1.0
  - Bars: 2-pair comparison, counter "+4% AP" gold burst
  - IROS + CVPR badge bottom-right

PHẦN P04-S08 (QUANTV2X) DETAIL:
  - 3-stage pipeline build top-to-bottom
  - Squeeze reveal: large red Rectangle (BEV blob FP32) → animate width&height
    scaling 0.1× while color interpolates RED_ERROR → GREEN_FIX
  - V2X channel: 2 parallel Line representing pipe, packets struggle (red) → flow
    freely (green) after squeeze
  - Counter: 100 MB → 0.33 MB, "300×" gold burst at settle

CONSTRAINTS:
- P04-S04 reconstruction phải tạo cảm giác puzzle hoàn thành — không rush
- P04-S05 landscape: contour lines (use ParametricFunction) cần readable, không
  rối; max 5 contour rings
- KHÔNG quên P04-S07 arithmetic cost — 640 pJ vs 5 pJ là detail script
  emphasize mà beyond/ bỏ qua

DONE WHEN:
- 10 scenes render -ql
- Frame check P04-S04 (voxel reconstruct mid), S08 (squeeze mid) — save
- Final response log "PHASE 5 DONE — Part 4, 10 scenes"
```

---

## PHASE 6 — PART 5 + FINALE

> 11 scenes. **P05-S09 Living City** là visual climax cả video. P05-S11 là dramatic close.

```
Đọc trước:
- OPUS_PLAN.md rows P05-S01 → P05-S11 và detail blocks
- materials/scripts/script_part5.md (full)
- 5_PART_GUIDE.md sections P5-01 đến P5-07 + GRAND FINALE
- References:
  * Source_manim_reference/3b1b_videos/custom/logo.py:216 LogoGenerationFivefold
  * Source_manim_reference/3b1b_videos/custom/opening_quote.py:8 OpeningQuote
  * Source_manim_reference/3b1b_videos/_2020/covid.py (ViralSpread agents)
  * Source_manim_reference/3b1b_videos/_2026/spheres_talk/random_puzzles.py:18 DotHistory
  * Source_manim_reference/3b1b_videos/_2026/hairy_ball/model3d.py (RadioTower + RadioBroadcast)
  * Source_manim_reference/3b1b_videos/_2026/spheres_talk/volumes.py:365 (splat)

NHIỆM VỤ PHASE 6: 11 scenes trong studio/scenes/part05/.

THỨ TỰ:
  1. P05-S01 title — first time all 5 roadmap nodes light up
  2. P05-S02a/b — LLM vs Robot data + 2 barriers (with zombie preview)
  3. P05-S03 micromobility cards
  4. P05-S04a — Stuart Geman quote scene — letters fly from random positions
  5. P05-S04b/c — MetaUrban generator + scaling curve
  6. P05-S05a/b — UrbanSim bottleneck + results
  7. P05-S06a/b — CityWalker + PedGen
  8. P05-S07 — Zombie to Alive transform (emotional moment)
  9. P05-S08 — Vid2Sim
  10. **P05-S09 LIVING CITY** — 3D hero finale
  11. P05-S10 — Chain of Solutions Montage (5 vignettes)
  12. P05-S11 — Final Frame — "Beyond Self-Driving. Not just smarter cars. A safer world."

PHẦN P05-S09 (LIVING CITY) DETAIL — câu chuyện 50s:
  - Studio3DScene, isometric 60°
  - Phase 1 (0-15s): agents fade in by type theo schedule trong 5_PART_GUIDE P5-07:
    t=1s cars, t=3s robots, t=5s wheelchairs, t=7s pedestrians, t=9s RSU, t=11s drones
  - Phase 2 (15-30s): V2X web links LaggedStart cực lag (lag_ratio=0.01) — hàng trăm
    Line giữa agents
  - Phase 2 (parallel): radar waves từ all agents — interference pattern toàn thành phố
  - Camera move: theta rotate +30° trong run_time=15s, smooth
  - Phase 3 (30-50s): camera pullback (move_camera with frame_height larger), city
    becomes background. KHÔNG dropdown 5 vignettes ở đây — đó là S10.

PHẦN P05-S10 (MONTAGE) DETAIL:
  - 5 panels drop in từ top với LaggedStart 0.2
  - Mỗi panel: ImageMobject (rendered still của iconic moment) hoặc mini VGroup
    replay (3s mini-anim)
  - Đơn giản nhất: 5 contribution_badge cards với key visual summary
  - Settle then fade out

PHẦN P05-S11 (FINAL FRAME) DETAIL:
  - City vẫn move (carry-over từ S09 — có thể restart 1 phần)
  - 3 lines write-chiseled GOLD italic centered:
    Line 1: "Beyond Self-Driving." (pause 1s)
    Line 2: "Not just smarter cars." (pause 1s)
    Line 3: "A safer world." (pause 2s)
  - Roadmap strip: all 5 nodes GOLD, connector gold pulsing
  - UCLA logo fade in
  - dust_dissolve (inverse) — particles converge to center single dot, pulse 1×, fade

CONSTRAINTS:
- P05-S09 KHÔNG SKIP các loại agent. 6 loại = 6 visual personalities.
- P05-S11 hold timings PHẢI tôn trọng (1s, 1s, 2s) — đây là kết phim
- KHÔNG để P05-S09 leak vào P05-S10 hoặc P05-S11 — mỗi scene self-contained

DONE WHEN:
- 11 scenes render -ql
- P05-S09 render -ql < 15 phút (nếu chậm hơn: optimize agent count)
- Frame check P05-S07 (zombie→alive mid), S09 (phase 1 end, phase 2 mid), S11 (each line)
- Final response: "PHASE 6 DONE — Part 5 + Finale, 11 scenes — STUDIO COMPLETE"
```

---

## PHASE 7 — FULL RENDER + QA + CONCAT

> Đây là phase đóng gói: render -qh 1080p60, frame-check toàn bộ, fix bugs found, concat thành 1 file MP4 cuối.

```
Đọc trước:
- OPUS_PLAN.md Section 8 (Risk Log)
- merge_videos.ps1 và merge_videos.py (existing scripts trong root)
- studio/PHASE0_REPORT.md (kiểm tra fallback nếu OpenGL fail)

NHIỆM VỤ PHASE 7: render full quality + QA + final concat.

STEP 1 — DRY RUN
  - Render mọi scene ở -ql lần nữa (đảm bảo session-to-session không broken)
  - List scenes nào fail → fix trước khi -qh

STEP 2 — FULL RENDER -qh (1080p60)
  - Create studio/render/ scripts:
    render_intro.ps1, render_part01.ps1 ... render_part05.ps1, render_all_final.ps1
  - Mỗi script chạy tất cả scenes của part đó ở -qh
  - Pattern: foreach scene file in part: manim -qh --disable_caching $file ClassName
  - Render OpenGL scenes (I-02, P02-S05, P05-S09) với --renderer=opengl
  - Chạy trong background nếu mỗi part > 30 phút

STEP 3 — FRAME CHECK PROTOCOL
  - Cho mỗi scene, frame check tại 35/60/85% time:
    ```python
    import cv2
    cap = cv2.VideoCapture(mp4_path)
    dur = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    for pct in [0.35, 0.60, 0.85]:
        cap.set(cv2.CAP_PROP_POS_MSEC, dur * pct * 1000)
        ret, frame = cap.read()
        if ret: cv2.imwrite(f'qa/{scene_id}_{int(pct*100)}.png', frame)
    cap.release()
    ```
  - Save vào studio/qa/
  - Manual scan các PNG — list anything looks off

STEP 4 — BUG FIX ROUND
  - Cho mỗi issue from frame check: open scene file, fix, re-render -qh
  - Common issues:
    * Text bleed beyond x=±6.5 → reposition
    * Color contrast too low (pastel on pastel) → swap to accent
    * Hold timing too short → bump self.wait()
    * Leftover mobjects → add to _close() final FadeOut
  - KHÔNG fix bằng cách disable feature — fix root cause

STEP 5 — CONCAT
  - Per-part concat: dùng existing merge_videos.ps1 (adapt cho studio paths nếu cần)
  - Final concat: tất cả 5 parts + intro → studio/output/beyond_self_driving_final.mp4
  - Verify total duration ~50-60 phút (target từ OPUS_PLAN.md)

STEP 6 — FINAL REPORT
  - studio/FINAL_QA_REPORT.md:
    * Total scenes: 73
    * Total duration: X min
    * Render time per part
    * Issues found + fixed
    * Known issues remaining (if any)
    * Output file path

CONSTRAINTS:
- KHÔNG render -qh nếu -ql còn fail
- KHÔNG concat nếu missing scenes
- Disk space check trước khi render -qh (~10-20GB cần)
- Mỗi scene -qh fail: stop, fix, re-render. Đừng skip.

DONE WHEN:
- 73 scenes render -qh thành công
- Frame check PNGs saved cho mọi scene
- Concat file beyond_self_driving_final.mp4 plays đầu đến cuối
- FINAL_QA_REPORT.md viết xong
- Final response: "PHASE 7 DONE — Beyond Self-Driving studio rebuild complete.
  Output: studio/output/beyond_self_driving_final.mp4"
```

---

## PHASE 8 — POLISH & VOICEOVER (OPTIONAL)

> Phase optional sau khi base render xong. Add voiceover, color grading fine-tune, transition smoothing.

```
Đọc trước:
- studio/FINAL_QA_REPORT.md
- https://github.com/ManimCommunity/manim-voiceover (manim-voiceover docs)
- Đảm bảo `pkg_resources` patch đã apply (xem README.md)

NHIỆM VỤ PHASE 8: voiceover + polish.

VOICEOVER:
  - Chọn TTS service:
    * OpenAI TTS (cao chất lượng, paid)
    * ElevenLabs (best quality, paid)
    * Azure Speech (free tier OK, multiple voices)
    * gTTS (free, basic quality)
  - Convert mỗi scene từ Scene → VoiceoverScene
  - Top-of-file SCRIPT đã sẵn — wrap trong with self.voiceover(text=SCRIPT):
  - Adjust timings để match audio length (manim-voiceover handles tự động bằng
    tracker.duration)
  - Re-render -qh từng scene với voiceover

POLISH ROUND:
  - Hero scenes (I-02, P02-S05, P04-S08, P05-S09, P05-S11) — frame-by-frame
    review tại 24fps export
  - Transition smoothing: 0.5s crossfade giữa scenes khi concat (ffmpeg)
  - Color grading: optional LUT applied via ffmpeg colorbalance/curves
  - Audio: background music subtle (BG_DARK ambient) — only during 3D heros và
    finale, ducked under voiceover

FINAL DELIVERY:
  - Final MP4 với voiceover, transitions, optional music
  - Subtitle SRT file generated từ SCRIPT strings (timing matched)
  - Studio/output/beyond_self_driving_v2_voiceover.mp4

DONE WHEN:
- Voiceover MP4 finalized
- Subtitle SRT generated
- User confirms playback OK
```

---

## QUICK START — TỪ ZERO

Nếu bắt đầu mới hoàn toàn:

```
1. Copy OPUS_PLAN.md + STUDIO_BUILD_PROMPTS.md + CLAUDE.md vào project root (đã có).
2. Mở Claude Code session mới.
3. Paste PHASE 0 prompt. Run.
4. Đọc studio/PHASE0_REPORT.md → confirm "READY FOR PHASE 1: YES".
5. Mở session mới. Paste PHASE 1 prompt. Run.
6. Tiếp tục Phase 2 → 7 theo thứ tự, mỗi phase một session mới.
7. Phase 8 optional.
```

## NOTES CHUNG CHO MỌI PHASE

- **Mỗi session bắt đầu**: Claude đọc OPUS_PLAN.md + CLAUDE.md + relevant section của plan trước khi viết code. KHÔNG bắt đầu code mà chưa đọc plan.
- **Render command chuẩn (Windows PowerShell)**:
  ```powershell
  manim -ql --disable_caching studio/scenes/part01/p01_s01_title.py P01S01Title
  ```
- **OpenGL render**:
  ```powershell
  manim -ql --renderer=opengl --disable_caching studio/scenes/intro/i02_the_hook.py I02TheHook
  ```
- **Python binary**: `C:\Users\admin\miniconda3\python.exe` (base conda, KHÔNG manim_env)
- **Anti-patterns** đã list trong OPUS_PLAN.md Section 7A — re-check trước khi commit
- **Hold timings** từ 5_PART_GUIDE.md "Phụ lục: Timing" — KHÔNG rút ngắn
- **Mỗi scene self-contained**: `_open()` đầu, `_close()` cuối, không leak mobjects sang scene sau

---

*File này là playbook execution. OPUS_PLAN.md là design spec. CLAUDE.md là project-wide rules. Đọc đúng thứ tự đó cho mỗi session.*
