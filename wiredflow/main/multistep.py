import inspect

from wiredflow.main.actions.stages.configuration_stage import \
    ConfigurationInterface
from wiredflow.main.actions.stages.core_stage import CoreLogicInterface
from wiredflow.main.actions.stages.http_stage import StageCustomHTTPConnector


def is_current_stage_multi_step(current_stage) -> bool:
    """
    Check if current stage multi step (implemented through generator) or not
    """
    is_config = isinstance(current_stage, ConfigurationInterface)
    is_core = isinstance(current_stage, CoreLogicInterface)
    is_custom_http = isinstance(current_stage, StageCustomHTTPConnector)

    if is_config is True or is_core is True or is_custom_http is True:
        return inspect.isgeneratorfunction(current_stage.function_to_launch)

    # For all other cases it will always be single execution
    return False
