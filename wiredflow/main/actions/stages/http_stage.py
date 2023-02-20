from abc import abstractmethod
from typing import Dict, Union

import requests


class HTTPInterface:
    """ Base class which define common interface for all HTTP data request """

    def __init__(self, source: Union[str, None], headers: Union[Dict, None], **params):
        self.connector_name = 'HTTP/HTTPS connector'
        self.source = source
        self.headers = headers

    @abstractmethod
    def get(self):
        """ Get data via HTTP request """
        raise NotImplementedError()

    @property
    def get_connector_name(self):
        return self.connector_name


class StageHTTPConnector(HTTPInterface):
    """
    Base class for HTTP-like connector implementation
    for actively requesting desired data
    """

    def __init__(self, source: Union[str, None], headers: Union[Dict, None], **params):
        super().__init__(source, headers, **params)

    def get(self):
        http_info = requests.get(self.source, headers=self.headers)
        return http_info.json()
