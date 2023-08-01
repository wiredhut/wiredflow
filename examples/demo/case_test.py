from pathlib import Path

from loguru import logger

from wiredflow.main.build import FlowBuilder


TOKEN = "Bearer token"
URL = "https://datahub.sbcdc.ch/swip_test/api/heatmaps/total/hourly?datetime=2023-01-12T10%3A00&zone_id=238&soft_calculation=false"


def check_output(**parameters_to_use):
    """ Check that output from endpoint has appropriate structure """
    db_connectors = parameters_to_use['db_connectors']
    testing_pipeline_artifacts = db_connectors['testing_pipeline'].load()

    # Always take last one
    response = testing_pipeline_artifacts[-1]

    assert response['totalScore'] is not None
    logger.info(f'Testing procedure was successfully passed for response time {response["datetime"]}')


def launch_test_demo_case():
    """
    Example of how to apply wiredflow for third-party service testing (generate token first)
    """
    flow_builder = FlowBuilder()

    # Repeat actions in pipeline every 1 minute - send GET request and store response
    flow_builder.add_pipeline('testing_pipeline', timedelta_seconds=60)\
        .with_http_connector(source=URL, headers={'accept': 'application/json', 'Authorization': TOKEN})\
        .with_storage('json', preprocessing='add_datetime', folder_to_save=Path('artifacts'))\
        .with_core_logic(check_output)

    # Configure service and launch it
    flow = flow_builder.build()
    flow.launch_flow()


if __name__ == '__main__':
    launch_test_demo_case()
