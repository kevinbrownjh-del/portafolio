# API de resultados de muestras

API REST para registrar resultados analíticos de muestras (por ejemplo aguas) y detectar
automáticamente los que salen de especificación. Los límites los define quien registra
el resultado, así que sirve para cualquier norma o método.

**Tecnologías:** Python, FastAPI, SQLAlchemy 2, SQLite, Pydantic, pytest.

## Qué hace

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/muestras` | Crea una muestra (código único, matriz, punto de muestreo, fecha) |
| POST | `/muestras/{id}/resultados` | Registra un parámetro con su valor y límites; calcula si es conforme |
| GET | `/muestras/{id}/resumen` | Total de parámetros, conformes, fuera de especificación y estado |
| GET | `/resultados/fuera-de-especificacion?parametro=` | Todos los resultados no conformes |

Detalles de diseño:
- La evaluación (`app/especificacion.py`) es una función pura, con límites inclusivos y
  opcionales (solo mínimo, solo máximo o ambos), probada de forma independiente.
- Un mínimo mayor que el máximo se rechaza con `422`.
- Un código de muestra duplicado devuelve `409`.

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Documentación interactiva en http://127.0.0.1:8000/docs.

## Pruebas

```bash
python -m pytest -q
```
