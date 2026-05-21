---
name: user-animation-preferences
description: User preferences for the Beyond Self-Driving Manim animation project — what they like and dislike
metadata:
  type: feedback
---

Render xong thì cứ send lệnh background, không cần chờ signal.

**Why:** Terminal đôi khi không signal lại khi done, nên dùng run_in_background=true và không block.

**How to apply:** Mọi `manim -ql` render đều dùng run_in_background=true.

---

Đừng đọc quá nhiều code cũ trong drivex/ — nguồn chính là BEYOND_SELFDRIVING_ANIMATION_GUIDE.md và MICRO_ANIMATION_BIBLE.md.

**Why:** Code cũ đã bị reject vì xấu, đang làm lại từ đầu trong beyond/.

**How to apply:** Khi implement scene mới, đọc guide và bible trước, không tham khảo drivex/.

---

Mỗi file code phải "chứa đựng tâm huyết và sự sáng tạo" — guide chỉ là một phần, sáng tạo trong từng animation, chú trọng align và chi tiết.

**Why:** User muốn video chất lượng cao, không phải mechanical translation của guide.

**How to apply:** Mỗi scene thêm creative touches ngoài guide — particle effects, camera moves, micro-animations từ MICRO_ANIMATION_BIBLE.

---

Dark theme chính (BG_VOID #030508, BG_SPACE #090E1A), white theme có config để switch.

**Why:** BEYOND_SELFDRIVING guide chọn dark như Welch Labs style, user đồng ý nhưng muốn có option đổi.

**How to apply:** `beyond/config.py` THEME = "dark" | "light".

---

Mascot hơi xấu nhưng "tạm được" — không cần đầu tư quá nhiều vào mascot SVG.

**Why:** User acknowledge mascot cần cải thiện nhưng chưa phải ưu tiên hiện tại.

**How to apply:** Dùng geometric fallback trong mascots.py, không cần làm SVG custom.
