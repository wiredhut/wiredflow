import time
from typing import List

import schedule
from loguru import logger

from wiredflow.main.actions.action_interface import Action, \
    calculate_break_interval
from wiredflow.main.actions.assimilation.interface import ProxyStage
from wiredflow.messages.failures_check import ExecutionStatusChecker
from wiredflow.settings import WARM_START_CORE_SECONDS


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
        number_of_seconds_to_break = calculate_break_interval(self.timedelta_seconds)

        # Launch once before loop - give some time for non core
        if self.params.get('delay_seconds') is not None:
            time.sleep(self.params.get('delay_seconds'))
        else:
            time.sleep(WARM_START_CORE_SECONDS)

        self.perform_action()

        schedule.every(self.timedelta_seconds).seconds.do(self.perform_action)
        while True:
            failures_checker = ExecutionStatusChecker()
            if failures_checker.status.is_ok is False:
                logger.info(f'Service failure due to "{failures_checker.ex}". '
                            f'Stop pipeline "{self.pipeline_name}" execution')
                break

            schedule.run_pending()

            if self.timeout_timer is not None and self.timeout_timer.is_limit_reached():
                # Finish execution
                break
            elif self.timeout_timer is not None and self.timeout_timer.will_limit_be_reached(number_of_seconds_to_break):
                break

            time.sleep(number_of_seconds_to_break)
