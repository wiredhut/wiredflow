import threading
from wiredflow.main.pipeline import Pipeline


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

    def __init__(self):
        self.processing_pool = {}
        # Information about DB connectors (extractors) in each pipeline
        # DB connectors help to get information about databases in the system
        # So through Processor it's available to get access to the all databases
        # in all pipelines
        self.extract_objects = {}

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

        self._reassign_db_connectors_to_core_logic_pipeline()

    def launch_flow(self):
        """ Launch each pipeline in its own thread """
        self.initialize_internal_structure()

        threads = [threading.Thread(target=launch_pipeline, args=(pipeline,))
                   for pipeline in self.processing_pool.values()]

        # Launch pipelines without core processing
        for thread in threads:
            thread.start()

        # Finish all threads processing
        for thread in threads:
            thread.join()

    def _get_db_connectors(self):
        """ Get instances of all DB connectors from all pipelines """
        for pipeline_name, pipeline in self.processing_pool.items():
            if pipeline.with_storage_action is True:
                extract_object = pipeline.action.get_db_connector_object
                self.extract_objects.update({pipeline_name: extract_object})

    def _reassign_db_connectors_to_core_logic_pipeline(self):
        """
        Assign DB connectors from data getter pipelines to one with core logic.
        It allows to core logic submodule get access to all desired databases
        (storages) in the pipeline
        """
        for pipeline_name, pipeline in self.processing_pool.items():
            if pipeline.with_core_action is True:
                pipeline.db_connectors = self.extract_objects


def launch_pipeline(pipeline):
    pipeline.run()
