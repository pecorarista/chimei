from __future__ import annotations

from pathlib import Path

import toml


class TokenizerCofig:
    def __init__(
        self,
        normalized_stopwords: list[str],
        stoptags: list[str],
        stoptags1: list[str]
    ) -> TokenizerCofig:
        self.normalized_stopwords = normalized_stopwords
        self.stoptags = stoptags
        self.stoptags1 = stoptags1


class Config:
    def __init__(self, filename: Path | str) -> Config:
        config = toml.load(filename)
        self.tokenizer = TokenizerCofig(**config['tokenizer'])
