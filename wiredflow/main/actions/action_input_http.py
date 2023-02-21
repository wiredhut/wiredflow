from typing import List, Optional
import schedule
import time

from wiredflow.main.actions.action_interface import Action
from wiredflow.main.actions.assimilation.interface import ProxyStage


class InputActionHttps(Action):
    """
    Class for input actions execution such as https get requests
    and data storing.

    Responsibility zone: Launching desired stages in suitable time stamps
    input data processing functionality. Launched by schedule
    """

    def __init__(self, pipeline_name: str, stages: List[ProxyStage], **params):
        super().__init__(pipeline_name, stages, **params)

    def execute_action(self):
        """ Launch process with defined parameters """
        number_of_seconds_to_break = self.timedelta_seconds / 2
        if number_of_seconds_to_break < 1:
            number_of_seconds_to_break = 1
        # Launch once before loop
        self.perform_action()

        schedule.every(self.timedelta_seconds).seconds.do(self.perform_action)
        while True:
            schedule.run_pending()
            time.sleep(number_of_seconds_to_break)

    def perform_action(self):
        """
        Launch defined stages execution in current action
        """
        # Get data via client connection
        relevant_info = self.launch_http_connector()
        if relevant_info is None:
            # Skip further steps
            return None

        # Store into database or into other source
        self.launch_storage(relevant_info)