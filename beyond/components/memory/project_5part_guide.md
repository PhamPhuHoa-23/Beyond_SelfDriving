---
name: project-5part-cinematic-guide
description: Full cinematic scene-by-scene guide for "Beyond Self-Driving" — emotional arc, hold times, iconic visuals per scene
metadata:
  type: project
---

5_PART_GUIDE.md là kịch bản sáng tạo đầy đủ (không phải spec kỹ thuật). Key facts:

**Sợi chỉ đỏ:** Mỗi phần kết thúc bằng câu hỏi mới — giới hạn → vượt giới hạn.

**Iconic scenes cần làm xuất sắc nhất:**
- I-02: The Hook — radar gravitational waves (CẢNH ĐẶC TRƯNG NHẤT)
- P1-04: Long-tail power-law curve (ĐẸP NHẤT Part 1) — icon positioning bug đã fix
- P2-04: Occlusion với radar waves (75s cinematic) — pedestrian = stick figure, quote split 2 lines
- P4-03: CooPre masked voxel puzzle (WOW của Part 4) — FadeIn+animate conflict đã fix
- P5-07: Living City finale (KHÔNG GIỚI HẠN render time) — "A safer world." hold 3s

**Hold times bắt buộc (verified in code):**
- "So we taught them to cooperate." → 3.0s (i02)
- "Cooperation is a physics solution..." → 2.5s (p02_s04)
- "We need generalist experience..." → 2.5s (p01_s04)
- "All three share the same fundamental flaw." → 1.8s wait (p01_s03)
- "The world is compositional..." → 3.0s (p05_s03)
- "A safer world." → 3.0s (p05_s07)
- "Not yet." → 2.0s (p02_s03)

**Beyond/ folder structure:**
- 61 scene files + 2 test files
- All Part title cards: forge effect + ambient background + Write(quote) + 2.0-2.5s hold
- All body scenes: BeyondScene base with ambient particles, scene_open/close
- All closing questions/bridges: Write() not FadeIn()
- All wait times before close(): 1.5s minimum

**Polish session completed 2026-05-21:**
- Fixed FadeIn+animate conflicts in p01_s01, p02_s03, p04_s03
- Fixed icon positioning bug in p01_s04 (pre-compute ghost targets)
- Added stick figure pedestrian + ghost materialization in p02_s04
- COT typewriter pacing improved in p01_s08
- Ambient neural net background in p01_s01_title
- Batch: 7 files wait(1.0-1.2) → wait(1.5)
- Quote reveals: Write() across all title cards P2-P5

**Why:** Guide là nguồn chính để biết intent của từng cảnh. Manim code triển khai từ guide này.
