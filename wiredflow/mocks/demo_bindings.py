from functools import partial
from multiprocessing import Pool

from wiredflow.main.flow import FlowProcessor
from wiredflow.mocks.http_server import start_mock_int_http_server, \
    start_mock_str_http_server
from wiredflow.mocks.mqtt_broker import configure_int_mqtt_broker
from wiredflow.paths import get_tmp_folder_path


def remove_temporary_folder_for_demo():
    """ Remove folder with saved files """
    import shutil

    tmp_path = get_tmp_folder_path()
    if tmp_path.is_dir() and len(list(tmp_path.iterdir())) > 0:
        shutil.rmtree(tmp_path)


def _parallel_launching(mode: str, flow_processor: FlowProcessor):
    """
    Function for launching flow processing service and additional demo / mock
    instruments in separate processes
    """

    if mode == 'default':
        flow_processor.launch_flow()
    elif mode == 'http_int_demo':
        return start_mock_int_http_server()
    elif mode == 'http_str_demo':
        return start_mock_str_http_server()
    elif mode == 'mqtt_int_demo':
        return configure_int_mqtt_broker()
    else:
        raise ValueError(f'Does not support mode {mode} for demo purposes')


def launch_demo_with_int_http_connector(flow_processor: FlowProcessor):
    """ Launch flow processing and local HTTP server in separate processes """
    with Pool(processes=2) as pool:
        return pool.map(partial(_parallel_launching, flow_processor=flow_processor),
                        ['http_int_demo', 'default'])


def launch_demo_with_str_http_connector(flow_processor: FlowProcessor):
    """ Launch flow processing and local HTTP server in separate processes """
    with Pool(processes=2) as pool:
        return pool.map(partial(_parallel_launching, flow_processor=flow_processor),
                        ['http_str_demo', 'default'])


def launch_demo_with_several_http_connectors(flow_processor: FlowProcessor):
    """ Launch flow processing and local HTTP server in separate processes """
    with Pool(processes=3) as pool:
        return pool.map(partial(_parallel_launching, flow_processor=flow_processor),
                        ['http_str_demo', 'http_int_demo', 'default'])


def launch_demo_with_int_mqtt_connector(flow_processor: FlowProcessor):
    """ Launch flow processing and local MQTT broker in separate processes """
    with Pool(processes=2) as pool:
        return pool.map(partial(_parallel_launching, flow_processor=flow_processor),
                        ['mqtt_int_demo', 'default'])
