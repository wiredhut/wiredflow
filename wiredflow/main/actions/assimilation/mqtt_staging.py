from typing import Union

from wiredflow.main.actions.assimilation.interface import ProxyStage
from wiredflow.main.actions.stages.mqtt_stage import \
    StageMQTTConnectorInterface, DefaultMQTTConnector


class MQTTStageProxy(ProxyStage):
    """ Class for compiling actual MQTT connectors via Stages when it is required """

    def __init__(self, source: Union[str, None], port: int,
                 topic: Union[str, None], **kwargs):
        self.source = source
        self.port = port
        self.topic = topic
        self.kwargs = kwargs

    def compile(self) -> StageMQTTConnectorInterface:
        """ Compile HTTP connector stage object """
        return DefaultMQTTConnector(self.source, self.port, self.topic, **self.kwargs)
