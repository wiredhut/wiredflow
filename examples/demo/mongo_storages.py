from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings_threads import launch_demo_with_int_http_connector


def launch_flow_with_mongo_storage():
    """
    Example of usage MongoDB as storage in the pipeline. Single pipeline service is used for demonstration
    """
    flow_builder = FlowBuilder()
    flow_builder.add_pipeline('http_integers', timedelta_seconds=2)\
        .with_http_connector(source='http://localhost:8027',
                             headers={'accept': 'application/json',
                                      'apikey': 'custom_key_1234'})\
        .with_storage('mongo', source='mongodb+srv://clusterdreamlone.ryubwzt.mongodb.net/?retryWrites=true&w=majority',
                      database_name='wiredflow', collection_name='demo',
                      username='dreamlone', password='mydreamlonepassword')
    flow = flow_builder.build()
    launch_demo_with_int_http_connector(flow, execution_seconds=10)


if __name__ == '__main__':
    launch_flow_with_mongo_storage()
