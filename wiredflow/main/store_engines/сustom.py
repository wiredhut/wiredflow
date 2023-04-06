from typing import Union, Callable, Any

from loguru import logger

from wiredflow.main.actions.stages.storage_stage import StageStorageInterface


class CustomStorageStage(StageStorageInterface):
    """ Class for launching custom functions to save data """

    def __init__(self, function_to_launch: Callable,
                 stage_id: str, use_threads: bool, **params):
        super().__init__(stage_id, use_threads, **params)
        self.function_to_launch = function_to_launch

    def save(self, relevant_info: Any, **kwargs):
        kwargs = {**self.params, **kwargs}
        self.function_to_launch(relevant_info, **kwargs)

        logger.debug(f'Custom database save info. Successfully save data into database')

    def load(self, **kwargs):
        return None
