import time
from typing import List, Optional

import schedule

from wiredflow.main.actions.action_interface import Action
from wiredflow.main.actions.assimilation.interface import ProxyStage


class FullProcessingAction(Action):
    """
    Launch data processing issues when the data has already been collected
    or were collecting during the pipeline execution.
    Apply scheduling for launches
    """

    def __init__(self, pipeline_name: str, stages: List[ProxyStage], **params):
        super().__init__(pipeline_name, stages, **params)

    def execute_action(self):
        """ Launch all processes in single flow """
        number_of_seconds_to_break = self.timedelta_seconds / 2
        if number_of_seconds_to_break < 1:
            number_of_seconds_to_break = 1

        schedule.every(self.timedelta_seconds).seconds.do(self.perform_action)
        while True:
            schedule.run_pending()
            time.sleep(number_of_seconds_to_break)

            if self.timeout_timer is not None and self.timeout_timer.is_limit_reached():
                # Finish execution
                break
            elif self.timeout_timer is not None and self.timeout_timer.will_limit_be_reached(number_of_seconds_to_break):
                break

    def perform_action(self):
        """ Launch all processes for desired launch """
        if self.connector is not None:
            # The connector is exist
            for obtained_data in self.launch_http_connector():
                if obtained_data is None:
                    continue

                self.launch_storage(obtained_data)
                core_data = self.launch_core(obtained_data)
                self.launch_senders(core_data)
        else:
            # There is no connector in the pipeline so launch core
            core_data = self.launch_core(None)
            self.launch_senders(core_data)
