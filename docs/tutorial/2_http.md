# Single thread service with HTTP connector

On this page we will take a closer look at how wiredflow can handle HTTP requests. 
This example will be the basis of a larger service that we will build together by the end of this tutorial. 
We will gradually add new blocks step by step, increasing the complexity of the business logic (and the whole service).

Let's start with a simple example. Suppose we have a service (URL - `http://localhost:8027`) that returns a 
random number every time a GET request is sent. Let's assume that to use this service we have to use `apikey` - `custom_key_1234`.
Our task will be to build a service that makes such a request every 10 seconds and saves the results in a JSON file. 
Example for launching can be found below: 

```Python
from wiredflow.main.build import FlowBuilder
from wiredflow.mocks.demo_bindings_threads import remove_temporary_folder_for_demo, \
    launch_demo_with_int_http_connector


def launch_http_processing_flow():
    """
    Example of usage HTTP connector in the pipeline
    """
    flow_builder = FlowBuilder()

    # Repeat actions in pipeline every 1 minute - send GET request and store response
    flow_builder.add_pipeline('my_custom_name', timedelta_seconds=10)\
        .with_http_connector(source='http://localhost:8027',
                             headers={'accept': 'application/json',
                                      'apikey': 'custom_key_1234'})\
        .with_storage('json')

    # Configure service and launch it
    flow = flow_builder.build()

    # Or simply flow.launch_flow()
    # if there is no need to launch local demo http server
    launch_demo_with_int_http_connector(flow, execution_seconds=30)


if __name__ == '__main__':
    remove_temporary_folder_for_demo()
    launch_http_processing_flow()
```

Looks familiar, doesn't it? 

Indeed. This example is very similar to the one discussed on page ["Quick start"](1_quick_start.md). 
The only difference is in the `source` parameter that we specified, and the parameters that affect the execution time
(but this parameters are not vital here) . 
This is the convenience of using ETL pipelines built with wiredflow. They are pretty flexible. 

Thus, some of the key parameters that can significantly affect the behavior of a service using the HTTP connector are:

- `source` - endpoint URL to apply request
- `headers` - dictionary with headers for request. In this dictionary you can put credentials for initialization for example
- `configuration` - name of HTTP client realization to use or custom implementation. Possible variants: 
  - `get` - use HTTP GET method
  - `post` - use HTTP POST method
  - custom implementation through functions. See [Customization](7_customization.md) section for more information

Note that storage in this case stores data of any structure. So if we connect to another service and process the 
new data - we will have to change the `source` and credentials for authentication / authorization. 
**The structure of the pipeline will remain unchanged**. This feature seems to us to be a crucial property of wiredflow.

Nevertheless, launch example - output in the terminal: 

```
2023-04-12 14:25:14.357 | INFO     | wiredflow.main.flow:launch_flow:65 - Launch service with 1 pipelines using thread mode
2023-04-12 14:25:14.357 | INFO     | wiredflow.mocks.http_server:_start_mock_http_server:150 - Start mock HTTP server in separate process: 127.0.0.1, port 8027. Execution timeout, seconds: 30
2023-04-12 14:25:14.358 | INFO     | wiredflow.main.pipeline:run:155 - Launch pipeline "my_custom_name". Execution timeout, seconds: 30
2023-04-12 14:25:14.362 | DEBUG    | wiredflow.main.store_engines.json_engine.json_db:save:37 - JSON info. Storage json_in_my_custom_name successfully save data in .../wiredflow/files/json_in_my_custom_name.json
2023-04-12 14:25:24.370 | DEBUG    | wiredflow.main.store_engines.json_engine.json_db:save:37 - JSON info. Storage json_in_my_custom_name successfully save data in .../wiredflow/files/json_in_my_custom_name.json
2023-04-12 14:25:34.381 | DEBUG    | wiredflow.main.store_engines.json_engine.json_db:save:37 - JSON info. Storage json_in_my_custom_name successfully save data in .../wiredflow/files/json_in_my_custom_name.json
2023-04-12 14:25:39.387 | INFO     | wiredflow.wiredtimer.timer:will_limit_be_reached:44 - WiredTimer info: timeout was reached
2023-04-12 14:25:39.387 | INFO     | wiredflow.main.flow:launch_flow:79 - Flow finish execution
2023-04-12 14:26:04.411 | INFO     | wiredflow.mocks.http_server:_start_mock_http_server:165 - WiredTimer info: timeout was reached
```

From the logs it can be seen that the service was really running for 30 seconds. During this time our flow 
managed to send GET request three times. Check JSON file using mentioned path above in the terminal (".../wiredflow/files/json_in_my_custom_name.json"): 

```JSON
[
  {
    "Generated random number": 6
  },
  {
    "Generated random number": 91
  },
  {
    "Generated random number": 6
  }
]
```

Yes, indeed, pipeline saved all the data correctly. It is worth noting that you may obtain other 
values stored when you run this example (the mock HTTP server generates random numbers between 0 and 100).
