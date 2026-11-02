from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ReactivoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    formula: str | None = None
    cas: str | None = None
    lote: str
    cantidad: float = Field(ge=0)
    unidad: str = Field(description="g, mg, mL, L, ...")
    fecha_vencimiento: date
    ubicacion: str | None = None
    peligrosidad: str | None = Field(default=None, description="p. ej. corrosivo, inflamable")


class ReactivoCrear(ReactivoBase):
    pass


class ReactivoOut(ReactivoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class Consumo(BaseModel):
    cantidad: float = Field(gt=0)
