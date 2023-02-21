from typing import Union, Callable

from wiredflow.main.actions.assimilation.interface import ProxyStage
from wiredflow.main.actions.stages.storage_stage import StageStorageInterface
from wiredflow.main.store_engines.json_engine.json_db import JSONStorageStage
from wiredflow.main.store_engines.mongo_engine.mongo_db import MongoStorageStage


class StoreStageProxy(ProxyStage):
    """
    Class for compiling actual databases (or files) connectors via Stages when
    it is required
    """

    storage_by_name = {'json': JSONStorageStage,
                       'mongo': MongoStorageStage}

    def __init__(self, storage_name: Union[str, Callable], stage_id: str, **kwargs):
        if isinstance(storage_name, str):
            self.storage_stage = self.storage_by_name[storage_name]
        else:
            self.storage_stage = storage_name

        self.stage_id = stage_id
        self.kwargs = kwargs

    def compile(self) -> StageStorageInterface:
        """ Compile Database connector stage object """
        return self.storage_stage(self.stage_id, **self.kwargs)
