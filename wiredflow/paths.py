from pathlib import Path


def get_project_path() -> Path:
    return Path(__file__).parent.parent


def get_tmp_folder_path() -> Path:
    """ Return path to folder where different files can be stored """
    return Path(get_project_path(), 'wiredflow', 'files')


def get_test_folder_path() -> Path:
    """ Return path to folder where tests placed """
    return Path(get_project_path(), 'tests')


def get_mocks_payloads_path() -> Path:
    """ Return path with messages examples for mocks """
    return Path(get_project_path(), 'wiredflow', 'mocks')
