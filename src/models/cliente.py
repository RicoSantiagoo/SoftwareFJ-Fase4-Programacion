"""
Módulo del Modelo Cliente.
Implementa encapsulación rigurosa y validación estricta de datos personales.
"""

import re
from typing import Any, Dict
from src.models.base import EntidadSistema
from src.exceptions.custom_exceptions import ClienteInvalidoError


class Cliente(EntidadSistema):
    """
    Representa a un cliente dentro de Software FJ.
    Aplica encapsulación mediante atributos privados y propiedades con validación.
    """

    # Expresión regular para validación de correos electrónicos bajo estándar RFC 5322
    PATRON_CORREO = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    # Expresión regular para teléfonos celulares estándar (10 dígitos numéricos)
    PATRON_TELEFONO = re.compile(r"^\d{10}$")

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str, es_frecuente: bool = False):
        """
        Constructor que inicializa y valida rigurosamente los datos del cliente.
        """
        # Inicializa la entidad base con el identificador del cliente
        super().__init__(id_cliente)

        # Asignación mediante setters protegidos para garantizar validación en el instanciamiento
        self._nombre: str = ""
        self._correo: str = ""
        self._telefono: str = ""
        self._es_frecuente: bool = bool(es_frecuente)

        # Se invocan los setters para ejecutar las validaciones
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

        # Validación holística del objeto
        self.validar()

    @property
    def id_cliente(self) -> str:
        """Propiedad de lectura para el identificador del cliente."""
        return self._id

    @property
    def nombre(self) -> str:
        """Obtiene el nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Establece y valida el nombre del cliente."""
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(
                "El nombre del cliente debe contener al menos 3 caracteres alfabéticos.",
                detalle=f"Valor recibido: '{valor}'"
            )
        if any(char.isdigit() for char in valor):
            raise ClienteInvalidoError(
                "El nombre del cliente no puede contener dígitos numéricos.",
                detalle=f"Valor recibido: '{valor}'"
            )
        self._nombre = valor.strip().title()

    @property
    def correo(self) -> str:
        """Obtiene el correo electrónico del cliente."""
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Establece y valida el correo electrónico mediante expresión regular."""
        if not isinstance(valor, str) or not self.PATRON_CORREO.match(valor.strip()):
            raise ClienteInvalidoError(
                "El correo electrónico no posee un formato válido (ejemplo: usuario@dominio.com).",
                detalle=f"Valor recibido: '{valor}'"
            )
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        """Obtiene el número telefónico del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Establece y valida que el teléfono corresponda a una línea móvil válida de 10 dígitos."""
        if not isinstance(valor, str) or not self.PATRON_TELEFONO.match(valor.strip()):
            raise ClienteInvalidoError(
                "El número de teléfono debe componerse exactamente de 10 dígitos numéricos.",
                detalle=f"Valor recibido: '{valor}'"
            )
        self._telefono = valor.strip()

    @property
    def es_frecuente(self) -> bool:
        """Indica si el cliente posee estatus frecuente para descuentos especiales."""
        return self._es_frecuente

    @es_frecuente.setter
    def es_frecuente(self, valor: bool) -> None:
        """Actualiza el estatus de fidelización del cliente."""
        self._es_frecuente = bool(valor)

    def validar(self) -> bool:
        """
        Verifica integralmente la consistencia de los datos del cliente.
        """
        if not self._id or not self._nombre or not self._correo or not self._telefono:
            raise ClienteInvalidoError("Existen campos requeridos incompletos o vacíos en el cliente.")
        return True

    def a_diccionario(self) -> Dict[str, Any]:
        """Convierte los atributos del cliente en un diccionario representativo."""
        return {
            "id_cliente": self._id,
            "nombre": self._nombre,
            "correo": self._correo,
            "telefono": self._telefono,
            "es_frecuente": self._es_frecuente,
            "fecha_registro": self._fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __str__(self) -> str:
        tipo = "Frecuente (VIP)" if self._es_frecuente else "Estándar"
        return f"Cliente: {self._nombre} | ID: {self._id} | Correo: {self._correo} | Tel: {self._telefono} [{tipo}]"
