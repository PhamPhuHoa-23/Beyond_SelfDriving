# CODEX SUPER PROMPT - Beyond Self-Driving Full Visual Rebuild

You are Codex working in:

`c:\Users\admin\Downloads\ML\Lab01_3B1B`

Project: `beyond/`, a 3Blue1Brown-style Manim tutorial for UCLA Mobility Lab's ICCV 2025 tutorial "Beyond Self-Driving".

The current problem is not a small alignment pass. The whole video flow feels too text-heavy, static, and visually underpowered. Your job is to rebuild the scenes into a more cinematic, direct, colorful, and intuitive animated explanation while keeping every scene renderable.

This prompt overrides the old priority-list mindset. Do not prioritize only a few scenes. Treat every scene as important.

---

## 0. Mission

Make the full video feel like a real animated tutorial, not slides.

Every scene must answer:

1. What breaks?
2. What changes?
3. What does the viewer see happen?
4. What number anchors the claim?
5. Why does it matter for AV safety?

If a scene is mostly text, rebuild it into visual objects, motion, diagrams, timelines, maps, agents, sensors, packets, occlusion masks, uncertainty clouds, charts, or before/after comparisons.

If a scene has overlapping boxes, stiff animation, half-written text captures, or cluttered labels, rewrite the layout instead of nudging positions forever.

---

## 1. Non-Negotiables

Do not edit:

- `beyond/components/`
- `beyond/config.py`
- `drivex/`
- `drivex_white/`
- `materials/`
- `plans/`
- `spec_prompts/`
- `README.md`
- `requirements.txt`

In scope:

- `.py` files under `beyond/scenes/`
- `CODEX_PROMPT.md` only if the user explicitly asks to update this prompt again

3D restrictions:

- `beyond/scenes/intro/i02_the_hook.py`
- `beyond/scenes/part02/p02_s04_occlusion.py`
- `beyond/scenes/part05/p05_s07_living_city.py`

Do not change their renderer or 3D geometry. Overlay text, timing, and fixed-frame UI can be improved.

Frozen rule:

- If a scene has `# FROZEN` in its header, do not edit it. Still render/check it and record visual risks.

Visible text rules:

- Use ASCII visible text only.
- Use `->`, not Unicode arrows.
- Use `-`, not em dash.
- Use `[OK]`, `[!]`, `[*]`, not check/warning/star glyphs.
- No `Text(..., font_size=N)` below `SIZE_MICRO`.

Color rules:

- Use colors already exported by `beyond/components/colors_dark.py`.
- Do not invent random hex colors in scene files.
- Do not create a one-color monotone deck. Each part should have accent color plus supporting contrast: GOLD for numbers, RED_ALERT for failures, GREEN_SIGNAL for fixes, CYAN_NEON/ORANGE_INFRA for sensor distinction, TEXT_DIM/TEXT_GHOST for secondary layers.

End rules:

- End every scene cleanly.
- No orphaned mobjects.
- Final readable beat must hold long enough to read.

---

## 2. Required First Reads

Read these first, no exceptions:

```powershell
Get-Content beyond/config.py
Get-Content beyond/components/colors_dark.py
Get-Content beyond/components/base_scene.py
Get-Content beyond/components/animations.py
Get-Content beyond/components/pipeline_block.py
Get-Content beyond/components/__init__.py
```

Then inspect all scene files:

```powershell
rg --files beyond/scenes -g "*.py"
```

Also inspect the project guides:

```powershell
Get-Content BEYOND_SELFDRIVING_ANIMATION_GUIDE.md
Get-Content MICRO_ANIMATION_BIBLE.md
Get-Content 5_PART_GUIDE.md
Get-Content ENHANCEMENT_PROMPT.md
Get-Content EXECUTION_PROMPTS.md
```

Use `rg`, not slow manual searching.

---

## 3. Source_manim_reference Reuse Mandate

There is a local folder:

`Source_manim_reference/`

It contains reference Manim source that can greatly improve the visual language of this project.

You must inspect it before rewriting scenes.

Run:

```powershell
rg --files Source_manim_reference
rg -n "class |def |Scene|ThreeDScene|MovingCameraScene|always_redraw|ValueTracker|Updater|Transform|ReplacementTransform|TransformMatching|LaggedStart|AnimationGroup|Succession|Flash|Indicate|Circumscribe|ShowPassingFlash|MoveAlongPath|ParametricFunction|Axes|NumberPlane|StreamLines|Surface|VMobject|VGroup" Source_manim_reference
```

Create an inventory in your working notes before editing scenes:

1. List every major reference folder.
2. List important scene classes.
3. List reusable helper functions/classes.
4. List animation idioms worth stealing conceptually.
5. List visual motifs worth adapting: camera moves, trails, graph morphs, packet flow, transformations, handwritten math reveals, tiling, geometry diagrams, overlays, color rhythm, value trackers, updaters, morphing labels, dynamic braces, axes choreography.
6. For each candidate, record the source path and line number.

Important legal/engineering rule:

- Do not waste time rebuilding from scratch when reuse is allowed and technically safe.
- If the code/assets are clearly permissive, user-owned, or already intended for reuse in this project, copy/adapt the smallest useful unit and cite the file path in your notes.
- If a file says "do not copy", has unclear rights, or is not safe to reuse literally, do not paste it verbatim. Instead, extract the idea, animation pattern, layout strategy, or mathematical structure and implement an original equivalent inside the target scene.
- Never let "do not copy" stop you from learning from the reference. It only stops literal copying. The goal is fast reuse of concepts, structure, and reusable permitted snippets.

Deliverable from this phase:

Create a short `SOURCE_REFERENCE_AUDIT.md` in the workspace only if the user allows docs edits. If docs edits are not allowed, include the audit in your final response. The audit must have:

```text
Reference Path | What It Contains | Reusable As-Is? | Adapt-Only Ideas | Target Scenes
```

Do this before scene rewrites.

---

## 4. Full Scene Inventory

Do not prioritize only selected scenes. Inventory all scenes.

Run:

```powershell
rg -n "^class " beyond/scenes
rg -n "Text\\(|MarkupText\\(|Tex\\(|MathTex\\(|Paragraph\\(" beyond/scenes
rg -n "font_size\\s*=\\s*SIZE_MICRO\\s*-|font_size\\s*=\\s*[0-9]+" beyond/scenes
rg -n "→|—|✓|⚠|★|∞|·|×|≈|≤|≥" beyond/scenes
rg -n "#[0-9A-Fa-f]{6}" beyond/scenes
rg -n "\\.animate\\([^\\n]*\\).*\\.animate|self\\.play\\([^\\n]*\\.animate[^\\n]*,\\s*[^\\n]*\\.animate" beyond/scenes
rg -n "AddTextLetterByLetter|Write\\(" beyond/scenes
rg -n "to_edge\\(|to_corner\\(|move_to\\(|shift\\(" beyond/scenes
rg -n "Axes\\(|BarChart\\(|plot\\(" beyond/scenes
```

Make a working table:

```text
Scene | Class | Current visual problem | Proposed visual rebuild | Reference ideas to adapt | Render status
```

Every scene must be classified into one of these rebuild types:

1. Problem-first visual
2. Before/after comparison
3. Pipeline with moving packets
4. Timeline/evolution
5. Chart with animated data
6. City/intersection/agent simulation
7. Method gallery with contribution cards
8. Bridge/summary cinematic recap
9. Title card/minimal cinematic identity

---

## 5. Design Standard

Every scene must become visual-first.

Bad:

- Five bullets with tiny text.
- Boxes connected by arrows with no motion.
- Method names without visual action.
- A title plus text blocks.
- Labels touching boxes/arrows.
- Half-written text visible in sampled frames.
- Dimming old sections but leaving them visually competing.

Good:

- A problem appears first as a failure visual.
- A solution changes the scene physically.
- Packets move along arrows.
- Occlusion masks reveal hidden agents.
- Sensor cones overlap and fuse.
- Data appears after axes.
- Numbers bounce.
- Before and after states are visually different.
- Text is short and anchored to an object.
- The viewer can understand the idea from the picture before reading.

Every scene should contain at least three of these:

- moving packet/dot/beam/path
- before/after split
- failure state in RED_ALERT
- fix state in GREEN_SIGNAL
- key number in GOLD
- camera or group movement
- morph/transform between concepts
- visible AV/city/sensor/agent object
- chart/axis/metric
- PiMascot question only when useful
- final takeaway

---

## 6. Layout Standard

Canvas:

- width about 14.22 units
- height about 8.0 units

Safe bounds:

- x within `[-6.8, 6.8]`
- y within `[-3.6, 3.6]`

Zones:

- title zone: `y > 2.6`
- content zone: `-3.4 < y < 2.5`
- footnote zone: `y < -3.3`

Rules:

- Do not stack title, subtitle, badges, and diagrams in the same vertical band.
- Do not put labels directly on arrow shafts.
- Minimum gap between text and geometry: 0.16 units.
- If a label competes with an object, move it outside or replace it with a small color-coded legend.
- If three or more boxes form a pipeline, use `.arrange(RIGHT, buff=0.55)` or an equivalent calculated layout.
- Use `next_to(..., buff=0.18 or higher)` for labels.
- Avoid manual per-box coordinates unless the scene is a deliberate map/simulation.
- If a section is done, fade it out fully or move it into a clear background layer. Do not leave ghost content behind a chart unless it is intentionally a watermark.

---

## 7. Animation Standard

Prefer:

- `FadeIn`
- `Create`
- `GrowFromCenter`
- `ReplacementTransform`
- `TransformMatchingShapes`
- `LaggedStart` with readable timing
- `AnimationGroup`
- `MoveAlongPath`
- `ShowPassingFlash`
- `Flash`
- `Indicate`
- short pulse/bounce on key numbers
- updaters/value trackers when they make the concept clearer

Avoid:

- long `Write` or `AddTextLetterByLetter` for important readable text
- simultaneous `.animate` calls on the same object inside one `self.play`
- decorative motion that does not explain anything
- labels fading in while geometry underneath is still moving into them

If a frame sampled at 35%, 60%, or 85% catches half-written text, change that text reveal to `FadeIn` or `ReplacementTransform`.

Every pipeline needs motion:

```python
pkt = Dot(radius=0.055, color=arrow_color)
pkt.move_to(blocks[0].get_right())
path = Line(blocks[0].get_right(), blocks[-1].get_left())
self.play(MoveAlongPath(pkt, path, run_time=0.45), FadeOut(pkt, run_time=0.1))
```

Every key number needs emphasis:

```python
self.play(number_mob.animate(run_time=0.25).scale(1.18))
self.play(number_mob.animate(run_time=0.20).scale(1 / 1.18))
```

---

## 8. Narrative Standard

For each scene, rewrite toward this structure:

```text
Beat 1: Failure or question
Beat 2: Visual mechanism
Beat 3: Evidence number
Beat 4: Safety takeaway
```

Method/paper labels should be short:

```text
[Method] - [one contribution]; [one number]
```

Examples:

```text
V2VNet - graph fusion; +8 AP
DiscoNet - distillation; less bandwidth
V2X-ViT - attention fusion; robust under delay
AutoVLA - VLA driving policy; closed-loop planning
QuantV2X - compressed V2X; 300x smaller
UrbanSim - GPU city sim; 180 days -> 3 hours
CityWalker - pedestrian corpus; 227 cities
```

If the exact number is unknown, read `materials/scripts/` or the relevant paper notes already in the repo. Do not invent scientific claims.

---

## 9. Scene Rebuild Workflow

Work scene by scene across all scene files.

For each scene:

1. Read the scene file.
2. Read relevant script/notes from `materials/scripts/` if needed.
3. Check reference audit for reusable/adaptable patterns.
4. Decide the visual rebuild type.
5. Patch the scene.
6. Render.
7. Extract frames.
8. View frames.
9. Fix overlap/clutter/ugly timing.
10. Re-render until clean.
11. Mark the scene done in your working notes.

Render:

```powershell
manim -ql --disable_caching "beyond/scenes/.../file.py" ClassName
```

3D render:

```powershell
manim -ql --renderer=opengl --disable_caching "beyond/scenes/.../file.py" ClassName
```

Extract frames:

```powershell
C:\Users\admin\miniconda3\python.exe -c "import cv2, os, numpy as np; p=r'media/videos/FOLDER/480p15/CLASS.mp4'; cap=cv2.VideoCapture(p); fps=cap.get(cv2.CAP_PROP_FPS); frames=cap.get(cv2.CAP_PROP_FRAME_COUNT); dur=frames/fps if fps else 0; out=os.path.dirname(p); imgs=[]; print('dur',dur);
for t in [0.35,0.60,0.85]:
    cap.set(cv2.CAP_PROP_POS_MSEC,dur*t*1000); ret,frame=cap.read(); print(t,ret)
    if ret:
        cv2.imwrite(os.path.join(out,f'check_{int(t*100)}.png'),frame); imgs.append(frame)
cap.release()
if imgs: cv2.imwrite(os.path.join(out,'contact_check.png'), np.hstack(imgs))"
```

Then view `contact_check.png`.

Do not call a scene done until the actual frames look clean.

---

## 10. Strong Rebuild Targets By Part

Intro:

- Must feel like a hook, not a syllabus.
- Use motion, contrast, and a clear "why beyond self-driving?" visual.
- Roadmap should be a living map/timeline, not five static labels.

Part 1:

- Show the AV stack as a machine with moving perception/planning/control signals.
- Show foundation models as compression of capability, not text.
- VLA gallery should feel like a visual museum of methods with contribution cards.
- AutoVLA should show closed-loop sense-think-act motion.

Part 2:

- Show cooperative perception through occlusion removal.
- Use sensor beams, hidden objects, V2X packets, fusion maps.
- Related works should be a visual evolution, not a name list.
- Questions should be animated as three real bottlenecks.

Part 3:

- Simulation and digital twins must look spatial.
- Calibration/localization should move coordinate frames into alignment.
- Kalman should visibly reduce uncertainty.
- CooperFuse should show uncertainty-aware fusion without label collisions.
- OpenCDA should show ecosystem modules, not just bullet points.

Part 4:

- Efficiency scenes must show compression, latency, bandwidth, annotation cost as physical transformations.
- QuantV2X should visibly shrink packets.
- Latency should be a chain with timing pulses.
- Summaries should use visual scorecards, not text slabs.

Part 5:

- Physical AI scenes must look like cities with agents.
- MetaUrban/UrbanSim/Vid2Sim should show generation/transformation, not terminal text only.
- CityWalker/PedGen should show pedestrian diversity.
- Final summary should feel like a cinematic closing montage.

---

## 11. Quality Gate

Before marking any scene done:

```text
[ ] Scene renders at -ql
[ ] 35/60/85 frames viewed
[ ] No clipped text/object
[ ] No overlap between labels, boxes, arrows, charts
[ ] No half-written important text in sampled frames
[ ] At least one visual mechanism, not just bullets
[ ] At least one number in GOLD or similarly prominent style
[ ] Problem/fix/evidence/takeaway are visible
[ ] Motion explains the idea
[ ] Scene has enough color contrast
[ ] Old sections do not compete with new sections
[ ] No visible Unicode font-risk glyphs
[ ] No font below SIZE_MICRO
[ ] No hardcoded new hex colors
[ ] No orphaned mobjects at end
[ ] self.close() remains the final line
```

If any box/label overlaps, rebuild the layout. Do not just say "acceptable".

If the scene still looks like a PowerPoint slide, rebuild it again.

---

## 12. Final Report Expected

When done, report:

```text
Changed files
Rendered scenes
Scenes visually checked
Reference patterns reused or adapted from Source_manim_reference
Known remaining risks
Frozen/3D-safe scenes intentionally left structurally untouched
```

Keep the report concise, but include enough file paths for the user to verify.

