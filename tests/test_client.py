from cratedb_async.client import _create_insert_query

def test_bulk_query():
    query = _create_insert_query('t', row_count=1)

    assert isinstance(query, str)
    assert query == 'insert into "t" values (?)'
    assert _create_insert_query('t', row_count=5) == 'insert into "t" values (?,?,?,?,?)'
