"""
Módulo de la Clase Abstracta Base del Sistema.
Define el contrato fundamental para todas las entidades del dominio de Software FJ.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict


class EntidadSistema(ABC):
    """
    Clase abstracta que define las características generales y comunes
    para todas las entidades del sistema (Clientes, Servicios, Reservas).
    """

    def __init__(self, identificador: str):
        """
        Inicializa una entidad del sistema con un identificador único y su marca temporal de registro.
        """
        if not isinstance(identificador, str) or not identificador.strip():
            from src.exceptions.custom_exceptions import ParametroInvalidoError
            raise ParametroInvalidoError(
                "El identificador de la entidad no puede ser nulo, vacío ni un tipo de dato diferente a cadena.",
                detalle=f"Valor recibido: {identificador}"
            )
        self._id: str = identificador.strip()
        self._fecha_creacion: datetime = datetime.now()

    @property
    def id(self) -> str:
        """Obtiene el identificador único de la entidad."""
        return self._id

    @property
    def fecha_creacion(self) -> datetime:
        """Obtiene la fecha y hora de creación de la entidad."""
        return self._fecha_creacion

    @abstractmethod
    def validar(self) -> bool:
        """
        Valida que el estado interno y atributos de la entidad cumplan las reglas de negocio.
        Debe lanzar excepciones derivadas de ValidacionError si encuentra inconsistencias.
        """
        pass

    @abstractmethod
    def a_diccionario(self) -> Dict[str, Any]:
        """
        Exporta la información de la entidad a una estructura de diccionario estándar.
        """
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id='{self._id}', creado='{self._fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}')>"

    def __eq__(self, otro: Any) -> bool:
        if not isinstance(otro, EntidadSistema):
            return False
        return self._id == otro.id and self.__class__ == otro.__class__
