# Tables & Matrices Reference

Mobjects for displaying structured data.

## Tables

### `Table`
Base class for tables.
- `Table(data, row_labels=None, col_labels=None)`
- **Methods**:
    - `get_rows()`, `get_columns()`: Access groups of cells.
    - `add_highlighted_cell(index, color)`: Highlights a specific cell.
    - `create_stats_table()`: Specialized table for statistics.

### `MathTable`
A table where every entry is rendered with `MathTex`.
- `MathTable([[1, 2], [3, 4]])`

## Matrices

### `Matrix`
Displays a matrix with brackets.
- `Matrix([[1, 2], [3, 4]])`
- **Subclasses**:
    - `DecimalMatrix`: For floating point numbers.
    - `IntegerMatrix`: For integers.
    - `MobjectMatrix`: For a matrix of other mobjects.

### Brackets
- `PMatrix`: Matrix with parentheses `( )`.
- `BMatrix`: Matrix with square brackets `[ ]`.
- `VMatrix`: Matrix with vertical bars `| |`.
