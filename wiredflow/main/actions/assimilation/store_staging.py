from typing import Union, Callable

from wiredflow.main.actions.assimilation.interface import ProxyStage
from wiredflow.main.actions.stages.storage_stage import StageStorageInterface
from wiredflow.main.store_engines.csv_engine.csv_db import CSVStorageStage
from wiredflow.main.store_engines.json_engine.json_db import JSONStorageStage
from wiredflow.main.store_engines.mongo_engine.mongo_db import MongoStorageStage
from wiredflow.main.store_engines.сustom import CustomStorageStage


class StoreStageProxy(ProxyStage):
    """
    Class for compiling actual databases (or files) connectors via Stages when
    it is required
    """

    storage_by_name = {'json': JSONStorageStage,
                       'csv': CSVStorageStage,
                       'mongo': MongoStorageStage}

    def __init__(self, configuration: Union[str, Callable], stage_id: str,
                 use_threads: bool, **kwargs):
        self.custom_realization = False
        if isinstance(configuration, str):
            self.storage_stage = self.storage_by_name[configuration]
        else:
            self.custom_realization = True
            self.storage_stage = configuration

        self.stage_id = stage_id
        self.kwargs = kwargs
        self.use_threads = use_threads

    def compile(self) -> StageStorageInterface:
        """ Compile Database connector stage object """
        if self.custom_realization is True:
            # Custom realization need to be applied
            return CustomStorageStage(self.storage_stage, self.stage_id, self.use_threads, **self.kwargs)
        else:
            return self.storage_stage(self.stage_id, self.use_threads, **self.kwargs)
