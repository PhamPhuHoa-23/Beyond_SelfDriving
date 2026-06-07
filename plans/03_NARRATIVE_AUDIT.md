# 03 — Narrative Audit

> User feedback: *"video hiện tại và các bản kịch bản đều rút gọn một số papers, vì ban đầu tôi nghĩ nó chỉ đơn giản liệt kê nhưng có lẽ bạn nên check lại vì presenter gốc nêu nó ra ắc hẳn phải có lý do trong việc dẫn dắt câu chuyện."*
>
> Translation: papers were over-compressed in the draft. The presenter named each one for a *narrative reason* — restore that reason.

This file maps **every paper / system mentioned in the original scripts** to:
1. The 1-line reason it's named.
2. The scene that should cover it.
3. Whether the current draft already does that or needs a rewrite.

References:
- Original scripts: `materials/scripts/script_part{1..5}.md`
- Slide PDFs: `materials/slides/Part {1..5}.pdf` (or pptx)
- Slide image extracts: `materials/images/part{1..5}/`

---

## Part 1 — Foundation Models for AV

### Slide-to-scene mapping

| Slide | Topic | Scene | Note |
|---|---|---|---|
| 1 | Title | `i01_title_card` | Speaker = Dr. Zhiyu Huang |
| 2 | Outline (3 parts) | `i03_roadmap` (5-node version) | Roadmap is broader (5 parts), not the talk's 3 |
| 3 | Generative AI boom | `p01_s02_genai_boom` | Reasoning, image, code, video gen → "all foundation models" |
| 4 | What is a foundation model? | `p01_s02_genai_boom` (2nd half) | Stanford CRFM definition; self-supervised, downstream tasks |
| 5 | AV architectures | `p01_s03_av_arch` | Modular vs Hybrid vs E2E. Modular = most-deployed but accumulates errors |
| 6 | Long-tail problem | `p01_s04_longtail` | 3 hero images: phone-on-road person, traffic-light truck, snow-covered road |
| 7 | FMs empower AV | `p01_s05_fm_empower` | Diagram: VFM/VGM/LLM/MLLM → AV needs (auto-label, sim, vehicle iface, E2E) → goal: long-tail generalization |
| 9–11 | VLA roadmap + datasets | `p01_s06_vla_roadmap` | Ways: text action / numerical action / explicit guidance / implicit transfer. DriveLM, CoVLA, Impromptu VLA datasets |
| 12 | GPT-Driver, DriveGPT4 | `p01_s07_vla_arch` (sub-section 1) | GPT-Driver = zero-shot LLM as planner; DriveGPT4 = fine-tuned for control |
| 13 | OpenDriveVLA, BEVDriver | `p01_s07_vla_arch` (sub-section 2) | BEV input + Q-Former projection into LLM |
| 14–15 | EMMA (Waymo) | `p01_s07_vla_arch` (sub-section 3) | Built on Gemini, all output through language; chain-of-thought + perception + road graph; **slow** for real-time |
| 16 | DriveVLM (Tsinghua) | `p01_s07_vla_arch` (sub-section 4) | Dual-system: VLM low-freq + traditional high-freq; engineering complexity |
| 17–20 | AutoVLA | `p01_s08_autovla` | Dual fast/slow modes; SFT then RFT (GRPO); +10.6% planning, −66.8% runtime |
| 22 | Key takeaways | `p01_s09_takeaways` | 4-point recap: long-tail, MLLMs, diverse archs, open challenges |
| 23 | Future directions | end of `p01_s09_takeaways` or new `p01_s10_future` | Post-training, unified backbone, efficient VLA, continual learning |
| 24 | Bridge to Part 2 | `p02_s01_title` opening | "Single agent vẫn bị giới hạn bởi tầm nhìn của chính mình" |

### Reasons-to-name (don't lose these)

- **GPT-Driver**: shows even *zero-shot* LLM has decent driving common-sense → motivates putting language at the center.
- **BEVDriver**: shows we can compress 3D into BEV before tokenizing for the LLM — answers "how do you give an LLM a 3D scene?"
- **EMMA**: end-to-end ambitious example; *every* output passes through language. The point: language as the universal intermediate representation.
- **DriveVLM**: dual-system trade-off; sets up *why* AutoVLA picks dual-thinking inside one model instead of two systems.
- **AutoVLA**: UCLA team's own work — climax of Part 1, gets the most screen time.

### Compression checklist (current draft fails here)

- [ ] EMMA's chain-of-thought workflow shown explicitly (input → CoT → trajectory + bbox + road graph)
- [ ] DriveVLM's "fast traditional + slow VLM" split shown as two parallel tracks
- [ ] AutoVLA's two-mode toggling shown as a switch driven by scene complexity
- [ ] GRPO step in AutoVLA training labelled as "verified rewards from environment" — not just "RL"

---

## Part 2 — Cooperative Perception

### Slide-to-scene mapping

| Slide | Topic | Scene |
|---|---|---|
| 1 | Title | `p02_s01_title` |
| 2–3 | Why AV matters: 1.19M deaths/yr, 94% human error, Waymo 80% reduction | `p02_s02_background` |
| 4 | Modular → E2E | `p02_s03_evolution` (timeline: PnPNet → GameFormer → UniAD → DiffusionDrive) |
| 5 | Occlusion | `p02_s04_occlusion` (single LiDAR vs multi-LiDAR coverage) |
| 6–8 | Related works + gaps | `p02_s05_related_works` (V2VNet → V2X-ViT → Where2comm → CodeFilling) |
| 9 | Multi-agent multi-frame multi-task gap | `p02_s06_three_questions` (what / when / how to fuse) |
| 10–15 | V2XPnP framework + V2XPnP-Seq dataset | `p02_s07_v2xpnp` |
| 13 (sub) | V2XPnP-Seq dataset stats | `p02_s08_dataset` |
| 16–22 | TurboTrain | `p02_s09_turbotrain` |
| 23–25 | RiskMap (interpretable planning) | `p02_s10_riskmap` |
| 26–28 | Summary (3 problems → 3 solutions) | `p02_s11_summary` |
| 28 | Bridge to Part 3 | `p02_s12_bridge` |

### Reasons-to-name

- **PnPNet, GameFormer, UniAD, DiffusionDrive**: these define the *trajectory* of single-agent E2E methods. Each milestone advances joint optimization. The story: even with all this, single-agent can't beat occlusion.
- **V2VNet**: GNN approach — first cooperative perception architecture worth comparing.
- **V2X-ViT**: Transformer-based attention — next level.
- **Where2comm**: sparse communication — solves bandwidth issue.
- **CodeFilling**: codebook compression — efficient features.

The reason these 4 form a chain: *the field progressed by tackling each new bottleneck*. V2VNet had the *fusion idea*; V2X-ViT had *better fusion math*; Where2comm asked *what to send*; CodeFilling asked *how to send less*. Show this as a **timeline with each addressing the previous one's bottleneck**, not a flat list.

- **OPV2V (sim) → V2X-Real (real-world)**: the dataset evolution. Important because the user/audience needs to know cooperative perception research isn't sim-only anymore.

### Compression checklist

- [ ] Each related-works method labeled with the specific advance it adds (not just author + year)
- [ ] PnPNet uses CNN+LSTM — flag this as the legacy approach being replaced
- [ ] DiffusionDrive's anchored distribution is the *latest*, leading into "but still single-agent" argument
- [ ] V2XPnP-Seq dataset gets its own scene (S08) — 40K LiDAR + 208K camera + HD maps + 2 vehicles + 2 infra

---

## Part 3 — Sim-to-Real V2X

### Slide-to-scene mapping

| Slide | Topic | Scene |
|---|---|---|
| 1 | Title | `p03_s01_title` |
| 3–5 | 4 pillars + background | `p03_s02_four_pillars` |
| 6–11 | UCLA Smart Intersection (NW + SE corners, 2 CAVs) | `p03_s03_smart_intersection` |
| 12–14 | Time calibration (50ms ≈ 1m at 60km/h) | `p03_s04_calibration_time` |
| 15–17 | Space calibration (intrinsic, extrinsic, ghost objects) | `p03_s05_calibration_space` |
| 18–22 | Data collection (basic + combined routes, V2X-Real, V2XPnP-Seq) | `p03_s06_data_collection` |
| 23–28 | HD Map central role, why localization matters | `p03_s07_localization_why` |
| 29–32 | Multi-rate error-state Kalman Filter (GNSS 5Hz, IMU 100Hz, LiDAR 1Hz) | `p03_s08_kalman_filter` |
| 33–43 | CooperFuse (late fusion, temporal BBX features vs NMS) | `p03_s09_cooper_fuse` |
| 44–49 | V2X-ReaLO (intermediate fusion, 0.5MB/msg, 32× compression) | `p03_s10_v2x_realo` |
| 50–54 | OpenCDA-ROS bridge | `p03_s11_opencda_ros` |
| 55–58 | CDA-SimBoost (digital twin loop) | `p03_s12_simboost` |
| 59 | OpenCDA-InfraX (data generation platform) | `p03_s13_infrax` |
| — | Bridge to Part 4 | `p03_s14_bridge` |

### Reasons-to-name

- **UCLA Smart Intersection** (Charles E. Young & Westwood Plaza): *real intersection, not sim*. Sets up the entire engineering credibility of Part 3.
- **PJLab SensorsCalibration**: open-source tools released — academic contribution.
- **V2X-Real (ECCV 2024) & V2XPnP-Seq**: explicit chain — Part 2's data came from Part 3's hardware.
- **CooperFuse (IV 2024)**: "first real-time cooperative late fusion for V2X." The temporal-BBX-features insight is the contribution; NMS-by-confidence comparison is the punchline.
- **V2X-ReaLO (T-PAMI submission)**: "first online intermediate fusion in real-world." 0.5MB / 32× compression is the working point.
- **OpenCDA-ROS**: the bridge between simulation code and real-world code — same code runs both.
- **CDA-SimBoost**: closes the loop — real data → digital twin → generated scenarios → train → benchmark.
- **OpenCDA-InfraX**: data generation platform — multi-modality, weather, vector maps.

### Compression checklist

- [ ] Smart Intersection scene shows actual sensor counts (NW: LiDAR-128 + 2 cam + radar; SE: LiDAR-64 + 2 cam + C-V2X) — not generic "RSU"
- [ ] Time calibration uses the *concrete number* 60km/h × 50ms ≈ 1m as the visual hook
- [ ] CooperFuse contrasts NMS (confidence-only) vs temporal BBX features explicitly — animate the bbox with better orientation winning over higher confidence
- [ ] V2X-ReaLO shows the 32× compression as a concrete bandwidth shrink, not just a ratio
- [ ] CDA-SimBoost loop: Real → Digital Twin → Scenarios → Train → Real (closed cycle visible)

---

## Part 4 — Efficiency

### Slide-to-scene mapping

| Slide | Topic | Scene |
|---|---|---|
| 1 | Title | `p04_s01_title` |
| 2–7 | Why efficiency? V2X overview, US DoT smart intersection partnership | `p04_s02_why_efficiency` |
| 9–14 | CooPre (data efficiency, IROS 2025) | `p04_s04_coopre` (after `p04_s03_annotation_cost`) |
| — | Annotation cost explosion | `p04_s03_annotation_cost` (240K → 460K → 1.2M annotations) |
| 15–22 | TurboTrain (training efficiency, ICCV 2025) revisited deeper | `p04_s06_turbotrain` (preceded by `p04_s05_multi_task_conflict`) |
| — | Why multi-task multi-agent is hard (gradient conflict, init sensitivity) | `p04_s05_multi_task_conflict` |
| 22–31 | Inference efficiency: latency chain + QuantV2X | `p04_s07_latency_chain` + `p04_s08_quantv2x` |
| — | Summary | `p04_s09_efficiency_summary` |
| — | Bridge to Part 5 | `p04_s10_bridge` |

### Reasons-to-name

- **CooPre (IROS 2025)**: *first* multi-agent self-supervised pretraining for V2X. Multi-agent masked LiDAR reconstruction. Works without any annotation. Result: 50% data → 100%-baseline performance, +4% AP at full data.
- **TurboTrain**: re-introduced from Part 2 with deeper dive — emphasis on *why one-time training fails* (orange dots on chart) and *why manual 4-stage stages*.
- **QuantV2X**: *first fully-quantized V2X system*. Quantization at two levels: model (FP32→INT8) AND communication (300× compression of features). The "fully" word is the contribution — others did one or the other.

### Compression checklist

- [ ] Annotation-scale chart: V2V4Real 240K → DAIR-V2X 460K → V2X-Real 1.2M (5× growth, hits annotation wall)
- [ ] CooPre's "ask other agents what you can't see" intuition is animated explicitly
- [ ] TurboTrain comparison chart shows 4-stage manual (blue, 120 epochs) vs TurboTrain (45 epochs), with one-time training (orange) failing
- [ ] QuantV2X two-level quantization shown as 2 separate compressions, not one

---

## Part 5 — Physical AI

### Slide-to-scene mapping

| Slide | Topic | Scene |
|---|---|---|
| 1 | Title | `p05_s01_title` |
| 2–8 | Vision + 2 barriers | `p05_s02_physai_vision` |
| 9–12 | Micro-mobility (60% trips < 5 miles, COCO Robotics) | `p05_s03_micromobility` |
| 13–24 | MetaUrban (compositional gen + power-law scaling + UrbanVerse) | `p05_s04_metaurban` |
| 25–38 | UrbanSim (180 GPU days → 3 hours, 2620 FPS / 256 envs) | `p05_s05_urbansim` |
| 39–47 | CityWalker dataset + PedGen (zombie city, 30.8h video, diffusion-conditioned-on-scene) | `p05_s06_citywalker` |
| 50–54 | Vid2Sim (3DGS + mesh, sim-to-real gap) | `p05_s07_vid2sim` |
| 55–56 | Grand finale (5-part recap + populated city + comm web) | `p05_s08_finale` |
| 57 | Credits | `p05_s09_credits` |

### Reasons-to-name

- **MetaUrban (ICLR 2025 Spotlight)**: compositional scene generation + Stuart Geman's quote *"The world is compositional, or there is a god."* This quote is structurally important — it justifies why compositional generation works.
- **UrbanVerse**: real-world video → simulation. Removes human-design bias from MetaUrban's procedural worlds.
- **UrbanSim (CVPR 2025 Highlight)**: GPU-native training. The 180 GPU days vs 3 hours comparison is the punchline.
- **CityWalker**: 30.8h, 120914 pedestrians, 16215 scenes, 227 cities. *Diversity is the contribution* — not raw count. The "person taking selfie", "person with stroller" examples make this concrete.
- **PedGen**: diffusion model with 3 conditioning inputs (Scene Context voxels / Body Context SMPL / Goal). 3 loss components (Reconstruction / Trajectory / Geometry).
- **Vid2Sim (CVPR 2025)**: 3DGS + Mesh = appearance + physics. Sim-to-real gap shrinks dramatically.

### Compression checklist (Part 5 currently has stub scenes)

- [ ] Stuart Geman quote rendered with weight (≥ 1.5s hold)
- [ ] Power-law chart contrasts power-law vs linear vs log curves explicitly
- [ ] PedGen's 3 inputs shown as 3 separate arrows feeding the central skeleton
- [ ] PedGen's 3 losses shown as 3 cards in a row
- [ ] Zombie city: pedestrians moving in straight lines, walking through walls — set up the comparison
- [ ] Sim-to-real gap visualization: arrow shrinks from wide (before Vid2Sim) to near-zero (after)
- [ ] Grand finale shows ALL agent types from all 5 parts coexisting + dense communication web

---

## Creative liberty — when to deviate from slides

The user's brief: *"hiểu rõ hơn slides gốc ban đầu... làm chi tiết hơn một xíu"* (understand the original slides more deeply, then make them more detailed). The implication is **not** "copy the slides" — it's *"use the slides to understand the story, then re-tell it for an animated medium."*

Slides and 3B1B-style animations are different mediums. A slide is static, dense, and a presenter narrates around it. An animation reveals one idea at a time. The translation is not 1:1.

### What you SHOULD change / invent

| Thing | Why |
|---|---|
| **Slide layouts** | A slide stuffs 10 things on one frame. An animation reveals them sequentially. Decompose. |
| **Bullet-list slides** | Re-cast as a sequence of focused reveals (one idea, hold, fade, next). Don't render the bullets verbatim. |
| **Dense diagrams** | Redraw cleanly in Manim. Don't screenshot the slide. Drop visual elements that don't carry weight. |
| **Stock-photo hero images** | If the slide has a screenshot of a paper figure (e.g., EMMA pipeline, MetaUrban scenes), you can either embed it via `SlideImage` or redraw a simplified version. **Default: redraw simplified.** Use `SlideImage` only when the image carries information that's hard to reproduce (real-world photos, sensor outputs, complex 3D figures). |
| **Animations the slide implies but cannot show** | A slide with 4 frames stitched together → in Manim, animate the morph between them. A slide with overlaid before/after → in Manim, animate the transition. |
| **Mascot-driven framing** | Slides have no mascots. Add PI/CAR to introduce the *question* a section answers and to mark transitions — this is a 3B1B convention the slides won't have. |
| **Quotes** | Slides may show a quote inline as one of many bullets. Promote important quotes to a dedicated reveal (italic, gold, hold ≥ 1.5s). E.g., Stuart Geman quote in P05-S04. |

### What you should NOT change

| Thing | Why |
|---|---|
| **Author names of papers** | Naming the right papers is necessary for credit. |
| **Specific numbers cited in the talk** | 1.19M deaths, 94% human error, 2620 FPS, 180 GPU days, 30.8h video, 120914 pedestrians — these are concrete signals. Keep them. |
| **The order of major arguments within a part** | Each part is a tight chain. Don't reorder. |
| **The chain between parts** | The "each part solves the previous part's bottleneck" structure is the spine of the whole tutorial. Don't move sections between parts. |
| **UCLA's own contributions** | These are climaxes. Don't swap them for related works. |

### When in doubt — escalate, don't guess

If a slide is ambiguous and you have to make a choice (e.g., "should I show the EMMA figure as a screenshot or redraw it?"), pick what you think is best, do it, and **note the choice in a comment** at the top of the scene file:

```python
# CREATIVE CHOICE: redrew EMMA pipeline as 4 abstract boxes instead of
#   embedding the slide screenshot — slide image is too dense.
```

The user can override later.

### Examples of creative reinterpretation already in the plan

- **P01-S04 Long-tail**: original slide is 3 photos + a curve. The plan moves the curve up and shrinks it, then has PI and CAR discuss — this is invention, not in the slide.
- **P01-S07 VLA Arch**: original slides have 4 separate slides for 4 architectures. The plan compresses to one scene with 4 uniform-height pipeline rows — invention.
- **P02-S03 Evolution**: original is a list of 4 papers. Plan turns it into a *chain* showing each method addressing the previous one's bottleneck.
- **P05-S08 Finale**: original slide is a 2-line summary. Plan turns it into a populated city wide-shot with all agent types and a communication web — pure invention to give emotional closure.

### Working against the slides

If a slide says something the script *contradicts* or that you genuinely think weakens the story (e.g., a slide overstates a result or mis-attributes a method), trust the script first, the slide second. Flag the conflict in a comment so the user can adjudicate.

---

## Cross-cutting — narrative throughlines

These threads should be felt across all 5 parts:

1. **Each part solves a bottleneck the previous part created.** State this explicitly in P05-S08:
   - Part 1: long-tail → motivates need for cooperation (Part 2)
   - Part 2: cooperation needs data → motivates real-world infra (Part 3)
   - Part 3: real-world deployment is expensive → motivates efficiency (Part 4)
   - Part 4: efficiency for cars only → motivates broader Physical AI (Part 5)

2. **UCLA Mobility Lab's own contributions are the climaxes**: AutoVLA (P1), V2XPnP/TurboTrain/RiskMap (P2), CooperFuse/V2X-ReaLO/OpenCDA (P3), CooPre/QuantV2X (P4), MetaUrban/UrbanSim/PedGen/Vid2Sim (P5). The animation should privilege these over related-works lists.

3. **The "long tail" is the entire tutorial's protagonist.** Foundation models (P1) tackle the cognitive long tail. V2X (P2-P4) tackles the perceptual long tail. Physical AI (P5) tackles the embodiment long tail.

When you write a scene, ask: *which throughline is this scene serving?* Anchor a sentence to it.
