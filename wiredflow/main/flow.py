import multiprocessing
import threading
from multiprocessing import Lock
from multiprocessing.context import Process
from multiprocessing.managers import Namespace, BaseManager
from multiprocessing.pool import Pool

from typing import Union, Optional

from loguru import logger

from wiredflow.main.pipeline import Pipeline
from wiredflow.messages.failures_check import ExecutionStatusChecker
from wiredflow.wiredtimer.timer import WiredTimer

# SuperFastPython.com
# example of using a manager to create a custom class
from time import sleep
from random import random
from multiprocessing import Process
from multiprocessing.managers import BaseManager


class FlowProcessor:
    """
    Class for launching all defined tasks (pipelines) in the processing pool
    using Python threads - launch each pipeline in new separate thread. So
    all pipelines can be executed "simultaneously"

    TaskProcessor launch Pipelines, Pipeline launch Actions and Action
    launch Stages
    Responsibility zone: Launching all defined pipelines in threads and
    ensuring their consistency
    """

    def __init__(self, use_threads: bool = True):
        self.processing_pool = {}
        # Information about DB connectors (extractors) in each pipeline
        # DB connectors help to get information about databases in the system
        # So through Processor it's available to get access to the all databases
        # in all pipelines
        self.extract_objects = {}
        self.use_threads = use_threads

    def add_new_pipeline_into_pool(self, pipeline: Pipeline):
        """
        Add new pipeline for further execution during launch method call
        """
        self.processing_pool.update({pipeline.pipeline_name: pipeline})

    def initialize_internal_structure(self):
        """ Initialize actions and stages in nested abstractions """

        # Initialize actions in the pipelines
        for pipeline in self.processing_pool.values():
            pipeline.create_action()
        self._get_db_connectors()

        self._reassign_db_connectors_to_custom_pipeline()

    def launch_flow(self, execution_seconds: Union[int, None] = None):
        """
        Launch each pipeline in its own thread

        :param execution_seconds: timeout for process execution in seconds
        """
        timeout_timer = WiredTimer(execution_seconds)

        self.initialize_internal_structure()

        timeout_timer.set_failures_time()
        if self.use_threads is True:
            logger.info(f'Launch service with {len(self.processing_pool.values())} pipelines using thread mode')
            failures_checker = ExecutionStatusChecker()
            # Launch threads
            threads = [threading.Thread(target=launch_pipeline, args=(pipeline, timeout_timer, failures_checker))
                       for pipeline in self.processing_pool.values()]

            # Launch pipelines into separate threads
            for thread in threads:
                thread.start()

            # Finish all threads processing
            for thread in threads:
                thread.join()

            logger.info(f'Flow finish execution')
            if failures_checker.is_current_status_ok() is False:
                raise ValueError(f'Service was failed. Please reconfigure flow. '
                                 f'Exception: {failures_checker.exception_message()}')
        else:
            logger.info(f'Launch service with {len(self.processing_pool.values())} pipelines using parallel mode')

            BaseManager.register('ExecutionStatusChecker', ExecutionStatusChecker)
            with BaseManager() as manager:
                failures_checker = manager.ExecutionStatusChecker()
                processes = [Process(target=launch_pipeline, args=(pipeline, timeout_timer, failures_checker))
                             for pipeline in self.processing_pool.values()]

                # Launch pipelines into separate processes
                for process in processes:
                    process.start()

                # Finish all threads processing
                for process in processes:
                    process.join()

                logger.info(f'Flow finish execution')
                if failures_checker.is_current_status_ok() is False:
                    raise ValueError(f'Service was failed. Please reconfigure flow. '
                                     f'Exception: {failures_checker.exception_message()}')
        return failures_checker.status.is_ok

    def _get_db_connectors(self):
        """ Get instances of all DB connectors from all pipelines """
        for pipeline_name, pipeline in self.processing_pool.items():
            if pipeline.action.get_db_connector_object is not None:
                extract_object = pipeline.action.get_db_connector_object
                self.extract_objects.update({pipeline_name: extract_object})

    def _reassign_db_connectors_to_custom_pipeline(self):
        """
        Assign DB connectors from data getter pipelines to one with core logic
        or custom configuration logic.
        It allows to core logic submodule get access to all desired databases
        (storages) in the pipeline
        """
        for pipeline_name, pipeline in self.processing_pool.items():
            if pipeline.with_core_action is True:
                pipeline.db_connectors = self.extract_objects
            if pipeline.with_configuration_action is True:
                pipeline.db_connectors = self.extract_objects


def launch_pipeline(pipeline, timeout_timer: WiredTimer, failures_checker: ExecutionStatusChecker):
    """ Wrapper for launching in separate process or thread

    :param pipeline: pipeline to launch
    :param timeout_timer: object for checking allocated time
    :param failures_checker: failures checker object or AutoProxy
    """
    try:
        pipeline.run(timeout_timer, failures_checker)
    except Exception as ex:
        # Set new status - message will propagate to other threads
        failures_checker.set_failed_status(ex)

        logger.info(f'Service failure due to "{failures_checker.exception_message()}". '
                    f'Stop pipeline "{pipeline.pipeline_name}" execution')

        return None
