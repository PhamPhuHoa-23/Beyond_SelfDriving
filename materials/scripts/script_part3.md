# Script — Part 3: Bridging Simulation and Reality in Cooperative V2X Systems
**Tutorial: Beyond Self-Driving — ICCV 2025**
*Speaker: Zhaoliang Zheng, PhD Candidate, UCLA Mobility Lab*

---

## [Slide 1 — Title]

Hai phần trước xây được một stack khá solid trên lý thuyết — cooperative fusion, spatio-temporal reasoning, interpretable planning. Nhưng có một gap mà tất cả những thứ đó chưa chạm tới: **data đến từ đâu, và khi deploy ra đường thực thì trông như thế nào?**

Phần này là phần engineering nặng nhất của toàn bộ tutorial — từ bolt và sensor cho đến pipeline chạy real-time ngoài đường.

---

## [Slide 3-5 — Bốn mảng chính & Background]

Nội dung chia làm bốn mảng, đúng theo thứ tự bạn phải build một hệ thống thực: Hardware & Data Collection trước, rồi Mapping & Localization, rồi mới đến Late & Intermediate Fusion, và cuối cùng là Digital Twin.

Ba challenge cốt lõi: giải quyết "can't-see" problem qua cooperative driving automation; làm data đủ trustworthy để model có thể học được từ nó; và đảm bảo safety trong các khu vực nguy hiểm như giao lộ đô thị. Để làm ba thứ đó, nhóm UCLA triển khai V2X sensor suite tại một giao lộ thực và build data acquisition platform share thông tin qua V2X network.

---

## [Slide 6-11 — UCLA Smart Intersection]

Nhìn vào hình map này — giao lộ Charles E. Young Dr và Westwood Plaza ngay trong campus UCLA. Hai góc đỏ là hai infrastructure nodes, và bạn có thể thấy luôn ảnh thực tế của giao lộ bên trái.

Đây không phải simulation. Đây là một giao lộ đang hoạt động với xe cộ thật và người đi bộ thật.

Hệ thống gồm: **2 infrastructure nodes** — Northwest corner có LiDAR 128-line, 2 cameras, 1 radar; Southeast corner có LiDAR 64-line, 2 cameras, và C-V2X communication unit. Và **2 Connected Automated Vehicles** — mỗi xe có 4 stereo cameras, LiDAR RoboSense Ruby Plus 128-line, và GNSS/IMU integration.

Tại sao cần nhiều sensor đến vậy? Vì mỗi loại có điểm mù riêng: camera fail trong điều kiện ngược sáng hoặc đêm tối, LiDAR xuống cấp khi mưa lớn, GNSS mất tín hiệu khi có tòa nhà cao chắn. Redundancy không phải overkill — đó là điều kiện cần để hệ thống reliable ngoài thực tế.

---

## [Slide 12-17 — Sensor Calibration: Time & Space]

Khi có nhiều agents và nhiều sensors hoạt động đồng thời, có một vấn đề gần như ngay lập tức xuất hiện: **làm sao sync tất cả lại với nhau?**

**Time calibration** — đồng bộ thời gian. Một xe đang chạy 60km/h, nếu infrastructure gửi observation bị lệch 50ms thì đối tượng sẽ bị "hiện" ở vị trí lệch gần 1 mét so với thực tế. Giải pháp: GPS làm time reference chung cho tất cả agents, kết hợp hardware trigger để đảm bảo tất cả sensors chụp đúng cùng một thời điểm — không phải software trigger vì software có jitter.

**Space calibration** — đồng bộ không gian. Mỗi sensor sống trong hệ tọa độ riêng của nó. Intrinsic calibration cho camera xác định focal length và distortion. Extrinsic calibration xác định transform từ camera frame sang LiDAR frame, từ LiDAR frame của xe sang world frame. Không có extrinsic calibration chính xác, point clouds từ các nguồn khác nhau khi fuse lại sẽ bị lệch và tạo ra "ghost objects" — đối tượng ảo không tồn tại.

Calibration tools được release open-source qua PJLab SensorsCalibration trên GitHub.

---

## [Slide 18-22 — Data Collection]

Với hardware calibrated, bước tiếp theo là thu thập dữ liệu một cách có hệ thống. Không phải lái xe random rồi record — mà có các **basic routes** được thiết kế: rẽ phải, rẽ trái, đi thẳng; sau đó **combined routes** kết hợp nhiều maneuvers lại. Mỗi combination cho ra góc nhìn và overlap khác nhau giữa infrastructure và vehicle sensors.

Ngoài các routes, data cũng được thu thập ở các **thời điểm khác nhau trong ngày** — để capture đủ điều kiện ánh sáng, mật độ giao thông, và thời tiết.

Kết quả là datasets V2X-Real (ECCV 2024) và V2XPnP-Seq — hai dataset mà các phần trước đã reference. Đây là nguồn gốc thực tế của chúng.

---

## [Slide 23-32 — Mapping & Localization]

HD Map và Localization là backbone của toàn bộ hệ thống — không phải một feature thêm vào sau, mà là điều kiện tiên quyết cho mọi thứ khác.

HD Map đóng vai trò trung tâm trong ba thứ: Data Acquisition Platform cần map để geo-tag sensor data; Localization cần map để xe biết chính xác mình đang ở đâu; và Digital Twin cần map làm environment scaffold.

Nhưng với cooperative perception, localization có thêm một ý nghĩa đặc biệt. Slide 27 minh họa rõ nhất: infrastructure node thấy một đối tượng ở một góc, vehicle thấy cùng đối tượng từ góc khác. Để fuse hai observations này, cả hai **phải biết chính xác vị trí của mình trong world frame**. Không có localization chính xác, hai point clouds không có relationship với nhau — bạn không biết chúng đang nói về cùng một đối tượng hay hai đối tượng khác nhau.

Slide 28 cho thấy điều tệ hơn: với localization sai, fused result không chỉ kém mà còn **tệ hơn single-agent** — vì bạn đang fuse thông tin sai vị trí vào.

Giải pháp là **multi-rate error-state Kalman Filter** cho real-time localization. Ba nguồn sensor với tần số khác nhau được fuse lại: GNSS cung cấp absolute position nhưng chỉ 5Hz và bị block bởi buildings. IMU và wheel speed sensors cho high-frequency updates 100Hz nhưng tích lũy drift theo thời gian. LiDAR map-matching cho pose correction bằng cách so scan hiện tại với pre-built HD map — chính xác nhưng computation nặng nên chạy 1Hz.

Kalman Filter tích hợp cả ba, xử lý measurement delay do đồng bộ, và output pose liên tục ở 100Hz — real-time, lane-level accuracy.

---

## [Slide 33-43 — Late Fusion trong thực tế: CooperFuse]

**CooperFuse** là hệ thống cooperative late fusion real-time đầu tiên cho V2X — được present tại IV 2024.

Late fusion: mỗi agent detect locally, share detected bounding boxes, fuse kết quả lại. Lightweight về bandwidth, không cần share raw data hay intermediate features. Nhưng có một vấn đề kỹ thuật cụ thể khi fuse bounding boxes từ nhiều agents.

Cách truyền thống: NMS — Non-Maximum Suppression — pick bounding box nào có confidence score cao hơn. Nhưng confidence score chỉ trả lời "tôi có chắc là detect được object không?" — nó không encode bất kỳ thông tin nào về **đặc điểm vật lý** của bounding box: position XYZ, orientation, scale.

Insight của CooperFuse: thay vì dùng confidence score, **dùng temporal features của bounding box để fuse** — vị trí, hướng, kích thước của object qua nhiều frames lịch sử. Một bounding box từ infrastructure có thể có confidence thấp hơn nhưng orientation chính xác hơn vì góc nhìn tốt hơn. Fusion by temporal BBX features capture điều đó, còn NMS thuần túy thì không.

---

## [Slide 44-49 — Intermediate Fusion trong thực tế: V2X-ReaLO]

Nếu late fusion trade accuracy để đổi lấy bandwidth thấp, intermediate fusion đi ngược lại — share BEV features để giữ rich representation nhưng phải kiểm soát latency chặt.

**V2X-ReaLO** là hệ thống online intermediate fusion đầu tiên cho V2X trong thực tế — submit to T-PAMI.

Trade-off cụ thể ở đây: message size lớn thì accuracy cao hơn nhưng latency tăng; message size nhỏ thì latency thấp nhưng mất thông tin. Trong V2X, latency là tối kỵ — một xe đang di chuyển không thể chờ. Nhóm tìm được working point ở **0.5MB per message** — nén BEV feature xuống 32 lần so với uncompressed — đủ giữ accuracy mà vẫn fit trong real-world V2X bandwidth budget.

BEV feature là một high-dimensional map nhìn từ trên xuống, mỗi "cell" encode thông tin về môi trường tại vị trí đó: static features như đường và vỉa hè, dynamic features như xe và người đi bộ, tất cả trong cùng một representation. Đây là thứ được compress và truyền đi giữa các agents.

---

## [Slide 50-59 — Digital Twin: OpenCDA-ROS và CDA-SimBoost]

Phần cuối của pipeline — đóng vòng lặp giữa simulation và reality.

**OpenCDA-ROS** là bridge giữa hai thế giới. ROS — Robot Operating System — là middleware chuẩn trong robotics. OpenCDA-ROS kết nối simulation environment với real-world data flow qua ROS, xử lý V2X communication modules, multi-agent time synchronization, và data streaming. Kết quả: code viết để chạy trên xe thật cũng chạy được trong simulation mà không cần rewrite.

**CDA-SimBoost** làm được toàn bộ vòng lặp: import real-world data từ ROS, build digital twin của environment đó trong CARLA, generate challenging scenarios từ digital twin, rồi train và benchmark trong simulation. Modular design cho phép swap từng component khi cần.

Tại sao cần generate challenging scenarios thay vì chỉ replay real data? Vì data ngoài đường chủ yếu là tình huống bình thường — giao lộ thông suốt, thời tiết tốt, không có ai cắt đầu xe đột ngột. Model cần được expose với edge cases: tầm nhìn hạn chế khi trời mưa, pedestrian băng qua đột ngột, sensor failure một phần. Digital twin cho phép tạo ra những scenarios này có kiểm soát và ở số lượng đủ để train.

Cuối cùng, **OpenCDA-InfraX** là data generation platform với flexible sensor configuration, multi-modality, weather variation, và vector maps — tất cả trong một để support downstream model training.

---

## [Cầu nối sang Part 4]

Từ hardware đến real-world deployment, phần này đã xây xong toàn bộ infrastructure layer cho V2X.

Nhưng vẫn còn một thực tế phũ phàng chưa được giải quyết: annotation dataset real-world cực kỳ tốn kém, training framework phức tạp khó converge, và khi deploy lên edge devices trên xe thì computation budget rất hạn chế.

Đây là bộ ba bottleneck về efficiency — data, training, và inference — mà phần tiếp theo sẽ tackle trực tiếp.

---

*[Hết Part 3 — ~12 phút trình bày]*
