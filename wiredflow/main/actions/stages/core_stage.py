from typing import Any, Dict, Callable

from loguru import logger


class CoreLogicInterface:
    """ Base class for defining interface for core logic connectors """

    def __init__(self, function_to_launch: Callable, use_threads: bool, **kwargs):
        self.function_to_launch = function_to_launch
        self.kwargs = kwargs
        self.use_threads = use_threads

    def launch(self, relevant_info: Any, db_connectors: Dict, **kwargs):
        arguments = {**{'relevant_info': relevant_info}, **{'db_connectors': db_connectors}}
        arguments = {**arguments, **kwargs}
        logger.debug(f'Launch core logic stage')
        return self.function_to_launch(**arguments)
