# API de inventario de reactivos

API REST para controlar el stock y los vencimientos de reactivos de un laboratorio.
Nace de mi experiencia en laboratorio ambiental (pasantía en Envirolab), donde el orden
del inventario y el control de vencimientos son parte del trabajo diario.

**Tecnologías:** Python, FastAPI, SQLAlchemy 2, SQLite, pytest.

## Qué hace

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/reactivos` | Registra un reactivo (nombre, fórmula, CAS, lote, cantidad, vencimiento, peligrosidad) |
| GET | `/reactivos?nombre=` | Lista y busca por nombre |
| GET | `/reactivos/{id}` | Detalle de un reactivo |
| POST | `/reactivos/{id}/consumo` | Descuenta stock; responde `409` si no alcanza |
| GET | `/reactivos/por-vencer?dias=30` | Reactivos vencidos o próximos a vencer |
| GET | `/reactivos/stock-bajo?minimo=10` | Reactivos con poco stock |
| DELETE | `/reactivos/{id}` | Elimina un reactivo |

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abre http://127.0.0.1:8000/docs para probar la API desde el navegador.

## Pruebas

```bash
python -m pytest -q
```

Las pruebas usan una base de datos en memoria y cubren creación, consumo con stock
insuficiente, vencimientos, stock bajo y validaciones.
