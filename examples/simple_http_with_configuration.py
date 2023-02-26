from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings import remove_temporary_folder_for_demo, \
    launch_demo_with_int_http_connector


def configure_post_request_parameters(**params):
    """ Configure post request parameters based on local database fullness """
    if params['my_custom_name'].load() is None:
        return {'data': 'select * from demo_table limit 5'}
    else:
        return {'data': 'select * from demo_table limit 1'}


def launch_simple_http_demo_with_configuration():
    """
    An example how to create linear pipeline with configuration stage.
    Task: if the database is empty, then query for 5 new rows with numbers.
    Then query only 1 line at a time

    NB: Demo will be executed in the loop. This means that the example won't
    finish calculating until you stop it yourself. Alternatively - you can assign
    'execution_seconds' parameter to set the timeout
    """
    flow_builder = FlowBuilder()

    flow_builder.add_pipeline('my_custom_name', timedelta_seconds=10)\
        .with_configuration(configure_post_request_parameters)\
        .with_http_connector(configuration='post', source='http://localhost:8027')\
        .with_storage('json', preprocessing='add_datetime')

    # Configure service and launch it
    flow = flow_builder.build()

    # Or simply flow.launch_flow()
    # if there is no need to launch local demo http server
    launch_demo_with_int_http_connector(flow, execution_seconds=30)


if __name__ == '__main__':
    remove_temporary_folder_for_demo()
    launch_simple_http_demo_with_configuration()
