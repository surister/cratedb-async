from typing import Optional

import httpx

from cratedb_async.types import SeveralServers, SingleServer, Rows
from cratedb_async.response import SQLResponse

_CRATE_ENDPOINT = "/_sql"


def _create_insert_query(table_name: str, row_count: int) -> str:
    """Creates an insert query with value placeholders

    Args:
        table_name: The name of the table.
        row_count: How many values will be inserted, for placeholder generation.

    Returns:
        The insert query.

    Examples:
        >>> _create_insert_query("tbl", 4)
        'insert into "tbl" values (?,?,?,?)'

    """
    placeholders = "?," * row_count

    if row_count > 0:
        placeholders = placeholders[:-1]

    return f"insert into \"{table_name}\" values ({placeholders})"


class CrateClient:
    """
    Represents a connection to a CrateDB cluster, the `HTTP` api is used.
    """

    def __init__(self,
                 servers: SingleServer | SeveralServers,
                 client: httpx.AsyncClient = None):
        self.servers = servers
        self.client_async = client or httpx.AsyncClient()

    def _parse_response(self, response: httpx.Response) -> SQLResponse:
        obj = response.json()
        return SQLResponse(
            error=obj.get("error", {}).get("message") or None,
            columns=obj.get("cols"),
            rows=obj.get("rows"),
            duration=obj.get("duration"),
            row_count=obj.get("rowcount", 0)
        )

    async def query(self, stmt: str, json: Optional[dict] = None) -> SQLResponse:
        """
        Runs a SQL statement in the cluster asynchronously.

        Args:
            stmt: The query statement.
            json: JSON data sent in the ``httpx.post`` request.
            **kwargs: Additional parameters for ``httpx``.

        Returns:
            The response from the cluster.
        """
        json_dict = {"stmt": stmt}

        if json:
            json_dict |= json  # Merge the received json to the dict object we pass to the client

        response = await self.client_async.post(
            self.servers + _CRATE_ENDPOINT,
            json=json_dict,

        )

        return self._parse_response(response)

    async def bulk_insert(self, table_name: str, rows: Rows = None) -> SQLResponse:
        """Runs a bulk insert to the cluster; this is the most efficient way to ingest data.

        Args:
            table_name: The name of the table.
            rows: Rows that will be sent in the bulk_insert, every row is sent in the same request.

        Note:
            Rows are not batched, if the number of rows is large, you will benefit from batching.

        Returns:
            The response from the cluster.
        """

        query = _create_insert_query(table_name, value_count=len(rows[0]))
        return await self.query(query, {'bulk_args': rows})
