from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.models.base import TimestampedDbModel


organization_activity = sa.Table(
    "organization_activity",
    TimestampedDbModel.metadata,
    sa.Column("organization_pk", sa.ForeignKey("organization.pk"), primary_key=True),
    sa.Column("activity_pk", sa.ForeignKey("activity.pk"), primary_key=True),
    extend_existing=True,
)


class Activity(TimestampedDbModel):
    __tablename__ = "activity"
    
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    parent_pk: Mapped[int | None] = mapped_column(sa.ForeignKey("activity.pk"), nullable=True)

    parent = relationship(
        "Activity",
        remote_side="Activity.pk",
        back_populates="children",
    )
    children = relationship(
        "Activity",
        back_populates="parent",
        cascade="all, delete-orphan",
    )

    organizations = relationship(
        'Organization', secondary=organization_activity, back_populates="activities"
    )