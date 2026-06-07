# 02 — Component Rework

> Phase 1 deliverable: refresh `drivex/components/` so all scenes can rely on the new design system without per-scene workarounds.

Order matters — do these in sequence; later edits depend on earlier ones.

---

## 2.1 — `drivex/components/colors.py`

**Status today**: white-theme palette already in place.

### Add (Part 5)

Append before "UCLA brand" section:

```python
# ── Part 05 specific ────────────────────────────────────────────
COL_PEDESTRIAN = "#F39C12"   # human figures
COL_ROBOT_TEAL = "#1ABC9C"   # delivery robots, quadrupeds
COL_SIM_PURPLE = "#9B59B6"   # MetaUrban / UrbanSim simulation
COL_MESH_GRAY = "#7F8C8D"    # mesh / collision geometry
```

### Add (bubble fills)

Append in the "Secondary accents" block:

```python
# Bubble-specific (light fills for white BG)
COL_BUBBLE_PI_FILL = "#DBEAFE"   # PI mascot bubble background
COL_BUBBLE_CAR_FILL = "#FEF3C7"  # CAR mascot bubble background
```

### Add (part-transition navy)

```python
# Part-transition card (deliberate navy contrast)
BG_PART_TITLE = "#0F172A"
```

### Verify

`COL_NAVY = "#334155"` is darker enough on white (contrast ratio ~9:1). Keep.

`COL_GREEN = "#4ADE80"` is too light on white for text — keep for fills, but don't use as text color. For "success" text use `#16A34A` — add as `COL_GREEN_DARK`:

```python
COL_GREEN_DARK = "#16A34A"   # text-on-white green
COL_BLUE_DARK = "#1D4ED8"    # text-on-white blue
```

---

## 2.2 — `drivex/components/thought_bubble.py` (REWRITE)

Replace the entire file. The new `TightBubble` fits text tightly and uses light fills.

```python
# drivex/components/thought_bubble.py
# ─────────────────────────────────────────────────────────────────
# Tight-fit bubble components for white-theme tutorial.
#
#   TightBubble    — base class, fits text tightly with thin border.
#   PIBubble       — wrapper for the PI mascot (blue).
#   SpeechBubble   — wrapper for the CAR mascot (gold).
# ─────────────────────────────────────────────────────────────────

from manim import *
import numpy as np

from .colors import (
    COL_NAVY, COL_BLUE, COL_GOLD,
    COL_BUBBLE_PI_FILL, COL_BUBBLE_CAR_FILL,
)


class TightBubble(VGroup):
    """
    Speech / thought bubble that hugs its text with a small padding.
    Light fill, thin border — designed for white background.

    Parameters
    ----------
    target        : Mobject the tail points toward (mascot's body)
    text          : str | Text — bubble content
    position      : direction relative to target (e.g., UP+RIGHT)
    font_size     : int, default 22
    fill_color    : hex, default light blue
    border_color  : hex, default navy
    text_color    : hex, default navy
    pad           : (pad_x, pad_y) extra around text (default (0.30, 0.18))
    corner_radius : default 0.18
    stroke_width  : default 1.5
    buff          : gap between bubble and target (default 0.55)
    show_tail     : bool, default True
    """

    def __init__(
        self,
        target: Mobject,
        text,
        position=UP + RIGHT,
        font_size: int = 22,
        fill_color: str = "#DBEAFE",
        border_color: str = COL_NAVY,
        text_color: str = COL_NAVY,
        pad=(0.30, 0.18),
        corner_radius: float = 0.18,
        stroke_width: float = 1.5,
        buff: float = 0.55,
        show_tail: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)

        # Build label (allow caller to pass a Text already)
        if isinstance(text, str):
            label = Text(text, font_size=font_size, color=text_color,
                         line_spacing=0.45)
        else:
            label = text
            label.set_color(text_color)

        pad_x, pad_y = pad
        bw = label.width + pad_x * 2
        bh = label.height + pad_y * 2

        bubble = RoundedRectangle(
            corner_radius=corner_radius,
            width=bw,
            height=bh,
            fill_color=fill_color, fill_opacity=0.92,
            stroke_color=border_color, stroke_width=stroke_width,
        )
        label.move_to(bubble.get_center())
        bubble_grp = VGroup(bubble, label)
        bubble_grp.next_to(target, position, buff=buff)

        self.main_bubble = bubble
        self.label = label
        self.tail_shape = None

        if show_tail:
            self.tail_shape = self._make_tail(
                target, bubble, position,
                fill_color, border_color, stroke_width,
            )
            self.add(self.tail_shape)

        self.add(bubble_grp)

    def _make_tail(self, target, bubble, position,
                   fill_color, border_color, stroke_width):
        """Triangular tail pointing from bubble corner toward target."""
        # Use the bubble corner closest to the target
        anchor = bubble.get_corner(-position) * 0.7 + bubble.get_center() * 0.3
        tip = target.get_critical_point(position) * 0.4 + target.get_center() * 0.6

        direction = tip - anchor
        length = float(np.linalg.norm(direction))
        if length < 1e-6:
            d_norm = np.array([1.0, 0.0, 0.0])
        else:
            d_norm = direction / length

        perp = np.array([-d_norm[1], d_norm[0], 0.0]) * 0.10

        tail = Polygon(
            anchor + perp,
            anchor - perp,
            tip,
            fill_color=fill_color, fill_opacity=0.92,
            stroke_color=border_color, stroke_width=stroke_width,
        )
        return tail

    def get_pop_animation(self, lag: float = 0.12):
        """Tail → bubble → text."""
        anims = []
        if self.tail_shape is not None:
            anims.append(GrowFromCenter(self.tail_shape))
        anims.append(GrowFromCenter(self.main_bubble))
        anims.append(Write(self.label))
        return LaggedStart(*anims, lag_ratio=lag)


class PIBubble(TightBubble):
    """Bubble styled for PI mascot (curious questioner — blue accent)."""
    def __init__(self, target, text, **kw):
        kw.setdefault("border_color", COL_BLUE)
        kw.setdefault("fill_color", COL_BUBBLE_PI_FILL)
        kw.setdefault("text_color", COL_NAVY)
        super().__init__(target, text, **kw)


class SpeechBubble(TightBubble):
    """Bubble styled for CAR mascot (guide — gold accent)."""
    def __init__(self, target, text, **kw):
        kw.setdefault("border_color", COL_GOLD)
        kw.setdefault("fill_color", COL_BUBBLE_CAR_FILL)
        kw.setdefault("text_color", COL_NAVY)
        super().__init__(target, text, **kw)


# Back-compat alias — older scenes import ThoughtBubble directly.
ThoughtBubble = TightBubble
```

### What changed (vs. existing `thought_bubble.py`)

| Aspect | Old | New |
|---|---|---|
| Min size clamp | `max(text+pad, 3.2)` × `max(text+pad, 1.5)` | None — pure tight fit |
| Fill | Dark `#111111` / `#0D1B2E` / `#1A1200` | Light `#DBEAFE` (PI) / `#FEF3C7` (CAR) |
| Border | `#FFFFFF` / `COL_BLUE` / `COL_GOLD`, 2.5pt | Navy/blue/gold, 1.5pt |
| Default font_size | 24 | 22 |
| Tail anchor | Bubble corner exactly | Slightly inside bubble (`0.7×corner + 0.3×center`) — looks more attached |

---

## 2.3 — `drivex/components/mascots.py`

Mostly fine. Two small edits:

### Edit 1 — PI mascot for white BG

The current PI uses gold body fill (`#E8A838`) which clashes with `COL_GOLD` as bubble border. On white BG the gold body looks washed-out. Switch to a soft body with navy face:

```python
# In PiMascot.__init__, change defaults:
def __init__(self, height: float = 1.0,
             color: str = "#BFDBFE",        # was "#E8A838" — light blue body
             stroke_color: str = COL_NAVY,
             face_color: str = COL_NAVY,
             **kwargs):
```

Update `head` stroke to `stroke_color`, eyes to `face_color`, smile to `face_color`, and pi_text to `face_color`.

### Edit 2 — CAR mascot for white BG

`body_color="#2E75B6"` is OK but the white outline (`stroke_color=WHITE`) is invisible on white BG. Switch:

```python
# In CarMascot.__init__:
def __init__(self, height: float = 1.5,
             body_color: str = "#2774AE",       # UCLA blue, slightly more saturated
             window_color: str = "#BFDBFE",
             stroke_color: str = COL_NAVY,      # was WHITE
             **kwargs):
```

Replace all `stroke_color=WHITE` lines in the body with `stroke_color=stroke_color`. Wheels can keep `#222222` fill since they're dark by design.

### Add — `wave_animation` helper

For the credits scene (P05-S09 / P05-S10), the spec calls for "CAR mascot waves." Add:

```python
def wave_animation(mascot, run_time=1.0):
    """Subtle tilt-and-bounce wave gesture."""
    return Succession(
        mascot.animate(rate_func=there_and_back, run_time=run_time/2)
              .rotate(0.10).shift(UP * 0.08),
    )
```

---

## 2.4 — `drivex/components/roadmap.py`

Without reading the full file, the recurring complaint is: **labels above/below the spine alternate (zigzag) and overlap with body content**.

Two operating modes needed:

| Mode | Use | Behavior |
|---|---|---|
| `RoadmapStrip(... mini=False)` | The dedicated `I03Roadmap` scene | Full version with labels — that scene clears the rest of the canvas |
| `RoadmapStrip(... mini=True)` | Bottom of every part title card | **Dots only**, no labels. Pure spine + 5 dots, current dot gold. |

If the existing `roadmap.py` already has `mini=True`, ensure it suppresses labels entirely. If not, add a `show_labels: bool = True` parameter and respect it.

---

## 2.5 — `drivex/components/title_card.py`

Part title cards are the deliberate navy-bg breath-mark. Verify:

- `bg = Rectangle(...).set_fill(BG_PART_TITLE)` (use the new constant)
- Body text: `COL_GOLD` for title, light blue for subtitle
- `RoadmapStrip(current_part=N, mini=True)` at bottom
- Scene fades **in** from white (so previous scene's white BG matches), and fades **out** to white before the next scene starts

```python
def construct(self):
    # Open with white frame to match previous scene
    self.camera.background_color = "#FFFFFF"
    self.play(self.camera.background_color.animate.set_value(BG_PART_TITLE), run_time=0.5)
    # ... body of title card ...
    self.play(FadeOut(everything), run_time=0.5)
    self.play(self.camera.background_color.animate.set_value("#FFFFFF"), run_time=0.5)
```

(Note: in Manim, `camera.background_color` is not always animatable directly; alternative is to use a full-screen `Rectangle` and animate its fill. Whichever path works on `manim==0.20.1`, document it.)

---

## 2.6 — `drivex/components/slide_helper.py`

Verify placeholder color contrasts on white BG:

```python
placeholder = Rectangle(
    width=width, height=height,
    fill_color=COL_GRAY_FILL,   # #F1F5F9 — visible against white
    fill_opacity=1,
    stroke_color=COL_NAVY,
    stroke_width=1,
)
label = Text(rel_path, font_size=14, color=COL_NAVY).move_to(placeholder)
```

---

## 2.7 — Smoke test scene

Create `drivex/scenes/_smoke_test.py`:

```python
"""
Render: manim -ql drivex/scenes/_smoke_test.py SmokeTest
Verifies all components render cleanly on white BG.
"""
from manim import *
from drivex.components.colors import (
    BG_DARK, COL_NAVY, COL_GOLD, COL_BLUE,
)
from drivex.components.mascots import create_pi_mascot, create_car_mascot
from drivex.components.thought_bubble import PIBubble, SpeechBubble
from drivex.components.roadmap import RoadmapStrip


class SmokeTest(Scene):
    def construct(self):
        self.camera.background_color = BG_DARK

        title = Text("Smoke Test — White Theme",
                     font_size=30, color=COL_NAVY, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        # PI on the left with a question bubble
        pi = create_pi_mascot(height=1.0).shift(LEFT * 4 + DOWN * 0.5)
        self.play(FadeIn(pi))

        pi_bubble = PIBubble(pi, "Why do bubbles\nfit text now?",
                             position=UP + RIGHT)
        self.play(pi_bubble.get_pop_animation())
        self.wait(1.0)
        self.play(FadeOut(pi_bubble))

        # CAR on the right with an answer
        car = create_car_mascot(height=1.4).shift(RIGHT * 4 + DOWN * 0.5)
        self.play(FadeIn(car))

        car_bubble = SpeechBubble(car, "Tight padding\n+ thin border.",
                                  position=UP + LEFT)
        self.play(car_bubble.get_pop_animation())
        self.wait(1.0)

        # Mini roadmap at bottom
        roadmap = RoadmapStrip(current_part=2, mini=True, spine_width=8)
        roadmap.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(roadmap))
        self.wait(1.5)

        # Clean exit
        self.play(FadeOut(VGroup(title, pi, car, car_bubble, roadmap)))
        self.wait(0.2)
```

Acceptance: this scene renders, every element is readable on white, no overlaps, mascots and bubbles look intentional.

---

## Summary checklist

- [ ] 2.1 `colors.py` — add Part 5 colors, bubble fills, BG_PART_TITLE, GREEN_DARK, BLUE_DARK
- [ ] 2.2 `thought_bubble.py` — rewritten as `TightBubble`
- [ ] 2.3 `mascots.py` — PI body color, CAR stroke; add `wave_animation`
- [ ] 2.4 `roadmap.py` — mini mode = dots only
- [ ] 2.5 `title_card.py` — clean BG transition for navy → white
- [ ] 2.6 `slide_helper.py` — verify placeholder readable on white
- [ ] 2.7 `_smoke_test.py` — render and review

Once all checked, Phase 1 is done; proceed to Phase 2 (per-part scene rework).
