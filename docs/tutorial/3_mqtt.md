# Single thread service with MQTT connector

This section is devoted to building pipelines that are noticeably different from HTTP-connectors-based ones.
In this example we will use the MQTT protocol to receive messages (data). 
The key difference from the [previous pipeline](2_http.md) is that when we used the HTTP protocol, 
we requested the data ourselves according to a schedule. MQTT works differently.

We will build a so-called real-time service for continuous streaming workflows. 
That is, the service will subscribe to the MQTT broker and wait for a message from it. Messages may be sent irregularly!
As soon as the pipeline receives messages from the MQTT broker, it will save the data in a JSON file.

## What is MQTT protocol

<span style="color:orange">In progress</span>

## Service implementation 

A description of the task: The MQTT broker (localhost, port 1883, topic '/demo/integers') generates messages with a random number (range from 0 to 100). 
It is required to receive these messages and save them to a file.

The code below accomplishes this task
```Python
from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings_threads import remove_temporary_folder_for_demo, \
    launch_demo_with_int_mqtt_connector


def launch_mqtt_processing_flow():
    """
    Example of usage MQTT connector in the pipeline
    """
    flow_builder = FlowBuilder()

    # Subscribe to desired MQTT broker and start get messages
    flow_builder.add_pipeline('my_custom_name')\
        .with_mqtt_connector(source='localhost', port=1883, topic='/demo/integers',
                             username='wiredflow', password='wiredflow')\
        .with_storage('json')

    # Configure service and launch it
    flow = flow_builder.build()

    # Or simply flow.launch_flow()
    # if there is no need to launch local demo mqtt broker
    launch_demo_with_int_mqtt_connector(flow, execution_seconds=10)


if __name__ == '__main__':
    remove_temporary_folder_for_demo()
    launch_mqtt_processing_flow()
```

And this code is very similar to the one shown in the example with the HTTP connector. 
Except in this example the `with_mqtt_connector()` method was used during service building.

Output in the terminal: 

```
2023-04-12 14:40:09.792 | INFO     | wiredflow.main.flow:launch_flow:65 - Launch service with 1 pipelines using thread mode
2023-04-12 14:40:09.792 | INFO     | wiredflow.main.pipeline:run:155 - Launch pipeline "my_custom_name". Execution timeout, seconds: 10
2023-04-12 14:40:09.798 | DEBUG    | wiredflow.main.actions.stages.mqtt_stage:mqtt_on_connect:31 - Alert MQTT subscriber connected to topic /demo/integers with result code 0
2023-04-12 14:40:12.795 | INFO     | wiredflow.mocks.mqtt_broker:configure_int_mqtt_broker:27 - Start mock MQTT broker in separate process - topic: /demo/integers. Execution timeout, seconds: 10
2023-04-12 14:40:12.796 | DEBUG    | wiredflow.mocks.mqtt_broker:configure_int_mqtt_broker:36 - MQTT local broker. Send generated int 0 from topic /demo/integers
2023-04-12 14:40:12.832 | DEBUG    | wiredflow.main.store_engines.json_engine.json_db:save:37 - JSON info. Storage json_in_my_custom_name successfully save data in .../wiredflow/files/json_in_my_custom_name.json
2023-04-12 14:40:13.798 | DEBUG    | wiredflow.mocks.mqtt_broker:configure_int_mqtt_broker:36 - MQTT local broker. Send generated int 1 from topic /demo/integers
2023-04-12 14:40:13.869 | DEBUG    | wiredflow.main.store_engines.json_engine.json_db:save:37 - JSON info. Storage json_in_my_custom_name successfully save data in .../wiredflow/files/json_in_my_custom_name.json
2023-04-12 14:40:14.800 | DEBUG    | wiredflow.mocks.mqtt_broker:configure_int_mqtt_broker:36 - MQTT local broker. Send generated int 2 from topic /demo/integers
2023-04-12 14:40:14.877 | DEBUG    | wiredflow.main.store_engines.json_engine.json_db:save:37 - JSON info. Storage json_in_my_custom_name successfully save data in .../wiredflow/files/json_in_my_custom_name.json
2023-04-12 14:40:15.802 | DEBUG    | wiredflow.mocks.mqtt_broker:configure_int_mqtt_broker:36 - MQTT local broker. Send generated int 3 from topic /demo/integers
2023-04-12 14:40:15.863 | DEBUG    | wiredflow.main.store_engines.json_engine.json_db:save:37 - JSON info. Storage json_in_my_custom_name successfully save data in .../wiredflow/files/json_in_my_custom_name.json
2023-04-12 14:40:16.804 | DEBUG    | wiredflow.mocks.mqtt_broker:configure_int_mqtt_broker:36 - MQTT local broker. Send generated int 4 from topic /demo/integers
2023-04-12 14:40:16.870 | DEBUG    | wiredflow.main.store_engines.json_engine.json_db:save:37 - JSON info. Storage json_in_my_custom_name successfully save data in .../wiredflow/files/json_in_my_custom_name.json
2023-04-12 14:40:17.806 | DEBUG    | wiredflow.mocks.mqtt_broker:configure_int_mqtt_broker:36 - MQTT local broker. Send generated int 5 from topic /demo/integers
2023-04-12 14:40:17.852 | DEBUG    | wiredflow.main.store_engines.json_engine.json_db:save:37 - JSON info. Storage json_in_my_custom_name successfully save data in .../wiredflow/files/json_in_my_custom_name.json
2023-04-12 14:40:18.807 | DEBUG    | wiredflow.mocks.mqtt_broker:configure_int_mqtt_broker:36 - MQTT local broker. Send generated int 6 from topic /demo/integers
2023-04-12 14:40:18.868 | DEBUG    | wiredflow.main.store_engines.json_engine.json_db:save:37 - JSON info. Storage json_in_my_custom_name successfully save data in .../wiredflow/files/json_in_my_custom_name.json
2023-04-12 14:40:19.792 | INFO     | wiredflow.wiredtimer.timer:is_limit_reached:29 - WiredTimer info: timeout was reached
2023-04-12 14:40:19.808 | INFO     | wiredflow.wiredtimer.timer:is_limit_reached:29 - WiredTimer info: timeout was reached
2023-04-12 14:40:19.869 | INFO     | wiredflow.main.flow:launch_flow:79 - Flow finish execution
```

The service worked for 10 seconds and during that time it received one message per second 
(when no messages came, the pipelines waited). 
As expected, all values are saved in the JSON file:

```JSON
[
  {
    "Generated number": "0"
  },
  {
    "Generated number": "1"
  },
  {
    "Generated number": "2"
  },
  {
    "Generated number": "3"
  },
  {
    "Generated number": "4"
  },
  {
    "Generated number": "5"
  },
  {
    "Generated number": "6"
  }
]
```

Congratulations! - You learned how to configure a service with an MQTT connector