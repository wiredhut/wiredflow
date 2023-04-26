from wiredflow.main.build import FlowBuilder


def custom_function_first(**kwargs):
    print('Hello')


def custom_function_second(**kwargs):
    print('World!')


def wiredflow_simple_customization():
    """
    Quick example, which show how to configure and launch very simple ETL pipeline
    """
    flow_builder = FlowBuilder()
    flow_builder.add_pipeline('my_logic')\
        .with_core_logic(custom_function_first)\
        .with_http_connector(custom_function_second)

    # Configure service and launch it
    flow = flow_builder.build()
    flow.launch_flow(execution_seconds=30)


if __name__ == '__main__':
    wiredflow_simple_customization()
