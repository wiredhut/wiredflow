from abc import abstractmethod
from typing import Any


class StageStorageInterface:
    """ Base class for defining interface for database stages connectors """

    def __init__(self, stage_id: str, **params):
        self.stage_id = stage_id
        self.params = params

    @abstractmethod
    def save(self, relevant_info: Any, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def load(self, **kwargs):
        raise NotImplementedError()
