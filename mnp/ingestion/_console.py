"""
Utilidades de consola Rich para visualización del proceso de extracción.
"""

from rich.console import Console as RichConsole
from rich.console import Group
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TaskProgressColumn
from rich.rule import Rule
from rich.table import Table
from rich.text import Text


class Console:
    """Interfaz de consola con Rich para el proceso de extracción ENDES."""

    def __init__(self):
        self.rich = RichConsole()

    def welcome(self):
        """Muestra el banner de bienvenida."""
        self.rich.print("\n")
        self.rich.print(
            Panel(
                "[bold cyan]EXTRACCIÓN DE DATOS ENDES (INEI)[/bold cyan]",
                border_style="bold cyan",
                expand=False,
            )
        )

    def separator(self, label, style="yellow"):
        """Muestra un separador con etiqueta."""
        self.rich.print("\n")
        self.rich.print(Rule(label, style=style))

    def proceso_completado(self):
        """Muestra mensaje de proceso completado."""
        self.rich.print("\n[bold green]✅ ✨ PROCESO COMPLETADO ✨[/bold green]")

    def render_module_row(self, title, stats, verbose=False):
        """Genera la representación visual de un módulo con layout anticolisión."""
        info = stats[title]
        grid = Table.grid(expand=True, padding=(0, 1))

        # Estructura de columnas optimizada
        grid.add_column(no_wrap=True, width=3)  # Bullet
        grid.add_column(no_wrap=False)  # Nombre (Permite wrap)
        grid.add_column(no_wrap=True, ratio=1)  # Puntos guía
        grid.add_column(no_wrap=True, width=24, justify="right")  # ZIP
        grid.add_column(no_wrap=True, width=18, justify="right")  # Peso
        grid.add_column(no_wrap=True, width=8, justify="right")  # Tiempo
        grid.add_column(no_wrap=True, width=25, justify="right")  # Barra
        grid.add_column(no_wrap=True, width=12, justify="right")  # Estado

        # Configuración de barra
        b_color = "cyan"
        t_val = info["total"]
        if "Extraer" in info["status"] or "Extrayendo" in info["status"]:
            b_color, t_val = "yellow", None
        elif "Completado" in info["status"]:
            b_color = "green"

        p = Progress(
            BarColumn(bar_width=20, complete_style=b_color, finished_style="green"),
            TaskProgressColumn(),
        )
        p.add_task("", completed=info["progress"], total=t_val)

        # Métricas con auditoría cloud
        zip_file = info.get("zip_name", "---")
        size_mb = info.get("total_bytes", 0) / (1024 * 1024)
        remote_mb = info.get("remote_bytes", 0) / (1024 * 1024)

        if remote_mb > 0:
            # Comparativa: Local (Extraído) / Nube (ZIP)
            size_str = f"{size_mb:.1f}/{remote_mb:.1f} MB"
        else:
            size_str = f"{size_mb:.1f} MB" if size_mb > 0 else "-"

        elapsed = info.get("elapsed", 0.0)
        time_str = f"{elapsed:.1f}s" if elapsed > 0 else "-"

        # Bloque de Nombre y Archivos
        name_text = Text()
        name_text.append(f"{title} ", style="cyan bold")

        if verbose and info["files"]:
            folder = info.get("folder", "---")
            for f_data in sorted(info["files"], key=lambda x: x[0] if isinstance(x, tuple) else x):
                f, sz = f_data if isinstance(f_data, tuple) else (f_data, 0)
                is_sav = f.lower().endswith(".sav")
                is_meta = f == "metadata.json"

                icon = "⚙️ " if is_meta else ("💾" if is_sav else "📄")
                suffix = " (generated)" if is_meta else ""
                f_size = (
                    f"{sz / (1024 * 1024):.2f} MB" if sz > 1024 * 512 else f"{sz / 1024:.1f} KB"
                )

                # Jerarquía de colores
                if is_sav:
                    f_style = "magenta italic"
                elif is_meta:
                    f_style = "grey30 italic"
                else:
                    f_style = "grey82 italic"

                name_text.append(f"\n      {icon} {folder}/{f}{suffix} ({f_size})", style=f_style)

        grid.add_row(
            Text("•", style="magenta"),
            name_text,
            Text("." * 150, style="dim"),  # Guía de puntos
            Text(f"[{zip_file}]", style="dim"),
            Text(size_str, style="yellow"),
            Text(time_str, style="dim"),
            p,
            Text.from_markup(info["status"]),
        )
        return grid

    def render_extraction_view(self, stats, verbose=False, limit=6):
        """Genera el grupo visual completo para Live."""
        pending = [t for t, s in stats.items() if not s["done"]]
        if not pending:
            return Text("")

        to_show = [self.render_module_row(t, stats, verbose) for t in pending[:limit]]
        if len(pending) > limit:
            to_show.append(
                Text(
                    f"  ... y {len(pending) - limit} módulos más en espera",
                    style="dim italic",
                )
            )
        return Group(*to_show)

    def tabla_inventario(self, anio, filas):
        """Muestra tabla de inventario de datos para un año."""
        table = Table(title=f"INVENTARIO RAW — AÑO {anio}", header_style="bold magenta")
        table.add_column("Módulo", style="cyan", ratio=3)
        table.add_column("Estado", justify="center")
        table.add_column("Archivos", justify="right")

        for f in filas:
            table.add_row(f[0], f[1], f[2])
        self.rich.print(table)
