# Functionality review

This page provides an overview of existing and planned functionality in the library. 
Here, in the form of tables and graphs, the main components of the pipelines and services 
blocks and their possible variations are shown. 

## Brief introduction 

First, a short section on terms. Services in wiredflow are called **Flow** or **Service**. 
A **service** can consist of one or more **pipelines**. 
**Pipelines** can consist of individual operations (**stages**). 

That's it - move on!

## What stages can a Pipeline consist of?

Wiredflow allows users to design services with any number of pipelines. Pipelines can also consist of different number of stages.
Let's take a look at the possible combinations: 

<img src="https://raw.githubusercontent.com/wiredhut/wiredflow/main/docs/media/flow_examples.png" width="800"/>

Thus, there are the following possible stages in pipelines:
* **Configuration** - requires a custom implementation. The stage configures the parameters for the following stages;
* **Connectors** (HTTP and MQTT connector) - connector to external data source;
* **Storage** - save data into file or database;
* **Core logic** - requires a custom implementation. Business logic of developing application;
* **Send** - send message from service to external services.

Some stages always require custom implementation, others have several possible default configurations.
Wiredflow uses a builder to generate services, so the pipelines are modified by sequentially adding blocks. 

### Available connectors (per protocols)

| Connector |   Command for adding    | Short description                                                          |
|-----------|-------------------------|----------------------------------------------------------------------------|
| MQTT      | `with_mqtt_connector()` | Create stage with ability to subscribe to MQTT topic and recieve data      |
| HTTP      | `with_http_connector()` | Create stage with ability to send GET requests using HTTP / HTTPS protocol |

### Available storages (databases and files storages for local usage)

|  Storage  |      Command for adding           | Short description                                             |
|-----------|-----------------------------------|---------------------------------------------------------------|
| JSON file | `with_storage('json', **params)`  | Create and use local JSON file and use it as data storage     |
| CSV file  | `with_storage('csv', **params)`   | Create and use local CSV file and use it as data storage      |
| MongoDB   | `with_storage('mongo', **params)` | Define connect to already initialized MongoDB instance        |

### Available senders

|  Sender       |      Command for adding       | Short description                                        |
|---------------|-------------------------------|----------------------------------------------------------|
| MQTT broker   | `send('mqtt', **params)`      | Send defined data aggregate using MQTT protocol          |
| POST request  | `send('http_post', **params)` | Send defined data aggregate using HTTP POST method       |
| PUT request   | `send('http_put', **params)`  | Send defined data aggregate using HTTP PUT method        |

