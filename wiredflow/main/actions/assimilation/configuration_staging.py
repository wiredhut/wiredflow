from typing import Union, Callable, Dict

from wiredflow.main.actions.assimilation.interface import ProxyStage
from wiredflow.main.actions.stages.configuration_stage import \
    ConfigurationInterface


class ConfigurationStageProxy(ProxyStage):
    """
    Class for compiling configuration logic using custom functions
    """

    def __init__(self, configurator: Callable, **kwargs):
        self.configurator = configurator
        self.kwargs = kwargs

    def compile(self) -> ConfigurationInterface:
        return ConfigurationInterface(self.configurator, **self.kwargs)
