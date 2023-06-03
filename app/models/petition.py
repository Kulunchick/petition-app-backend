from typing import List, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.vote import Vote
    from app.models.user import User


class Petition(TimestampMixin, Base):
    __tablename__ = "petitions"

    title: Mapped[str]
    description: Mapped[str]

    votes: Mapped[List["Vote"]] = relationship(back_populates="petition")

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="petitions")
