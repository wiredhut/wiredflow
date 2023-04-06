import json
from pathlib import Path
from typing import Any, Optional, Union, List, Dict

from loguru import logger

from wiredflow.main.actions.stages.storage_stage import StageStorageInterface
from wiredflow.main.store_engines.preprocessors.mapping import DataMapper
from wiredflow.main.store_engines.preprocessors.preprocessing import Preprocessor
from wiredflow.main.synchronization import EventSynchronization
from wiredflow.paths import get_tmp_folder_path


class JSONStorageStage(StageStorageInterface):
    """ Connector to JSON file """

    def __init__(self, stage_id: str, use_threads: bool, **params):
        super().__init__(stage_id, use_threads, **params)
        self.stage_id = stage_id
        # Prepare local folder where there is a need to save json file
        if 'folder_to_save' in list(params.keys()):
            self.db_path: Path = params['folder_to_save']
        else:
            self.db_path: Path = get_tmp_folder_path()
        if self.db_path.is_dir() is False:
            self.db_path.mkdir(parents=True, exist_ok=True)
        self.db_path_file = Path(self.db_path, f'{self.stage_id}.json')

        self.preprocessor = Preprocessor(params.get('preprocessing'))
        self.mapper = DataMapper(params.get('mapping'), self.db_path_file)

        self.synchronizer = EventSynchronization(use_threads)
        self.synchronizer.initialize()

    def save(self, relevant_info: Any, **kwargs):
        self._access_to_file('write', info_to_write=relevant_info)
        logger.debug(f'JSON info. Storage {self.stage_id} successfully save data'
                     f' in {self.db_path_file}')

    def load(self, **kwargs):
        logger.debug(f'JSON info. Storage {self.stage_id} load data')
        return self._access_to_file('read', **kwargs)

    def _access_to_file(self, mode: str, info_to_write: Optional = None, **read_kwargs):
        """
        Read or write to file with Lock protection

        :param mode: name of mode (read or write)
        :param info_to_write: dictionary to store information
        :param read_kwargs: additional parameters to request data
        """
        # To avoid deadlock - synchronize thread during file storing or reading
        self.synchronizer.wait()

        loaded_files = None
        if mode == 'read':
            if self.db_path_file.is_file() is False:
                # There are no saved data yet - return None
                self.synchronizer.release()
                return None

            with open(self.db_path_file, 'r') as fp:
                loaded_files = json.load(fp)

            read_kwargs['data'] = loaded_files
            self.preprocessor.apply_during_load(**read_kwargs)
            self.mapper.apply_during_load(**read_kwargs)
        else:
            # Save obtained data into the file
            info_to_write = self.preprocessor.apply_during_save(info_to_write)
            info_to_write = self.mapper.apply_during_save(info_to_write)
            self._save_dict_into_file(info_to_write)

        self.synchronizer.release()
        return loaded_files

    def _save_dict_into_file(self, info_to_write: Union[List, Dict]):
        """ Save dictionary into json file """
        self.__remove_old_file()
        with open(self.db_path_file, 'w') as fp:
            json.dump(info_to_write, fp)

    def __remove_old_file(self):
        """ Remove old JSON file """
        if self.db_path_file.is_file():
            # File already exist - delete it and add new one
            self.db_path_file.unlink()
