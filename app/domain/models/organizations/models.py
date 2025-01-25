import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql.array import ARRAY

from domain.models.activities.models import Activity
from domain.models.base import TimestampedDbModel
from domain.models.buildings.models import Building
from domain.models.activities.models import organization_activity


class Organization(TimestampedDbModel):
    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)

    phone_numbers: Mapped[list[str]] = mapped_column(ARRAY(sa.String), nullable=False)

    building_id: Mapped[int] = mapped_column(sa.ForeignKey("building.id"))
    building: Mapped["Building"] = relationship(back_populates="organizations")

    activities: Mapped[list["Activity"]] = relationship(
        secondary=organization_activity, back_populates="organizations"
    )