from typing import Literal

SingleServer = str
SeveralServers = list[SingleServer]

Column = str
Columns = list[Column]

Row = list | tuple
Rows = list[Row]

ColumnCenter = Literal["left", "center", "right"]
