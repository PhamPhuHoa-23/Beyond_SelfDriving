# Text & LaTeX Reference

Mobjects for displaying text and mathematical formulas.

## Text Mobjects

### `Text`
Standard text using Pango.
- `Text("Hello World", font="Arial", font_size=24)`
- **Methods**:
    - `set_color_by_text(text, color)`: Colors specific substrings.
    - `t2c={"word": RED}`: Text-to-color mapping in constructor.

### `MarkupText`
Supports Pango markup (HTML-like tags).
- `MarkupText("<b>Bold</b> and <i>Italic</i>")`

## LaTeX Mobjects

### `MathTex`
For mathematical formulas. Requires LaTeX (MiKTeX/TeXLive) and `dvisvgm`.
- `MathTex(r"e^{i\pi} + 1 = 0")`
- **Subscripts/Superscripts**: Use `{{ }}` for easy indexing/animating parts.
- `set_color_by_tex(tex, color)`: Colors specific parts of the formula.

### `Tex`
For standard LaTeX text.
- `Tex(r"This is a \LaTeX\ sentence.")`

## Alignment & Arrangement
- `VGroup(text1, text2).arrange(DOWN, center=True)`
- `text.to_edge(UP)`
- `text.to_corner(UL)`
