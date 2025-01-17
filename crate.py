import dataclasses
from typing import Literal

import httpx

import trio

CRATE_ENDPOINT = '/_sql'

SINGLE_SERVER = str
SEVERAL_SERVERS = list[SINGLE_SERVER]

COLUMN = str
COLUMNS = list[COLUMN]

ROW = list
ROWS = list[ROW]

COLUMN_CENTER = Literal['left', 'center', 'right']


def center_string(string: str, pad_length: int, direction: COLUMN_CENTER = 'left') -> str:
    if direction == 'left':
        return string.ljust(pad_length)

    if direction == 'right':
        return string.rjust(pad_length)

    return string.center(pad_length)


def print_table(columns: COLUMNS, rows: ROWS, center_column: COLUMN_CENTER = 'left'):
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
        f"{center_string(col, col_widths[i], center_column)}" for i, col in enumerate(columns)) + " |"

    # Create rows
    row_lines = ["| " + " | ".join(
        f"{center_string(str(row[i]), col_widths[i], center_column)}" for i in range(len(columns))) + " |" for row in rows]

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
    error: str = ''
    columns: list[str] = dataclasses.field(default_factory=list)
    rows: list = dataclasses.field(repr=False, default=list)
    row_count: int = 0
    duration: float = 0

    def as_table(self, max_rows=10) -> str:
        # Error message
        if not self.columns and self.error:
            return print_table(['error'], [[self.error]])

        # No columns nor row, typical in DDL and DML
        if not self.columns and not self.error:
            return print_table([' '], [[self.row_count]])

        return print_table(self.columns, self.rows[:max_rows], 'left')


class CrateClient:
    """
    Represents a connection to a CrateDB cluster.
    """
    def __init__(self, servers: SINGLE_SERVER | SEVERAL_SERVERS):
        self.servers = servers
        self.client_async = httpx.AsyncClient()
        self.client = httpx.Client()

    def _parse_response(self, response: httpx.Response) -> SQLResponse:
        obj = response.json()
        return SQLResponse(
            error=obj.get('error', {}).get('message') or None,
            columns=obj.get('cols'),
            rows=obj.get('rows'),
            duration=obj.get('duration'),
            row_count=obj.get('rowcount', 0)
        )

    async def query(self, stmt: str) -> None:
        response = await self.client_async.post(self.servers + CRATE_ENDPOINT, json={'stmt': stmt})
        return self._parse_response(response)

    async def bulk_insert(self, table_name: str, rows: list):
        stmt = f"insert into {table_name} VALUES (?,?,?,?,?)"
        await self.client_async.post(self.servers + CRATE_ENDPOINT,
                                     json={'stmt': stmt, "bulk_args": rows})
