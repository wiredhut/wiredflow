import json
from abc import abstractmethod
from typing import Any, List, Dict, Callable
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
                data = output_data[self.label_to_send]
                if isinstance(data, dict):
                    data = json.dumps(data)
                requests.put(self.destination, headers=self.headers, data=data)


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
                data = output_data[self.label_to_send]
                if isinstance(data, dict):
                    data = json.dumps(data)
                requests.post(self.destination, headers=self.headers, data=data)


class CustomSendStage:
    """ Class for launching custom implementations of Send operation """

    def __init__(self, function_to_launch: Callable, **kwargs):
        self.function_to_launch = function_to_launch
        self.kwargs = kwargs

    def send(self, data_to_send: Any, **params):
        if data_to_send is None:
            # There is no info to send
            return None

        arguments = self.kwargs
        if isinstance(params, dict) is True:
            arguments = {**self.kwargs, **params}

        return self.function_to_launch(data_to_send, **arguments)
