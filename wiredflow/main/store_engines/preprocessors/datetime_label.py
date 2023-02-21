from typing import Dict, List, Union
from datetime import datetime, timezone


class DatetimeEnrich:
    """ Add label with datetime into dictionary """

    def __init__(self):
        self.enrich_procedure_name = 'Datetime label adding'

    @staticmethod
    def apply_on_item(item_to_update: Union[Dict, List]):
        """ Add datetime label in each item """

        datetime_label = str(datetime.now(timezone.utc).astimezone())
        if isinstance(item_to_update, dict):
            item_to_update['datetime_label'] = datetime_label
        elif isinstance(item_to_update, list):
            for dictionary in item_to_update:
                dictionary['datetime_label'] = datetime_label

        return item_to_update
