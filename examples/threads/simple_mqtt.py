from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings_threads import remove_temporary_folder_for_demo, \
    launch_demo_with_int_mqtt_connector


def launch_advanced_mqtt_demo():
    """
    An example of how to launch a flow to collect some data from MQTT queue
    and save it into a file

    NB: Demo will be executed in the loop. This means that the example won't
    finish calculating until you stop it yourself. Alternatively - you can assign
    'execution_seconds' parameter to set the timeout
    """
    flow_builder = FlowBuilder()

    # Subscribe to desired MQTT broker and start get messages
    flow_builder.add_pipeline('mqtt_subscriber')\
        .with_mqtt_connector(source='localhost', port=1883, topic='/demo/integers',
                             username='wiredflow', password='wiredflow')\
        .with_storage('json', preprocessing='add_datetime')

    # Configure service and launch it
    flow = flow_builder.build()

    # Or simply flow.launch_flow()
    # if there is no need to launch local demo http server
    launch_demo_with_int_mqtt_connector(flow, execution_seconds=10)


if __name__ == '__main__':
    remove_temporary_folder_for_demo()
    launch_advanced_mqtt_demo()

