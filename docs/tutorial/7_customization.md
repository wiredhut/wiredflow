# Customization

When developing services, we are inevitably faced with the need to implement custom business logic.
Wiredflow allows flexible implementation of custom logic at various stages of development using simple 
primitives - Python functions. 

The integration will not require the implementation of classes with specific methods, inheritance,
etc. Everything is pretty transparent - a custom function will have one entry 
point and one exit point. 

In this document you will find detailed instructions describing how to implement 
and integrate "self-made" functions into wiredflow-based service.
And we also will continue improving services which was configured during the previous stages of the tutorial. 

## Stage customization capability

Wiredflow consists of several key blocks (stages). Some stages do not involve default implementations and 
require custom implementations in any case:

- **Configuration** - Configure parameters for next stage in the pipeline;
- **Core logic** - General abstraction to implement custom logic.

The following stages have default implementations, but they can easily be replaced with custom ones

- **HTTP connector** - Retrieving data using `HTTP` requests - active requester;
- **MQTT connector** - Retrieving data using `MQTT` protocol - passive subscriber;
- **Storage** - Client to database;
- **Send** - Send messages to external services.

**<span style="color:orange">NB:</span>** It is up to you to decide in which block to implement the custom functions. 
Depending on the task description above, feel free to choose the right architecture 
for application. However, it's always possible, for example, to implement 
completely custom pipelines with only core logic blocks.

To insert a custom function into a declared stage, simply pass its 
implementation to the parameter `configuration` (first argument at each method):

```Python
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
```

## Usage example

We will continue to modify [the service](4_service_with_pipelines.md), which has already become quite complex. Let's take a look at 
the updated technical requirements:

- There is a need to 1) obtain random numbers via HTTP get request and 2) get ordered numbers via MQTT;
- Save data into MongoDB into collections `http_demo` and `mqtt_demo` using MongoDB Atlas service;
- Every 15 seconds load all available data from MongoDB collections, merge lists with values (sorted list), sort united listed and
  subtract from the sum of the numbers received via MQTT the sum of the numbers received via HTTP (calculated value);
- Send messages via MQTT protocol to topic `demo/sorted` with sorted list and to `demo/subtraction` with calculated value. Configure 
  MQTT broker locally on port 1883. 

As can be seen from the explanation above, we will need to integrate a custom business logic that will allow 
sorting lists and calculating according to desired equation.

## Custom logic

To implement custom business logic, there is a need to prepare a function - Python callable. 
Functions in Python can use `return` or `yield` operators. 
Depending on how exactly the data needs to be processed, we can choose the appropriate option. 

### Function (`return` something)

Suppose the function is quite capable of handling the volume of data it receives. 
In this case we don't need to complicate things, just use `return` in the implementation. 

```Python
from copy import deepcopy

from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings_threads import launch_demo_for_complex_case


def order_and_calculate(**kwargs):
    # Through storages we can obtain data from other pipelines
    db_connectors = kwargs['db_connectors']

    # Load all numbers from databases
    numbers_via_http = list(db_connectors['http_numbers'].load())
    numbers_via_mqtt = list(db_connectors['mqtt_numbers'].load())

    http_numbers = list(map(lambda x: int(x['Generated random number']), numbers_via_http))
    mqtt_numbers = list(map(lambda x: int(x['Generated number']), numbers_via_mqtt))

    # Create united list and sort it
    full_list = deepcopy(http_numbers)
    full_list.extend(mqtt_numbers)
    full_list.sort()

    # Calculate the value
    response_value = sum(http_numbers) - sum(mqtt_numbers)

    return {'sorted list': str(full_list), 'calculated value': response_value}


def launch_custom_flow():
    """
    Example of how to configure and launch flow with several pipelines, MongoDB storages and
    custom core
    """
    mongo_url = 'mongodb+srv://clusterdreamlone.ryubwzt.mongodb.net/?retryWrites=true&w=majority'
    mongo_user = 'dreamlone'
    mongo_password = 'mydreamlonepassword'
    
    flow_builder = FlowBuilder()

    # Pipeline for HTTP numbers processing
    flow_builder.add_pipeline('http_numbers', timedelta_seconds=10)\
        .with_http_connector(source='http://localhost:8027',
                             headers={'accept': 'application/json',
                                      'apikey': 'custom_key_1234'}) \
        .with_storage('mongo', source=mongo_url, database_name='wiredflow', collection_name='http_numbers',
                      username=mongo_user, password=mongo_password)

    # Pipeline for MQTT data processing
    flow_builder.add_pipeline('mqtt_numbers') \
        .with_mqtt_connector(source='localhost', port=1883,
                             topic='/demo/integers',
                             username='wiredflow', password='wiredflow') \
        .with_storage('mongo', source=mongo_url, database_name='wiredflow', collection_name='mqtt_numbers',
                      username=mongo_user, password=mongo_password)

    # Add pipeline with custom function and send stages
    flow_builder.add_pipeline('custom_logic', timedelta_seconds=15)\
        .with_core_logic(order_and_calculate)\
        .send(destination='localhost', port=1883, topic='demo/sorted', label_to_send='sorted list') \
        .send(destination='localhost', port=1883, topic='demo/subtraction', label_to_send='calculated value')

    flow = flow_builder.build()

    # Or simply flow.launch_flow()
    # if there is no need to launch local demo http server
    launch_demo_for_complex_case(flow, execution_seconds=30)


if __name__ == '__main__':
    launch_custom_flow()
```

As can be seen, the number of arguments in a custom function is unlimited. 
All of them will be passed to the body of the function as a dictionary. You can always access all available database connectors through the `db_connectors` field.
The syntax for these connectors will differ depending on which database you are using.

### Generator (`yield` something)

Sometimes the amount of data to be processed can be pretty large. 
Then you may want to divide your data into small portions and process them iteratively. 
At the same time, make sure that all subsequent stages in the pipeline 
are also applied in the declared order beforehand. Then just use the `yield` construction:

```Python
def order_and_calculate_by_batches(**kwargs):
    # Set processing limit
    max_number_of_items = 5
    db_connectors = kwargs['db_connectors']

    http_numbers = list(map(lambda x: int(x['Generated random number']), list(db_connectors['http_numbers'].load())))
    mqtt_numbers = list(map(lambda x: int(x['Generated number']), list(db_connectors['mqtt_numbers'].load())))

    if len(http_numbers) > max_number_of_items:
        # Process by batches
        start_batch_id = 0
        for i in range(max_number_of_items, len(http_numbers), max_number_of_items):
            print(f'Processing items from {start_batch_id} to {i}')
            batch_http_numbers = deepcopy(http_numbers[start_batch_id: i])
            batch_http_numbers.extend(mqtt_numbers)
            batch_http_numbers.sort()

            # Update the start id of item
            start_batch_id = i
            yield {'sorted list': str(batch_http_numbers),
                   'calculated value': sum(batch_http_numbers) - sum(mqtt_numbers)}
    else:
        full_list = deepcopy(http_numbers)
        full_list.extend(mqtt_numbers)
        full_list.sort()

        yield {'sorted list': str(full_list), 'calculated value': sum(http_numbers) - sum(mqtt_numbers)}
```

If we replace the core logic with `order_and_calculate_by_batches` function, we will obtain the following output in terminal: 

```
2023-04-26 10:31:06.715 | DEBUG    | wiredflow.main.actions.stages.core_stage:launch:17 - Launch core logic stage
Processing items from 0 to 5
2023-04-26 10:31:06.925 | DEBUG    | wiredflow.main.actions.stages.send_stage:send_to_subscribers:57 - Successfully send messages to topic demo/sorted via MQTT protocol
2023-04-26 10:31:06.982 | DEBUG    | wiredflow.main.actions.stages.send_stage:send_to_subscribers:57 - Successfully send messages to topic demo/subtraction via MQTT protocol
Processing items from 5 to 10
2023-04-26 10:31:07.059 | DEBUG    | wiredflow.main.actions.stages.send_stage:send_to_subscribers:57 - Successfully send messages to topic demo/sorted via MQTT protocol
2023-04-26 10:31:07.146 | DEBUG    | wiredflow.main.actions.stages.send_stage:send_to_subscribers:57 - Successfully send messages to topic demo/subtraction via MQTT protocol
Processing items from 10 to 15
2023-04-26 10:31:07.223 | DEBUG    | wiredflow.main.actions.stages.send_stage:send_to_subscribers:57 - Successfully send messages to topic demo/sorted via MQTT protocol
2023-04-26 10:31:07.301 | DEBUG    | wiredflow.main.actions.stages.send_stage:send_to_subscribers:57 - Successfully send messages to topic demo/subtraction via MQTT protocol
```

Let's take a closer look at how such a design is used. Running core logic. Then the function "understands" that there is too much data and splits the list into parts. 
For each part is calculated according to the business logic. As soon as the calculation is finished, the generated data structure is sent via senders.
That is, all subsequent stages are applied to each batch iteratively as they become available.

**Another example:** Imagine that the task for the designed service is to copy data from database 1 to database 2. We plan to repeat this procedure once a day.
Limitation - we cannot copy more than 10 rows from database 1 at once. 

In this case, if during the day in the database 1 appeared 100 new rows, then we need to repeat the operation 
to upload and save data in the database 2 10 times (10 rows each). Using the generator and yield operator allows to adapt the original logic natively to compute in a batch mode.
So, for example, if the pipeline consists of two stages "core logic - storage", then using the generator we will apply save action on each data partition in the cycle.
All of the actions described above will take place within one launch (the run in the current example is repeated once a day).
**The structure of the pipeline won't be any different when using a simple custom function - only the custom function itself will change!**

## Send stages

Below are a few words about senders. Senders are stages that allow sending notifications, data, various messages 
to third-party services. For example, it could be a message sent via MQTT protocol, or a small data sample via HTTP PUT method.
To add a send stage to the structure of the pipelines, the `send()` method is used.

Parameters for configuration: 

- `configuration` name of sender to apply or custom implementation. Possible options:

    - `mqtt` to send messages via MQTT. It is required to set `port` and `topic` if mqtt option is used
    - `http_post` to send message via HTTP post request
    - `http_put` to send message via HTTP put request

- `destination` - URL of destination - where to send messages
- `label_to_send` - name of data aggregation to send

All the stages used are run sequentially in the pipeline, so that each sends only the required chunk of data (determined by label to send).