# Beyond Self-Driving: Exploring Three Levels of Driving Automation | ICCV 2025

## Introduction
Self-driving technologies have demonstrated significant potential to transform human mobility. However, single-agent systems face inherent limitations in perception and decision-making capabilities. Transitioning from self-driving vehicles to cooperative multi-vehicle systems and large-scale intelligent transportation systems is essential to enable safer and more efficient mobility. However, realizing such sophisticated mobility systems introduces significant challenges, requiring comprehensive tools and models, simulation environments, real-world datasets, and deployment frameworks. This tutorial will delve into key areas of driving automation, beginning with advanced end-to-end self-driving techniques such as vision-language-action (VLA) models, interactive prediction and planning, and scenario generation. The tutorial emphasizes V2X communication and cooperative perception in real-world settings, as well as datasets including V2X-Real and V2XPnP. The tutorial also covers simulation and deployment frameworks for urban mobility, such as MetaDrive, MetaUrban, and UrbanSim. By bridging foundational research with real-world deployment, this tutorial offers practical insights into developing future-ready autonomous mobility systems.

## Schedule

### Foundation Models for Autonomous Driving: Past, Present, and Future
**Speaker:** Zhiyu Huang (Postdoctoral Researcher, UCLA)
**Abstract:** Foundation models are transforming autonomous driving by unifying perception, reasoning, and planning within a single multimodal learning framework. This tutorial introduces how recent advances in generative AI, spanning vision, language, and world modeling, enable autonomous systems to generalize beyond closed datasets and handle long-tail real-world scenarios. We begin by revisiting the limitations of modular and hybrid AV pipelines and discuss how foundation models bring unified optimization, contextual reasoning, and improved interpretability. The tutorial surveys state-of-the-art vision-language-action frameworks such as LINGO-2, DriveVLM, EMMA, ORION, and AutoVLA, highlighting how language serves as both an interface for human interaction and a medium for model reasoning and decision-making. We further explore emerging techniques in reinforcement fine-tuning, alignment of actions with linguistic reasoning, and continual learning for safe, efficient post-training.

### Towards End-to-End Cooperative Automation with Multi-agent Spatio-temporal Scene Understanding
**Speaker:** Zewei Zhou (PhD Candidate, UCLA)
**Abstract:** Vehicle-to-Everything (V2X) technologies offer a promising paradigm to mitigate the limitations of constrained observability in single-vehicle systems through information exchange. However, existing cooperative systems are limited in cooperative perception tasks with single-frame multi-agent fusion, leading to a constrained scenario understanding without temporal cues. This tutorial will explore how cooperative systems can achieve a comprehensive spatio-temporal scene understanding and be jointly optimized for the full autonomy stack: perception, prediction, and planning. The tutorial will begin by introducing V2XPnP-Seq, the first real-world sequential dataset supporting all V2X collaboration modes. Attendees will learn how to leverage this dataset and its comprehensive benchmark to validate their own cooperative models. Next, the tutorial will delve into V2XPnP, a novel intermediate fusion end-to-end framework that operates within a single communication step. Compared to traditional multi-step strategies, this framework achieves a 12% gain in perception and prediction accuracy while reducing communication overhead by 5×. Finally, TurboTrain and RiskMap as Middleware (RiskMM) are introduced to address training challenges and interpretable planning.

### Bridging Simulation and Reality in Cooperative V2X Systems
**Speaker:** Zhaoliang Zheng (PhD Candidate, UCLA)
**Abstract:** Bridging the gap between simulation and deployment for cooperative V2X perception demands algorithms and systems that remain robust to bandwidth limits, latency spikes, and localization/synchronization errors. This tutorial surveys an end-to-end sim-to-real pipeline and proposes design patterns that make cooperative perception practical “from sims to streets.” Key components include OpenCDA-ROS, CooperFuse (a real-time late-fusion framework), and V2X-ReaLO (an online framework integrating early, late, and intermediate fusion).

### From Pre-Training to Post-Training: Building an Efficient V2X Cooperative Perception System
**Speaker:** Seth Z. Zhao (PhD Candidate, UCLA)
**Abstract:** Recent advances in cooperative perception have demonstrated significant performance gains, but real-world deployment remains challenging due to high data requirements and strict real-time constraints. This tutorial provides a full-stack perspective on designing efficient V2X systems. Key strategies include data-efficient pretraining (CooPre), training-efficient methods (TurboTrain), and inference-efficient deployment techniques (QuantV2X, a fully quantized cooperative perception system).

### Building Scalable, Human-Centric Physical AI Systems
**Speaker:** Wayne Wu (Research Associate, UCLA)
**Abstract:** Large language models and generative models have made remarkable progress by scaling with internet-scale data. In contrast, physical AI still lags behind. This tutorial discusses how to build scalable, human-centric physical AI systems by rethinking both the usage of data and the modeling of humans. The three-pronged recipe includes: 1) Simulation (MetaDrive, MetaUrban, UrbanSim); 2) Human-created videos; and 3) Human modeling (PedGen, CityWalker).

## Resources
- [AutoVLA](https://github.com/ucla-mobility/AutoVLA)
- [Awesome-VLA-for-AD](https://github.com/worldbench/awesome-vla-for-ad)
- [OpenCDA](https://github.com/ucla-mobility/OpenCDA)
- [V2X-Real](https://mobility-lab.seas.ucla.edu/v2x-real/)
- [V2XPnP](https://mobility-lab.seas.ucla.edu/v2xpnp/)
- [QuantV2X](https://github.com/ucla-mobility/QuantV2X)
- [TurboTrain](https://github.com/ucla-mobility/TurboTrain)
- [MetaDrive](https://github.com/metadriverse/metadrive)
- [MetaUrban](https://github.com/metadriverse/metaurban)
- [UrbanSim](https://github.com/metadriverse/urban-sim)
