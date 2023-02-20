from time import sleep
import json

from loguru import logger
import paho.mqtt.client as mqtt
from paho.mqtt.publish import multiple


def configure_int_mqtt_broker():
    """
    Generate messages with random integers and then send messages through
    configured MQTT broker
    """
    topic = '/demo/integers'
    # Waiting for successful subscriber initialization
    sleep(5)

    for generated_int in range(0, 500):
        payload = {"Generated number": str(generated_int)}
        current_message = {'topic': topic, 'payload': json.dumps(payload)}
        multiple([current_message], hostname='localhost', port=1883,
                 client_id="", keepalive=60, will=None, auth=None, tls=None,
                 protocol=mqtt.MQTTv5, transport="tcp")

        logger.debug(f'MQTT local broker. Send generated int {generated_int} from topic {topic}')
        sleep(1)
