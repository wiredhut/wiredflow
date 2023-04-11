from functools import partial
from multiprocessing import Pool
from typing import Union

from wiredflow.main.flow import FlowProcessor
from wiredflow.mocks.http_server import start_mock_int_http_server, \
    start_mock_str_http_server, start_mock_hello_world_http_server
from wiredflow.mocks.mqtt_broker import configure_int_mqtt_broker, \
    configure_str_mqtt_broker
from wiredflow.paths import get_tmp_folder_path


def remove_temporary_folder_for_demo():
    """ Remove folder with saved files """
    import shutil

    tmp_path = get_tmp_folder_path()
    if tmp_path.is_dir() and len(list(tmp_path.iterdir())) > 0:
        shutil.rmtree(tmp_path)


def _parallel_launching(mode: str, flow_processor: FlowProcessor,
                        execution_seconds: Union[int, None]):
    """
    Function for launching flow processing service and additional demo / mock
    instruments in separate processes

    :param mode: name of mode to launch in process
    :param flow_processor: service to launch
    :param execution_seconds: timeout for process execution in seconds
    """

    if mode == 'default':
        flow_processor.launch_flow(execution_seconds)
    elif mode == 'http_int_demo':
        return start_mock_int_http_server(execution_seconds)
    elif mode == 'http_str_demo':
        return start_mock_str_http_server(execution_seconds)
    elif mode == 'mqtt_int_demo':
        return configure_int_mqtt_broker(execution_seconds)
    elif mode == 'mqtt_str_demo':
        return configure_str_mqtt_broker(execution_seconds)
    elif mode == 'hello_world_demo':
        return start_mock_hello_world_http_server(execution_seconds)
    else:
        raise ValueError(f'Does not support mode {mode} for demo purposes')


def launch_demo_with_int_hello_world_connector(flow_processor: FlowProcessor,
                                               execution_seconds: Union[int, None] = None):
    """ Launch flow processing and local HTTP server in separate processes """
    with Pool(processes=2) as pool:
        return pool.map(partial(_parallel_launching, flow_processor=flow_processor,
                                execution_seconds=execution_seconds),
                        ['hello_world_demo', 'default'])


def launch_demo_with_int_http_connector(flow_processor: FlowProcessor,
                                        execution_seconds: Union[int, None] = None):
    """ Launch flow processing and local HTTP server in separate processes """
    with Pool(processes=2) as pool:
        return pool.map(partial(_parallel_launching, flow_processor=flow_processor,
                                execution_seconds=execution_seconds),
                        ['http_int_demo', 'default'])


def launch_demo_with_str_http_connector(flow_processor: FlowProcessor,
                                        execution_seconds: Union[int, None] = None):
    """ Launch flow processing and local HTTP server in separate processes """
    with Pool(processes=2) as pool:
        return pool.map(partial(_parallel_launching, flow_processor=flow_processor,
                                execution_seconds=execution_seconds),
                        ['http_str_demo', 'default'])


def launch_demo_with_several_http_connectors(flow_processor: FlowProcessor,
                                             execution_seconds: Union[int, None] = None):
    """ Launch flow processing and local HTTP server in separate processes """
    with Pool(processes=3) as pool:
        return pool.map(partial(_parallel_launching, flow_processor=flow_processor,
                                execution_seconds=execution_seconds),
                        ['http_str_demo', 'http_int_demo', 'default'])


def launch_demo_with_int_mqtt_connector(flow_processor: FlowProcessor,
                                        execution_seconds: Union[int, None] = None):
    """ Launch flow processing and local MQTT broker in separate processes """
    with Pool(processes=2) as pool:
        return pool.map(partial(_parallel_launching, flow_processor=flow_processor,
                                execution_seconds=execution_seconds),
                        ['mqtt_int_demo', 'default'])


def launch_demo_with_str_mqtt_connector(flow_processor: FlowProcessor,
                                        execution_seconds: Union[int, None] = None):
    """ Launch flow processing and local MQTT broker in separate processes """
    with Pool(processes=2) as pool:
        return pool.map(partial(_parallel_launching, flow_processor=flow_processor,
                                execution_seconds=execution_seconds),
                        ['mqtt_str_demo', 'default'])


def launch_demo_with_several_mqtt_connectors(flow_processor: FlowProcessor,
                                             execution_seconds: Union[int, None] = None):
    """ Launch flow processing and local MQTT broker in separate processes """
    with Pool(processes=3) as pool:
        return pool.map(partial(_parallel_launching, flow_processor=flow_processor,
                                execution_seconds=execution_seconds),
                        ['mqtt_str_demo', 'mqtt_int_demo', 'default'])


def launch_demo_for_complex_case(flow_processor: FlowProcessor,
                                 execution_seconds: Union[int, None] = None):
    with Pool(processes=4) as pool:
        return pool.map(partial(_parallel_launching, flow_processor=flow_processor,
                                execution_seconds=execution_seconds),
                        ['http_str_demo', 'http_int_demo', 'mqtt_int_demo', 'default'])
