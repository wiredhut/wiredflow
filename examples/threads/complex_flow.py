from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings_threads import remove_temporary_folder_for_demo, \
    launch_demo_for_complex_case


def custom_core_logic(**parameters_to_use):
    # Through storages we can obtain data from other pipelines
    db_connectors = parameters_to_use['db_connectors']

    # Load all currently available integers and current letter
    http_integers = db_connectors['http_source_int'].load()
    http_letter = db_connectors['http_source_str'].load()[0]
    mqtt_integers = db_connectors['mqtt_source_int'].load()

    # Get numbers
    http_integers = list(map(lambda x: int(x['Generated random number']), http_integers))
    mqtt_integers = list(map(lambda x: int(x['Generated number']), mqtt_integers))

    message = {}
    if http_letter['Generated random letter'].isupper():
        calculation_mode = 'Upper case'
        response = sum(http_integers) + sum(mqtt_integers)
        message.update({'uppercase': f'Calculated value is {response}'})
    else:
        calculation_mode = 'Lower case'
        response = sum(http_integers) - sum(mqtt_integers)
        message.update({'uppercase': f'Calculated value is {response}'})

    message.update({'calculation_mode': calculation_mode})
    print(f'For letter "{http_letter["Generated random letter"]}" response is: {response:.1f}')
    return message


def custom_sender(data_to_send, **params):
    """ Example of custom sender implementation """
    print(f'Launch my custom data sending for data: {data_to_send}')


def launch_complex_demo():
    """
    An example of how to run a service that process information from various
    sources (HTTP and MQTT), complex multi-step data processing and sender
    notifications both using MQTT protocol and HTTP PUT method

    The task: from two endpoints it is required to retrieve data about numbers
    and letters every 10 seconds using HTTP requests. It is also necessary to
    retrieve information from MQTT queue.

    If a capital letter is received via HTTP, then the sum of all the numbers
    received via MQTT and received via HTTP must be calculated. If the letter
    is lowercase, the sum of values obtained via MQTT is subtracted from the
    sum of values obtained via HTTP. The calculated values must be sent to
    three places: two MQTT queues and a PUT request to local server

    NB: Demo will be executed in the loop. This means that the example won't
    finish calculating until you stop it yourself. Alternatively - you can assign
    'execution_seconds' parameter to set the timeout
    """
    flow_builder = FlowBuilder()

    # Define first data sources with random integers
    flow_builder.add_pipeline('http_source_int', timedelta_seconds=10) \
        .with_http_connector(source='http://localhost:8027').with_storage('json')

    # Second HTTP source with random letters
    flow_builder.add_pipeline('http_source_str', timedelta_seconds=10) \
        .with_http_connector(source='http://localhost:8026')\
        .with_storage('json', mapping='overwrite')

    # MQTT source with integers
    flow_builder.add_pipeline('mqtt_source_int') \
        .with_mqtt_connector(source='localhost', port=1883, topic='/demo/integers',
                             username='wiredflow', password='wiredflow') \
        .with_storage('json')

    # Create core logic and send messages to desired endpoints or MQTT subscribers
    flow_builder.add_pipeline('core_logic', timedelta_seconds=15)\
        .with_core_logic(custom_core_logic) \
        .send(destination='localhost', port=1883, topic='demo/uppercase', label_to_send='uppercase') \
        .send(destination='localhost', port=1883, topic='demo/lowercase', label_to_send='lowercase')\
        .send('http_put', destination='http://localhost:8027', label_to_send='calculation_mode')\
        .send(custom_sender)

    # Configure service and launch it
    flow = flow_builder.build()

    # Or simply flow.launch_flow()
    # if there is no need to launch local demo http servers
    launch_demo_for_complex_case(flow, execution_seconds=30)


if __name__ == '__main__':
    remove_temporary_folder_for_demo()
    launch_complex_demo()
