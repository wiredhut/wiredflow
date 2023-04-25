from pathlib import Path

from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings_threads import launch_demo_with_int_http_connector


def launch_flow_with_local_storage_config(storage_configuration: str, **params):
    """
    Example of usage local files as storages

    :param storage_configuration: name of configuration to be applied
    """
    flow_builder = FlowBuilder()
    flow_builder.add_pipeline('http_integers', timedelta_seconds=2)\
        .with_http_connector(source='http://localhost:8027',
                             headers={'accept': 'application/json',
                                      'apikey': 'custom_key_1234'})\
        .with_storage(storage_configuration, **params)
    flow = flow_builder.build()
    launch_demo_with_int_http_connector(flow, execution_seconds=10)


if __name__ == '__main__':
    # Save data into json file into new folder
    launch_flow_with_local_storage_config('json', folder_to_save=Path('./json_storage'))

    # Apply csv engine
    launch_flow_with_local_storage_config('csv', folder_to_save=Path('./csv_storage'))

    # Customization with preprocessing
    launch_flow_with_local_storage_config('json', preprocessing='add_datetime', folder_to_save=Path('./preprocessing'))

    # Apply overwrite mapping strategy
    launch_flow_with_local_storage_config('json', mapping='overwrite', folder_to_save=Path('./overwrite'))