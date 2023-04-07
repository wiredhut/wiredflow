from typing import Union, Callable, Dict

from wiredflow.main.actions.assimilation.interface import ProxyStage
from wiredflow.main.actions.stages.http_stage import HTTPConnectorInterface, \
    StageGetHTTPConnector, StagePostHTTPConnector, StageCustomHTTPConnector


class HTTPStageProxy(ProxyStage):
    """ Class for compiling actual HTTP connectors via Stages when it is required """

    http_stage_by_name = {'get': StageGetHTTPConnector,
                          'post': StagePostHTTPConnector}

    def __init__(self,
                 configuration: Union[str, Callable], source: Union[str, None],
                 headers: Union[Dict, None], use_threads: bool, **kwargs):
        self.custom_realization = False
        if isinstance(configuration, str):
            self.http_stage = self.http_stage_by_name[configuration]
        else:
            # Custom function to process HTTP requests
            self.custom_realization = True
            self.http_stage = configuration

        self.source = source
        self.headers = headers
        self.kwargs = kwargs
        self.use_threads = use_threads

    def compile(self) -> Union[HTTPConnectorInterface, StageCustomHTTPConnector]:
        """ Compile HTTP connector stage object """
        if self.custom_realization is True:
            # Custom implementation through function
            if self.source is not None:
                self.kwargs['source'] = self.source
            if self.headers is not None:
                self.kwargs['headers'] = self.headers
            return StageCustomHTTPConnector(self.http_stage, self.use_threads, **self.kwargs)

        return self.http_stage(self.source, self.headers, self.use_threads, **self.kwargs)
