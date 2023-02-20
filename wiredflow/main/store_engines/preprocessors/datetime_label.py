from typing import Dict
from datetime import datetime, timezone


class DatetimeEnrich:
    """ Add label with datetime into dictionary """

    def __init__(self):
        self.enrich_procedure_name = 'Datetime label adding'

    @staticmethod
    def apply_on_item(dict_to_update: Dict):
        dict_to_update['datetime_label'] = str(datetime.now(timezone.utc).astimezone())
        return dict_to_update
