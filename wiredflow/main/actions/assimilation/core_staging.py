from typing import Callable

from wiredflow.main.actions.assimilation.interface import ProxyStage
from wiredflow.main.actions.stages.core_stage import CoreLogicInterface


class CoreStageProxy(ProxyStage):
    """
    Class for compiling core logic using custom functions
    """

    def __init__(self, configuration: Callable, **kwargs):
        self.configuration = configuration
        self.kwargs = kwargs

    def compile(self) -> CoreLogicInterface:
        return CoreLogicInterface(self.configuration, **self.kwargs)
