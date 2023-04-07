from typing import Callable
from wiredflow.main.actions.assimilation.interface import ProxyStage
from wiredflow.main.actions.stages.configuration_stage import \
    ConfigurationInterface


class ConfigurationStageProxy(ProxyStage):
    """
    Class for compiling configuration logic using custom functions
    """

    def __init__(self, configuration: Callable, use_threads: bool, **kwargs):
        self.configuration = configuration
        self.use_threads = use_threads
        self.kwargs = kwargs

    def compile(self) -> ConfigurationInterface:
        return ConfigurationInterface(self.configuration, self.use_threads, **self.kwargs)
