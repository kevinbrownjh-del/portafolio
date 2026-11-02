import os
from datetime import date, timedelta

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

client = TestClient(app)


def reactivo(**extra):
    base = {
        "nombre": "Ácido clorhídrico",
        "formula": "HCl",
        "cas": "7647-01-0",
        "lote": "L-001",
        "cantidad": 500,
        "unidad": "mL",
        "fecha_vencimiento": str(date.today() + timedelta(days=365)),
        "peligrosidad": "corrosivo",
    }
    return {**base, **extra}


def test_crear_y_obtener():
    r = client.post("/reactivos", json=reactivo())
    assert r.status_code == 201
    rid = r.json()["id"]
    assert client.get(f"/reactivos/{rid}").json()["formula"] == "HCl"


def test_consumo_descuenta_stock_y_rechaza_exceso():
    rid = client.post("/reactivos", json=reactivo(nombre="NaOH", cantidad=100)).json()["id"]
    assert client.post(f"/reactivos/{rid}/consumo", json={"cantidad": 40}).json()["cantidad"] == 60
    assert client.post(f"/reactivos/{rid}/consumo", json={"cantidad": 1000}).status_code == 409


def test_por_vencer_incluye_vencidos():
    ayer = str(date.today() - timedelta(days=1))
    client.post("/reactivos", json=reactivo(nombre="Vencido", fecha_vencimiento=ayer))
    nombres = [x["nombre"] for x in client.get("/reactivos/por-vencer?dias=7").json()]
    assert "Vencido" in nombres


def test_stock_bajo():
    client.post("/reactivos", json=reactivo(nombre="Poco", cantidad=2))
    nombres = [x["nombre"] for x in client.get("/reactivos/stock-bajo?minimo=5").json()]
    assert "Poco" in nombres


def test_404_y_validacion():
    assert client.get("/reactivos/99999").status_code == 404
    assert client.post("/reactivos", json=reactivo(cantidad=-1)).status_code == 422
