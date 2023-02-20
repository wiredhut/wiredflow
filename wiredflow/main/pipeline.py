import uuid
from typing import Union, Dict, Callable

from loguru import logger

from wiredflow.main.actions.assimilation.core_staging import CoreStageProxy
from wiredflow.main.actions.assimilation.http_staging import HTTPStageProxy
from wiredflow.main.actions.assimilation.send_staging import SendStageProxy
from wiredflow.main.actions.assimilation.store_staging import StoreStageProxy
from wiredflow.main.template import PipelineActionTemplate


class Pipeline:
    """
    Class for creating and launching graphs with actions.
    Pipeline launch Actions and Action launch Stages
    """

    def __init__(self, pipeline_name: str, **params):
        self.pipeline_name = pipeline_name
        self.params = params

        # Info about actions in the pipeline
        self.with_get_request_action = False
        self.with_mqtt_connection = False
        self.with_storage_action = False
        self.with_core_action = False
        self.with_sender = False

        self.stages = []
        self.action = None
        self.db_connectors = []

    def with_http_connector(self,
                            name: Union[str, Callable] = 'default',
                            source: Union[str, None] = None,
                            headers: Union[Dict, None] = None, **kwargs):
        """
        Add new client into processing pipeline to get data via HTTPS requests

        :param name: name of HTTP client realization to use or custom realization
        :param source: endpoint to apply get method
        :param headers: dictionary with headers for request
        """
        self.with_get_request_action = True

        self.stages.append(HTTPStageProxy(name, source, headers, **kwargs))
        return self

    def with_storage(self, storage_name: Union[str, Callable], **kwargs):
        """ Add data storing functionality into processing pipeline

        :param storage_name: name of storage to use or custom realization
        Possible options:
            - 'json' - save results into json file
            - 'mongo' - save results into mongo DB

        Additional parameters for 'json' storage:
            - folder_to_save - path to the folder where to save json files
            - preprocessing - name of preprocessor(s) for JSON storage engine.
            Possible variants:
                - 'update' - update dictionary with new kye-values pairs
                - 'overwrite' - create file from scratch
                - 'extend' - if the structure list-related - then just add new
                dictionaries to existing ones
                - 'add_datetime' - add datetime label to obtained dictionary
        """
        self.with_storage_action = True

        # Define unique name for storage stage
        stage_id = f'{storage_name} in {self.pipeline_name}'
        self.stages.append(StoreStageProxy(storage_name, stage_id, **kwargs))
        return self

    def with_core_logic(self, core_logic: Callable, **kwargs):
        """
        Define custom core logic into processing pipeline and define parameters
        to it
        """
        self.with_core_action = True

        self.stages.append(CoreStageProxy(core_logic, **kwargs))
        return self

    def send(self, send_name: Union[str, Callable] = 'mqtt',
             destination: Union[str, None] = None,
             data_aggregate: Union[str, None] = None, **kwargs):
        """
        Configure sender for desired data aggregates

        :param send_name: name of sender to apply or custom implementation
        :param destination: name of topic to send message to or source
        :param data_aggregate: name of data aggregation
        """
        self.with_sender = True
        kwargs = {**kwargs, **{'data_aggregate': data_aggregate}}

        self.stages.append(SendStageProxy(send_name, destination, **kwargs))
        return self

    def run(self):
        """ Launch compiled action in current pipeline """
        logger.info(f'Launch pipeline "{self.pipeline_name}"')

        self.action.db_connectors = self.db_connectors
        self.action.execute_action()

    def create_action(self):
        """
        Internal objects initialization.
        Based on pipeline template (determined automatically) action assigned
        """
        # Generate action based on current pipeline structure
        template = PipelineActionTemplate(self, **self.params)
        self.action = template.compile_action()


def generate_pipeline_name(pipeline_name: Union[str, None]) -> str:
    """ Generate unique pipeline name if it was not defined yet """
    if pipeline_name is None:
        # Generate name for pipeline
        pipeline_name = str(uuid.uuid4())

    return pipeline_name
