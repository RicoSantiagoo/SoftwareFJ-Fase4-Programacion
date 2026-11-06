"""
Jerarquía de Excepciones Personalizadas para Software FJ
Estudiante: Santiago Rico Hernández
Curso: Programación (213023) - UNAD - Fase 4
"""

from typing import Optional


class SoftwareFJError(Exception):
    """Excepción raíz del proyecto Software FJ."""
    def __init__(self, mensaje: str, codigo_error: str = "ERR_SISTEMA", detalle: Optional[str] = None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo_error = codigo_error
        self.detalle = detalle

    def __str__(self) -> str:
        if self.detalle:
            return f"[{self.codigo_error}] {self.mensaje} - Detalle: {self.detalle}"
        return f"[{self.codigo_error}] {self.mensaje}"


# --- Errores de Validación ---
class ValidacionError(SoftwareFJError):
    """Error general cuando un dato no cumple las condiciones del negocio."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, codigo_error="ERR_VALIDACION", detalle=detalle)


class ClienteInvalidoError(ValidacionError):
    """Error específico para datos incorrectos de un cliente."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, detalle=detalle)
        self.codigo_error = "ERR_CLIENTE_INVALIDO"


class ServicioInvalidoError(ValidacionError):
    """Error para configuraciones no permitidas en un servicio."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, detalle=detalle)
        self.codigo_error = "ERR_SERVICIO_INVALIDO"


class ParametroInvalidoError(ValidacionError):
    """Error cuando se envía un valor nulo o fuera de rango."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, detalle=detalle)
        self.codigo_error = "ERR_PARAMETRO_INVALIDO"


# --- Errores de Disponibilidad y Capacidad ---
class DisponibilidadError(SoftwareFJError):
    """Error cuando un servicio o sala no está disponible."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, codigo_error="ERR_DISPONIBILIDAD", detalle=detalle)


class ServicioNoDisponibleError(DisponibilidadError):
    """Lanzada cuando un servicio está desactivado en catálogo."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, detalle=detalle)
        self.codigo_error = "ERR_SERVICIO_NO_DISPONIBLE"


class CapacidadExcedidaError(DisponibilidadError):
    """Lanzada si el aforo solicitado supera la capacidad máxima de la sala."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, detalle=detalle)
        self.codigo_error = "ERR_CAPACIDAD_EXCEDIDA"


# --- Errores de Operación y Transición de Estados ---
class OperacionNoPermitidaError(SoftwareFJError):
    """Lanzada para operaciones que violan el flujo normal del sistema."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, codigo_error="ERR_OPERACION_NO_PERMITIDA", detalle=detalle)


class EstadoReservaInvalidoError(OperacionNoPermitidaError):
    """Lanzada si se intenta una acción sobre una reserva en un estado que no lo permite."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, detalle=detalle)
        self.codigo_error = "ERR_ESTADO_RESERVA_INVALIDO"


class EntidadNoEncontradaError(OperacionNoPermitidaError):
    """Lanzada cuando no se encuentra un cliente, servicio o reserva por su ID."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, detalle=detalle)
        self.codigo_error = "ERR_NO_ENCONTRADO"


class CalculoFinancieroError(SoftwareFJError):
    """Lanzada ante incongruencias en liquidación de precios, tarifas o IVA."""
    def __init__(self, mensaje: str, detalle: Optional[str] = None):
        super().__init__(mensaje, codigo_error="ERR_CALCULO_FINANCIERO", detalle=detalle)
