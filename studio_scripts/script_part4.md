# Script — Part 4: From Pre-Training to Post-Training — Building an Efficient V2X System
**Tutorial: Beyond Self-Driving — ICCV 2025**
*Speaker: Seth Z. Zhao, PhD Candidate, UCLA Mobility Lab*

> Scene IDs map to `studio/scenes/part04/`.

---

### [P04S01Title — "From Pre-Training to Post-Training"]

Part 4 asks how the full V2X system can scale. We follow the efficiency problem from data and pre-training through optimization, compression, and real-time inference.

---

### [P04S02V2XOverview — "V2X: The Full Picture"]

Vehicle-to-Everything — V2X — is the paradigm in which vehicles and infrastructure share sensor data to overcome the physical limitations of any single agent's viewpoint. Parts 2 and 3 built the theoretical foundation and the real-world deployment infrastructure. The result is a system that works.

But "works" in a research context is different from "scales in deployment." V2X at scale means thousands of intersections, millions of vehicles, edge devices with fixed compute budgets, and training pipelines that researchers can actually run. The U.S. Department of Transportation is actively funding smart intersection programs for pedestrian safety — which means the efficiency questions in this part have near-term practical consequences.

Three bottlenecks stand between the systems built in Parts 2 and 3 and real-world scalability: how to reach good performance when labeled data is limited, how to train efficiently without extensive human guidance, and how to run inference in real time on edge hardware.

---

### [P04S03AnnotationCost — "The Annotation Bottleneck"]

The V2X dataset ecosystem has grown rapidly. V2V4Real contains 240,000 annotated frames. DAIR-V2X has 460,000. V2X-Real has 1.2 million. The scale of data is impressive — but annotation cost scales linearly with it.

Annotating 3D LiDAR point clouds is labor-intensive. It requires specialized software, trained annotators who understand 3D spatial relationships, and multi-layer quality control processes. A single annotated LiDAR frame can cost orders of magnitude more than a labeled 2D image. Scaling to millions of frames through human annotation alone is not economically viable.

The question becomes: how do we get good model performance without requiring every frame to be labeled?

---

### [P04S04CooPReMasked — "CooPre: Masked Voxel Pretraining"]

**CooPre** — Cooperative Pretraining for V2X — is the first self-supervised pretraining method designed specifically for multi-agent cooperative perception, published at IROS 2025.

The mechanism is masked voxel reconstruction. During pretraining, the model receives multi-agent LiDAR point clouds projected onto BEV voxel grids. Forty percent of the voxels are randomly masked — hidden from the model. The model is then asked to reconstruct the masked regions. No detection labels are needed. No task objective is defined. The model simply learns to predict what the environment looks like in locations it cannot directly observe.

This pretraining task has a strong and relevant inductive bias for cooperative perception: to reconstruct masked voxels, the model must learn to use information from the other agent's viewpoint to fill in what is missing from its own. That is precisely the cooperative skill that downstream detection will require.

After pretraining, the model is fine-tuned on the detection task with labeled data. The result: at 50% of the labeled training data, CooPre matches the performance of a model trained from scratch on 100% of the data. With all 100% labels, it improves by an additional 4.5 mAP points. Cross-domain pretraining — pretrain on one dataset, fine-tune on another — also outperforms single-domain baselines, suggesting the representations are genuinely general.

---

### [P04S05TurboTrainLandscape — "TurboTrain: Training Landscape"]

Part 2 introduced TurboTrain as a solution to training instability. Here we look more carefully at why the problem is as hard as it is.

This chart shows the training outcome landscape for multi-agent, multi-frame, multi-task systems. Orange points are one-time training attempts on the full architecture — they cluster near zero on both detection and prediction accuracy. They don't degrade gracefully; they fail. The blue points are the result of a carefully sequenced four-stage manual training process requiring 120 epochs and expert judgment at each transition.

The two root causes are initialization sensitivity and gradient conflict. A system with temporal, multi-agent, and multi-task dimensions has a loss landscape with many sharp local minima — starting from random initialization almost always lands in one of them. And when detection loss, prediction loss, and planning loss are optimized simultaneously, their gradients frequently point in opposing directions in weight space. Standard SGD has no mechanism for resolving this — one task's progress undoes another's.

---

### [P04S06LatencyChain — "Latency Chain"]

Before addressing inference efficiency, it helps to understand the full latency budget of a V2X system.

Each agent runs local inference on its sensor data. This takes time. The compressed features are transmitted over the V2X communication channel. Transmission adds latency. The receiving agent runs fusion inference to integrate the received features with its own. This adds more time. The total round-trip must fit within the real-time decision cycle — typically 100–200 milliseconds — or the system is already operating on stale information.

Every component of this chain matters. Improving model-level inference speed without addressing communication bandwidth misses half the problem. The full system must be co-optimized.

---

### [P04S07AArithmeticCost — "Arithmetic Cost"]

Why is neural network inference expensive on edge hardware?

Neural networks are dominated by two operations: multiply-accumulate in fully connected and convolutional layers, and memory reads to load weights from off-chip memory. The energy costs are revealing. A 32-bit floating-point multiplication costs roughly 3.7 picojoules. A 32-bit memory access from DRAM costs approximately 640 picojoules — more than 170 times more expensive than the computation itself.

---

### [P04S07BMemoryBound — "Memory-Bound Inference"]

This means inference on edge hardware is memory-bound, not compute-bound. The bottleneck is not running the arithmetic but loading the model parameters. Reducing the bit-width of weights from 32-bit float to 8-bit integer cuts the memory footprint by 4×, replaces multiplications with cheaper integer additions, and enables hardware accelerators designed specifically for INT8 operations on modern edge chips.

---

### [P04S08QuantV2X — "QuantV2X: Fully Quantized Pipeline"]

**QuantV2X** is the first fully quantized cooperative perception pipeline, addressing both the model and the communication channel simultaneously.

At the model level, all weights and activations are quantized from FP32 to INT8. This gives the 4× memory reduction, enables INT8-optimized hardware paths, and reduces both energy consumption and inference latency. The challenge is that cooperative perception involves spatial feature maps — quantization of structured representations requires careful calibration to avoid accuracy loss.

At the communication level, instead of transmitting FP32 BEV features, QuantV2X compresses features into a learned low-bit codebook representation. The transmitted codewords are 300× smaller than uncompressed BEV features in raw bytes. This directly reduces the transmission latency in the V2X communication step of the latency chain.

The key contribution is not demonstrating that quantization works for a single model — that was known. It is demonstrating that a fully quantized end-to-end cooperative perception pipeline — both model and communication — achieves acceptable accuracy on real benchmarks, making it viable for deployment.

---

### [P04S09EfficiencySummary — "Efficiency Summary"]

Three bottlenecks, three solutions.

**CooPre** addresses the data bottleneck: self-supervised pretraining that learns cooperative representations without annotation, cutting the labeled data requirement by half.

**TurboTrain** addresses the training bottleneck: masked pretraining establishes a stable initialization, then conflict-suppressing gradient balancing enables multi-task convergence — reducing training from 120 to 45 epochs, with no manual stage management required.

**QuantV2X** addresses the inference bottleneck: full INT8 quantization of both the model and the communication channel, cutting memory footprint and transmission cost while preserving operational accuracy.

Together, these make the V2X system built in Parts 2 and 3 tractable: it can be trained, it can learn from limited data, and it can run on real edge hardware.

---

### [P04S10BridgeToP5 — "Bridge to Part 5"]

The efficiency problems are solved. The V2X stack is now deployable.

But Parts 2, 3, and 4 have been focused entirely on one category of agent: wheeled vehicles on roads, coordinating with fixed infrastructure. The physical world is much wider. Delivery robots on sidewalks, electric wheelchairs at crosswalks, quadruped robots in parks, humanoid robots in offices — and all of them operating in the same spaces as human pedestrians, cyclists, and children.

Safe operation in environments shared with humans requires something that V2X systems for vehicles have not needed to model: human behavior. And building AI that operates safely in those environments requires simulation tools, training pipelines, and behavior datasets that simply don't exist yet — or didn't, until recently.

That is the subject of Part 5.

---
*[End of Part 4 — ~10 min]*
