from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings_threads import \
    remove_temporary_folder_for_demo, launch_demo_for_complex_case


def print_into_terminal(**kwargs):
    # Through storages we can obtain data from other pipelines
    db_connectors = kwargs['db_connectors']

    # Load all currently available integers
    http_integers = db_connectors['http_numbers'].load()
    mqtt_integers = db_connectors['mqtt_numbers'].load()

    http_integers = list(map(lambda x: int(x['Generated random number']), http_integers))
    mqtt_integers = list(map(lambda x: int(x['Generated number']), mqtt_integers))

    print(f'\nCustom logic checkout:')
    print(f'HTTP integers: {http_integers}')
    print(f'MQTT integers: {mqtt_integers}')


def launch_multiple_pipelines_flow():
    """
    Example of how to configure and launch flow with several pipelines
    """
    flow_builder = FlowBuilder()

    # Pipeline for HTTP numbers processing
    flow_builder.add_pipeline('http_numbers', timedelta_seconds=10)\
        .with_http_connector(source='http://localhost:8027',
                             headers={'accept': 'application/json',
                                      'apikey': 'custom_key_1234'})\
        .with_storage('json')

    # Pipeline for MQTT data processing
    flow_builder.add_pipeline('mqtt_numbers') \
        .with_mqtt_connector(source='localhost', port=1883,
                             topic='/demo/integers',
                             username='wiredflow', password='wiredflow') \
        .with_storage('json')

    # Add very simple custom logic as separate pipeline
    flow_builder.add_pipeline('custom_logic', timedelta_seconds=15)\
        .with_core_logic(print_into_terminal)

    flow = flow_builder.build()

    # Or simply flow.launch_flow()
    # if there is no need to launch local demo http server
    launch_demo_for_complex_case(flow, execution_seconds=30)


if __name__ == '__main__':
    remove_temporary_folder_for_demo()
    launch_multiple_pipelines_flow()
