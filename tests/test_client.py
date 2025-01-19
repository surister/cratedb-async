import trio

from cratedb_async.client import CrateClient


def test_client_request():
    client = CrateClient('http://localhost:4200')
    response = trio.run(client.query, 'create table (a text)')


def test_bulk_query():
    client = CrateClient('')

    query = client._create_bulk_query('t', row_count=1) == 'insert into t values (?)'
    assert isinstance(query, str)
    assert query == 'insert into t values (?)'
    assert client._create_bulk_query('t', row_count=5) == 'insert into t values (?,?,?,?,?)'
