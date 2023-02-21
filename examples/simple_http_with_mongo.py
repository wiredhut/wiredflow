from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings import launch_demo_with_int_http_connector


def launch_simple_http_demo_with_mongo_database():
    """
    An example of configuration of a simple data retrieval pipeline via HTTP.
    All data will be saved into configured remote database

    NB: Demo will be executed in the loop. This means that the example won't
    finish calculating until you stop it yourself
    """
    flow_builder = FlowBuilder()

    # Repeat actions in pipeline every 1 minute - send GET request and store response
    flow_builder.add_pipeline('my_custom_name', timedelta_seconds=10)\
        .with_http_connector(source='http://localhost:8027',
                             headers={'accept': 'application/json',
                                      'apikey': 'custom_key_1234'})\
        .with_storage('mongo',
                      source='mongodb+srv://clusterdreamlone.ryubwzt.mongodb.net/?retryWrites=true&w=majority',
                      database_name='test', collection_name='info',
                      username='username', password='password')

    # Configure service and launch it
    flow = flow_builder.build()

    # Or simply flow.launch_flow()
    # if there is no need to launch local demo http server
    launch_demo_with_int_http_connector(flow)


if __name__ == '__main__':
    launch_simple_http_demo_with_mongo_database()
