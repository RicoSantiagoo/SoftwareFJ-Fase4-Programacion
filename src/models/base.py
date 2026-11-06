"""
Clase Abstracta Base - EntidadSistema
Estudiante: Santiago Rico Hernández
Curso: Programación (213023) - UNAD
"""

from abc import ABC, abstractmethod
from datetime import datetime


class EntidadSistema(ABC):
    """
    Clase abstracta base para las entidades del proyecto (Clientes, Servicios, Reservas).
    Define identificador, fecha de creación y métodos obligatorios para clases hijas.
    """

    def __init__(self, identificador: str):
        if not isinstance(identificador, str) or not identificador.strip():
            from src.exceptions.custom_exceptions import ParametroInvalidoError
            raise ParametroInvalidoError(
                "El ID de la entidad no puede estar vacío.",
                detalle=f"Recibido: {identificador}"
            )
        self._id = identificador.strip()
        self._fecha_creacion = datetime.now()

    @property
    def id(self) -> str:
        return self._id

    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion

    @abstractmethod
    def validar(self) -> bool:
        """Método abstracto: cada entidad debe implementar sus validaciones."""
        pass

    @abstractmethod
    def a_diccionario(self) -> dict:
        """Método abstracto: convierte los atributos de la entidad a diccionario."""
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id='{self._id}'>"
