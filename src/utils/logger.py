"""
Módulo de Configuración de Logging para Software FJ.
Configura manejadores de archivo y consola con codificación UTF-8 y formatos homogéneos.
"""

import logging
import os
from typing import Optional

LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "software_fj.log")


def configurar_logger(nombre_logger: str = "SoftwareFJ", nivel: int = logging.INFO) -> logging.Logger:
    """
    Configura y retorna una instancia de logger configurada con:
    1. FileHandler hacia 'software_fj.log' con codificación UTF-8.
    2. StreamHandler hacia la consola estándar.
    """
    logger = logging.getLogger(nombre_logger)
    logger.setLevel(nivel)

    # Evitar duplicar manejadores si la función se invoca múltiples veces
    if not logger.handlers:
        formato = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s:%(module)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Manejador de archivo UTF-8
        file_handler = logging.FileHandler(LOG_FILE_PATH, mode="a", encoding="utf-8")
        file_handler.setLevel(nivel)
        file_handler.setFormatter(formato)
        logger.addHandler(file_handler)

        # Manejador de consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(nivel)
        console_handler.setFormatter(formato)
        logger.addHandler(console_handler)

    return logger


# Instancia por defecto lista para su uso en toda la solución
logger_sistema = configurar_logger()
