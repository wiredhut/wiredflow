from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings_process import launch_demo_with_several_mqtt_connectors_processes
from wiredflow.mocks.demo_bindings_threads import remove_temporary_folder_for_demo


def custom_logic(**parameters_to_use):
    """ Simple realization of core logic """
    db_connectors = parameters_to_use['db_connectors']
    obtained_integers = db_connectors['int_subscriber'].load()
    obtained_letters = db_connectors['str_subscriber'].load()

    integers = list(map(lambda x: int(x['Generated number']), obtained_integers))
    letters = list(map(lambda x: x['Generated letter'], obtained_letters))

    match_to_send = f'{integers[-1]}-{letters[-1]}'
    print(f'Match to send {match_to_send}')
    return {'match': match_to_send}


def launch_advanced_mqtt_demo_using_processes():
    """
    An example of how to launch a flow with processes usage (parallel mode)
    """
    flow_builder = FlowBuilder(use_threads=False)

    # Get integers values via MQTT
    flow_builder.add_pipeline('int_subscriber')\
        .with_mqtt_connector(source='localhost', port=1883, topic='/demo/integers',
                             username='wiredflow', password='wiredflow')\
        .with_storage('json', preprocessing='add_datetime')

    # Get letters via MQTT
    flow_builder.add_pipeline('str_subscriber') \
        .with_mqtt_connector(source='localhost', port=1883, topic='/demo/letters',
                             username='wiredflow', password='wiredflow') \
        .with_storage('json', preprocessing='add_datetime')

    flow_builder.add_pipeline('custom_core', timedelta_seconds=10) \
        .with_core_logic(custom_logic) \
        .send(destination='localhost', port=1883, topic='demo/matched',
              label_to_send='match')

    launch_demo_with_several_mqtt_connectors_processes(flow_builder,
                                                       execution_seconds=20)


if __name__ == '__main__':
    remove_temporary_folder_for_demo()
    launch_advanced_mqtt_demo_using_processes()
