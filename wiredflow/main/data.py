from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class CoreData:
    """ Class to store data aggregates for further processing """
    core_name: str = 'dummy'
