# Animations Reference

Animations are procedures that interpolate between two mobjects or states over time.

## Core Classes

### `Animation`
The base class for all animations.
- **Parameters**:
    - `mobject`: The mobject to animate.
    - `run_time`: Duration in seconds.
    - `rate_func`: Function mapping [0, 1] to [0, 1] (e.g., `smooth`, `linear`, `there_and_back`).

### `AnimationGroup`
Plays multiple animations simultaneously or with a lag.
- `AnimationGroup(*animations, lag_ratio=0)`

## Common Animations

### Creation
- `Create(mobject)`: Draws the mobject.
- `Uncreate(mobject)`: Undraws the mobject.
- `Write(text)`: Draws text (simulates writing).
- `FadeIn(mobject)`: Fades in from transparency.
- `FadeOut(mobject)`: Fades out to transparency.

### Transformation
- `Transform(mobject, target_mobject)`: Morphs the first mobject into the second.
- `ReplacementTransform(mobject, target_mobject)`: Morphs and replaces the first with the second in the scene.
- `Restore(mobject)`: Returns a mobject to its saved state (using `mob.save_state()`).

### Indication
- `Indicate(mobject)`: Briefly highlights a mobject (usually by scaling and changing color).
- `Flash(point)`: Creates a brief burst of lines at a point.
- `FocusOn(mobject_or_point)`: Draws a shrinking circle around a target.

### Movement
- `MoveAlongPath(mobject, path)`: Moves a mobject along a specified curve.
- `Rotate(mobject, angle)`: Rotates the mobject over time.
