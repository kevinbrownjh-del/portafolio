from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .especificacion import validar_limites


class MuestraCrear(BaseModel):
    codigo: str = Field(min_length=1, max_length=40)
    matriz: str = Field(description="agua residual, agua potable, suelo, ...")
    punto_muestreo: str | None = None
    fecha_toma: date


class MuestraOut(MuestraCrear):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ResultadoCrear(BaseModel):
    parametro: str = Field(min_length=1)
    valor: float
    unidad: str
    limite_min: float | None = None
    limite_max: float | None = None

    @model_validator(mode="after")
    def _limites_coherentes(self):
        validar_limites(self.limite_min, self.limite_max)
        return self


class ResultadoOut(ResultadoCrear):
    model_config = ConfigDict(from_attributes=True)
    id: int
    muestra_id: int
    conforme: bool


class ResumenMuestra(BaseModel):
    codigo: str
    total_parametros: int
    conformes: int
    fuera_de_especificacion: int
    estado: str
