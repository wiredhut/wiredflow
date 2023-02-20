import json
from pathlib import Path
from typing import Union, List, Dict

from wiredflow.main.store_engines.preprocessors.datetime_label import \
    DatetimeEnrich


class Preprocessor:
    """
    Base class for processing data before storing it into the data base.
    Implement logic of matching and updating. Applies after getting the data
    sample via HTTP request (for example)
    """
    preprocessor_by_name = {'add_datetime': DatetimeEnrich}

    def __init__(self, name: Union[str, None, List[str]], db_path_file: Path):
        self.preprocessors_on_items = ['add_datetime']

        if name is None:
            # Default strategy is extending file with new batches
            name = 'extend'
        if isinstance(name, list) is False:
            # Wrap in list
            name = [name]

        self.preprocessors_to_apply = name
        self.db_path_file = db_path_file

    def apply_during_save(self, info_to_write: Dict):
        """ Apply all defined preprocessors to obtained data """
        for mapper_name in self.preprocessors_to_apply:
            if mapper_name in self.preprocessors_on_items:
                mapper = self.preprocessor_by_name[mapper_name]()
                info_to_write = mapper.apply_on_item(info_to_write)

        # Apply others preprocessors / mappers
        name = self.get_preprocessor_name_to_apply()
        current_db_exists = self.db_path_file.is_file()

        if name == 'update' and current_db_exists:
            # Apply preprocessor with updating
            with open(self.db_path_file, 'r') as fp:
                old_data = json.load(fp)

            if old_data is None:
                return info_to_write
            info_to_write = {**old_data, **info_to_write}
        elif name == 'extend':
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

    def get_preprocessor_name_to_apply(self):
        for name in self.preprocessors_to_apply:
            if name not in self.preprocessors_on_items:
                return name

        # Default value is 'extend'
        return 'extend'
