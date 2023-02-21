from abc import abstractmethod
from typing import Any, List, Dict
import paho.mqtt.client as mqtt
import requests
from loguru import logger
from paho.mqtt.publish import multiple


class StageSendInterface:
    """ Base class for defining interface for senders """

    def __init__(self, destination: str, **params):
        self.destination = destination
        self.params = params

    @abstractmethod
    def send(self, info_to_send: Any, **kwargs):
        """ Method to send desired message to somewhere """
        raise NotImplementedError()


class MQTTSendStage(StageSendInterface):
    """ Send message to destination via MQTT protocol """

    def __init__(self, destination: str, **params):
        super().__init__(destination, **params)
        self.port = params['port']
        self.topic = params['topic']
        self.label_to_send = params['label_to_send']

    def send(self, data_to_send: Any, **kwargs):
        if isinstance(data_to_send, list) is False:
            data_to_send = [data_to_send]

        messages = []
        for output_data in data_to_send:
            if output_data is None:
                continue

            if self.label_to_send in output_data.keys():
                payload = output_data[self.label_to_send]
                messages.append({'topic': self.topic, 'payload': payload})

        if len(messages) > 0:
            self.send_to_subscribers(messages)

    def send_to_subscribers(self, msgs: List[Dict]):
        """ Send desired messages via MQTT protocol

        :param msgs: list with payloads and topic
        """
        multiple(msgs, hostname=self.destination, port=self.port, client_id="",
                 keepalive=60, will=None, auth=None, tls=None,
                 protocol=mqtt.MQTTv5, transport="tcp")
        logger.debug(f'Successfully send messages to topic {self.topic} via MQTT protocol')


class HTTPPUTSendStage(StageSendInterface):
    """ Send message to destination via HTTP protocol using put method """

    def __init__(self, destination: str, **params):
        super().__init__(destination, **params)
        self.headers = params.get('headers')
        self.label_to_send = params['label_to_send']

    def send(self, data_to_send: Any, **kwargs):
        if isinstance(data_to_send, list) is False:
            data_to_send = [data_to_send]

        for output_data in data_to_send:
            if output_data is None:
                continue

            if self.label_to_send in output_data.keys():
                requests.put(self.destination, headers=self.headers,
                             data=output_data[self.label_to_send])


class HTTPPOSTSendStage(StageSendInterface):
    """ Send message to destination via HTTP protocol using POST method """

    def __init__(self, destination: str, **params):
        super().__init__(destination, **params)
        self.headers = params.get('headers')
        self.label_to_send = params['label_to_send']

    def send(self, data_to_send: Any, **kwargs):
        if isinstance(data_to_send, list) is False:
            data_to_send = [data_to_send]

        for output_data in data_to_send:
            if output_data is None:
                continue

            if self.label_to_send in output_data.keys():
                requests.post(self.destination, headers=self.headers,
                              data=output_data[self.label_to_send])
