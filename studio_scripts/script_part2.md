# Script — Part 2: Towards End-to-End Cooperative Automation
**Tutorial: Beyond Self-Driving — ICCV 2025**
*Speaker: Zewei Zhou, PhD Candidate, UCLA Mobility Lab*

> Scene IDs map to `studio/scenes/part02/`.

---

### [P02S01Title — "Cooperative Perception"]

Part 2 moves from one intelligent vehicle to many connected agents. The focus is cooperative perception: sharing complementary viewpoints across vehicles and infrastructure.

---

### [P02S02A119M — "1.19 Million Deaths"]

Every year, 1.19 million people die in road traffic crashes worldwide. That is a 737 crashing every hour, every day, every year. 94% of these accidents involve human error — driver distraction, impaired judgment, failure to see a hazard in time.

This is not an abstract statistic for a paper introduction. It is the actual scale of the problem that motivates this entire research area. Automated mobility, done correctly, could eliminate most of these deaths.

---

### [P02S02BWaymoReduce — "Waymo: 80% Reduction"]

Waymo recently released a large-scale safety study comparing its autonomous vehicles to human drivers in equivalent traffic conditions. The result: an 80% reduction in injury-causing crashes.

This is a meaningful number because it comes from real-world deployment, not simulation. It demonstrates that the technology works at some level — and raises the question of how to make it work everywhere, for all agents, not just well-funded robotaxis in select geofenced areas.

---

### [P02S03E2EEvolution — "Single-Agent Evolution"]

Before multi-agent systems, let's look at where single-agent autonomous driving had arrived by 2024.

The trajectory is clear. PnPNet introduced joint perception and prediction using convolutional networks and recurrent modules. GameFormer brought interactive prediction into planning, modeling other agents as game-theoretic players. UniAD unified the entire pipeline — perception, prediction, planning — into a single query-based end-to-end model optimized jointly. DiffusionDrive, the most recent milestone, uses a diffusion model to generate trajectory distributions with principled uncertainty representation.

Each step reduced the handoff cost between modules and improved joint optimization. End-to-end architectures are genuinely better than modular ones on benchmarks, with three key advantages: no error accumulation between stages, no information loss between representations, and global optimization toward a single driving objective.

But performance on benchmarks in controlled conditions is not the same as safety in the full physical world.

---

### [P02S04AOcclusionProblem — "The Occlusion Problem"]

Here is the fundamental limitation that end-to-end improvements cannot fix.

These two rows of LiDAR scans show the same intersection. The top row is a single-agent scan: one point of origin, one field of view. Large dark regions surround the vehicle — areas where no point cloud data exists, where the sensor cannot reach. The bottom row adds a second agent at a different position: the dark regions shrink dramatically. Information that was simply absent in the single-agent view is now present.

This is not an algorithm problem. It is a geometry problem. A single LiDAR cannot see around occlusions. If a truck is blocking the view, there is no signal to process. The only solution is complementary information from a different vantage point — which means multiple agents, and communication between them.

---

### [P02S05RadarWaves — "Cooperative Coverage"]

*(3D visualization — radar spheres expanding from two vehicles. Brief hold.)*

When two vehicles share their perception data, the combined field of view is not just the union of two circles. It fills in the precise occlusions that each individual agent experiences. The cooperation is geometrically additive: what one cannot see, the other can.

---

### [P02S06RelatedWorks — "Related Works"]

The cooperative perception community has been working on this problem for several years, and the methods have become progressively more sophisticated.

V2VNet was one of the early systems, using graph neural networks to aggregate features from multiple agents. V2X-ViT extended this with Transformer-based attention across vehicle-to-infrastructure pairs. Where2comm introduced sparse communication, learning which spatial locations are worth transmitting rather than sending the entire feature map. CodeFilling brought codebook-based feature compression, reducing the communication cost further.

Datasets have similarly matured: from the purely simulated OPV2V, to DAIR-V2X with real infrastructure data, to V2X-Real — the first large-scale real-world dataset covering both vehicle-to-vehicle and vehicle-to-infrastructure scenarios.

But across all of these contributions, two critical gaps remained open.

---

### [P02S07ResearchGaps — "Research Gaps"]

**Gap one: the task scope.** Every prior method addressed cooperative perception as a detection problem — classify objects, output bounding boxes, stop there. How cooperation benefits the full automation chain — prediction and motion planning — was unexplored. Prediction requires understanding the history of object motion, not just its current position. Without temporal context, the forecast is severely limited.

**Gap two: the data.** Existing datasets lacked the sequential, time-series structure that temporal fusion requires. And critically, no dataset covered all V2X collaboration modes simultaneously: vehicle-to-vehicle, vehicle-to-infrastructure, and infrastructure-to-infrastructure in one place, at scale.

---

### [P02S08ThreeQuestions — "Three Core Questions"]

The gaps point to three concrete research questions that any serious V2X system must answer.

**What to transmit?** Raw sensor data, detected objects, or intermediate feature maps — each trade-off has implications for bandwidth, accuracy, and latency. **When to transmit?** A single frame? A history? And how do you decide when agents are too far apart to communicate efficiently? **How to fuse?** Once data from multiple agents arrives at the ego vehicle, how do you integrate information from different viewpoints, timestamps, and sensor modalities into a single coherent scene representation?

These three questions frame the contributions in this part.

---

### [P02S09V2XPnPArch — "V2XPnP Framework"]

**V2XPnP** — Vehicle-to-Everything Spatio-Temporal Fusion for Perception and Prediction — addresses all three questions in a unified end-to-end framework presented at ICCV 2025.

*What to transmit?* V2XPnP evaluates all three fusion strategies — early (raw data), late (detected objects), and intermediate (BEV feature maps) — each with a temporal dimension. The comparison is not just about accuracy, but about which representation preserves the most useful structure for downstream tasks.

*When to transmit?* This is the subtle question. Agents are not always within communication range. The opportunity to exchange information is finite — once two vehicles have passed each other, that data is gone. V2XPnP uses a one-step communication strategy: when agents are within range, they transmit their full history — multiple frames compressed together — in a single exchange. Temporal attention then compresses this multi-frame history into a single-frame representation before transmission, preserving temporal context within a practical bandwidth budget.

*How to fuse?* Two complementary modules: temporal attention aggregates the motion history of each individual agent, and spatial attention then integrates information across different agents at the same timestep. Together, they produce a multi-agent spatio-temporal representation that captures both the dynamics of the scene and the complementary viewpoints of all cooperating agents.

---

### [P02S10V2XPnPDataset — "V2XPnP-Seq Dataset"]

To support the framework, the team built **V2XPnP-Seq** — the first real-world sequential dataset covering all V2X collaboration modes simultaneously.

The setup includes two connected automated vehicles and two infrastructure nodes at a real urban intersection. The dataset contains 40,000 LiDAR frames, 208,000 camera frames, and full HD map annotations and trajectory labels for downstream prediction and planning tasks. V2V, V2I, V2X, and I2I scenarios are all represented.

Benchmark results confirm the framework's design choices: intermediate feature fusion combined with one-step communication and temporal-spatial-map fusion outperforms all prior state-of-the-art methods.

---

### [P02S11ATurboTrainProblem — "Training Challenge"]

Building the framework is one thing. Training it is another.

This chart shows the core difficulty. On the x-axis is detection accuracy; on the y-axis is prediction accuracy. The orange dots are one-time training attempts on the full multi-agent, multi-frame, multi-task system — they fail outright, landing near zero on both axes. The blue dots are the result of carefully sequenced manual training: four separate stages (single-agent detection, temporal prediction, joint fine-tuning, multi-agent fusion), run sequentially over 120 epochs, requiring expert judgment about when to transition between stages.

Why is one-time training so hard? Two reasons. **Initialization sensitivity**: a complex architecture with multiple dimensions — temporal, multi-agent, multi-task — converges to a bad local minimum when trained from random initialization. **Gradient conflict**: detection, prediction, and planning objectives pull the model's weights in contradictory directions. When conflict is severe, improving one task degrades another. Standard stochastic gradient descent has no mechanism to resolve this.

---

### [P02S11BTurboTrainSolution — "TurboTrain Solution"]

**TurboTrain** solves both problems with a two-stage pipeline that replaces the fragile four-stage manual process.

**Stage 1 — Masked Pretraining**: the model learns a task-agnostic 4D spatio-temporal representation by reconstructing masked LiDAR point clouds from multi-agent, multi-frame data. No annotations are needed. No task-specific objective is defined. The model simply learns the structure of cooperative scenes — what voxels look like, how they evolve over time, how one agent's missing data can be inferred from another's. This establishes a stable initialization that resolves the sensitivity problem.

**Stage 2 — Gradient Balancing**: fine-tuning alternates between free gradient steps — where each task learns without interference — and conflict-suppressing steps that detect gradient conflicts and apply a resolution strategy. This prevents any one task from dominating the optimization.

The result: 45 epochs instead of 120, higher final performance than the manual four-stage process, and no requirement for human expertise to manage the training schedule.

---

### [P02S12RiskMap — "RiskMap"]

Perception and prediction enable the vehicle to understand the scene. Planning requires using that understanding to make safe decisions. And this is where interpretability becomes critical.

Consider the three architectures for this transition. Modular: perception feeds prediction feeds planning through separate modules — error accumulation, limited range, but interpretable. Conventional end-to-end: the network decides everything — compact and jointly optimized, but a black box. No engineer can verify why a specific planning decision was made.

**RiskMap** introduces a middle path: an explicit Risk Map as middleware between the learned representation and the planner. The Risk Map is a probabilistic spatial-temporal representation of danger — a two-dimensional map in which each cell encodes the likelihood of a hazardous event at that location and time. A learning-based Model Predictive Controller then uses the Risk Map to compute a safe trajectory.

This separates two questions that the black-box approach conflates: "where is the environment dangerous?" (which AI handles well) and "given that danger map, what is the safest trajectory?" (which can be formally verified). RiskMap outperforms all prior fusion methods and planning models on detection, prediction, and planning metrics simultaneously.

---

### [P02S13Summary — "Part 2 Summary"]

Three problems, three solutions forming a complete stack.

**V2XPnP** establishes the foundation: a real-world dataset covering all V2X modes, and a framework that answers the what-when-how of spatio-temporal cooperative fusion, evaluated end-to-end across perception and prediction tasks.

**TurboTrain** solves the practical training bottleneck: a pretraining-plus-balancing pipeline that makes the complex multi-task system trainable without expert intervention, cutting training time by more than half.

**RiskMap** extends the stack toward safe planning: an interpretable middleware that turns learned scene understanding into a verifiable planning interface.

---

### [P02S14BridgeToP3 — "Bridge to Part 3"]

All three systems have now been built. They work in simulation and on benchmark datasets. But deploying them in the real world requires something we have not discussed: the hardware, the sensors, the calibration, the localization infrastructure, and the data collection pipelines that make real-world training and operation possible.

The gap between a simulated cooperative perception system and one that runs on a real intersection is significant — and it is exactly the gap that Part 3 addresses.

---
*[End of Part 2 — ~10 min]*
