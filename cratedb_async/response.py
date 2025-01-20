import dataclasses

from .types import Columns, Rows, ColumnCenter


def center_string(string: str, pad_length: int, direction: ColumnCenter = "left") -> str:
    if direction == "left":
        return string.ljust(pad_length)

    if direction == "right":
        return string.rjust(pad_length)

    return string.center(pad_length)


def print_table(columns: Columns, rows: Rows, column_center: ColumnCenter = "left"):
    # The width of every column, calculated as the max
    # length from the column name, or the biggest value.
    col_widths = []

    for i, column in enumerate(columns):
        # Get the biggest value (in character count) of the values from a given column.
        biggest_value_in_chars: int = 0
        for row in rows:
            # We assume that the index of the column in columns matches the row index inside rows.
            biggest_value_in_chars = max(len(str(row[i])), biggest_value_in_chars)

        col_widths.append(
            max(biggest_value_in_chars, len(column))
        )

    # Create separator
    separator = "+" + "+".join("-" * (width + 2) for width in col_widths) + "+"
    # Create header
    header = "| " + " | ".join(
        f"{center_string(col, col_widths[i], column_center)}" for i, col in
        enumerate(columns)) + " |"

    # Create rows
    row_lines = ["| " + " | ".join(
        f"{center_string(str(row[i]), col_widths[i], column_center)}" for i in
        range(len(columns))) + " |" for row in
                 rows]

    # Combine everything
    table = "\n".join(
        [
            separator,
            header,
            separator,
            *row_lines,
            separator
        ]
    )
    return table


@dataclasses.dataclass
class SQLResponse:
    """Response from a CrateDB cluster request."""
    error: str = ""
    columns: list[str] = dataclasses.field(default_factory=list)
    rows: list = dataclasses.field(repr=False, default=list)
    row_count: int = 0
    duration: float = 0

    def as_table(self, max_rows=10) -> str:
        # Error message
        if not self.columns and self.error:
            return print_table(["error"], [[self.error]])

        # No columns nor row, typical in DDL and DML.
        if not self.columns and not self.error:
            return print_table([" "], [[self.row_count]])

        return print_table(self.columns, self.rows[:max_rows], "left")

    @property
    def ok(self) -> bool:
        """Returns whether the query resulted in an error."""
        return not self.error
