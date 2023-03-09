from pathlib import Path
from typing import Union, Callable, Any

import pytest

from wiredflow.main.actions.assimilation.http_staging import HTTPStageProxy
from wiredflow.main.actions.assimilation.send_staging import SendStageProxy
from wiredflow.main.actions.assimilation.store_staging import StoreStageProxy
from wiredflow.main.actions.stages.http_stage import StageGetHTTPConnector, StagePostHTTPConnector, \
    StageCustomHTTPConnector
from wiredflow.main.actions.stages.send_stage import HTTPPUTSendStage, HTTPPOSTSendStage, MQTTSendStage, CustomSendStage
from wiredflow.main.store_engines.csv_engine.csv_db import CSVStorageStage
from wiredflow.main.store_engines.json_engine.json_db import JSONStorageStage
from wiredflow.main.store_engines.mongo_engine.mongo_db import MongoStorageStage
from wiredflow.main.store_engines.сustom import CustomStorageStage


def custom_common_implementation():
    return None


@pytest.mark.parametrize("storage_config, params, expected_stage",
                         [('json', {'folder_to_save': Path('./data')}, JSONStorageStage),
                          ('csv', {'folder_to_save':  Path('./data')}, CSVStorageStage),
                          ('mongo', {'source': 'mongodb://localhost'}, MongoStorageStage),
                          (custom_common_implementation, {'custom': 'value'}, CustomStorageStage)])
def test_storage_stage_proxy(storage_config: Union[str, Callable], params: dict, expected_stage: Any):
    """ Check that proxy configure correct Storage stage object based on desired parameters """
    proxy_stage = StoreStageProxy(storage_config, stage_id='test', **params)
    compiled_stage = proxy_stage.compile()

    assert isinstance(compiled_stage, expected_stage)
    if isinstance(storage_config, str) and storage_config in ['json', 'csv']:
        assert compiled_stage.db_path == params['folder_to_save']
    elif isinstance(storage_config, str) and storage_config == 'mongo':
        assert compiled_stage.source == params['source']
    elif isinstance(compiled_stage, CustomStorageStage):
        assert compiled_stage.params == params


@pytest.mark.parametrize("connector_config, params, expected_stage",
                         [('get', {'payload': 'select * from table limit 1'}, StageGetHTTPConnector),
                          ('post', {'payload': 'select * from table limit 1'}, StagePostHTTPConnector),
                          (custom_common_implementation, {'custom': 'value'}, StageCustomHTTPConnector)])
def test_http_connection_stage_proxy(connector_config: Union[str, Callable], params: dict, expected_stage: Any):
    """ Check that proxy configure correct HTTP connector stage based on desired parameters """
    proxy_stage = HTTPStageProxy(connector_config, source='test', headers={'accept': 'application/json',
                                                                           'apikey': '1234'}, **params)
    compiled_stage = proxy_stage.compile()

    assert isinstance(compiled_stage, expected_stage)
    if isinstance(connector_config, str) and connector_config in ['get', 'post']:
        assert compiled_stage.source == 'test'
        assert compiled_stage.params['payload'] == params['payload']
    else:
        assert compiled_stage.params['custom'] == params['custom']


@pytest.mark.parametrize("send_config, params, expected_stage",
                         [('mqtt', {'topic': 'test', 'port': 1883, 'label_to_send': 'mqtt'}, MQTTSendStage),
                          ('http_put', {'label_to_send':  'put'}, HTTPPUTSendStage),
                          ('http_post', {'label_to_send': 'post'}, HTTPPOSTSendStage),
                          (custom_common_implementation, {'custom': 'value'}, CustomSendStage)])
def test_send_stage_proxy(send_config: Union[str, Callable], params: dict, expected_stage: Any):
    """ Check that proxy configure correct Send stage based on desired parameters """
    proxy_stage = SendStageProxy(send_config, destination='test', **params)
    compiled_stage = proxy_stage.compile()

    assert isinstance(compiled_stage, expected_stage)
    if isinstance(compiled_stage, CustomSendStage):
        assert compiled_stage.kwargs['destination'] == 'test'
        assert compiled_stage.kwargs['custom'] == params['custom']
        assert proxy_stage.custom_realization is True

    else:
        assert compiled_stage.label_to_send == params['label_to_send']
