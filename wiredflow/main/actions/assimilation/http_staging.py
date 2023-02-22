from typing import Union, Callable, Dict

from wiredflow.main.actions.assimilation.interface import ProxyStage
from wiredflow.main.actions.stages.http_stage import HTTPConnectorInterface, \
    StageGetHTTPConnector, StagePostHTTPConnector


class HTTPStageProxy(ProxyStage):
    """ Class for compiling actual HTTP connectors via Stages when it is required """

    http_stage_by_name = {'get': StageGetHTTPConnector,
                          'post': StagePostHTTPConnector}

    def __init__(self,
                 name: Union[str, Callable], source: Union[str, None],
                 headers: Union[Dict, None], **kwargs):
        if isinstance(name, str):
            if name == 'default' and source is None:
                raise ValueError(f'"source" parameter must be specified for {name} HTTP connector')
            self.http_stage = self.http_stage_by_name[name]
        else:
            # Custom class to process HTTP requests
            self.http_stage = name

        self.source = source
        self.headers = headers
        self.kwargs = kwargs

    def compile(self) -> HTTPConnectorInterface:
        """ Compile HTTP connector stage object """
        return self.http_stage(self.source, self.headers, **self.kwargs)
