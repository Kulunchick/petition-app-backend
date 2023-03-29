from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as P_UUID
from uuid import UUID, uuid4

from app.models.base import Base, TimestampMixin
from app.models.enums import Gender

if TYPE_CHECKING:
    from app.models.petition import Petition
    from app.models.vote import Vote


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(P_UUID(as_uuid=True), default=uuid4, primary_key=True)
    username: Mapped[str] = mapped_column(String(32))
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64))
    gender: Mapped[Gender]
    email: Mapped[str] = mapped_column(String(64))
    password: Mapped[str] = mapped_column(String(256))

    petitions: Mapped[List["Petition"]] = relationship(back_populates="user")
    votes: Mapped[List["Vote"]] = relationship(back_populates="user")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
