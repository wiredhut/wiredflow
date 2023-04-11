from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings_threads import remove_temporary_folder_for_demo,\
    launch_demo_with_int_hello_world_connector


def wiredflow_hello_world():
    """
    Quick example, which show how to configure and launch very simple ETL pipeline
    """
    # Initialize builder to configure ETL services
    flow_builder = FlowBuilder()

    # Repeat actions in pipeline every 1 minute - send GET request and store response
    flow_builder.add_pipeline('hello_world', timedelta_seconds=60)\
        .with_http_connector(source='http://localhost:8025',
                             headers={'accept': 'application/json',
                                      'apikey': 'custom_key_1234'})\
        .with_storage('json', preprocessing='add_datetime')

    # Configure service and launch it
    flow = flow_builder.build()

    # Or simply flow.launch_flow()
    # if there is no need to launch local demo http server
    launch_demo_with_int_hello_world_connector(flow, execution_seconds=20)


if __name__ == '__main__':
    remove_temporary_folder_for_demo()
    wiredflow_hello_world()
