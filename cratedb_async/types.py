from typing import Literal

SINGLE_SERVER = str
SEVERAL_SERVERS = list[SINGLE_SERVER]

COLUMN = str
COLUMNS = list[COLUMN]

ROW = list
ROWS = list[ROW]

COLUMN_CENTER = Literal['left', 'center', 'right']
