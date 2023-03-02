import datetime
from typing import Union, Callable


class Scheduler:
    """ Class for controlling execution time for desired functions """

    def __init__(self, function_to_launch: Callable,
                 timedelta_seconds: float,
                 launch_time: Union[str, None]):
        self.function_to_launch = function_to_launch
        self.timedelta_seconds = timedelta_seconds
        self.launch_time = launch_time

        self.start_time = datetime.datetime.now()

    def run(self):
        """ Launch function if it is time for that """
        if self.launch_time is None:
            self.launch_via_delta()
        else:
            self.launch_via_particular_time()

    def launch_via_delta(self):
        current_time = datetime.datetime.now()
        time_from_previous_launch = current_time - self.start_time

        if time_from_previous_launch.total_seconds() >= self.timedelta_seconds:
            self.start_time = datetime.datetime.now()
            self.function_to_launch()

    def launch_via_particular_time(self):
        raise NotImplementedError(f'Launch time does not supported yet')
