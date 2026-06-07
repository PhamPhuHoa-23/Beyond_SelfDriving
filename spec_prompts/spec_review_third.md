P01S01Opening:
Mascot Pi ở vị trí hơi cao, làm cho cái box nói chuyện của nó bị overlap lên box chữ trước đó.
P01S04LongTail
Còn lỗi vẽ trục sau khi đã hiển thị phân phối, 99 và 1, đúng ra nó phải là vẽ trục rồi mới vẽ mấy cái hàm chứ
P01S06VLARoadmap
Làm cho cái box language is at the core bự  hơn về chiều rộng một xíu tại vì hiện tại chữ đang dính với box ở 2 phía trái phải
Tự nhiên cuối scene nó hiện tất cả mọi thứ lên lại nó kỳ cục nên bỏ giúp tôi nhé
P01S07VLAArch
Cái BEV Map có cái hình gì hay sao mà không align thẳng hàng vậy, nếu bạn muốn vẽ thì cụ thể hoặc không thì bỏ đi tại vì flow đang khá align và thẳng cái BEV nó bị tụt xuống dưới
P01S08AutoVLA
Chỉnh lại ending tại vì tụi mình còn merge video (lỗi hơi kiểu kiểu P01S06VVLARoadma nhưng nó hơi nnngượclaf nó ẩn đi hết và tự nhiên để 2 cái text stage 1 với stage 2 lại)
P02S02Background: 
Bỏ cái note dưới chỗ 80% đi vì nó overlap với ggrid tai nạn
P02S03Evolution:
vấn đề ending, tất cả hiện lại ở những giây cuối
P04S05MultiTaskConflict
box multiframe gì đó ở cảnh đầu tăng chiều rộng lên, chú ý coi chừng overlap mũi tên
P05S08Vid2Sim:
2 cái rect 3d gauss với mask gì đó, cho nó xa nnhaulucs xuất hiện theo chiều dọc một xíu
với lại tôi không hiểu tại sao lại kéo gần 2 cái rect kia lại để làm gì, nếu không kéo thì bạn phải căn chỉnh cái chứ appearance ggìddos cao lên trên tránh overlap vùng center
chỗ sim to real bạn thu nhỏ mũi tên hơi mắc cười tại vì sim với real không thay đổi position, với lại text nó cũng nhỏ quá