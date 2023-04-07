from threading import Event as ThreadEvent
from multiprocessing import Lock


class EventSynchronization:
    """
    Class for processes and threads synchronization. Based on current mode
    apply threads or processes synchronization
    """

    def __init__(self, use_threads: bool):
        self.use_threads = use_threads
        if self.use_threads is True:
            self.event = ThreadEvent()
        else:
            self.lock = Lock()

    def initialize(self):
        if self.use_threads:
            self.event.set()

    def wait(self):
        if self.use_threads:
            self.event.wait()
            self.event.clear()
        else:
            self.lock.acquire()

    def release(self):
        if self.use_threads:
            self.event.set()
        else:
            self.lock.release()
