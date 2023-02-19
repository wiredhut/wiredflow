from typing import List, Optional
import schedule
import time

from wiredflow.main.actions.action_interface import Action


class InputActionHttps(Action):
    """
    Class for input actions execution such as https get requests
    and data storing.

    Responsibility zone: Launching desired stages in suitable time stamps
    input data processing functionality. Launched by schedule
    """

    def __init__(self, pipeline_name: str, stages: List[dict], **params):
        super().__init__(pipeline_name, stages, **params)

    def execute_action(self):
        """ Launch process with defined parameters """
        number_of_seconds_to_break = (self.timedelta_minutes * 60) / 2
        if number_of_seconds_to_break < 1:
            number_of_seconds_to_break = 1
        # Launch once before loop
        self.perform_action()

        schedule.every(self.timedelta_minutes).minutes.do(self.perform_action)
        while True:
            schedule.run_pending()
            time.sleep(number_of_seconds_to_break)

    def perform_action(self):
        """
        Launch defined stages execution in current action
        """
        # Get data via client connection
        for relevant_info in self.launch_http_connector():
            if relevant_info is None:
                # Skip further steps
                continue

            # Store into database or into other source
            self.launch_saver(relevant_info)
