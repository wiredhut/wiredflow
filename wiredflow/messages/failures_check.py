from dataclasses import dataclass

from threading import Lock
from typing import Any, Optional


@dataclass
class ExecutionStatus:
    is_ok: bool
    ex: Optional[Any] = 'Exception does not arisen'


class FailuresCheckMeta(type):
    """ Thread-safe realization of Failures check singleton """
    # Objects for synchronization
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls):
        with cls._lock:
            if cls not in cls._instances:
                status = ExecutionStatus(is_ok=True)
                instance = super().__call__(status)
                cls._instances[cls] = instance
        return cls._instances[cls]


class ExecutionStatusChecker(metaclass=FailuresCheckMeta):

    def __init__(self, status: ExecutionStatus):
        self.status = status

    def is_current_status_ok(self):
        return self.status.is_ok

    def set_failed_status(self, exception_message):
        self.status.is_ok = False
        self.status.ex = exception_message

    def exception_message(self):
        return self.status.ex