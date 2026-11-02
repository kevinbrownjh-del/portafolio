from datetime import date

from sqlalchemy import Date, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Reactivo(Base):
    __tablename__ = "reactivos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), index=True)
    formula: Mapped[str | None] = mapped_column(String(60), nullable=True)
    cas: Mapped[str | None] = mapped_column(String(20), nullable=True)
    lote: Mapped[str] = mapped_column(String(40))
    cantidad: Mapped[float] = mapped_column(Float)
    unidad: Mapped[str] = mapped_column(String(10))
    fecha_vencimiento: Mapped[date] = mapped_column(Date)
    ubicacion: Mapped[str | None] = mapped_column(String(60), nullable=True)
    peligrosidad: Mapped[str | None] = mapped_column(String(40), nullable=True)
