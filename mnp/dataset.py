"""
CLI para la generación y compilación del dataset consolidado (Capa Cleaned y Validated).

Orquesta los pipelines locales de limpieza y validación de datos a partir de data/raw.
"""

import typer

from mnp.pipeline import cleaning, validation

# TODO
app = typer.Typer(help="Generación de Datasets ENDES")


@app.command()
def clean():
    """Ejecutar pipeline de limpieza (raw -> interim/master_cleaned.csv)."""
    cleaning.main()


@app.command()
def validate():
    """Ejecutar pipeline de validación (master_cleaned.csv -> interim/master_validated.csv)."""
    validation.main()


@app.command()
def make():
    """Ejecutar el flujo completo de construcción del dataset (limpieza + validación)."""
    cleaning.main()
    validation.main()


if __name__ == "__main__":
    app()
