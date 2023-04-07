import json
from pathlib import Path

import pytest

from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings_threads import launch_demo_with_int_http_connector, launch_demo_with_int_mqtt_connector
from wiredflow.paths import get_test_folder_path, remove_folder_with_files


def test_http_local():
    """
    Test correctness of simple linear flow execution.
    Data source - HTTP endpoint
    """
    path_to_save_files = Path(get_test_folder_path(), 'test_http_local')
    remove_folder_with_files(path_to_save_files)
    flow_builder = FlowBuilder()

    flow_builder.add_pipeline('test_http_local', timedelta_seconds=5) \
        .with_http_connector(source='http://localhost:8027') \
        .with_storage('json', preprocessing='add_datetime', folder_to_save=path_to_save_files)

    # Configure service and launch it
    flow = flow_builder.build()
    launch_demo_with_int_http_connector(flow, execution_seconds=10)

    created_file = Path(path_to_save_files, 'json_in_test_http_local.json')
    assert created_file.is_file()
    with open(created_file, 'r') as fp:
        loaded_file = json.load(fp)

    assert isinstance(loaded_file, list)
    assert isinstance(loaded_file[0]['Generated random number'], int)
    remove_folder_with_files(path_to_save_files)


@pytest.mark.skip()
def test_mqtt_local():
    """
    Test correctness of simple linear flow execution.
    Data source - MQTT broker
    """
    path_to_save_files = Path(get_test_folder_path(), 'test_mqtt_local')
    remove_folder_with_files(path_to_save_files)
    flow_builder = FlowBuilder()

    flow_builder.add_pipeline('mqtt_subscriber') \
        .with_mqtt_connector(source='localhost', port=1883, topic='/demo/integers') \
        .with_storage('json', preprocessing='add_datetime', folder_to_save=path_to_save_files)

    # Configure service and launch it
    flow = flow_builder.build()
    launch_demo_with_int_mqtt_connector(flow, execution_seconds=10)

    created_file = Path(path_to_save_files, 'json_in_mqtt_subscriber.json')
    assert created_file.is_file()
    with open(created_file, 'r') as fp:
        loaded_file = json.load(fp)

    assert isinstance(loaded_file, list)
    assert int(loaded_file[0]['Generated number']) == 0
    remove_folder_with_files(path_to_save_files)
