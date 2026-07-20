[![ftmq-search on pypi](https://img.shields.io/pypi/v/ftmq-search)](https://pypi.org/project/ftmq-search/) [![Python test and package](https://github.com/investigativedata/ftmq-search/actions/workflows/python.yml/badge.svg)](https://github.com/investigativedata/ftmq-search/actions/workflows/python.yml) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit) [![Coverage Status](https://coveralls.io/repos/github/investigativedata/ftmq-search/badge.svg?branch=main)](https://coveralls.io/github/investigativedata/ftmq-search?branch=main) [![MIT License](https://img.shields.io/pypi/l/ftmq-search)](./LICENSE)

# ftmq-search

Search stores logic for [FollowTheMoney](https://followthemoney.tech) data.

The aim is to experiment around with different full-text search backends for efficient _shallow search_ of entities.

Currently supported backends:

- [Sqlite FTS5](https://www.sqlite.org/fts5.html)
- [Tantivy](https://github.com/quickwit-oss/tantivy) (persistent or in-memory)

For [Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html), use either [openaleph-search](https://openaleph.org/docs/lib/openaleph-search/) that can be used standalone outside [OpenAleph](https://openaleph.org) or [yente](https://yente.followthemoney.tech/).

## Install

Python 3.11 or later.

    pip install ftmq-search

## Generate search documents

    ftmqs transform -i entities.ftm.json > entities.transformed.json

Speed it up via [GNU Parallel](https://www.gnu.org/software/parallel/sphinx.html)

    cat entities.ftm.json | parallel -j8 --pipe --roundrobin ftmqs transform > entities.transformed.json

## Index transformed documents

### Sqlite FTS

    ftmqs --uri sqlite:///ftmqs.store index -i entities.transformed.json

### Tantivy

    ftmqs --uri tantivy://tantivy.db index -i entities.transformed.json

## Search

    ftmqs search <query>

## Autocomplete

    ftmqs autocomplete <query>

## Python

```python
from ftmq import Query, smart_read_proxies

from ftmqs import get_store
from ftmqs.logic import index_proxies

# sqlite
store = get_store("sqlite:///ftmqs.db")

# tantivy
store = get_store("tantivy://tantivy.db")

# tantivy in-memory
store = get_store("memory://")

# index entity data
proxies = smart_read_proxies("./entities.ftm.json")
index_proxies(proxies, store)

# search
store.search("jane doe")

# filter for country and schema
q = Query().where(country="de", schema="Person")
store.search("jane doe", q)
```
