from wiredflow.main.build import FlowBuilder


def custom_core_logic():
    pass


def launch_complex_demo():
    """
    An example of how to run a service that process information from various
    sources (HTTP and MQTT), complex multi-step data processing and sender
    notifications
    """
    flow_builder = FlowBuilder()

    # Define first data sources
    flow_builder.add_pipeline('http_source_1', timedelta_seconds=10). \
        with_http_connector(source='localhost:8024',
                            headers={'accept': 'application/json',
                                     'apikey': 'my_custom_key'}).with_storage('json')

    # Second HTTP source
    flow_builder.add_pipeline('http_source_2', timedelta_seconds=20). \
        with_http_connector(source='localhost:8025',
                            headers={'accept': 'application/json',
                                     'apikey': 'my_custom_key'}).with_storage('json')

    flow_builder.add_pipeline('mqtt_source'). \
        with_mqtt_connector(source='localhost', port=150, topic='/test/topic',
                            username='wiredflow', password='wiredflow').with_storage('json')

    # Create core logic which will be launched 3 times
    flow_builder.add_pipeline('core_logic', timedelta_seconds=15)\
        .with_core_logic(custom_core_logic)\
        .send('demo/predict', data_aggregate='predict') \
        .send('demo/bad_request', data_aggregate='request') \

    # Configure service and launch it
    flow = flow_builder.build()

    raise NotImplementedError()
