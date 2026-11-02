"""Genera un reporte en Excel a partir de resultados de laboratorio en CSV.

Uso:
    python reportes.py datos_ejemplo.csv -o reporte.xlsx
"""
import argparse
import sys

import pandas as pd

COLUMNAS = ["muestra", "parametro", "valor", "unidad", "limite_min", "limite_max"]


def cargar(ruta: str) -> pd.DataFrame:
    df = pd.read_csv(ruta)
    faltan = [c for c in COLUMNAS if c not in df.columns]
    if faltan:
        raise ValueError(f"Faltan columnas en el archivo: {', '.join(faltan)}")
    df["valor"] = pd.to_numeric(df["valor"], errors="raise")
    for col in ("limite_min", "limite_max"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def evaluar(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega la columna `conforme` (límites inclusivos y opcionales)."""
    df = df.copy()
    bajo = df["limite_min"].notna() & (df["valor"] < df["limite_min"])
    alto = df["limite_max"].notna() & (df["valor"] > df["limite_max"])
    df["conforme"] = ~(bajo | alto)
    return df


def resumen_por_muestra(df: pd.DataFrame) -> pd.DataFrame:
    grupos = df.groupby("muestra")["conforme"]
    resumen = pd.DataFrame(
        {
            "parametros": grupos.size(),
            "fuera_de_especificacion": grupos.apply(lambda s: int((~s).sum())),
        }
    )
    resumen["estado"] = resumen["fuera_de_especificacion"].map(
        lambda n: "conforme" if n == 0 else "no conforme"
    )
    return resumen.reset_index()


def escribir_reporte(df: pd.DataFrame, salida: str) -> None:
    resumen = resumen_por_muestra(df)
    fuera = df[~df["conforme"]]
    with pd.ExcelWriter(salida, engine="openpyxl") as writer:
        resumen.to_excel(writer, sheet_name="Resumen", index=False)
        df.to_excel(writer, sheet_name="Resultados", index=False)
        fuera.to_excel(writer, sheet_name="Fuera de especificación", index=False)
        for hoja in writer.sheets.values():
            for columna in hoja.columns:
                ancho = max(len(str(c.value)) if c.value is not None else 0 for c in columna)
                hoja.column_dimensions[columna[0].column_letter].width = ancho + 3


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("entrada", help="CSV con columnas: " + ", ".join(COLUMNAS))
    parser.add_argument("-o", "--salida", default="reporte.xlsx")
    args = parser.parse_args(argv)

    try:
        df = evaluar(cargar(args.entrada))
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    escribir_reporte(df, args.salida)
    total, fuera = len(df), int((~df["conforme"]).sum())
    print(f"{total} resultados procesados, {fuera} fuera de especificación -> {args.salida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
