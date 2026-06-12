# Script — Part 3: Bridging Simulation and Reality
**Tutorial: Beyond Self-Driving — ICCV 2025**
*Speaker: Zhaoliang Zheng, PhD Candidate, UCLA Mobility Lab*

> Scene IDs map to `studio/scenes/part03/`.

---

### [P03S01Title — "Bridging Simulation and Reality"]

Part 3 leaves the benchmark and enters the physical world. We now examine the hardware, calibration, localization, and deployment work needed to bridge simulation and reality.

---

### [P03S02SimRealGap — "The Sim-to-Real Gap"]

Parts 1 and 2 built a theoretically solid stack — foundation models for reasoning, cooperative spatio-temporal fusion for perception, RiskMap for interpretable planning. But every one of those systems was trained and evaluated on datasets. And datasets come from somewhere.

There is a well-known problem in robotics and autonomous driving called the sim-to-real gap: systems that work in simulation, or on carefully collected datasets, often fail when deployed on real hardware in real conditions. The reasons are concrete — sensors have noise characteristics that simulation doesn't perfectly model, weather changes in ways that training data doesn't cover, and the physical world has edge cases that no dataset designer anticipated.

This part is the engineering part. It covers how to build, calibrate, and deploy a real V2X system — from the hardware bolted to a pole at an intersection, to the algorithms running real-time on a moving vehicle.

---

### [P03S03SmartIntersection — "UCLA Smart Intersection"]

The testbed for this work is a real intersection: Charles E. Young Drive and Westwood Plaza, on the UCLA campus. This is not a closed test track. It is an active public intersection with real vehicles and pedestrians, operating every day.

The hardware deployment includes two infrastructure nodes. The northwest corner node carries a 128-line LiDAR, two cameras, and a radar unit. The southeast corner node carries a 64-line LiDAR, two cameras, and a C-V2X communication unit. Two connected automated vehicles complete the system, each equipped with a 128-line RoboSense Ruby Plus LiDAR, four stereo cameras, and tightly integrated GNSS and IMU.

Why so many sensors? Because each sensor type has its own failure modes. Cameras fail in direct sunlight and at night. LiDAR degrades in heavy rain. GNSS loses accuracy near tall buildings. Redundancy is not overkill — it is the minimum viable design for a system that needs to be reliable, not just functional under ideal conditions.

---

### [P03S04ATimeCalibration — "Time Calibration"]

Running multiple agents with multiple sensor types introduces an immediate synchronization problem: how do you know that the LiDAR scan from the infrastructure node and the LiDAR scan from the vehicle were captured at the same physical moment?

The math is unforgiving. A vehicle traveling at 60 km/h moves 0.83 meters per second. A 50-millisecond timing offset displaces the reported object position by more than 40 centimeters. In lane-level driving, that is the difference between a correct and an incorrect obstacle classification.

The solution is hardware-level synchronization. GPS provides a shared global time reference visible to all agents simultaneously. Hardware triggers on each sensor ensure that capture happens at a precisely defined moment — not via software scheduling, which has unpredictable latency jitter.

---

### [P03S04BSpaceCalibration — "Space Calibration"]

Every sensor lives in its own coordinate frame. The camera has an intrinsic model that maps 3D world points to 2D image pixels, including lens distortion. The LiDAR has its own origin and orientation. The vehicle has a reference frame. The global map has a reference frame.

Extrinsic calibration establishes the rigid body transforms between all of these: from camera to LiDAR, from vehicle LiDAR to world frame, from infrastructure LiDAR to world frame. If any of these transforms are wrong, point clouds from different sources fuse incorrectly — producing ghost objects that appear to exist but don't, or missing real objects entirely by placing them at wrong positions.

Calibration tools for this system have been released open-source as PJLab SensorsCalibration.

---

### [P03S05DataCollection — "Data Collection"]

Calibration gives you a system that records correctly. The next challenge is ensuring the data you collect is diverse and representative enough for training.

Data collection at the UCLA Smart Intersection follows a structured protocol. Basic routes include consistent left turns, right turns, and straight-through passes, each repeated multiple times to build per-maneuver statistics. Combined routes chain multiple maneuvers, capturing the full range of spatial overlap patterns between infrastructure and vehicle sensors. Data was collected at multiple times of day to cover varying lighting, traffic density, and shadow patterns.

This structured approach produced the V2X-Real dataset (ECCV 2024) and V2XPnP-Seq described in Part 2 — both of which are grounded in this specific hardware deployment.

---

### [P03S06LocalizationRole — "Why Localization Matters"]

Cooperative perception requires that all agents share a common world model. And that means every agent needs to know precisely where it is in the world.

Consider the scenario: an infrastructure node observes an object in its field of view, and a vehicle observes the same object from a different angle. To fuse these two observations, both agents must know their own position and orientation in the same world coordinate frame. If their localization is off, the fused result is a corrupt representation — worse than either individual observation alone.

The degradation is not graceful. With incorrect localization, a fused LiDAR result can be worse than a single-agent result, because you are confidently combining two wrong frames of reference. Precise localization is not optional for cooperative systems — it is load-bearing.

---

### [P03S07KalmanFilter — "Kalman Filter: Three Rivers"]

The solution is a multi-rate error-state Kalman filter that fuses three sensor modalities with very different characteristics.

GNSS provides absolute position — it grounds the vehicle in the global coordinate frame — but operates at only 5 Hz and degrades significantly near tall buildings. The IMU and wheel speed sensors provide high-frequency velocity and attitude updates at 100 Hz, enabling rapid dead-reckoning corrections, but they accumulate drift over time. LiDAR map-matching compares the current point cloud scan against a pre-built HD map to correct pose — highly accurate when the match succeeds, but computationally expensive and running at just 1 Hz.

The Kalman filter integrates all three streams, accounts for measurement delays and the asynchronous nature of the sensor updates, and produces a continuous, smooth pose estimate at 100 Hz. The output is lane-level accuracy — sufficient for precise cooperative fusion — delivered in real time.

---

### [P03S08CooperFuse — "CooperFuse: Late Fusion"]

With calibration and localization in place, the first fusion system can run.

**CooperFuse** is the first real-time cooperative late fusion system for V2X, published at IV 2024. Late fusion means each agent runs detection locally, transmits its detected bounding boxes, and the receiver fuses the results. It is lightweight — no raw sensor data is shared, and no intermediate feature compression is needed.

The challenge in late fusion is deciding which bounding box to keep when two agents detect the same object. Traditional Non-Maximum Suppression simply keeps the box with the highest detection confidence score. But a confidence score only answers "am I sure I detected something?" — it says nothing about the physical properties of the detected box: its position, size, orientation, or velocity history.

CooperFuse instead fuses using the temporal features of each bounding box — position, heading, and size tracked over multiple frames of history. An infrastructure node with a favorable overhead viewing angle may have a less confident detection of a pedestrian than the ego vehicle's forward-facing camera, but its orientation estimate is more accurate because its viewing geometry is better. Temporal feature fusion captures that geometric quality; confidence-based NMS cannot.

---

### [P03S09V2XReaLO — "V2X-ReaLO: Online Intermediate Fusion"]

Late fusion is bandwidth-efficient but discards information. Intermediate fusion keeps richer representations — transmitting compressed BEV feature maps — and achieves higher accuracy, but must solve a harder bandwidth and latency problem.

**V2X-ReaLO** is the first online intermediate fusion system for real-world V2X deployment, submitted to T-PAMI. The core engineering challenge is finding the working point on the accuracy-latency trade-off curve. Larger messages preserve more information but increase transmission time. Smaller messages are faster but lose detail.

The system operates at **0.5 MB per message** — a 32× compression of the uncompressed BEV feature representation. This size fits within practical V2X network bandwidth budgets while retaining sufficient spatial detail for downstream detection. BEV features encode both static environment structure — road geometry, lanes, curbs — and dynamic object features in a single spatial representation, making them an efficient intermediate for multi-agent fusion.

---

### [P03S10OpenCDAROS — "OpenCDA-ROS: Sim-to-Real Bridge"]

Developing and testing these systems requires the ability to run the same code in simulation as on real hardware — otherwise, every algorithm change requires a full hardware deployment cycle.

**OpenCDA-ROS** bridges simulation and reality using the Robot Operating System (ROS) as middleware. ROS is the standard communication framework in robotics; it provides a message-passing architecture that decouples sensor drivers, processing modules, and actuator commands through a shared topic system. OpenCDA-ROS implements the full V2X communication stack, multi-agent time synchronization, and data streaming in ROS, so that code written for the CARLA simulator can run directly on real vehicles with driver-level substitutions but no algorithmic changes.

---

### [P03S11SimBoost — "CDA-SimBoost: Digital Twin"]

**CDA-SimBoost** closes the loop between real-world data and simulation-based training.

The pipeline works as follows: import real-world sensor data via the OpenCDA-ROS bridge; reconstruct the physical environment as a digital twin in CARLA; use the digital twin to generate challenging scenario variants — different weather, different traffic densities, different agent failure modes — that do not appear in the raw real-world data; train and benchmark cooperative perception and planning systems on this augmented data.

Why generate scenarios rather than just replaying real data? Because real data is overwhelmingly nominal. Sensor failures, rare pedestrian behaviors, occluded intersections in heavy rain — these events are statistically rare but disproportionately important for safety. The digital twin is the mechanism for controlled exposure to edge cases at the scale needed for robust training.

---

### [P03S12DigitalTwin — "Digital Twin Details"]

The digital twin is not just a visual replica. It is a physically consistent simulation environment built from real sensor measurements, preserving the spatial geometry, sensor placement, and traffic patterns of the actual intersection.

Agent behavior models are fit from the real trajectory data collected at the UCLA Smart Intersection. The environment supports swapping sensor configurations, adding virtual agents with programmable behaviors, and injecting sensor degradation models. This makes it possible to evaluate how a cooperative perception system responds to partial sensor failure before that failure happens in the real world.

---

### [P03S13InfraX — "OpenCDA-InfraX"]

**OpenCDA-InfraX** is the data generation platform built on top of the digital twin infrastructure. It provides a unified interface for generating multi-modal sensor data across flexible configurations — varying numbers of infrastructure nodes, different sensor loadouts, multiple weather conditions, and full vector map output.

The platform is designed to feed downstream model training directly: structured annotations, calibrated sensor data, and ground-truth labels are produced in a format compatible with standard detection and prediction training pipelines. This reduces the friction between data collection and model development.

---

### [P03S14Summary — "Part 3 Summary"]

This part built the entire infrastructure layer for real-world V2X deployment.

Hardware: a multi-modal, redundant sensor suite at a real urban intersection, with two infrastructure nodes and two connected vehicles. Calibration: hardware-level time synchronization and precise multi-sensor extrinsic alignment. Localization: a multi-rate Kalman filter that fuses GNSS, IMU, and LiDAR map-matching into a continuous 100 Hz lane-level pose stream. Fusion systems: CooperFuse for real-time late fusion via temporal bounding box features; V2X-ReaLO for online intermediate fusion at a practical bandwidth working point. Digital twin: OpenCDA-ROS for simulation-reality bridging, CDA-SimBoost for scenario generation, and OpenCDA-InfraX for structured data generation.

---

### [P03S15BridgeToP4 — "Bridge to Part 4"]

The infrastructure is in place. The fusion algorithms work. The digital twin closes the loop between simulation and reality.

But there are three practical bottlenecks that this part did not resolve. Annotating real-world LiDAR data is extremely expensive in both time and labor — and annotation costs scale with dataset size. Training the complex multi-agent, multi-task framework described in Part 2 is slow and difficult to converge. And running inference on edge hardware inside a vehicle, with constrained compute and power budgets, is a hard real-time requirement that research-grade systems often don't meet.

These three bottlenecks — data, training, and inference efficiency — are exactly what Part 4 addresses.

---
*[End of Part 3 — ~12 min]*
