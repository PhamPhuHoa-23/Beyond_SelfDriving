# Script — Part 5: Building Scalable, Human-Centric Physical AI Systems
**Tutorial: Beyond Self-Driving — ICCV 2025**
*Speaker: Wayne Wu, Research Associate, UCLA*

---

## [Slide 1 — Title]

Bốn phần trước đã xây một stack hoàn chỉnh cho xe tự lái: từ foundation models cho reasoning, đến multi-agent V2X cooperation, đến real-world deployment, đến efficient inference trên edge devices.

Phần này bước ra khỏi xe hơi hoàn toàn.

Câu hỏi không còn là "làm sao xe tự lái tốt hơn" — mà là "làm sao AI vận hành an toàn trong bất kỳ môi trường vật lý nào, cùng với con người?" Đây là bài toán **Physical AI** theo nghĩa rộng hơn.

---

## [Slide 2-8 — Vision và hai rào cản cơ bản]

Hình dung một general-purpose Physical AI: có thể hoạt động trong bất kỳ môi trường nào, thực hiện bất kỳ task nào. Nghe giống science fiction — nhưng nhìn vào những gì LLMs đã làm được với ngôn ngữ, câu hỏi là tại sao chúng ta không thể làm điều tương tự với thế giới vật lý?

LLMs thành công vì một lý do rất cụ thể: **web-scale data**. Toàn bộ internet — hàng nghìn tỷ tokens — là training data. Model học được world knowledge, reasoning, và common sense từ đó.

Physical AI không có điều này. Có hai rào cản cơ bản.

**Barrier 1 — Thiếu web-scale robot learning data.** Không có robot-created data trên internet ở quy mô đủ lớn cho behavior cloning. Không giống text, behavior data trong thế giới vật lý phải được thu thập chủ động — từng robot, từng environment, từng task. Scale-up theo cách đó là impossible.

**Barrier 2 — Thiếu human modeling trong context.** Robots hoạt động trong môi trường có con người — người đi bộ, người đạp xe, người đứng chắn đường. Không model được behavior của con người thì không thể đảm bảo safety. Và đây không phải vấn đề nhỏ — slide trong tutorial dùng đúng từ "zombie city" để mô tả simulation environment không có con người thực sự.

Recipe để giải quyết cả hai: **Scene Simulation → Scalable** kết hợp với **Human Modeling → Human-Centric**.

---

## [Slide 9-12 — Micro-mobility: Testbed thực tế]

Trước khi đi vào từng contribution, cần hiểu context của bài toán.

60% chuyến đi ở Mỹ ngắn hơn 5 dặm — đây là domain của micro-mobility: delivery robots, AI-powered electric wheelchairs, intelligent scooters, và humanoid robots. Đây không phải highway autonomous driving — đây là navigation trong môi trường đô thị dày đặc, với pedestrians, curbs, uneven terrain, và vô số edge cases.

UCLA hợp tác với COCO Robotics — delivery robots thực tế trong môi trường campus và urban areas — làm testbed để validate các methods.

---

## [Slide 13-24 — MetaUrban: Scalable Scene Simulation (ICLR 2025 Spotlight)]

**Trụ cột đầu tiên: Scene Simulation.**

Nếu không có đủ real-world data, phải build simulation environment đủ tốt để substitute. Nhưng một simulation environment cụ thể không scale — bạn cần vô số environments đa dạng.

**MetaUrban** giải quyết điều này bằng compositional scene generation. Insight cốt lõi đến từ một câu quote trong slide: *"The world is compositional, or there is a god"* — Stuart Geman.

Thay vì design từng scene thủ công, MetaUrban dùng **description scripts** để procedurally generate urban scenes: số lượng blocks, loại intersections, lane width, sidewalk layout, loại và mật độ objects. Kết hợp các parameters này theo các distribution khác nhau tạo ra infinite unique environments — không có hai training scenes nào giống hệt nhau.

Và đây là empirical finding quan trọng nhất từ MetaUrban: **power-law scaling giữa scene diversity và performance**. Khi số lượng unique training layouts tăng lên, performance trên unseen test environments tăng theo power-law — không phải linear, không phải logarithmic, mà power-law. Điều này có nghĩa là diversity trong training environments quan trọng hơn quantity — 100 diverse scenes tốt hơn 1000 scenes lặp lại cùng một layout.

Kết hợp với **UrbanVerse** — reconstruct real-world scenes từ city-tour videos thành simulation environments — để có thêm realistic asset distribution không bị bias bởi human design decisions.

---

## [Slide 25-38 — UrbanSim: Training Efficiency (CVPR 2025 Highlight)]

Scene diversity không đủ nếu training quá chậm. Và đây là vấn đề thực tế: training một RL agent đơn giản với traditional platforms như MetaUrban, iGibson, CARLA cần đến 180 GPU days để đạt 95% success rate — con số không thực tế cho research iteration.

Bottleneck là architecture của traditional platforms: CPU xử lý physics và observations, transfer data sang GPU, GPU chạy neural network forward pass, transfer actions ngược lại về CPU. Mỗi lần transfer giữa CPU và GPU là một latency hit, và với hàng trăm parallel environments thì nó cộng dồn nghiêm trọng.

**UrbanSim** xây trên NVIDIA Omniverse để giữ mọi thứ trên GPU end-to-end — physics simulation, observation computation, neural network inference, tất cả đều ở trên GPU. Không CPU-GPU transfer trong hot loop.

Thêm vào đó, **asynchronous scene sampling** thay vì synchronous: thay vì tất cả environments dùng cùng một set of objects, mỗi environment có heterogeneous configuration riêng — khác nhau về layout, obstacles, và pedestrian placement. Agents trong các environments khác nhau không bị sync với nhau, tăng throughput đáng kể.

Kết quả: **2,620 FPS** với 256 parallel environments, chỉ dùng **11.2GB GPU memory** (24.3% của 46GB available). Trong 3 giờ wall-clock time, UrbanSim với 256 environments đạt 41% success rate — so với 6% của single environment. 180 GPU days → 3 giờ.

Real-world deployment trên COCO wheeled delivery robot và Unitree Go2 quadruped robot xác nhận: **PPO-UrbanVerse** — agent train trong UrbanVerse real-world reconstructed environments — outperform tất cả SOTA navigation models (S2E, CityWalker, NoMaD) trên cả crosswalk và sidewalk scenarios.

---

## [Slide 39-47 — CityWalker & PedGen: Human Modeling (ICLR 2025)]

Đây là chỗ mà "zombie city" problem được tackle trực tiếp.

Existing human motion datasets như AMASS capture human motion trong isolation — không có scene context, không có destination, không có surrounding environment. Một người đi bộ generated từ những datasets này sẽ đi xuyên tường, ignore obstacles, và có trajectory không realistic.

**CityWalker** là dataset đầu tiên capture pedestrian behavior trong context của urban environments thực tế: 30.8 giờ video chất lượng cao, 120,914 pedestrians, 16,215 scenes trên 227 thành phố. Diversity không chỉ về số lượng mà về loại movement — người dắt stroller, người lấy điện thoại ra chụp ảnh, người gãi đầu khi ngồi, người chỉ vào tường. Đây là behavior data thực, không phải performance trong motion capture studio.

Từ dataset đó, **PedGen** được train — một diffusion model cho pedestrian motion generation có điều kiện trên scene context.

Ba conditioning inputs: **Scene Context** — 3D voxel representation của môi trường xung quanh để pedestrian biết đâu là chướng ngại vật; **Body Context** — SMPL body shape parameters để motion phù hợp với thể trạng người cụ thể; và **Goal** — điểm đến mà pedestrian đang hướng tới.

Loss function gồm ba thành phần: reconstruction loss để giữ body poses anatomically realistic; trajectory loss để đảm bảo path tích phân velocity đi đúng hướng; và geometry loss qua forward kinematics để giữ joints ở đúng vị trí trong không gian 3D.

Kết quả với/không có context conditioning cho thấy sự khác biệt rõ: without context, pedestrian generated đi theo trajectory không realistic, xuyên qua objects. With context, pedestrian navigate một cách coherent với môi trường.

---

## [Slide 50-54 — Vid2Sim: Simulation từ Video (CVPR 2025)]

Mảng cuối cùng: làm sao build simulation environment realistic mà không cần manual modeling.

**Vid2Sim** cho phép convert video thực tế thành interactive 3D simulation environment. Pipeline kết hợp hai kỹ thuật: **3D Gaussian Splatting** cho realistic visual rendering — reconstruct scene geometry và appearance từ multi-view images, cho ra ảnh photorealistic từ bất kỳ viewpoint nào; và **mesh reconstruction** để có physical interaction — robot có thể va chạm, đứng trên mặt đất, và interact với objects.

Kết hợp 3DGS (realistic observations) và mesh (physical interactions) cho ra simulator mà robot được train trong đó sẽ thấy environment trông giống real world, và physics interaction cũng realistic.

Robot train trong Vid2Sim simulator, rồi deploy ra environment thực tế — sim-to-real gap giảm đáng kể vì visual fidelity cao.

---

## [Slide 55-56 — Kết luận: Full Picture]

Nhìn lại toàn bộ five-part tutorial.

**Part 1** đặt câu hỏi: tại sao single-agent autonomous driving chạm giới hạn và foundation models là hướng đột phá. **Part 2** mở rộng sang multi-agent V2X — làm sao nhiều xe hợp tác spatiotemporally. **Part 3** grounding vào reality — hardware, calibration, localization, và real-world deployment. **Part 4** giải quyết efficiency — data, training, và inference. Và **Part 5** mở rộng toàn bộ bức tranh sang Physical AI — scalable simulation và human-centric safety.

Đây không phải năm topics riêng rẽ. Đây là một chuỗi nhân quả: mỗi phần giải quyết bottleneck mà phần trước để lại, và mỗi solution tạo ra câu hỏi mới cho phần tiếp theo.

Đó là câu chuyện của *Beyond Self-Driving* — không phải làm cho một chiếc xe thông minh hơn, mà xây dựng toàn bộ ecosystem để AI vận hành an toàn trong thế giới vật lý với con người.

---

*[Hết Part 5 — ~12 phút trình bày]*
