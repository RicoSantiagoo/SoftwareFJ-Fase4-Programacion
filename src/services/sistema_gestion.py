"""
Módulo de Gestión Central de Software FJ.
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
    ServicioNoDisponibleError,
    EstadoReservaInvalidoError,
    OperacionNoPermitidaError,
    SoftwareFJError
)
from src.utils.logger import logger_sistema, LOG_FILE_PATH


class SistemaGestionFJ:
    """
    Controlador central del sistema. Implementa el patrón Fachada para coordinar
    las operaciones del negocio manteniendo el estado exclusivamente en memoria.
    """

    def __init__(self, nombre_organizacion: str = "Software FJ"):
        """Inicializa las estructuras de datos en memoria y el registro de auditoría."""
        self._nombre_organizacion: str = nombre_organizacion
        self._clientes: List[Cliente] = []
        self._servicios: List[Servicio] = []
        self._reservas: List[Reserva] = []

        logger_sistema.info("=== Sistema de Gestión Integral '%s' Inicializado ===", self._nombre_organizacion)

    # =========================================================================
    # GESTIÓN DE CLIENTES
    # =========================================================================

    def registrar_cliente(
        self,
        id_cliente: str,
        nombre: str,
        correo: str,
        telefono: str,
        es_frecuente: bool = False
    ) -> Cliente:
        """
        Registra un nuevo cliente validando unicidad de ID y consistencia de atributos.
        Aplica estructura: try / except / else / finally.
        """
        logger_sistema.info("Intentando registrar cliente [ID: %s, Nombre: %s]...", id_cliente, nombre)
        cliente_creado = None

        try:
            # 1. Verificar unicidad de ID en la lista interna
            if any(c.id_cliente == id_cliente for c in self._clientes):
                raise ValidacionError(
                    f"Ya existe un cliente registrado con el identificador '{id_cliente}'.",
                    detalle="Violación de regla de unicidad."
                )

            # 2. Instanciación con validación interna
            nuevo_cliente = Cliente(
                id_cliente=id_cliente,
                nombre=nombre,
                correo=correo,
                telefono=telefono,
                es_frecuente=es_frecuente
            )

        except ClienteInvalidoError as error_cliente:
            logger_sistema.warning("Datos inválidos al registrar cliente [%s]: %s", id_cliente, error_cliente)
            raise

        except ValidacionError as error_val:
            logger_sistema.warning("Conflicto de validación de negocio para cliente [%s]: %s", id_cliente, error_val)
            raise

        except Exception as error_inesperado:
            logger_sistema.error("Error imprevisto en registro de cliente [%s]: %s", id_cliente, error_inesperado, exc_info=True)
            raise OperacionNoPermitidaError(
                "Error crítico al intentar registrar al cliente.",
                detalle=str(error_inesperado)
            ) from error_inesperado

        else:
            # Se ejecuta cuando la instanciación y validación resultaron impecables
            self._clientes.append(nuevo_cliente)
            cliente_creado = nuevo_cliente
            logger_sistema.info("Cliente [%s] agregado exitosamente a la lista del sistema.", id_cliente)

        finally:
            total_actual = len(self._clientes)
            logger_sistema.debug("Auditoría Clientes: Registro concluido. Total clientes en memoria: %d.", total_actual)

        return cliente_creado

    def buscar_cliente(self, id_cliente: str) -> Cliente:
        """Busca un cliente por su ID en la lista en memoria o lanza excepción personalizada."""
        for cliente in self._clientes:
            if cliente.id_cliente == id_cliente:
                return cliente
        raise EntidadNoEncontradaError(
            f"El cliente con identificación '{id_cliente}' no se encuentra en el sistema.",
            detalle="Búsqueda infructuosa en lista interna."
        )

    # =========================================================================
    # GESTIÓN DE SERVICIOS
    # =========================================================================

    def agregar_servicio(self, servicio: Servicio) -> Servicio:
        """
        Incorpora un servicio al catálogo interno previa validación.
        """
        try:
            if not isinstance(servicio, Servicio):
                raise ParametroInvalidoError("El elemento debe heredar de la clase abstracta Servicio.")

            if any(s.id_servicio == servicio.id_servicio for s in self._servicios):
                raise ServicioInvalidoError(
                    f"El código de servicio '{servicio.id_servicio}' ya existe en el portafolio.",
                    detalle="Código duplicado."
                )

            servicio.validar()
            self._servicios.append(servicio)
            logger_sistema.info("Servicio [%s - %s] incorporado al portafolio.", servicio.id_servicio, servicio.nombre)
            return servicio

        except (ParametroInvalidoError, ServicioInvalidoError) as error_serv:
            logger_sistema.warning("Rechazo al agregar servicio [%s]: %s", getattr(servicio, "id_servicio", "N/A"), error_serv)
            raise

        except Exception as error_critico:
            logger_sistema.critical("Falla grave agregando servicio: %s", error_critico, exc_info=True)
            raise OperacionNoPermitidaError("Error al registrar servicio en el sistema.") from error_critico

    def buscar_servicio(self, id_servicio: str) -> Servicio:
        """Busca un servicio por su ID o lanza EntidadNoEncontradaError."""
        for servicio in self._servicios:
            if servicio.id_servicio == id_servicio:
                return servicio
        raise EntidadNoEncontradaError(
            f"El servicio con identificador '{id_servicio}' no existe en el catálogo activo.",
            detalle="Servicio no disponible o no registrado."
        )

    # =========================================================================
    # GESTIÓN DE RESERVAS
    # =========================================================================

    def crear_reserva(
        self,
        id_reserva: str,
        id_cliente: str,
        id_servicio: str,
        duracion: float,
        parametros_adicionales: Optional[Dict[str, Any]] = None,
        procesar_inmediatamente: bool = True,
        descuento_promocional: float = 0.0
    ) -> Reserva:
        """
        Orquesta la generación de una reserva conectando cliente y servicio.
        Demuestra encadenamiento de excepciones ('raise ... from ...').
        """
        logger_sistema.info(
            "Creando solicitud de Reserva [%s] para Cliente [%s] con Servicio [%s]...",
            id_reserva, id_cliente, id_servicio
        )

        try:
            # Validar unicidad del identificador de reserva
            if any(r.id == id_reserva for r in self._reservas):
                raise ValidacionError(f"El identificador de reserva '{id_reserva}' ya está ocupado.")

            # Búsqueda de entidades asociadas
            cliente = self.buscar_cliente(id_cliente)
            servicio = self.buscar_servicio(id_servicio)

            # Instanciación de la reserva
            reserva = Reserva(
                id_reserva=id_reserva,
                cliente=cliente,
                servicio=servicio,
                duracion=duracion,
                parametros_adicionales=parametros_adicionales
            )

            # Procesamiento de costos si se solicitó inmediato
            if procesar_inmediatamente:
                reserva.procesar(descuento_base=descuento_promocional)
                reserva.confirmar()

            self._reservas.append(reserva)
            logger_sistema.info("Reserva [%s] creada y registrada exitosamente.", id_reserva)
            return reserva

        except EntidadNoEncontradaError as error_entidad:
            # Encadenamiento explícito de excepción de negocio
            logger_sistema.error("Error de dependencia en reserva [%s]: %s", id_reserva, error_entidad)
            raise OperacionNoPermitidaError(
                f"No es posible crear la reserva [{id_reserva}] porque faltan entidades requeridas.",
                detalle=str(error_entidad)
            ) from error_entidad

        except SoftwareFJError as error_negocio:
            logger_sistema.error("Regla de negocio infringida en reserva [%s]: %s", id_reserva, error_negocio)
            raise

        except Exception as error_general:
            logger_sistema.critical("Error inesperado en creación de reserva [%s]: %s", id_reserva, error_general, exc_info=True)
            raise OperacionNoPermitidaError(
                f"Excepción general no controlada durante la reserva [{id_reserva}].",
                detalle=str(error_general)
            ) from error_general

    def cancelar_reserva(self, id_reserva: str, motivo: str) -> bool:
        """Cancela una reserva existente."""
        for reserva in self._reservas:
            if reserva.id == id_reserva:
                return reserva.cancelar(motivo)
        raise EntidadNoEncontradaError(
            f"No se encontró la reserva con identificador '{id_reserva}' para su cancelación."
        )

    # =========================================================================
    # CONSULTAS Y ESTADÍSTICAS
    # =========================================================================

    def listar_clientes(self) -> List[Dict[str, Any]]:
        return [c.a_diccionario() for c in self._clientes]

    def listar_servicios(self) -> List[Dict[str, Any]]:
        return [s.a_diccionario() for s in self._servicios]

    def listar_reservas(self) -> List[Dict[str, Any]]:
        return [r.a_diccionario() for r in self._reservas]

    def obtener_resumen_operativo(self) -> Dict[str, Any]:
        """Calcula métricas globales de la operación en memoria."""
        total_ingresos = sum(r.costo_total for r in self._reservas if r.estado in ("CONFIRMADA", "COMPLETADA"))
        conteo_por_estado = {
            "CREADA": sum(1 for r in self._reservas if r.estado == "CREADA"),
            "CONFIRMADA": sum(1 for r in self._reservas if r.estado == "CONFIRMADA"),
            "CANCELADA": sum(1 for r in self._reservas if r.estado == "CANCELADA"),
            "COMPLETADA": sum(1 for r in self._reservas if r.estado == "COMPLETADA")
        }

        return {
            "total_clientes": len(self._clientes),
            "total_servicios": len(self._servicios),
            "total_reservas": len(self._reservas),
            "ingresos_facturados": round(total_ingresos, 2),
            "distribucion_estados": conteo_por_estado
        }

    @staticmethod
    def leer_ultimos_logs(lineas: int = 25) -> List[str]:
        """Lee y devuelve las últimas líneas del archivo de logs para auditoría."""
        try:
            with open(LOG_FILE_PATH, mode="r", encoding="utf-8") as archivo_log:
                todas_lineas = archivo_log.readlines()
                return todas_lineas[-lineas:] if len(todas_lineas) >= lineas else todas_lineas
        except FileNotFoundError:
            return ["El archivo de logs no existe aún."]
