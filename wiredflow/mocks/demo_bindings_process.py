from http.server import HTTPServer
from typing import Union

from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.http_server import RandomIntegersHandler, INT_PORT, \
    HTTP_LOCALHOST, _start_mock_http_server, STR_PORT, RandomStringHandler


def stage_mock_int_http_server(**kwargs):
    server = HTTPServer((HTTP_LOCALHOST, INT_PORT), RandomIntegersHandler)
    execution_seconds = kwargs.get('execution_seconds')
    return _start_mock_http_server(execution_seconds, server)


def stage_mock_str_http_server(**kwargs):
    server = HTTPServer((HTTP_LOCALHOST, STR_PORT), RandomStringHandler)
    execution_seconds = kwargs.get('execution_seconds')
    return _start_mock_http_server(execution_seconds, server)


def launch_demo_with_int_http_connector_processes(flow_builder: FlowBuilder,
                                                  execution_seconds: Union[int, None] = None):
    """ Launch flow processing and local HTTP server in separate processes """
    # Add additional pipeline in the service
    flow_builder.add_pipeline('http_int_demo', timedelta_seconds=60,
                              delay_seconds=0) \
        .with_core_logic(stage_mock_int_http_server,
                         execution_seconds=execution_seconds)

    # Launch the service with two pipelines (each pipeline in different process)
    service = flow_builder.build()
    service.launch_flow(execution_seconds)


def launch_demo_with_several_http_connectors_processes(flow_builder: FlowBuilder,
                                                       execution_seconds: Union[int, None] = None):
    flow_builder.add_pipeline('http_int_demo', timedelta_seconds=60, delay_seconds=0) \
        .with_core_logic(stage_mock_int_http_server,
                         execution_seconds=execution_seconds)

    flow_builder.add_pipeline('http_str_demo', timedelta_seconds=60, delay_seconds=0) \
        .with_core_logic(stage_mock_str_http_server,
                         execution_seconds=execution_seconds)

    service = flow_builder.build()
    service.launch_flow(execution_seconds)
