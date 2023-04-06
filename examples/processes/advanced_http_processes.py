from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings_process import \
    launch_demo_with_several_http_connectors_processes
from wiredflow.mocks.demo_bindings_threads import remove_temporary_folder_for_demo


def toy_example_logic(**parameters_to_use):
    """ Example of core logic implementation """
    # Through storages we can obtain data from other pipelines
    db_connectors = parameters_to_use['db_connectors']

    # Load all currently available integers and current letter
    available_integers = db_connectors['integers_processing'].load()
    current_letter = db_connectors['letters_processing'].load()[0]

    if available_integers is None or current_letter is None:
        # Skip current iteration - there are no data to process
        return None

    # Transform dictionary into values
    integers = list(map(lambda x: int(x['Generated random number']), available_integers))

    message = {}
    if current_letter['Generated random letter'].isupper():
        # We need to calculate sum
        response = sum(integers)
        message.update({'uppercase': f'Calculated value is {response}'})
    else:
        # Mean value because current letter is lowercase
        response = sum(integers) / len(integers)
        message.update({'lowercase': f'Calculated value is {response}'})

    print(f'For letter {current_letter["Generated random letter"]} and {integers} response is: {response:.1f}')
    return message


def launch_advanced_http_demo_using_processes():
    """
    An example of how to run a service with processes usage (parallel mode)
    """
    flow_builder = FlowBuilder(use_threads=False)

    # Launch pipeline every 10 seconds
    flow_builder.add_pipeline('integers_processing', timedelta_seconds=10) \
        .with_http_connector(source='http://localhost:8027') \
        .with_storage('json', preprocessing='add_datetime')

    # Launch pipeline every 1 minute and overwrite all previous recordings
    flow_builder.add_pipeline('letters_processing', timedelta_seconds=60) \
        .with_http_connector(source='http://localhost:8026') \
        .with_storage('json', preprocessing='add_datetime', mapping='overwrite')

    # Core logic of our case
    # Configure notification sender: send message based on calculation approach
    flow_builder.add_pipeline('core_matching', timedelta_seconds=20, delay_seconds=10) \
        .with_core_logic(toy_example_logic)\
        .send(destination='localhost', port=1883, topic='demo/uppercase', label_to_send='uppercase')\
        .send(destination='localhost', port=1883, topic='demo/lowercase', label_to_send='lowercase')

    # Configure service and launch it
    launch_demo_with_several_http_connectors_processes(flow_builder,
                                                       execution_seconds=60)


if __name__ == '__main__':
    remove_temporary_folder_for_demo()
    launch_advanced_http_demo_using_processes()
