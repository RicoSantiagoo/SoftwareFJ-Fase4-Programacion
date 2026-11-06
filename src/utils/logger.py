"""
Configuración de Logger para Software FJ
Guarda eventos y errores en 'software_fj.log' y los muestra por consola.
Estudiante: Santiago Rico Hernández - UNAD
"""

import logging
import os

# Ruta donde se crea el archivo de log en la raíz del proyecto
LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "software_fj.log")
LOG_FILE_PATH = LOG_PATH


def configurar_logger(nombre: str = "SoftwareFJ") -> logging.Logger:
    logger = logging.getLogger(nombre)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Formato de fecha y mensaje para el log
        formato = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Guarda en archivo con codificación utf-8
        archivo_handler = logging.FileHandler(LOG_PATH, mode="a", encoding="utf-8")
        archivo_handler.setLevel(logging.INFO)
        archivo_handler.setFormatter(formato)
        logger.addHandler(archivo_handler)

        # Muestra en consola
        consola_handler = logging.StreamHandler()
        consola_handler.setLevel(logging.INFO)
        consola_handler.setFormatter(formato)
        logger.addHandler(consola_handler)

    return logger


# Logger listo para importar en otros módulos
logger_sistema = configurar_logger()
