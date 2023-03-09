from typing import Callable
from wiredflow.main.actions.assimilation.interface import ProxyStage
from wiredflow.main.actions.stages.configuration_stage import \
    ConfigurationInterface


class ConfigurationStageProxy(ProxyStage):
    """
    Class for compiling configuration logic using custom functions
    """

    def __init__(self, configuration: Callable, **kwargs):
        self.configuration = configuration
        self.kwargs = kwargs

    def compile(self) -> ConfigurationInterface:
        return ConfigurationInterface(self.configuration, **self.kwargs)
