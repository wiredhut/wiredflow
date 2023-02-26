from typing import Union, Callable

from wiredflow.main.actions.assimilation.interface import ProxyStage
from wiredflow.main.actions.stages.send_stage import StageSendInterface, \
    MQTTSendStage, HTTPPUTSendStage, HTTPPOSTSendStage, CustomSendStage


class SendStageProxy(ProxyStage):
    """
    Class for compiling actual sender for data
    """

    sender_by_name = {'mqtt': MQTTSendStage,
                      'http_put': HTTPPUTSendStage,
                      'http_post': HTTPPOSTSendStage}

    def __init__(self, send_name: Union[str, Callable],
                 destination: str, **kwargs):
        self.custom_realization = False
        if isinstance(send_name, str):
            self.send_stage = self.sender_by_name[send_name]
        else:
            self.custom_realization = True
            self.send_stage = send_name

        self.destination = destination
        self.kwargs = kwargs

    def compile(self) -> Union[StageSendInterface, CustomSendStage]:
        """ Compile Database connector stage object """
        if self.custom_realization is True:
            # Custom implementation through function
            if self.destination is not None:
                self.kwargs['destination'] = self.destination
            return CustomSendStage(self.send_stage, **self.kwargs)

        return self.send_stage(self.destination, **self.kwargs)
