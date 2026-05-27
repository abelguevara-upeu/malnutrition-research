"""
Ingeniería de features para modelado.

Lee desde data/interim/master_validated.csv y genera features
para los modelos de desnutrición crónica.
"""

from pathlib import Path

from loguru import logger
from tqdm import tqdm
import typer

from mnp.config import INTERIM_DATA_DIR, PROCESSED_DATA_DIR

# TODO
app = typer.Typer()

@app.command()
def main(
    input_path: Path = INTERIM_DATA_DIR / "master_validated.csv",
    output_path: Path = PROCESSED_DATA_DIR / "features.csv",
):
    """Genera features desde el dataset validado."""
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info(f"Generating features from {input_path}...")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Features generation complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
