# Script — Part 5: Building Scalable, Human-Centric Physical AI
**Tutorial: Beyond Self-Driving — ICCV 2025**
*Speaker: Wayne Wu, Research Associate, UCLA Mobility Lab*

> Scene IDs map to `studio/scenes/part05/`.

---

### [P05S01Title — "Scalable, Human-Centric Physical AI"]

Part 5 broadens the discussion from self-driving cars to physical AI. The goal is scalable embodied intelligence that can operate safely in complex spaces shared with people.

---

### [P05S02ALLMVsRobot — "Why Robots Are Different from LLMs"]

Large language models succeeded because of one thing: the internet. Trillions of tokens of human-generated text, freely available, covering virtually every domain of human knowledge and behavior. Training on that corpus gave LLMs world knowledge, common sense, and generalizable reasoning — capabilities that emerged from scale, not from hand-engineered rules.

Robots do not have an internet.

Robotic behavior data must be collected physically — each robot, in each environment, performing each task, observed by sensors and annotated either by humans or by auxiliary systems. You cannot crawl the web for robot navigation trajectories. There is no existing corpus of "how a delivery robot should navigate a crowded university campus." The data problem for physical AI is categorically different from the data problem for language AI.

---

### [P05S02BTwoBarriers — "Two Barriers"]

The path from current robotics to general-purpose Physical AI is blocked by two distinct barriers.

**Barrier 1: No web-scale robot behavior data.** Behavior cloning — the most direct path to learning robot skills — requires large quantities of demonstration data in the target environment. Collecting it at the scale needed for general policies requires either an enormous fleet of physical robots or a simulation environment realistic enough that sim-to-real transfer works reliably.

**Barrier 2: No human modeling in context.** Robots operating in shared human spaces — urban streets, campuses, malls, hospitals — must predict and respond to human behavior to be safe. A robot that cannot model pedestrian intent cannot safely navigate a crosswalk. And pedestrian behavior is highly variable, context-dependent, and affected by subtle social cues that are very difficult to capture in existing motion datasets.

The recipe for overcoming both barriers requires two complementary tracks: **scalable scene simulation** to generate the robot behavior data that doesn't exist in the real world, and **human behavior modeling** to bring pedestrians and cyclists out of the "zombie" category — scripted, unrealistic, incapable of surprising the robot — into genuinely interactive agents.

---

### [P05S03Micromobility — "Micro-Mobility Testbed"]

The testbed for this work is not highways or freeways. It is the environment where most urban movement actually happens.

In the United States, approximately 60% of all trips are shorter than 5 miles — distances ideally served by micro-mobility: delivery robots, AI-powered wheelchairs, electric scooters, compact unmanned ground vehicles. These agents navigate sidewalks, crosswalks, and mixed pedestrian-vehicle spaces. Their operating environment is far more complex than a highway — it is unstructured, highly variable, and shared with humans who do not follow predictable rules.

UCLA partners with COCO Robotics, a company deploying autonomous delivery robots in real campus and urban environments, as the real-world validation testbed for the methods in this part.

---

### [P05S04ACompositionalQuote — "A Fundamental Insight"]

> *"The world is compositional, or there is a god."* — Stuart Geman

This observation from Brown University statistician Stuart Geman points at something fundamental about how environments work. The world is not a fixed list of named places. It is built from components — roads, intersections, sidewalks, buildings, trees, furniture — combined in an essentially infinite number of configurations. If a robot can understand the components and their relationships, it can generalize to any combination it has never seen before.

This insight is the foundation of the simulation approach in this part.

---

### [P05S04BMetaUrban — "MetaUrban"]

**MetaUrban**, published as an ICLR 2025 Spotlight, is a compositional simulation platform for urban environments.

Instead of designing specific scenes, MetaUrban uses **description scripts** to procedurally generate environments: the number of city blocks, intersection types, lane widths, sidewalk configurations, vegetation density, and the placement and density of objects — vehicles, pedestrians, traffic signs, street furniture. Varying these parameters across different distributions generates an effectively infinite variety of unique training environments. No two training scenes need to be identical.

UrbanVerse, built on top of MetaUrban, adds realism by reconstructing real urban environments from city-tour video footage into simulation scenes, capturing the actual spatial distribution of urban assets without the manual effort of 3D modeling.

---

### [P05S04CMetaUrbanScaling — "Power-Law Scaling"]

The most important empirical finding from MetaUrban is about **scene diversity**, not quantity.

When you vary the number of unique training environment layouts and measure performance on unseen test environments, the relationship follows a power law: doubling the number of unique layouts improves generalization by a consistent multiplicative factor. This is not linear, and it is not subject to diminishing returns in the dataset size range studied.

The practical implication: a training set of 100 diverse, procedurally varied scenes generalizes better than 1,000 repetitions of the same scene layout with minor agent placement variations. Diversity in the environment distribution matters more than raw volume of experience in any specific environment.

---

### [P05S05AUrbanSimBottleneck — "UrbanSim: The Training Bottleneck"]

Scene diversity creates another problem: if training an agent to navigate diverse environments requires 180 GPU-days on a state-of-the-art platform, the computational cost of experimentation becomes a fundamental barrier.

Traditional simulation platforms like iGibson and CARLA have a CPU-GPU architecture: the physics simulation runs on CPU, observations are computed on CPU, the data is transferred to GPU for neural network inference, and actions are transferred back to CPU for execution. Each CPU-GPU data transfer in this loop adds latency. With hundreds of parallel environments, these transfers dominate the wall-clock time.

This is the bottleneck that UrbanSim was built to eliminate.

---

### [P05S05BUrbanSimResults — "UrbanSim: 180 Days → 3 Hours"]

**UrbanSim**, published as a CVPR 2025 Highlight, moves the entire hot training loop onto the GPU — physics simulation, observation computation, and neural network inference all running on-device, with no CPU-GPU transfers in the critical path.

The additional design decision is **asynchronous scene sampling**: instead of all parallel environments sharing a synchronized global clock and identical object configurations, each environment has an independent, heterogeneous configuration that is resampled asynchronously. This maximizes the diversity of experience per GPU-hour while further reducing synchronization overhead.

The measured results: **2,620 simulation frames per second** running 256 parallel environments simultaneously, using only 11.2 GB of GPU memory — 24.3% of the available 46 GB on a single GPU.

Training outcome: after 3 hours of wall-clock training with 256 parallel environments, the agent reaches **41% task success rate**. A single-environment baseline — the standard research setup — reaches only 6% in the same wall-clock time. The old 180 GPU-day estimate corresponds to approximately 3 hours on UrbanSim.

Deployment validation on a COCO wheeled delivery robot and a Unitree Go2 quadruped confirms the sim-to-real transfer: agents trained in UrbanVerse reconstructed environments outperform all prior state-of-the-art navigation models on both crosswalk and sidewalk scenarios.

---

### [P05S06ACityWalker — "CityWalker Dataset"]

The simulation bottleneck is resolved. Now for the human modeling problem.

Existing human motion datasets — AMASS, HumanAct12, and similar motion capture collections — record human movement in isolation. A person performs actions in a studio, without environmental context, without a destination, without other people around. Motion generated from these datasets walks through walls, ignores obstacles, and produces trajectories that are spatially incoherent with any real environment.

**CityWalker** is the first dataset designed to capture pedestrian behavior in the context of real urban environments: 30.8 hours of high-quality egocentric video, 120,914 individual pedestrians tracked, 16,215 distinct scene segments from 227 cities worldwide.

The diversity is not just quantitative. The dataset captures people pushing strollers, looking at their phones while walking, stopping to take photos, gesturing to companions, navigating through crowds — the full spectrum of real urban pedestrian behavior, not performance for a camera.

---

### [P05S06BPedGen — "PedGen: Pedestrian Motion Generation"]

**PedGen** is a diffusion model for pedestrian motion generation conditioned on three input streams.

**Scene Context**: a 3D voxel representation of the immediate environment, encoding what is a wall, what is a road, where obstacles are. This allows the generated pedestrian to navigate around real obstacles rather than through them. **Body Context**: SMPL body shape parameters representing the physical characteristics of the specific individual, so that motion is appropriate for their body size and proportions. **Goal**: the spatial destination the pedestrian is moving toward, which governs the overall trajectory direction.

The loss function combines three terms: reconstruction loss to keep body poses anatomically plausible, trajectory loss to ensure the integrated path goes in the right direction, and geometry loss through forward kinematics to keep all joints in physically valid positions in 3D space.

The qualitative result is significant: without context conditioning, generated pedestrians walk through obstacles and follow incoherent paths. With context, they navigate naturally, avoid barriers, and move toward their goals in ways that a robot interacting with them could reasonably predict.

---

### [P05S07ZombieToAlive — "From Zombie City to Living City"]

Simulation environments without realistic pedestrian models are often described as "zombie cities" — populated with agents that move mechanically, without behavioral intent or social awareness. These agents don't react to robots, don't avoid each other naturally, and don't produce the kind of social dynamics that real urban environments contain.

PedGen begins the transition from zombie city to living city. When pedestrians are generated with scene-aware, goal-conditioned motion, the simulation environment starts to exhibit the emergent social dynamics — crowd dispersion, path negotiation, stopping-and-starting — that any robot deployed in a real city will need to navigate.

---

### [P05S08Vid2Sim — "Vid2Sim"]

**Vid2Sim**, published at CVPR 2025, offers a different approach to the simulation realism problem: instead of building environments from scratch or from 3D models, convert video footage of real environments directly into interactive simulation.

The pipeline combines two reconstruction techniques. **3D Gaussian Splatting** reconstructs the visual appearance of a scene from multi-view images, producing photo-realistic rendering from arbitrary viewpoints. This gives the robot observations that look like the real world. **Mesh reconstruction** provides the physical geometry: surfaces the robot can stand on, walls it cannot walk through, objects it can interact with physically.

The combination gives a simulation environment where observations are photorealistic (from 3DGS) and physics are accurate (from mesh). A robot trained in a Vid2Sim environment sees and feels something very close to the real environment — which is why sim-to-real transfer works better here than in environments constructed purely from parametric 3D models.

---

### [P05S09LivingCity — "The Living City"]

*(Camera pan across a populated urban simulation environment. Brief hold — emotional payoff.)*

This is what the full stack produces: a simulated city with realistic geometry, photorealistic rendering, physically correct surfaces, and populated by pedestrians that navigate, react, and move in ways that reflect real human behavior.

A robot trained in this environment inherits all of that: spatial awareness, reactive navigation, and the ability to anticipate the kind of behavior it will encounter when deployed in the real world.

---

### [P05S10ChainOfSolutions — "Chain of Solutions"]

The five parts of this tutorial form a causal chain of problems and solutions.

**Part 1** identified the fundamental limitation of single-agent autonomous driving — long-tail edge cases that exceed the generalization capacity of any fixed training distribution — and proposed foundation models as the mechanism for acquiring the generalizable world knowledge needed to address them.

**Part 2** identified the physical limitation of any single agent regardless of its intelligence — occlusion — and proposed V2X cooperative perception with spatio-temporal fusion, trained efficiently through TurboTrain, planned through the interpretable RiskMap.

**Part 3** grounded the cooperative system in reality — hardware, calibration, localization, real-world datasets, and the digital twin infrastructure needed to close the loop between simulation and deployment.

**Part 4** made the system efficient — CooPre for data efficiency, TurboTrain for training efficiency, QuantV2X for inference efficiency — so that it can scale from research prototypes to real deployments.

**Part 5** extended the entire paradigm beyond cars: MetaUrban and UrbanSim for scalable training environments, CityWalker and PedGen for realistic human modeling, Vid2Sim for photorealistic sim-to-real transfer.

---

### [P05S11FinalFrame — "Beyond Self-Driving"]

The title of this tutorial is *Beyond Self-Driving*. The "beyond" has two meanings.

It means beyond the capability of today's autonomous vehicles: beyond the occlusions, the long-tail edge cases, the deployment barriers, the efficiency constraints. Every part of this tutorial addressed a piece of that gap.

And it means beyond self-driving cars entirely: toward Physical AI that operates safely in any physical environment, alongside any agent — human or robotic — in the shared spaces of our cities.

That is the research program of the UCLA Mobility Lab. And this tutorial is an invitation to contribute to it.

---
*[End of Part 5 — ~12 min]*
