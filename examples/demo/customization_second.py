from copy import deepcopy

from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings_threads import launch_demo_for_complex_case


def order_and_calculate(**kwargs):
    # Through storages we can obtain data from other pipelines
    db_connectors = kwargs['db_connectors']

    # Load all numbers from databases
    numbers_via_http = list(db_connectors['http_numbers'].load())
    numbers_via_mqtt = list(db_connectors['mqtt_numbers'].load())

    http_numbers = list(map(lambda x: int(x['Generated random number']), numbers_via_http))
    mqtt_numbers = list(map(lambda x: int(x['Generated number']), numbers_via_mqtt))

    # Create united list and sort it
    full_list = deepcopy(http_numbers)
    full_list.extend(mqtt_numbers)
    full_list.sort()

    # Calculate the value
    response_value = sum(http_numbers) - sum(mqtt_numbers)

    return {'sorted list': str(full_list), 'calculated value': response_value}


def order_and_calculate_by_batches(**kwargs):
    # Set processing limit
    max_number_of_items = 5
    db_connectors = kwargs['db_connectors']

    http_numbers = list(map(lambda x: int(x['Generated random number']), list(db_connectors['http_numbers'].load())))
    mqtt_numbers = list(map(lambda x: int(x['Generated number']), list(db_connectors['mqtt_numbers'].load())))

    if len(http_numbers) > max_number_of_items:
        # Process by batches
        start_batch_id = 0
        for i in range(max_number_of_items, len(http_numbers), max_number_of_items):
            print(f'Processing items from {start_batch_id} to {i}')
            batch_http_numbers = deepcopy(http_numbers[start_batch_id: i])
            batch_http_numbers.extend(mqtt_numbers)
            batch_http_numbers.sort()

            # Update the start id of item
            start_batch_id = i
            yield {'sorted list': str(batch_http_numbers),
                   'calculated value': sum(batch_http_numbers) - sum(mqtt_numbers)}
    else:
        full_list = deepcopy(http_numbers)
        full_list.extend(mqtt_numbers)
        full_list.sort()

        yield {'sorted list': str(full_list), 'calculated value': sum(http_numbers) - sum(mqtt_numbers)}


def launch_custom_flow():
    """
    Example of how to configure and launch flow with several pipelines, MongoDB storages and
    custom core
    """
    mongo_url = 'mongodb+srv://clusterdreamlone.ryubwzt.mongodb.net/?retryWrites=true&w=majority'
    mongo_user = 'dreamlone'
    mongo_password = 'mydreamlonepassword'

    flow_builder = FlowBuilder()

    # Pipeline for HTTP numbers processing
    flow_builder.add_pipeline('http_numbers', timedelta_seconds=10)\
        .with_http_connector(source='http://localhost:8027',
                             headers={'accept': 'application/json',
                                      'apikey': 'custom_key_1234'}) \
        .with_storage('mongo', source=mongo_url, database_name='wiredflow', collection_name='http_numbers',
                      username=mongo_user, password=mongo_password)

    # Pipeline for MQTT data processing
    flow_builder.add_pipeline('mqtt_numbers') \
        .with_mqtt_connector(source='localhost', port=1883,
                             topic='/demo/integers',
                             username='wiredflow', password='wiredflow') \
        .with_storage('mongo', source=mongo_url, database_name='wiredflow', collection_name='mqtt_numbers',
                      username=mongo_user, password=mongo_password)

    # Add pipeline with custom function and send stages
    flow_builder.add_pipeline('custom_logic', timedelta_seconds=15)\
        .with_core_logic(order_and_calculate)\
        .send(destination='localhost', port=1883, topic='demo/sorted', label_to_send='sorted list') \
        .send(destination='localhost', port=1883, topic='demo/subtraction', label_to_send='calculated value')

    flow = flow_builder.build()

    # Or simply flow.launch_flow()
    # if there is no need to launch local demo http server
    launch_demo_for_complex_case(flow, execution_seconds=30)


if __name__ == '__main__':
    launch_custom_flow()
