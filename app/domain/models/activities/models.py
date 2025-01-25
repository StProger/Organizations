import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.models.base import TimestampedDbModel


organization_activity = sa.Table(
    "organization_activity",
    TimestampedDbModel.metadata,
    sa.Column("organization_id", sa.ForeignKey("organization.id"), primary_key=True),
    sa.Column("activity_id", sa.ForeignKey("activity.id"), primary_key=True),
)


class Activity(TimestampedDbModel):
    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    parent_id: Mapped[int | None] = mapped_column(sa.ForeignKey("activity.id"), nullable=True)

    parent: Mapped["Activity | None"] = relationship(
        "Activity",
        remote_side="Activity.id",
        back_populates="children",
    )
    children: Mapped[list["Activity"]] = relationship(
        "Activity",
        back_populates="parent",
        cascade="all, delete-orphan",
    )

    organizations: Mapped[list] = relationship(
        secondary=organization_activity, back_populates="activities"
    )