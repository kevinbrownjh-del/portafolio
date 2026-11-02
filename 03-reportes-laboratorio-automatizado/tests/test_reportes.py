import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import reportes  # noqa: E402

EJEMPLO = Path(__file__).resolve().parent.parent / "datos_ejemplo.csv"


def test_evaluar_marca_fuera_de_especificacion():
    df = reportes.evaluar(reportes.cargar(str(EJEMPLO)))
    fuera = df[~df["conforme"]]
    assert set(zip(fuera["muestra"], fuera["parametro"])) == {
        ("M-002", "pH"),
        ("M-002", "Turbidez"),
    }


def test_resumen_por_muestra():
    df = reportes.evaluar(reportes.cargar(str(EJEMPLO)))
    estados = reportes.resumen_por_muestra(df).set_index("muestra")["estado"]
    assert estados["M-001"] == "conforme"
    assert estados["M-002"] == "no conforme"


def test_cargar_rechaza_columnas_faltantes(tmp_path):
    malo = tmp_path / "malo.csv"
    malo.write_text("muestra,valor\nM-1,3\n")
    with pytest.raises(ValueError, match="Faltan columnas"):
        reportes.cargar(str(malo))


def test_cli_genera_excel_con_tres_hojas(tmp_path):
    salida = tmp_path / "reporte.xlsx"
    assert reportes.main([str(EJEMPLO), "-o", str(salida)]) == 0
    hojas = pd.ExcelFile(salida).sheet_names
    assert hojas == ["Resumen", "Resultados", "Fuera de especificación"]


def test_cli_archivo_inexistente_devuelve_error(tmp_path):
    assert reportes.main([str(tmp_path / "nada.csv")]) == 1
