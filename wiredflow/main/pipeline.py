import uuid
from typing import Union, Dict, Callable

from loguru import logger

from wiredflow.main.actions.assimilation.configuration_staging import ConfigurationStageProxy
from wiredflow.main.actions.assimilation.core_staging import CoreStageProxy
from wiredflow.main.actions.assimilation.http_staging import HTTPStageProxy
from wiredflow.main.actions.assimilation.mqtt_staging import MQTTStageProxy
from wiredflow.main.actions.assimilation.send_staging import SendStageProxy
from wiredflow.main.actions.assimilation.store_staging import StoreStageProxy
from wiredflow.main.template import PipelineActionTemplate
from wiredflow.messages.failures_check import ExecutionStatusChecker
from wiredflow.wiredtimer.timer import WiredTimer


class Pipeline:
    """
    Class for creating and launching graphs with actions.
    Pipeline launch Actions and Action launch Stages
    """

    def __init__(self, pipeline_name: str, use_threads: bool, **params):
        self.pipeline_name = pipeline_name
        self.use_threads = use_threads
        self.params = params

        # Info about actions in the pipeline
        self.with_configuration_action = False
        self.with_get_request_action = False
        self.with_mqtt_connection = False
        self.with_storage_action = False
        self.with_core_action = False
        self.with_sender = False

        self.stages = []
        self.action = None
        self.db_connectors = {}

    def with_configuration(self, configuration: Callable, **kwargs):
        """ Configuration of subsequent stage parameters in the pipeline """
        self.with_configuration_action = True

        self.stages.append(ConfigurationStageProxy(configuration, self.use_threads, **kwargs))
        return self

    def with_http_connector(self,
                            configuration: Union[str, Callable] = 'get',
                            source: Union[str, None] = None,
                            headers: Union[Dict, None] = None, **kwargs):
        """
        Add new client into processing pipeline to get data via HTTPS requests

        :param configuration: name of HTTP client realization to use or custom
        implementation
        :param source: endpoint to apply get method
        :param headers: dictionary with headers for request
        """
        self.with_get_request_action = True

        self.stages.append(HTTPStageProxy(configuration, source, headers,
                                          self.use_threads, **kwargs))
        return self

    def with_mqtt_connector(self,
                            source: Union[str, None] = None,
                            port: int = 1883,
                            topic: str = None,
                            **kwargs):
        """
        Add new client into processing pipeline to get data via MQTT

        :param source: endpoint to subscribe to MQTT broker
        :param port: port for connection
        :param topic: topic for subscription
        """
        self.with_mqtt_connection = True

        self.stages.append(MQTTStageProxy(source, port, topic,
                                          self.use_threads, **kwargs))
        return self

    def with_storage(self, configuration: Union[str, Callable],
                     **kwargs):
        """ Add data storing functionality into processing pipeline

        :param configuration: name of storage to use or custom realization
        Possible options:
            - 'json' - save results into json file
            - 'csv' - save results into csv files locally
            - 'mongo' - save results into mongo DB

        Additional parameters for 'json' or 'csv' storage:
            - folder_to_save - path to the folder where to save json files
            - preprocessing - name of preprocessing to apply or list of
            preprocessors
            Possible options:
                - 'add_datetime' - add datetime label to obtained dictionary

            - mapping - name of mapping procedure to apply during save stage
            Possible variants:
                - 'update' - update dictionary with new kye-values pairs
                - 'overwrite' - create file from scratch
                - 'extend' - if the structure list-related - then just add new
                dictionaries to existing ones
        """
        self.with_storage_action = True

        # Define unique name for storage stage
        if isinstance(configuration, str) is True:
            stage_id = f'{configuration}_in_{self.pipeline_name}'
        else:
            stage_id = f'custom_in_{self.pipeline_name}'
        self.stages.append(StoreStageProxy(configuration, stage_id, self.use_threads,
                                           **kwargs))
        return self

    def with_core_logic(self, configuration: Callable, **kwargs):
        """
        Define custom core logic into processing pipeline and define parameters
        to it
        """
        self.with_core_action = True

        self.stages.append(CoreStageProxy(configuration, self.use_threads, **kwargs))
        return self

    def send(self, configuration: Union[str, Callable] = 'mqtt',
             destination: Union[str, None] = None,
             label_to_send: Union[str, None] = None, **kwargs):
        """
        Configure sender for desired data aggregates

        :param configuration: name of sender to apply or custom implementation.
        Possible options:
            - 'mqtt' to send messages via MQTT
            - 'http_post' to send message via HTTP post request
            - 'http_put' to send message via HTTP put request
        :param destination: ip of destination - where to send messages
        :param label_to_send: name of data aggregation to send
        """
        self.with_sender = True
        kwargs = {**kwargs, **{'label_to_send': label_to_send}}

        self.stages.append(SendStageProxy(configuration, destination,
                                          self.use_threads, **kwargs))
        return self

    def run(self, timeout_timer: WiredTimer, failures_checker: ExecutionStatusChecker):
        """ Launch compiled action in current pipeline """
        common_message = f'Launch pipeline "{self.pipeline_name}"'
        if timeout_timer.execution_seconds is None:
            logger.info(common_message)
        else:
            logger.info(f'{common_message}. Execution timeout, seconds: {timeout_timer.execution_seconds}')

        self.action.db_connectors = self.db_connectors
        self.action.timeout_timer = timeout_timer
        self.action.execute_action(failures_checker)

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
