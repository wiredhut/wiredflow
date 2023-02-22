import datetime
from typing import Union

from loguru import logger


class WiredTimer:
    """
    Class for measuring time
    """

    def __init__(self, execution_seconds: Union[int, None]):
        self.current_spend_time = datetime.datetime.now()
        self.execution_seconds = execution_seconds

    def is_limit_reached(self):
        """ Check does the timeout limit was reached or not """
        if self.execution_seconds is None:
            # There is no limit for execution
            return False

        current_time = datetime.datetime.now()
        spend_time = current_time - self.current_spend_time

        if spend_time.total_seconds() >= self.execution_seconds:
            logger.info(f'WiredTimer info: timeout was reached')
            return True
        else:
            return False

    def will_limit_be_reached(self, sleep_seconds: float):
        """ Check if the timeout will be reached after sleep time """
        if self.execution_seconds is None:
            # There is no limit for execution
            return False

        current_time = datetime.datetime.now()
        spend_time = current_time - self.current_spend_time

        if (spend_time.total_seconds() + sleep_seconds) >= self.execution_seconds:
            logger.info(f'WiredTimer info: timeout was reached')
            return True
        else:
            return False
