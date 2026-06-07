# 01 — Design System

> Single source of truth for visuals. Every scene must conform.

---

## 1. Background

| Context | Background |
|---|---|
| Body scene (any explanatory content) | **Pure white `#FFFFFF`** |
| Part title card (intro to a part) | **Deep navy `#0F172A`** — used as a deliberate "breath mark" between parts |
| Intro hook scene `I02Hook` | Navy is acceptable for emotional emphasis |
| Grand finale (P05-S08, P05-S09) | Navy → white transition is acceptable |

Use `BG_DARK = "#FFFFFF"` for the default. Title cards override `self.camera.background_color` to navy explicitly.

**Transitions between parts** = deliberate dark frame (navy) → white. Don't transition in the middle of a part.

---

## 2. Color palette (white-theme)

Defined in [drivex/components/colors.py](../drivex/components/colors.py). Always import — never hardcode hex.

### Core (already defined, white-theme)

| Constant | Hex | Usage |
|---|---|---|
| `BG_DARK` | `#FFFFFF` | Body scene background |
| `BG_BLACK` | `#FFFFFF` | (alias for white — kept so older scenes don't break) |
| `BG_NIGHT` | `#FFFFFF` | (alias) |
| `COL_NAVY` | `#334155` | Default text, headers — slate-navy, not pure black |
| `COL_BLUE` | `#3B82F6` | Accents, arrows, highlights |
| `COL_GOLD` | `#F59E0B` | Emphasis, key terms, quote text |
| `COL_LIGHT_BLUE` | `#BFDBFE` | Soft info-box fill |
| `COL_WHITE` | `#334155` | (alias for navy — used by older scenes that say "white text") |
| `COL_RED` | `#EF5350` | Warnings, ✗ marks |
| `COL_GREEN` | `#4ADE80` | Success, ✓ marks |
| `COL_PURPLE` | `#A78BFA` | VLA / neural model accents |

### Part-specific

| Constant | Hex | Used in |
|---|---|---|
| `COL_INFRA_ORANGE` | `#FB923C` | Part 3 — infrastructure / RSU |
| `COL_ROAD_GRAY` | `#94A3B8` | Part 3 — road geometry |
| `COL_SENSOR_CYAN` | `#06B6D4` | Part 3 — sensor beams |
| `COL_INT8_GREEN` | `#34D399` | Part 4 — quantization / efficiency wins |
| `COL_FP32_RED` | `#F87171` | Part 4 — heavy/expensive |
| `COL_ENERGY_YELLOW` | `#FBBF24` | Part 4 — compute cost |

### Soft fills (for boxes on white BG)

| Constant | Hex | Use |
|---|---|---|
| `COL_DEEP_PURPLE` | `#E9D5FF` | Light purple box fill (neural net "brain" boxes) |
| `COL_DEEP_GREEN` | `#DCFCE7` | Light green box fill (positive / accept) |
| `COL_DEEP_BLUE` | `#DBEAFE` | Light blue box fill (info / neutral) |
| `COL_GRAY_FILL` | `#F1F5F9` | Placeholder, subtle separator fill |
| `COL_DANGER_FILL` | `#FECACA` | Light red box fill (warning) |
| `COL_SOFT_PURPLE` | `#C4B5FD` | Stronger purple text on white |

### To add (Part 5)

Add to `colors.py`:

```python
# ── Part 05 specific ────────────────────────────────────────────
COL_PEDESTRIAN = "#F39C12"   # human figures
COL_ROBOT_TEAL = "#1ABC9C"   # delivery robots, quadrupeds
COL_SIM_PURPLE = "#9B59B6"   # MetaUrban / UrbanSim simulation
COL_MESH_GRAY = "#7F8C8D"    # mesh / collision geometry
```

### UCLA brand (use sparingly — title cards only)

| Constant | Hex |
|---|---|
| `UCLA_BLUE` | `#2774AE` |
| `UCLA_GOLD` | `#FFD100` |

---

## 3. Typography

| Element | Font | Size | Color |
|---|---|---|---|
| Scene title (top of body scene) | Latin Modern Roman, bold | 30 | `COL_NAVY` |
| Body paragraph | Latin Modern Roman | 22–26 | `COL_NAVY` |
| Box label | Latin Modern Roman | 18–22 | `COL_NAVY` or part-color |
| Caption / sub-label | Latin Modern Roman | 14–16 | `COL_NAVY` 70% opacity |
| Quote (emphasis) | Latin Modern Roman, italic | 24–28 | `COL_GOLD` |
| Math (`MathTex`) | LaTeX default | 22+ | `COL_NAVY` |
| Code/mono | Latin Modern Mono if available; else default mono | 16 | `COL_NAVY` |

> **Never go below 22pt** for body text. Latin Modern has letter-spacing artifacts at small sizes (per README troubleshooting note).

Use `Text(...)` for prose. Use `MathTex(...)` for symbols (`L_{rec}`, `O(n^2)` etc.).

---

## 4. Bubbles (THE big change)

Current `ThoughtBubble` has two structural problems:
1. Minimum width 3.2u and minimum height 1.5u, regardless of content. A short string like "I see." gets the same gigantic box as a 5-line paragraph.
2. Dark fill (`#111111`, `#0D1B2E`) — designed for a dark BG, looks heavy on white.

### New bubble spec

```
┌─ TightBubble (replaces ThoughtBubble) ─────────────┐
│  Fill: light, semi-opaque                          │
│    PI:  #DBEAFE (light blue, 92% opacity)          │
│    CAR: #FEF3C7 (light gold,  92% opacity)         │
│  Border: 1.5pt, color = mascot's accent            │
│    PI:  COL_BLUE  (#3B82F6)                        │
│    CAR: COL_GOLD  (#F59E0B)                        │
│  Text color: COL_NAVY (#334155)                    │
│  Padding: 0.30u horizontal, 0.18u vertical         │
│  Corner radius: 0.18u                              │
│  Tail: small triangle, same fill+border, points    │
│        toward the mascot's mouth/face anchor       │
└────────────────────────────────────────────────────┘
```

### Sizing rule

```python
text_w = label.width
text_h = label.height
pad_x, pad_y = 0.30, 0.18
bubble_w = text_w + pad_x * 2
bubble_h = text_h + pad_y * 2
# NO minimum-width clamping.
```

### Tail rule

Tail is a small filled triangle (~0.15u wide at base, ~0.25u tall) attached to the bubble edge nearest the mascot. It must not cover any text. If the bubble is positioned `UP+RIGHT` of the mascot, the tail goes on the bubble's bottom-left corner pointing down-left.

### Behavior rules

- **One PI bubble visible at a time.** Show, hold (≥ 1.0s), fade out. Don't pop a second bubble next to a still-visible first one.
- **Bubbles must not overlap any mobject** that's currently on screen. If geometry is tight, move the bubble or fade other content first.
- **Position consistently within a scene.** From review #1: "thay vì hiện box của pi theo sequence và lần lượt nhiều vị trí khác nhau thì chỉnh cho nó 1 vị trí box thôi, chỉ là ẩn hiện." — pick one anchor per scene.
- **Multi-line text:** allowed, but use `Text("line1\nline2", line_spacing=0.4)`. The bubble auto-grows.

### API to keep

Replace existing `PIBubble` and `SpeechBubble` with thin wrappers around the new `TightBubble`:

```python
class PIBubble(TightBubble):
    """Bubble styled for PI mascot (curious questioner)."""
    def __init__(self, target, text, **kw):
        kw.setdefault("border_color", COL_BLUE)
        kw.setdefault("fill_color", "#DBEAFE")  # light blue
        kw.setdefault("text_color", COL_NAVY)
        super().__init__(target, text, **kw)

class SpeechBubble(TightBubble):
    """Bubble styled for CAR mascot (guide)."""
    def __init__(self, target, text, **kw):
        kw.setdefault("border_color", COL_GOLD)
        kw.setdefault("fill_color", "#FEF3C7")  # light gold
        kw.setdefault("text_color", COL_NAVY)
        super().__init__(target, text, **kw)
```

---

## 5. Mascots

### Identity

| Mascot | Role | Anchor color | When to use |
|---|---|---|---|
| **PI** (`PiMascot`) | Curious questioner — asks "why?", "how?", expresses confusion | `COL_BLUE` | At the start of a topic; when raising the *question* the next animation answers |
| **CAR** (`CarMascot`) | Guide — answers, narrates, transitions | `COL_GOLD` | When stating a result, summarizing, or transitioning |

PI asks → animation reveals → CAR confirms / summarizes. Use this rhythm sparingly (not every scene).

### Visual style (white BG)

PI:
- Round body, navy outline (1.5pt)
- Body fill: light blue `#BFDBFE` or soft cream
- Eyes: navy dots
- Small `π` symbol on body

CAR:
- Side-view car silhouette
- Body fill: navy `#334155` or UCLA blue `#2774AE`
- Stroke: 2pt navy
- Roof, windows, wheels visible

The current geometric fallback in `mascots.py` is fine. The user said: "code chỉ cần add đại 1 dummy image là được." So *don't* over-invest in custom SVGs; keep it functional.

### Sizing

| Use | Height (Manim units) |
|---|---|
| Title card / hero shot | 1.6 |
| Speaking in body scene | 1.0 |
| Background presence | 0.7 |

---

## 6. Layout rules

### Roadmap strip (mini, bottom of part title card)

5 dots on a horizontal line, current part highlighted gold.

**Critical:** zigzag labels (alternating up/down) caused recurring overlaps with body content. Two acceptable solutions:

1. **Dots only** (no labels) for the in-body version. Labels appear only in the dedicated `I03Roadmap` scene.
2. If labels are needed, **place them all below the spine** at uniform offset, with body content kept at least 1.0u above the spine.

Default to (1) unless the scene is specifically about the roadmap.

### Pipelines / horizontal block diagrams

- Use `VGroup(...).arrange(RIGHT, buff=0.6)` for spacing — never eyeball.
- Arrows: `Arrow(box1.get_right(), box2.get_left(), buff=0.05)` — short buff so arrow visibly touches both boxes.
- All blocks the same `height` and `width` unless they semantically differ. Use a helper: `def _pill(text, w=2.2, h=0.9, color=COL_BLUE): ...`.

### Charts / distributions

- Build axes first: `axes = Axes(...)`
- `self.play(Create(axes))`
- Then plot data on top.
- Label both axes.
- For long-tail / power-law charts, use a `ParametricFunction` and label the curve, not just the dots.

### Bullet lists

- Left-align all bullets to the same x.
- 0.35u line gap.
- Use `•` (BULLET) — not `*`. In Manim Text, `•`.

### Empty space

3B1B style breathes. Don't fill every quadrant. Center the focal element; let margins exist.

---

## 7. Animation patterns

| Pattern | Use |
|---|---|
| `Write(text, run_time=0.8–1.2)` | Title or quote — typewriter feel |
| `FadeIn(obj, shift=UP*0.15, run_time=0.4)` | Body element appearing |
| `Create(line_or_arrow, run_time=0.4)` | Drawing a line, arrow, or axis |
| `GrowFromCenter(obj, run_time=0.4)` | Compact element popping in |
| `LaggedStart(*[...], lag_ratio=0.15)` | Cascade of similar elements |
| `Transform(a, b)` / `ReplacementTransform(a, b)` | Diagram morphs into its next state |
| `FadeOut(VGroup(*all_transient), run_time=0.5)` | End-of-scene cleanup — ALWAYS run before scene ends |

**Default `run_time`** is 0.4–0.6s for short reveals, 0.8–1.2s for typewritten text, 1.5s for hero animations.

`self.wait(0.5)` between major beats. `self.wait(1.0–1.5)` after a key takeaway.

---

## 8. End-of-scene checklist (the "merge cleanup")

Every scene ends with:

```python
self.play(
    FadeOut(VGroup(*[m for m in self.mobjects if not isinstance(m, Rectangle) or m is not bg]),
            run_time=0.5)
)
self.wait(0.2)
```

Or more conservatively, fade specific groups:

```python
self.play(FadeOut(VGroup(title, content, bubble, mascot)), run_time=0.5)
self.wait(0.2)
```

**No scene should leave residual text on screen at the end.** This was a recurring bug (P01-S06, P01-S08, P02-S03 all reappeared things at the end).

---

## 9. Checklist for review

When auditing a scene visually:

- [ ] White background (or correct deliberate exception)
- [ ] All text in English
- [ ] Bubble sized to text, not text floating in oversized rect
- [ ] Single bubble visible at a time per mascot
- [ ] No overlap at any frame
- [ ] Axes drawn before data
- [ ] All transient mobjects faded out at end
- [ ] Scene end frame matches scene-start of the *next* scene (BG color, no leftover content)
