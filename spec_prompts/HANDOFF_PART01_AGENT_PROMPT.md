# HANDOFF PROMPT — Studio Part 01 Only (Foundation Models)

> **Copy toàn bộ file này** làm system/context cho agent mới.  
> **Phạm vi:** CHỈ Part 01 (`studio/scenes/part01/` — 17 scene).  
> **KHÔNG** sửa Part 02–05, intro, `drivex/`, `drivex_white/`, `beyond/` (legacy).

---

## 0. Một câu nhiệm vụ

Hoàn thiện **17 scene Part 01** trong `studio/`: render **TẤT CẢ**, **đọc frame ảnh** (không chỉ log heuristic), sửa layout/contrast/animation/nghĩa hình ảnh, lặp đến khi mỗi scene ổn @ 85% hold.

---

## 1. Phạm vi & cấm

| Làm | Không làm |
|-----|-----------|
| `studio/scenes/part01/*.py` (17 files) | `studio/scenes/part02/**` — **người khác lo** |
| `studio/components/*` khi cần shared fix | `drivex/`, `drivex_white/` |
| `studio/reference/*` port từ audit | Tạo file scene mới trừ khi user yêu cầu |
| Cập nhật `studio/_qa_loop/PART01_FRAME_AUDIT.md` sau mỗi vòng | Báo “xong” khi chỉ render 1 scene |

**Engine:** **ManimGL** (`manimgl.exe`), KHÔNG phải Manim Community.  
**BG hiện tại:** cream `#FFF9E6` (`BG_PAPER` trong `studio/components/colors.py`) — mọi stroke/fill phải **đủ tương phản trên nền sáng**.

---

## 2. Workflow BẮT BUỘC (user nhắc nhiều lần — đừng bỏ qua)

```powershell
cd C:\Users\admin\Downloads\ML\Lab01_3B1B
$env:PYTHONPATH = "C:\Users\admin\Downloads\ML\Lab01_3B1B"

# Render + extract frame 35% / 60% / 85% — CẢ PART 01
python scripts/scene_qa_loop.py --part 01

# Một scene sau khi sửa
python scripts/scene_qa_loop.py --only P01S07BEMMA
```

Sau mỗi lần render:

1. **Mở và ĐỌC** `studio/_qa_loop/frames/<ClassName>/<ClassName>_85pct.jpg` (và 35/60 nếu animation step-by-step).
2. Ghi nhận overlap, chữ mờ, mũi tên xiên, chart lệch, timing sai.
3. Sửa code → render lại scene đó → đọc lại ảnh.
4. Khi xong cả 17: chạy lại `--part 01` một lần, cập nhật audit doc.

**MP4:** `videos/<ClassName>.mp4`  
**Manifest:** `studio/_qa_loop/manifest.jsonl`

User tức giận khi agent chỉ QA 1 scene hoặc không đọc ảnh — **luôn batch Part 01 + đọc frame**.

---

## 3. Danh sách 17 scene (check từng file một)

| # | Class | File |
|---|--------|------|
| 1 | `P01S01Title` | `p01_s01_title.py` |
| 2 | `P01S02AGenAITimeline` | `p01_s02a_genai_timeline.py` |
| 3 | `P01S02BFMDefinition` | `p01_s02b_fm_definition.py` |
| 4 | `P01S03AModular` | `p01_s03a_modular.py` |
| 5 | `P01S03BE2E` | `p01_s03b_e2e.py` |
| 6 | `P01S03CHybrid` | `p01_s03c_hybrid.py` |
| 7 | `P01S04ALongtailProblem` | `p01_s04a_longtail_problem.py` |
| 8 | `P01S04BLongtailInsight` | `p01_s04b_longtail_insight.py` |
| 9 | `P01S05FMEmpower` | `p01_s05_fm_empower.py` |
| 10 | `P01S06VLARoadmap` | `p01_s06_vla_roadmap.py` |
| 11 | `P01S07ABEVDriver` | `p01_s07a_bevdriver.py` |
| 12 | `P01S07BEMMA` | `p01_s07b_emma.py` |
| 13 | `P01S07CDriveVLM` | `p01_s07c_drivevlm.py` |
| 14 | `P01S08AAutoVLASwitch` | `p01_s08a_autovla_switch.py` |
| 15 | `P01S08BAutoVLAResults` | `p01_s08b_autovla_results.py` |
| 16 | `P01S09Takeaways` | `p01_s09_takeaways.py` |
| 17 | `P01S10BridgeToP2` | `p01_s10_bridge_to_p2.py` |

---

## 4. Quy tắc thiết kế (toàn Part 01)

### 4.1 Layout & typography
- Chữ on-screen **tiếng Anh** (user VN, narration có thể VN).
- Dùng `SIZE_LABEL`, `SIZE_BODY`, `SIZE_CAPS` từ `studio/components/typography.py` — **không** `SIZE_LABEL-4` / font lúc to lúc nhỏ.
- Không overlap title, footer, bubble, chart labels.
- `place_footer()` cho dòng cuối scene; `CONTENT_TOP` để stack không đè header.
- Cuối scene: `FadeOut` mọi thứ không mang sang scene sau — **không** replay/fade-in lại hết ở cuối.

### 4.2 Màu & contrast (nền cream)
- Không dot/line/synapse **trắng hoặc xám nhạt** trên cream — dùng `INK_DARK`, `#0F766E`, `PURPLE_MODEL`, v.v.
- LiDAR / point cloud: **không** trắng — đã fix BEV: `#0F766E` + stroke `INK_DARK`.
- Panel/pastel fill phải **khác** nền đủ để thấy khối; stroke ≥ 2.5pt.
- `set_opacity` trên cả `VGroup` có chữ → chữ mờ; chỉ dim **rect/arrow**, giữ label/legend.

### 4.3 Mũi tên (user: “không thẳng hàng, overlap một đống”)
- **Luôn** dùng `h_arrow`, `v_arrow`, `pipeline_arrow` từ `studio/components/pipeline.py`.
- **Không** `Arrow(mob.get_right(), other.get_bottom())` — gây xiên/chồng.
- Ngang: cùng `y`; dọc: cùng `x`; fork nhiều nhánh: mỗi nhánh `x` = center block đích.
- `pipeline_row` đã `aligned_edge=DOWN`; đừng thêm mũi tên dọc cắt qua hàng ngang (EMMA đã tách).

### 4.4 Animation
- **Step-by-step:** reveal từng stage; **không** fade-in hết rồi mới chạy lại animation từng phần (BEV user gọi “rất ngu”).
- Trục chart: **vẽ axes trước**, data sau (long-tail — issue R1/R2/R3 lặp lại).
- Không “show everything then replay” ở VLA roadmap / scene kết.

### 4.5 Ít box hơn — port từ reference
- Đọc `SOURCE_MANIM_REFERENCE_AUDIT.md` + `studio/reference/` **trước khi** vẽ tay.
- NN / FM: dùng `EmbeddingArray`, `mlp_synapse_block`, `play_simple_attention_animation`, `make_embedding_row_stack`, `bev_grid`, `qformer_stack` — **adapt**, không chép nguyên manimlib path.
- User: “quá nhiều box”, “hand-coded rất xấu”, “đừng chỉ visualize bằng vài dot”.
- Neural network **tượng trưng** (3×4 dots, vài layer) — **không** grid số `NumericEmbedding` dense tràn màn (EMMA).

### 4.6 ManimGL pitfalls (đã crash production)
- **Không** `centered=True` trong `.arrange()` → `TypeError`.
- **Không** `corner_radius` trên `SurroundingRectangle` → dùng `RoundedRectangle`.
- **Không** import `GREEN_B` — dùng `GREEN_FIX`.
- `NumericEmbedding`: dùng `.get_family()` không phải `.get_mob_family()`.
- `stage_panel(..., show_inner_bg=False)` hoặc `_stage_shell` khi inner_bg che content (BEV).

---

## 5. Feedback user theo scene (từ chat — ưu tiên khi sửa)

### P01S02AGenAITimeline
- Label **LLaMA / GPT-4o+ đè nhau** trên timeline — alternate UP/DOWN hoặc rút label; kiểm tra cluster 2024–25.
- Trục hạ xuống; label không nằm đè bead.

### P01S02BFMDefinition / P01S05FMEmpower
- Đã bỏ `centered=True`; bracket/side bar đủ đậm (`INK_MID`).
- FM empower: không pale brackets.

### P01S03AModular
- **Ý nghĩa:** error = `error_propagation_marker` (đỏ), không dot trắng; xe = output Control, “Actuator command”, unsafe maneuver.
- Callout không đè box; mũi tên dọc một cột `x`.

### P01S03BE2E
- Synapse `INK_DARK`, đủ dày; panel tight; không inner_bg nuốt MLP.

### P01S03CHybrid
- **Không** tag `[ML]` `[Classical]` trôi không màu — legend + thanh màu + tag ML/Cls; dim chỉ box/arrow.
- Stack **dưới** title (`next_to(header)`), không đè title.
- Footer: “All three **architectures** share one weakness”.

### P01S04ALongtailProblem
- Axes **trước** distribution; shrink chart trước khi mascot/dialog; “fundamental problem” **không sát** box.

### P01S06VLARoadmap
- Chip/year `SIZE_LABEL`; không replay cuối scene.

### P01S07ABEVDriver
- **Step-by-step:** Sensors → BEV → Q-Former+LLM → Waypoints; mỗi bước panel + content cùng lúc.
- LiDAR tối; không pre-fade all boxes.

### P01S07BEMMA
- Layout: Camera → symbolic VLM (icon nhỏ) → CoT `stage_panel`; dưới: 3 `pipeline_block` (Trajectory/BBox/Road graph) — **không** `NumericEmbedding` dưới mỗi head.
- Mũi tên: `h_arrow` hàng trên, `v_arrow` xuống outputs, `h_arrow` giữa 3 block.
- CoT `SIZE_BODY`; không dense EmbeddingArray + attention.

### P01S07CDriveVLM
- Fast/Slow pipelines; 2 `v_arrow` vào Action tại **2 x** khác nhau (không chồng).
- Fast stroke đủ đậm.

### P01S08AAutoVLASwitch
- Classifier có **toggle FAST/SLOW**; phase A simple→fast; phase B complex→slow+CoT; fade nhánh fast khi slow bật.
- Mũi tên `h_arrow` theo `y` từng nhánh; `v_arrow` slow→CoT.

### P01S08BAutoVLAResults
- Chart lớn hơn; **y tick bên trái** trục; `y_label="Score"`.
- `bar_group_labels` cho nuPlan / nuScenes **căn giữa** dưới từng cặp bar — **không** dính cạnh nuScenes.
- Key numbers `+10.6%` / `-66.8%` **không đè** lên cột chart — đặt `RIGHT` hoặc trên/dưới có buff.

### P01S09Takeaways
- Card đủ rộng (checklist R1).

### P01S10BridgeToP2
- Footer `place_footer`; không clip đáy.

---

## 6. Component API (dùng thay vì tự vẽ)

```python
from studio.components import (
    StudioScene, h_arrow, v_arrow, pipeline_arrow, pipeline_row, pipeline_block,
    stage_panel, place_footer, CONTENT_TOP,
    axes_deploy, bar_reveal, bar_group_labels, place_chart, key_number,
    error_propagation_marker, error_callout, vehicle_icon,
    EmbeddingArray, play_simple_attention_animation, make_embedding_row_stack,
    # colors: INK_DARK, INK_MID, PURPLE_MODEL, ACCENT_BLUE, ...
)
from studio.reference.bev_grid import lidar_point_cloud_side, bev_token_grid, qformer_stack
from studio.reference.network_mlp import mlp_synapse_block
```

---

## 7. Tài liệu đọc trước khi code

1. `plans/09_FIX_CHECKLIST.md` — Part 1 rows (R1/R2/R3).
2. `plans/04_PART_INTRO_AND_PART01.md` — blueprint từng scene (paths `drivex/` cũ → map sang `studio/scenes/part01/`).
3. `SOURCE_MANIM_REFERENCE_AUDIT.md` — port ý tưởng, không import nguyên 3b1b.
4. `studio/_qa_loop/PART01_FRAME_AUDIT.md` — trạng thái frame gần nhất.
5. `materials/scripts/script_part1.md` + slides Part 1 — **lý do** mỗi paper/khái niệm xuất hiện.

---

## 8. Đã làm trong session trước (đừng phá)

- `h_arrow` / `v_arrow` / `link_rect` trong `pipeline.py`.
- Hybrid legend màu; EMMA layout gọn; Modular error đỏ; BEV step-by-step; AutoVLA switch; chart helpers.
- Loại `centered=True` trên P01S02b, S05, S07b.

**Vẫn cần verify bằng frame:** P01S08B chart labels, P01S02A label crowding, P01S04A axes order, P01S04A footer spacing.

---

## 9. Definition of done (Part 01)

- [ ] `python scripts/scene_qa_loop.py --part 01` → **17/17 Render OK**
- [ ] Agent đã **đọc** mỗi `*_85pct.jpg` và ghi trong `PART01_FRAME_AUDIT.md` PASS/OPEN + 1 dòng note
- [ ] Không overlap title/footer; mũi tên thẳng; contrast OK trên cream
- [ ] Animation step-by-step đúng trên BEV, AutoVLA, EMMA
- [ ] `videos/P01*.mp4` timestamp mới sau batch cuối

---

## 10. Prompt ngắn dán vào agent (copy block này)

```
Bạn nhận Part 01 Beyond Self-Driving (studio/, ManimGL). CHỈ sửa studio/scenes/part01/ (17 scene). KHÔNG đụng Part 02+.

Quy trình: python scripts/scene_qa_loop.py --part 01 → đọc studio/_qa_loop/frames/<Class>/*_85pct.jpg cho TỪNG scene → sửa → render lại → lặp.

Đọc spec_prompts/HANDOFF_PART01_AGENT_PROMPT.md, plans/09_FIX_CHECKLIST.md (Part 1), SOURCE_MANIM_REFERENCE_AUDIT.md.

User yêu cầu: contrast trên cream #FFF9E6; h_arrow/v_arrow (không Arrow xiên); step-by-step animation; ít box, port reference; English on-screen; SIZE_LABEL/SIZE_BODY nhất quán; đọc ảnh không chỉ heuristic.

Ưu tiên mở: P01S08B (chart labels), P01S02A (timeline overlap), P01S04A (axes trước data, footer spacing), rà lại 17 file một vòng.

Báo cáo: bảng 17 scene Render OK/FAIL + link frame 85% + việc còn OPEN.
```

---

*Generated 2026-05-23 from full chat handoff. Part 02+ explicitly out of scope.*
