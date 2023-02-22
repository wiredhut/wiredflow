import json
import csv
from pathlib import Path
from typing import Union, Dict, List


def read_csv_as_list_with_dict(db_path_file: Path) -> List[Dict]:
    """ Read csv file as list with dictionary or dictionaries """
    json_data = []
    with open(db_path_file, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        # Convert list structure into dictionary
        data = [row for row in csv_reader]
        headers = data[0]
        for batch_id in range(1, len(data)):
            data_batch = data[batch_id]
            dictionary_to_add = {}
            for column_id, header in enumerate(headers):
                dictionary_to_add.update({header: data_batch[column_id]})

            json_data.append(dictionary_to_add)

    return json_data


def update_json(db_path_file: Path, info_to_write: Union[Dict, List]):
    """ Update information using JSON file """

    with open(db_path_file, 'r') as fp:
        old_data = json.load(fp)

    if old_data is None:
        return info_to_write

    if isinstance(info_to_write, dict):
        info_to_write = {**old_data, **info_to_write}
    else:
        # Information in a form of list - map data iteratively
        for info_item in info_to_write:
            old_data = {**old_data, **info_item}
        info_to_write = old_data
    return info_to_write


def extend_json(db_path_file: Path, info_to_write: Union[Dict, List],
                current_db_exists: bool):
    """ Extend information in JSON file """

    if current_db_exists:
        with open(db_path_file, 'r') as fp:
            old_data = json.load(fp)

        if isinstance(info_to_write, dict):
            old_data.append(info_to_write)
        else:
            old_data.extend(info_to_write)
        info_to_write = old_data
    else:
        # File does not exist for now
        if isinstance(info_to_write, list) is False:
            info_to_write = [info_to_write]

    return info_to_write


def update_csv(db_path_file: Path, info_to_write: Union[Dict, List]):
    """ Update information using CSV file """
    old_data = read_csv_as_list_with_dict(db_path_file)

    if isinstance(info_to_write, dict):
        info_to_write = {**old_data, **info_to_write}
    else:
        # Information in a form of list - map data iteratively
        for info_item in info_to_write:
            old_data = {**old_data, **info_item}
        info_to_write = old_data
    return info_to_write


def extend_csv(db_path_file: Path, info_to_write: Union[Dict, List],
               current_db_exists: bool):
    """ Extend information in CSV file """
    if isinstance(info_to_write, list) is False:
        info_to_write = [info_to_write]

    if current_db_exists:
        old_data = read_csv_as_list_with_dict(db_path_file)

        # Add new data to old dictionary
        old_data.extend(info_to_write)
        info_to_write = old_data

    return info_to_write


class DataMapper:
    """
    Base class for mapping data before storing it into the data base.
    Implement logic of matching and updating. Applies after getting the data
    sample via HTTP request (for example) and before storing it into the database

    :param name: name of mapping strategy to apply
    :param db_path_file: path to file with data
    :param mapper_mode: name of local database (file) to use
    """
    update_by_mode = {'csv': update_csv,
                      'json': update_json}
    extend_by_mode = {'csv': extend_csv,
                      'json': extend_json}

    def __init__(self, name: Union[str, None], db_path_file: Path,
                 mapper_mode: str = 'json'):
        if name is None:
            # Default value is extend
            name = 'extend'
        self.name = name
        self.db_path_file = db_path_file
        self.mapper_mode = mapper_mode

    def apply_during_save(self, info_to_write: Union[Dict, List]):
        """ Apply all defined mappers to obtained data """
        current_db_exists = self.db_path_file.is_file()

        if self.name == 'update' and current_db_exists:
            info_to_write = self.update_by_mode[self.mapper_mode](self.db_path_file,
                                                                  info_to_write)
        elif self.name == 'extend':
            info_to_write = self.extend_by_mode[self.mapper_mode](self.db_path_file,
                                                                  info_to_write,
                                                                  current_db_exists)

        # If overwrite - just return new data without any mapping
        return info_to_write

    @staticmethod
    def apply_during_load(**kwargs):
        return kwargs
