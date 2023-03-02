from abc import abstractmethod
from typing import List, Any, Dict, Union

from loguru import logger

from wiredflow.main.actions.assimilation.interface import ProxyStage
from wiredflow.main.actions.stages.configuration_stage import \
    ConfigurationInterface
from wiredflow.main.actions.stages.core_stage import CoreLogicInterface
from wiredflow.main.actions.stages.http_stage import HTTPConnectorInterface, \
    StageCustomHTTPConnector
from wiredflow.main.actions.stages.send_stage import StageSendInterface, \
    CustomSendStage
from wiredflow.main.actions.stages.storage_stage import StageStorageInterface
from wiredflow.main.multistep import is_current_stage_multi_step
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
        self.params = params
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
            if params.get('timedelta_seconds') is not None:
                self.timedelta_seconds = params.get('timedelta_seconds')

        self.launch_time = None
        if params is not None and len(params) > 0:
            self.launch_time = params.get('launch_time')

        if self.timedelta_seconds < 1:
            logger.info(f'Replace timedelta values with 1 because value {self.timedelta_seconds}'
                        f'is too small')
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

    def perform_action(self):
        """ Launch all processes for desired action. Default execution strategy """
        input_data = None
        configured_params = None
        for stage_id, current_stage in enumerate(self.init_stages):

            if is_current_stage_multi_step(current_stage) is False:
                output_data = self.launch_stage(current_stage, input_data,
                                                configured_params)
                input_data = output_data.get('data')
                configured_params = output_data.get('configured_params')
            else:
                # Multi step function - there is a need to launch several times
                for output_data in self.launch_multi_stage(current_stage, input_data, configured_params):
                    part_input_data = output_data.get('data')
                    part_configured_params = output_data.get('configured_params')

                    # Launch all defined post-processing
                    if stage_id + 1 == len(self.init_stages):
                        # That was last stage
                        continue

                    for remained_stage in self.init_stages[stage_id + 1:]:
                        output_data = self.launch_stage(remained_stage,
                                                        part_input_data,
                                                        part_configured_params)
                        input_data = output_data.get('data')
                        configured_params = output_data.get('configured_params')
                return None

    def launch_stage(self, current_stage, input_data, configured_params) -> Dict:
        """ Launch desired stage with configured parameters and data as input """
        is_custom_connector = isinstance(current_stage, StageCustomHTTPConnector)

        if isinstance(current_stage, ConfigurationInterface):
            ##############################
            # Launch configuration stage #
            ##############################
            configured_params = current_stage.launch(**self.db_connectors)
            return {'configured_params': configured_params}

        elif isinstance(current_stage, HTTPConnectorInterface) or is_custom_connector:
            ###########################
            # Launch connection stage #
            ###########################
            if configured_params is None:
                return {'data': current_stage.get()}
            else:
                return {'data':  current_stage.get(**configured_params)}

        elif isinstance(current_stage, StageStorageInterface):
            #####################
            # Launch save stage #
            #####################
            if input_data is None:
                # Does not save any data
                return {'data': input_data, 'configured_params': configured_params}

            if configured_params is None:
                current_stage.save(input_data)
            else:
                current_stage.save(input_data, **configured_params)

            # Pass the same data further
            return {'data': input_data, 'configured_params': configured_params}

        elif isinstance(current_stage, CoreLogicInterface):
            ###############################
            # Launch core logic execution #
            ###############################
            if configured_params is None:
                core_output = current_stage.launch(input_data, self.db_connectors)
            else:
                core_output = current_stage.launch(input_data, self.db_connectors,
                                                   **configured_params)
            return {'data': core_output}

        elif isinstance(current_stage, StageSendInterface) or isinstance(current_stage, CustomSendStage):
            #####################
            # Launch send stage #
            #####################
            if configured_params is None:
                current_stage.send(input_data)
            else:
                current_stage.send(input_data, **configured_params)

            # Pass the same data further
            return {'data': input_data, 'configured_params': configured_params}
        else:
            raise ValueError(f'Wiredflow does not support {current_stage} stage type launch')

    def launch_multi_stage(self, current_stage, input_data, configured_params) -> Dict:
        """ Launch generator custom functions to generate parameters or data """
        if isinstance(current_stage, ConfigurationInterface):
            configured_params = current_stage.launch(**self.db_connectors)
            for params in configured_params:
                yield {'configured_params': params}

        elif isinstance(current_stage, CoreLogicInterface):
            if configured_params is None:
                core_output = current_stage.launch(input_data, self.db_connectors)
            else:
                core_output = current_stage.launch(input_data, self.db_connectors,
                                                   **configured_params)

            for output in core_output:
                yield {'data': output}

        elif isinstance(current_stage, StageCustomHTTPConnector):
            if configured_params is None:
                request_data = current_stage.get()
            else:
                request_data = current_stage.get(**configured_params)

            for data in request_data:
                yield {'data': data}

        else:
            raise ValueError(f'Wiredflow does not support generator launch for {current_stage} stage type')


def calculate_break_interval(timedelta_seconds) -> float:
    number_of_seconds_to_break = timedelta_seconds / 2
    if number_of_seconds_to_break < 0.5:
        number_of_seconds_to_break = 0.5
    if number_of_seconds_to_break > 10:
        number_of_seconds_to_break = 10

    return number_of_seconds_to_break
