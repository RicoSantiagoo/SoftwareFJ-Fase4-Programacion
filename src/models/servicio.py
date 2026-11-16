
"""
Modulo 3 - Catalogo de Servicios
Proyecto: Software FJ - Fase 4
Curso: Programacion (213023) - UNAD
Responsable: Andres Felipe Nieves Leon
"""

from abc import abstractmethod
import math

from src.models.base import EntidadSistema

from src.exceptions.custom_exceptions import (
    SoftwareFJError,
    ServicioInvalidoError,
    ParametroInvalidoError,
    ServicioNoDisponibleError,
    CapacidadExcedidaError,
    CalculoFinancieroError
)

from src.utils.logger import logger_sistema


class Servicio(EntidadSistema):
    """
    Clase abstracta que representa los servicios
    ofrecidos por la empresa Software FJ.
    """

    def __init__(
        self,
        identificador: str,
        nombre: str,
        descripcion: str,
        tarifa_base: float,
        disponible: bool = True
    ):
        super().__init__(identificador)

        self._nombre = nombre.strip() if isinstance(nombre, str) else nombre
        self._descripcion = descripcion.strip() if isinstance(descripcion, str) else descripcion
        self._tarifa_base = tarifa_base
        self._disponible = disponible

        self._validar_datos_comunes()

    def _validar_datos_comunes(self):
        """Valida los atributos generales del servicio."""

        if not isinstance(self._nombre, str) or not self._nombre:
            raise ServicioInvalidoError(
                "El nombre del servicio no puede estar vacío."
            )

        if not isinstance(self._descripcion, str) or not self._descripcion:
            raise ServicioInvalidoError(
                "La descripción del servicio no puede estar vacía."
            )

        if (
            isinstance(self._tarifa_base, bool)
            or not isinstance(self._tarifa_base, (int, float))
            or not math.isfinite(self._tarifa_base)
            or self._tarifa_base < 0
        ):
            raise ParametroInvalidoError(
                "La tarifa base debe ser un número válido y no negativo.",
                detalle=f"Tarifa recibida: {self._tarifa_base}"
            )

        if not isinstance(self._disponible, bool):
            raise ParametroInvalidoError(
                "La disponibilidad debe ser True o False."
            )

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    def verificar_disponibilidad(self) -> bool:
        """Comprueba si el servicio puede ser utilizado."""

        if not self._disponible:
            logger_sistema.warning(
                f"Intento de utilizar servicio no disponible: {self._nombre}"
            )
            raise ServicioNoDisponibleError(
                f"El servicio '{self._nombre}' no está disponible."
            )

        return True
    def calcular_costo_seguro(self, *args, **kwargs) -> float:
        """
        Ejecuta el cálculo del servicio con manejo de excepciones.
        """

        try:
            resultado = self.calcular_costo(*args, **kwargs)

        except SoftwareFJError as error:
            logger_sistema.exception(
                f"Error controlado al calcular el servicio "
                f"{self.nombre}: {error}"
            )
            raise

        except Exception as error:
            logger_sistema.exception(
                f"Error inesperado durante el cálculo de "
                f"{self.nombre}: {error}"
            )

            raise CalculoFinancieroError(
                "No fue posible completar el cálculo del servicio.",
                detalle=str(error)
            ) from error

        else:
            logger_sistema.info(
                f"Cálculo seguro exitoso: Servicio={self.nombre}, "
                f"Costo={resultado}"
            )
            return resultado

        finally:
            logger_sistema.info(
                f"Finalizó el proceso de cálculo del servicio: "
                f"{self.nombre}"
            )
    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        pass

    @abstractmethod
    def validar(self) -> bool:
        pass

    @abstractmethod
    def a_diccionario(self) -> dict:
        pass


class ReservaSala(Servicio):
    """Representa el servicio de reserva de salas."""

    def __init__(
        self,
        identificador: str,
        nombre: str,
        descripcion: str,
        tarifa_base: float,
        capacidad_maxima: int,
        disponible: bool = True
    ):
        super().__init__(
            identificador,
            nombre,
            descripcion,
            tarifa_base,
            disponible
        )

        self._capacidad_maxima = capacidad_maxima
        self.validar()

        logger_sistema.info(
            f"Servicio creado: ID={self.id}, "
            f"Nombre={self.nombre}, Tipo={self.__class__.__name__}"
        )

    @property
    def capacidad_maxima(self) -> int:
        return self._capacidad_maxima

    def validar(self) -> bool:
        """Valida los datos específicos de la sala."""

        self._validar_datos_comunes()

        if (
            isinstance(self._capacidad_maxima, bool)
            or not isinstance(self._capacidad_maxima, int)
            or self._capacidad_maxima <= 0
        ):
            raise ParametroInvalidoError(
                "La capacidad máxima debe ser un entero mayor que cero.",
                detalle=f"Capacidad recibida: {self._capacidad_maxima}"
            )

        return True

    def calcular_costo(
        self,
        horas: int,
        cantidad_personas: int,
        descuento: float = 0
    ) -> float:
        """Calcula el costo de reservar una sala por horas."""

        self.verificar_disponibilidad()

        if isinstance(horas, bool) or not isinstance(horas, int) or horas <= 0:
            raise ParametroInvalidoError(
                "Las horas de reserva deben ser un entero mayor que cero."
            )

        if (
            isinstance(cantidad_personas, bool)
            or not isinstance(cantidad_personas, int)
            or cantidad_personas <= 0
        ):
            raise ParametroInvalidoError(
                "La cantidad de personas debe ser un entero mayor que cero."
            )

        if cantidad_personas > self._capacidad_maxima:
            raise CapacidadExcedidaError(
                "La cantidad de personas supera la capacidad de la sala.",
                detalle=(
                    f"Solicitadas: {cantidad_personas}. "
                    f"Capacidad máxima: {self._capacidad_maxima}."
                )
            )

        if (
            isinstance(descuento, bool)
            or not isinstance(descuento, (int, float))
            or not math.isfinite(descuento)
            or not 0 <= descuento <= 100
        ):
            raise ParametroInvalidoError(
                "El descuento debe estar entre 0 y 100."
            )

        subtotal = self._tarifa_base * horas
        costo_final = subtotal * (1 - descuento / 100)

        logger_sistema.info(
            f"Calculo realizado: Servicio={self.nombre}, "
            f"Tipo={self.__class__.__name__}, "
            f"Costo={round(costo_final, 2)}"
        )

        return round(costo_final, 2)

    def a_diccionario(self) -> dict:
        """Convierte la información de la sala a un diccionario."""

        return {
            "tipo_servicio": "ReservaSala",
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "tarifa_base": self.tarifa_base,
            "disponible": self.disponible,
            "capacidad_maxima": self.capacidad_maxima,
            "fecha_creacion": self.fecha_creacion.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }


class AlquilerEquipo(Servicio):
    """Representa el servicio de alquiler de equipos."""

    def __init__(
        self,
        identificador: str,
        nombre: str,
        descripcion: str,
        tarifa_base: float,
        equipo: str,
        disponible: bool = True
    ):
        super().__init__(
            identificador,
            nombre,
            descripcion,
            tarifa_base,
            disponible
        )

        self._equipo = equipo.strip() if isinstance(equipo, str) else equipo
        self.validar()

        logger_sistema.info(
            f"Servicio creado: ID={self.id}, "
            f"Nombre={self.nombre}, Tipo={self.__class__.__name__}"
        )

    @property
    def equipo(self) -> str:
        return self._equipo

    def validar(self) -> bool:
        """Valida los datos específicos del alquiler."""

        self._validar_datos_comunes()

        if not isinstance(self._equipo, str) or not self._equipo:
            raise ServicioInvalidoError(
                "El nombre del equipo no puede estar vacío."
            )

        return True

    def calcular_costo(
        self,
        dias: int,
        cantidad: int = 1,
        descuento: float = 0
    ) -> float:
        """Calcula el costo del alquiler por días y unidades."""

        self.verificar_disponibilidad()

        if isinstance(dias, bool) or not isinstance(dias, int) or dias <= 0:
            raise ParametroInvalidoError(
                "Los días de alquiler deben ser un entero mayor que cero."
            )

        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, int)
            or cantidad <= 0
        ):
            raise ParametroInvalidoError(
                "La cantidad de equipos debe ser un entero mayor que cero."
            )

        if (
            isinstance(descuento, bool)
            or not isinstance(descuento, (int, float))
            or not math.isfinite(descuento)
            or not 0 <= descuento <= 100
        ):
            raise ParametroInvalidoError(
                "El descuento debe estar entre 0 y 100."
            )

        subtotal = self._tarifa_base * dias * cantidad
        costo_final = subtotal * (1 - descuento / 100)

        logger_sistema.info(
            f"Calculo realizado: Servicio={self.nombre}, "
            f"Tipo={self.__class__.__name__}, "
            f"Costo={round(costo_final, 2)}"
        )

        return round(costo_final, 2)

    def a_diccionario(self) -> dict:
        """Convierte los datos del alquiler a un diccionario."""

        return {
            "tipo_servicio": "AlquilerEquipo",
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "tarifa_base": self.tarifa_base,
            "disponible": self.disponible,
            "equipo": self.equipo,
            "fecha_creacion": self.fecha_creacion.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }


class AsesoriaEspecializada(Servicio):
    """Representa el servicio de asesoría especializada."""

    def __init__(
        self,
        identificador: str,
        nombre: str,
        descripcion: str,
        tarifa_base: float,
        especialidad: str,
        disponible: bool = True
    ):
        super().__init__(
            identificador,
            nombre,
            descripcion,
            tarifa_base,
            disponible
        )

        self._especialidad = (
            especialidad.strip()
            if isinstance(especialidad, str)
            else especialidad
        )

        self.validar()

        logger_sistema.info(
            f"Servicio creado: ID={self.id}, "
            f"Nombre={self.nombre}, Tipo={self.__class__.__name__}"
        )

    @property
    def especialidad(self) -> str:
        return self._especialidad

    def validar(self) -> bool:
        """Valida los datos específicos de la asesoría."""

        self._validar_datos_comunes()

        if not isinstance(self._especialidad, str) or not self._especialidad:
            raise ServicioInvalidoError(
                "La especialidad de la asesoría no puede estar vacía."
            )

        return True

    def calcular_costo(
        self,
        horas: int,
        descuento: float = 0
    ) -> float:
        """Calcula el costo de una asesoría según las horas contratadas."""

        self.verificar_disponibilidad()

        if isinstance(horas, bool) or not isinstance(horas, int) or horas <= 0:
            raise ParametroInvalidoError(
                "Las horas de asesoría deben ser un entero mayor que cero."
            )

        if (
            isinstance(descuento, bool)
            or not isinstance(descuento, (int, float))
            or not math.isfinite(descuento)
            or not 0 <= descuento <= 100
        ):
            raise ParametroInvalidoError(
                "El descuento debe estar entre 0 y 100."
            )

        subtotal = self._tarifa_base * horas
        costo_final = subtotal * (1 - descuento / 100)

        logger_sistema.info(
            f"Calculo realizado: Servicio={self.nombre}, "
            f"Tipo={self.__class__.__name__}, "
            f"Costo={round(costo_final, 2)}"
        )

        return round(costo_final, 2)

    def a_diccionario(self) -> dict:
        """Convierte los datos de la asesoría a un diccionario."""

        return {
            "tipo_servicio": "AsesoriaEspecializada",
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "tarifa_base": self.tarifa_base,
            "disponible": self.disponible,
            "especialidad": self.especialidad,
            "fecha_creacion": self.fecha_creacion.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }
