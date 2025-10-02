from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.sql import func

from database import Base
from sqlalchemy.orm import Mapped, mapped_column

class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    data: Mapped[str] = mapped_column()
    user_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"{self.id} {self.title} {self.data} {self.user_id}"
