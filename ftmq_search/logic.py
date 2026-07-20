from typing import Iterable

import orjson
from anystore.io import logged_items, smart_open, smart_stream
from anystore.logic.constants import DEFAULT_WRITE_MODE
from anystore.types import Uri
from followthemoney import EntityProxy
from ftmq.io import smart_read_proxies

from ftmq_search.logging import get_logger
from ftmq_search.model import EntityDocument
from ftmq_search.store.base import BaseStore

log = get_logger(__name__)


def transform(in_uri: Uri, out_uri: Uri) -> None:
    with smart_open(out_uri, DEFAULT_WRITE_MODE) as o:
        for entity in logged_items(
            smart_read_proxies(in_uri),
            "Transform",
            uri=in_uri,
            item_name="Entity",
            logger=log,
        ):
            doc = EntityDocument.from_entity(entity)
            data = doc.model_dump(by_alias=True, mode="json")
            line = orjson.dumps(data, option=orjson.OPT_APPEND_NEWLINE)
            o.write(line)


def index(in_uri: Uri, store: BaseStore) -> None:
    for line in logged_items(
        smart_stream(in_uri),
        "Index",
        from_uri=in_uri,
        uri=store.uri,
        item_name="EntityDocument",
        logger=log,
    ):
        doc = EntityDocument(**orjson.loads(line))
        store.put(doc)
    store.flush()


def index_entities(entities: Iterable[EntityProxy], store: BaseStore) -> None:
    for entity in logged_items(
        entities, "Index", item_name="Entity", uri=store.uri, logger=log
    ):
        doc = EntityDocument.from_entity(entity)
        store.put(doc)
    store.flush()
