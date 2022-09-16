import json
from pathlib import Path

from jsonschema import validate

from chimei.tokenizer import Tokenizer


def test_detect(tokenizer: Tokenizer) -> None:

    result = tokenizer.detect('花巻と盛岡を通過し、八戸まで行った。')
    assert set(result.keys()) == set(['岩手県', '青森県']) and result['岩手県'] > result['青森県']

    result = tokenizer.detect('鹿児島から那覇へ行き、宮古島にも行った。')
    assert set(result.keys()) == set(['鹿児島県', '沖縄県']) and result['沖縄県'] > result['鹿児島県']


def test_create_mapping(tokenizer: Tokenizer) -> None:
    result = tokenizer.create_mapping()
    with Path('tests/resources/schema.json').open(mode='r') as r:
        schema = json.load(r)
    validate(result, schema=schema)
