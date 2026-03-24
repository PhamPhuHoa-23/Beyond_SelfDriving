# Geometry Reference

Commonly used geometric shapes in Manim.

## 2D Shapes

### `Circle`
- `Circle(radius=1.0, color=WHITE)`
- `Dot(point=ORIGIN, radius=0.08)`
- `Ellipse(width=2.0, height=1.0)`
- `Annulus(inner_radius=0.5, outer_radius=1.0)`

### `Polygon`
- `Triangle()`: Equilateral triangle.
- `Square(side_length=2.0)`
- `Rectangle(width=4.0, height=2.0)`
- `RoundedRectangle(corner_radius=0.5)`
- `RegularPolygon(n=6)`: A hexagon, etc.
- `Polygon(*vertices)`: Custom polygon defined by points.

### `Lines`
- `Line(start, end)`
- `Arrow(start, end)`
- `DoubleArrow(start, end)`
- `Vector(direction)`: Arrow starting at `ORIGIN`.
- `Arc(radius=1.0, start_angle=0, angle=TAU/4)`

## Styling Constants
- Colors: `WHITE`, `BLACK`, `RED`, `BLUE`, `GREEN`, `YELLOW`, `PINK`, `ORANGE`, `PURPLE`, `GOLD`.
- Directions: `UP`, `DOWN`, `LEFT`, `RIGHT`, `UL` (UpLeft), `UR`, `DL`, `DR`.
