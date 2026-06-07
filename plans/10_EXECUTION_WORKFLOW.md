# 10 — Execution Workflow

> **Audience:** Claude Sonnet 4.6 implementing the rework, scene by scene.
> **Read first:** [00_MASTER_PLAN.md](00_MASTER_PLAN.md) for phases.

---

## Per-session boot-up

When you (Sonnet 4.6) open this repo with no prior session context:

1. Read [CLAUDE.md](../CLAUDE.md) at repo root.
2. Read [plans/00_MASTER_PLAN.md](00_MASTER_PLAN.md).
3. Identify what phase you're in (Phase 1 components, or Phase 2 scenes part-by-part).
4. Read the part-specific plan if you're on Phase 2.

---

## Phase 1 workflow — Component refresh

Reference: [02_COMPONENTS.md](02_COMPONENTS.md).

For each step (2.1 → 2.7):

1. Open the component file.
2. Apply edits exactly as specified.
3. Run the smoke test:
   ```powershell
   manim -ql drivex\scenes\_smoke_test.py SmokeTest
   ```
4. Open the output `.mp4` and visually verify.
5. If failure, revert the last edit and try a smaller change.

**Don't proceed to Phase 2 until the smoke test passes cleanly.**

---

## Phase 2 workflow — Per-scene rework

For each scene file (e.g., `drivex/scenes/part01/p01_s04_longtail.py`):

### Step 1 — Triage

Open these in order:
- The scene file itself
- The corresponding section in the part plan (e.g., [04_PART_INTRO_AND_PART01.md](04_PART_INTRO_AND_PART01.md) §P01-S04)
- [09_FIX_CHECKLIST.md](09_FIX_CHECKLIST.md) row for that scene
- The relevant section of the original script (`materials/scripts/script_part{N}.md`)

Skim the scene's existing code. Note:
- Does it import from `drivex.components.*`? Good — those will already use the new design system after Phase 1.
- Does it have hardcoded hex strings? Replace with constants from `colors.py`.
- Does it have `â”€` mojibake comments? Strip them.
- Does it import `sys.path.insert(...)` boilerplate at top? Often deletable.

### Step 2 — Plan the diff

In your head (or in a TodoWrite):
- List every issue from `09_FIX_CHECKLIST.md` for this scene.
- List every design-system gap (if a scene still uses old `ThoughtBubble` patterns or hardcoded dark colors, that's a gap).
- List every narrative gap from `03_NARRATIVE_AUDIT.md` (does the scene cover the *reason* the paper is mentioned?).

### Step 3 — Edit

Use `Edit` (preferred) or `Write` (only for full rewrites). Common patterns:

#### Replace dark fill with light fill

```python
# Before
fill_color="#111111", fill_opacity=1, stroke_color=COL_WHITE,

# After
fill_color=COL_DEEP_BLUE, fill_opacity=1, stroke_color=COL_NAVY,
```

#### Force axes-before-data

```python
# Before
curve = ParametricFunction(...)
self.play(Create(curve))
axes = Axes(...)
self.play(Create(axes))

# After
axes = Axes(x_range=[0, 10], y_range=[0, 1], ...).set_color(COL_NAVY)
self.play(Create(axes), run_time=0.6)
self.play(Write(axes_x_label), Write(axes_y_label), run_time=0.4)
curve = axes.plot(lambda x: ..., color=COL_BLUE)
self.play(Create(curve), run_time=1.2)
```

#### Force uniform pipeline blocks

At top of scene (or in a helper module):
```python
def _block(text, w=2.2, h=0.9, color=COL_BLUE,
           fill=COL_DEEP_BLUE):
    box = RoundedRectangle(corner_radius=0.1, width=w, height=h,
                           fill_color=fill, fill_opacity=1,
                           stroke_color=color, stroke_width=1.5)
    label = Text(text, font_size=18, color=COL_NAVY).move_to(box)
    return VGroup(box, label)

# Use:
blocks = VGroup(_block("A"), _block("B"), _block("C")).arrange(RIGHT, buff=0.5)
```

#### Clean end-of-scene

```python
# At the very end of construct():
self.play(FadeOut(VGroup(*[m for m in self.mobjects if m is not bg])),
          run_time=0.5)
self.wait(0.2)
```

Or explicitly enumerate:
```python
self.play(FadeOut(VGroup(title, content_a, content_b, mascot, bubble, footnote)),
          run_time=0.5)
self.wait(0.2)
```

#### Single bubble per mascot

```python
# WRONG — two bubbles at once
b1 = PIBubble(pi, "Why?")
self.play(b1.get_pop_animation())
b2 = PIBubble(pi, "How?", position=DOWN+RIGHT)
self.play(b2.get_pop_animation())  # ← b1 still on screen, OVERLAP

# RIGHT — one bubble that transforms
b1 = PIBubble(pi, "Why?")
self.play(b1.get_pop_animation())
self.wait(1.2)
b2 = PIBubble(pi, "How?")  # same position by default
self.play(ReplacementTransform(b1, b2))
self.wait(1.2)
self.play(FadeOut(b2))
```

### Step 4 — Render and verify

```powershell
manim -ql drivex\scenes\part01\p01_s04_longtail.py P01S04LongTail
```

Open the output `.mp4`. Watch the entire scene at normal speed. Check:
- White background
- All text in English, ≥ 22pt
- No overlap at any frame
- Bubbles tight on text
- Axes drawn before data (where applicable)
- Scene ends clean

### Step 5 — Mark done

In the part plan file, tick the scene's checkbox. Move on.

---

## When stuck

### "I can't render — manim errors"

- Check that `manim` is callable from cwd. The README says base conda env, NOT `manim_env`.
- If LaTeX errors: scene uses `MathTex` and LaTeX path isn't set. Restart shell.

### "Layout still overlaps and I've tried everything"

- Take a screenshot at the problematic timestamp.
- Read the `09_FIX_CHECKLIST.md` row again — maybe a fix was missed.
- Try the "fade the older mobject before showing the new one" rule (U10) — it solves more problems than spatial nudging.
- If still stuck after 2 attempts, leave a `# TODO(layout):` comment and surface the issue back to the user.

### "The narrative drifts from the script"

- Re-read the script chunk in `materials/scripts/script_part{N}.md`.
- Re-read [03_NARRATIVE_AUDIT.md](03_NARRATIVE_AUDIT.md) — the "reason this paper is named" section.
- Add a `# CREATIVE CHOICE:` comment if you're deliberately deviating.

### "Should this be one scene or two?"

Default: keep the existing file structure. Splitting scenes mid-rework is a big change — discuss with user first.

---

## Don't do

- Don't rewrite `drivex_white/`. It's reference only.
- Don't add new component files unless the existing ones genuinely can't accommodate.
- Don't add docstrings longer than one line. The user prefers terse code.
- Don't write `Co-Authored-By` lines or AI signatures in code or comments.
- Don't run `git commit` unless explicitly asked.
- Don't render at `-qh` or `-qk` until the user signs off `-ql`.
- Don't delete the `spec_prompts/` directory or any review file — they are history.

---

## Communication with the user

After each scene rework, in your text response (NOT in code comments):

- 1 sentence: what you did.
- 1–2 lines: what you noticed (e.g., "fixed axes-before-data; verified bubble fits text").
- If you made a creative choice, mention it.
- If you got stuck, ask 1 specific question.

That's it. The user reads the diff for everything else.

---

## Phase progression

| Phase | Done when |
|---|---|
| Phase 1 | All 7 component edits made; smoke test renders cleanly |
| Phase 2 — Intro | All 3 scenes pass DS checklist |
| Phase 2 — Part 1 | All 9 scenes pass + per-part user sign-off |
| Phase 2 — Part 2 | All 12 scenes + sign-off |
| Phase 2 — Part 3 | All 14 scenes + sign-off |
| Phase 2 — Part 4 | All 10 scenes + sign-off |
| Phase 2 — Part 5 | All 9 scenes + sign-off |
| Phase 3 | All render scripts updated; `render_all_final.ps1` works |
| Phase 4 | (Deferred — voiceover hookup; separate plan) |
