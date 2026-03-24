# Script — Part 4: From Pre-Training to Post-Training: Building an Efficient V2X Cooperative Perception System
**Tutorial: Beyond Self-Driving — ICCV 2025**
*Speaker: Seth Z. Zhao, PhD Candidate, UCLA Mobility Lab*

---

## [Slide 1 — Title]

Ba phần trước đã xây được một hệ thống V2X hoạt động được trong thực tế — từ hardware, đến fusion algorithm, đến digital twin. Nhưng có một câu hỏi thực tế luôn bị defer: **làm sao để hệ thống này efficient đủ để tồn tại trong điều kiện thực?**

Không phải chỉ là chạy được — mà là chạy được trên dữ liệu hạn chế, train được mà không cần GPU months, và deploy được trên edge hardware của xe.

Phần này tackle ba bottleneck đó theo thứ tự: data efficiency, training efficiency, inference efficiency.

---

## [Slide 2-7 — Overview V2X và tại sao efficiency quan trọng]

V2X — Vehicle-to-Everything — là paradigm để các agents chia sẻ thông tin và "mượn mắt" nhau, giải quyết bài toán occlusion mà single-agent không thể làm được. Công nghệ này đang nhận được sự chú ý không chỉ từ academia mà còn từ US Department of Transportation trong các dự án smart intersection cho pedestrian safety.

Nhưng để build một V2X system thực sự scalable và deployable, có ba câu hỏi chưa có câu trả lời thỏa đáng từ các phần trước: làm sao đạt performance tốt khi data annotated bị hạn chế? Làm sao train một multi-task multi-agent framework mà không tốn hàng tháng compute? Và làm sao chạy inference real-time trên edge device với memory và power budget thấp?

Ba câu hỏi đó tương ứng với ba hướng nghiên cứu của phần này.

---

## [Slide 9-14 — Data Efficiency: CooPre (IROS 2025)]

**Mặt trận đầu tiên: Data.**

Datasets V2X đang tăng nhanh về scale — V2V4Real có 240K annotations, DAIR-V2X có 460K, V2X-Real của UCLA lên đến 1.2 triệu. Số lượng tăng 5 lần nhưng annotation cost cũng tăng theo tỉ lệ đó. Annotation 3D LiDAR data đòi hỏi software toolkit phức tạp, human annotators được train bài bản, và quy trình checking nhiều lớp. Không scale được theo cách này.

Câu hỏi: **làm sao model học được khi không có đủ labeled data?**

**CooPre** — Cooperative Pretraining for V2X — là phương pháp self-supervised pretraining đa agent đầu tiên cho cooperative perception. Không cần annotation nào.

Cơ chế cốt lõi: multi-agent masked reconstruction. Trong pretraining stage, model nhận LiDAR point cloud từ nhiều agents, random mask một số voxels trên BEV plane, rồi được yêu cầu reconstruct lại các phần bị mask đó. Task đơn giản nhưng để làm được, model phải học được 3D geometric structure của môi trường — và quan trọng hơn là học cách khai thác thông tin từ các agents khác để fill in những gì mình không thấy.

Đây là một inductive bias rất mạnh và rất phù hợp với cooperative perception: model học rằng "khi tôi không thấy một phần của scene, tôi có thể hỏi agent khác." Đây chính xác là cái mà cooperative perception cần.

Sau khi pretrain, model được fine-tune trên downstream detection task với labeled data. Kết quả: dùng 50% labeled data, CooPre đạt performance tương đương model train từ đầu với 100% data. Và khi dùng đủ 100% data, CooPre cải thiện thêm 4% AP so với baseline.

Ngoài ra, pretraining cross-domain — train trên một dataset rồi transfer sang dataset khác — cũng cho kết quả tốt hơn single-domain, cho thấy representation mà CooPre học được là genuinely generalizable.

---

## [Slide 15-22 — Training Efficiency: TurboTrain (ICCV 2025)]

**Mặt trận thứ hai: Training.**

Phần 2 đã giới thiệu TurboTrain — nhưng ở đây đào sâu hơn vào lý do tại sao training một multi-agent multi-frame multi-task system lại khó đến vậy.

Khi bạn extend single-frame cooperative perception sang multi-frame multi-task, kiến trúc trở nên phức tạp hơn nhiều chiều: temporal dimension, multiple agents, multiple tasks cùng lúc. Độ phức tạp này tạo ra hai vấn đề.

Thứ nhất: **model initialization sensitivity** — một model phức tạp như vậy rất sensitive với điểm khởi đầu. Train từ đầu một lần duy nhất (one-time training) thường dẫn đến instability hoặc convergence về local minima tệ. Đó là những orange dots trên chart — các powerful models fail hoàn toàn khi train one-time.

Thứ hai: **gradient conflict** giữa các tasks — detection, prediction, và planning thường có gradients kéo model theo hướng khác nhau trong weight space. Khi conflict nặng, improving một task làm degrade task kia.

TurboTrain giải quyết cả hai bằng hai-stage pipeline. Stage 1 — pretraining: học task-agnostic 4D representation bằng cách reconstruct masked LiDAR point cloud của multi-agent, multi-frame data. Không annotation, không task-specific objective — chỉ học cấu trúc spatiotemporal của môi trường. Stage 2 — balancing: fine-tune với hybrid training strategy xen kẽ free gradient steps và conflict-suppressing steps.

Từ 120 epochs manual 4-stage → 45 epochs TurboTrain, với performance cao hơn và không cần human expertise để quyết định khi nào chuyển stage.

---

## [Slide 22-31 — Inference Efficiency: QuantV2X]

**Mặt trận thứ ba: Inference.**

Đây là bottleneck thường bị bỏ qua trong research nhưng là thứ quyết định một hệ thống có deploy được hay không.

Để hiểu tại sao inference efficiency quan trọng trong V2X, nhìn vào latency chain: mỗi agent phải chạy local inference, sau đó communication latency để truyền features, rồi fusion inference để tích hợp thông tin từ nhiều agents. Mỗi bước đều có time budget — và tổng latency phải đủ nhỏ để decision-making vẫn real-time.

Vấn đề cơ bản là về **arithmetic cost**. Neural networks thường dùng FP32 — floating point 32-bit. Multiplication FP32 tốn năng lượng nhiều hơn addition, và tệ hơn là nó scale quadratically. Memory access là bottleneck thứ hai: đọc 32-bit data từ DRAM tốn khoảng 640 pJ mỗi lần, so với 5 pJ từ SRAM. Với hàng triệu parameters cần được load, con số này cộng dồn rất nhanh trên edge hardware.

Giải pháp là **quantization** — giảm bit-width của weights và activations. Chuyển từ FP32 sang INT8, phép nhân trở thành phép cộng số nguyên, memory footprint giảm 4 lần, và nhiều chip edge có hardware support cho INT8 inference với throughput cao hơn nhiều.

**QuantV2X** là hệ thống V2X fully quantized đầu tiên — đồng thời ở hai levels. Model-level: toàn bộ neural network từ FP32 sang INT8. Communication-level: thay vì truyền FP32 BEV features, compress thành low-bit codebook — nhỏ hơn 300 lần so với uncompressed.

Đây là bước tiến quan trọng cho thực tế: không phải chứng minh rằng quantization hoạt động trong isolation, mà chứng minh rằng **fully quantized cooperative perception pipeline** — cả model lẫn communication — là viable cho deployment, mà performance drop là chấp nhận được.

---

## [Cầu nối sang Part 5]

Ba bottleneck về efficiency đã được giải quyết. Hệ thống giờ có thể học từ ít data, train không cần nhiều compute, và chạy được trên edge devices.

Nhưng toàn bộ Parts 2, 3, 4 đều tập trung vào một thứ: **xe hơi và infrastructure**. Thế giới vật lý rộng hơn nhiều so với đó — có delivery robots, humanoid robots, electric scooters, electric wheelchairs. Và tất cả những thứ đó phải hoạt động trong cùng một không gian với **con người** — những thứ unpredictable nhất trong toàn bộ equation.

Đây là câu hỏi mà phần cuối sẽ trả lời: làm thế nào để build Physical AI systems thực sự scalable và an toàn trong môi trường có con người?

---

*[Hết Part 4 — ~10 phút trình bày]*
