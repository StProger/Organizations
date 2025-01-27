"""empty message

Revision ID: 1d5055053459
Revises: 
Create Date: 2025-01-27 16:53:03.671725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.dialects import postgresql

from domain.models.activities.models import Activity
from domain.models.buildings.models import Building
from domain.models.organizations.models import Organization

# revision identifiers, used by Alembic.
revision: str = '1d5055053459'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activity',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('parent_pk', sa.UUID(), nullable=True),
    sa.Column('pk', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['parent_pk'], ['activity.pk'], ),
    sa.PrimaryKeyConstraint('pk')
    )
    op.create_index(op.f('ix_activity_created_at'), 'activity', ['created_at'], unique=False)
    op.create_table('building',
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('pk', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('pk')
    )
    op.create_index(op.f('ix_building_created_at'), 'building', ['created_at'], unique=False)
    op.create_table('organization',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('phone_numbers', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('building_pk', sa.UUID(), nullable=False),
    sa.Column('pk', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['building_pk'], ['building.pk'], ),
    sa.PrimaryKeyConstraint('pk')
    )
    op.create_index(op.f('ix_organization_created_at'), 'organization', ['created_at'], unique=False)
    op.create_table('organization_activity',
    sa.Column('pk', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('organization_pk', sa.UUID(), nullable=False),
    sa.Column('activity_pk', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['activity_pk'], ['activity.pk'], ),
    sa.ForeignKeyConstraint(['organization_pk'], ['organization.pk'], ),
    sa.PrimaryKeyConstraint('pk')
    )
    # ### end Alembic commands ###

    bind = op.get_bind()
    session = Session(bind=bind)
    building1 = Building(address="Ул. Ленина 45", latitude=40.7128, longitude=-74.0060)
    building2 = Building(address="Ул. Горького 100", latitude=34.0522, longitude=-118.2437)

    session.add(building1)
    session.add(building2)
    session.commit()

    activity1 = Activity(name="Еда")
    activity2 = Activity(name="Автомобили")
    activity3 = Activity(name="Мясная продукция", parent_pk=activity1.pk)
    
    session.add(activity1)
    session.add(activity2)
    session.add(activity3)

    session.commit()
    organization1 = Organization(
        name="Сбербанк",
        phone_numbers=["+1-800-555-1234", "+1-800-555-5678"],
        building_pk=building1.pk
    )
    organization2 = Organization(
        name="Яндекс",
        phone_numbers=["+1-800-555-9876", "+1-800-555-5432"],
        building_pk=building2.pk
    )

    session.add(organization1)
    session.add(organization2)

    session.commit()
    organization1.activities.append(activity1)
    organization2.activities.append(activity2)
    organization2.activities.append(activity3)

    session.commit()

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('organization_activity')
    op.drop_index(op.f('ix_organization_created_at'), table_name='organization')
    op.drop_table('organization')
    op.drop_index(op.f('ix_building_created_at'), table_name='building')
    op.drop_table('building')
    op.drop_index(op.f('ix_activity_created_at'), table_name='activity')
    op.drop_table('activity')
    # ### end Alembic commands ###
