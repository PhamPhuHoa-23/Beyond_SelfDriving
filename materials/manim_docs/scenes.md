# Scenes Reference

The `Scene` class is the canvas where all animations are defined.

## Core Class

### `Scene`
- **`construct()`**: The main method where you write your code.
- **`play(*animations, **play_kwargs)`**: Plays one or more animations.
- **`wait(duration=1)`**: Pauses the scene for a given number of seconds.
- **`add(*mobjects)`**: Adds mobjects to the scene without animation.
- **`remove(*mobjects)`**: Removes mobjects from the scene.
- **`clear()`**: Removes everything from the scene.

## Camera
- `self.camera.background_color`: Sets the background color (e.g., `self.camera.background_color = WHITE`).
- `self.camera.frame`: The frame mobject (can be moved or scaled for zooming/panning).

## Interaction
- `self.interactive_embed()`: Opens an interactive terminal to manipulate mobjects in real-time (useful for debugging).
