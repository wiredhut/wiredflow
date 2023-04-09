# Functionality review

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

