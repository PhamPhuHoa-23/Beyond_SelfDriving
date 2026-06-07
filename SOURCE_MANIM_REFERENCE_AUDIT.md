# Source Manim Reference Audit for Beyond Self-Driving Rebuild

Date: 2026-05-22

Scope: `Source_manim_reference/`

Goal: identify reusable or adaptable components, scene classes, helper functions, and visual idioms that can upgrade every scene in `beyond/` from slide-like layouts into cinematic Manim explanations.

Important note: much of this reference is written for 3B1B `manimlib` or Welch Labs local tooling, not Manim Community. Treat most items as adapt-only unless a small function is self-contained and compatible. For the rebuild, prefer porting the visual idea into `beyond/scenes/` using this project's palette and Manim CE APIs.

## Major Reference Folders

| Reference Path | What It Contains | Reusable As-Is? | Adapt-Only Ideas | Target Scenes |
|---|---|---:|---|---|
| `Source_manim_reference/3b1b_videos/` | 3B1B production source: 3D, transformers, optics, probability, calculus, logos, character systems, custom scenes | Usually no | Camera choreography, transform language, vector fields, surface/mesh staging, recurrence motifs | All parts |
| `Source_manim_reference/3b1b_videos/custom/` | Logo, end screens, opening quotes, drawings, characters | Usually no | Particle/assembly title cards, closing montage, quote framing | I01, part titles, P05 finale |
| `Source_manim_reference/3b1b_videos/custom/characters/` | PiCreature classes and animations | No for literal import | Mascot expressions, blink/wave timing, reaction beats | Mascot moments, bridge scenes |
| `Source_manim_reference/3b1b_videos/_2024/transformers/` | Transformer and attention visualizations: embeddings, attention, MLPs, network flow | No | Token streams, attention arcs, embedding arrays, blocks in depth | P01 VLA scenes, AutoVLA, V2XPnP |
| `Source_manim_reference/3b1b_videos/_2023/optics_puzzles/` | Wave propagation, field visualizations, optics annotations, cylinders | No | Radar wave interference, distortion, occlusion physics | I02, P02S04, P05S07 |
| `Source_manim_reference/3b1b_videos/_2026/hairy_ball/` | 3D models, radio broadcast, vector fields, moving 3D objects along paths | No | 3D radar shells, RSU towers, city signal fields, camera orbit | I02, P02S04, P05S07 |
| `Source_manim_reference/3b1b_videos/_2026/spheres_talk/` | 3D surfaces, meshes, volume grids, ring decomposition, high-dimensional diagrams | No | Shell decomposition, grid-to-volume transforms, 3D scoreboards | P03, P04, P05 |
| `Source_manim_reference/3b1b_videos/once_useful_constructs/` | Legacy helpers for graph scenes, complex transforms, regions, fractals, light | Some small math helpers maybe | Graph/network layouts, spotlight, partitioning, matrices, vector-space motion | Part 2-4 diagrams |
| `Source_manim_reference/welchlabs_videos/` | Welch Labs ML/AI visuals: VLA, RL, backprop, generalization, DeepSeek, Sora, geometry | Usually no | Modern ML visual language, camera pacing, image-patch grids, model internals | Part 1, Part 4, Part 5 |
| `Source_manim_reference/welchlabs_videos/_2026/vla/` | VLA architecture, action expert, diffusion/action sequences, attention flow | No | Best source for Part 1 VLA rebuild | P01S06-P01S08 |
| `Source_manim_reference/welchlabs_videos/_2025/backprop_3/` | Geometry of neural nets, decision regions, plane folding, learning surfaces | No | Loss landscapes, gradient conflict, decision boundary morphs | P04S04, P04S07 |
| `Source_manim_reference/welchlabs_videos/once_useful_constructs/` | Welch copy of legacy Manim helpers including `light.py`, graph/linear algebra | Some small self-contained ideas | Spotlights, ambient lights, graph scenes, region partition | 3D lighting, city scenes |

## High-Priority Components and Classes

| Source Path:Line | Class/Function | What It Does | Use/Adapt Plan | Target Scenes |
|---|---|---|---|---|
| `3b1b_videos/_2026/hairy_ball/model3d.py:7` | `faulty_perp` | Computes a perpendicular direction for a 3D heading | Adapt small vector math for vehicle/drone orientation along curved paths | I02, P05S07 |
| `3b1b_videos/_2026/hairy_ball/model3d.py:10` | `get_position_vectors` | Returns center, heading, and wing/perp vectors along a trajectory | Port concept for cars/drones to face along `VMobject` paths | P05S07, P05S08 |
| `3b1b_videos/_2026/hairy_ball/model3d.py:15` | `S3Viking` | Textured 3D aircraft model, partial reveal, path placement | Do not copy model dependency; adapt `place_on_path` and `set_partial` behavior | 3D agent motion |
| `3b1b_videos/_2026/hairy_ball/model3d.py:68` | `RadioTower` | 3D lattice radio tower made from line legs/struts | Copy concept into Manim CE with `Line3D`; excellent RSU tower asset | I02, P02S04, P05S07 |
| `3b1b_videos/_2026/hairy_ball/model3d.py:87` | `OrientAModel` | Moving 3D model on curves with camera reorientation and vector helpers | Adapt camera-and-path choreography for drone/car trajectories | P05 living city |
| `3b1b_videos/_2026/hairy_ball/model3d.py:260` | `RadioBroadcast` | Expanding spherical shells, time tracker, vector-field EM waves | Top-tier reference for radar/V2X waves; port to CE rings/shells | I02, P02S04, P05S07 |
| `3b1b_videos/_2026/hairy_ball/model3d.py:275` | `update_shells` inner function | Animated expanding/fading shells based on `ValueTracker` | Use directly as pattern, not literal import | 3D radar |
| `3b1b_videos/_2026/hairy_ball/model3d.py:306` | `wave_func` inner function | Computes time-varying E/B vector fields around source | Adapt for cooperative interference field or sensor uncertainty field | P02S04, P05S07 |
| `3b1b_videos/_2024/transformers/network_flow.py:5` | `HighLevelNetworkFlow` | Full transformer network flow through embeddings, attention, MLP, unembedding | Conceptual goldmine for VLA/ML architecture scenes | P01S06-P01S08 |
| `3b1b_videos/_2024/transformers/network_flow.py:32` | `get_embedding_array` | Builds numeric embedding arrays | Adapt as colored BEV/token feature arrays | P01S07, P02S07 |
| `3b1b_videos/_2024/transformers/network_flow.py:47` | `get_next_layer_array` | Copies and randomizes embedding values into next layer | Use for model-layer transitions and latent feature updates | P01S07, P01S08 |
| `3b1b_videos/_2024/transformers/network_flow.py:55` | `get_block` | Creates 3D block/cube with title beside embedding layer | Port to CE `Prism`/`Cube` for depth-aware pipeline blocks | P01, P02, P04 |
| `3b1b_videos/_2024/transformers/network_flow.py:73` | `show_initial_text_embedding` | Tokenizes text visually, rectangles -> embedding vectors | Adapt to prompt/image/sensor -> token/latent rows | P01 VLA gallery |
| `3b1b_videos/_2024/transformers/network_flow.py:123` | `progress_through_attention_block` | Camera moves through attention block, transforms layer copy | Use as blueprint for attention-fusion scenes | P02S07, P01S07 |
| `3b1b_videos/_2024/transformers/network_flow.py:161` | `play_simple_attention_animation` | Attention arcs flash between token embeddings | Directly adapt with `ShowPassingFlash`/`ShowCreationThenFadeOut` | P01S07, P02S07 |
| `3b1b_videos/_2024/transformers/network_flow.py:174` | `progress_through_mlp_block` | Shows neuron clouds and connections inside a block | Use for FM/VLA model internals and black-box contrast | P01S03, P01S08 |
| `3b1b_videos/_2024/transformers/network_flow.py:224` | `remove_mlps` | Clears MLP internals after transition | Good cleanup pattern | All model scenes |
| `3b1b_videos/_2024/transformers/network_flow.py:227` | `mention_repetitions` | Shows repeated layers with thin blocks and brace | Use to show deep stack/computation repeated without text slab | P01S07 |
| `welchlabs_videos/once_useful_constructs/light.py:32` | `inverse_power_law` | Opacity falloff helper | Copy/adapt small helper safely if needed | Radar, spotlight |
| `welchlabs_videos/once_useful_constructs/light.py:35` | `inverse_quadratic` | Quadratic light falloff | Copy/adapt small helper safely if needed | All glow scenes |
| `welchlabs_videos/once_useful_constructs/light.py:38` | `SwitchOn` | Lagged fade-in for light rings/sectors | Adapt animation pattern | I02, P05 |
| `welchlabs_videos/once_useful_constructs/light.py:46` | `SwitchOff` | Reverse/fade light rings/sectors | Adapt cleanup pattern | I02, P05 |
| `welchlabs_videos/once_useful_constructs/light.py:56` | `Lighthouse` | SVG lighthouse source object | Do not copy asset dependency; replace with RSU icon | P02, P05 |
| `welchlabs_videos/once_useful_constructs/light.py:65` | `AmbientLight` | Annular rings with radial opacity falloff | Port as CE `VGroup` of `Annulus`/`Circle` rings | Radar/spotlight glow |
| `welchlabs_videos/once_useful_constructs/light.py:95` | `Spotlight` | Sector-based spotlight projected from source to screen | Strong blueprint for sensor cones and LiDAR beams | I02, P02S04, P05S07 |
| `welchlabs_videos/once_useful_constructs/light.py:216` | `LightSource` | Combines ambient, spotlight, source icon, shadow | Adapt into `SensorSource` or `RSUSource` helper inside scenes | P02/P05 |
| `welchlabs_videos/once_useful_constructs/light.py:363` | `ScreenTracker` | Updater wrapper for light source | Use pattern for moving sensor/occluder light | Occlusion scenes |
| `welchlabs_videos/_2026/vla/p31_61_1.py:26` | `patch_bright_average` | Computes representative colors from image patches | Useful for image-patch visual encoding; can copy if using image assets | P01S06, P01S07 |
| `welchlabs_videos/_2026/vla/p31_61_1.py:32` | `boost_colors_hsv` | Boosts saturation/value of RGB colors | Useful small helper for generated patch grids | P01, P05 Vid2Sim |
| `welchlabs_videos/_2026/vla/p31_61_1.py:43` | `P61a` | Multi-camera image patches -> encoders layout | Adapt layout: 3 camera feeds, patch grids, encoder arrows | P01S07, AutoVLA |
| `welchlabs_videos/_2026/vla/p31_61_1.py:96` | `P61b` | Same VLA image patch pipeline at different frame | Adapt for temporal frame comparison | P01S08 |
| `welchlabs_videos/_2026/vla/p31_61_1.py:149` | `P52_61` | Large VLA architecture: image encoders, embeddings, Gemma, action expert, diffusion/action output | Highest-value VLA reference; adapt structurally, not literal asset paths | P01S06-P01S08 |
| `welchlabs_videos/_2026/vla/p31_61_1.py:214` | `make_embedding_row` inner function | Creates thin colored embedding bars from image patches | Copy/adapt as feature-token row helper | P01S07, P02S07 |
| `welchlabs_videos/_2026/vla/p31_61_1.py:385` | `attn_dots` block | Ellipsis and tiny attention indicator rows | Adapt for compact model internals without text clutter | P01/P02 |
| `welchlabs_videos/_2026/vla/p31_61_1.py:447` | `attn_dots_ae` block | Action-expert Q/K/V ellipsis rows | Adapt for AutoVLA action expert | P01S08 |
| `welchlabs_videos/_2026/vla/p31_61_1.py:631` | `_make_lines` inner function | Generates stacked colored line rows for attention heads | Copy/adapt small helper | P01S08 |
| `welchlabs_videos/_2026/vla/p31_61_1.py:654` | `ReplacementTransform` rows | Transforms LLM attention rows into action-expert rows | Use for "language reasoning -> action policy" morph | P01S08 |
| `welchlabs_videos/_2026/vla/p31_61_1.py:671` | `P34_Pickup` | Prompt + multi-view images + pi0/action expert box | Adapt for AutoVLA sense-think-act demonstration | P01S08 |
| `welchlabs_videos/_2026/vla/p31_61_1.py:744` | `P31_49b` | Similar multi-view/VLA/action sequence | Adapt staging and camera framing | P01S07-P01S08 |
| `welchlabs_videos/_2026/vla/p31_61_1.py:1322` | `P43a1` | Attention/architecture detail scene | Adapt attention zoom idioms | P01S07 |
| `welchlabs_videos/_2026/vla/p31_61_1.py:1399` | `P43b2` | Attention/architecture detail scene | Adapt attention zoom idioms | P01S07 |
| `welchlabs_videos/_2026/vla/p52.py:31` | `P52Part1` | VLA-specific scene chunk | Inspect before P01 VLA rewrite | P01S06-P01S08 |
| `welchlabs_videos/_2026/vla/p52.py:109` | `P52Part2` | Continuation of VLA/action visuals | Inspect before AutoVLA rewrite | P01S08 |
| `welchlabs_videos/_2026/vla/p51.py:35` | `get_index_labels` | Adds index labels to SVG groups | Adapt for debugging complex diagrams, not final visuals | Scene development |
| `welchlabs_videos/_2026/vla/p51.py:44` | `P51` | VLA/action output visual | Inspect for diffusion/action panels | P01S08 |
| `welchlabs_videos/_2026/vla/p51.py:89` | `P51v2` | VLA/action output variant | Inspect for diffusion/action panels | P01S08 |
| `welchlabs_videos/_2026/vla/p50.py:5` | `P50` | VLA-adjacent visual | Inspect if rebuilding action/diffusion | P01S08 |
| `welchlabs_videos/_2026/vla/p35.py:6` | `P35` | VLA image/frame visual | Inspect for multi-camera input layout | P01S07 |
| `welchlabs_videos/_2026/vla/poster_1.py:43` | `poster_1` | Poster-like VLA composition | Adapt composition, not asset paths | Title/thumbnail-like beats |
| `welchlabs_videos/_2026/vla/poster_1.py:565` | `poster_2` | Poster composition variant | Adapt composition | Title/summary beats |
| `welchlabs_videos/_2026/vla/poster_1.py:642` | `poster_3` | Poster composition variant | Adapt composition | Title/summary beats |
| `3b1b_videos/custom/logo.py:25` | `Logo` | 3B1B iris/spike logo VMobject | Do not use as brand; adapt assembly/flurry geometry idea | I01, final montage |
| `3b1b_videos/custom/logo.py:103` | `LogoGenerationTemplate` | Base scene for logo assembly | Adapt title-card object assembly | I01, part titles |
| `3b1b_videos/custom/logo.py:125` | `LogoGeneration` | Restores logo spikes from scattered/arranged state | Adapt for "Beyond Self-Driving" wordmark particles | I01 |
| `3b1b_videos/custom/logo.py:163` | `SortingLogoGeneration` | Random spike rotations restore into logo | Adapt as roadmap dots/parts assembling into one story | I03, P05 finale |
| `3b1b_videos/custom/logo.py:192` | `LogoGenerationFlurry` | Flurry/complex transform into logo | Excellent opening particle burst pattern | I01 |
| `3b1b_videos/custom/logo.py:211` | `WrittenLogo` | Writes complex logo with tiny lag ratio | Adapt for elegant title draw | I01/title cards |
| `3b1b_videos/custom/logo.py:216` | `LogoGenerationFivefold` | Fivefold radial assembly | Adapt for 5-part roadmap lighting up | I03, P05S01, finale |
| `3b1b_videos/custom/opening_quote.py:8` | `OpeningQuote` | Quote scene base | Adapt quote pacing and frame emphasis | Part title cards, P05S03 |
| `3b1b_videos/_2026/spheres_talk/volumes.py:9` | `CircumferenceToArea` | Circle-to-area transformation | Adapt for "coverage area grows" scenes | P02 cooperation |
| `3b1b_videos/_2026/spheres_talk/volumes.py:32` | `SurfaceAreaToVolume` | 3D sphere surface/volume relation | Adapt for sensor-volume coverage | P02/P03 |
| `3b1b_videos/_2026/spheres_talk/volumes.py:53` | `VolumeGrid` | Structured grid/table + highlight cells | Adapt for method scorecards and metric tables | Summaries |
| `3b1b_videos/_2026/spheres_talk/volumes.py:365` | `BuildCircleWithCombinedAnnulusses` | Builds circle from many annuli | Adapt for radar shells and uncertainty rings | P02/P03 |
| `3b1b_videos/_2026/spheres_talk/volumes.py:486` | `SeparateRingsOfLatitude` | Separates sphere rings | Adapt for 3D sensor shell decomposition | I02/P02 |
| `3b1b_videos/_2026/spheres_talk/random_puzzles.py:18` | `DotHistory` | Glow dot history/trails | Adapt for moving agents and packet trails | P05 city, packet flows |
| `3b1b_videos/_2026/spheres_talk/random_puzzles.py:363` | `Random3DVectors` | 3D vector distributions | Adapt for uncertainty/fusion vectors | P03 Kalman/CooperFuse |
| `welchlabs_videos/once_useful_constructs/vector_space_scene.py:42` | `VectorScene` | Vector plane and vector animation base | Adapt for calibration/localization vectors | P03 |
| `welchlabs_videos/once_useful_constructs/vector_space_scene.py:204` | `LinearTransformationScene` | Matrix/linear transform scene base | Adapt coordinate-frame alignment | P03S04 calibration |
| `welchlabs_videos/once_useful_constructs/region.py:7` | `Region` | Region masks/sets | Adapt for occlusion masks and risk fields | P02/P03 |
| `welchlabs_videos/once_useful_constructs/region.py:29` | `HalfPlane` | Half-plane geometry | Adapt for line-of-sight and blocked cones | P02S04 |
| `welchlabs_videos/once_useful_constructs/region.py:41` | `region_from_line_boundary` | Region from line boundaries | Adapt occlusion polygons | P02 |
| `welchlabs_videos/once_useful_constructs/region.py:50` | `plane_partition` | Partitions plane by line set | Adapt sensor coverage partition | P02/P03 |
| `welchlabs_videos/once_useful_constructs/graph_theory.py:10` | `Graph` | Simple graph data structure | Adapt for V2X graph topology | P02/P03 |
| `welchlabs_videos/once_useful_constructs/graph_theory.py:56` | `DiscreteGraphScene` | Graph visualization scene | Adapt for multi-agent communication networks | P02, P05 |
| `welchlabs_videos/once_useful_constructs/graph_scene.py:21` | `GraphScene` | Legacy axes/graph scene | Usually not copy; use idea of plot lifecycle | Chart scenes |
| `welchlabs_videos/once_useful_constructs/linear_algebra.py:19` | `matrix_to_tex_string` | Matrix formatting helper | Can copy/adapt if needed | Calibration matrices |
| `welchlabs_videos/once_useful_constructs/linear_algebra.py:32` | `vector_coordinate_label` | Coordinate labels for vectors | Adapt for calibration/localization | P03 |
| `welchlabs_videos/once_useful_constructs/linear_algebra.py:51` | `get_det_text` | Determinant annotation | Probably low priority | P03 transform math |
| `welchlabs_videos/once_useful_constructs/fractals.py:24` | `fractalify` | Adds recursive jagged detail to a VMobject | Adapt sparingly for uncertainty/noise textures | Long-tail, sim gap |
| `welchlabs_videos/once_useful_constructs/fractals.py:51` | `SelfSimilarFractal` | Fractal object base | Low priority; adapt for terrain/city diversity motif | P05 MetaUrban |
| `welchlabs_videos/once_useful_constructs/complex_transformation_scene.py` | `ComplexTransformationScene` classes | Plane/field transformations | Adapt for sim-to-real warp or calibration alignment | P03 |
| `welchlabs_videos/_2025/backprop_3/decision_boundary_utils.py` | Decision boundary helpers | Builds/visualizes neural decision regions | Adapt for long-tail/generalization and gradient conflict | P01S04, P04S04 |
| `welchlabs_videos/_2025/backprop_3/plane_folding_utils.py` | Plane folding helpers | Geometric deep learning/folding visual | Adapt for model compression/generalization | P01/P04 |
| `welchlabs_videos/_2025/backprop_3/geometric_dl_utils.py` | Geometric neural net visualization helpers | Neural geometry components | Adapt if building loss landscape scenes | P04S04 |
| `welchlabs_videos/_2025/backprop_3/geometry_while_learning_2.py` | Learning geometry scene | Motion of boundaries during training | Adapt for TurboTrain optimization | P04S04 |
| `welchlabs_videos/_2025/generalization/p8_15.py` | Generalization visual scene | Bias/generalization and data fit visuals | Adapt for long-tail and FM generalization | P01S04 |
| `welchlabs_videos/_2025/generalization/p46_56.py` | Generalization scene | Curves, data distribution, model behavior | Adapt for long-tail and scaling charts | P01S04/P05S03 |
| `3b1b_videos/_2020/covid.py:205` | `ViralSpreadModel` | Agent-based spread with clusters/travel | Adapt for city-agent population dynamics | P05 living city |
| `3b1b_videos/_2020/covid.py:723` | `ViralSpreadModelWithClusters` | Clustered agent dynamics | Adapt city districts and human-agent interactions | P05 |
| `3b1b_videos/_2020/covid.py:770` | `ShowLogisticCurve` | Dynamic chart reveal | Adapt performance/scaling curves | P05 MetaUrban, P04 |
| `3b1b_videos/_2017/nn/network.py` | Neural-network object classes | 3B1B classic neural net visuals | Adapt only if simple VGroup network needed | P01/P04 |
| `3b1b_videos/_2018/uncertainty.py` | Uncertainty/probability visuals | Distributions and uncertainty language | Adapt uncertainty clouds | P03 Kalman/CooperFuse |
| `3b1b_videos/_2018/fourier.py` | Fourier/wave visuals | Wave decomposition and traces | Adapt for radar/signal scenes | P02 |
| `3b1b_videos/_2023/optics_puzzles/objects.py` | Optics scene objects | Lenses/objects/waves | Adapt for occlusion, visibility, sensor beams | P02 |
| `3b1b_videos/_2023/optics_puzzles/adding_waves.py` | Wave addition/interference scenes | Interference pattern reference | Adapt for cooperative radar waves | I02/P02 |
| `3b1b_videos/_2023/optics_puzzles/e_field.py` | Electric field visualization | Vector fields and wave fields | Adapt sensor field maps | P02/P05 |
| `3b1b_videos/_2023/optics_puzzles/wave_machine.py` | Mechanical wave machine | Wave propagation timing | Adapt signal/latency demos | P02/P04 |

## Visual Motifs Worth Stealing Conceptually

| Motif | Source Path:Line | Why It Is Useful | Implementation Direction |
|---|---|---|---|
| Expanding 3D signal shells | `3b1b_videos/_2026/hairy_ball/model3d.py:260` | Makes V2X/radar feel physical instead of flat circles | Build CE `VGroup` of `Sphere`/`Circle` rings with `ValueTracker`, opacity falloff |
| RSU tower lattice | `3b1b_videos/_2026/hairy_ball/model3d.py:68` | Instantly communicates infrastructure | Port `RadioTower` using `Line3D`; color with `ORANGE_INFRA` |
| Camera orbit during signal propagation | `3b1b_videos/_2026/hairy_ball/model3d.py:262` | Adds cinematic depth | Use `move_camera` in CE 3D scenes; avoid wild rotations |
| Token rectangles -> embedding arrays | `3b1b_videos/_2024/transformers/network_flow.py:73` | Perfect for VLA: text/image/sensor becomes latent state | Replace text tokens with camera/BEV/sensor tiles |
| Attention arcs between embeddings | `3b1b_videos/_2024/transformers/network_flow.py:161` | Makes "attention fusion" visible | Use `ShowPassingFlash` on arcs between agent feature rows |
| 3D block stack for repeated layers | `3b1b_videos/_2024/transformers/network_flow.py:227` | Shows depth without listing layers | Use thin repeated `Prism`/rectangles with brace label |
| Neuron clouds inside model block | `3b1b_videos/_2024/transformers/network_flow.py:174` | Turns black-box model into active mechanism | Use sparse dots/lines in P01/P04, keep labels minimal |
| Spotlight sectors and shadows | `welchlabs_videos/once_useful_constructs/light.py:95` | Stronger sensor cone/occlusion visual than simple triangle | Port as layered `AnnularSector` fan with falloff |
| Ambient light rings | `welchlabs_videos/once_useful_constructs/light.py:65` | Reusable glow around cars/RSUs/key nodes | Build `ambient_rings(center, color, radius)` helper per scene |
| Image patch grids | `welchlabs_videos/_2026/vla/p31_61_1.py:43` | Good visual for camera input compression | Use generated colored squares if original assets unavailable |
| Embedding row bars | `welchlabs_videos/_2026/vla/p31_61_1.py:214` | Compact, high-density model feature visual | Create local `_feature_rows` helper in VLA scenes |
| Diffusion/action sequence frames | `welchlabs_videos/_2026/vla/p31_61_1.py:332` onwards | Great for AutoVLA "action expert" and PedGen | Use abstract ghost frames/noise particles -> clean path |
| Attention-row transfer | `welchlabs_videos/_2026/vla/p31_61_1.py:654` | Explains model specialization via transformation | Transform rows from "language" color stack to "action" color stack |
| Logo/flurry assembly | `3b1b_videos/custom/logo.py:192` | Opening and finale can feel designed, not static | Use particles/triangles assembling title/roadmap, not 3B1B logo |
| Fivefold radial assembly | `3b1b_videos/custom/logo.py:216` | Perfect metaphor for 5 parts becoming one ecosystem | Adapt for P05S01 and finale all-parts lighting |
| Ring decomposition | `3b1b_videos/_2026/spheres_talk/volumes.py:365` | Radar/sensor coverage as measurable shells | Use for coverage-before/after cooperative perception |
| Dot trails/history | `3b1b_videos/_2026/spheres_talk/random_puzzles.py:18` | Makes agents and packets feel alive | Use `TracedPath` or dissipating paths in city/packet scenes |
| Plane/linear transforms | `welchlabs_videos/once_useful_constructs/vector_space_scene.py:204` | Calibration scene should visibly align coordinate frames | Transform misaligned point cloud/grid into common frame |
| Region partitioning | `welchlabs_videos/once_useful_constructs/region.py:50` | Clean occlusion/risk map geometry | Use for blind zones, risk fields, sensor partitions |
| Neural decision boundaries | `welchlabs_videos/_2025/backprop_3/decision_boundary_utils.py` | Better than generic "model training" boxes | Use for TurboTrain and generalization scenes |
| Agent cluster dynamics | `3b1b_videos/_2020/covid.py:723` | Living city needs population motion, not random dots | Adapt for pedestrians/robots interacting by district |

## Scene Rebuild Targets Mapped to References

| Target Scene(s) | Recommended Reference Patterns | Rebuild Direction |
|---|---|---|
| `intro/i01_title_card.py` | `custom/logo.py:192`, `custom/logo.py:216` | Particle/geometry assembly of title; five-part spark motif |
| `intro/i02_the_hook.py` | `model3d.py:260`, `light.py:95`, optics wave files | Full 3D city/RSU/radar shells, distorted around buildings |
| `intro/i03_roadmap.py` | `lost_lecture.py:96`, `custom/logo.py:216` | Orbital roadmap with moving packet/lightning chain |
| `part01/p01_s02_genai_boom.py` | `network_flow.py:73`, `covid.py:770` | Timeline/curve plus token/data streams into FM |
| `part01/p01_s03_av_arch.py` | `network_flow.py:174`, `network_flow.py:227` | Three architectures as machines, not boxes |
| `part01/p01_s04_longtail.py` | `generalization/*`, `decision_boundary_utils.py` | Long-tail distribution with failure icons and boundary morph |
| `part01/p01_s06_vla_gallery.py` | `welchlabs_videos/_2026/vla/p31_61_1.py` | Museum/gallery cards with real mini mechanisms per method |
| `part01/p01_s07_vla_arch.py` | `network_flow.py:73`, `network_flow.py:161`, `p31_61_1.py:214` | Sensor tiles -> embedding rows -> attention/LLM/action |
| `part01/p01_s08_autovla.py` | `p31_61_1.py:671`, `p31_61_1.py:654` | AutoVLA as fast/slow routing and action expert transformation |
| `part02/p02_s04_occlusion.py` | `model3d.py:260`, `light.py:95`, `optics_puzzles/adding_waves.py` | Cooperative waves resolve occlusion with interference |
| `part02/p02_s05_related_works.py` | `network_flow.py:227`, timeline ideas | Evolution as living timeline with method mechanism in each node |
| `part02/p02_s07_v2xpnp.py` | `network_flow.py:161`, `graph_theory.py:56` | Multi-agent temporal/spatial attention as moving arcs |
| `part03/p03_s04_calibration.py` | `vector_space_scene.py:204`, `linear_algebra.py:32` | Coordinate frames physically align, matrix flies into point cloud |
| `part03/p03_s05_kalman.py` | `uncertainty.py`, `random_puzzles.py:363` | Uncertainty clouds collapse into clean 100 Hz stream |
| `part03/p03_s06_cooperfuse.py` | `region.py`, `VectorScene`, probability visuals | Fusion as weighted uncertainty fields, no label clutter |
| `part04/p04_s03_coopre.py` | `VolumeGrid`, ring/grid transforms | Masked voxel puzzle, particles reconstruct missing voxels |
| `part04/p04_s04_turbotrain_gradient.py` | `backprop_3/geometry_while_learning_2.py`, decision boundary utilities | Loss landscape/gradient conflict as moving vectors on surface |
| `part04/p04_s05_quantv2x.py` | `network_flow.py` block stack + compression motif | 32-bit feature blob squeezes into codebook/INT8 packets |
| `part04/p04_s07_latency_chain.py` | `wave_machine.py`, packet flow | Latency chain with moving pulses and bottleneck glow |
| `part05/p05_s03_metaurban.py` | `custom/logo.py:216`, `generalization` scaling curves | Procedural scene tiles assemble, curve shows diversity > quantity |
| `part05/p05_s04_urbansim.py` | `network_flow.py` depth blocks, `covid.py` agent grids | CPU/GPU bottleneck removed, 256 environments tile grid |
| `part05/p05_s05_citywalker_pedgen.py` | VLA diffusion/action frames, agent cluster dynamics | Zombie city -> human-aware paths with diffusion skeleton emergence |
| `part05/p05_s06_vid2sim.py` | image-patch grids, 3D mesh/surface ideas | Video -> gaussian particles -> mesh -> interactive sim |
| `part05/p05_s07_living_city.py` | `model3d.py:260`, `light.py:216`, `covid.py:723` | 3D living city with RSU towers, waves, links, agent choreography |
| `part05/p05_s08_final_summary.py` | `custom/logo.py:192`, `custom/logo.py:216`, city agent dynamics | Full closing montage: five parts converge into living city |

## Copy vs Adapt Guidance

| Category | Recommendation | Reason |
|---|---|---|
| Tiny pure helpers (`inverse_quadratic`, color boost, vector math) | Copy/adapt into scene-local helper only if needed | Small, self-contained, easy to port |
| Manimlib classes (`InteractiveScene`, `TexturedGeometry`, `DotCloud`, `VFadeIn`, `LaggedStartMap`) | Do not import directly | Project uses Manim Community; APIs diverge |
| Asset-dependent VLA scenes | Adapt only | Paths are local to Welch machine and assets are not guaranteed |
| 3B1B logo/characters | Do not copy branding | Use assembly/animation ideas only |
| 3D tower/waves/spotlight math | Port original CE equivalent | High visual value and relevant to AV/V2X |
| Neural/attention diagrams | Reimplement with project palette | Best fit for Part 1 and Part 2, but local visuals must be original |

## Rebuild Helper Candidates to Add Later

Do not add these to `beyond/components/` unless user explicitly allows component edits. For now, implement scene-local helpers or a new allowed scene helper file if scope changes.

| Helper Name | Inspired By | Purpose |
|---|---|---|
| `make_rsu_tower_3d` | `RadioTower` | Reusable 3D V2X infrastructure tower |
| `expanding_signal_shells` | `RadioBroadcast.update_shells` | 3D radar/V2X wave pulses |
| `spotlight_fan` | `Spotlight` | Sensor cone / LiDAR / camera frustum |
| `ambient_glow_rings` | `AmbientLight` | Node glow and coverage halo |
| `feature_rows` | `p31_61_1.make_embedding_row` | Compact latent feature visualization |
| `attention_flash_arcs` | `play_simple_attention_animation` | Attention/fusion as flashing arcs |
| `token_to_embedding_flow` | `show_initial_text_embedding` | Prompt/image/sensor -> token features |
| `repeated_model_stack` | `mention_repetitions` | Show many layers without text |
| `agent_trails` | `DotHistory` | Living movement paths for cars/pedestrians |
| `coordinate_frame_align` | `LinearTransformationScene` | Calibration transforms |
| `region_mask_from_lines` | `region_from_line_boundary` | Occlusion/risk fields |

## Immediate Recommended Next Steps

1. Rebuild the three iconic 3D scenes first:
   - `intro/i02_the_hook.py`
   - `part02/p02_s04_occlusion.py`
   - `part05/p05_s07_living_city.py`

2. Then rebuild Part 1 VLA scenes using Welch VLA references:
   - `part01/p01_s06_vla_gallery.py`
   - `part01/p01_s07_vla_arch.py`
   - `part01/p01_s08_autovla.py`

3. Then rebuild Part 4 training/efficiency scenes using geometry/decision-boundary references:
   - `part04/p04_s03_coopre.py`
   - `part04/p04_s04_turbotrain_gradient.py`
   - `part04/p04_s05_quantv2x.py`

4. For each scene, port only the smallest useful pattern and render-check frames at 35/60/85 percent.

