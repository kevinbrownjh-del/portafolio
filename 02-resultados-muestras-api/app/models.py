from datetime import date

from sqlalchemy import Boolean, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Muestra(Base):
    __tablename__ = "muestras"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    matriz: Mapped[str] = mapped_column(String(60))
    punto_muestreo: Mapped[str | None] = mapped_column(String(80), nullable=True)
    fecha_toma: Mapped[date] = mapped_column(Date)
    resultados: Mapped[list["Resultado"]] = relationship(
        back_populates="muestra", cascade="all, delete-orphan"
    )


class Resultado(Base):
    __tablename__ = "resultados"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    muestra_id: Mapped[int] = mapped_column(ForeignKey("muestras.id"))
    parametro: Mapped[str] = mapped_column(String(60), index=True)
    valor: Mapped[float] = mapped_column(Float)
    unidad: Mapped[str] = mapped_column(String(20))
    limite_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    limite_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    conforme: Mapped[bool] = mapped_column(Boolean)
    muestra: Mapped[Muestra] = relationship(back_populates="resultados")
