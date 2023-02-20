from typing import Any

from loguru import logger

from wiredflow.main.store_engines.json_engine.json_db import JSONConnector


class StageStorageInterface:
    """ Class to store data into file or database """
    engine_by_name = {'json': JSONConnector,
                      'mongo': None}

    def __init__(self, storage_name: str, stage_id: str, **params):
        self.stage_id = stage_id
        self.storage_name = storage_name
        self.connector = self.engine_by_name[storage_name](stage_id, **params)

    def save(self, relevant_info: Any, **kwargs):
        logger.debug(f'{self.storage_name} info. Storage {self.stage_id} save data')
        return self.connector.save(relevant_info, **kwargs)

    def load(self, **kwargs):
        logger.debug(f'{self.storage_name} info. Storage {self.stage_id} load data')
        return self.connector.load(**kwargs)
