import uuid
from typing import Union, Dict

from loguru import logger

from wiredflow.main.actions.stages.http_stage import StageHTTPConnector
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
        self.with_save_action = False
        self.with_db_connector_action = False
        self.with_core_action = False
        self.with_sender = False

        self.stages = []
        self.action = None
        self.db_connectors = []

    def with_http_connector(self, source: str, headers: Dict, **kwargs):
        """
        Add new client into processing pipeline to get data via HTTPS requests

        :param source: endpoint to apply get method
        :param headers: dictionary with headers for request
        """
        self.with_get_request_action = True

        self.stages.append(StageHTTPConnector(source, headers, **kwargs))
        return self

    def with_storage(self, configuration_name: str, **kwargs):
        """ Add data storing functionality into processing pipeline

        :param configuration_name: name of saver to use.
        Possible options:
            - 'json' - save results into json file
            - 'mongo' - save results into mongo DB

        Additional parameters for 'json' saver:
            - folder_to_save - path to the folder where to save json files
        """
        self.with_save_action = True

        self.stages.append({'storage': configuration_name, 'params': kwargs})
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
