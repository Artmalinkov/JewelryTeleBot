from sqlalchemy import String, Integer, Text, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(255), nullable=True)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True
    )

    photo: Mapped[str] = mapped_column(
        String(255),
        nullable=True  # сюда кладём Telegram file_id
    )

    weight: Mapped[float | None] = mapped_column(Numeric(6, 2))
    size: Mapped[str | None] = mapped_column(String(50))
    inserts: Mapped[str | None] = mapped_column(String(255))
    metal: Mapped[str | None] = mapped_column(String(100))

    # Уникальный идентификатор изделия
    uin: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=True
    )
