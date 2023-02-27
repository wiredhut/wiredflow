from dataclasses import dataclass
from typing import Union

from threading import Lock


@dataclass
class ExecutionStatus:
    is_ok: bool


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
        self.ex = None
