# Script — Part 1: Foundation Models for Autonomous Driving
**Tutorial: Beyond Self-Driving — ICCV 2025**
*Speaker: Dr. Zhiyu Huang, Postdoctoral Researcher, UCLA*

---

## [Slide 1 — Title]

Câu hỏi mình muốn bắt đầu hôm nay rất đơn giản:

*Tại sao năm 2025, với tất cả những thứ AI đã làm được — viết code, vẽ tranh, trả lời mọi câu hỏi — xe tự lái vẫn chưa chạy được khắp nơi?*

Để trả lời câu đó, chúng ta cần hiểu AI đang ở đâu và autonomous driving đang ở đâu.

---

## [Slide 2 — Outline]

Bài này sẽ đi theo ba bước. Trước tiên là bức tranh tổng quan — AI đang làm được gì và ngành xe tự lái đang ở đâu. Sau đó xem cộng đồng nghiên cứu đang làm gì để kết nối hai thứ đó với nhau. Và cuối cùng, những thách thức còn lại và tương lai của ngành.

---

## [Slide 3 — Generative AI Boom]

Từ năm 2023, những mô hình AI tạo sinh bùng nổ theo cách chưa từng có — hỗ trợ coding, suy luận phức tạp, xử lý ảnh, hiểu ngữ cảnh, thậm chí tạo video từ một câu mô tả.

Tất cả những mô hình đó đều có một điểm chung: chúng là **foundation models** — hay mô hình nền tảng. Theo định nghĩa từ Stanford Center for Research on Foundation Models, một foundation model là bất kỳ mô hình nào được huấn luyện trên dữ liệu đa dạng, quy mô lớn — thường thông qua self-supervised learning, tức là tự học không cần nhãn do con người gán — và có thể tinh chỉnh, thích nghi cho vô số downstream tasks: từ Information Extraction, Object Recognition, Image Captioning, cho đến Question Answering.

Đây không chỉ là một xu hướng. Những mô hình này đang làm mọi thứ tốt hơn trên hầu hết mọi lĩnh vực. Vậy thì câu hỏi đặt ra rất tự nhiên: **tại sao không áp dụng điều đó cho xe tự lái?**

Nhưng trước khi trả lời, chúng ta cần hiểu ngành AV hiện tại đang đứng ở đâu.

---

## [Slide 4 — Foundation Model Diagram]

Diagram này tóm gọn cơ chế của foundation models. Bên trái là dữ liệu: text, ảnh, speech, 3D signals. Tất cả đi qua quá trình training để tạo ra một model lõi. Và từ model lõi đó, chỉ cần adaptation nhỏ là có thể giải quyết được hàng chục task khác nhau ở bên phải.

Điểm then chốt: thay vì xây một model riêng cho mỗi bài toán, bạn xây **một model lớn hiểu thế giới**, rồi chỉ cần fine-tune nhẹ cho từng ứng dụng. GPT-4, CLIP, DINO — tất cả đều là foundation models theo nghĩa này.

---

## [Slide 5 — Ba trường phái kiến trúc AV]

Nhìn vào ba kiến trúc phổ biến nhất trong ngành xe tự lái.

**Modular system** là kiến trúc được triển khai thương mại nhiều nhất hiện nay — và không phải ngẫu nhiên, vì nó dễ debug, dễ kiểm soát từng phần. Pipeline chia làm các module tuần tự: perception để nhìn và phân loại môi trường, localization để biết xe đang ở đâu trên bản đồ, prediction để đoán xe khác sẽ đi đâu, planning để quyết định xe mình sẽ làm gì, và cuối cùng control để thực hiện hành động đó.

Nhưng modular system đối mặt với những thách thức cơ bản. Thứ nhất là **error accumulation** — lỗi tích lũy qua từng module: perception sai một chút, prediction sai theo, planning ra quyết định sai, control thực hiện hành động sai. Thứ hai là **sự thiếu nhất quán** giữa các module — mỗi module được tối ưu riêng lẻ, không có cơ chế joint optimization. Thứ ba, và quan trọng nhất: mỗi module thường được train một lần và đóng băng lại — **không thể học liên tục** từ kinh nghiệm thực tế.

**End-to-end system** thay toàn bộ pipeline bằng một neural network duy nhất: sensors vào, action ra. Không mất thông tin giữa các bước, tối ưu toàn bộ hệ thống cùng lúc. Nhưng khi xe làm sai, rất khó biết lỗi xuất phát từ đâu — và safety verification trở nên cực kỳ khó khăn.

**Hybrid system** kết hợp cả hai: dùng ML cho perception và planning, giữ lại control module truyền thống. Đây là hướng mà nhiều công ty lớn đang theo vì nó cân bằng được khả năng học với độ tin cậy của phần cứng.

Nhưng cả ba đều có chung một điểm yếu mà foundation models sẽ phơi bày rõ ràng nhất.

---

## [Slide 6 — Long-tail Problem]

Những foundation models mang lại rất nhiều lợi ích — nhưng chúng sẽ lộ điểm yếu ngay khi phải đối mặt với những thứ **chưa từng thấy trong training data**. Đây chính là bài toán long-tail.

Ba tấm ảnh này là minh họa trực tiếp.

Ảnh thứ nhất: một người đứng giữa làn đường đang dừng lại, tay cầm điện thoại. Không rõ họ đang làm gì, không rõ họ có nhận ra xe đang đến không. Ảnh thứ hai: một chiếc xe tải chở ba cái đèn giao thông — ngược đầu, không sáng — trên cao tốc. Model nào sẽ classify đây là "đèn giao thông" hay "vật thể lạ"? Ảnh thứ ba: đường phủ tuyết dày đến mức không còn thấy vạch kẻ đường. Lane detection hoàn toàn mù.

Không có dataset nào đủ lớn để bao phủ tất cả những tình huống như này. 99% thời gian xe chạy hoàn toàn bình thường — nhưng 1% còn lại chứa đủ loại edge cases mà không ai nghĩ đến trước. Và chính trong 1% đó, tai nạn xảy ra.

Vậy tại sao con người xử lý được những tình huống này? Vì chúng ta có **contextual reasoning** — khả năng suy luận dựa trên ngữ cảnh — được xây dựng qua cả một cuộc đời liên tục tương tác với thế giới. Chúng ta hiểu ý định của người khác, hiểu vật lý của môi trường, hiểu rằng đèn giao thông trên xe tải không phải tín hiệu thật. Đó là common sense.

Và đây là điều mà bài hôm nay muốn lập luận: **We need common-sense reasoning and generalist experience to handle new domains and the long tail.**

---

## [Slide 7 — Foundation Models empower AV]

Và đây là lý do tại sao foundation models trở nên quan trọng với autonomous driving.

Nhìn vào diagram này: bên trái là toàn bộ hệ sinh thái foundation models — Vision Foundation Models như SAM, DINO, CLIP; Video Generation Models như Wan và NVIDIA Cosmos; Vector Space Models như MotionLM và SceneDiffuser; Large Language Models; và Multi-modal Language Models như Gemma3, Qwen3-VL. Bên phải là những gì autonomous driving cần: auto-labeling, scenario generation, sensor simulation, vehicle interface, understanding & reasoning, và đặc biệt là **E2E Driving Stacks**.

Mũi tên ở giữa là "Empower" — và đây không phải từ ngẫu nhiên. Foundation models không thay thế AV stack, chúng **trao quyền** cho nó: giúp label dữ liệu tự động, sinh ra training scenarios phong phú hơn, và quan trọng nhất — đưa language reasoning vào quá trình ra quyết định.

Tất cả điều này hướng đến một mục tiêu duy nhất ở phía dưới: **Long-tail Generalization and Generalist Experience** — khả năng tổng quát hóa ra những tình huống chưa gặp, và kinh nghiệm đa dạng như một người lái xe thực thụ.

---

## [Slide 9-11 — Roadmap VLA cho AV & Datasets]

Từ 2023, cả academia lẫn industry đã bắt đầu khai thác LLMs và VLMs cho driving theo bốn hướng chính: sinh ra text action, sinh numerical action trực tiếp, cung cấp explicit guidance, và implicit representation transfer.

Như slide trích dẫn: *"Language is not only employed as input for human instructions but, more importantly, serves as an interface for contextual understanding and reasoning, aiming to enable informed decision-making and improve the handling of long-tail scenarios."*

Để train được những model này, cần có dữ liệu mới. DriveLM xây dựng cấu trúc graph liên kết ngôn ngữ với hành vi: từ "tôi thấy gì" → "tôi dự đoán điều gì sẽ xảy ra" → "tôi nên làm gì" → "trajectory cụ thể ra sao". CoVLA và Impromptu VLA thu thập hàng chục ngàn video clip lái xe thực, mỗi clip đi kèm cả trajectory lẫn language annotation.

Tại sao language quan trọng? Vì nó **ép model phải giải thích**. Thay vì học một mapping mờ từ pixels sang steering angle, model phải articulate lý do — và điều đó tạo ra một inductive bias rất mạnh cho generalization.

---

## [Slide 12-16 — Các kiến trúc VLA: GPT-Driver, BEVDriver, EMMA, DriveVLM]

Có nhiều cách khác nhau để kết hợp language model với AV.

**GPT-Driver** thử dùng GPT-3.5 như một motion planner zero-shot — không fine-tune, chỉ mô tả tình huống bằng text và hỏi nên làm gì. Nghe có vẻ naive nhưng thực ra hoạt động được ở mức cơ bản, vì GPT-3.5 đã encode rất nhiều common sense về giao thông từ internet.

**BEVDriver** kỹ càng hơn: encode LiDAR và camera thành BEV map — Bird's Eye View, tức là nhìn cảnh vật từ trên xuống — rồi project vào LLM để predict waypoints. Cách này kết hợp 3D spatial understanding với language reasoning.

**EMMA** từ Waymo là một trong những model end-to-end ambitious nhất. Được build trên Gemini, toàn bộ pipeline đi qua ngôn ngữ: input là raw camera frames, output là chain-of-thought kèm trajectory, perception bounding boxes, và road graph. Xe không trực tiếp output steering angle — nó *nghĩ to* rồi mới hành động. Giống như người học lái xe mới thường nói thành tiếng: "xe trước đang phanh, mình cần giảm tốc."

**DriveVLM** từ Tsinghua chọn hướng dual-system: VLM xử lý scene understanding và high-level planning ở tần số thấp, trong khi traditional 3D perception và trajectory planning module chạy real-time ở tần số cao. Kết hợp được thế mạnh của cả hai nhưng đổi lại là engineering complexity rất cao.

Điểm chung: language không còn là add-on nữa — nó trở thành trung tâm của kiến trúc.

---

## [Slide 17-20 — AutoVLA]

Đây là nơi bài toán trở nên thú vị hơn. Nhóm UCLA đề xuất AutoVLA — giải pháp xử lý đồng thời cả vấn đề latency lẫn vấn đề reasoning.

Hai hạn chế của các VLA models trước đó: thứ nhất, action generation thường không physically feasible hoặc có cấu trúc quá phức tạp; thứ hai, reasoning cứng nhắc — model lúc nào cũng phải "nghĩ dài" dù tình huống không cần.

Ý tưởng của AutoVLA: train model với **dual thinking modes**. Fast mode — chỉ output action khi tình huống đơn giản. Slow mode — kích hoạt chain-of-thought khi tình huống phức tạp. Tương tự cách hệ thống nhận thức của con người hoạt động: lái đường quen thì tay lái gần như tự động, nhưng gặp ngã tư lạ hay điều kiện thời tiết xấu thì phải dừng lại, quan sát kỹ, rồi mới quyết định.

Training gồm hai bước: SFT — Supervised Fine-tuning — để dạy model cả hai chế độ tư duy; và RFT — Reinforcement Fine-tuning dùng GRPO — để align model với verified rewards, tức là phần thưởng có thể kiểm chứng được từ môi trường.

Kết quả trên nuPlan và nuScenes — cả bốn metrics — đều cho thấy một pattern nhất quán: **reasoning training luôn outperform action-only training**, kể cả khi đo bằng metrics không liên quan đến language. Dạy model suy luận tốt hơn giúp nó hành động tốt hơn. RFT mang lại cải thiện 10.6% trên planning score và giảm 66.8% runtime.

---

## [Slide 22 — Key Takeaways]

Vậy tóm lại có bốn điều cần ghi nhớ từ phần này.

Thứ nhất: foundation models mở khóa khả năng xử lý **long-tail generalization** — điều mà các kiến trúc truyền thống không làm được vì chúng encode rules thay vì hiểu thế giới.

Thứ hai: MLLMs — Multimodal Large Language Models — đang nổi lên như một hướng đi hứa hẹn cho scalable AV, mang theo out-of-domain generalization và world knowledge từ internet.

Thứ ba: kiến trúc hiện tại rất đa dạng — dual-system, unified E2E, BEV input, RL fine-tuning — phản ánh một lĩnh vực đang trong giai đoạn tìm kiếm tích cực, chưa có một paradigm thống trị rõ ràng.

Thứ tư, và thành thật nhất: foundation models không phải magic. Safety, interpretability, và verification vẫn là những thách thức cơ bản chưa được giải quyết. Chi phí tính toán và latency vẫn là rào cản lớn cho real-time deployment. Và trong academia, hạn chế lớn nhất là **thiếu dữ liệu open-source chất lượng cao**.

---

## [Slide 23 — Future Directions]

Bốn hướng mà ngành đang hướng tới.

**Post-training for VLA Alignment**: dùng reinforcement learning kết hợp với simulation thực tế để align language reasoning với driving actions, đồng thời giảm latency và tăng khả năng online adaptation.

**Unified Multimodal Backbone**: fuse 2D, 3D, và spatial representations trong một backbone duy nhất, dùng language làm medium chung cho scene understanding và future prediction.

**Efficient VLA Models**: tối ưu inference để đạt low-latency, closed-loop control phù hợp với deployment thực tế — đây là điều kiện bắt buộc để ra khỏi lab.

**Continual Learning**: cho phép model tiếp tục học từ real-world feedback, thích nghi với môi trường mới, và generalize qua các vùng địa lý, điều kiện thời tiết, và văn hóa giao thông khác nhau.

---

## [Slide 24 — Cầu nối sang Part 2]

Và đây là nơi câu chuyện tiếp tục — vì dù foundation models có giải quyết được long-tail problem, vẫn còn một giới hạn căn bản mà không model nào vượt qua được chỉ bằng cách nhìn rõ hơn.

**Single agent, dù có thông minh đến đâu, vẫn bị giới hạn bởi tầm nhìn của chính mình.**

Nếu có xe khác đỗ chắn tầm nhìn, nếu có người đi bộ khuất sau góc khuất, không có foundation model nào giúp được. Đó là lý do tại sao phần tiếp theo sẽ nói về một paradigm hoàn toàn khác: **không phải làm cho một agent thông minh hơn, mà là để nhiều agent hợp tác với nhau.**

---

*[Hết Part 1 — ~10 phút trình bày]*
