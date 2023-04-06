import json
from pathlib import Path
from typing import Union

import pytest

from wiredflow.main.store_engines.csv_engine.csv_db import CSVStorageStage
from wiredflow.main.store_engines.json_engine.json_db import JSONStorageStage
from wiredflow.paths import get_test_folder_path, remove_folder_with_files


@pytest.mark.parametrize("preprocessing, number_of_records",
                         [(None, 1), ('add_datetime', 2)])
def test_initialization_json_file(preprocessing: Union[str, None], number_of_records):
    """
    Check that local JSON storage initialized correctly.
    Perform testing with different preprocessors

    :param preprocessing: name of preprocessing to apply
    :param number_of_records: number of keys in each document
    """
    path_to_save_files = Path(get_test_folder_path(), 'json_storage_test')
    remove_folder_with_files(path_to_save_files)

    storage_stage = JSONStorageStage(stage_id='json_storage_test', use_threads=True,
                                     **{'folder_to_save': path_to_save_files, 'preprocessing': preprocessing})

    # Save single dictionary
    storage_stage.save({'First message': 'Some description of first message'})

    # Add several items at once
    storage_stage.save([{'Second message': 'Some description of second message'},
                        {'Third message': 'Some description of third message'}])

    # Check the content of JSON file
    created_file = Path(path_to_save_files, 'json_storage_test.json')
    assert created_file.is_file()

    loaded_file = storage_stage.load()

    assert loaded_file[0]['First message'] == 'Some description of first message'

    # Check number of keys
    for i in loaded_file:
        assert len(i.keys()) == number_of_records

    # Remove folder with files
    remove_folder_with_files(path_to_save_files)


@pytest.mark.parametrize("mapping, number_of_documents",
                         [('extend', 3),
                          ('update', 2),
                          ('overwrite', 1)])
def test_json_storage_with_mapping(mapping: str, number_of_documents: int):
    """ Check different mappings for JSON local storage """
    path_to_save_files = Path(get_test_folder_path(), 'json_storage_mapping_test')
    remove_folder_with_files(path_to_save_files)

    storage_stage = JSONStorageStage(stage_id='json_storage_test', use_threads=True,
                                     **{'folder_to_save': path_to_save_files, 'mapping': mapping})

    for item in [{'Item 1': 1}, {'Item 1': 11}, {'Item 2': 2}]:
        # Iteratively save data
        storage_stage.save(item)

    created_file = Path(path_to_save_files, 'json_storage_test.json')
    assert created_file.is_file()

    loaded_file = storage_stage.load()

    assert len(loaded_file) == number_of_documents
    remove_folder_with_files(path_to_save_files)


def test_initialization_csv_file():
    """ Test csv local storage initialization """
    path_to_save_files = Path(get_test_folder_path(), 'csv_storage_test')
    remove_folder_with_files(path_to_save_files)

    storage_stage = CSVStorageStage(stage_id='csv_storage_test',
                                    use_threads=True, **{'folder_to_save': path_to_save_files})

    # Save single dictionary
    storage_stage.save({'First message': 'Some description of first message', 'Message id': 0})

    # Add several items at once
    storage_stage.save([{'Second message': 'Some description of second message', 'Message id': 1},
                        {'Third message': 'Some description of third message', 'Message id': 2}])

    # Check the content of JSON file
    created_file = Path(path_to_save_files, 'csv_storage_test.csv')
    assert created_file.is_file()

    loaded_data = storage_stage.load()
    assert len(loaded_data) == 3
    assert loaded_data[0]['Message id'] == '0'

    # Remove folder with files
    remove_folder_with_files(path_to_save_files)
