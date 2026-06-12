# Script — Part 1: Foundation Models for Autonomous Driving
**Tutorial: Beyond Self-Driving — ICCV 2025**
*Speaker: Dr. Zhiyu Huang, Postdoctoral Researcher, UCLA Mobility Lab*

> Scene IDs map to `studio/scenes/intro/` (preamble) and `studio/scenes/part01/`.
> On-screen text is English; this script is the English narration for voice recording.

---

## INTRO PREAMBLE

### [I01TitleCard — "Beyond Self-Driving"]

This video was created as a project for the Introduction to Machine Learning course at the University of Science, VNU-HCM. We are Continuer: Phạm Phú Hòa, student ID 23122030; Nguyễn Lâm Phú Quý, 23122048; and Bàng Mỹ Linh, 23122009.

Together, we will summarize *Beyond Self-Driving*, an ICCV 2025 tutorial from the UCLA Mobility Lab, and connect its five parts into one story.

---

### [I02TheHook — "The Hook"]

Imagine a smart car equipped with the latest AI. It perceives its surroundings in real time, reasons about what it sees, and makes split-second decisions. But here is the fundamental problem: even the most intelligent single agent is blind to what it cannot physically see. A truck parked at the corner, a pedestrian hidden behind a wall — no model, no matter how powerful, can see through obstacles.

Now add a second vehicle with a different vantage point. Suddenly the hidden pedestrian is visible. What one agent misses, another agent catches. This is the core insight behind cooperative perception: not making one agent smarter in isolation, but enabling multiple agents to collaborate.

That's the thesis of this tutorial. So we taught them to cooperate.

---

### [I03Roadmap — "Five Parts"]

The tutorial unfolds in five parts. Part 1 asks why foundation models matter for autonomous driving and how they address its hardest problems. Part 2 explores how multiple agents fuse information across space and time. Part 3 grounds everything in real hardware and real-world deployment. Part 4 addresses efficiency — data, training, and inference. Part 5 zooms out to the broader frontier: Physical AI that operates safely in a world shared with humans.

---

### [I04BridgeToP1 — "Foundation Models Await"]

We begin with the models that bring broad world knowledge and general-purpose reasoning into autonomous driving.

---

## PART 1

### [P01S01Title — "Foundation Models for Autonomous Driving"]

Part 1 asks a simple question: can foundation models help autonomous vehicles reason beyond the situations explicitly covered by their training data?

---

### [P01S02AGenAITimeline — "The GenAI Boom"]

Here is the tension that motivates this entire part. Since 2020, generative AI has made extraordinary progress. GPT-3 appeared in 2020. CLIP and DALL-E followed. ChatGPT arrived in late 2022 and changed the public perception of what AI could do. GPT-4 in 2023, Gemini, LLaMA 3, and models that see, reason, and converse simultaneously — the timeline is relentless.

So why, in 2025, with all of this capability, have self-driving cars still not spread everywhere? That question is exactly what we need to answer.

---

### [P01S02BFMDefinition — "What Is a Foundation Model?"]

A foundation model is trained once on broad, large-scale data and then adapted to many downstream tasks. The data can span text, images, speech, and 3D signals. Pre-training compresses these modalities into a shared representation rather than building an isolated model for every task.

That shared model can then be adapted for information extraction, object recognition, instruction following, question answering, and many other applications. The key idea is visible in the diagram: broad data in, one reusable representation in the middle, and many specialized tasks out.

---

### [P01S03AModular — "Modular Architecture"]

The dominant deployed architecture for autonomous driving is the modular pipeline. Perception identifies objects and classifies the environment. Localization places the vehicle on the map. Prediction forecasts the future trajectories of other agents. Planning decides what the ego vehicle should do. Control executes that decision.

This pipeline is interpretable and easy to debug — each module can be tested independently — which is why it dominates commercial systems. But it has three fundamental weaknesses: errors accumulate from module to module, no joint optimization means each module pursues a local objective that may conflict with others, and the system cannot learn continuously from new experiences because each module is trained and frozen separately.

---

### [P01S03BE2E — "End-to-End Architecture"]

End-to-end systems replace the entire pipeline with a single neural network. Sensors go in, actions come out. There is no handoff between modules, no error accumulation, and the system can be optimized jointly for the final goal.

The cost is interpretability. When an end-to-end car makes a mistake, it is very difficult to diagnose where reasoning went wrong. Safety verification in a black box is a fundamental research challenge that the field has not yet solved.

---

### [P01S03CHybrid — "Hybrid Architecture"]

Hybrid architectures occupy the middle ground. Machine learning handles perception and high-level planning where it excels. Classical, verifiable control modules handle the actuators where reliability matters most. Many leading companies are converging on this design because it balances learning-based adaptability with engineering-grade hardware guarantees.

But all three architectures share a common weakness. Foundation models will make that weakness visible.

---

### [P01S04ALongtailProblem — "The Long-Tail Problem"]

Look at three real images from public roads.

First: a person standing in the middle of an active lane, phone in hand. Is the car still moving? Are they even aware of approaching vehicles? Second: a truck on the highway carrying three traffic lights — upside down, unlit, bouncing with the truck's movement. Will any detection module classify them as irrelevant? Third: a road buried under deep snow, lane markings completely invisible. Lane detection fails entirely.

These aren't constructed hypotheticals. They are the long tail of the distribution — rare events that are outside the training data of any system trained on standard conditions. 99% of driving is uneventful. But accidents happen in the 1% that looks like these three images. No dataset is large enough to enumerate all possible edge cases. The system needs another way.

---

### [P01S04BLongtailInsight — "The Common-Sense Gap"]

Why can human drivers handle these situations? Because we have contextual reasoning built over a lifetime of experience. We understand intent, physical causality, and social norms. We know that traffic lights strapped to a truck are irrelevant signals. We read behavioral cues from the person on their phone and adjust our expectations accordingly.

This is what autonomous systems lack: not more labeled examples of known scenarios, but genuine world knowledge that generalizes to scenarios never seen before. The thesis of this part is that foundation models are the first technology that may actually supply it. We need common-sense reasoning and generalist experience to handle new domains and the long tail.

---

### [P01S05FMEmpower — "Foundation Models Empower AV"]

Here is the connection between the foundation model ecosystem and autonomous driving.

On the left is the foundation-model ecosystem: vision models such as SAM, DINO, and CLIP; video generation models such as Cosmos and Wan; large language models; and multimodal language models such as Gemma and Qwen-VL.

Their shared world knowledge empowers the capabilities on the right: auto-labeling, scenario generation, sensor simulation, vehicle interfaces, language reasoning, and end-to-end driving.

Foundation models do not replace the autonomous-driving stack. They strengthen it with reusable knowledge, with the goal of long-tail generalization and more generalist driving experience.

---

### [P01S06VLARoadmap — "VLA Roadmap"]

Since 2023, researchers have explored four ways to integrate language models into driving: generating textual actions, producing numerical waypoints directly, providing high-level guidance to a separate trajectory planner, and transferring representations learned through language to downstream driving tasks.

The key insight: language is not just a channel for human-issued commands. It serves as an interface for contextual understanding and reasoning — a way for the model to articulate why it is making a decision, not just what the decision is. That articulation creates a strong inductive bias toward generalization.

To train these systems, new datasets were necessary. DriveLM chains language through perception, prediction, planning, and trajectory — forcing the model to explain each step. CoVLA and Impromptu VLA annotate real driving video clips with both trajectory data and language commentary. The result is a training signal that captures not just what happened, but why.

---

### [P01S07ABEVDriver — "BEVDriver"]

BEVDriver encodes LiDAR and camera data into a Bird's Eye View map — a unified top-down spatial representation of the environment — then feeds that representation into a large language model for waypoint prediction. The approach combines principled 3D geometric reasoning with the world knowledge and language capabilities of the language model. The BEV encoding bridges the two domains: spatial structure in, language reasoning through, trajectory out.

---

### [P01S07BEMMA — "EMMA"]

EMMA — End-to-End Multimodal Model for Autonomous Driving — from Waymo takes the most ambitious approach yet. Built on Gemini, the entire pipeline runs through language tokens. Raw camera frames arrive as input. The model produces a chain of thought: it first describes what it observes in the scene, then reasons about what other agents are likely to do, and only then commits to a trajectory — alongside structured outputs for object detection and road graph prediction.

There is no separate perception module, no rule-based planner. The model reasons out loud before it acts — like a student driver learning to narrate their thinking: "the car ahead is braking, I need to reduce speed and increase following distance."

---

### [P01S07CDriveVLM — "DriveVLM"]

DriveVLM from Tsinghua takes a dual-system approach. A Vision-Language Model operates at low frequency — perhaps a few times per second — handling scene understanding and high-level planning where language reasoning adds the most value. In parallel, a traditional 3D perception and trajectory planning module runs at full real-time frequency, handling the fast, safety-critical control loop.

The design combines the reasoning power of language models with the speed guarantees of classical modules. The trade-off is significant engineering complexity, but it is currently one of the most practical paths to a deployable VLA system.

---

### [P01S08AAutoVLASwitch — "AutoVLA: Dual Thinking"]

Previous VLA models had two related problems. First, generated action sequences were often physically infeasible — the model didn't learn the geometric and dynamic constraints of real vehicle motion well enough. Second, reasoning was always "slow" — the same chain-of-thought computation happened regardless of whether the scene required it, creating unnecessary latency.

AutoVLA, from UCLA, addresses both with a dual thinking mode design. In fast mode, the model outputs an action directly when the situation is routine. In slow mode, it activates a full chain-of-thought when the scene is ambiguous or complex — a pedestrian with unclear intent, a traffic event that requires interpreting multiple agents simultaneously.

This mirrors what cognitive science tells us about human decision-making. Routine routes run on near-automatic processing; unfamiliar or high-stakes situations trigger deliberate, effortful reasoning.

---

### [P01S08BAutoVLAResults — "AutoVLA Results"]

Results on the nuPlan and nuScenes benchmarks show a consistent finding across all four evaluation metrics: reasoning-augmented training outperforms action-only training. Teaching the model to think well makes it act well. This is not circular — the reasoning is evaluated separately from the action, so the improvement is genuine.

Reinforcement Fine-Tuning adds a 10.6% improvement in planning score and, notably, a 66.8% reduction in runtime. The slow-thinking mode is selective enough — only activated when needed — that it reduces the average computational burden rather than increasing it.

---

### [P01S09Takeaways — "Part 1 Takeaways"]

Four takeaways from this part.

**Foundation models open the long tail.** Systems that understand the world rather than memorizing rules can reason about situations never seen in training. **Multimodal LLMs are the leading architecture.** They bring out-of-domain reasoning, internet-scale world knowledge, and interpretable reasoning chains to a domain that has historically resisted all three. **There is no dominant paradigm yet.** Dual-system, unified end-to-end, BEV encoding, RL fine-tuning — the field is in active exploration, which is a sign of genuine intellectual progress, not stagnation. **Foundation models are not a complete solution.** Safety verification, interpretability, and formal guarantees remain open problems. Compute cost and latency are still real barriers to deployment at scale.

---

### [P01S10BridgeToP2 — "Bridge to Part 2"]

Foundation models may address the long-tail problem — but there is a physical limit that no model, however capable, can overcome alone.

A single agent is bounded by what it can see from its own position. If a vehicle is parked across the line of sight, if a pedestrian is hidden around a corner, no foundation model helps. The information simply doesn't exist at that sensor location.

The solution isn't a smarter model. It's a different paradigm entirely: enabling multiple agents to share what they see, so that collectively they perceive more than any one of them could alone. That's the subject of Part 2.

---
*[End of Part 1 — ~10 min]*
