from dataclasses import dataclass
from typing import Any
import uuid


@dataclass
class Organization:

    pk: uuid.UUID
    title: str
    phone_number_list: list[str]
    building: dict[str, Any]
    activities: list[str]

