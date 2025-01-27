import uuid
from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from application.api.schemas import ErrorSchema
from application.api.v1.organizations.schemas import OrganizationResponseSchema, ListOrganizationResponseSchema
from domain.db_session import get_db
from domain.entities.organizations import Organization
from logic.exceptions.organizations import OrganizationNotFoundException
from logic.services.organizations import ORMOrganizationService, BaseOrganizationService


router = APIRouter(
    prefix='/organizations', tags=['Organizations']
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
    '/{organization_id}',
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