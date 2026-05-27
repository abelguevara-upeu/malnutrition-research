# Usamos una imagen oficial liviana de Python 3.12.13 basada en Debian Bookworm
FROM python:3.12.13-slim-bookworm

# Evitar que Python escriba archivos .pyc y forzar salida de logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema necesarias
# - build-essential y make para compilar librerías y tareas del Makefile
# - git para control de versiones si alguna librería de pip lo requiere
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    make \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /workspace

# Copiar archivos de dependencias iniciales para aprovechar la caché de Docker
COPY pyproject.toml README.md LICENSE ./
COPY mnp/ mnp/

# Instalar dependencias del proyecto en modo editable
RUN pip install --no-cache-dir -e .

# Copiar el resto del código del proyecto
COPY . .

# Exponer el puerto de Jupyter Lab
EXPOSE 8888

# Comando por defecto al levantar el contenedor (Jupyter Lab)
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]
