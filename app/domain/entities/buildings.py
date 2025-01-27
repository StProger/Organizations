from dataclasses import dataclass
import uuid


@dataclass
class Buildings:

    pk: uuid.UUID
    address: str
    latitude: float
    longitude: float