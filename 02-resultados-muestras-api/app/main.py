from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, engine, get_db
from .especificacion import evaluar

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de resultados de muestras",
    description="Registra resultados analíticos y detecta los que salen de especificación.",
)


def _muestra(db: Session, muestra_id: int) -> models.Muestra:
    muestra = db.get(models.Muestra, muestra_id)
    if muestra is None:
        raise HTTPException(404, "Muestra no encontrada")
    return muestra


@app.post("/muestras", response_model=schemas.MuestraOut, status_code=201)
def crear_muestra(datos: schemas.MuestraCrear, db: Session = Depends(get_db)):
    existe = db.scalar(select(models.Muestra).where(models.Muestra.codigo == datos.codigo))
    if existe:
        raise HTTPException(409, "Ya existe una muestra con ese código")
    muestra = models.Muestra(**datos.model_dump())
    db.add(muestra)
    db.commit()
    db.refresh(muestra)
    return muestra


@app.post(
    "/muestras/{muestra_id}/resultados",
    response_model=schemas.ResultadoOut,
    status_code=201,
)
def registrar_resultado(
    muestra_id: int, datos: schemas.ResultadoCrear, db: Session = Depends(get_db)
):
    _muestra(db, muestra_id)
    resultado = models.Resultado(
        muestra_id=muestra_id,
        conforme=evaluar(datos.valor, datos.limite_min, datos.limite_max),
        **datos.model_dump(),
    )
    db.add(resultado)
    db.commit()
    db.refresh(resultado)
    return resultado


@app.get("/muestras/{muestra_id}/resumen", response_model=schemas.ResumenMuestra)
def resumen(muestra_id: int, db: Session = Depends(get_db)):
    muestra = _muestra(db, muestra_id)
    total = len(muestra.resultados)
    fuera = sum(1 for r in muestra.resultados if not r.conforme)
    if total == 0:
        estado = "sin resultados"
    else:
        estado = "conforme" if fuera == 0 else "no conforme"
    return schemas.ResumenMuestra(
        codigo=muestra.codigo,
        total_parametros=total,
        conformes=total - fuera,
        fuera_de_especificacion=fuera,
        estado=estado,
    )


@app.get("/resultados/fuera-de-especificacion", response_model=list[schemas.ResultadoOut])
def fuera_de_especificacion(parametro: str | None = None, db: Session = Depends(get_db)):
    consulta = select(models.Resultado).where(models.Resultado.conforme.is_(False))
    if parametro:
        consulta = consulta.where(models.Resultado.parametro == parametro)
    return db.scalars(consulta).all()
