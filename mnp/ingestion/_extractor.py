"""
Motor de extracción de datos del INEI.
Descarga y extrae módulos ENDES desde el portal de microdatos.
"""

import json
import os
import re
import shutil
import time
import urllib.parse
import zipfile

from bs4 import BeautifulSoup
import requests

from mnp.config import ENDES_SURVEY_NAME, INEI_BASE_URL, RAW_DATA_DIR


class IneiExtractor:
    """
    Motor de extracción de datos del INEI.
    Lógica pura de scraping, consultas y descargas.
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )
        self.base_url = INEI_BASE_URL
        self.encuesta_nombre = ENDES_SURVEY_NAME

    def login(self):
        """Establece sesión con el portal de microdatos."""
        try:
            self.session.get(f"{self.base_url}/microdatos/Consulta_por_Encuesta.asp")
            return True
        except Exception:
            return False

    # =========================================================================
    # --- MÉTODOS DE ACCIÓN Y ESCRITURA (Modifican o guardan archivos en la PC) ---
    # =========================================================================

    def download_module(self, year, url, metadata=None, on_progress_callback=None, force=False):
        """Descarga un módulo en formato ZIP, lo extrae localmente y limpia."""
        filename_zip = url.split("/")[-1]

        # Nombre limpio: ModuloXXXX
        if metadata and "module_code" in metadata:
            base_name = f"Modulo{metadata['module_code']}"
        else:
            # Fallback por si no hay metadata
            base_name = re.sub(r"^\d+-", "", filename_zip.replace(".zip", ""))

        output_dir = RAW_DATA_DIR / str(year) / base_name
        temp_zip = RAW_DATA_DIR / str(year) / filename_zip

        if not force and output_dir.exists():
            self._save_metadata(str(output_dir), metadata)
            return True, "skipped", list(os.listdir(output_dir))

        output_dir.mkdir(parents=True, exist_ok=True)
        try:
            res = self.session.get(url, stream=True)
            total_size = int(res.headers.get("content-length", 0))

            with open(temp_zip, "wb") as f:
                for chunk in res.iter_content(chunk_size=8192):
                    f.write(chunk)
                    if on_progress_callback:
                        on_progress_callback(len(chunk), total_size, filename_zip, "Descargando")

            from datetime import datetime

            if metadata is None:
                metadata = {}
            metadata["remote_zip_size"] = total_size
            metadata["downloaded_at"] = datetime.now().isoformat()

            with zipfile.ZipFile(temp_zip, "r") as z:
                members = [m for m in z.namelist() if not m.endswith("/")]
                for member in members:
                    z.extract(member, output_dir)
                    f_name = os.path.basename(member)
                    if on_progress_callback:
                        on_progress_callback(0, total_size, filename_zip, f"Extrayendo: {f_name}")
                    time.sleep(0.02)

            os.remove(temp_zip)
            self._flatten_dir(str(output_dir))
            self._save_metadata(str(output_dir), metadata)
            return True, "downloaded", list(os.listdir(output_dir))
        except Exception as e:
            return False, str(e), []

    def _save_metadata(self, output_dir, metadata):
        """Guarda metadata del módulo como JSON local."""
        if metadata:
            with open(os.path.join(output_dir, "metadata.json"), "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=4, ensure_ascii=False)

    def _flatten_dir(self, target_path):
        """Aplana subdirectorios de extracción moviendo los archivos a la raíz."""
        for root, dirs, files in os.walk(target_path, topdown=False):
            for f in files:
                current = os.path.join(root, f)
                final = os.path.join(target_path, f)
                if current != final:
                    shutil.move(current, final)
            if root != target_path:
                try:
                    os.rmdir(root)
                except Exception:
                    pass

    # =========================================================================
    # --- MÉTODOS DE CONSULTA Y LECTURA (Cero escritura en disco / Solo lectura) ---
    # =========================================================================

    @staticmethod
    def parse_years(year_str: str = None) -> list[int]:
        """Parsea un string de año o rango (ej: 2024 o 1996-2004) a una lista de enteros."""
        from mnp.config import ENDES_YEAR_END, ENDES_YEAR_START

        if year_str is None:
            return list(range(ENDES_YEAR_START, ENDES_YEAR_END + 1))
        if "-" in year_str:
            start, end = map(int, year_str.split("-"))
            return list(range(start, end + 1))
        return [int(year_str)]

    def get_module_links(self, year):
        """Obtiene la lista de módulos disponibles para un año en el servidor INEI."""
        url = f"{self.base_url}/microdatos/cambiaPeriodo.asp"
        modulos = []

        # El INEI usa '5' (Anual) y '51' (Línea de Base PpR...) para ENDES 2008.
        for trimestre in ["5", "51"]:
            payload = urllib.parse.urlencode(
                {
                    "bandera": "1",
                    "_cmbEncuesta": self.encuesta_nombre,
                    "_cmbAnno": str(year),
                    "_cmbTrimestre": trimestre,
                },
                encoding="iso-8859-1",
            )
            try:
                response = self.session.post(url, data=payload)
                soup = BeautifulSoup(response.text, "html.parser")
                for fila in soup.find_all("tr"):
                    enlaces = fila.find_all("a", href=True)
                    for e in enlaces:
                        if "SPSS" in e.get("title", "").upper() or "SPSS" in e.text.upper():
                            celdas = fila.find_all("td")
                            if len(celdas) >= 7:
                                module_code = celdas[5].text.strip()
                                module_name_raw = celdas[6].text.strip()
                                if not module_code.isdigit():
                                    continue
                                nombre = f"{module_code} - {module_name_raw}"
                                metadata = {
                                    "survey_code": celdas[3].text.strip(),
                                    "survey_name": celdas[4].text.strip(),
                                    "module_code": module_code,
                                    "module_name": module_name_raw,
                                    "year": str(year),
                                }
                                link = self.base_url + e["href"]
                                if not any(m[1] == link for m in modulos):
                                    modulos.append((nombre, link, metadata))
            except Exception:
                pass
        return modulos

    def get_remote_size(self, url):
        """Obtiene el tamaño del archivo en el servidor remoto sin descargarlo."""
        try:
            res = self.session.head(url, allow_redirects=True, timeout=5)
            return int(res.headers.get("content-length", 0))
        except Exception:
            return 0

    def check_local_exists(self, year, base_name):
        """Verifica si el módulo ya fue extraído en el disco local."""
        return (RAW_DATA_DIR / str(year) / base_name).exists()

    def get_module_files(self, year, base_name):
        """Lista los nombres de archivos dentro de un módulo local."""
        path = RAW_DATA_DIR / str(year) / base_name
        if path.exists():
            return [f.name for f in path.iterdir() if f.is_file()]
        return []

    def get_local_metadata(self, year, base_name):
        """Lee la metadata de descarga guardada localmente en JSON."""
        path = RAW_DATA_DIR / str(year) / base_name / "metadata.json"
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def get_local_module_size(self, year, base_name):
        """Calcula el peso total acumulado en bytes de un módulo en disco."""
        path = RAW_DATA_DIR / str(year) / base_name
        total = 0
        if path.exists():
            for root, _, files in os.walk(path):
                for f in files:
                    total += os.path.getsize(os.path.join(root, f))
        return total

    def get_file_size(self, year, base_name, filename):
        """Obtiene el peso en bytes de un archivo específico local."""
        path = RAW_DATA_DIR / str(year) / base_name / filename
        return path.stat().st_size if path.exists() else 0
