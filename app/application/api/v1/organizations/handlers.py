import uuid
from fastapi import APIRouter, HTTPException, status, Depends, Query

from sqlalchemy.ext.asyncio import AsyncSession

from application.api.schemas import ErrorSchema
from application.api.v1.organizations.schemas import OrganizationResponseSchema, ListOrganizationResponseSchema
from domain.db_session import get_db
from domain.entities.buildings import Buildings
from domain.entities.organizations import Organization
from logic.exceptions.organizations import OrganizationNotFoundException, OrganizationWithActivityNotFoundException, OrganizationWithBuildingNotFoundException, OrganizationWithNameNotFoundException
from logic.services.organizations import ORMOrganizationService, BaseOrganizationService


router = APIRouter(
    prefix='/organizations', tags=['Organizations']
)


@router.get(
    '/by_area',
    description='Список зданий, находящихся в заданном радиусе относительно точки на карте.',
    response_model=ListOrganizationResponseSchema,
    responses={
        status.HTTP_200_OK: {'model': ListOrganizationResponseSchema},
    }
)
async def get_buildings_by_radius(
    min_latitude: float,
    max_latitude: float,
    min_longitude: float,
    max_longitude: float,
    db_session: AsyncSession = Depends(get_db)
):
    
    service: BaseOrganizationService = ORMOrganizationService()
    organization_list: list[Organization] = await service.get_organization_list_by_area(
        min_latitude=min_latitude,
        max_latitude=max_latitude,
        min_longitude=min_longitude,
        max_longitude=max_longitude,
        db_session=db_session
    )

    return [
        OrganizationResponseSchema.from_entity(entity=entity) for entity in organization_list
    ]


@router.get(
    '/by_radius',
    description='Список зданий, находящихся в заданном радиусе относительно точки на карте.',
    response_model=ListOrganizationResponseSchema,
    responses={
        status.HTTP_200_OK: {'model': ListOrganizationResponseSchema},
    }
)
async def get_buildings_by_radius(
    latitude: float,
    longitude: float,
    radius_km: float,
    db_session: AsyncSession = Depends(get_db)
):
    
    service: BaseOrganizationService = ORMOrganizationService()
    organization_list: list[Buildings] = await service.get_organization_list_by_radius(
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
        db_session=db_session
    )

    return [
        OrganizationResponseSchema.from_entity(entity=entity) for entity in organization_list
    ]

@router.get(
    '/buildings/{pk_building}',
    description='Получение организаций в конкретном здании.',
    response_model=ListOrganizationResponseSchema,
    responses={
        status.HTTP_200_OK: {'model': ListOrganizationResponseSchema},
        status.HTTP_404_NOT_FOUND: {'model': ErrorSchema}
    }
)
async def get_organization_list_by_building(pk_building: uuid.UUID, db_session: AsyncSession = Depends(get_db)):

    service: BaseOrganizationService = ORMOrganizationService()
    try:
        organization_list: list[Organization] = await service.get_organization_list_by_building(pk_building=pk_building, db_session=db_session)
        return [OrganizationResponseSchema.from_entity(entity=entity) for entity in organization_list]
    except OrganizationWithBuildingNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )


@router.get(
    '/name',
    description='Получение организаций по названию, будет возвращаться список организаций с вхождением строки, которую ввели.',
    response_model=ListOrganizationResponseSchema,
    responses={
        status.HTTP_200_OK: {'model': ListOrganizationResponseSchema},
        status.HTTP_404_NOT_FOUND: {'model': ErrorSchema}
    }
)
async def get_organization_list_by_name(name: str = Query(..., description='Название организации'), db_session: AsyncSession = Depends(get_db)):
    service: BaseOrganizationService = ORMOrganizationService()
    try:
        organization_list: list[Organization] = await service.get_organization_list_by_name(name=name, db_session=db_session)
        return [OrganizationResponseSchema.from_entity(entity=entity) for entity in organization_list]
    except OrganizationWithNameNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )


@router.get(
        '/single_activity',
        description='Получение организаций только по определённому виду деятельности, не включая вложенные.',
        response_model=ListOrganizationResponseSchema,
        responses={
            status.HTTP_200_OK: {'model': ListOrganizationResponseSchema},
            status.HTTP_404_NOT_FOUND: {'model': ErrorSchema}
        }
)
async def get_organization_by_activity(activity_name: str = Query(..., description="Название деятельности"), db_session: AsyncSession = Depends(get_db)):
    service: BaseOrganizationService = ORMOrganizationService()
    try:
        organization_list: list[Organization] = await service.get_organization_list_by_single_activity(activity_name=activity_name.capitalize(), db_session=db_session)
        return [OrganizationResponseSchema.from_entity(entity=entity) for entity in organization_list]
    except OrganizationWithActivityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )


@router.get(
    '/activity',
    description='Получение организаций по виду деятельности, включая вложенные деятельности.',
    response_model=ListOrganizationResponseSchema,
    responses={
        status.HTTP_200_OK: {'model': ListOrganizationResponseSchema},
        status.HTTP_404_NOT_FOUND: {'model': ErrorSchema}
    }
)
async def get_organization_by_activity(activity_name: str = Query(..., description="Название деятельности"), db_session: AsyncSession = Depends(get_db)):
    service: BaseOrganizationService = ORMOrganizationService()
    try:
        organization_list: list[Organization] = await service.get_organization_list_by_activity(activity_name=activity_name.capitalize(), db_session=db_session)
        return [OrganizationResponseSchema.from_entity(entity=entity) for entity in organization_list]
    except OrganizationWithActivityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )

@router.get(
    '/',
    response_model=ListOrganizationResponseSchema,
    description='Получение всех организаций.',
    responses={
        status.HTTP_200_OK: {'model': ListOrganizationResponseSchema}
    },
)
async def get_organization_list(db_session: AsyncSession = Depends(get_db)):

    service: BaseOrganizationService = ORMOrganizationService()
    organization_list: list[Organization] = await service.get_organization_list(db_session=db_session)
    return [OrganizationResponseSchema.from_entity(entity=entity) for entity in organization_list]
    

@router.get(
    '/{organization_pk}',
    response_model=OrganizationResponseSchema,
    description='Получение организации по идентификатору. В случае отсутствия организации возвращает 404 Not Found.',
    responses={
        status.HTTP_200_OK: {'model': OrganizationResponseSchema},
        status.HTTP_404_NOT_FOUND: {'model': ErrorSchema}
    }
)
async def get_organization(organization_pk: uuid.UUID, db_session: AsyncSession = Depends(get_db)):

    service: BaseOrganizationService = ORMOrganizationService()

    try:
        organization: Organization = await service.get_organization_by_id(pk=organization_pk, db_session=db_session)
        return OrganizationResponseSchema.from_entity(entity=organization)
    except OrganizationNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


