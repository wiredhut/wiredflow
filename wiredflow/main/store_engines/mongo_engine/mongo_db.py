from pymongo import MongoClient

from typing import Any

from loguru import logger

from wiredflow.main.actions.stages.storage_stage import StageStorageInterface
from wiredflow.main.store_engines.preprocessors.preprocessing import \
    Preprocessor


class MongoStorageStage(StageStorageInterface):
    """ Connector to MongoDB file """

    def __init__(self, stage_id: str, **params):
        super().__init__(stage_id, **params)
        self.stage_id = stage_id
        # Auth
        self.username = params.get('username')
        if self.username is None:
            self.username = 'user'
        self.password = params.get('password')
        if self.password is None:
            self.password = 'password'

        # Define database name
        self.database_name = params.get('database_name')
        if self.database_name is None:
            self.database_name = self.stage_id

        # Define collection name
        self.collection_name = params.get('collection_name')
        if self.collection_name is None:
            self.collection_name = 'wiredflow_connection'

        # Initialize MongoDB or connect to existing one
        self.source = params.get('source')
        if self.source is None:
            self.source = 'mongodb://localhost:27017'

        # Connect to desired database
        client = MongoClient(self.source, username=self.username, password=self.password)
        self.db = client[self.database_name]

        self.preprocessor = Preprocessor(params.get('preprocessing'))

    def save(self, relevant_info: Any, **kwargs):
        """ Add new document to collection """
        relevant_info = self.preprocessor.apply_during_save(relevant_info)

        # Insert new item to database
        collection = self.db[self.collection_name]
        if isinstance(relevant_info, dict):
            collection.insert_one(relevant_info)
        elif isinstance(relevant_info, list):
            collection.insert_many(relevant_info)

        logger.debug(f'MongoDB info. Successfully save data into database '
                     f'"{self.database_name}" collection "{self.collection_name}"')

    def load(self, **kwargs):
        list_of_collections = self.db.list_collection_names()
        if self.collection_name not in list_of_collections:
            # Current collection does not exist
            return None

        return self.db[self.collection_name].find()
