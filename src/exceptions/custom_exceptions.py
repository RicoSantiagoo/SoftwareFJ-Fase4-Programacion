"""
Módulo de Excepciones Personalizadas para Software FJ.
Define una jerarquía estructurada de excepciones orientadas al negocio.
"""

from datetime import datetime
from typing import Optional


class SoftwareFJError(Exception):
    """
    Excepción base para todas las anomalías dentro del sistema Software FJ.
    Permite encapsular un mensaje descriptivo, código de error y timestamp.
    """
    def __init__(self, mensaje: str, codigo_error: str = "ERR_GENERICO", detalle: Optional[str] = None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo_error = codigo_error
        self.detalle = detalle
        self.timestamp = datetime.now()

    def __str__(self) -> str:
        base = f"[{self.codigo_error}] {self.mensaje}"
        if self.detalle:
            base += f" (Detalle: {self.detalle})"
        return base


class ValidacionError(SoftwareFJError):
    """Lanzada cuando fallan las validaciones de datos o reglas de negocio."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, codigo_error="ERR_VALIDACION", detalle=detalle)


class ClienteInvalidoError(ValidacionError):
    """Lanzada ante fallos en los datos de un cliente (correo, teléfono, nombre)."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, detalle=detalle)
        self.codigo_error = "ERR_CLIENTE_INVALIDO"


class ServicioInvalidoError(ValidacionError):
    """Lanzada cuando la configuración o parámetros de un servicio son inconsistentes."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, detalle=detalle)
        self.codigo_error = "ERR_SERVICIO_INVALIDO"


class ParametroInvalidoError(ValidacionError):
    """Lanzada cuando un argumento recibido es inválido, fuera de rango o nulo."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, detalle=detalle)
        self.codigo_error = "ERR_PARAMETRO_INVALIDO"


class DisponibilidadError(SoftwareFJError):
    """Lanzada cuando un recurso o servicio solicitado no se encuentra disponible."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, codigo_error="ERR_DISPONIBILIDAD", detalle=detalle)


class ServicioNoDisponibleError(DisponibilidadError):
    """Lanzada específicamente cuando un servicio está deshabilitado o en mantenimiento."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, detalle=detalle)
        self.codigo_error = "ERR_SERVICIO_NO_DISPONIBLE"


class CapacidadExcedidaError(DisponibilidadError):
    """Lanzada cuando se solicita un aforo o cupo mayor al disponible."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, detalle=detalle)
        self.codigo_error = "ERR_CAPACIDAD_EXCEDIDA"


class OperacionNoPermitidaError(SoftwareFJError):
    """Lanzada ante violaciones al flujo de estados u operaciones ilegales."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, codigo_error="ERR_OPERACION_NO_PERMITIDA", detalle=detalle)


class EstadoReservaInvalidoError(OperacionNoPermitidaError):
    """Lanzada cuando se intenta una transición de estado inválida en una reserva."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, detalle=detalle)
        self.codigo_error = "ERR_ESTADO_RESERVA_INVALIDO"


class EntidadNoEncontradaError(OperacionNoPermitidaError):
    """Lanzada cuando una entidad (cliente, servicio, reserva) no existe en la lista."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, detalle=detalle)
        self.codigo_error = "ERR_ENTIDAD_NO_ENCONTRADA"


class CalculoFinancieroError(SoftwareFJError):
    """Lanzada ante inconsistencias en el cálculo de costos, impuestos o descuentos."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, codigo_error="ERR_CALCULO_FINANCIERO", detalle=detalle)
