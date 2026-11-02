import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

client = TestClient(app)


def nueva_muestra(codigo):
    r = client.post(
        "/muestras",
        json={"codigo": codigo, "matriz": "agua residual", "fecha_toma": "2026-10-01"},
    )
    assert r.status_code == 201
    return r.json()["id"]


def resultado(mid, parametro, valor, minimo=None, maximo=None):
    return client.post(
        f"/muestras/{mid}/resultados",
        json={
            "parametro": parametro,
            "valor": valor,
            "unidad": "u",
            "limite_min": minimo,
            "limite_max": maximo,
        },
    )


def test_resumen_conforme_y_no_conforme():
    mid = nueva_muestra("M-001")
    assert resultado(mid, "pH", 7.2, 6.5, 8.5).json()["conforme"] is True
    assert client.get(f"/muestras/{mid}/resumen").json()["estado"] == "conforme"
    assert resultado(mid, "DBO", 300, None, 35).json()["conforme"] is False
    r = client.get(f"/muestras/{mid}/resumen").json()
    assert (r["estado"], r["fuera_de_especificacion"], r["conformes"]) == ("no conforme", 1, 1)


def test_codigo_duplicado():
    nueva_muestra("M-DUP")
    r = client.post(
        "/muestras", json={"codigo": "M-DUP", "matriz": "x", "fecha_toma": "2026-10-01"}
    )
    assert r.status_code == 409


def test_fuera_de_especificacion_filtra_por_parametro():
    mid = nueva_muestra("M-002")
    resultado(mid, "pH", 9.5, 6.5, 8.5)
    resultado(mid, "DQO", 500, None, 150)
    solo_ph = client.get("/resultados/fuera-de-especificacion?parametro=pH").json()
    assert solo_ph and all(x["parametro"] == "pH" for x in solo_ph)


def test_limites_invalidos_y_muestra_inexistente():
    mid = nueva_muestra("M-003")
    assert resultado(mid, "pH", 7, 9, 5).status_code == 422
    assert resultado(9999, "pH", 7).status_code == 404
