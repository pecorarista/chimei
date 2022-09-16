import pytest

from chimei.config import Config
from chimei.tokenizer import Tokenizer


@pytest.fixture(scope='session')
def config() -> Config:
    return Config('config.toml')


@pytest.fixture(scope='session')
def tokenizer(config: Config) -> Tokenizer:
    return Tokenizer(config)
