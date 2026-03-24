# Manim Community Documentation - Quickstart & Building Blocks

This document contains a compilation of the Quickstart and Building Blocks sections from the official Manim Community documentation. It is intended to be a searchable local resource for creating animations.

---

## 1. Quickstart

### Overview
Manim is an animation engine for precise programmatic animations. You create a `Scene` class, and inside its `construct()` method, you define what to animate.

### Starting a New Project
To start a new project with default settings, run:
```bash
manim init project my-project --default
```

### Basic Example: Animating a Circle
```python
from manim import *

class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen
```
**Render command:** `manim -pql main.py CreateCircle`
*   `-p`: Play immediately.
*   `-q`: Quality (`l` for low, `h` for high).

### Transforming a Square into a Circle
```python
class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)
        square = Square()
        square.rotate(PI / 4)
        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))
```

### Positioning Mobjects
Use `next_to` for relative positioning:
```python
square.next_to(circle, RIGHT, buff=0.5)
```
- Directions: `UP`, `DOWN`, `LEFT`, `RIGHT`, `ORIGIN`.

### Using .animate Syntax
The `.animate` syntax is a powerful way to animate any method that modifies a Mobject:
```python
self.play(square.animate.rotate(PI / 4))
self.play(square.animate.set_fill(PINK, opacity=0.5))
```

---

## 2. Manim’s Building Blocks

### Mobjects (Mathematical Objects)
Mobjects are the basic building blocks. Everything on screen is a Mobject.
- Simple shapes: `Circle`, `Square`, `Triangle`, `Rectangle`, `Arrow`.
- Complex: `Axes`, `FunctionGraph`, `BarChart`.
- `VMobject` (Vectorized Mobject): Most shapes are VMobjects, using vector graphics.

### Creating and Displaying
- `self.add(mobject)`: Immediately adds to the scene (no animation).
- `self.remove(mobject)`: Immediately removes from the scene.

### Positioning Methods
- `shift(vector)`: Moves the mobject by a certain vector (e.g., `LEFT`, `UP * 2`).
- `move_to(point)`: Moves to an absolute coordinate (relative to `ORIGIN`).
- `next_to(target, direction)`: Places relative to another mobject.
- `align_to(target, direction)`: Aligns borders.

### Styling
- `set_stroke(color, width)`: Changes the border.
- `set_fill(color, opacity)`: Changes the interior.
- `set_color(color)`: Simple color change for the whole object.

### Animations
Animations interpolate between two states of a Mobject.
- `FadeIn(mob)` / `FadeOut(mob)`: Smoothly changes opacity.
- `Create(mob)`: Draws the mobject.
- `Rotate(mob, angle)`: Rotates over time.
- `Transform(mob1, mob2)`: Morphs the points of `mob1` into `mob2`.
- `ReplacementTransform(mob1, mob2)`: Replaces `mob1` with `mob2`.

### Run Time & Wait
- `self.play(..., run_time=2)`: Sets animation duration.
- `self.wait(1)`: Pauses for a duration.

### Scenes
The `Scene` class is the container. All code must be inside the `construct()` method of a `Scene` subclass.

---

## 3. Local Technical Reference (Full)

For detailed information on specific modules, refer to these local files:

- [**Mobjects Reference**](file:///c:/Users/admin/Downloads/ML/Lab01_3B1B/materials/manim_docs/mobjects.md): Base classes, updaters, and groups.
- [**Animations Reference**](file:///c:/Users/admin/Downloads/ML/Lab01_3B1B/materials/manim_docs/animations.md): Creation, transformation, and movement.
- [**Scenes Reference**](file:///c:/Users/admin/Downloads/ML/Lab01_3B1B/materials/manim_docs/scenes.md): Play, wait, and camera controls.
- [**Geometry Reference**](file:///c:/Users/admin/Downloads/ML/Lab01_3B1B/materials/manim_docs/geometry.md): Circles, squares, lines, and arrows.
- [**Graphing Reference**](file:///c:/Users/admin/Downloads/ML/Lab01_3B1B/materials/manim_docs/graphing.md): Axes, function plotting, and coordinate systems.
- [**Text & LaTeX Reference**](file:///c:/Users/admin/Downloads/ML/Lab01_3B1B/materials/manim_docs/text.md): Text, Markup, and mathematical formulas.
- [**3D Mobjects**](file:///c:/Users/admin/Downloads/ML/Lab01_3B1B/materials/manim_docs/three_d.md): Spheres, Cubes, and 3D camera controls.
- [**SVG & Images**](file:///c:/Users/admin/Downloads/ML/Lab01_3B1B/materials/manim_docs/svg_images.md): Loading external assets and traced paths.
- [**Tables & Matrices**](file:///c:/Users/admin/Downloads/ML/Lab01_3B1B/materials/manim_docs/tables_matrices.md): Displaying structured data and linear algebra.
- [**Probability & Stats**](file:///c:/Users/admin/Downloads/ML/Lab01_3B1B/materials/manim_docs/probability.md): Sample spaces and bar charts.
- [**Utilities & Colors**](file:///c:/Users/admin/Downloads/ML/Lab01_3B1B/materials/manim_docs/utilities.md): Constants, directions, and color palettes.
- [**FAQ & Troubleshooting**](file:///c:/Users/admin/Downloads/ML/Lab01_3B1B/materials/manim_docs/faq_troubleshooting.md): Common errors and solutions.
- [**Advanced Config & CLI**](file:///c:/Users/admin/Downloads/ML/Lab01_3B1B/materials/manim_docs/advanced_config.md): `manim.cfg` and all command-line flags.
- [**Plugins**](file:///c:/Users/admin/Downloads/ML/Lab01_3B1B/materials/manim_docs/plugins.md): Extending Manim (Voiceover, Physics, etc.).
- [**Full Module Sitemap**](file:///c:/Users/admin/Downloads/ML/Lab01_3B1B/materials/manim_docs/sitemap.md): A map of the entire Manim library structure.

---

## 4. Tips for Searching Local Docs

To find what you need quickly without searching the web:
1. **Global Search**: Open the `materials/manim_docs/` folder in VS Code and press `Ctrl+Shift+F`. Type the class name (e.g., `Matrix`) to see all definitions and examples.
2. **Method Search**: Once in a file (e.g., `mobjects.md`), use `Ctrl+F` to find specific methods like `shift` or `scale`.
3. **Syntax Reference**: Keep the [**Cheat Sheet**](#2-cheat-sheet-quick-reference) above open for 90% of your daily needs.

---

## 5. Online Reference (Absolute Full)

If you need to search for a very specific class not covered here, refer to the [Full Online Reference](https://docs.manim.community/en/stable/reference.html).

---
*Source: https://docs.manim.community/en/stable/*
