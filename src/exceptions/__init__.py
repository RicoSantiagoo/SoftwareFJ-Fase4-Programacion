"""Módulo de excepciones personalizadas."""
from src.exceptions.custom_exceptions import (
    SoftwareFJError,
    ValidacionError,
    ClienteInvalidoError,
    ServicioInvalidoError,
    ParametroInvalidoError,
    DisponibilidadError,
    ServicioNoDisponibleError,
    CapacidadExcedidaError,
    OperacionNoPermitidaError,
    EstadoReservaInvalidoError,
    EntidadNoEncontradaError,
    CalculoFinancieroError,
)

__all__ = [
    "SoftwareFJError",
    "ValidacionError",
    "ClienteInvalidoError",
    "ServicioInvalidoError",
    "ParametroInvalidoError",
    "DisponibilidadError",
    "ServicioNoDisponibleError",
    "CapacidadExcedidaError",
    "OperacionNoPermitidaError",
    "EstadoReservaInvalidoError",
    "EntidadNoEncontradaError",
    "CalculoFinancieroError",
]
