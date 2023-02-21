import json
from pathlib import Path
from typing import Union, List, Dict

from wiredflow.main.store_engines.preprocessors.datetime_label import \
    DatetimeEnrich


class Preprocessor:
    """
    Base class for processing data before storing it into the data base.
    Implement logic of adding additional data or transform data into desired form
    """
    preprocessor_by_name = {'add_datetime': DatetimeEnrich}

    def __init__(self, name: Union[str, None, List[str]], db_path_file: Path):
        if name is not None and isinstance(name, list) is False:
            # Wrap in list
            name = [name]

        self.preprocessors_to_apply = name
        self.db_path_file = db_path_file

    def apply_during_save(self, info_to_write: Dict):
        """ Apply all defined preprocessors to obtained data """
        if self.preprocessors_to_apply is None:
            # There is no need to apply any preprocessing
            return info_to_write

        for preprocessor_to_apply in self.preprocessors_to_apply:
            if preprocessor_to_apply is not None:
                mapper = self.preprocessor_by_name[preprocessor_to_apply]()
                info_to_write = mapper.apply_on_item(info_to_write)

        return info_to_write

    @staticmethod
    def apply_during_load(**kwargs):
        return kwargs
