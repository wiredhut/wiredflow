from abc import abstractmethod
from typing import List, Any, Optional

from loguru import logger

from wiredflow.main.actions.stages.http_stage import StageHTTPConnector


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

    def __init__(self, pipeline_name: str, stages: List[dict],
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
        self.timedelta_minutes = 1440
        if params is not None and len(params) > 0:
            self.timedelta_minutes = params.get('timedelta_minutes')

        self.timedelta_minutes = round(self.timedelta_minutes)
        if self.timedelta_minutes < 1:
            self.timedelta_minutes = 1

    def _init_stages_objects(self):
        """ Sequentially launch stages initialization """
        if len(self.init_stages) > 0:
            logger.debug(f'Action in pipeline {self.pipeline_name} was already'
                         f' configured. Skip stage')
            return None

        self.init_stages = self.stages

    @abstractmethod
    def execute_action(self):
        """ Launch all internally defined stages """
        raise NotImplementedError()

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

    def launch_saver(self, relevant_info: Any):
        """
        Find saver stage in the action and execute it
        If there is no such a stage - skip this step

        :param relevant_info: information obtained from previous stage to save
        """
        if self.connector is None:
            raise ValueError('To launch saver connector is required')
        for current_stage in self.init_stages:
            if isinstance(current_stage, str):
                current_stage.save(relevant_info)
