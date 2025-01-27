from abc import ABC, abstractmethod
from typing import Iterable
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import and_, func

from geopy.distance import geodesic

from domain.entities.organizations import Organization as OrganizationEntity
from domain.entities.buildings import Buildings as BuildingsEntity
from domain.models.organizations.models import Organization
from domain.models.activities.models import Activity
from domain.models.buildings.models import Building
from logic.exceptions.organizations import OrganizationNotFoundException, OrganizationWithActivityNotFoundException, OrganizationWithBuildingNotFoundException, OrganizationWithNameNotFoundException


class BaseOrganizationService(ABC):

    @abstractmethod
    async def get_organization_list_by_building(self, db_session: AsyncSession, pk_building: uuid.UUID) -> Iterable[OrganizationEntity]:
        ...
    
    @abstractmethod
    async def get_organization_by_id(self, id: int, db_session: AsyncSession) -> OrganizationEntity:
        ...
    
    @abstractmethod
    async def get_organization_list(self, db_session: AsyncSession) -> Iterable[OrganizationEntity]:
        ...
    
    @abstractmethod
    async def get_organization_list_by_activity(self, db_session: AsyncSession, activity_name: str) -> Iterable[OrganizationEntity]:
        ...
    
    @abstractmethod
    async def get_organization_list_by_single_activity(self, db_session: AsyncSession, activity_name: str) -> Iterable[OrganizationEntity]:
        ...
    
    @abstractmethod
    async def get_organization_list_by_name(self, db_session: AsyncSession, name: str) -> Iterable[OrganizationEntity]:
        ...
    
    @abstractmethod
    async def get_organization_list_by_radius(
        self, 
        db_session: AsyncSession, 
        latitude: float, 
        longitude: float, 
        radius_km: float, 
    ) -> Iterable[OrganizationEntity]:
        ...

    @abstractmethod
    async def get_organization_list_by_area(
        self,
        db_session: AsyncSession, 
        min_latitude: float, 
        max_latitude: float, 
        min_longitude: float, 
        max_longitude: float
    ) -> Iterable[OrganizationEntity]:
        ...


class ORMOrganizationService(BaseOrganizationService):


    async def get_organization_list_by_area(
        self,
        db_session: AsyncSession, 
        min_latitude: float, 
        max_latitude: float, 
        min_longitude: float, 
        max_longitude: float
    ) -> Iterable[OrganizationEntity]:
        stmt = (
            select(Building)
            .filter(
                and_(
                    Building.latitude >= min_latitude,
                    Building.latitude <= max_latitude,
                    Building.longitude >= min_longitude,
                    Building.longitude <= max_longitude,    
                )
            )
        )
        building_list_orm: list[Building] = (await db_session.execute(stmt)).scalars().all()
        building_ids = [building.pk for building in building_list_orm]

        organization_list_stmt = (
            select(Organization)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities)
            )
            .filter(Organization.building_pk.in_(building_ids))
        )

        organization_list_orm: list[Organization] = (await db_session.execute(organization_list_stmt)).scalars().all()

        organization_list_entity = []
        for organization in organization_list_orm:
            
            building = {
                "pk": organization.building.pk,
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




    async def get_organization_list_by_radius(
        self, 
        db_session: AsyncSession, 
        latitude: float, 
        longitude: float, 
        radius_km: float, 
    ) -> Iterable[OrganizationEntity]:
        stmt = (select(Organization).options(selectinload(Organization.activities), selectinload(Organization.building)))
        organization_list_orm = (await db_session.execute(stmt)).scalars().all()
        center = (latitude, longitude)

        organization_list_entity = []
        for organization in organization_list_orm:
            building_location = (organization.building.latitude, organization.building.longitude)
            distance = geodesic(center, building_location).km
            if distance <= radius_km:
                building = {
                "pk": organization.building.pk,
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

    async def get_organization_list_by_building(self, db_session: AsyncSession, pk_building: uuid.UUID) -> Iterable[OrganizationEntity]:
        stmt = (
            select(Organization)
            .options(
                selectinload(Organization.activities), selectinload(Organization.building))
            .filter(Organization.building_pk == pk_building)
            )
        
        organization_list_orm: list[Organization] = (await db_session.execute(stmt)).scalars().all()
        if not organization_list_orm:
            raise OrganizationWithBuildingNotFoundException(pk_building=str(pk_building))
        organization_list_entity = []
        for organization in organization_list_orm:
            building = {
                "pk": organization.building.pk,
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
    
    async def get_organization_list_by_name(self, db_session: AsyncSession, name: str) -> Iterable[OrganizationEntity]:
        stmt = (
            select(Organization)
            .options(
                selectinload(Organization.building),  # Предварительная загрузка связанных зданий
                selectinload(Organization.activities),  # Предварительная загрузка активностей
            )
            .where(func.lower(Organization.name).contains(func.lower(name)))
        )
    
        # Выполнение запроса
        result = await db_session.execute(stmt)
        organization_list_orm = result.scalars().all()

        if not organization_list_orm:
            raise OrganizationWithNameNotFoundException(name=name)
        organization_list_entity = []
        for organization in organization_list_orm:
            building = {
                "pk": organization.building.pk,
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

    async def get_organization_list_by_single_activity(self, db_session: AsyncSession, activity_name: str) -> Iterable[OrganizationEntity]:
        activity_stmt = select(Activity).options(selectinload(Activity.children)).filter(Activity.name == activity_name)
        activity = (await db_session.execute(activity_stmt)).scalar_one_or_none()
        if not activity:
            raise OrganizationWithActivityNotFoundException(activity_name=activity_name)

        organization_list_stmt: list[Organization] = (
            select(Organization)
            .options(selectinload(Organization.building), selectinload(Organization.activities))
            .join(Organization.activities)
            .filter(Activity.pk == activity.pk))
        
        organization_list_orm: list[Organization] = (await db_session.execute(organization_list_stmt)).scalars().all()
        organization_list_entity = []

        for organization in organization_list_orm:
            building = {
                "pk": organization.building.pk,
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

    async def get_organization_by_id(self, pk: uuid.UUID, db_session: AsyncSession) -> OrganizationEntity:

        stmt = select(Organization).options(
            selectinload(Organization.building),
            selectinload(Organization.activities)
        ).filter(Organization.pk == pk)

        organization: Organization = (await db_session.execute(stmt)).scalar()
        if not organization:
            raise OrganizationNotFoundException(id=id)

        building = {
            "pk": organization.building.pk,
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
            selectinload(Organization.building),
            selectinload(Organization.activities)
        )
        
        organization_list_orm: list[Organization] = (await db_session.execute(stmt)).scalars().all()
        organization_list_entity = []

        for organization in organization_list_orm:
            building = {
                "pk": organization.building.pk,
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

    async def get_organization_list_by_activity(self, db_session: AsyncSession, activity_name: str) -> Iterable[OrganizationEntity]:
        
        root_activity_stmt = select(Activity).options(selectinload(Activity.children)).filter(Activity.name == activity_name)
        root_activity = (await db_session.execute(root_activity_stmt)).scalar_one_or_none()
        if not root_activity:
            raise OrganizationWithActivityNotFoundException(activity_name=activity_name)

        def get_all_sub_activities(activity: Activity):
            activities = [activity]
            for child in activity.children:
                activities.extend(get_all_sub_activities(child))
            return activities
        
        all_activities = get_all_sub_activities(activity=root_activity)

        activity_ids = [activity.pk for activity in all_activities]

        organization_list_stmt: list[Organization] = (
            select(Organization)
            .options(selectinload(Organization.building), selectinload(Organization.activities))
            .join(Organization.activities)
            .filter(Activity.pk.in_(activity_ids)))
        
        organization_list_orm: list[Organization] = (await db_session.execute(organization_list_stmt)).unique().scalars().all()
        organization_list_entity = []

        for organization in organization_list_orm:
            building = {
                "pk": organization.building.pk,
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
    
