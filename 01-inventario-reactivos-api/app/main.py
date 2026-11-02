from datetime import date, timedelta

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de inventario de reactivos",
    description="Control de stock y vencimientos de reactivos de laboratorio.",
)


def _obtener(db: Session, reactivo_id: int) -> models.Reactivo:
    reactivo = db.get(models.Reactivo, reactivo_id)
    if reactivo is None:
        raise HTTPException(404, "Reactivo no encontrado")
    return reactivo


@app.post("/reactivos", response_model=schemas.ReactivoOut, status_code=201)
def crear(datos: schemas.ReactivoCrear, db: Session = Depends(get_db)):
    reactivo = models.Reactivo(**datos.model_dump())
    db.add(reactivo)
    db.commit()
    db.refresh(reactivo)
    return reactivo


@app.get("/reactivos", response_model=list[schemas.ReactivoOut])
def listar(nombre: str | None = None, db: Session = Depends(get_db)):
    consulta = select(models.Reactivo).order_by(models.Reactivo.nombre)
    if nombre:
        consulta = consulta.where(models.Reactivo.nombre.ilike(f"%{nombre}%"))
    return db.scalars(consulta).all()


@app.get("/reactivos/por-vencer", response_model=list[schemas.ReactivoOut])
def por_vencer(dias: int = 30, db: Session = Depends(get_db)):
    """Reactivos vencidos o que vencen dentro de `dias` días."""
    limite = date.today() + timedelta(days=dias)
    consulta = (
        select(models.Reactivo)
        .where(models.Reactivo.fecha_vencimiento <= limite)
        .order_by(models.Reactivo.fecha_vencimiento)
    )
    return db.scalars(consulta).all()


@app.get("/reactivos/stock-bajo", response_model=list[schemas.ReactivoOut])
def stock_bajo(minimo: float = 10, db: Session = Depends(get_db)):
    consulta = select(models.Reactivo).where(models.Reactivo.cantidad < minimo)
    return db.scalars(consulta).all()


@app.get("/reactivos/{reactivo_id}", response_model=schemas.ReactivoOut)
def detalle(reactivo_id: int, db: Session = Depends(get_db)):
    return _obtener(db, reactivo_id)


@app.post("/reactivos/{reactivo_id}/consumo", response_model=schemas.ReactivoOut)
def registrar_consumo(
    reactivo_id: int, consumo: schemas.Consumo, db: Session = Depends(get_db)
):
    reactivo = _obtener(db, reactivo_id)
    if consumo.cantidad > reactivo.cantidad:
        raise HTTPException(409, "Stock insuficiente")
    reactivo.cantidad -= consumo.cantidad
    db.commit()
    db.refresh(reactivo)
    return reactivo


@app.delete("/reactivos/{reactivo_id}", status_code=204)
def eliminar(reactivo_id: int, db: Session = Depends(get_db)):
    db.delete(_obtener(db, reactivo_id))
    db.commit()
