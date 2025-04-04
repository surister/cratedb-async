[![Upload](https://github.com/surister/cratedb-async/actions/workflows/python-publish.yml/badge.svg)](https://github.com/surister/cratedb-async/actions/workflows/python-publish.yml)
![PyPI - Version](https://img.shields.io/pypi/v/cratedb-async?style=flat&color=green)
![Python version ](https://img.shields.io/pypi/pyversions/cratedb-async
)
# CrateDB Async driver based on httpx.


This CrateDB driver does not follow the DB-API, but its own API design.

## Usage

It can be used with any async library,

#### Asyncio
```python

import asyncio

from cratedb_async.client import CrateClient


async def main():
    crate = CrateClient('http://192.168.88.251:4200')
    response = await crate.query('SELECT * FROM sys.summits')
    print(response.as_table())

asyncio.run(main())

# +----------------+---------------------+---------+--------------+--------+----------------+------------+---------------+----------------------+
# | classification | coordinates         | country | first_ascent | height | mountain       | prominence | range         | region               |
# +----------------+---------------------+---------+--------------+--------+----------------+------------+---------------+----------------------+
# | I/B-07.V-B     | [6.86444, 45.8325]  | FR/IT   | 1786         | 4808   | Mont Blanc     | 4695       | U-Savoy/Aosta | Mont Blanc massif    |
# | I/B-09.III-A   | [7.86694, 45.93694] | CH      | 1855         | 4634   | Monte Rosa     | 2165       | Valais        | Monte Rosa Alps      |
# | I/B-09.V-A     | [7.85889, 46.09389] | CH      | 1858         | 4545   | Dom            | 1046       | Valais        | Mischabel            |
# | I/B-09.III-A   | [7.83556, 45.92222] | CH/IT   | 1861         | 4527   | Liskamm        | 376        | Valais/Aosta  | Monte Rosa Alps      |
# | I/B-09.II-D    | [7.71583, 46.10139] | CH      | 1861         | 4506   | Weisshorn      | 1235       | Valais        | Weisshorn-Matterhorn |
# | I/B-09.II-A    | [7.65861, 45.97639] | CH/IT   | 1865         | 4478   | Matterhorn     | 1042       | Valais/Aosta  | Weisshorn-Matterhorn |
# | I/B-09.II-C    | [7.61194, 46.03417] | CH      | 1862         | 4357   | Dent Blanche   | 915        | Valais        | Weisshorn-Matterhorn |
# | I/B-09.I-B     | [7.29917, 45.9375]  | CH      | 1859         | 4314   | Grand Combin   | 1517       | Valais        | Grand Combin Alps    |
# | I/B-12.II-A    | [8.12611, 46.53722] | CH      | 1829         | 4274   | Finsteraarhorn | 2280       | Bern/Valais   | Bernese Alps         |
# | I/B-09.II-D    | [7.69028, 46.065]   | CH      | 1864         | 4221   | Zinalrothorn   | 490        | Valais        | Weisshorn-Matterhorn |
# +----------------+---------------------+---------+--------------+--------+----------------+------------+---------------+----------------------+
```


#### Trio

```python
import trio

from cratedb_async.client import CrateClient


async def main():
    crate = CrateClient('http://192.168.88.251:4200')
    response = await crate.query('SELECT * FROM sys.summits')
    print(response.as_table())

trio.run(main)

# +----------------+---------------------+---------+--------------+--------+----------------+------------+---------------+----------------------+
# | classification | coordinates         | country | first_ascent | height | mountain       | prominence | range         | region               |
# +----------------+---------------------+---------+--------------+--------+----------------+------------+---------------+----------------------+
# | I/B-07.V-B     | [6.86444, 45.8325]  | FR/IT   | 1786         | 4808   | Mont Blanc     | 4695       | U-Savoy/Aosta | Mont Blanc massif    |
# | I/B-09.III-A   | [7.86694, 45.93694] | CH      | 1855         | 4634   | Monte Rosa     | 2165       | Valais        | Monte Rosa Alps      |
# | I/B-09.V-A     | [7.85889, 46.09389] | CH      | 1858         | 4545   | Dom            | 1046       | Valais        | Mischabel            |
# | I/B-09.III-A   | [7.83556, 45.92222] | CH/IT   | 1861         | 4527   | Liskamm        | 376        | Valais/Aosta  | Monte Rosa Alps      |
# | I/B-09.II-D    | [7.71583, 46.10139] | CH      | 1861         | 4506   | Weisshorn      | 1235       | Valais        | Weisshorn-Matterhorn |
# | I/B-09.II-A    | [7.65861, 45.97639] | CH/IT   | 1865         | 4478   | Matterhorn     | 1042       | Valais/Aosta  | Weisshorn-Matterhorn |
# | I/B-09.II-C    | [7.61194, 46.03417] | CH      | 1862         | 4357   | Dent Blanche   | 915        | Valais        | Weisshorn-Matterhorn |
# | I/B-09.I-B     | [7.29917, 45.9375]  | CH      | 1859         | 4314   | Grand Combin   | 1517       | Valais        | Grand Combin Alps    |
# | I/B-12.II-A    | [8.12611, 46.53722] | CH      | 1829         | 4274   | Finsteraarhorn | 2280       | Bern/Valais   | Bernese Alps         |
# | I/B-09.II-D    | [7.69028, 46.065]   | CH      | 1864         | 4221   | Zinalrothorn   | 490        | Valais        | Weisshorn-Matterhorn |
# +----------------+---------------------+---------+--------------+--------+----------------+------------+---------------+----------------------+

```

#### Bulk insert

```python
import asyncio

from cratedb_async.client import CrateClient


async def main():
    crate = CrateClient('http://192.168.88.251:4200')
    rows = [
        ('one', 2, ['three', ]),
        ('three', 4, ['five', ])
    ]
    table_name = 'my_tbl'
    
    create_table_resp = await crate.query(f'create table {table_name} (one text, two integer, three array(TEXT))')
    print(create_table_resp)
    # SQLResponse(error=None, columns=[], row_count=1, duration=177.55101)

    response = await crate.bulk_insert(table_name, rows)
    print(response)
    # SQLResponse(error=None, columns=[], row_count=0, duration=6.341763)

    await crate.query(f'refresh table {table_name}')

    select_response = await crate.query(f'select * from {table_name}')
    print(select_response.as_table())
    # SQLResponse(error=None, columns=[], row_count=1, duration=8.724443)

asyncio.run(main())
```



## Style guide
This project uses Google Python Style guide with minor tweaks, enforced by pyling, read more in
* Google documentation: https://google.github.io/styleguide/pyguide.html
* Docstring documentation: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

### Tweaks
* Max line is 100
* Indentation is four spaces.
