"""
Clase Cliente - Sistema Software FJ
Estudiante: Santiago Rico Hernández
Curso: Programación (213023) - UNAD
"""

import re
from src.models.base import EntidadSistema
from src.exceptions.custom_exceptions import ClienteInvalidoError


class Cliente(EntidadSistema):
    """
    Representa a un cliente de la empresa Software FJ.
    Aplica encapsulamiento con atributos privados y getters/setters (@property).
    """

    # Expresión regular para validar formato de correo (ejemplo: usuario@correo.com)
    PATRON_CORREO = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
    # Validación de número de celular estándar en Colombia (10 dígitos)
    PATRON_TELEFONO = re.compile(r"^\d{10}$")

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str, es_frecuente: bool = False):
        super().__init__(id_cliente)

        self._nombre = ""
        self._correo = ""
        self._telefono = ""
        self._es_frecuente = bool(es_frecuente)

        # Pasamos por los setters para validar desde la creación
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

        # Validación final de campos obligatorios
        self.validar()

    @property
    def id_cliente(self) -> str:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        # El nombre debe tener al menos 3 letras y no contener números
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(
                "El nombre del cliente debe tener al menos 3 letras.",
                detalle=f"Valor ingresado: '{valor}'"
            )
        if any(char.isdigit() for char in valor):
            raise ClienteInvalidoError(
                "El nombre no puede tener números.",
                detalle=f"Valor ingresado: '{valor}'"
            )
        self._nombre = valor.strip().title()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        # Valida que cumpla formato básico de correo
        if not isinstance(valor, str) or not self.PATRON_CORREO.match(valor.strip()):
            raise ClienteInvalidoError(
                "El correo electrónico no es válido (ejemplo: nombre@dominio.com).",
                detalle=f"Valor ingresado: '{valor}'"
            )
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        # Valida exactamente 10 dígitos numéricos
        if not isinstance(valor, str) or not self.PATRON_TELEFONO.match(valor.strip()):
            raise ClienteInvalidoError(
                "El teléfono debe tener exactamente 10 dígitos numéricos.",
                detalle=f"Valor ingresado: '{valor}'"
            )
        self._telefono = valor.strip()

    @property
    def es_frecuente(self) -> bool:
        return self._es_frecuente

    @es_frecuente.setter
    def es_frecuente(self, valor: bool):
        self._es_frecuente = bool(valor)

    def validar(self) -> bool:
        """Verifica que ningún dato obligatorio esté vacío."""
        if not self._id or not self._nombre or not self._correo or not self._telefono:
            raise ClienteInvalidoError("Todos los campos del cliente son obligatorios.")
        return True

    def a_diccionario(self) -> dict:
        """Convierte los datos del cliente a formato diccionario."""
        return {
            "id_cliente": self._id,
            "nombre": self._nombre,
            "correo": self._correo,
            "telefono": self._telefono,
            "es_frecuente": self._es_frecuente,
            "fecha_registro": self._fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __str__(self) -> str:
        estado_vip = "VIP" if self._es_frecuente else "Normal"
        return f"{self._nombre} (ID: {self._id}) - Correo: {self._correo} - Tel: {self._telefono} [{estado_vip}]"
