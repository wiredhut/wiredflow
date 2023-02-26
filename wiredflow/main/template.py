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
        is_http_input = self.p.with_get_request_action is True
        is_mqtt_input = self.p.with_mqtt_connection is True

        if is_mqtt_input:
            return InputActionMQTT(self.p.pipeline_name, self.p.stages, **self.params)

        elif is_http_input and self.p.with_core_action is False:
            return InputActionHttps(self.p.pipeline_name, self.p.stages, **self.params)

        else:
            return FullProcessingAction(self.p.pipeline_name, self.p.stages, **self.params)

