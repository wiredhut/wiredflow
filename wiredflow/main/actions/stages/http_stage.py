from abc import abstractmethod
from typing import Dict, Union

import requests


class HTTPConnectorInterface:
    """ Base class which define common interface for all HTTP data request """

    def __init__(self, source: Union[str, None], headers: Union[Dict, None], **params):
        self.connector_name = 'HTTP/HTTPS connector'
        self.source = source
        self.headers = headers

    @abstractmethod
    def get(self, **params):
        """ Get data via HTTP request """
        raise NotImplementedError()

    @property
    def get_connector_name(self):
        return self.connector_name


class StageGetHTTPConnector(HTTPConnectorInterface):
    """
    Base class for HTTP-like connector implementation
    for actively requesting desired data using GET method
    """

    def __init__(self, source: Union[str, None], headers: Union[Dict, None], **params):
        super().__init__(source, headers, **params)

    def get(self, **params):
        http_info = requests.get(self.source, headers=self.headers, **params)
        return http_info.json()


class StagePostHTTPConnector(HTTPConnectorInterface):
    """
    Class for requesting data using POST method (useful when it is required to
    use SQL commands to grab data)
    """

    def __init__(self, source: Union[str, None], headers: Union[Dict, None], **params):
        super().__init__(source, headers, **params)

    def get(self, **params):
        response = requests.request("POST", self.source, headers=self.headers,
                                    **params)
        return response.json()
