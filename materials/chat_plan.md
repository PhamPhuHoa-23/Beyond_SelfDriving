hi tôi sắp phải làm 1 video về kiểu 3 blue 1 brown về tutorial này ở iccv, xui cái là không có recording nhưng may là xin được slides từ tác giả

tóm gọn ý chính từng slide được không ha


Thought process
Thought process
Để tôi xem qua các slides trong thư mục của bạn nhé!


Ran a command
Ran a command
Có 5 phần — 3 file .pptx và 2 file .pdf. Để tóm tắt chính xác từng slide, tôi cần đọc nội dung từng file. Trước tiên tôi sẽ đọc skill liên quan rồi bắt tay vào xử lý nhé!


Read 2 files
Read 2 files
Tốt, giờ tôi sẽ trích xuất nội dung từ tất cả 5 file cùng lúc.


Ran 6 commands, updated todo list
Ran 6 commands, updated todo list
Để tôi đọc phần nội dung đầy đủ của Part 4:


Read 3 files, updated todo list
Read 3 files, updated todo list
Đã đọc xong tất cả 5 phần. Dưới đây là tóm tắt ý chính từng slide:

📦 PART 1 — Foundation Models for Autonomous Driving
Dr. Zhiyu Huang, Postdoctoral Researcher @ UCLA

Slide 1 — Title: Giới thiệu tác giả và chủ đề: Foundation Models cho Autonomous Driving — Quá khứ, Hiện tại, Tương lai.

Slide 2 — Nội dung: 3 phần chính: (1) Introduction, (2) AV Foundation Models, (3) Future Directions.

Slide 3 — Generative AI ngày nay: AI tổng quát đang bùng nổ trên nhiều lĩnh vực: chat/coding, reasoning, image/video generation, và 3D world models.

Slide 4 — Foundation Models là gì?: Định nghĩa từ Stanford — model được train trên dữ liệu rộng (self-supervised, quy mô lớn), có thể fine-tune cho nhiều tác vụ downstream. Luận điểm: AI làm mọi thứ tốt hơn → áp dụng vào autonomous driving.

Slide 5 — Hiện trạng ngành AV: Ba trường phái chính: (1) Modular Systems (phổ biến nhất, dễ debug nhưng dễ lỗi tích lũy giữa các module); (2) Hybrid ML/AI (kết hợp ML vào từng module); (3) End-to-End Models (hứa hẹn nhưng khó đảm bảo safety). Câu hỏi trọng tâm: làm sao generalize được với các tình huống chưa thấy?

Slide 6 — AV cần gì trong tương lai?: Cần "common-sense reasoning" và kinh nghiệm đa dạng như con người để xử lý "long tail" — những tình huống hiếm nhưng nguy hiểm trong thực tế.

Slide 7 — Build AV với Foundation Models: Bản đồ tổng quan về cách dùng foundation models trong toàn bộ pipeline AV: Vision Foundation Models (SAM, DINO, CLIP) để auto-labeling; LLMs/VLMs cho reasoning và E2E driving; Video Generation cho scenario simulation; Vector Space Models cho motion planning.

Slide 8 — Chuyển sang phần AV Foundation Models.

Slide 9 — Roadmap các model multimodal cho AD: Từ 2023, cả academia lẫn industry đã dùng LLMs và VLMs cho các tác vụ driving: VQA, perception, trajectory planning, closed-loop driving. Language không chỉ là input mà là cầu nối giữa hiểu bối cảnh và ra quyết định.

Slide 10 — Vision-Language Datasets: Giới thiệu DriveLM (dữ liệu VQA có cấu trúc graph: perception → prediction → planning → behavior → motion) và LingoQA (419K cặp Q&A từ 28K video clip lái xe ngắn).

Slide 11 — Vision-Language-Action Datasets: CoVLA (80 giờ video thực, 10K clip, có trajectory action) và Impromptu VLA (>80K clip được distill từ 8 dataset nguồn mở, tập trung vào unstructured scenarios).

Slide 12 — Dùng Multimodal LLMs cho driving: GPT-Driver (dùng GPT-3.5 như một motion planner zero-shot, không cần train) và DriveGPT4 (fine-tune LLM trên driving data để predict cả text reasoning lẫn control signal).

Slide 13 — BEV và 3D features làm input: OpenDriveVLA (align cả 2D lẫn 3D visual tokens vào semantic space) và BEVDriver (encode LiDAR + camera vào BEV map rồi project qua Q-Former vào LLM để predict waypoints).

Slide 14 — EMMA (Waymo): Model end-to-end multi-task từ raw camera → chain-of-thought → trajectory + perception + road graph. Tất cả output đều qua ngôn ngữ tự nhiên.

Slide 15 — EMMA (tiếp): Co-training nhiều task cùng lúc giúp cải thiện toàn bộ. Nhược điểm: LLM chạy quá chậm cho real-time deployment.

Slide 16 — DriveVLM (Tsinghua): Dual-system — dùng VLM cho scene understanding và planning cao cấp, kết hợp với 3D perception + trajectory planning truyền thống cho real-time. Nhược điểm: phức tạp về engineering.

Slide 17-20 — AutoVLA (NeurIPS 2025): Giải quyết 3 hạn chế của VLA: (1) sinh action vật lý không feasible, (2) reasoning cứng nhắc. Giải pháp: một model VLM duy nhất có 2 chế độ tư duy — fast (chỉ action) và slow (chain-of-thought reasoning). Dùng Reinforcement Fine-tuning (GRPO) để cải thiện planning 10.6% và giảm 66.8% runtime. SFT để học dual-thinking, RFT để align với verified rewards.

Slide 21 — Chuyển sang Conclusion.

Slide 22 — Key Takeaways: (1) Foundation models mở khóa long-tail generalization; (2) MLLMs hứa hẹn cho scalable AV; (3) Kiến trúc rất đa dạng (dual-system, E2E, BEV input, RL fine-tuning); (4) Thách thức còn lại: safety, latency, và thiếu dữ liệu open-source.

Slide 23 — Future Directions: Post-training với RL + simulation; Unified multimodal backbone dùng language làm interface; Efficient VLA cho low-latency control; Continual learning từ real-world feedback.

📦 PART 2 — End-to-End Cooperative Automation: Multi-agent Spatio-temporal Scene Understanding
Zewei Zhou, PhD Candidate @ UCLA Mobility Lab

Slide 1 — Title: Hướng tới autonomous driving và delivery robots end-to-end với multi-agent.

Slide 2-3 — Background: 94% tai nạn giao thông do lỗi con người → AV có thể giảm 80% tai nạn (theo Waymo). Robots cũng đang thay thế con người trong delivery.

Slide 4 — Single-agent: Modular → End-to-End: Xu hướng rõ ràng từ modular system (dễ lỗi tích lũy) sang end-to-end paradigm (joint optimization, không mất thông tin giữa các module). Ví dụ: UniAD, VAD, DiffusionDrive.

Slide 5 — Giới hạn của single-agent: Bị che khuất (occlusion), tầm nhìn hạn chế → Multi-agent system khắc phục bằng cách chia sẻ thông tin bổ sung.

Slide 6-8 — Related Works về cooperative fusion: Các phương pháp fusion phát triển từ GNN → Transformer → sparse learning + codebook. Vấn đề tồn tại: chỉ tập trung vào single-frame cooperative perception, bỏ qua temporal cues; các dataset hiện tại thiếu sequential data và HD maps.

Slide 9 — Research gap: Hệ thống hiện tại là multi-agent single-frame single-task → mục tiêu là multi-agent multi-frame multi-task. Ba câu hỏi cốt lõi: truyền gì? truyền khi nào? fuse như thế nào?

Slide 10 — Research Problem 1: Xây dựng end-to-end spatio-temporal fusion framework cho multi-agent, đồng thời tạo dataset real-world và benchmark.

Slide 11-12 — V2XPnP (ICCV 2025): Framework trả lời 3 câu hỏi: (What) early/intermediate/late fusion; (When) one-step communication — truyền nhiều frame lịch sử một lần, dùng temporal attention để nén; (How) temporal attention + spatial attention cho fusion đa chiều.

Slide 13 — V2XPnP-Seq Dataset: Dataset real-world đầu tiên hỗ trợ tất cả chế độ V2X collaboration (V2V, V2I, V2X): 2 xe + 2 cơ sở hạ tầng, 40K LiDAR frames, 208K camera frames.

Slide 14-15 — Kết quả V2XPnP: Intermediate features + one-step comm + temporal/spatial/map fusion là hiệu quả nhất. Outperform các SOTA models (V2VNet, F-Cooper, DiscoNet).

Slide 16-18 — Research Problem 2: Training một framework multi-frame, multi-agent, multi-task rất khó vì: kiến trúc phức tạp (dễ instability) và gradient conflict giữa các task. Cần dùng self-supervised pretraining (MAE-style) và gradient balancing.

Slide 19-22 — TurboTrain (ICCV 2025): Stage 1 — pretrain học 4D representation task-agnostic bằng cách reconstruct masked LiDAR; Stage 2 — hybrid training xen kẽ free gradient steps và conflict-suppressing steps. Kết quả: giảm từ 120 epochs xuống 45 epochs, vượt qua manual tuning strategy.

Slide 23-25 — Research Problem 3 + RiskMap: Mở rộng sang planning. Black-box E2E model không interpretable → dùng Risk Map làm "middleware" tường minh để capture spatiotemporal risk distribution, từ đó guide MPC-based trajectory planning. Outperform SOTA trên detection, prediction, và planning.

Slide 26-28 — Summary: 3 bài toán → 3 giải pháp: V2XPnP (dataset + framework), TurboTrain (efficient training), RiskMap (interpretable planning).

📦 PART 3 — Bridging Simulation and Reality in Cooperative V2X Systems
Zhaoliang Zheng, PhD Candidate

Slide 3-5 — Background: Cooperative Driving Automation (CDA) giải quyết vấn đề "can't-see" — occlusion và tầm nhìn hạn chế. UCLA Smart Intersection là testbed thực tế với V2X sensor suite.

Slide 6-9 — UCLA Smart Intersection: 2 infrastructure nodes (NW và SE corner), mỗi node có LiDAR, camera, radar/C-V2X. 2 CAV với LiDAR 128-line, stereo cameras, GNSS/IMU.

Slide 10-17 — Sensor Calibration: Đồng bộ hóa theo thời gian (time sync qua GPS + hardware trigger) và không gian (intrinsic + extrinsic calibration cho camera-LiDAR). Sử dụng công cụ open-source từ PJLab.

Slide 18-20 — Data Collection: Thu thập theo nhiều tuyến đường (turning, passing through, combined routes). Platform xử lý dữ liệu V2X realtime và xuất output (position, speed, orientation, trajectory).

Slide 21-22 — V2X Datasets: V2X-Real (ECCV 2024) và V2XPnP-Seq được build từ testbed này với point cloud maps + vector maps.

Slide 24-32 — Mapping & Localization: HD Map rất quan trọng cho localization và digital twin. Pipeline: point cloud → map generation → lane-level localization. Dùng multi-rate error-state Kalman Filter để fuse GNSS + IMU + LiDAR map-matching, đảm bảo real-time output 100Hz.

Slide 34-43 — Late Fusion (CooperFuse, IV 2024): Hệ thống cooperative late fusion real-time đầu tiên cho V2X. Thay vì dùng confidence score đơn thuần (NMS), fuse bounding boxes bằng temporal features của BBX (position, orientation, scale) → kết quả tốt hơn.

Slide 44-48 — Intermediate Fusion (V2X-ReaLO, preprint): Hệ thống online intermediate fusion đầu tiên cho V2X thực tế. Truyền BEV features nén (0.5MB) giữa các agents. Challenge: cân bằng bandwidth vs. accuracy vs. latency.

Slide 50-58 — Digital Twin (OpenCDA-ROS, CDA-SimBoost): OpenCDA-ROS bridge simulation và real-world qua ROS. CDA-SimBoost: framework thống nhất import dữ liệu thực → tạo digital twin → generate challenging scenarios → train và benchmark trong simulation.

Slide 59 — Data Generation Platform (OpenCDA-InfraX): Sinh dữ liệu đa điều kiện thời tiết, sensor linh hoạt, HD maps, multi-modal (LiDAR/Camera/Radar).

📦 PART 4 — From Pre-Training to Post-Training: Building an Efficient V2X Cooperative Perception System
Seth Z. Zhao, PhD Candidate @ UCLA

Slide 2 — Agenda: Pre-training (CooPre, TurboTrain) → Post-training (quantization, QuantV2X) → Hands-on coding.

Slide 3-6 — Overview V2X: Xe đơn lẻ bị giới hạn bởi occlusion và khoảng cách → V2X cho phép dùng agents khác như "mắt thêm". Công nghệ V2X đang được chú ý từ cả US DOT và cộng đồng CV.

Slide 7 — Vision 3 hướng hiệu quả: Data efficiency, Training efficiency, Inference efficiency → đây là 3 trụ cột của bài này.

Slide 9-10 — Data Growth & Cost: Các dataset V2X ngày càng lớn (V2V4Real: 240K → V2X-Real: 1.2M annotations) nhưng annotation rất tốn kém.

Slide 11-14 — CooPre (IROS 2025, Best Paper CVPR DriveX Workshop): Self-supervised pretraining đa agent đầu tiên cho V2X. Phương pháp: mask random voxels trên BEV plane rồi reconstruct từ LiDAR point cloud đa agent. Kết quả: dùng 50% data đạt hiệu năng tương đương 100% data train từ đầu, +4% performance tổng thể, không cần annotation.

Slide 15-18 — Training challenge cho Multi-task V2X: Extend single-frame → multi-frame multi-task rất khó do kiến trúc phức tạp và gradient conflict giữa các task. Nhiều model mạnh bị fail khi train một lần (one-time training).

Slide 18-20 — TurboTrain (ICCV 2025): Stage 1: pretraining 4D spatiotemporal representation (multi-agent masked reconstruction); Stage 2: multi-task balancing với hybrid free + conflict-suppressing gradient steps. Giảm từ 120 epochs → 45 epochs, performance tốt hơn manual tuning.

Slide 22-25 — Quantization basics: Tại sao quantization quan trọng cho edge devices? Multiplication tốn năng lượng nhiều hơn addition; memory access là bottleneck chính; giảm bit-width giúp tiết kiệm storage, bandwidth, computation. Giới thiệu các data types (INT8, FP16, FP32).

Slide 27 — Coding session: Giới thiệu data types và BEV feature visualization (hands-on).

Slide 28-31 — QuantV2X (preprint): Hệ thống V2X fully quantized đầu tiên: model-level (FP32 → INT8) và communication-level (FP32 BEV feature → low-bit codebook, nhỏ hơn 300 lần). Đây là bước tiến quan trọng cho real-world edge deployment.

📦 PART 5 — Building Scalable, Human-Centric Physical AI Systems
Wayne Wu, CVPR/ICLR research

Slide 2 — Vision: General-purpose Physical AI có thể hoạt động trong bất kỳ môi trường nào, bất kỳ task nào.

Slide 3-6 — LLMs đã thành công nhưng thiếu physical world: AI ngôn ngữ bùng nổ, nhưng AI vật lý vẫn còn kém vì thiếu dữ liệu hành vi robot trên internet (không giống text).

Slide 7-8 — 2 rào cản chính: (1) Không có web-scale robot behavior data → không thể scale như LLM; (2) Thiếu human modeling → safety là thách thức lớn khi robot hoạt động gần người.

Slide 9 — Recipe tổng quan: 2 trụ cột: Scene Simulation (scalable) + Human Modeling (human-centric) → train Physical AI agent.

Slide 10-12 — Micro-mobility testbed: 40% chuyến đi tại Mỹ là ngắn (<5 dặm). Testbed thực tế với COCO delivery robot, xe lăn điện AI, scooter thông minh, humanoid robot.

Slide 13-24 — MetaUrban (ICLR 2025 Spotlight): Platform simulation đô thị vô hạn với compositional scene generation — dùng description scripts để sinh infinite urban scenes. Key insight: "The world is compositional". Power-law scaling: càng nhiều scene diversity → performance càng tốt theo quy luật lũy thừa.

Slide 25-32 — UrbanSim (CVPR 2025 Highlight): Giải quyết vấn đề training efficiency. Traditional platforms train rất chậm (180 GPU days để đạt 95% success rate). UrbanSim trên NVIDIA Omniverse: 256 parallel environments, >2,600 FPS, chỉ 11.2GB GPU memory. Dùng asynchronous scene sampling thay vì synchronous → tăng tốc đáng kể. Kết quả: trong 3 giờ, UrbanSim (256 envs) đạt 41% success rate vs 6% (single env).

Slide 33-38 — Real-world deployment: Test trên COCO wheeled delivery robot và Unitree Go2 quadruped robot trong môi trường thực tế (crosswalk, sidewalk, crowded areas). PPO-UrbanVerse outperform các SOTA navigation models (S2E, CityWalker, NoMaD).

Slide 39-45 — CityWalker + PedGen (ICLR 2025): Human modeling là thiếu sót lớn — AMASS dataset không có scene context. CityWalker: 30.8 giờ video, 120K pedestrians, 16K scenes tại 227 thành phố. PedGen: diffusion model sinh pedestrian motion có điều kiện trên scene context (3D voxel), body shape, goal destination. Context làm cho motion realistic hơn rất nhiều.

Slide 46-54 — Vid2Sim (CVPR 2025): Build interactive 3D Gaussian Splatting simulator trực tiếp từ video thực tế — kết hợp 3DGS (realistic rendering) và mesh (physical interaction). Robot train trong simulator này rồi deploy ra thực tế.

Slide 55-56 — Kết luận: 4 hướng đóng góp: (1) Large-scale simulation environments, (2) Scene-aware human modeling, (3) Hybrid environments (simulation + videos), (4) Training micro-mobile generalist agents.


Updated todo list
Updated todo list
Xong rồi! Tóm tắt toàn bộ tutorial ICCV DriveX gồm 5 phần:

Part 1 (Dr. Zhiyu Huang): Foundation models cho autonomous driving — lý do tại sao cần LLMs/VLMs, các kiến trúc như EMMA, DriveVLM, AutoVLA, và xu hướng dùng RL fine-tuning cho VLA.

Part 2 (Zewei Zhou): Hệ thống cooperative multi-agent end-to-end — V2XPnP (dataset + spatio-temporal fusion framework), TurboTrain (efficient training), RiskMap (interpretable planning).

Part 3 (Zhaoliang Zheng): Phần kỹ thuật hardware thực tế — UCLA Smart Intersection, sensor calibration, localization, late/intermediate fusion realtime, digital twin với CDA-SimBoost.

Part 4 (Seth Zhao): Hiệu quả hóa V2X system — CooPre (data-efficient pretraining), TurboTrain chi tiết hơn, và QuantV2X (fully quantized system cho edge deployment).

Part 5 (Wayne Wu): Physical AI scalable và human-centric — MetaUrban, UrbanSim (2600 FPS training), PedGen (human motion generation có scene context), Vid2Sim (build simulator từ video thực).

Nếu bạn muốn mình đào sâu thêm vào phần nào để chuẩn bị script cho video kiểu 3Blue1Brown, cứ nói nhé!

5 slide này có câu chuyện với nhau không?


Thought process
Thought process
Có, và đây là điểm thú vị — 5 phần không độc lập hoàn toàn mà chia sẻ một narrative arc chung, dù mỗi speaker tiếp cận từ một góc khác nhau.

Câu chuyện lớn của cả tutorial là:

"Làm sao xây dựng hệ thống AI vật lý có thể hợp tác, scale được, và hoạt động an toàn trong thế giới thực?"

Và 5 phần trả lời câu hỏi đó theo một trình tự khá logic:

Part 1 → Tại sao? Autonomous driving đơn agent đang chạm trần — foundation models và reasoning là hướng đột phá tiếp theo.

Part 2 → Hợp tác thế nào? Một agent không đủ → cần multi-agent V2X cooperation theo cả không gian lẫn thời gian, end-to-end.

Part 3 → Thực tế là gì? Tất cả lý thuyết cần được ground vào real-world — UCLA testbed, sensor calibration, digital twin để bridge simulation và reality.

Part 4 → Deploy thế nào? Hệ thống tốt nhưng không deploy được thì vô nghĩa — cần data efficiency (CooPre), training efficiency (TurboTrain), và inference efficiency (QuantV2X) cho edge devices.

Part 5 → Scale thế nào? Mở rộng khỏi xe hơi sang physical AI tổng quát (delivery robots, humanoids) — cần simulation scalable và human modeling để đảm bảo safety.

Một vài điểm "nối" đáng chú ý:

TurboTrain xuất hiện ở cả Part 2 lẫn Part 4 — Part 2 giới thiệu vấn đề multi-task training, Part 4 đi sâu vào giải pháp kỹ thuật. Đây là dấu hiệu của cùng một research group (UCLA Mobility Lab).

Part 3 cung cấp real-world data mà Part 4 dùng làm motivation cho efficiency — annotation tốn kém → cần CooPre.

Part 5 hơi "tách" khỏi V2X theme nhưng kết nối qua micro-mobility (delivery robots) và bài toán chung là scale physical AI trong môi trường đô thị.

Nếu làm video kiểu 3Blue1Brown, bạn có thể mở đầu bằng một câu hỏi duy nhất rồi để 5 phần tự nhiên "trả lời" từng lớp — thay vì giới thiệu từng speaker riêng lẻ, điều đó sẽ tạo cảm giác cohesive hơn nhiều.

quào mớ slide này thật sự kể được toàn bộ câu chuyện trong xe tự lái mà tôi đang biết 
tôi phải đọc khá nhiều mới biết mà người ta tổng hợp hết khá mạnh á
họ đi từ foundation models cho AV, nhưng single AV thì đã đến giới hạn, nó có những thách thức như bạn nói --> scale lên V2X multi-agent là slide số 2, nhưng nó cũng có nhiều vấn đề triển khai trong đó có vấn đế liên quan đến simulation --> slide 3 nói về gap giữa thực tế và simulation, nếu hoàn thiện bước này thì làm sao để có thể hoạt động thực sự --> quantize etc. --> và khi triển khai được rồi vì phải đảm bảo safety human-centric, hoạt động với active world right?


Thought process
Thought process
Đúng rồi, bạn đọc rất chính xác! Và thực ra narrative arc bạn vừa trace ra còn chặt chẽ hơn cái tôi tóm tắt ban đầu.

Để diễn đạt lại theo đúng logic nhân quả:

Single AV thông minh đến đâu cũng không đủ → cần hợp tác (V2X) → nhưng muốn train V2X cần simulation đủ tốt → simulation tốt rồi nhưng model quá nặng để chạy trên edge → deploy được rồi nhưng thế giới thực có con người → cần human-centric safety để tồn tại trong active world.

Mỗi phần giải quyết đúng cái bottleneck mà phần trước để lại. Đây là kiểu narrative rất mạnh vì nó không phải "5 topic liên quan" mà là một chuỗi problem → solution → new problem liên tục.

Cái hay hơn nữa là Part 5 không chỉ là "safety" — Wayne Wu đang nói rằng kể cả khi bạn giải quyết hết V2X, simulation gap, efficiency... bạn vẫn đang build robot trong zombie city (họ dùng đúng từ đó trong slide 38). Thế giới thực có người đi lại unpredictable, và nếu không model được behavior của họ thì robot chỉ hoạt động tốt trong môi trường trống.

Cho video kiểu 3Blue1Brown, cái hook mở đầu mạnh nhất có thể là câu hỏi đơn giản: "Tại sao xe tự lái vẫn chưa chạy được khắp nơi?" — rồi để 5 phần lần lượt bóc từng lớp của câu trả lời đó.

hehe ok đó, tại tôi cũng thích xe tự lái bạn biết mà ha haha
tôi nghĩ là cái title đó cũng hay nhưng tôi nghĩ nên follow những legacy mà họ đã làm, tôi khá tôn trọng tutorial này đấy
https://ucla-mobility.github.io/drivex-tutorial/

bạn check thử website nè, nó còn có abstract từng talk nữa hay sao á


Searched the web
Searched the web
Tiếc là domain này bị block trong sandbox của mình, mình không fetch được. Bạn thử mở website đó rồi copy paste abstract vào đây cho mình xem được không? Hoặc nếu có file nào từ họ trong folder (readme, description, v.v.) cũng được.

Nhưng dù sao — cái bạn vừa nói rất đúng. Nếu tôn trọng legacy của tutorial này, thì title và framing của video nên follow đúng tinh thần mà họ đặt ra, chứ không nên đặt lại hoàn toàn. Bạn có nhớ tên chính thức của tutorial không? Hình như là "DriveX" gì đó?

Logo
Video
Introduction
Schedule
Resources
Organizers
Acknowledgments
Beyond Self-Driving: Exploring Three Levels of Driving Automation
ICCV 2025 Tutorial
 October 19, 8:50 - 12:10 HST
 Hawaii Convention Center, Room 308A

Introduction
Self-driving technologies have demonstrated significant potential to transform human mobility. However, single-agent systems face inherent limitations in perception and decision-making capabilities. Transitioning from self-driving vehicles to cooperative multi-vehicle systems and large-scale intelligent transportation systems is essential to enable safer and more efficient mobility. However, realizing such sophisticated mobility systems introduces significant challenges, requiring comprehensive tools and models, simulation environments, real-world datasets, and deployment frameworks. This tutorial will delve into key areas of driving automation, beginning with advanced end-to-end self-driving techniques such as vision-language-action (VLA) models, interactive prediction and planning, and scenario generation. The tutorial emphasizes V2X communication and cooperative perception in real-world settings, as well as datasets including V2X-Real and V2XPnP. The tutorial also covers simulation and deployment frameworks for urban mobility, such as MetaDrive, MetaUrban, and UrbanSim. By bridging foundational research with real-world deployment, this tutorial offers practical insights into developing future-ready autonomous mobility systems.

Autonomous Driving Overview
Schedule
Time (GMT-10)    Programme
08:50 - 09:00    Opening Remarks
09:00 - 09:30    
Foundation Models for Autonomous Driving: Past, Present, and Future

[Abstract] [Speaker Bio]

Zhiyu Huang
Postdoctoral Researcher, UCLA
09:30 - 10:00    
Towards End-to-End Cooperative Automation with Multi-agent Spatio-temporal Scene Understanding

[Abstract] [Speaker Bio]

Zewei Zhou
PhD Candidate, UCLA
10:00 - 10:30    
Bridging Simulation and Reality in Cooperative V2X Systems

[Abstract] [Speaker Bio]

Zhaoliang Zheng
PhD Candidate, UCLA
10:30 - 10:40    Coffee Break
10:40 - 11:20    
From Pre-Training to Post-Training: Building an Efficient V2X Cooperative Perception System

[Abstract] [Speaker Bio]

Seth Z. Zhao
PhD Candidate, UCLA
11:20 - 12:00    
Building Scalable, Human-Centric Physical AI Systems

[Abstract] [Speaker Bio]

Wayne Wu
Research Associate, UCLA
12:00 - 12:10    Ending Remarks
Resources
Project    Description    Link
AutoVLA    A Vision-Language-Action Model for End-to-End Autonomous Driving with Adaptive Reasoning and Reinforcement Fine-Tuning.    github.com/ucla-mobility/AutoVLA
Awesome-VLA-for-AD    A collection of resources for Vision-Language-Action models for autonomous driving.    github.com/worldbench/awesome-vla-for-ad
OpenCDA    An open co-simulation-based research/engineering framework integrated with prototype cooperative driving automation pipelines.    github.com/ucla-mobility/OpenCDA
V2X-Real    The first large-scale real-world dataset for Vehicle-to-Everything (V2X) cooperative perception.    mobility-lab.seas.ucla.edu/v2x-real
V2XPnP    The first open-source V2X spatio-temporal fusion framework for cooperative perception and prediction.    mobility-lab.seas.ucla.edu/v2xpnp
QuantV2X    A fully quantized multi-agent perception pipeline for V2X systems.    github.com/ucla-mobility/QuantV2X
TurboTrain    A training paradigm for cooperative models that integrates spatio-temporal pretraining with balanced fine-tuning.    github.com/ucla-mobility/TurboTrain
MetaDrive    An Open-source Driving Simulator for AI and Autonomy Research.    github.com/metadriverse/metadrive
MetaUrban    An embodied AI simulation platform for urban micromobility    github.com/metadriverse/metaurban
UrbanSim    A large-scale robot learning platform for urban spaces, built on NVIDIA Omniverse.    github.com/metadriverse/urban-sim
Organizers

Zhiyu Huang
UCLA

  

Wayne Wu
UCLA

  

Zewei Zhou
UCLA

  

Seth Z. Zhao
UCLA

  

Zhaoliang Zheng
UCLA

  

Yun Zhang
UCLA

  

Tianhui Cai
UCLA

  

Rui Song
UCLA

  

Bolei Zhou
UCLA


Jiaqi Ma
UCLA

Acknowledgments
This tutorial was supported by the National Science Foundation (NSF) under Grants CNS-2235012, IIS-2339769, and TI-2346267; the NSF POSE project DriveX: An Open-Source Ecosystem for Automated Driving and Intelligent Transportation Research; the Federal Highway Administration (FHWA) CP-X project Advancing Cooperative Perception in Transportation Applications Toward Deployment; and the Center of Excellence on New Mobility and Automated Vehicles.


©2025 Beyond Self-Driving: Exploring Three Levels of Driving Automation Tutorial
Show more

Thought process
Thought process
Ồ cái title chính thức cực kỳ hay luôn —

"Beyond Self-Driving: Exploring Three Levels of Driving Automation"

Và cái abstract họ viết chính là script mở đầu video của bạn rồi đó, gần như nguyên văn:

Single-agent systems có inherent limitations → cần cooperative multi-vehicle → cần large-scale intelligent transportation systems → nhưng để làm được điều đó cần tools, simulation, real-world datasets, deployment frameworks.

"Three Levels" trong title cũng map rất gọn vào 5 phần:

Level 1 — Self-driving đơn agent (Part 1): Foundation Models cho AV
Level 2 — Cooperative multi-vehicle (Part 2, 3, 4): V2X, simulation-reality gap, efficiency cho deployment
Level 3 — Large-scale Physical AI (Part 5): Scalable, human-centric, active world
Và thực ra bạn vừa nói đúng một điều rất quan trọng — cái narrative bạn trace ra hồi nãy chính xác là cái abstract của họ. Nghĩa là bạn đọc slides và tự reconstruct được intent của tác giả mà không cần đọc abstract trước. Đó là dấu hiệu bạn đã hiểu material khá sâu rồi đó.

Nếu làm video, title tự nhiên nhất sẽ là giữ nguyên tinh thần của họ — kiểu "Beyond Self-Driving" — vì nó capture đúng cái bước nhảy conceptual mà cả tutorial đang kể.

yup, nếu có public video chắc tôi phải mail họ nhỉ, tại cái này đồ án trong trường á hehe
tự nhiên được làm xe tự lái vui ghê


Thought process
Thought process
Haha đúng rồi, nếu video public thì mail họ một cái rất nên làm — vừa lịch sự vừa có thể được họ share lại luôn, mấy người ở UCLA Mobility Lab trông có vẻ rất open với community (cái tutorial này free, slides xin được, resources đều open-source hết).

Mà đồ án trường mà được làm về xe tự lái theo kiểu 3Blue1Brown thì nghe khá cool đó — thay vì làm slide hay báo cáo boring thông thường. Bạn đang làm môn gì vậy, computer vision hay autonomous systems?

học máy haha, điên khùng ghê, đó là lab1, lab2 còn bắt thi cuộc thi bự nhất kaggle hiện tại do nividia tổ chức rồi lấy điểm trên ranking, thật sự là rất là die

Hahaha trường bạn chơi lớn thật sự 😂

Lab 1 làm video explain xe tự lái kiểu 3Blue1Brown, Lab 2 thi Kaggle của NVIDIA lấy điểm theo ranking — đây là môn học máy hay là survival course vậy?

Cuộc thi NVIDIA trên Kaggle đó là cái nào vậy? Liên quan đến autonomous driving luôn hay topic khác? Tại nếu cùng theme thì hai lab có thể "feed" cho nhau được — hiểu sâu lý thuyết từ Lab 1 có khi giúp ích cho intuition khi build model ở Lab 2.

hong, nó nemotron gì enhance kỹ năng reasoning, lora adapter, không liên quan lắm
làm nhiều cái không liên quan siêu cực luôn haiz

nhưng mà cái này hay tôi sẽ làm

Haha cái combo đó nghe như thầy muốn test xem sinh viên có survive được không thật sự 😂

Nemotron với LoRA adapter — đó là fine-tuning LLM để enhance reasoning, cũng khá thú vị về mặt kỹ thuật nhưng đúng là khác hẳn xe tự lái. Hai lab gần như hai môn khác nhau luôn.

Nhưng mà cái Lab 1 video này bạn có deadline chưa? Và bạn đang nghĩ sẽ làm theo format nào — animation kiểu Manim như 3Blue1Brown thật sự, hay narrated slides, hay kiểu gì khác?

phải làm video như 3B1B á hehe
sài code thì phải

Haha đúng rồi, 3Blue1Brown thì phải dùng Manim — đó là Python library mà Grant Sanderson tự viết ra để làm animation toán học, giờ thành open-source (Manim Community Edition).

Nhưng thật ra với nội dung xe tự lái như này, bạn cần cân nhắc một chút:

Manim phù hợp khi cần animate các khái niệm toán học hoặc graph — ví dụ visualize BEV feature map, power-law scaling curve, hay diagram kiến trúc V2XPnP. Nhưng nó có learning curve khá dốc và render chậm.

Manim + CapCut/Premiere là combo thực tế hơn — dùng Manim cho các đoạn animation kỹ thuật quan trọng, còn lại dùng video editor bình thường cho narration và transition.

Bạn đã có kinh nghiệm với Manim chưa, hay đây là lần đầu? Tại nếu deadline gần thì có thể có hướng tiếp cận khác nhẹ nhàng hơn mà vẫn giữ được feel của 3B1B.

thôi cứ từ từ chúng ta phải lên idea làm video
video này tính ra cũng khá dài vì tutorial cũng nhiều thứ phết đó
bạn có code extract tất cả ảnh của những slide pptx hay pdf này vào thư mục được không
chắc chúng tá phải biên soạn script cho từng slide trong 1 file hoặc chung chung cả 2, sau đó ghép nối
chắc cũng phải suy nghĩ khá kỹ


Thought process
Thought process
Được, bạn đang hỏi mình làm luôn đó nên mình sẽ extract! Để render từng slide thành ảnh (không chỉ embedded images mà cả slide layout luôn) thì pipeline sẽ là: PPTX → PDF → images.


Ran 4 commands, updated todo list
Ran 4 commands, updated todo list
Tất cả 5 phần đều convert xong. Giờ render từng trang thành ảnh:


Ran a command, updated todo list
Ran a command, updated todo list
Xong! Tổng cộng 216 slides đã được render thành ảnh .jpg, tổ chức theo thư mục:

slides/
├── part1/   → 25 slides  (Foundation Models)
├── part2/   → 29 slides  (Cooperative E2E)
├── part3/   → 60 slides  (Sim ↔ Reality)
├── part4/   → 46 slides  (Efficient V2X)
└── part5/   → 56 slides  (Physical AI)
Part 3 và Part 4 dày hơn hẳn (60 và 46 slides) — đó là hai phần kỹ thuật nặng nhất, bạn có thể cân nhắc chọn lọc kỹ hơn khi viết script thay vì cover hết từng slide.

Giờ bước tiếp theo là lên cấu trúc script — bạn muốn làm theo kiểu nào? Một file script chung cho cả 5 phần, hay script riêng từng phần để dễ phân chia công việc?

noh noh, hom phải, ảnh trong từng slide, chứ k phải biến cái trang thành ảnh


Thought process
Thought process
À hiểu rồi — bạn muốn lấy các ảnh được nhúng bên trong từng slide (diagrams, figures, photos) ra thành file riêng. Để làm video thì dùng các hình đó làm visual asset đúng không?


Ran 11 commands
Ran 11 commands
Part 5 bị interrupted giữa chừng vì quá lớn. Để chạy nốt:


Ran 4 commands
Ran 4 commands
Done! Part 5 xong rồi. Tổng kết:

images/
├── part1/  →  41 ảnh   (PPTX, đã deduplicate)
├── part2/  →  66 ảnh   (PPTX, đã deduplicate)
├── part3/  → 490 ảnh   (PDF)
├── part4/  →  63 ảnh   (PPTX, đã deduplicate)
└── part5/  → 294 ảnh   (PDF)
Một lưu ý thật thà: Part 3 và Part 5 nhiều ảnh bất thường vì pdfimages extract tất cả mọi thứ kể cả icon nhỏ, logo, ảnh nền — rất nhiều file vô dụng. Part 1/2/4 từ PPTX thì sạch hơn vì mình có deduplicate và chỉ lấy shape type picture.

Bạn muốn mình filter bớt Part 3 và Part 5 không — ví dụ bỏ các ảnh nhỏ hơn một kích thước nhất định?

ok đến lúc viết script rồi
bạn thử viết script nếu bạn phải thuyết trình slide part 1 đi


Thought process
Thought process
Để mình xem nhanh một số slide ảnh của Part 1 trước khi viết, để script có thể reference đúng visual:


Read 9 files, ran 2 commands
Read 9 files, ran 2 commands
Được rồi, mình có đủ visual context. Viết thôi:

📝 SCRIPT — PART 1: Foundation Models for Autonomous Driving
[Slide 1 — Title]

Câu hỏi mình muốn bắt đầu hôm nay rất đơn giản:

Tại sao năm 2025, với tất cả những thứ AI đã làm được — viết code, vẽ tranh, trả lời mọi câu hỏi — xe tự lái vẫn chưa chạy được khắp nơi?

Để trả lời câu đó, chúng ta cần hiểu AI đang ở đâu trong hành trình làm cho xe biết tự lái.

[Slide 2 — Outline]

Bài này sẽ đi theo ba bước. Trước tiên nhìn lại bức tranh tổng quan — AI đang ở đâu và autonomous driving đang ở đâu. Sau đó xem các nhà nghiên cứu đang làm gì để kết nối hai thứ đó với nhau. Và cuối cùng, tương lai đang đi về đâu.

[Slide 3 — Generative AI boom]

Trong hai năm vừa rồi, AI tạo sinh bùng nổ theo cách chưa từng có. ChatGPT viết code, Sora tạo video từ một câu mô tả, Midjourney vẽ tranh theo phong cách bất kỳ. Và nếu bạn nhìn kỹ hơn, bạn sẽ thấy tất cả những thứ đó đều đến từ một ý tưởng chung: train một model đủ lớn trên đủ nhiều dữ liệu, nó sẽ tự học được cấu trúc của thế giới.

Câu hỏi tự nhiên là: có thể làm điều tương tự với thế giới vật lý — cụ thể là giao thông — không?

[Slide 4 — Foundation Models là gì?]

Diagram này nói lên tất cả. Một foundation model được train trên đủ loại dữ liệu — text, ảnh, âm thanh, 3D signals — và sau đó có thể được adapt ra rất nhiều task khác nhau mà không cần train lại từ đầu.

Đây là điểm then chốt: thay vì build một model cho mỗi task, bạn build một model lớn hiểu thế giới, rồi chỉ cần fine-tune nhẹ cho từng ứng dụng cụ thể. GPT-4, CLIP, DINO — tất cả đều là foundation models theo nghĩa này.

Câu hỏi đặt ra là: autonomous driving hiện tại có đang dùng paradigm này không?

[Slide 5 — Ba trường phái AV hiện tại]

Câu trả lời là: chưa hẳn. Nhìn vào ba kiến trúc phổ biến nhất hiện nay.

Modular system — cái đầu tiên — chia mọi thứ thành các module riêng: perception để nhìn, localization để biết mình đang ở đâu, prediction để đoán xe khác sẽ đi đâu, planning để quyết định mình sẽ làm gì, control để ra lệnh cho bánh xe. Ưu điểm là dễ debug từng phần. Nhược điểm là lỗi tích lũy — nếu perception sai một chút, planning sẽ ra quyết định sai, và control sẽ thực hiện hành động sai.

End-to-end system — cái giữa — thay tất cả bằng một neural network duy nhất: camera và LiDAR vào, tay lái ra. Joint optimization, không mất thông tin giữa các module. Nhưng rất khó interpret — khi xe làm sai, bạn không biết tại sao.

Hybrid system — cái thứ ba — kết hợp cả hai. Dùng ML cho perception và planning, giữ lại control truyền thống. Đây là hướng mà nhiều công ty như Waymo đang theo.

Nhưng cả ba đều có chung một vấn đề mà mình sẽ nói đến ngay bây giờ.

[Slide 6 — Long-tail problem]

Ba tấm ảnh này là câu trả lời cho câu hỏi đầu tiên của mình.

Ảnh thứ nhất: một người đứng giữa làn đường đang dừng, tay cầm điện thoại. Ảnh thứ hai: một chiếc xe tải chở ba cái đèn giao thông ngược đầu. Ảnh thứ ba: đường phủ tuyết dày đến mức không còn thấy vạch kẻ đường đâu nữa.

Không có dataset nào train được tất cả những tình huống này. Đây là long-tail problem — 99% thời gian xe chạy bình thường, nhưng 1% còn lại chứa đủ loại tình huống kỳ lạ mà không ai nghĩ đến trước. Và trong những tình huống đó, model được train trên data bình thường sẽ fail.

Con người xử lý được những tình huống này vì chúng ta có common sense — chúng ta hiểu ngữ cảnh, hiểu ý định của người khác, hiểu vật lý của thế giới. Câu hỏi là: làm sao đưa common sense đó vào xe tự lái?

[Slide 7 — Foundation Models trong AV pipeline]

Đây là bức tranh tổng quan về hướng nghiên cứu hiện tại.

Foundation models đang được đưa vào từng lớp của pipeline. Vision Foundation Models như SAM, DINO, CLIP giúp tự động label dữ liệu — thay vì con người phải vẽ tay từng bounding box. LLMs và VLMs — Vision-Language Models — được dùng cho reasoning và decision-making. Video generation models giúp sinh ra các tình huống training tổng hợp. Và vector space models hỗ trợ motion planning.

Điểm chung của tất cả những hướng này: thay vì encode thủ công từng rule cho từng tình huống, để model tự học từ dữ liệu lớn.

[Slide 9-11 — Roadmap và Datasets]

Từ 2023, cộng đồng nghiên cứu bắt đầu build các dataset kết hợp ngôn ngữ với hành vi lái xe. DriveLM tạo cấu trúc graph: từ "tôi thấy gì" → "tôi dự đoán điều gì" → "tôi nên làm gì" → "tay lái xoay bao nhiêu". CoVLA thu thập 80 giờ video lái xe thực với trajectory action đi kèm.

Tại sao language lại quan trọng? Vì nó là cầu nối. Thay vì model học một mapping không thể giải thích từ pixels sang steering angle, ngôn ngữ ép model phải nói ra lý do — và điều đó giúp generalize tốt hơn trong các tình huống chưa gặp.

[Slide 12-15 — Các kiến trúc VLA cho AV]

Có nhiều cách khác nhau để kết hợp language model với AV. GPT-Driver thử dùng GPT-3.5 như một motion planner zero-shot — không cần fine-tune gì cả, chỉ cần describe tình huống bằng text và hỏi nó nên làm gì. Nghe kỳ lạ nhưng thực ra hoạt động được ở mức cơ bản.

BEVDriver làm kỹ hơn: encode LiDAR và camera thành BEV map — tức là nhìn cảnh vật từ trên xuống — rồi project vào LLM để predict waypoints. Đây là cách kết hợp 3D understanding với language reasoning.

[Slide 14 — EMMA của Waymo]

EMMA — được Waymo công bố — là một trong những model end-to-end ambitious nhất. Toàn bộ hệ thống được build trên Gemini. Input là raw camera frames. Output là chain-of-thought bằng ngôn ngữ tự nhiên, kèm theo trajectory, perception bounding boxes, và road graph.

Diagram này cho thấy điều thú vị: tất cả output đều đi qua ngôn ngữ. Xe không trực tiếp output steering angle — nó "nghĩ to" rồi mới hành động. Giống như cách một người lái xe mới học thường nói thành tiếng: "xe trước đang dừng, mình cần phanh dần".

Nhưng có một vấn đề rõ ràng: LLM rất chậm. Chạy real-time trên xe là thách thức lớn.

[Slide 17-20 — AutoVLA và Reasoning Fine-tuning]

Đây là nơi bài toán trở nên thú vị hơn. Nhóm UCLA đề xuất AutoVLA — giải pháp cho cả vấn đề latency lẫn vấn đề reasoning.

Ý tưởng cốt lõi: thay vì model lúc nào cũng phải "nghĩ dài", train nó có hai chế độ. Khi tình huống đơn giản, nó output action ngay. Khi tình huống phức tạp, nó kích hoạt chain-of-thought. Tương tự như cách con người xử lý — lái xe quen đường thì tay lái tự động, nhưng gặp ngã tư lạ thì phải dừng nghĩ.

Và bốn graph này — performance trên nuPlan và nuScenes — cho thấy điều quan trọng: reasoning training luôn tốt hơn action-only training, kể cả khi bạn đo bằng metrics không liên quan đến language. Dạy model suy luận giúp nó hành động tốt hơn.

Kỹ thuật được dùng là GRPO — một dạng Reinforcement Fine-tuning — để align model với verified rewards. Kết quả: cải thiện 10.6% trên planning benchmark và giảm 66.8% inference time.

[Slide 22-23 — Kết luận và Tương lai]

Vậy trả lời cho câu hỏi ban đầu — tại sao xe tự lái chưa chạy được khắp nơi?

Vì long-tail problem. Vì thiếu common sense. Vì các kiến trúc truyền thống encode rules thay vì hiểu thế giới.

Foundation models là hướng đi hứa hẹn nhất hiện tại — không phải vì chúng là magic bullet, mà vì chúng mang theo cái mà các model trước không có: khả năng generalize từ hiểu biết rộng về thế giới.

Nhưng vẫn còn nhiều thứ chưa giải quyết được: safety, latency, thiếu open-source data chất lượng cao. Và một thứ mà bài tiếp theo sẽ đào sâu hơn — single agent dù có thông minh đến đâu, vẫn bị giới hạn bởi tầm nhìn của chính mình.

Đó là cơ bản script Part 1. Bạn thấy tone và độ dài như này ổn không, hay muốn mình điều chỉnh theo hướng nào trước khi bắt tay vào các part còn lại?

Uploaded image
image.jpeg
hơi thiếu chi tiết
để tôi thêm thắt
Để mình xem nhanh một số slide ảnh của Part 1 trước khi viết, để script có thể reference đúng visual:Được rồi, mình có đủ visual context. Viết thôi:
📝 SCRIPT — PART 1: Foundation Models for Autonomous Driving
[Slide 1 — Title]
Câu hỏi mình muốn bắt đầu hôm nay rất đơn giản:
Tại sao năm 2025, với tất cả những thứ AI đã làm được — viết code, vẽ tranh, trả lời mọi câu hỏi — xe tự lái vẫn chưa chạy được khắp nơi?
Để trả lời câu đó, chúng ta cần hiểu AI đang ở đâu trong hành trình làm cho xe biết tự lái.
[Slide 2 — Outline]
Bài này sẽ đi theo ba bước. Trước tiên nhìn lại bức tranh tổng quan — AI đang ở đâu và autonomous driving đang ở đâu. Sau đó xem cộng đồng nghiên cứu xe tự lái đang làm gì để kết nối hai thứ đó với nhau. Và cuối cùng, những thách thức và tương lai của ngành
[Slide 3 — Generative AI boom]
Trong hai năm vừa rồi, AI tạo sinh bùng nổ theo cách chưa từng có. ChatGPT viết code, Sora tạo video từ một câu mô tả, Midjourney vẽ tranh theo phong cách bất kỳ. Và nếu bạn nhìn kỹ hơn, bạn sẽ thấy tất cả những thứ đó đều đến từ một ý tưởng chung: train một model đủ lớn trên đủ nhiều dữ liệu, nó sẽ tự học được cấu trúc của thế giới.
Câu hỏi tự nhiên là: có thể làm điều tương tự với thế giới vật lý — cụ thể là giao thông — không?

để tối viết lại cái này một xíu: từ năm 2023 những mô hình tạo sinh bùng nổ theo cách chưa từng có, hỗ trợ coding, khả năng suy luận xử lý ảnh, hiểu thế giới, etc. Tất cả những mô hình tạo sinh này đều có 1 điểm chung, chúng là những foundation models, theo định nghĩa từ stanford center for rs in FMs thì FM là bất kỳ mô hình nào được huấn luyện trên dữ liệu rộng lớn (tôi không dịch sát nghĩa từ broad, bạn dịch lại nha) thường là tự học có giám sát (self-sup) và có thể tinh chỉnh, thích nghi với những luồn downstream task như IE, OR, IF, IC, AD, QA, ETC.

những mô hình này đang làm mọi thứ better, vậy thì hãy áp dụng cho cho xe tự lái nào

Trước tiên chúng ta cần hiểu ngành công nghiệp AV hiện nay đang như thế nào

có 3 trường phái chính
modular ... thường được commerical deploy nhưng nó đối mặt với nhiều thách thức, như không hiệu quả, không nhất quán giữa những module làm tích lũy sai số và không thể học, những cái này thường được huấn luyện một lần, và lắp ráp các phần không thể học liên tục, gì đó, mô tả cái hình modular ra

tiếp theo là end-to-end, hình như bạn có nói ở dưới
với hybird bạn cũng có nói nên chắc tôi dừng comment ở đây

[Slide 4 — Foundation Models là gì?]
Diagram này nói lên tất cả. Một foundation model được train trên đủ loại dữ liệu — text, ảnh, âm thanh, 3D signals — và sau đó có thể được adapt ra rất nhiều task khác nhau mà không cần train lại từ đầu.
Đây là điểm then chốt: thay vì build một model cho mỗi task, bạn build một model lớn hiểu thế giới, rồi chỉ cần fine-tune nhẹ cho từng ứng dụng cụ thể. GPT-4, CLIP, DINO — tất cả đều là foundation models theo nghĩa này.
Câu hỏi đặt ra là: autonomous driving hiện tại có đang dùng paradigm này không?
[Slide 5 — Ba trường phái AV hiện tại]
Câu trả lời là: chưa hẳn. Nhìn vào ba kiến trúc phổ biến nhất hiện nay.
Modular system — cái đầu tiên — chia mọi thứ thành các module riêng: perception để nhìn, localization để biết mình đang ở đâu, prediction để đoán xe khác sẽ đi đâu, planning để quyết định mình sẽ làm gì, control để ra lệnh cho bánh xe. Ưu điểm là dễ debug từng phần. Nhược điểm là lỗi tích lũy — nếu perception sai một chút, planning sẽ ra quyết định sai, và control sẽ thực hiện hành động sai.
End-to-end system — cái giữa — thay tất cả bằng một neural network duy nhất: camera và LiDAR vào, tay lái ra. Joint optimization, không mất thông tin giữa các module. Nhưng rất khó interpret — khi xe làm sai, bạn không biết tại sao.
Hybrid system — cái thứ ba — kết hợp cả hai. Dùng ML cho perception và planning, giữ lại control truyền thống. Đây là hướng mà nhiều công ty như Waymo đang theo.
Nhưng cả ba đều có chung một vấn đề mà mình sẽ nói đến ngay bây giờ.
[Slide 6 — Long-tail problem]
Những mô hình FM cung cấp rất nhiều lợi ích những nó sẽ để lộ điểm yếu khi phải đối mặt với những thứ chưa từng thấy i.e longtail

Ví dụ như một tình huống lạ hoắt, ảo ảnh thị giác, hay ảnh phù đầy tuyết

Ba tấm ảnh này là câu trả lời cho câu hỏi đầu tiên của mình.
Ảnh thứ nhất: một người đứng giữa làn đường đang dừng, tay cầm điện thoại. Ảnh thứ hai: một chiếc xe tải chở ba cái đèn giao thông ngược đầu. Ảnh thứ ba: đường phủ tuyết dày đến mức không còn thấy vạch kẻ đường đâu nữa.
Không có dataset nào train được tất cả những tình huống này. Đây là long-tail problem — 99% thời gian xe chạy bình thường, nhưng 1% còn lại chứa đủ loại tình huống kỳ lạ mà không ai nghĩ đến trước. Và trong những tình huống đó, model được train trên data bình thường sẽ fail.

Vậy con người navigate và đối diện với những tình huốn này thế nào
Con người xử lý được những tình huống này vì chúng ta có common sense — chúng ta hiểu ngữ cảnh, hiểu ý định của người khác, hiểu vật lý của thế giới. Câu hỏi là: làm sao đưa common sense đó vào xe tự lái? chúng ta có contexttial reasoning với một cuộc đời liên tục tương tác với thế giới, và thu thập dữ liệu từ việc lái xe --> We need common-sense reasoning and generalist experience to handle new domains and the long tail

[Slide 7 — Foundation Models trong AV pipeline]

tôi có chèn lại ảnh của slide - chỉnh lại nhé tại khúc này tôi không thích bạn viết lắm mà tôi cũng không biết viết làm sao, kiểu như những fm đang empower cho những gì đó, raise lên sự cấp thiết của: Long-tail Generalization and Generalist Experience

Đây là bức tranh tổng quan về hướng nghiên cứu hiện tại.
Foundation models đang được đưa vào từng lớp của pipeline. Vision Foundation Models như SAM, DINO, CLIP giúp tự động label dữ liệu — thay vì con người phải vẽ tay từng bounding box. LLMs và VLMs — Vision-Language Models — được dùng cho reasoning và decision-making. Video generation models giúp sinh ra các tình huống training tổng hợp. Và vector space models hỗ trợ motion planning.
Điểm chung của tất cả những hướng này: thay vì encode thủ công từng rule cho từng tình huống, để model tự học từ dữ liệu lớn.
[Slide 9-11 — Roadmap và Datasets]
Roadmap có 4 hướng chính từ 2023 --> 2025 
tạo ra text action
tạo ra numerical action
tạo ra explicit guidance 
implicit representation transfer

Since the popularization of LLMs and VLMs in 2023, both industry and academia have actively explored the use of these multimodal foundation models for driving tasks.
These tasks span visual question answering, meta-action inference, perception, trajectory planning, and closed-loop driving.
Language is not only employed as input for human instructions but, more importantly, serves as an interface for contextual understanding and reasoning, aiming to enable informed decision-making and improve the handling of long-tail scenarios - trích từ slide
Từ 2023, cộng đồng nghiên cứu bắt đầu build các dataset kết hợp ngôn ngữ với hành vi lái xe. DriveLM tạo cấu trúc graph: từ "tôi thấy gì" → "tôi dự đoán điều gì" → "tôi nên làm gì" → "tay lái xoay bao nhiêu". CoVLA thu thập 80 giờ video lái xe thực với trajectory action đi kèm.
Tại sao language lại quan trọng? Vì nó là cầu nối. Thay vì model học một mapping không thể giải thích từ pixels sang steering angle, ngôn ngữ ép model phải nói ra lý do — và điều đó giúp generalize tốt hơn trong các tình huống chưa gặp.
[Slide 12-15 — Các kiến trúc VLA cho AV]
Có nhiều cách khác nhau để kết hợp language model với AV. GPT-Driver thử dùng GPT-3.5 như một motion planner zero-shot — không cần fine-tune gì cả, chỉ cần describe tình huống bằng text và hỏi nó nên làm gì. Nghe kỳ lạ nhưng thực ra hoạt động được ở mức cơ bản.
BEVDriver làm kỹ hơn: encode LiDAR và camera thành BEV map — tức là nhìn cảnh vật từ trên xuống — rồi project vào LLM để predict waypoints. Đây là cách kết hợp 3D understanding với language reasoning.
[Slide 14 — EMMA của Waymo]
EMMA — được Waymo công bố — là một trong những model end-to-end ambitious nhất. Toàn bộ hệ thống được build trên Gemini. Input là raw camera frames. Output là chain-of-thought bằng ngôn ngữ tự nhiên, kèm theo trajectory, perception bounding boxes, và road graph.
Diagram này cho thấy điều thú vị: tất cả output đều đi qua ngôn ngữ. Xe không trực tiếp output steering angle — nó "nghĩ to" rồi mới hành động. Giống như cách một người lái xe mới học thường nói thành tiếng: "xe trước đang dừng, mình cần phanh dần".
Nhưng có một vấn đề rõ ràng: LLM rất chậm. Chạy real-time trên xe là thách thức lớn.
[Slide 17-20 — AutoVLA và Reasoning Fine-tuning]
Đây là nơi bài toán trở nên thú vị hơn. Nhóm UCLA đề xuất AutoVLA — giải pháp cho cả vấn đề latency lẫn vấn đề reasoning.
Ý tưởng cốt lõi: thay vì model lúc nào cũng phải "nghĩ dài", train nó có hai chế độ. Khi tình huống đơn giản, nó output action ngay. Khi tình huống phức tạp, nó kích hoạt chain-of-thought. Tương tự như cách con người xử lý — lái xe quen đường thì tay lái tự động, nhưng gặp ngã tư lạ thì phải dừng nghĩ.
Và bốn graph này — performance trên nuPlan và nuScenes — cho thấy điều quan trọng: reasoning training luôn tốt hơn action-only training, kể cả khi bạn đo bằng metrics không liên quan đến language. Dạy model suy luận giúp nó hành động tốt hơn.
Kỹ thuật được dùng là GRPO — một dạng Reinforcement Fine-tuning — để align model với verified rewards. Kết quả: cải thiện 10.6% trên planning benchmark và giảm 66.8% inference time.
[Slide 22-23 — Kết luận và Tương lai]
Vậy trả lời cho câu hỏi ban đầu — tại sao xe tự lái chưa chạy được khắp nơi?
Vì long-tail problem. Vì thiếu common sense. Vì các kiến trúc truyền thống encode rules thay vì hiểu thế giới.
Foundation models là hướng đi hứa hẹn nhất hiện tại — không phải vì chúng là magic bullet, mà vì chúng mang theo cái mà các model trước không có: khả năng generalize từ hiểu biết rộng về thế giới.
Nhưng vẫn còn nhiều thứ chưa giải quyết được: safety, latency, thiếu open-source data chất lượng cao. Và một thứ mà bài tiếp theo sẽ đào sâu hơn — single agent dù có thông minh đến đâu, vẫn bị giới hạn bởi tầm nhìn của chính mình.
Đó là cơ bản script Part 1. Bạn thấy tone và độ dài như này ổn không, hay muốn mình điều chỉnh theo hướng nào trước khi bắt tay vào các part còn lại?

tôi nghĩ mấy slide cuối bạn nên check thêm text của slide - khá ổn rồi
tạo md đi

Show more

Thought process
Thought process
Để mình extract text Part 1 ra kiểm tra mấy slide cuối trước khi viết lại hoàn chỉnh:


Ran a command
Ran a command
Đủ rồi. Viết lại hoàn chỉnh và lưu thành file:


Created a file, read a file
Created a file, read a file
Xong! Một vài thay đổi chính so với draft đầu:

Slide 3: Viết lại theo đúng ý bạn — FM boom từ 2023, dẫn vào định nghĩa Stanford với "dữ liệu đa dạng, quy mô lớn" thay vì dịch sát "broad", rồi mới transition sang AV.

Slide 5: Bổ sung đủ ba challenge của modular — error accumulation, thiếu nhất quán giữa modules, và không thể học liên tục.

Slide 6: Reframe theo hướng bạn gợi ý — FM expose long-tail weakness trước, mô tả 3 ảnh, rồi dẫn vào human contextual reasoning, kết bằng đúng câu của slide gốc.

Slide 7: Viết lại xoay quanh "empower" và dẫn đến Long-tail Generalization and Generalist Experience như focal point.

Slide 22-23: Dùng đúng text của slide gốc làm backbone, không tự bịa thêm.

Cầu nối sang Part 2: Thêm đoạn transition tự nhiên vào single-agent limitation.

C:\Users\admin\Downloads\ICCV_DriveX_Tutorial\script_part1.md
Document 


Antigravity

yah tạm tạm ổn rồi đó
giờ đến slide part 2
thử thuyết trình xem nào


Thought process
Thought process
Để mình đọc text và visual của Part 2 trước:


Ran a command
Ran a command
Giờ xem thêm một số visual key:


Read 7 files, ran a command
Read 7 files, ran a command
Đủ rồi, viết thôi:


Created a file, read a file
Created a file, read a file
Xong Part 2! Một vài điểm mình chú ý khi viết:

Slide 5 — dùng đúng hình LiDAR để minh họa occlusion bằng physics argument, không phải algorithm — vì đây là lý do cơ bản nhất tại sao cần multi-agent.

Slide 9 — giải thích diagram what-when-how bằng cách walk qua Object 1/2/3 trong hình để người xem hiểu tại sao temporal context quan trọng.

Slide 16 — dùng chart TurboTrain để kể câu chuyện thay vì list bullet points: orange dots fail, blue arrows manual 4 stages, red stars TurboTrain win.

Slide 23 — ba paradigms (a)(b)(c) có emoji mặt buồn/buồn/vui, mình follow đúng logic đó để build tension rồi giải quyết.

Transition — kết bằng data + simulation gap để dẫn thẳng vào Part 3 một cách tự nhiên.

Bạn check qua rồi mình làm Part 3 nhé — Part 3 dày nhất (60 slides) nên có thể cần chọn lọc kỹ hơn một chút.

C:\Users\admin\Downloads\ICCV_DriveX_Tutorial\script_part2.md
Document 


Antigravity

slide part 2 pptx nó có note hay comment gì ở dưới slide á, có gì xem rồi chỉnh lại trước khi tôi chỉnh


Thought process
Thought process
Mình đã có markitdown output với notes rồi — để đọc lại kỹ và so với script:


Ran a command
Ran a command
Notes khá thưa — chỉ có notes ở slides đầu (2-15), còn từ slide 17 trở đi hầu như trống. So sánh với script, mình thấy 3 điểm cần chỉnh:

1. Slide 11 — One-step communication: thiếu physical intuition quan trọng

Notes của speaker nói rất rõ lý do: "the surrounding vehicle will leave you when you two have a large distance" — tức là khi hai xe đang gần nhau là cơ hội duy nhất để truyền data, vì sau đó xa ra thì mất cơ hội. Script mình viết khá chung chung — nên thêm cái này vào vì nó giúp người xem feel được vấn đề thay vì chỉ hiểu về mặt kỹ thuật.

2. Slide 16 — màu của "one-time training" trong chart

Notes ghi là "yellow point" nhưng nhìn vào hình thực tế thì là orange circles. Đây là discrepancy nhỏ giữa notes và slide cuối — script mình đang dùng "orange" theo hình, giữ nguyên là đúng.

3. Slides 17–29 — notes gần như trống hết

Từ TurboTrain methodology (slide 19) cho đến RiskMap và Summary đều không có notes. Nghĩa là phần đó mình viết dựa hoàn toàn vào slide text và hình ảnh — không có gì mâu thuẫn, nhưng cũng không có thêm context ẩn nào từ speaker.

Chỉnh lại đoạn one-step comm trong slide 11 nhé:

Trước:

vì khoảng cách giữa hai xe thay đổi liên tục và cơ hội để truyền dữ liệu có thể mất

Sau:

vì hai xe không ở gần nhau mãi — khi khoảng cách còn đủ nhỏ để truyền được, đó là cơ hội duy nhất. Sau khi xe kia đã đi xa, cơ hội đó mất hoàn toàn. Nên thay vì truyền từng frame một và hy vọng xe kia vẫn còn gần, truyền tất cả lịch sử trong một lần duy nhất khi đang còn cơ hội


Edited a file
Edited a file
Chỉnh xong rồi. Hai file script hiện tại:

script_part1.md — đã có edits của bạn từ hồi nãy
script_part2.md — vừa patch thêm đoạn one-step comm
Tiếp theo Part 3 hay bạn muốn review Part 2 thêm trước?

ok good rồi đó bạn hiểu hiểu kiểu thuyết trình của họ và của tôi rồi
next đi


Thought process
Thought process
Part 3 là PDF 60 slides — dày nhất, nên mình đọc text và check visual trước:


Ran a command
Ran a command
You've hit your limit · resets 1am (Asia/Bangkok)

yah, giờ tôi có nhờ gemini tạo script part 3,4,5 nhưng chưa ưng ý lắm, bạn hãy follow cái mà chúng ta thảo luận có gì viết lại nhé


Thought process
Thought process
Để mình xem thêm một số hình key của Part 3 và Part 4, rồi viết cả ba cùng lúc luôn:


Retrieved three tutorial images from DriveX project directories
Retrieved three tutorial images from DriveX project directories

Running command

Script

Running command

Script

Running command

Script

Read

Read C:\Users\admin\Downloads\ICCV_DriveX_Tutorial\images\part4\slide06_006_90aa9f1f.png

Read C:\Users\admin\Downloads\ICCV_DriveX_Tutorial\images\part5\img-009.jpg

Read

Read C:\Users\admin\Downloads\ICCV_DriveX_Tutorial\images\part4\slide12_011_f920ac00.png

Read C:\Users\admin\Downloads\ICCV_DriveX_Tutorial\images\part5\img-022.jpg
Now I have enough context to write all three scripts. Let me write them one by one. I'll write them all in parallel and save to files.

Part 3: Bridging Simulation and Reality in Cooperative V2X Systems

Hardware & Data Collection (UCLA Smart Intersection)
Mapping & Localization
Late & Intermediate Fusion in Reality
Digital Twin
Part 4: From Pre-Training to Post-Training: Building an Efficient V2X Cooperative Perception System

V2X Overview
CooPre (data efficiency)
TurboTrain (training efficiency) - brief since covered in Part 2
QuantV2X (inference efficiency)
Part 5: Building Scalable, Human-Centric Physical AI Systems

Physical AI vision
Two barriers
MetaUrban + UrbanSim
CityWalker + PedGen
Vid2Sim
I'm ready to write all three parts now, keeping the same conversational, narrative style with Vietnamese and English technical terms, building intuition first, natural transitions between sections, callbacks to earlier parts, and a clear bridge to what comes next. Let me start with Part 3.

For Part 3, I'm structuring it around a core question: we've built these training methods in Part 2, but where does the actual data come from and how do we deploy it safely? I'll open by recalling V2XPnP, TurboTrain, and RiskMap, then move into the real-world messiness—the three hard problems of perception, data quality, and safety. The UCLA Smart Intersection becomes my concrete testbed, where I'll walk through the sensor setup and CAV infrastructure, then dive into the calibration challenges (time synchronization with GPS and hardware triggers, spatial calibration with intrinsic and extrinsic parameters). From there, I'll explain the data collection routes, why HD maps are essential for both localization and building digital twins, and how localization works with a multi-rate error state Kalman filter. Then I'll contrast two fusion approaches in practice: late fusion with CooperFuse showing why temporal bounding box features matter beyond simple NMS, and intermediate fusion with V2X-ReaLO demonstrating online BEV feature sharing. Finally, I'll tie it all together with the digital twin concept.

For Part 4, I'm opening with the practical constraint trilogy: annotation is expensive, training is complex, and edge devices are resource-limited. The three pillars are data efficiency (CooPre with self-supervised pretraining achieving full performance on 50% of data), training efficiency (recapping TurboTrain from Part 2), and inference efficiency (QuantV2X showing quantization applied to the full V2X system).

Part 5 is just starting—I need to see where this is heading.

Now I'm zooming out to the bigger picture: we've built single-agent systems, then multi-agent V2X cooperation, but the real challenge is Physical AI across all robots in human spaces. The fundamental gaps are the lack of web-scale robot data and the absence of human behavior models. I'm thinking about the recipe here: scalable scene simulation through MetaUrban's compositional generation and UrbanSim's massive parallel capability, paired with human modeling through CityWalker and PedGen to capture unpredictability. Vid2Sim bridges the gap by building simulators from real video, and the conclusion ties everything together from Part 1 through Part 5.

Show more
Done
Đủ visual rồi, viết cả ba luôn:


Read three tutorial script files for ICCV 2025 conference presentation
Read three tutorial script files for ICCV 2025 conference presentation

Update todo list

Result

Created C:\Users\admin\Downloads\ICCV_DriveX_Tutorial\script_part3.md
C:\Users\admin\Downloads\ICCV_DriveX_Tutorial\script_part3.md

Running command

Script

Read

Read C:\Users\admin\Downloads\ICCV_DriveX_Tutorial\script_part4.md

Read C:\Users\admin\Downloads\ICCV_DriveX_Tutorial\script_part5.md
Ah, so Gemini already wrote scripts for Parts 3, 4, and 5. The user said they're not happy with them. Let me now rewrite all three following our established style from Parts 1 and 2. The Gemini versions are:

More simplified, almost like a children's explanation
Too casual and uses metaphors that are a bit off
Ends with self-referential comments like "Bạn thấy sao?" which shouldn't be in the final script
Uses citations like [cite: X] which is weird
Part 3 is quite good actually but the framing is too dramatic
Part 4 mentions things like "tiền điện và thời gian thuê GPU" which is correct but the tone is off
My approach:

Keep the technical depth of Parts 1 and 2
Keep Vietnamese with English technical terms explained
Follow slide-by-slide structure like Parts 1 and 2
No self-referential comments at the end
Solid transitions between parts
Remove citation numbers [cite: X]
Be more precise about what's on each slide
Now I'm rewriting all three parts from scratch, maintaining that technical but accessible tone we established earlier.

Show more
Done
Mình thấy rồi — Gemini viết theo kiểu giải thích cho người ngoài ngành, có cả câu "Bạn thấy sao?" ở cuối, citations số, và metaphors hơi quá tay. Mình viết lại cả ba theo đúng style Part 1 và Part 2 của chúng ta:


Created comprehensive script for Physical AI systems tutorial presentation
Created comprehensive script for Physical AI systems tutorial presentation

Created C:\Users\admin\Downloads\ICCV_DriveX_Tutorial\script_part3.md
C:\Users\admin\Downloads\ICCV_DriveX_Tutorial\script_part3.md

Update todo list

Result

Created C:\Users\admin\Downloads\ICCV_DriveX_Tutorial\script_part4.md
C:\Users\admin\Downloads\ICCV_DriveX_Tutorial\script_part4.md

Update todo list

Result

Created C:\Users\admin\Downloads\ICCV_DriveX_Tutorial\script_part5.md
C:\Users\admin\Downloads\ICCV_DriveX_Tutorial\script_part5.md
The conversation was cut off right after completing scripts for Parts 3, 4, and 5. I need to present these files to the user for review, just like we did with Parts 1 and 2.

Done
Ba script vừa được viết lại xong. Bạn xem qua nhé:


Presented three DriveX tutorial script files for review
Presented three DriveX tutorial script files for review
Ba script đã sẵn sàng để bạn xem. Tóm tắt nhanh những gì được viết lại:

Part 3 — Đi từ hardware thực tế (UCLA Smart Intersection, sensor suite) → calibration thời gian và không gian → data collection có hệ thống → localization bằng multi-rate Kalman Filter → CooperFuse (late fusion qua temporal BBX features thay vì NMS) → V2X-ReaLO (intermediate fusion, 0.5MB BEV compression) → Digital Twin với OpenCDA-ROS và CDA-SimBoost.

Part 4 — Ba bottleneck efficiency theo thứ tự: CooPre (self-supervised masked reconstruction, 50% data đạt 100% performance) → TurboTrain (nhắc lại ngắn, vì Part 2 đã cover chi tiết) → QuantV2X (giải thích tại sao FP32 tốn kém về năng lượng và memory, rồi INT8 quantization ở cả model-level và communication-level).

Part 5 — Physical AI vision → hai rào cản cơ bản → MetaUrban với power-law scaling → UrbanSim 2620 FPS → real-world deployment trên COCO robot → CityWalker + PedGen → Vid2Sim → kết luận nối toàn bộ 5 phần thành một chuỗi nhân quả.

Bạn đọc qua và cho tôi biết chỗ nào cần chỉnh nhé.

C:\Users\admin\Downloads\ICCV_DriveX_Tutorial\script_part3.md
Document 


Antigravity

C:\Users\admin\Downloads\ICCV_DriveX_Tutorial\script_part4.md
Document 


Antigravity

C:\Users\admin\Downloads\ICCV_DriveX_Tutorial\script_part5.md
Document 


Antigravity

