from typing import List, Any, Union

import paho.mqtt.client as mqtt

from wiredflow.main.actions.action_interface import Action
from wiredflow.main.actions.assimilation.interface import ProxyStage
from wiredflow.main.actions.stages.mqtt_stage import StageMQTTConnectorInterface
from wiredflow.messages.failures_check import ExecutionStatusChecker
from wiredflow.wiredtimer.timer import WiredTimer


class MQTTMessagesProcessingSybAction:
    """ MQTT message processing with defined stages """
    def __init__(self, db_saver: Any, topic: str, timeout_timer: WiredTimer):
        self.db_saver = db_saver
        self.topic = topic
        self.messages = []

        self.timeout_timer = timeout_timer

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

    def __init__(self, pipeline_name: str, stages: List[ProxyStage], **params):
        super().__init__(pipeline_name, stages, **params)
        self.client = None

    def execute_action(self, failures_checker: ExecutionStatusChecker):
        """ Launch MQTT connection """
        # Get connector object and saver
        connector = self.init_stages[0]
        db_saver = self.init_stages[1]
        mqtt_processing = MQTTMessagesProcessingSybAction(db_saver, connector.topic,
                                                          self.timeout_timer)

        self.subscribe_to_broker(connector, mqtt_processing)

        # Launch as loop
        if self.timeout_timer is not None and self.timeout_timer.execution_seconds is not None:
            while self.timeout_timer.is_limit_reached() is False and failures_checker.is_current_status_ok() is True:
                self.client.loop_start()
            self.client.loop_stop()
            exit()
        else:
            # Execute till other threads are working
            while failures_checker.is_current_status_ok() is True:
                self.client.loop_start()
            self.client.loop_stop()

    def subscribe_to_broker(self, connector: StageMQTTConnectorInterface,
                            mqtt_processing: MQTTMessagesProcessingSybAction):
        """ Launch subscribe method for MQTT broker """
        self.client = mqtt.Client(userdata=mqtt_processing)
        # Authorization process
        self.client.username_pw_set(username=connector.username,
                                    password=connector.password)
        self.client = connector.configure_client(self.client)
