import json
from pathlib import Path

from wiredflow.main.build import FlowBuilder
from wiredflow.paths import get_test_folder_path, remove_folder_with_files


def custom_http_connector(**params):
    return {'Mock response': f'Get data from {params["source"]}'}


def test_custom_http_connector():
    """ Check that custom http connector launched correctly """
    path_to_save_files = Path(get_test_folder_path(), 'test_http_custom')
    remove_folder_with_files(path_to_save_files)

    source = 'http://localhost:8027'

    flow_builder = FlowBuilder()

    flow_builder.add_pipeline('test_custom_http', timedelta_seconds=5) \
        .with_http_connector(configuration=custom_http_connector,
                             source=source) \
        .with_storage('json', preprocessing='add_datetime',
                      folder_to_save=path_to_save_files)

    # Configure service and launch it
    flow = flow_builder.build()

    # Or simply flow.launch_flow()
    # if there is no need to launch local demo http server
    flow.launch_flow(execution_seconds=10)

    created_file = Path(path_to_save_files, 'json_in_test_custom_http.json')
    assert created_file.is_file()
    with open(created_file, 'r') as fp:
        loaded_file = json.load(fp)

    # Check that
    assert loaded_file[0]['Mock response'] == f'Get data from {source}'
    remove_folder_with_files(path_to_save_files)
