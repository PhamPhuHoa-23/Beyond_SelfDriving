# Probability & Statistics Reference

Mobjects for visualizing probability concepts.

## Probability

### `SampleSpace`
A rectangular area representing a sample space.
- `SampleSpace(width=5, height=5)`
- **Methods**:
    - `divide_vertically(fractions)`
    - `divide_horizontally(fractions)`

## Statistics

### `BarChart`
- `BarChart(values=[1, 2, 3], bar_names=["A", "B", "C"], y_range=[0, 5, 1])`

### `CoordinateSystem` (from Graphing)
- Many statistics visualizations use the base `Axes` or `NumberLine` classes.
