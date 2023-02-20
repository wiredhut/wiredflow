from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings import remove_temporary_folder_for_demo, \
    launch_demo_with_several_http_connectors


def launch_advanced_http_demo():
    """
    An example of how to run a service that receives information from
    several http servers and merges the data in a specified way.
    """
    flow_builder = FlowBuilder()

    # Launch pipeline every 2 minutes
    flow_builder.add_pipeline('integers_processing', timedelta_minutes=2) \
        .with_http_connector(source='http://localhost:8027') \
        .with_storage('json', preprocessing=['add_datetime'])

    # Launch pipeline every 1 minute and overwrite all previous recordings
    flow_builder.add_pipeline('letters_processing', timedelta_minutes=1) \
        .with_http_connector(source='http://localhost:8026') \
        .with_storage('json', preprocessing=['add_datetime', 'overwrite'])

    # Configure service and launch it
    flow = flow_builder.build()

    # Or simply flow.launch_flow()
    # if there is no need to launch local demo http servers
    launch_demo_with_several_http_connectors(flow)


if __name__ == '__main__':
    remove_temporary_folder_for_demo()
    launch_advanced_http_demo()
