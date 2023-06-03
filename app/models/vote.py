from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.petition import Petition


class Vote(TimestampMixin, Base):
    __tablename__ = "votes"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="votes")

    petition_id: Mapped[UUID] = mapped_column(ForeignKey("petitions.id", ondelete="CASCADE"))
    petition: Mapped["Petition"] = relationship(back_populates="votes")

    __table_args__ = (
        UniqueConstraint('user_id', 'petition_id'),
    )
