from dataclasses import dataclass
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Category:
    name: str
    priority: Priority
