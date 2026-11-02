# Reportes de laboratorio automatizados

Script de línea de comandos que toma un CSV con resultados de laboratorio, los evalúa
contra sus límites de especificación y genera un reporte en Excel con tres hojas:

1. **Resumen**: parámetros por muestra, cuántos están fuera de especificación y el estado.
2. **Resultados**: todos los datos con la columna `conforme`.
3. **Fuera de especificación**: solo los resultados que no cumplen.

Automatiza una tarea que en el laboratorio se hace a mano en Excel: revisar fila por fila
qué resultados salen de rango.

**Tecnologías:** Python, pandas, openpyxl, pytest.

## Uso

```bash
pip install -r requirements.txt
python reportes.py datos_ejemplo.csv -o reporte.xlsx
```

Formato del CSV: `muestra, parametro, valor, unidad, limite_min, limite_max`
(los límites pueden quedar vacíos si solo hay mínimo o solo máximo).

## Pruebas

```bash
python -m pytest -q
```

Cubren la evaluación de límites, el resumen por muestra, la validación de columnas, la
generación del Excel y el manejo de archivos inexistentes.
