# Functionality review

This page provides an overview of existing and planned functionality in the library. 
Here, in the form of tables and graphs, the main components of the pipelines and services 
blocks and their possible variations are shown.

## Brief introduction

First, a short section on terms. Services in wiredflow are called **Flow** or **Service**. 
A **service** can consist of one or more **pipelines**. 
**Pipelines** can consist of individual operations (**stages**). 

That's it - move on!

## What services can be designed?

With the functionality of this library, it is possible to compile services that:

1. Get data from external sources (e.g., using HTTP);
2. Transform data, merge data from various sources, perform calculations - business logic;
3. Save data into databases or files (.csv, .json);
4. Send messages (e.g. alerts) to external services;
5. Repeat above mentioned actions with a certain period (by schedule) - it is possible to use an internal scheduler;
6. Log execution and catch failures from each service component to ensure the consistency of the whole flow.

As stated in the library description, wiredflow can be used as a regular 
Python library, and you can run prototypes locally without using additional 
technologies such as CRON or docker. 
However, you can always use additional tools if you wish. 
Thus, the library is suitable for constructing and running ETL services.

Wiredflow is a multifunctional constructor. The users define the structure of 
the pipelines and the entire service architecture on their own. 
However, wiredflow [will suggest the most reliable option](friend.md).

## What stages can a Pipeline consist of?

Wiredflow allows users to design services with any number of pipelines. 
Pipelines can also consist of different number of stages.
Let's take a look at the possible combinations: 

<img src="https://raw.githubusercontent.com/wiredhut/wiredflow/main/docs/media/flow_examples.png" width="800"/>

Thus, there are the following possible stages in pipelines:

- **Configuration** - requires a custom implementation. The stage configures the parameters for the following stages;
- **Connectors** (HTTP and MQTT connector) - connector to external data source;
- **Storage** - save data into file or database;
- **Core logic** - requires a custom implementation. Business logic of developing application;
- **Send** - send messages from service to external services.

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

