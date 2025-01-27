from typing import Any
import uuid
from pydantic import BaseModel

from domain.entities.buildings import Buildings
from domain.entities.organizations import Organization


class OrganizationResponseSchema(BaseModel):

    pk: uuid.UUID
    title: str
    phone_number_list: list[str]
    building: dict[str, Any]
    activities: list[str]

    @classmethod
    def from_entity(cls, entity: Organization) -> "OrganizationResponseSchema":
        return OrganizationResponseSchema(
            pk=entity.pk,
            title=entity.title,
            phone_number_list=entity.phone_number_list,
            building=entity.building,
            activities=entity.activities
        )

ListOrganizationResponseSchema = list[OrganizationResponseSchema]


class BuildingResponseSchema(BaseModel):

    pk: uuid.UUID
    address: str
    latitude: float
    longitude: float

    @classmethod
    def from_entity(cls, entity: Buildings) -> "BuildingResponseSchema":
        return BuildingResponseSchema(
            pk=entity.pk,
            address=entity.address,
            latitude=entity.latitude,
            longitude=entity.longitude
        )

ListBuildingReponseSchema = list[BuildingResponseSchema]
