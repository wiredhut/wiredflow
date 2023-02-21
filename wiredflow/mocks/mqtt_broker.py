import string
from time import sleep
import json

from loguru import logger
import paho.mqtt.client as mqtt
from paho.mqtt.publish import multiple


def configure_int_mqtt_broker():
    """
    Generate messages with integers values and then send messages through
    configured MQTT broker
    """
    topic = '/demo/integers'
    # Waiting for successful subscriber initialization
    sleep(5)

    logger.info(f'Start mock MQTT broker in separate process - topic: {topic}')
    for generated_int in range(0, 500):
        payload = {"Generated number": str(generated_int)}
        current_message = {'topic': topic, 'payload': json.dumps(payload)}
        multiple([current_message], hostname='localhost', port=1883,
                 client_id="", keepalive=60, will=None, auth=None, tls=None,
                 protocol=mqtt.MQTTv5, transport="tcp")

        logger.debug(f'MQTT local broker. Send generated int {generated_int} from topic {topic}')
        sleep(1)


def configure_str_mqtt_broker():
    """
    Generate messages with letters and then send messages through
    configured MQTT broker
    """
    topic = '/demo/letters'
    # Waiting for successful subscriber initialization
    sleep(5)

    logger.info(f'Start mock MQTT broker in separate process - topic: {topic}')
    for generated_str in string.ascii_letters:
        payload = {"Generated letter": generated_str}
        current_message = {'topic': topic, 'payload': json.dumps(payload)}
        multiple([current_message], hostname='localhost', port=1883,
                 client_id="", keepalive=60, will=None, auth=None, tls=None,
                 protocol=mqtt.MQTTv5, transport="tcp")

        logger.debug(
            f'MQTT local broker. Send generated letter {generated_str} from topic {topic}')
        sleep(1)