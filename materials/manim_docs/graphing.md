# Graphing Reference

Coordinates, axes, and function plotting.

## Coordinate Systems

### `Axes`
- `Axes(x_range=[-5, 5, 1], y_range=[-3, 3, 1], axis_config={"include_tip": True})`
- **Methods**:
    - `get_graph(function)`: Returns a `ParametricFunction` for the given data.
    - `get_coords_from_point(point)`: Convers screen points to graph coordinates.
    - `get_axes_labels(x_label="x", y_label="y")`: Adds labels to the axes.

### `NumberLine`
- `NumberLine(x_range=[-10, 10, 1], length=10, include_numbers=True)`

## Plotting

### `FunctionGraph`
- `FunctionGraph(lambda x: x**2, x_range=[-2, 2])`

### `ParametricFunction`
- `ParametricFunction(lambda t: [np.cos(t), np.sin(t), 0], t_range=[0, TAU])`

## Data Visualization
- `BarChart(values=[1, 2, 3], y_range=[0, 5, 1])`
- `CoordinateSystem.get_area(graph, x_range=[0, 1])`: Shades the area under a curve.
