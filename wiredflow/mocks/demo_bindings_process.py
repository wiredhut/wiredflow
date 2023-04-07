import json
import string

from http.server import HTTPServer
from time import sleep
from typing import Union

from loguru import logger
from paho.mqtt.publish import multiple
import paho.mqtt.client as mqtt

from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.http_server import RandomIntegersHandler, INT_PORT, \
    HTTP_LOCALHOST, _start_mock_http_server, STR_PORT, RandomStringHandler
from wiredflow.wiredtimer.timer import WiredTimer


def stage_mock_int_http_server(**kwargs):
    server = HTTPServer((HTTP_LOCALHOST, INT_PORT), RandomIntegersHandler)
    execution_seconds = kwargs.get('execution_seconds')
    return _start_mock_http_server(execution_seconds, server)


def stage_mock_str_http_server(**kwargs):
    server = HTTPServer((HTTP_LOCALHOST, STR_PORT), RandomStringHandler)
    execution_seconds = kwargs.get('execution_seconds')
    return _start_mock_http_server(execution_seconds, server)


def stage_int_mqtt_broker(**kwargs):
    """
    Generate messages with integers values and then send messages through
    configured MQTT broker
    """
    execution_seconds = kwargs.get('execution_seconds')
    timeout_timer = WiredTimer(execution_seconds)
    topic = '/demo/integers'
    # Waiting for successful subscriber initialization
    sleep(3)

    common_message = f'Start mock MQTT broker as part of pipeline - topic: {topic}'
    if execution_seconds is None:
        logger.info(common_message)
    else:
        logger.info(f'{common_message}. Execution timeout, seconds: {execution_seconds}')

    for generated_int in range(0, 500):
        payload = {"Generated number": str(generated_int)}
        current_message = {'topic': topic, 'payload': json.dumps(payload)}
        multiple([current_message], hostname='localhost', port=1883,
                 client_id="", keepalive=60, will=None, auth=None, tls=None,
                 protocol=mqtt.MQTTv5, transport="tcp")

        logger.debug(f'MQTT local broker. Send generated int {generated_int} from topic {topic}')
        sleep(1)

        if timeout_timer.is_limit_reached():
            # Finish execution
            return None


def stage_str_mqtt_broker(**kwargs):
    """
    Generate messages with letters and then send messages through
    configured MQTT broker
    """
    execution_seconds = kwargs.get('execution_seconds')
    timeout_timer = WiredTimer(execution_seconds)
    topic = '/demo/letters'
    # Waiting for successful subscriber initialization
    sleep(3)

    common_message = f'Start mock MQTT broker as part of pipeline - topic: {topic}'
    if execution_seconds is None:
        logger.info(common_message)
    else:
        logger.info(f'{common_message}. Execution timeout, seconds: {execution_seconds}')
    for generated_str in string.ascii_letters:
        payload = {"Generated letter": generated_str}
        current_message = {'topic': topic, 'payload': json.dumps(payload)}
        multiple([current_message], hostname='localhost', port=1883,
                 client_id="", keepalive=60, will=None, auth=None, tls=None,
                 protocol=mqtt.MQTTv5, transport="tcp")

        logger.debug(f'MQTT local broker. Send generated letter {generated_str} from topic {topic}')
        sleep(1)

        if timeout_timer.is_limit_reached():
            # Finish execution
            return None


def launch_demo_with_int_http_connector_processes(flow_builder: FlowBuilder,
                                                  execution_seconds: Union[int, None] = None):
    """ Launch flow processing and local HTTP server in separate processes """
    # Add additional pipeline in the service
    flow_builder.add_pipeline('http_int_demo', timedelta_seconds=60,
                              delay_seconds=0) \
        .with_core_logic(stage_mock_int_http_server,
                         execution_seconds=execution_seconds)

    # Launch the service with two pipelines (each pipeline in different process)
    service = flow_builder.build()
    service.launch_flow(execution_seconds)


def launch_demo_with_several_http_connectors_processes(flow_builder: FlowBuilder,
                                                       execution_seconds: Union[int, None] = None):
    flow_builder.add_pipeline('http_int_demo', timedelta_seconds=60, delay_seconds=0) \
        .with_core_logic(stage_mock_int_http_server,
                         execution_seconds=execution_seconds)

    flow_builder.add_pipeline('http_str_demo', timedelta_seconds=60, delay_seconds=0) \
        .with_core_logic(stage_mock_str_http_server,
                         execution_seconds=execution_seconds)

    service = flow_builder.build()
    service.launch_flow(execution_seconds)


def launch_demo_with_several_mqtt_connectors_processes(flow_builder: FlowBuilder,
                                                       execution_seconds: Union[int, None] = None):
    """ Launch flow processing and local MQTT broker in separate processes """
    flow_builder.add_pipeline('mqtt_int_demo', timedelta_seconds=60, delay_seconds=0) \
        .with_core_logic(stage_int_mqtt_broker, execution_seconds=execution_seconds)

    flow_builder.add_pipeline('mqtt_str_demo', timedelta_seconds=60, delay_seconds=0) \
        .with_core_logic(stage_str_mqtt_broker, execution_seconds=execution_seconds)

    service = flow_builder.build()
    service.launch_flow(execution_seconds)
