import pymongo
from pymongo import MongoClient, WriteConcern

from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings import launch_demo_with_int_http_connector


def custom_save(data_to_save, **params):
    """
    Custom realization for MongoDB storage.
    In this example we will identify unique indexes for database to
    avoid duplicates in the storage.

    NB: current realization does not produce threads synchronization
    Requests synchronization is Database responsibility
    """
    # Connect to the database
    client = MongoClient(params['source'],
                         username=params['username'], password=params['password'])
    db = client[params['database_name']]
    collection = db[params['collection_name']]

    # Does not allow to produce duplicates
    # So in MongoDB there will be no items with equal random numbers
    # According to https://stackoverflow.com/a/35020346 we can freely launch command each
    # time during execution
    collection.create_index([('Generated random number', pymongo.ASCENDING)],
                            unique=True)

    # Insert our values
    # collection.insert_one(data_to_save[0])
    collection.with_options(write_concern=WriteConcern(w=0))\
        .insert_one(data_to_save[0])


def launch_simple_http_demo_with_custom_mongo():
    """
    An example of configuration of a simple data retrieval pipeline via HTTP.
    All data will be saved into configured remote database.
    We apply custom realization which will not allow

    NB: Demo will be executed in the loop. This means that the example won't
    finish calculating until you stop it yourself. Alternatively - you can assign
    'execution_seconds' parameter to set the timeout
    """
    flow_builder = FlowBuilder()

    # Repeat actions in pipeline every 1 minute - send GET request and store response
    flow_builder.add_pipeline('my_custom_name', timedelta_seconds=10)\
        .with_http_connector(source='http://localhost:8027',
                             headers={'accept': 'application/json',
                                      'apikey': 'custom_key_1234'})\
        .with_storage(custom_save,
                      source='mongodb+srv://clusteryoucluster.ryubwzt.mongodb.net/?retryWrites=true&w=majority',
                      database_name='test', collection_name='info',
                      username='username', password='password')

    # Configure service and launch it
    flow = flow_builder.build()

    # Or simply flow.launch_flow()
    # if there is no need to launch local demo http server
    launch_demo_with_int_http_connector(flow)


if __name__ == '__main__':
    launch_simple_http_demo_with_custom_mongo()
