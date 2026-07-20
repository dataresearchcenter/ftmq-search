from followthemoney import ValueEntity
from ftmq.model.entity import EntityModel as Entity
from ftmq.query import Query

from ftmq_search.logic import index_entities
from ftmq_search.store import get_store
from ftmq_search.store.base import BaseStore


def _test_store(donations, store: BaseStore):
    index_entities(donations, store)
    res = [r for r in store.search("metall")]
    assert len(res) == 3
    assert res[0].id == "62ad0fe6f56dbbf6fee57ce3da76e88c437024d5"
    assert isinstance(res[0].entity, Entity)
    assert isinstance(res[0].to_proxy(), ValueEntity)

    res = [r for r in store.search("metall OR tchibo")]
    assert len(res) == 4
    res = [r for r in store.search("metall AND tchibo")]
    assert len(res) == 0
    res = [r for r in store.autocomplete("verband")]
    assert len(res) == 5

    # use filters
    q = Query().where(dataset="donations")
    res = [r for r in store.search("metall", q)]
    assert len(res) == 3
    q = Query().where(dataset="foo")
    res = [r for r in store.search("metall", q)]
    assert len(res) == 0

    q = Query().where(dataset="donations", schema="Organization")
    res = [r for r in store.search("metall", q)]
    assert len(res) == 3
    q = Query().where(dataset="foo", schema="Organization")
    res = [r for r in store.search("metall", q)]
    assert len(res) == 0
    q = Query().where(dataset="donations", schema="Person")
    res = [r for r in store.search("metall", q)]
    assert len(res) == 0

    q = Query().where(country__in=["de", "lu"])
    res = [r for r in store.search("metall", q)]
    assert len(res) == 3
    q = Query().where(country="gb")
    res = [r for r in store.search("metall", q)]
    assert len(res) == 0

    return True


def test_store_sqlite(donations, tmp_path):
    store = get_store(uri="sqlite:///" + str(tmp_path / "ftmqs.db"))
    assert _test_store(donations, store)


def test_store_tantivy(donations, tmp_path):
    store = get_store(uri=f'tantivy://{tmp_path / "tantivy.db"}')
    assert _test_store(donations, store)


def test_store_memory(donations):
    store = get_store(uri="memory:///")
    assert _test_store(donations, store)
