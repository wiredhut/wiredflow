# Customization

When developing services, we are inevitably faced with the need to implement custom business logic.
Wiredflow allows flexible implementation of custom logic at various stages of development using simple 
primitives - Python functions. 

The integration will not require the implementation of classes with specific methods, inheritance,
etc. Everything is pretty transparent - a custom function will have one entry 
point and one exit point. 

In this document you will find detailed instructions describing how to implement 
and integrate "self-made" functions into wiredflow-based service.

## Common description 

Wiredflow consists of several key blocks (stages). Some stages do not involve default implementations and require custom implementations in any case:

- **Configuration** - Configure parameters for next stage in the pipeline;
- **Core logic** - General abstraction to implement custom logic.

The following stages have default implementations, but they can easily be replaced with custom ones

- **HTTP connector** - Retrieving data using `HTTP` requests - active requester;
- **MQTT connector** - Retrieving data using `MQTT` protocol - passive subscriber;
- **Storage** - Client to database;
- **Send** - Send messages to external services.

**NB**: It is up to you to decide in which block to implement the custom functions. 
Depending on the task description above, feel free to choose the right architecture 
for application. However, it's always possible, for example, to implement 
completely custom pipelines with only core logic blocks.

To insert a custom function into a declared stage, simply pass its 
implementation to the parameter `configuration` (first argument):

```Python
from wiredflow.main.build import FlowBuilder


def custom_function_first(**kwargs):
    print('Hello')


def custom_function_second(**kwargs):
    print('World!')


# Service implementation
flow_builder = FlowBuilder()
flow_builder.add_pipeline('my_logic').with_core_logic(custom_function_first).with_http_connector(custom_function_second)
```


## Implementation examples 

### Function (`return` something)

Let's start with the simple example. 
Suppose your service should go to database 1, take information A from it, 
then get information B from database 2, merge the data, and pass the dictionary on. 

Implementation of the service using wiredflow will look the following 
(full code snippet can be found in [advanced_http.py](../examples/threads/advanced_http.py) example):

```Python
from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings_threads import remove_temporary_folder_for_demo, launch_demo_with_several_http_connectors

# Initialize builder
flow_builder = FlowBuilder()

# Launch pipeline every 10 seconds
flow_builder.add_pipeline('integers_processing', timedelta_seconds=10).with_http_connector(source='http://localhost:8027').with_storage('json', preprocessing='add_datetime')

# Launch pipeline every 1 minute and overwrite all previous recordings
flow_builder.add_pipeline('letters_processing', timedelta_seconds=60).with_http_connector(source='http://localhost:8026').with_storage('json', preprocessing='add_datetime', mapping='overwrite')

# Core logic of our case
# Configure notification sender: send message based on calculation approach
flow_builder.add_pipeline('core_matching', timedelta_seconds=30, delay_seconds=10).with_core_logic(toy_example_logic).send(destination='localhost', port=1883, topic='demo/uppercase', label_to_send='uppercase').send(destination='localhost', port=1883, topic='demo/lowercase', label_to_send='lowercase')

# Configure service and launch it
flow = flow_builder.build()

# Or simply flow.launch_flow()
# if there is no need to launch local demo http servers
launch_demo_with_several_http_connectors(flow)
```

In this case we need to implement a function "toy_example_logic" with the following signature:

```Python
def toy_example_logic(**parameters_to_use):
    return {}
```

As can be seen, the number of arguments in a custom function is unlimited. 
All of them will be passed to the body of the function as a dictionary.

You can always access all available database connectors through the `db_connectors` field.
The syntax for these connectors will differ depending on which database you are using:

```Python
def toy_example_logic(**parameters_to_use):
    db_connectors = parameters_to_use['db_connectors']
    available_integers = db_connectors['integers_processing'].load()
    current_letter = db_connectors['letters_processing'].load()[0]

    if available_integers is None or current_letter is None:
        # Skip current iteration - there are no data to process
        return None

    # Transform dictionary into values
    integers = list(map(lambda x: int(x['Generated random number']), available_integers))
    
    # Generate messages
    message = {}
    if current_letter['Generated random letter'].isupper():
        # We need to calculate sum
        response = sum(integers)
        message.update({'uppercase': f'Calculated value is {response}'})
    else:
        # Mean value because current letter is lowercase
        response = sum(integers) / len(integers)
        message.update({'lowercase': f'Calculated value is {response}'})
    return message
```

### Generator (`yield` something)

Sometimes the amount of data to be processed can be pretty large. 
Then you may want to divide your data into small portions and process them iteratively. 
At the same time, make sure that all subsequent stages in the pipeline 
are also applied in the declared order beforehand. Then just use the `yield` construction:

```Python
def batch_data_processing(**parameters_to_use):
    """ Load all available data from database and pass small data batches further """
    db_connectors = parameters_to_use['db_connectors']
    available_integers = db_connectors['integers_processing'].load()

    if available_integers is None:
        return None

    # Transform dictionary into values
    integers = list(map(lambda x: int(x['Generated random number']), available_integers))
    
    for current_integer in integers:
        # Simple case - pass single values
        yield current_integer
```

Let's take a closer look at how such a design is used. For this we will consider the real task of. 
Imagine that the task for the designed service is to copy data from database 1 to database 2. We plan to repeat this procedure once a day.
Limitation - we cannot copy more than 10 rows from database 1 at once. 

In this case, if during the day in the database 1 appeared 100 new rows, then we need to repeat the operation 
to upload and save data in the database 2 10 times (10 rows each). Using the generator and yield operator allows to adapt the original logic natively to compute in a batch mode.
So, for example, if the pipeline consists of two stages "core logic - storage", then using the generator we will apply save action on each data partition in the cycle.
All of the actions described above will take place within one launch (the run in the current example is repeated once a day).
**The structure of the pipeline won't be any different than when using a simple custom function - only the custom function itself will change!**
