# Single thread service with HTTP connector

On this page we will take a closer look at how wiredflow can handle HTTP requests. 
This example will be the basis of a larger service that we will build together by the end of this tutorial. 
We will gradually add new blocks step by step, increasing the complexity of the business logic.

Let's start with a simple example. Suppose we have a service (URL - `http://localhost:8027`) that returns a 
random number every time a GET request is sent. Our task will be to build a service that makes such a request every 10 seconds and saves the results in a JSON file. 
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
        .with_storage('json', preprocessing='add_datetime')

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
The only difference is in the `source` parameter that we specified, and the parameters that affect the execution time. 
This is the convenience of using ETL pipelines built with wiredflow. They are pretty flexible. 

Thus, some of the key parameters that can significantly affect the behavior of a service using the HTTP connector are:

- `source` - endpoint URL to apply request
- `headers` - dictionary with headers for request. In this dictionary you can put credentials for initialization
- `configuration` - name of HTTP client realization to use or custom implementation. Possible variants: 
  - `get` - use HTTP GET method
  - `post` - use HTTP POST method
  - custom implementation through functions. See [Customization](7_customization.md) section for more information

<span style="color:orange">In progress</span>
