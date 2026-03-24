# Mobjects Reference

Mobjects (Mathematical Objects) are the base classes for all objects that can be displayed in Manim.

## Core Classes

### `Mobject`
Base class for all objects on screen.
- **Methods**:
    - `add(*mobjects)`: Adds mobjects as sub-mobjects.
    - `remove(*mobjects)`: Removes sub-mobjects.
    - `shift(*vectors)`: Moves the mobject by a vector.
    - `move_to(point_or_mobject)`: Moves to a coordinate or another mobject's center.
    - `next_to(mobject, direction=RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER)`: Positions relative to another mobject.
    - `align_to(mobject, direction=UP)`: Aligns a border with another mobject's border.
    - `rotate(angle, axis=OUT, about_point=None)`: Rotates the mobject.
    - `scale(scale_factor, **kwargs)`: Scales the mobject.
    - `set_color(color)`: Sets the color.

### `VMobject` (Vectorized Mobject)
A mobject that uses vector graphics. Most geometric shapes are VMobjects.
- **Methods**:
    - `set_fill(color=None, opacity=None)`: Sets the fill color and opacity.
    - `set_stroke(color=None, width=None, opacity=None)`: Sets the stroke (outline) properties.

### `Group` / `VGroup`
Groups multiple mobjects together so they can be manipulated as one.
- **Example**: `VGroup(circle, square).shift(UP)`

## Updaters
- `add_updater(updater_func)`: Adds a function to be called every frame to update the mobject's state.
- `remove_updater(updater_func)`: Removes an updater.
