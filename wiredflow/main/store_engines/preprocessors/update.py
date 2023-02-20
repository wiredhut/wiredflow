from typing import Union


class UpdateMapper:
    """
    Class for data matching before saving into JSON 'database'.
    Combines the old records with the new ones so that the new ones
    only overwrite the data that matches the old labels
    """

    def __init__(self):
        self.name = 'update'

    @staticmethod
    def apply_during_update_save(info_to_write: dict, old_data: Union[dict, None]):
        """
        Apply logic during save stage. Match already saved data and new
        dictionary (if old data exists)
        """
        if old_data is None:
            return info_to_write

        info_to_write = {**old_data, **info_to_write}
        return info_to_write
