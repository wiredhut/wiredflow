from typing import Callable

from loguru import logger


class ConfigurationInterface:
    """ Base class for defining interface for core logic connectors """

    def __init__(self, function_to_launch: Callable, **kwargs):
        self.function_to_launch = function_to_launch
        self.kwargs = kwargs

    def launch(self, **kwargs):
        logger.debug(f'Launch configuration stage')

        # Merge parameters
        kwargs = {**self.kwargs, **kwargs}
        return self.function_to_launch(**kwargs)
