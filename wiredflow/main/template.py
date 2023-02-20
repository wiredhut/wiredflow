from wiredflow.main.actions.action_input_http import InputActionHttps
from wiredflow.main.actions.action_input_mqtt import InputActionMQTT
from wiredflow.main.actions.actions_full import FullProcessingAction


class PipelineActionTemplate:
    """
    Based on stages in pipeline define appropriate template
    and group stages into suitable actions

    :param pipeline: pipeline object with configured execution pool
    """

    def __init__(self, pipeline, **params):
        self.p = pipeline
        self.params = params

    def compile_action(self):
        """ Compile action based on pipeline """
        is_http_input = self.p.with_get_request_action is True and self.p.with_storage_action is True
        is_mqtt_input = self.p.with_mqtt_connection is True and self.p.with_storage_action is True

        if len(self.p.stages) <= 3 and is_http_input:
            # Short pipeline with only input data actions (use https connection)
            return InputActionHttps(self.p.pipeline_name, self.p.stages, **self.params)

        elif len(self.p.stages) <= 3 and is_mqtt_input:
            # Short pipeline with only input data actions (use mqtt connection)
            return InputActionMQTT(self.p.pipeline_name, self.p.stages, **self.params)

        elif len(self.p.stages) >= 2 and self.p.with_core_action is True:
            # Relatively long pipeline with core action
            return FullProcessingAction(self.p.pipeline_name, self.p.stages, **self.params)

        else:
            raise NotImplementedError(f'Does not support pipeline "{self.p.pipeline_name}" due to unexpected structure')
