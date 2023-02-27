import string
from time import sleep
import json
from typing import Union

from loguru import logger
import paho.mqtt.client as mqtt
from paho.mqtt.publish import multiple

from wiredflow.wiredtimer.timer import WiredTimer


def configure_int_mqtt_broker(execution_seconds: Union[int, None] = None):
    """
    Generate messages with integers values and then send messages through
    configured MQTT broker
    """
    timeout_timer = WiredTimer(execution_seconds)
    topic = '/demo/integers'
    # Waiting for successful subscriber initialization
    sleep(3)

    common_message = f'Start mock MQTT broker in separate process - topic: {topic}'
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


def configure_str_mqtt_broker(execution_seconds: Union[int, None] = None):
    """
    Generate messages with letters and then send messages through
    configured MQTT broker
    """
    timeout_timer = WiredTimer(execution_seconds)
    topic = '/demo/letters'
    # Waiting for successful subscriber initialization
    sleep(3)

    common_message = f'Start mock MQTT broker in separate process - topic: {topic}'
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
