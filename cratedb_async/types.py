from typing import Literal, Any

SingleServer = str
SeveralServers = list[SingleServer]

Column = str
Columns = list[Column]

Row = list | tuple
Rows = list[Row]
Object = dict[str: Any]
JsonRows = list[Object]

ColumnCenter = Literal["left", "center", "right"]
