from wiredflow.main.actions.stages.configuration_stage import ConfigurationInterface
from wiredflow.main.actions.stages.core_stage import CoreLogicInterface
from wiredflow.main.actions.stages.http_stage import StageCustomHTTPConnector
from wiredflow.main.actions.stages.send_stage import CustomSendStage
from wiredflow.main.build import FlowBuilder
from wiredflow.main.store_engines.сustom import CustomStorageStage


def mock_http_data(**params):
    return {'Mock data': 1234}


def custom_configuration_stage_checker(**params):
    """ Simulate custom stage function implementation for configuration """
    assert len(params.keys()) == 2
    assert params['custom_parameter'] == 'parameter'
    assert params['pipeline_name'] == 'test_pipeline'


def custom_http_connector_stage_checker(**params):
    """ Simulate custom stage function implementation for HTTP connection """
    assert len(params.keys()) == 2
    assert params['source'] == 'localhost'
    assert params['pipeline_name'] == 'test_pipeline'


def custom_storage_stage_checker(data_to_save, **params):
    """ Simulate custom stage for mqtt processing """
    assert len(params.keys()) == 2
    assert params['source'] == 'localhost'
    assert params['pipeline_name'] == 'test_pipeline'
    assert isinstance(data_to_save, dict)
    assert data_to_save['Mock data'] == 1234


def custom_core_logic_stage_checker(**params):
    assert len(params.keys()) == 4
    assert params['relevant_info'] is None
    assert params['pipeline_name'] == 'test_pipeline'
    assert len(params['db_connectors']) == 0


def custom_send_stage_checker(data_to_send, **params):
    assert isinstance(data_to_send, dict)
    assert data_to_send['Mock data'] == 1234
    assert params['message'] == 'custom_message'


def common_checking(**params):
    assert params['param_1'] == 'param_new'
    assert params['param_2'] == 'param_2'


def test_parameters_passed_correctly_into_configuration():
    """ Check that parameters was unified correctly for Configuration stage """
    flow_builder = FlowBuilder()
    flow_builder.add_pipeline('test_pipeline', timedelta_seconds=60, delay_seconds=1) \
        .with_configuration(configuration=custom_configuration_stage_checker, custom_parameter='parameter')

    flow = flow_builder.build()
    flow.launch_flow(execution_seconds=2)


def test_parameters_passed_correctly_into_http_connector():
    """ Check that parameters was unified correctly for HTTP connection stage """
    flow_builder = FlowBuilder()
    flow_builder.add_pipeline('test_pipeline', timedelta_seconds=60, delay_seconds=1) \
        .with_http_connector(configuration=custom_http_connector_stage_checker, source='localhost')

    flow = flow_builder.build()
    flow.launch_flow(execution_seconds=2)


def test_parameters_passed_correctly_into_storage():
    """ Check that parameters was unified correctly for Storage stage """

    flow_builder = FlowBuilder()
    flow_builder.add_pipeline('test_pipeline', timedelta_seconds=60, delay_seconds=1) \
        .with_http_connector(mock_http_data) \
        .with_storage(configuration=custom_storage_stage_checker, source='localhost')

    flow = flow_builder.build()
    flow.launch_flow(execution_seconds=2)


def test_parameters_passed_correctly_into_core():
    """ Check that parameters was unified correctly for Core logic stage """

    flow_builder = FlowBuilder()
    flow_builder.add_pipeline('test_pipeline', timedelta_seconds=60, delay_seconds=1) \
        .with_core_logic(configuration=custom_core_logic_stage_checker, mode='test')

    flow = flow_builder.build()
    flow.launch_flow(execution_seconds=2)


def test_parameters_passed_correctly_into_senders():
    """ Check that parameters was unified correctly for Send stage """
    flow_builder = FlowBuilder()
    flow_builder.add_pipeline('test_pipeline', timedelta_seconds=60, delay_seconds=1) \
        .with_http_connector(mock_http_data) \
        .send(configuration=custom_send_stage_checker, message='custom_message')

    flow = flow_builder.build()
    flow.launch_flow(execution_seconds=2)


def test_parameters_into_configuration_stage():
    """ Check that parameters correctly define on a Stages level for configuration """

    config = ConfigurationInterface(function_to_launch=common_checking,
                                    use_threads=True, **{'param_1': 'param_1'})
    config.launch(**{'param_1': 'param_new', 'param_2': 'param_2'})


def test_parameters_into_http_connector_stage():
    """ Check that parameters correctly define on a Stages level for HTTP connection """

    connector = StageCustomHTTPConnector(function_to_launch=common_checking,
                                         use_threads=True, **{'param_1': 'param_1'})
    connector.get(**{'param_1': 'param_new', 'param_2': 'param_2'})


def test_parameters_into_storage():
    """ Check that parameters correctly define on a Stages level for storage """

    def storage_checking(relevant_info, **params):
        assert params['param_1'] == 'param_new'
        assert params['param_2'] == 'param_2'

    storage = CustomStorageStage(function_to_launch=storage_checking, stage_id='test',
                                 use_threads=True, **{'param_1': 'param_1'})
    storage.save(relevant_info=None, **{'param_1': 'param_new', 'param_2': 'param_2'})


def test_parameters_into_core_logic():
    """ Check that parameters correctly define on a Stages level for core logic """

    def core_checking(relevant_info, db_connectors, **params):
        assert params['param_1'] == 'param_new'
        assert params['param_2'] == 'param_2'

    core = CoreLogicInterface(function_to_launch=core_checking, stage_id='test',
                              use_threads=True, **{'param_1': 'param_1'})
    core.launch(relevant_info=None, db_connectors={}, **{'param_1': 'param_new', 'param_2': 'param_2'})


def test_parameters_into_send():
    """ Check that parameters correctly define on a Stages level for send """
    def send_checking(data_to_send, **params):
        assert params['param_1'] == 'param_new'
        assert params['param_2'] == 'param_2'

    send = CustomSendStage(function_to_launch=send_checking, stage_id='test',
                           use_threads=True, **{'param_1': 'param_1'})
    send.send(data_to_send={'data': 'some info'}, **{'param_1': 'param_new', 'param_2': 'param_2'})
