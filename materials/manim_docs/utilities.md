# Utilities, Colors & Constants

Global constants and helper functions in Manim.

## Colors
- **Standard**: `WHITE`, `BLACK`, `GRAY`, `SILVER`.
- **Primary**: `BLUE`, `RED`, `GREEN`, `YELLOW`.
- **Others**: `PINK`, `ORANGE`, `PURPLE`, `GOLD`, `TEAL`, `MAROON`, `BROWN`.
- **3Blue1Brown Palette**: `BLUE_A` through `BLUE_E`, `GREEN_A` through `GREEN_E`, etc. (E is darkest).

## Constants
- **Mathematical**: `PI`, `TAU` (2*PI), `DEGREES` (PI/180).
- **Directions**: 
    - `UP`, `DOWN`, `LEFT`, `RIGHT`, `ORIGIN`.
    - `UL` (Up-Left), `UR` (Up-Right), `DL` (Down-Left), `DR` (Down-Right).
    - `OUT` (Z-axis positive), `IN` (Z-axis negative).
- **Buffers**: `SMALL_BUFF`, `MED_SMALL_BUFF`, `MED_LARGE_BUFF`, `LARGE_BUFF`.

## Rate Functions (Easing)
- `smooth` (Default)
- `linear`
- `rush_into` / `rush_from`
- `slow_into`
- `there_and_back`
- `wiggle`

## Config
- `config.pixel_height`, `config.pixel_width`: Frame dimensions.
- `config.frame_rate`: FPS.
- `config.background_color`: Default BG color.
