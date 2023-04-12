from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings_threads import remove_temporary_folder_for_demo, \
    launch_demo_with_int_mqtt_connector


def launch_mqtt_processing_flow():
    """
    Example of usage MQTT connector in the pipeline
    """
    flow_builder = FlowBuilder()

    # Subscribe to desired MQTT broker and start get messages
    flow_builder.add_pipeline('my_custom_name')\
        .with_mqtt_connector(source='localhost', port=1883, topic='/demo/integers',
                             username='wiredflow', password='wiredflow')\
        .with_storage('json')

    # Configure service and launch it
    flow = flow_builder.build()

    # Or simply flow.launch_flow()
    # if there is no need to launch local demo mqtt broker
    launch_demo_with_int_mqtt_connector(flow, execution_seconds=10)


if __name__ == '__main__':
    remove_temporary_folder_for_demo()
    launch_mqtt_processing_flow()
