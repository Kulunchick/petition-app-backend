from typing import List, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as P_UUID

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from vote import Vote
    from user import User


class Petition(TimestampMixin, Base):
    __tablename__ = "petitions"

    id: Mapped[UUID] = mapped_column(P_UUID(as_uuid=True), default=uuid4, primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(2048))

    votes: Mapped[List["Vote"]] = relationship(back_populates="petition")

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="petitions")
