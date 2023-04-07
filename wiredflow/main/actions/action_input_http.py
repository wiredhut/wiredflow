from typing import List, Union
import time

from loguru import logger

from wiredflow.main.actions.action_interface import Action, \
    calculate_break_interval
from wiredflow.main.actions.assimilation.interface import ProxyStage
from wiredflow.messages.failures_check import ExecutionStatusChecker
from wiredflow.schedule import Scheduler


class InputActionHttps(Action):
    """
    Class for input actions execution such as https get requests
    and data storing.

    Responsibility zone: Launching desired stages in suitable time stamps
    input data processing functionality. Launched by schedule
    """

    def __init__(self, pipeline_name: str, stages: List[ProxyStage], **params):
        super().__init__(pipeline_name, stages, **params)

    def execute_action(self, failures_checker: ExecutionStatusChecker):
        """ Launch process with defined parameters """
        number_of_seconds_to_break = calculate_break_interval(self.timedelta_seconds)
        if self.params.get('delay_seconds') is not None:
            # If there is a need to wait several seconds before start action execution
            time.sleep(self.params.get('delay_seconds'))

        # Launch once before loop
        self.perform_action()

        if self.timeout_timer is not None and self.timeout_timer.is_limit_reached():
            return None
        elif self.timeout_timer is not None and self.timeout_timer.will_limit_be_reached(number_of_seconds_to_break):
            return None

        scheduler = Scheduler(self.perform_action, self.timedelta_seconds, self.launch_time)
        while True:
            if failures_checker.is_current_status_ok() is False:
                logger.info(f'Service failure due to "{failures_checker.exception_message()}". '
                            f'Stop pipeline "{self.pipeline_name}" execution')
                break

            scheduler.run()
            if self.timeout_timer is not None and self.timeout_timer.is_limit_reached():
                # Finish execution
                break
            elif self.timeout_timer is not None and self.timeout_timer.will_limit_be_reached(number_of_seconds_to_break):
                break

            time.sleep(number_of_seconds_to_break)

        return None
