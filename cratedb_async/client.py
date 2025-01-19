import httpx

from .types import SEVERAL_SERVERS, SINGLE_SERVER, ROWS
from .response import SQLResponse

_CRATE_ENDPOINT = "/_sql"


class CrateClient:
    """
    Represents a connection to a CrateDB cluster.
    """

    def __init__(self,
                 servers: SINGLE_SERVER | SEVERAL_SERVERS,
                 client: httpx.AsyncClient = None):
        self.servers = servers
        self.client_async = client or httpx.AsyncClient()

    def _parse_response(self, response: httpx.Response) -> SQLResponse:
        obj = response.json()
        return SQLResponse(
            error=obj.get('error', {}).get('message') or None,
            columns=obj.get('cols'),
            rows=obj.get('rows'),
            duration=obj.get('duration'),
            row_count=obj.get('rowcount', 0)
        )

    def _create_bulk_query(self, table_name: str, row_count: int) -> str:
        """
        row_count: int For how many values will '?' placeholder be added.
        """
        placeholders = '?,' * row_count

        if row_count > 0:
            placeholders = placeholders[:-1]

        return f"insert into {table_name} values ({placeholders})"

    async def query(self, stmt: str, json: dict = None, **kwargs) -> SQLResponse:
        json_dict = {'stmt': stmt}
        if json:
            json_dict |= json  # Merge the received json to the dict object we pass to the client
        response = await self.client_async.post(self.servers + _CRATE_ENDPOINT, json=json_dict, **kwargs)
        return self._parse_response(response)

    async def bulk_insert(self, table_name: str, rows: ROWS = None) -> SQLResponse:
        """
        Makes a bulk insert of `rows` using the bulk http API, this is the recommended way to
        send rows to CrateDB
        """
        query = self._create_bulk_query(table_name, row_count=len(rows))
        return self.query(query, rows=rows)
