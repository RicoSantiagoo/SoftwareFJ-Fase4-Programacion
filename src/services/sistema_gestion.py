"""
Módulo 5 - Orquestador Central del Sistema (Software FJ)
Autor: Santiago Rico Hernández - Líder de Repositorio
Proyecto: Software FJ - Fase 4 (Programación UNAD)

Administra en memoria (mediante listas nativas, sin bases de datos) las entidades de
clientes, servicios y reservas, coordinando validaciones, logging y captura de excepciones.
"""

from typing import List, Optional, Dict, Any
from src.models.cliente import Cliente
from src.models.servicio import Servicio
from src.models.reserva import Reserva
from src.exceptions.custom_exceptions import (
    ValidacionError,
    ClienteInvalidoError,
    ServicioInvalidoError,
    ParametroInvalidoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
    SoftwareFJError
)
from src.utils.logger import logger_sistema, LOG_FILE_PATH


class SistemaGestionFJ:
    """
    Controlador central del sistema (Patrón Fachada / Orquestador).
    Coordina las operaciones de negocio manteniendo el estado 100% en memoria.
    """

    def __init__(self, nombre_organizacion: str = "Software FJ S.A.S."):
        self._nombre_organizacion: str = nombre_organizacion
        self._clientes: List[Cliente] = []
        self._servicios: List[Servicio] = []
        self._reservas: List[Reserva] = []

        logger_sistema.info(
            "=== Orquestador '%s' Inicializado en Memoria ===",
            self._nombre_organizacion
        )

    # -------------------------------------------------------------------------
    # PROPIEDADES DE ACCESO
    # -------------------------------------------------------------------------
    @property
    def total_clientes(self) -> int:
        return len(self._clientes)

    @property
    def total_servicios(self) -> int:
        return len(self._servicios)

    @property
    def total_reservas(self) -> int:
        return len(self._reservas)

    # -------------------------------------------------------------------------
    # GESTIÓN DE CLIENTES EN MEMORIA
    # -------------------------------------------------------------------------
    def registrar_cliente(
        self,
        id_cliente: str,
        nombre: str,
        correo: str,
        telefono: str,
        es_frecuente: bool = False
    ) -> Cliente:
        """
        Registra un nuevo cliente con validación de unicidad de ID y captura controlada.
        Aplica estructura: try / except / else / finally.
        """
        logger_sistema.info(
            "Intentando registrar cliente [ID: %s, Nombre: %s]...",
            id_cliente, nombre
        )
        cliente_creado = None

        try:
            # 1. Unicidad de ID en memoria
            if any(c.id_cliente == id_cliente for c in self._clientes):
                raise ValidacionError(
                    f"Ya existe un cliente registrado con el identificador '{id_cliente}'.",
                    detalle="Violación de regla de unicidad."
                )

            # 2. Instanciación con validaciones internas
            nuevo_cliente = Cliente(
                id_cliente=id_cliente,
                nombre=nombre,
                correo=correo,
                telefono=telefono,
                es_frecuente=es_frecuente
            )

        except ClienteInvalidoError as err_cliente:
            logger_sistema.warning(
                "Datos inválidos al registrar cliente [%s]: %s",
                id_cliente, err_cliente
            )
            raise

        except ValidacionError as err_val:
            logger_sistema.warning(
                "Conflicto de unicidad para cliente [%s]: %s",
                id_cliente, err_val
            )
            raise

        except Exception as err_inesperado:
            logger_sistema.error(
                "Falla imprevista en registro de cliente [%s]: %s",
                id_cliente, err_inesperado, exc_info=True
            )
            raise OperacionNoPermitidaError(
                "Error crítico al registrar cliente en memoria.",
                detalle=str(err_inesperado)
            ) from err_inesperado

        else:
            self._clientes.append(nuevo_cliente)
            cliente_creado = nuevo_cliente
            logger_sistema.info(
                "Cliente [%s] registrado exitosamente en memoria.",
                id_cliente
            )

        finally:
            logger_sistema.debug(
                "Auditoría: Registro finalizado. Total clientes: %d.",
                len(self._clientes)
            )

        return cliente_creado

    def buscar_cliente(self, id_cliente: str) -> Cliente:
        """Busca un cliente por su ID o lanza EntidadNoEncontradaError."""
        for cliente in self._clientes:
            if cliente.id_cliente == id_cliente:
                return cliente
        raise EntidadNoEncontradaError(
            f"El cliente con ID '{id_cliente}' no se encuentra registrado.",
            detalle="Búsqueda infructuosa en lista de clientes en memoria."
        )

    # -------------------------------------------------------------------------
    # GESTIÓN DE SERVICIOS EN MEMORIA
    # -------------------------------------------------------------------------
    def agregar_servicio(self, servicio: Servicio) -> Servicio:
        """Incorpora un servicio al catálogo en memoria previa validación."""
        if not isinstance(servicio, Servicio):
            raise ParametroInvalidoError(
                "El elemento a registrar debe ser una instancia derivada de Servicio."
            )

        if any(s.id == servicio.id for s in self._servicios):
            raise ServicioInvalidoError(
                f"El código de servicio '{servicio.id}' ya existe en el catálogo.",
                detalle="Identificador de servicio duplicado."
            )

        servicio.validar()
        self._servicios.append(servicio)
        logger_sistema.info(
            "Servicio [%s - %s] agregado al catálogo en memoria.",
            servicio.id, servicio.nombre
        )
        return servicio

    def buscar_servicio(self, id_servicio: str) -> Servicio:
        """Busca un servicio por su ID o lanza EntidadNoEncontradaError."""
        for servicio in self._servicios:
            if servicio.id == id_servicio:
                return servicio
        raise EntidadNoEncontradaError(
            f"El servicio con ID '{id_servicio}' no se encuentra en el catálogo.",
            detalle="Servicio no disponible o no registrado."
        )

    # -------------------------------------------------------------------------
    # GESTIÓN DE RESERVAS EN MEMORIA
    # -------------------------------------------------------------------------
    def crear_reserva(
        self,
        id_reserva: str,
        id_cliente: str,
        id_servicio: str,
        fecha: str,
        hora: str
    ) -> Reserva:
        """
        Orquesta la vinculación de un cliente y un servicio en una reserva.
        """
        logger_sistema.info(
            "Orquestando Reserva [%s]: Cliente [%s] -> Servicio [%s]...",
            id_reserva, id_cliente, id_servicio
        )

        # 1. Unicidad de reserva
        if any(r.id_reserva == id_reserva for r in self._reservas):
            raise ValidacionError(
                f"La reserva con identificador '{id_reserva}' ya existe en memoria."
            )

        # 2. Búsqueda y validación de existencia de cliente y servicio
        cliente = self.buscar_cliente(id_cliente)
        servicio = self.buscar_servicio(id_servicio)

        # 3. Creación de reserva vinculada
        nueva_reserva = Reserva(
            id_reserva=id_reserva,
            cliente=cliente.nombre,
            servicio=servicio.nombre,
            fecha=fecha,
            hora=hora,
            estado="pendiente"
        )

        self._reservas.append(nueva_reserva)
        logger_sistema.info(
            "Reserva [%s] registrada exitosamente en memoria.",
            id_reserva
        )
        return nueva_reserva

    def buscar_reserva(self, id_reserva: str) -> Reserva:
        """Busca una reserva por su ID o lanza EntidadNoEncontradaError."""
        for reserva in self._reservas:
            if reserva.id_reserva == id_reserva:
                return reserva
        raise EntidadNoEncontradaError(
            f"La reserva con ID '{id_reserva}' no existe en memoria."
        )

    def confirmar_reserva(self, id_reserva: str) -> str:
        """Confirma una reserva registrada."""
        reserva = self.buscar_reserva(id_reserva)
        resultado = reserva.confirmar()
        logger_sistema.info("Reserva [%s] confirmada en sistema.", id_reserva)
        return resultado

    def cancelar_reserva(self, id_reserva: str) -> str:
        """Cancela una reserva registrada."""
        reserva = self.buscar_reserva(id_reserva)
        resultado = reserva.cancelar()
        logger_sistema.info("Reserva [%s] cancelada en sistema.", id_reserva)
        return resultado

    # -------------------------------------------------------------------------
    # RESUMEN OPERATIVO Y ESTADÍSTICAS
    # -------------------------------------------------------------------------
    def obtener_resumen_operativo(self) -> Dict[str, Any]:
        """Devuelve las métricas consolidadas del sistema en memoria."""
        conteo_estados = {
            "pendiente": sum(1 for r in self._reservas if r.estado == "pendiente"),
            "confirmada": sum(1 for r in self._reservas if r.estado == "confirmada"),
            "cancelada": sum(1 for r in self._reservas if r.estado == "cancelada")
        }

        return {
            "organizacion": self._nombre_organizacion,
            "total_clientes": len(self._clientes),
            "total_servicios": len(self._servicios),
            "total_reservas": len(self._reservas),
            "distribucion_estados": conteo_estados
        }
