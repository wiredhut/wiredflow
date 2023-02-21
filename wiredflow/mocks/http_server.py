import cgi
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


def start_mock_int_http_server():
    server = HTTPServer((HTTP_LOCALHOST, INT_PORT), RandomIntegersHandler)
    logger.info(f'Start mock HTTP server in separate process: {HTTP_LOCALHOST},'
                f' port {INT_PORT}')
    server.serve_forever()


def start_mock_str_http_server():
    server = HTTPServer((HTTP_LOCALHOST, STR_PORT), RandomStringHandler)
    logger.info(f'Start mock HTTP server in separate process: {HTTP_LOCALHOST},'
                f' port {STR_PORT}')
    server.serve_forever()
