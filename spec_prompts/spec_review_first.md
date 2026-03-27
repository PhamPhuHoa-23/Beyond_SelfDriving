I01: Title Card: ok
I02: Hook: chữ i see còn đè lên 2 chữ gpt và vlm
I02: Roadmap: ok
P01S01: Pi đang nói tiếng việt, đổi hết thành tiếng anh, chữ ở chính giữa và Pi nói chuyện bị dính vào chính giữa, có thể nâng text lên trên và thay vì hiện box của pi theo sequence và lần lượt nhiều vị trí khác nhau thì chỉnh cho nó 1 vị trí box thôi, chỉ là ẩn hiện 
P01S02: box foundation models còn hơi sát với chữ, mở rộng chiều rộng sẽ ok, phần fms là gì thì mũi tên đang chưa thẳng tắp, có lẽ là lỗi align gì đó, chỉnh sau nó thẳng tại nó đang hơi đi xuống rồi đi lên
P01S03: AV Arch: ok
P01S04: cái trục của distribution xuất hiện sau khi nói chuyện (nó sai), nó nên xuất hiện đồng thời với phân phối, sau khi 3 cái node vào 1% thì nên thu nhỏ nó lên trên, sau đó cho 2 mascot nói chuyện chứ không nó overlap
P01S05: ổn nhưng không hiểu sao nền xanh
P01S06: trong cái chain thì cái chữ gần cái node quá, đừng chỉ làm mờ, bạn move nó vào giữa nó overlap hết, fadeout luôn hoặc thu nhỏ hoặc move lên trên head 1 cách có tổ chức
P01S07: BEVDriver mấy cái module không thẳng hàng, mũi tên thì thẳng rồi nhưng align giữa các block chưa đẹp, còn lại ổn
P01S08: Nâng những block đầu lên cao một xíu, vì khi hiển thị reasoning traning gì đó thì nó overlap vào block stage 1 stage 2 
P01S09: ok ổn, nhưng sẽ ổn hơn nếu tăng chiều rộng, và chỉnh lại khoảng cách giữa các box
P01S01: OK
P02S02: ok, chỗ 80% reduction tôi nghĩ là nên shrink cái cùng red trước đó nhỏ lại và biến nó thành màu cam thôi, đừng hiện box (nó overlap), phải có 1 cái gì đó như cái ngoặc để thể hiện giảm 80%, còn lại ok
P02S03: vì roadmap hiện trên dưới xen kẽ, nên là cái chỗ bạn phân ra modular với cái gì đó, vẽ lên nó bị đè lên những cái mô hình nào hiện phía dưới, chỉnh lại hợp lý. Cái box e2e advantage thif nó đè lên cái roadmap luôn, có lẽ cần fade đi hoặc chỉnh lại position, mascot hỏi bị overlap lên roadmap trong thời điểm hiện tại chưa sửa code
P02S04: chỗ coverage gain nó nhỏ xíu á, không biết là do vẽ sai hay sao mà toàn bộ vùng màu đỏ vẫn còn tồn tại nhưng idea thì vẫn ổn, nhưng cần check lại, nếu cần thì nên lấy 1 scene ở khoảng 5-6 giây để hiểu tôi nói gì
P02S05: Tương tự là cái chữ rất gần node, và nó không ẩn hoặc move đi nên box lúc sau hiện lên bị overlap: 
P02S06: ok
P02S07: các chữ gần mũi tên quá, tại scene fusion (recommend là xóa box màu vàng n-frames gì đó), thì nó sẽ đỡ gần nnhauhonw, về cái how to fuse thì cũng đẹp rồi nhưng chỗ box của spatial attention thì nó hơi gần temporal feature và agent2 feature, nên cho nó dịch sang phải một chút và hiện tại 2 mũi tên từ 2 box feature đang trỏ sai, và box detection không align theo hàng ngang với multi-agent spatio-temporal representation và nó quá gần nên bị overlap luôn
P02S08: ok hay
P02S09: Cái pipeline stage bên phải overlap với cái chú thích, nếu được thì mmovecais chú thích sang gần chỗ cái hệ trục, tiếp theo là stage 2 hhiện4 cái mũi tên chĩa ra phía ngang liên tiếp (tôi không rõ nghĩa của việc này)
P02S10: Chữ riskmap bị overlap, tôi nghĩ bạn nên move x và tick xuống dưới thay vì ở trên 1 dòng với các block module để có thể move các block qua bên phải thì sẽ hết overlap
P02S11: ok
P02S12: box nói chuyện của mascot overlap với box reality
P03S02: move cái pipeline 4 block sang trái còn vấn đề sang phải, hiện tại 1 cái ơ giữa 1 cái bên phải overlap nhau tùm lum
P03S03:thêm cái chú thích intersection ở đâu, 2 cái chú thích infa node với connect, mình xếp theo chiều dọc và cho nó qua trái luôn, bạn xếp nó thành 1 hàng ngang thì box infra node bị overlap với cái hình sau khi đã thu nhỏ, box nói chuyện xong rồi thì ẩn xuống tại để đó thì nó overlap
P03S04: tôi nghĩ là bạn nên để 1 cái box trùng nhau, nhưng mà box đó là kết hợp của 2 box xanh đỏ, xong box đỏ di chuyển cchậmhonw còn box xanh di chuyển nhanh hơn thì sẽ đúng hơn (kiểu nó tách ra á), và cái vạch kẻ đường hiển thị sau cùng cũng hơi lạ nha
P03S05: chỗ mà 2 điểm align hay không align á, thhìbanj cũng nên vẽ trục tọa độ, và nên thêm nhiều điểm tương tự như vậy nữa, rồi khi mà nó align thì mấy cái chữ của 2 cái cục nó chồng lên nhau á, tôi nghĩ bạn ênn suy nghĩ cách fix
P03S06: ok
P03S07: ok
P03S08: ok
P03S09: ổn rồi nhưng mà cho thêm hiệu ứng bên NMS là một cái box nào đó xoay hoặc move nha
P03S10: tôi nghĩ là bạn nên design theo kiểu cái đó compress thành 1 cái nhỏ hơn rồi move cái đó lên cái cán cân thì nó cân bằng (nên có sự rung lắc), với lại mũi tên chưa có thẳng nha
P03S11: mấy cái mũi tên nó overlap với nhau hết, siêu gần nhau luôn
P03S12: ok
P03S13: ok
P03S14: nói xong ẩn box của mascot xe tự lái là được, tại nó overlap với phần sau hiển thị
P04S01: ok
P04S02: ok
P04S03: cái distribution vẽ center quá, cái chứ 5x in 2 years nó bị đè lên chính giữa cái bar chart cuối, mấy cái bullet point move sang phải chứ nó vẫn còn overlap trong cái chart
P04S04: cái mũi tên từ 2 cái rect trỏ vào vào cái grid và nó chưa có align chính giữa 2 cái. cái mũi tên tăng 4% AP thì nó đang bị bay ra ngoài chart 
P04S05: cái chỗ gradient conflict thì vẽ cái 3d coord, vẽ một cái mặt phẳng gì đó vẽ mấy vector ngược hướng nhau trên đó nó trực quan hơn á.
P04S06: ok
P04S07: ở scene đầu cái total time thì để nó xuống dòng đi, để kế bên bố cục nó không có cân, 3 cái block thì nên xa nhau thì mũi tên mới rõ hơn. scene 2 cái bar chart thì cái chart đứng, cái chữ nó đè lên cái chart đỏ cao và tôi nghĩ mình nên consistency giữa 2 cái chart luôn, một cái ngang 1 cái đứng thì cũng kỳ, và tôi nghĩ bạn có thể tận dụng không gian bên dưới tại vì như bạn vẽ từ đâu đó center lên á, nên phía dưới trống và scene này cũng không có text gì nhiều, chúng ta có thêr tăng kích thước lên kiểu vậy
P04S08: cái int8 nó đè hẳn lên FP32 luôn, nếu bạn làm hiệu ứng shrink thì làm lại tại vì nó nằm chính giữa cái dải màu đỏ luôn ấy. chỗ distribution thì cái chữ vàng đang overlap với chữ đỏ ở 1 phần góc trái trên của chữ đỏ
P04S09: ok
P04S10: 3 cái bullet point chưa căn lề trái cho bằng nhau