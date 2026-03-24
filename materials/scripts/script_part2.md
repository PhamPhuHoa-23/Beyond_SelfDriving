# Script — Part 2: Towards End-to-End Cooperative Automation
**Tutorial: Beyond Self-Driving — ICCV 2025**
*Speaker: Zewei Zhou, PhD Candidate, UCLA Mobility Lab*

---

## [Slide 1 — Title]

Phần trước chúng ta đã nói về foundation models và long-tail problem của single-agent systems. Và câu kết là: dù xe có thông minh đến đâu, nó vẫn bị giới hạn bởi tầm nhìn của chính mình.

Phần này sẽ đi tiếp từ đó — không phải làm cho một agent nhìn thông minh hơn, mà làm cho nhiều agent **hợp tác với nhau** để cùng hiểu môi trường.

---

## [Slide 2-3 — Background: Tại sao xe tự lái quan trọng]

Mỗi năm có 1.19 triệu người chết vì tai nạn giao thông trên toàn thế giới. 94% trong số đó do lỗi con người. Waymo gần đây công bố rằng xe tự lái của họ giảm được 80% số vụ tai nạn gây thương tích so với lái xe người.

Và không chỉ dừng lại ở xe hơi — delivery robots đang thay thế con người trong vận chuyển hàng hóa, từ Amazon đến COCO. AI agents đang reshape toàn bộ cách chúng ta di chuyển và vận hành logistics.

Đây là lý do tại sao bài toán này quan trọng.

---

## [Slide 4 — Single-agent: từ Modular đến End-to-End]

Trước khi nói về multi-agent, cần nhìn lại trajectory của single-agent systems. Có một xu hướng rõ ràng trong vài năm qua: từ modular pipeline sang end-to-end paradigm.

Những milestone quan trọng: PnPNet dùng CNN+LSTM cho joint perception và prediction. GameFormer đưa interactive prediction vào planning. UniAD xây dựng hệ thống end-to-end với query-based design, tối ưu toàn bộ pipeline cùng lúc. DiffusionDrive mới nhất dùng diffusion model để generate trajectory với anchored distribution.

So với modular, end-to-end có ba lợi thế cốt lõi: không có error accumulation giữa các module, không mất thông tin khi chuyển qua các bước, và joint optimization cho phép toàn bộ hệ thống học hướng tới một mục tiêu chung.

Vậy end-to-end đã giải quyết mọi thứ chưa?

---

## [Slide 5 — Giới hạn của single-agent: Occlusion]

Chưa. Và đây là lý do tại sao.

Nhìn vào hai hàng ảnh LiDAR này. Hàng trên là single-agent nhìn một giao lộ — LiDAR scan từ một điểm duy nhất, rất nhiều vùng tối xung quanh. Hàng dưới là cùng giao lộ đó nhưng có thêm một agent khác — vùng phủ tăng lên đáng kể, những khoảng tối được lấp đầy.

Đây là vấn đề cơ bản của physics, không phải của algorithm. Nếu có một xe tải đỗ chắn tầm nhìn, không có foundation model nào nhìn xuyên qua được. Nếu có người đi bộ khuất sau góc khuất, single-agent không thể biết.

Giải pháp duy nhất là **complementary information sharing** — để các agents chia sẻ những gì mỗi người nhìn thấy mà người khác không thấy. Multi-agent system ra đời từ đây.

---

## [Slide 6-8 — Related Works và Research Gaps]

Cộng đồng đã nghiên cứu multi-agent fusion khá tích cực. Các phương pháp phát triển theo hướng ngày càng tinh vi: từ simple GNN trong V2VNet, sang Transformer-based attention trong V2X-ViT, đến sparse communication trong Where2comm, và codebook-based compression trong CodeFilling.

Về dataset, hành trình từ simulation (OPV2V) sang real-world (V2X-Real) cũng được ghi nhận rõ.

Nhưng có hai gaps quan trọng mà tất cả những công trình này chưa giải quyết.

**Gap thứ nhất về mô hình**: tất cả chỉ tập trung vào cooperative perception đơn lẻ — detect đối tượng rồi dừng. Làm sao cooperation benefit được toàn bộ automation chain — prediction và planning — vẫn còn là câu hỏi mở. Và quan trọng hơn: tất cả đều single-frame, bỏ qua temporal cues. Không biết lịch sử chuyển động của đối tượng thì prediction sẽ rất hạn chế.

**Gap thứ hai về data**: các dataset hiện tại thiếu sequential data và HD maps cho downstream tasks. Và hầu hết chỉ hỗ trợ V2V hoặc V2I riêng lẻ, chưa có dataset nào cover đầy đủ tất cả collaboration modes.

---

## [Slide 9 — Research gap: Single-frame → Multi-frame Multi-task]

Diagram này nói lên tất cả sự khác biệt.

Hệ thống truyền thống — hàng trên — là single-frame cooperative perception: agents chia sẻ thông tin của một frame duy nhất, fuse lại, detect bounding boxes, rồi tracking qua các frame để ra trajectory. Pipeline rời rạc, mỗi bước xử lý độc lập.

Hệ thống mà phần này hướng tới — hàng dưới — là cooperative temporal perception and prediction: agents chia sẻ thông tin qua nhiều frames lịch sử, spatio-temporal fusion xảy ra đồng thời, và detection lẫn prediction được tối ưu cùng lúc trong một end-to-end framework.

Và đây là lý do tại sao temporal dimension quan trọng: khi nhìn vào ba đối tượng ở hàng dưới — Object 1 đang rẽ, Object 2 đi thẳng, Object 3 đang dừng — không có lịch sử chuyển động thì không thể phân biệt được ai sẽ làm gì tiếp theo.

Điều này dẫn đến ba câu hỏi cốt lõi mà phần này phải trả lời: **truyền gì? truyền khi nào? fuse như thế nào?**

---

## [Slide 10-15 — V2XPnP (ICCV 2025)]

**Research Problem 1**: Làm thế nào để build và test một end-to-end spatio-temporal fusion framework cho multiple tasks trong multi-agent system?

Câu trả lời là **V2XPnP** — Vehicle-to-Everything Spatio-Temporal Fusion for Multi-Agent Perception and Prediction.

*What to transmit?* V2XPnP xem xét cả ba chiến lược: early fusion truyền raw LiDAR, late fusion truyền detected bounding boxes, và intermediate fusion truyền BEV features. Điểm khác biệt so với cooperative perception truyền thống là cả ba chiều đều có temporal dimension — không phải một frame mà là chuỗi lịch sử.

*When to transmit?* Đây là vấn đề tinh tế hơn. Nếu truyền từng frame một — multi-step communication — nghe có vẻ đơn giản, nhưng thực ra không ổn định. Lý do rất cụ thể: hai xe không ở gần nhau mãi. Khi khoảng cách còn đủ nhỏ để liên lạc được, đó là cơ hội duy nhất để trao đổi thông tin — sau khi xe kia đã đi xa, cơ hội đó mất hoàn toàn. Giải pháp của V2XPnP là one-step communication: khi đang còn gần, truyền toàn bộ lịch sử nhiều frames trong một lần duy nhất. Tất nhiên điều này tạo ra communication load lớn, nên temporal attention được dùng để nén toàn bộ lịch sử đó về kích thước single-frame trước khi truyền đi — giữ được temporal context mà không tốn băng thông quá mức.

*How to fuse?* Hai module chính: temporal attention và spatial attention. Temporal attention xử lý lịch sử chuyển động của từng agent riêng lẻ. Spatial attention sau đó fuse thông tin across different agents tại cùng một thời điểm. Kết hợp lại cho ra multi-agent spatio-temporal representation đầy đủ.

Song song với framework, nhóm cũng xây dựng **V2XPnP-Seq** — dataset real-world đầu tiên hỗ trợ tất cả V2X collaboration modes: V2V, V2I, V2X, I2I. 2 xe và 2 infrastructure nodes, 40K LiDAR frames, 208K camera frames, kèm HD maps và trajectories.

Kết quả benchmark cho thấy: intermediate features + one-step communication + temporal/spatial/map fusion là combination hiệu quả nhất, và V2XPnP outperform tất cả SOTA models trước đó.

---

## [Slide 16-22 — TurboTrain (ICCV 2025)]

**Research Problem 2**: Làm thế nào để train một framework multi-agent, multi-frame, multi-task hiệu quả với limited data?

Nhìn vào chart này sẽ hiểu ngay vấn đề. Trục x là AP@0.5 — detection accuracy. Trục y là EPA — prediction accuracy. Các điểm màu cam là one-time training attempts: performance rất thấp, thậm chí fail hoàn toàn. Các điểm màu xanh là manual training qua 4 stages: Stage 1 single-agent detection → Stage 2 temporal prediction → Stage 3 joint tuning → Stage 4 multi-agent fusion. Mỗi stage là một lần train riêng, tổng cộng 120 epochs.

Có hai lý do cơ bản tại sao multi-agent multi-task system khó train. Thứ nhất: kiến trúc phức tạp với nhiều dimensions làm model rất sensitive với initialization — train một lần thường dẫn đến instability hoặc fail hoàn toàn như những điểm cam kia. Thứ hai: **gradient conflict** — các tasks khác nhau thường "kéo" model theo hướng ngược nhau trong weight space, không có cơ chế balancing thì task này improve task kia lại degrade.

**TurboTrain** giải quyết cả hai bằng một pipeline 2-stage thay vì 4-stage thủ công.

Stage 1 — Pretrain: học một task-agnostic 4D representation bằng cách reconstruct LiDAR point cloud bị mask. Không cần annotation, không cần biết task cuối cùng là gì. Mục tiêu đơn giản là: hiểu cấu trúc spatiotemporal của môi trường. Đây giải quyết vấn đề initialization.

Stage 2 — Balance: fine-tune với hybrid training strategy xen kẽ giữa *free gradient steps* — cho các tasks học tự do — và *conflict-suppressing steps* — phát hiện và giải quyết gradient conflict giữa các tasks. Đây giải quyết vấn đề gradient conflict.

Kết quả trên chart: TurboTrain đạt performance cao nhất với chỉ khoảng 45 epochs — ít hơn một nửa so với manual 4-stage training. Và quan trọng hơn là **không cần human expertise** để quyết định khi nào chuyển stage.

---

## [Slide 23-25 — RiskMap]

**Research Problem 3**: Làm thế nào để extend spatio-temporal fusion framework sang planning, hướng tới cooperative end-to-end autonomous driving thực sự?

Diagram này tóm tắt rất gọn ba paradigms.

(a) Modular — vẫn error accumulation, vẫn limited perception range. Đã biết vấn đề này.

(b) Conventional end-to-end — black box. Xe biết phải làm gì nhưng không ai biết tại sao, kể cả engineer. Safety verification gần như impossible.

(c) Proposed — và đây là điểm mấu chốt: thay vì để model tự quyết định trong black box, đưa vào một **Risk Map** làm middleware. Risk Map là một explicit representation của spatiotemporal risk distribution trong môi trường — về cơ bản là một bản đồ xác suất nguy hiểm theo không gian và thời gian. Từ Risk Map đó, một learning-based MPC module tính toán trajectory.

Tại sao cần Risk Map làm trung gian? Vì nó tách biệt hai câu hỏi: *"môi trường này nguy hiểm ở đâu?"* và *"với nguy hiểm đó, tôi nên đi đường nào?"*. Câu hỏi đầu là perception/prediction — AI giỏi. Câu hỏi sau là planning — có thể kiểm chứng, có thể interpret, có thể constrain về mặt safety.

RiskMM outperform tất cả SOTA fusion methods và planning models trên cả ba tasks: detection, prediction, và planning.

---

## [Slide 26-28 — Summary]

Ba vấn đề — ba giải pháp tạo thành một stack hoàn chỉnh.

**V2XPnP** xây dựng nền tảng: dataset real-world đầy đủ và framework để trả lời ba câu hỏi what-when-how cho spatio-temporal fusion.

**TurboTrain** giải quyết thực tiễn: làm cho framework đó trainable và efficient với pretrain-then-balance paradigm.

**RiskMap** mở rộng về phía output: từ perception và prediction sang interpretable planning với middleware tường minh.

---

## [Cầu nối sang Part 3]

Nhưng để tất cả những thứ này hoạt động ngoài thực tế, có một điều kiện tiên quyết mà chúng ta chưa đề cập.

Tất cả các model trên đều cần được train và test. Và để train multi-agent systems ở quy mô thực, bạn cần cả hai thứ: **dữ liệu thực từ sensor thật ngoài đường**, và **môi trường simulation đủ tốt** để tạo ra đủ loại tình huống training.

Đây là cái gap mà phần tiếp theo sẽ đào sâu vào — khoảng cách giữa simulation và reality trong cooperative V2X systems, và làm thế nào để bridge nó.

---

*[Hết Part 2 — ~10 phút trình bày]*
