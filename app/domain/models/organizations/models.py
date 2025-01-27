from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql.array import ARRAY

from domain.models.base import TimestampedDbModel
from domain.models.activities.models import organization_activity


class Organization(TimestampedDbModel):
    __tablename__ = "organization"

    name: Mapped[str] = mapped_column(sa.String, nullable=False)

    phone_numbers: Mapped[List[str]] = mapped_column(ARRAY(sa.String), nullable=False)

    building_pk: Mapped[int] = mapped_column(sa.ForeignKey("building.pk"))
    building = relationship('Building', back_populates="organizations")

    activities = relationship(
        'Activity', secondary=organization_activity, back_populates="organizations"
    )