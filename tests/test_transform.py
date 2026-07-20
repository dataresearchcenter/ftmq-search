from ftmq.io import orjson, smart_stream

from ftmq_search.logic import transform
from ftmq_search.model import EntityDocument


def test_transform(fixtures_path, tmp_path, donations):
    tested = False
    for proxy in donations:
        data = EntityDocument.from_entity(proxy)
        assert data.model_dump(by_alias=True) == {
            "id": "6d03aec76fdeec8f9697d8b19954ab6fc2568bc8",
            "caption": "MLPD",
            "schema": "Organization",
            "datasets": ["donations"],
            "countries": [],
            "names": ["MLPD"],
            "text": "MLPD",
            "fingerprints": ["mlpd"],
            "temporal_start": None,
            "temporal_end": None,
            "linked_entities": [],
            "dates": [],
        }

        tested = True
        break
    assert tested

    # tested = False
    # for proxy in donations:
    #     if proxy.schema.is_a("Payment"):
    #         data = EntityDocument.from_entity(proxy)
    #         assert data.model_dump(by_alias=True) == {
    #             "id": "2216b422a31242fe204654ce194864661f515921",
    #             "caption": "Payment",
    #             "schema": "Payment",
    #             "datasets": ["donations"],
    #             "countries": [],
    #             "temporal_start": "2011-12-29",
    #             "temporal_end": "2011-12-29",
    #             "dates": ["2011-12-29"],
    #             "names": ["Frau Lina Dachner", "MLPD"],
    #             "fingerprints": ["dachner lina", "mlpd"],
    #             "text": "100000 2011-12-29 6d03aec76fdeec8f9697d8b19954ab6fc2568bc8 Frau Lina Dachner MLPD f9c295f21b233ac878fbac4d271bb6fd13d7952a",
    #         }

    #         tested = True
    #         break
    # assert tested

    out = tmp_path / "transformed.json"
    transform(fixtures_path / "donations.ijson", out)
    transformed = [d for d in smart_stream(out)]
    assert len(transformed) == 474
    data = orjson.loads(transformed[0])
    assert "donations" in EntityDocument(**data).datasets
