"""Guardado de figuras para los scripts de analisis.

Reemplaza los outputs incrustados de los notebooks: cada figura se escribe en
`reports/figures/<ruta del script bajo scripts/>/<nombre>.png`, de modo que
queda versionada como archivo real y referenciable desde el manuscrito.

Uso tipico dentro de un script de `scripts/`:

    from mnp.utils.figures import save_fig
    save_fig("01_nulos_categoricas")        # cierra la figura actual

En una sesion interactiva (Run Cell en VS Code) la figura se guarda igual y
ademas se muestra si `show=True`.
"""

import inspect
from pathlib import Path

from mnp.config import FIGURES_DIR, PROJ_ROOT

SCRIPTS_DIR = PROJ_ROOT / "scripts"


def _caller_dir() -> Path:
    """Carpeta de salida derivada del script que invoca, relativa a scripts/."""
    for frame in inspect.stack()[1:]:
        path = Path(frame.filename).resolve()
        if path.is_file() and path.suffix == ".py" and SCRIPTS_DIR in path.parents:
            return path.relative_to(SCRIPTS_DIR).with_suffix("")
    # fallback: ejecucion desde consola/REPL sin archivo identificable
    return Path("_interactive")


def figures_dir() -> Path:
    """Directorio de figuras del script actual, creado si no existe."""
    out = FIGURES_DIR / _caller_dir()
    out.mkdir(parents=True, exist_ok=True)
    return out


def save_fig(name: str, fig=None, dpi: int = 150, show: bool | None = None) -> Path:
    """Guarda `fig` (o la figura activa) como PNG y devuelve su ruta.

    La figura SIEMPRE se escribe a disco. Ademas se muestra en pantalla cuando
    el backend de matplotlib es interactivo (Run Cell en VS Code, Jupyter, o una
    ejecucion normal en escritorio); con un backend headless como `Agg` solo se
    guarda. Pasar `show=True/False` fuerza el comportamiento.
    """
    import matplotlib
    import matplotlib.pyplot as plt

    if fig is None:
        fig = plt.gcf()
    path = figures_dir() / f"{name}.png"
    fig.savefig(path, dpi=dpi, bbox_inches="tight")

    if show is None:
        show = matplotlib.get_backend().lower() != "agg"
    if show:
        plt.show()
    else:
        plt.close(fig)
    return path
