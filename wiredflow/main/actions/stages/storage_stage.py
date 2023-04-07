from abc import abstractmethod
from typing import Any


class StageStorageInterface:
    """ Base class for defining interface for database stages connectors """

    def __init__(self, stage_id: str, use_threads: bool, **params):
        self.stage_id = stage_id
        self.use_threads = use_threads
        self.params = params

    @abstractmethod
    def save(self, relevant_info: Any, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def load(self, **kwargs):
        raise NotImplementedError()
