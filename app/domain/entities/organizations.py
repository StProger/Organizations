from dataclasses import dataclass
from typing import Any


@dataclass
class Organization:

    title: str
    phone_number: list[str]
    building: dict[str, Any]
    activities: list[str]

