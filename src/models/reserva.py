"""
Módulo del Modelo Reserva.
Integra Cliente y Servicio, orquestando confirmación, cancelación y procesamiento con excepciones.
"""

from typing import Any, Dict, Optional
from datetime import datetime
from src.models.base import EntidadSistema
from src.models.cliente import Cliente
from src.models.servicio import Servicio
from src.exceptions.custom_exceptions import (
    ParametroInvalidoError,
    EstadoReservaInvalidoError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
    SoftwareFJError,
)
from src.utils.logger import logger_sistema


class Reserva(EntidadSistema):
    """
    Clase que consolida el vínculo contractual entre un Cliente y un Servicio ofertado.
    Administra la máquina de estados de la reserva y audita cada transición mediante logs.
    """

    ESTADOS_VALIDOS = ("CREADA", "CONFIRMADA", "CANCELADA", "COMPLETADA")

    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion: float,
        parametros_adicionales: Optional[Dict[str, Any]] = None
    ):
        """
        Inicializa una reserva en estado inicial CREADA.
        """
        super().__init__(id_reserva)

        if not isinstance(cliente, Cliente):
            raise ParametroInvalidoError("El cliente asociado debe ser una instancia válida de la clase Cliente.")

        if not isinstance(servicio, Servicio):
            raise ParametroInvalidoError("El servicio asociado debe ser una instancia derivada de la clase Servicio.")

        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ParametroInvalidoError(
                "La duración de la reserva debe ser un número estrictamente positivo.",
                detalle=f"Duración recibida: {duracion}"
            )

        self._cliente: Cliente = cliente
        self._servicio: Servicio = servicio
        self._duracion: float = float(duracion)
        self._parametros_adicionales: Dict[str, Any] = parametros_adicionales or {}
        self._estado: str = "CREADA"
        self._costo_total: float = 0.0
        self._motivo_cancelacion: Optional[str] = None
        self._fecha_confirmacion: Optional[datetime] = None

        logger_sistema.info(
            "Instancia de Reserva [%s] inicializada para Cliente [%s] y Servicio [%s].",
            self._id, self._cliente.id_cliente, self._servicio.id_servicio
        )

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def duracion(self) -> float:
        return self._duracion

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    @property
    def motivo_cancelacion(self) -> Optional[str]:
        return self._motivo_cancelacion

    def validar(self) -> bool:
        """Verifica la coherencia entre cliente, servicio y estado actual."""
        if self._estado not in self.ESTADOS_VALIDOS:
            raise EstadoReservaInvalidoError(
                f"El estado '{self._estado}' no pertenece a los estados autorizados {self.ESTADOS_VALIDOS}."
            )
        return True

    def procesar(self, descuento_base: float = 0.0, impuesto: float = 0.19) -> float:
        """
        Procesa el cálculo financiero de la reserva empleando manejo robusto de excepciones:
        Estructura: try / except / else / finally con encadenamiento de excepciones.
        """
        logger_sistema.info("Iniciando procesamiento y liquidación para la Reserva [%s]...", self._id)
        operacion_exitosa = False

        try:
            # 1. Validación de disponibilidad del servicio
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self._servicio.nombre}' está marcado como no disponible en catálogo.",
                    detalle=f"ID Servicio: {self._servicio.id_servicio}"
                )

            # 2. Validación de parámetros específicos del servicio
            self._servicio.validar_parametros(self._duracion, **self._parametros_adicionales)

            # 3. Cálculo financiero sobrecargado aprovechando polimorfismo y beneficios VIP del cliente
            self._costo_total = self._servicio.calcular_costo_total(
                duracion=self._duracion,
                descuento=descuento_base,
                impuesto=impuesto,
                es_vip=self._cliente.es_frecuente,
                **self._parametros_adicionales
            )

        except (SoftwareFJError, ValueError) as error_origen:
            # Encadenamiento explícito de excepciones (raise ... from ...)
            mensaje = f"Fallo durante el procesamiento de la Reserva [{self._id}]: {str(error_origen)}"
            logger_sistema.error(mensaje, exc_info=True)
            raise OperacionNoPermitidaError(
                f"No se pudo completar el procesamiento de la reserva debido a inconsistencias operativas.",
                detalle=str(error_origen)
            ) from error_origen

        else:
            # Se ejecuta únicamente si no se presentó ninguna excepción
            operacion_exitosa = True
            logger_sistema.info(
                "Procesamiento exitoso de Reserva [%s]. Costo total liquidado: $%.2f (VIP: %s)",
                self._id, self._costo_total, self._cliente.es_frecuente
            )

        finally:
            # Garantiza auditoría y cierre del ciclo de procesamiento
            estado_resultado = "EXITOSO" if operacion_exitosa else "FALLIDO"
            logger_sistema.debug("Finalizado ciclo de procesamiento para Reserva [%s]. Resultado: %s", self._id, estado_resultado)

        return self._costo_total

    def confirmar(self) -> bool:
        """
        Confirma la reserva tras verificar que no se encuentre cancelada o finalizada.
        """
        if self._estado == "CONFIRMADA":
            logger_sistema.warning("La reserva [%s] ya se encontraba en estado CONFIRMADA.", self._id)
            return True

        if self._estado in ("CANCELADA", "COMPLETADA"):
            raise EstadoReservaInvalidoError(
                f"No es posible confirmar la reserva [{self._id}] porque se encuentra en estado '{self._estado}'.",
                detalle=f"Estado actual: {self._estado}"
            )

        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                f"Imposible confirmar reserva: el servicio [{self._servicio.id_servicio}] no está disponible."
            )

        # Si aún no ha sido procesada financieramente, se procesa
        if self._costo_total <= 0:
            self.procesar()

        self._estado = "CONFIRMADA"
        self._fecha_confirmacion = datetime.now()
        logger_sistema.info("Reserva [%s] confirmada satisfactoriamente.", self._id)
        return True

    def cancelar(self, motivo: str) -> bool:
        """
        Cancela la reserva registrando el motivo justificado.
        Utiliza try / finally para garantizar el registro del evento en logs ante cualquier situación.
        """
        cancelado_correctamente = False
        try:
            if not isinstance(motivo, str) or not motivo.strip():
                raise ParametroInvalidoError("Se debe suministrar un motivo explícito para cancelar la reserva.")

            if self._estado == "CANCELADA":
                raise EstadoReservaInvalidoError(
                    f"La reserva [{self._id}] ya fue cancelada previamente.",
                    detalle=f"Motivo previo: {self._motivo_cancelacion}"
                )

            if self._estado == "COMPLETADA":
                raise EstadoReservaInvalidoError(
                    f"No se puede cancelar una reserva que ya ha sido COMPLETADA y prestada.",
                    detalle=f"ID Reserva: {self._id}"
                )

            self._estado = "CANCELADA"
            self._motivo_cancelacion = motivo.strip()
            cancelado_correctamente = True

        except Exception as exc:
            logger_sistema.error("Error al intentar cancelar la Reserva [%s]: %s", self._id, str(exc))
            raise

        finally:
            if cancelado_correctamente:
                logger_sistema.info(
                    "Reserva [%s] CANCELADA con éxito. Motivo: '%s'.",
                    self._id, self._motivo_cancelacion
                )
            else:
                logger_sistema.warning("Intento de cancelación fallido para la Reserva [%s].", self._id)

        return cancelado_correctamente

    def completar(self) -> bool:
        """Marca la reserva como ejecutada y completada."""
        if self._estado != "CONFIRMADA":
            raise EstadoReservaInvalidoError(
                f"Solo las reservas CONFIRMADAS pueden ser marcadas como COMPLETADAS (estado actual: '{self._estado}')."
            )
        self._estado = "COMPLETADA"
        logger_sistema.info("Reserva [%s] marcada como COMPLETADA exitosamente.", self._id)
        return True

    def a_diccionario(self) -> Dict[str, Any]:
        """Serializa la reserva a diccionario."""
        return {
            "id_reserva": self._id,
            "id_cliente": self._cliente.id_cliente,
            "nombre_cliente": self._cliente.nombre,
            "id_servicio": self._servicio.id_servicio,
            "nombre_servicio": self._servicio.nombre,
            "duracion": self._duracion,
            "estado": self._estado,
            "costo_total": self._costo_total,
            "motivo_cancelacion": self._motivo_cancelacion,
            "fecha_creacion": self._fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __str__(self) -> str:
        return (
            f"Reserva [{self._id}] | Estado: {self._estado} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | Duración: {self._duracion} | Total: ${self._costo_total:,.2f}"
        )
