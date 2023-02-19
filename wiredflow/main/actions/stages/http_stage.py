from typing import Dict

import requests


class StageHTTPConnector:
    """
    Base class for HTTP-like connector implementation
    for actively requesting desired data
    """

    def __init__(self, source: str, headers: Dict, **params):
        self.connector_name = 'HTTP/HTTPS connector'
        self.source = source
        self.headers = headers

    def get(self):
        http_info = requests.get(self.source, headers=self.headers)
        return http_info.json()

    @property
    def get_connector_name(self):
        return self.connector_name
