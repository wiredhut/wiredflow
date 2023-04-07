from abc import abstractmethod
from typing import Union

import paho.mqtt.client as mqtt
from loguru import logger


class StageMQTTConnectorInterface:
    """
    Base class for MQTT-like connector implementation
    for passively getting data from brokers
    """

    def __init__(self, source: Union[str, None], port: int,
                 topic: Union[str, None], **params):
        self.source = source
        self.port = port
        self.topic = topic
        self.params = params

        # Optional parameters for authentication
        self.username = self.params.get('username')
        self.password = self.params.get('password')

    @abstractmethod
    def configure_client(self, client: mqtt.Client):
        raise NotImplementedError()


def mqtt_on_connect(client, userdata, flags, rc):
    logger.debug(f"Alert MQTT subscriber connected to topic {userdata.topic} "
                 f"with result code {str(rc)}")
    client.subscribe(userdata.topic)


def mqtt_on_message(client, userdata, message):
    """ Activate every time client got the message via MQTT """
    userdata.messages.append(message)
    userdata.launch_processors()


class DefaultMQTTConnector(StageMQTTConnectorInterface):

    def __init__(self, source: Union[str, None], port: int,
                 topic: Union[str, None], use_threads: bool, **params):
        super().__init__(source, port, topic, **params)
        self.use_threads = use_threads

    def configure_client(self, client: mqtt.Client):
        client.on_connect = mqtt_on_connect
        client.on_message = mqtt_on_message

        client.connect(self.source, self.port, 60)
        return client
