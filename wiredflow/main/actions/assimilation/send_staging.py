from typing import Union, Callable

from wiredflow.main.actions.assimilation.interface import ProxyStage
from wiredflow.main.actions.stages.send_stage import StageSendInterface, \
    MQTTSendStage, HTTPPUTSendStage, HTTPPOSTSendStage


class SendStageProxy(ProxyStage):
    """
    Class for compiling actual sender for data
    """

    sender_by_name = {'mqtt': MQTTSendStage,
                      'http_put': HTTPPUTSendStage,
                      'http_post': HTTPPOSTSendStage}

    def __init__(self, send_name: Union[str, Callable],
                 destination: str, **kwargs):
        if isinstance(send_name, str):
            self.send_stage = self.sender_by_name[send_name]
        else:
            self.send_stage = send_name

        self.destination = destination
        self.kwargs = kwargs

    def compile(self) -> StageSendInterface:
        """ Compile Database connector stage object """
        return self.send_stage(self.destination, **self.kwargs)
