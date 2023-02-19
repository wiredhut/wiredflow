import time
from typing import List, Optional, Any

import paho.mqtt.client as mqtt

from wiredflow.main.actions.action_interface import Action


class MQTTMessagesProcessingSybAction:
    """ MQTT message processing with defined stages """
    def __init__(self, db_saver: Any):
        self.db_saver = db_saver
        self.messages = []

        # If flow with messages too frequent - it is possible to use small stack
        self.max_messages_in_stack = 1

    def launch_processors(self):
        """ Start execute processors """
        if len(self.messages) >= self.max_messages_in_stack:
            # Save data into database
            for mqtt_message in self.messages:
                self.db_saver.save(eval(mqtt_message.payload.decode("utf-8")))
            self.messages = []


class InputActionMQTT(Action):
    """
    Class for input actions execution such as mqtt subscribe and data storing.
    Always work with only MQTT data sources.

    Responsibility zone: Launching desired stages in suitable time stamps
    input data processing functionality. Launched by schedule
    """

    def __init__(self, pipeline_name: str, stages: List[dict], **params):
        super().__init__(pipeline_name, stages, **params)
        self.client = None

    def execute_action(self):
        """ Launch MQTT connection """
        # Get connector object and saver
        connector = self.init_stages[0]
        db_saver = self.init_stages[1]
        mqtt_processing = MQTTMessagesProcessingSybAction(db_saver)

        self.subscribe_to_broker(connector, mqtt_processing)

        # Launch as loop
        self.client.loop_forever()

    def subscribe_to_broker(self, connector: Any,
                            mqtt_processing: MQTTMessagesProcessingSybAction):
        """ Launch subscribe method for MQTT broker """
        self.client = mqtt.Client(userdata=mqtt_processing)
        # Authorization process
        self.client.username_pw_set(username='',
                                    password='')
        self.client = connector.configure_client(self.client)
