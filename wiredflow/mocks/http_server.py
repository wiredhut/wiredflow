import json

from http.server import HTTPServer, BaseHTTPRequestHandler
import random
from typing import Union
import string

from attrs import asdict
from loguru import logger

HTTP_LOCALHOST = "127.0.0.1"
INT_PORT = 8027
STR_PORT = 8026


class RandomIntegersHandler(BaseHTTPRequestHandler):
    """
    Class for imitating API with GET requests. Return random integers values
    """

    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        send_data = self.rfile.read(content_length)
        send_data = send_data.decode('utf-8')

        print(f'Local HTTP server obtain data via PUT method: {send_data}')

        jsonbytes = self._prepare_json_response()
        self.wfile.write(jsonbytes)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        send_data = self.rfile.read(content_length)
        send_data = send_data.decode('utf-8')

        print(f'Local HTTP server obtain data via POST method: {send_data}')

        jsonbytes = self._prepare_json_response()
        self.wfile.write(jsonbytes)

    def do_GET(self):
        """ Generate random number and send it by request """
        data_to_send = json.dumps([{'Generated random number': random.randint(0, 100)}])
        logger.trace(f'HTTP server send data: {data_to_send} by request')

        jsonbytes = self._prepare_json_response(data_to_send)
        self.wfile.write(jsonbytes)

    def _prepare_json_response(self, data_to_send: Union[str, None] = None) -> bytes:
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        if data_to_send is None:
            data_to_send = json.dumps(json.dumps({'correct': True}),
                                      indent=4, default=asdict)

        return data_to_send.encode(encoding='utf_8')


class RandomStringHandler(BaseHTTPRequestHandler):
    """
    Class for imitating API with GET requests. Return random letters
    """

    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        send_data = self.rfile.read(content_length)
        send_data = send_data.decode('utf-8')

        print(f'Local HTTP server obtain data via PUT method: {send_data}')

        jsonbytes = self._prepare_json_response()
        self.wfile.write(jsonbytes)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        send_data = self.rfile.read(content_length)
        send_data = send_data.decode('utf-8')

        print(f'Local HTTP server obtain data via POST method: {send_data}')

        jsonbytes = self._prepare_json_response()
        self.wfile.write(jsonbytes)

    def do_GET(self):
        """ Generate random number and send it by request """
        data_to_send = json.dumps([{'Generated random letter': random.choice(string.ascii_letters)}])
        logger.trace(f'HTTP server send data: {data_to_send} by request')

        jsonbytes = self._prepare_json_response(data_to_send)
        self.wfile.write(jsonbytes)

    def _prepare_json_response(self,
                               data_to_send: Union[str, None] = None) -> bytes:
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        if data_to_send is None:
            data_to_send = json.dumps(json.dumps({'correct': True}),
                                      indent=4, default=asdict)

        return data_to_send.encode(encoding='utf_8')


def _start_mock_http_server(execution_seconds: Union[int, None],
                            server: HTTPServer):
    common_message = f'Start mock HTTP server in separate process: {HTTP_LOCALHOST},' \
                     f' port {server.server_port}'
    if execution_seconds is None:
        logger.info(common_message)
    else:
        logger.info(
            f'{common_message}. Execution timeout, seconds: {execution_seconds}')

    # Forever loop
    if execution_seconds is None:
        server.serve_forever()

    # Execute server for desired number of seconds
    # Solution from https://stackoverflow.com/a/61644043/12195438
    try:
        server.timeout = execution_seconds
        server.handle_timeout = lambda: (_ for _ in ()).throw(TimeoutError())
        while True:
            server.handle_request()
    except TimeoutError:
        logger.info(f'WiredTimer info: timeout was reached')

    return None


def start_mock_int_http_server(execution_seconds: Union[int, None] = None):
    server = HTTPServer((HTTP_LOCALHOST, INT_PORT), RandomIntegersHandler)
    return _start_mock_http_server(execution_seconds, server)


def start_mock_str_http_server(execution_seconds: Union[int, None] = None):
    server = HTTPServer((HTTP_LOCALHOST, STR_PORT), RandomStringHandler)
    return _start_mock_http_server(execution_seconds, server)
