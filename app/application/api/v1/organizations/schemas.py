from typing import Any
import uuid
from pydantic import BaseModel

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
