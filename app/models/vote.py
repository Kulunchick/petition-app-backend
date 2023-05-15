from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint

from app.models.base import Base, TimestampMixin

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as P_UUID

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.petition import Petition


class Vote(TimestampMixin, Base):
    __tablename__ = "votes"

    id: Mapped[UUID] = mapped_column(P_UUID(as_uuid=True), default=uuid4, primary_key=True)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="votes")

    petition_id: Mapped[UUID] = mapped_column(ForeignKey("petitions.id", ondelete="CASCADE"))
    petition: Mapped["Petition"] = relationship(back_populates="votes")

    __table_args__ = (
        UniqueConstraint('user_id', 'petition_id'),
    )
