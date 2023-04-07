from typing import Optional

from wiredflow.main.pipeline import generate_pipeline_name, Pipeline
from wiredflow.main.flow import FlowProcessor


class FlowBuilder:
    """
    Class for flows building

    NB: only if all income components are obtained launch common
    processing core with business logic. If not - it is uses just
    separate modules to perform local tasks. Checking the condition
    of sufficiency of connectors is checked at the core logic level

    :param use_threads: is there a need to use threads or processes to launch
    pipelines
    """

    def __init__(self, use_threads: bool = True):
        self.processor = FlowProcessor(use_threads)
        self.use_threads = use_threads

    def add_pipeline(self, pipeline_name: Optional[str] = None,
                     **params):
        """
        Add new pipeline to execution pool

        :param pipeline_name: name of pipeline to add for better debugging
        and identification purposes (mainly for core logic implementation)
        """
        pipeline_name = generate_pipeline_name(pipeline_name)

        if pipeline_name in list(self.processor.processing_pool.keys()):
            raise ValueError('Pipeline names in processor must be unique. Duplicates were detected')

        new_pipeline = Pipeline(pipeline_name, self.use_threads, **params)
        self.processor.add_new_pipeline_into_pool(new_pipeline)
        return new_pipeline

    def build(self) -> FlowProcessor:
        """ Return Flow processing object to be executed """
        return self.processor
