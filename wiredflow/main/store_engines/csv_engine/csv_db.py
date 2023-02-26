import csv

from pathlib import Path
from typing import Any, Optional, Union, List, Dict

from loguru import logger
from threading import Event

from wiredflow.main.actions.stages.storage_stage import StageStorageInterface
from wiredflow.main.store_engines.preprocessors.mapping import DataMapper, \
    read_csv_as_list_with_dict
from wiredflow.main.store_engines.preprocessors.preprocessing import \
    Preprocessor
from wiredflow.paths import get_tmp_folder_path


class CSVStorageStage(StageStorageInterface):
    """ Connector to CSV file """

    def __init__(self, stage_id: str, **params):
        super().__init__(stage_id, **params)
        self.stage_id = stage_id
        # Prepare local folder where there is a need to save json file
        if 'folder_to_save' in list(params.keys()):
            self.db_path: Path = params['folder_to_save']
        else:
            self.db_path: Path = get_tmp_folder_path()
        if self.db_path.is_dir() is False:
            self.db_path.mkdir(parents=True, exist_ok=True)
        self.db_path_file = Path(self.db_path, f'{self.stage_id}.csv')

        self.preprocessor = Preprocessor(params.get('preprocessing'))
        self.mapper = DataMapper(params.get('mapping'), self.db_path_file,
                                 mapper_mode='csv')

        self.event = Event()
        self.event.set()

    def save(self, relevant_info: Any, **kwargs):
        self._access_to_file('write', info_to_write=relevant_info)
        logger.debug(f'CSV info. Storage {self.stage_id} successfully save data'
                     f' in {self.db_path_file}')

    def load(self, **kwargs):
        logger.debug(f'CSV info. Storage {self.stage_id} load data')
        return self._access_to_file('read', **kwargs)

    def _access_to_file(self, mode: str, info_to_write: Optional = None, **read_kwargs):
        """
        Read or write to file with Lock protection

        :param mode: name of mode (read or write)
        :param info_to_write: dictionary to store information
        :param read_kwargs: additional parameters to request data
        """
        # To avoid deadlock - synchronize thread during file storing or reading
        self.event.wait()
        self.event.clear()

        loaded_files = None
        if mode == 'read':
            if self.db_path_file.is_file() is False:
                # There are no saved data yet - return None
                self.event.set()
                return None

            # Read file in a form of dictionary
            loaded_files = read_csv_as_list_with_dict(self.db_path_file)

            read_kwargs['data'] = loaded_files
            self.preprocessor.apply_during_load(**read_kwargs)
            self.mapper.apply_during_load(**read_kwargs)
        else:
            # Save obtained data into the file
            info_to_write = self.preprocessor.apply_during_save(info_to_write)
            info_to_write = self.mapper.apply_during_save(info_to_write)
            self._save_dict_into_file(info_to_write)

        self.event.set()
        return loaded_files

    def _save_dict_into_file(self, info_to_write: Union[List, Dict]):
        """ Save dictionary into json file """
        self.__remove_old_file()

        # Prepare data for storage
        if isinstance(info_to_write, dict):
            header = list(info_to_write.keys())
            data = [list(info_to_write.values())]
        else:
            header = list(info_to_write[0].keys())
            data = []
            for dictionary in info_to_write:
                data.append(list(dictionary.values()))

        with open(self.db_path_file, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header and data
            writer.writerow(header)
            writer.writerows(data)

    def __remove_old_file(self):
        """ Remove old JSON file """
        if self.db_path_file.is_file():
            # File already exist - delete it and add new one
            self.db_path_file.unlink()
