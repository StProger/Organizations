import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, Mapped, relationship


from domain.models.base import TimestampedDbModel


class Building(TimestampedDbModel):
    __tablename__ = "building"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(sa.String, nullable=False)
    latitude: Mapped[float] = mapped_column(sa.Float, nullable=False)
    longitude: Mapped[float] = mapped_column(sa.Float, nullable=False)

    # Связь с организациями
    organizations: Mapped[list] = relationship(
        back_populates="building", cascade="all, delete-orphan"
    )