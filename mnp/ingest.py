"""
CLI de ingesta y extracción de datos ENDES desde el INEI.

Se encarga de descargar los archivos crudos (ZIPs) y colocarlos en data/raw,
además de auditar su integridad física.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time

from rich.live import Live
import typer

from mnp.utils.console import Console
from mnp.utils.extractor import IneiExtractor

app = typer.Typer(help="Ingesta de datos ENDES (INEI)")


# TODO: Refactorizar a futuro para desacoplar completamente la interfaz de usuario de Rich
# (Live, Console, cb_live) de la lógica de control de ingesta, delegando la
# visualización de progreso a un sistema de eventos o listener.
def _run_extraction(
    years: list[int],
    module: str = None,
    force: bool = False,
    check: bool = False,
    verbose: bool = False,
):
    """Lógica central de extracción."""
    extractor = IneiExtractor()
    console = Console()
    console.welcome()

    for year in years:
        console.separator(f"📂 EXTRACCIÓN AÑO: {year}")

        # 1. Obtener catálogo de módulos
        catalog = extractor.get_module_links(year)
        if module:
            catalog = [m for m in catalog if str(module) in m[0]]

        if not catalog:
            console.rich.print(f"[yellow]⚠️ No se encontraron módulos para el año {year}[/]")
            continue

        # 2. Preparar estadísticas de seguimiento
        stats = {}
        to_download = []

        for title, link, metadata in catalog:
            zip_name = link.split("/")[-1]
            base = f"Modulo{metadata['module_code']}"
            exists = extractor.check_local_exists(year, base)

            # Auditoría Cloud
            remote_b = extractor.get_remote_size(link)
            local_b = extractor.get_local_module_size(year, base) if exists else 0
            status = "[green]Local[/]" if exists else "[red]Faltante[/]"
            progress = 100 if exists else 0

            # Validación de integridad física
            if exists and remote_b > 0 and local_b < remote_b:
                status = "[red]Incompleto[/]"
                progress = 50

            if force and exists:
                status = "[yellow]Update[/]"

            stats[title] = {
                "status": status,
                "progress": progress,
                "total": 100,
                "files": [],
                "folder": base,
                "zip_name": zip_name,
                "done": False,
                "total_bytes": local_b,
                "remote_bytes": remote_b,
                "elapsed": 0.0,
                "start_time": time.time(),
            }

            if check:
                stats[title]["done"] = True
                if verbose and exists:
                    files = extractor.get_module_files(year, base)
                    stats[title]["files"] = [
                        (f, extractor.get_file_size(year, base, f)) for f in files
                    ]
                console.rich.print(console.render_module_row(title, stats, verbose))
            else:
                if "Local" not in status or force:
                    to_download.append((title, link, metadata))
                else:
                    stats[title]["done"] = True
                    if verbose:
                        files = extractor.get_module_files(year, base)
                        stats[title]["files"] = [
                            (f, extractor.get_file_size(year, base, f)) for f in files
                        ]
                    console.rich.print(console.render_module_row(title, stats, verbose))

        # 3. Descarga y Extracción con UI Live
        if not to_download:
            continue

        ui_lock = threading.Lock()

        def generate_view():
            return console.render_extraction_view(stats, verbose)

        def cb_live(m_title, current, total, f_name, status=None):
            with ui_lock:
                if status:
                    stats[m_title]["status"] = status
                stats[m_title]["progress"] = current
                stats[m_title]["total"] = total
                if not stats[m_title]["done"]:
                    stats[m_title]["elapsed"] = time.time() - stats[m_title]["start_time"]

        with Live(generate_view(), refresh_per_second=10, transient=False) as live:
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = {}
                for title, link, metadata in to_download:
                    force_this = force or stats[title]["status"] in [
                        "[red]Incompleto[/]",
                        "[yellow]Update[/]",
                    ]

                    futures[
                        executor.submit(
                            extractor.download_module,
                            year,
                            link,
                            metadata,
                            lambda c, t, f, s=None, mt=title: cb_live(mt, c, t, f, s),
                            force=force_this,
                        )
                    ] = title

                for future in as_completed(futures):
                    m_title = futures[future]
                    success, res_status, files = future.result()
                    with ui_lock:
                        stats[m_title]["done"] = True
                        stats[m_title]["elapsed"] = time.time() - stats[m_title]["start_time"]
                        if success:
                            f_with_size = []
                            total_b = 0
                            for f in files:
                                sz = extractor.get_file_size(year, stats[m_title]["folder"], f)
                                f_with_size.append((f, sz))
                                total_b += sz

                            stats[m_title]["total_bytes"] = total_b
                            stats[m_title]["files"] = f_with_size
                            stats[m_title]["status"] = "[green]Completado[/]"
                            stats[m_title]["progress"] = stats[m_title]["total"]

                        live.console.print(console.render_module_row(m_title, stats, verbose))
                    live.update(generate_view())

    console.proceso_completado()


@app.command()
def extract(
    year: str = typer.Option(None, help="Año o rango de años (ej: 2024 o 1996-2004)"),
    module: str = typer.Option(None, help="Filtrar por nombre de módulo"),
    force: bool = typer.Option(False, help="Forzar re-descarga y extracción"),
    check: bool = typer.Option(False, help="Solo verificar existencia"),
    verbose: bool = typer.Option(False, help="Mostrar detalles de archivos"),
):
    """Extraer datos de INEI a data/raw."""
    years = IneiExtractor.parse_years(year)
    _run_extraction(years, module, force, check, verbose)


@app.command()
def audit(
    year: str = typer.Option(None, help="Año o rango de años"),
    module: str = typer.Option(None, help="Filtrar por nombre de módulo"),
    repair: bool = typer.Option(False, help="Intentar reparar módulos incompletos"),
):
    """Auditar integridad de los datos descargados."""
    years = IneiExtractor.parse_years(year)
    _run_extraction(years, module, force=repair, check=True, verbose=True)


if __name__ == "__main__":
    app()
