from abc import ABC, abstractmethod
from typing import Iterable
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from domain.entities.organizations import Organization as OrganizationEntity
from domain.models.organizations.models import Organization
from logic.exceptions.organizations import OrganizationNotFoundException


class BaseOrganizationService(ABC):

    # @abstractmethod
    # def get_organization_list_by_building(self, db_session: AsyncSession) -> Iterable[OrganizationEntity]:
    #     ...
    
    @abstractmethod
    async def get_organization_by_id(self, id: int, db_session: AsyncSession) -> OrganizationEntity:
        ...
    
    @abstractmethod
    async def get_organization_list(self, db_session: AsyncSession) -> Iterable[OrganizationEntity]:
        ...


class ORMOrganizationService(BaseOrganizationService):

    # def get_organization_list_by_building(self, db_session: AsyncSession) -> Iterable[OrganizationEntity]:
    #     ...
    
    async def get_organization_by_id(self, pk: uuid.UUID, db_session: AsyncSession) -> OrganizationEntity:

        stmt = select(Organization).options(
            joinedload(Organization.building),
            joinedload(Organization.activities)
        ).filter(Organization.pk == pk)

        organization: Organization = (await db_session.execute(stmt)).scalar()
        if not organization:
            raise OrganizationNotFoundException(id=id)

        building = {
            "address": organization.building.address,
            "latitude": organization.building.latitude,
            "longitude": organization.building.longitude,
        }

        return OrganizationEntity(
            pk=organization.pk,
            title=organization.name,
            phone_number_list=organization.phone_numbers,
            building=building,
            activities=[activity.name for activity in organization.activities],
        )

    async def get_organization_list(self, db_session: AsyncSession) -> Iterable[OrganizationEntity]:

        stmt = select(Organization).options(
            joinedload(Organization.building),
            joinedload(Organization.activities)
        )
        
        organization_list_orm: list[Organization] = (await db_session.execute(stmt)).unique().scalars().all()
        organization_list_entity = []

        for organization in organization_list_orm:
            building = {
                "address": organization.building.address,
                "latitude": organization.building.latitude,
                "longitude": organization.building.longitude,
            }
            organization_list_entity.append(
                OrganizationEntity(
                    pk=organization.pk,
                    title=organization.name,
                    phone_number_list=organization.phone_numbers,
                    building=building,
                    activities=[activity.name for activity in organization.activities],
                )
            )
        return organization_list_entity