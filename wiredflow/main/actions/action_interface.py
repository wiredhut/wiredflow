from abc import abstractmethod
from typing import List, Any, Dict, Union

from loguru import logger

from wiredflow.main.actions.assimilation.interface import ProxyStage
from wiredflow.main.actions.stages.core_stage import CoreLogicInterface
from wiredflow.main.actions.stages.http_stage import StageHTTPConnector
from wiredflow.main.actions.stages.send_stage import StageSendInterface
from wiredflow.main.actions.stages.storage_stage import StageStorageInterface
from wiredflow.wiredtimer.timer import WiredTimer


class Action:
    """
    Base class for single action execution into the pipeline.
    Responsibility zone: launch low-level function and classes to
    produce desired actions in the pipeline.

    NB: Action can contain several stages. For example - get data via HTTPS (1)
    and save in into database (2)

    :param pipeline_name: name of pipeline where this action was launched
    :param stages: list with configured stages (and parameters) to be launched
    :param is_single_execution: is there a need to launch all stages without loop
    """

    def __init__(self, pipeline_name: str, stages: List[ProxyStage],
                 **params):
        self.pipeline_name = pipeline_name
        self.stages = stages

        # Initialize all stages
        self.init_stages = []
        self._init_stages_objects()

        # Additional fields
        self.connector = None
        self.save_action_id = None
        self.db_connectors: dict = {}

        # Set regime of requests - default value is None
        self.timedelta_seconds = 120
        if params is not None and len(params) > 0:
            self.timedelta_seconds = params.get('timedelta_seconds')

        self.timedelta_seconds = round(self.timedelta_seconds)
        if self.timedelta_seconds < 1:
            self.timedelta_seconds = 1

        # Field for timer
        self.timeout_timer: Union[WiredTimer, None] = None

    def _init_stages_objects(self):
        """ Sequentially launch stages initialization """
        if len(self.init_stages) > 0:
            logger.debug(f'Action in pipeline {self.pipeline_name} was already'
                         f' configured. Skip stage')
            return None

        for stage_proxy in self.stages:
            self.init_stages.append(stage_proxy.compile())

    @abstractmethod
    def execute_action(self):
        """ Launch all internally defined stages """
        raise NotImplementedError()

    @property
    def get_db_connector_object(self):
        """
        Return identified database connector object from the action (pipeline)
        if it exists
        """
        for i, stage in enumerate(self.init_stages):
            if isinstance(stage, StageStorageInterface):
                return stage

        return None

    def launch_http_connector(self):
        """
        Find connector stage in the action and execute it.
        Allows to obtained data from external data sources via, for
        example, HTTP protocols
        """
        relevant_info = None
        for current_stage in self.init_stages:
            if isinstance(current_stage, StageHTTPConnector):
                self.connector = current_stage
                relevant_info = current_stage.get()
                return relevant_info

        return relevant_info

    def launch_storage(self, relevant_info: Any):
        """
        Find saver (storage) stage in the action and execute it
        If there is no such a stage - skip this step

        :param relevant_info: information obtained from previous stage to save
        """
        for current_stage in self.init_stages:
            if isinstance(current_stage, StageStorageInterface):
                current_stage.save(relevant_info)

    def launch_core(self, relevant_info: Any):
        """
        Launch core logic with all data

        :param relevant_info: data which were directly obtained
        from connectors or loaded with extractors
        """
        core_output = None
        for current_stage in self.init_stages:
            if isinstance(current_stage, CoreLogicInterface):
                core_output = current_stage.launch(relevant_info, self.db_connectors)

        return core_output

    def launch_senders(self, data_to_send: Dict):
        """ Send desired data to suitable endpoints. Launch all senders in the pipeline """
        for current_stage in self.init_stages:
            if isinstance(current_stage, StageSendInterface):
                current_stage.send(data_to_send)
