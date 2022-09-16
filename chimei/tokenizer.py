from __future__ import annotations

from itertools import takewhile
from typing import Any

import pandas
from sudachipy import dictionary
from sudachipy import tokenizer as sudachi_tokenizer

from chimei.config import Config


class Tokenizer:
    def __init__(self, config: Config) -> Tokenizer:
        self.mode = sudachi_tokenizer.Tokenizer.SplitMode.A
        self.tokenizer = dictionary.Dictionary().create()
        self.mapping = self.create_mapping()

    def detect(self, s: str) -> list[str]:
        score = dict()
        for token in self.tokenizer.tokenize(s, self.mode):
            if token.part_of_speech()[2] == '地名':
                for (prefecture, value) in self.mapping.get(token.dictionary_form(), {}).items():
                    score[prefecture] = score.get(prefecture, 0.0) + value
        return score

    def create_mapping(self) -> dict[str, Any]:
        key_pref = '都道府県名\n（漢字）'
        key_city = '市区町村名\n（漢字）'
        source = pandas \
            .read_excel('resources/000730858.xlsx') \
            .groupby(by=key_pref)[key_city] \
            .agg(list) \
            .to_dict()

        city2prefecture = dict()

        for (prefecture, cities) in source.items():
            for city in cities:

                # 都道府県の情報を表す行は、市町村名がNaN
                if pandas.isna(city):
                    city = prefecture

                tokens = [
                    t.surface() for t in takewhile(
                        lambda t: t.part_of_speech()[0] != '助詞',
                        self.tokenizer.tokenize(f'{city}に行く。', self.mode)
                    )
                ]

                # A単位で1語または2語になる地名のみを扱う
                if len(tokens) == 1 or (len(tokens) == 2 and tokens[-1] in ['市', '区', '町', '村']):
                    key = tokens[0]
                    suffix = tokens[0][-1] if len(tokens) == 1 else tokens[-1]
                    city2prefecture[key] = city2prefecture.get(key, []) + [(suffix, prefecture)]

            city2score = dict()
            for (name, possibilities) in city2prefecture.items():
                score = dict()
                for (suffix, prefecture) in possibilities:
                    if suffix in ['市', '区', '道']:
                        score[prefecture] = score.get(prefecture, 0.0) + 0.5
                    elif suffix in '町':
                        score[prefecture] = score.get(prefecture, 0.0) + 0.2
                    else:
                        score[prefecture] = score.get(prefecture, 0.0) + 0.1
                city2score[name] = score

        return city2score
