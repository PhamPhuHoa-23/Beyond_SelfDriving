# SVG & Images Reference

Working with external assets like SVG files and raster images.

## SVG Mobjects

### `SVGMobject`
Loads and displays an SVG file.
- `SVGMobject("path/to/file.svg")`
- **Properties**:
    - SVGs are loaded as a `VGroup` of sub-mobjects (paths).
    - You can style individual parts: `svg[0].set_color(RED)`.

## Image Mobjects

### `ImageMobject`
Displays a raster image (PNG, JPG, etc.).
- `ImageMobject("path/to/image.png")`
- **Methods**:
    - `set_resampling_filter(filter)`: Controls scaling quality.
    - `pixel_array`: Direct access to NumPy pixel data.

## Specialized Types

### `PMobject` (Point Mobject)
Mobjects made of discrete points rather than paths.
- `Point(location)`
- `DashedLine(start, end)` (Technically a VMobject but often used for specialized styles).

### `TracedPath`
Useful for creating "pencil-like" traces of a moving point.
- `TracedPath(dot.get_center)`
