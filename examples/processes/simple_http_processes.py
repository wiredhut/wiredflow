from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings_process import \
    launch_demo_with_int_http_connector_processes
from wiredflow.mocks.demo_bindings_threads import remove_temporary_folder_for_demo


def launch_simple_http_demo_using_processes():
    """
    An example of configuration of a simple data retrieval pipeline via HTTP.
    Example demonstrate how to launch pipelines in different processes (not threads)

    NB: Demo will be executed in the loop. This means that the example won't
    finish calculating until you stop it yourself. Alternatively - you can assign
    'execution_seconds' parameter to set the timeout
    """
    flow_builder = FlowBuilder(use_threads=False)

    # Repeat actions in pipeline every 1 minute - send GET request and store response
    flow_builder.add_pipeline('my_custom_name', timedelta_seconds=60)\
        .with_http_connector(source='http://localhost:8027',
                             headers={'accept': 'application/json',
                                      'apikey': 'custom_key_1234'})\
        .with_storage('json', preprocessing='add_datetime')

    # Or simply flow.launch_flow()
    # if there is no need to launch local demo http server
    launch_demo_with_int_http_connector_processes(flow_builder, execution_seconds=20)


if __name__ == '__main__':
    remove_temporary_folder_for_demo()
    launch_simple_http_demo_using_processes()
