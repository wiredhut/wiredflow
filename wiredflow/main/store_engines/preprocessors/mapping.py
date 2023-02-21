import json
from pathlib import Path
from typing import Union, Dict


class DataMapper:
    """
    Base class for mapping data before storing it into the data base.
    Implement logic of matching and updating. Applies after getting the data
    sample via HTTP request (for example) and before storing it into the database

    :param name: name of mapping strategy to apply
    :param db_path_file: path to file with data
    """
    def __init__(self, name: Union[str, None], db_path_file: Path):
        if name is None:
            # Default value is extend
            name = 'extend'
        self.name = name
        self.db_path_file = db_path_file

    def apply_during_save(self, info_to_write: Dict):
        """ Apply all defined mappers to obtained data """
        current_db_exists = self.db_path_file.is_file()

        if self.name == 'update' and current_db_exists:
            # Apply preprocessor with updating
            with open(self.db_path_file, 'r') as fp:
                old_data = json.load(fp)

            if old_data is None:
                return info_to_write
            info_to_write = {**old_data, **info_to_write}
        elif self.name == 'extend':
            # Extend JSON with new item
            if current_db_exists:
                with open(self.db_path_file, 'r') as fp:
                    old_data = json.load(fp)
                old_data.append(info_to_write)
                info_to_write = old_data
            else:
                info_to_write = [info_to_write]

        return info_to_write

    @staticmethod
    def apply_during_load(**kwargs):
        return kwargs
