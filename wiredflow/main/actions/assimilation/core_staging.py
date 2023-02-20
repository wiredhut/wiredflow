from typing import Union, Callable, Dict

from wiredflow.main.actions.assimilation.interface import ProxyStage
from wiredflow.main.actions.stages.core_stage import CoreLogicInterface


class CoreStageProxy(ProxyStage):
    """
    Class for compiling core logic using custom functions
    """

    def __init__(self, core_logic: Callable, **kwargs):
        self.core_logic = core_logic
        self.kwargs = kwargs

    def compile(self) -> CoreLogicInterface:
        return CoreLogicInterface(self.core_logic, **self.kwargs)
