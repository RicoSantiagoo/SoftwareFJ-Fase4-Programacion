"""
Módulo de la Clase Abstracta Servicio.
Define los contratos polimórficos y la lógica sobrecargada para cálculo de tarifas.
"""

from abc import abstractmethod
from typing import Any, Dict
from src.models.base import EntidadSistema
from src.exceptions.custom_exceptions import ServicioInvalidoError, CalculoFinancieroError


class Servicio(EntidadSistema):
    """
    Clase abstracta que modela los servicios tecnológicos provistos por Software FJ.
    Define las operaciones polimórficas que deben implementar las subclases.
    """

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        """
        Inicializa un servicio base con su código, denominación y tarifa horaria/diaria base.
        """
        super().__init__(id_servicio)

        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El nombre del servicio no puede ser una cadena vacía.")

        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise ServicioInvalidoError(
                "La tarifa base del servicio debe ser un valor numérico estrictamente positivo.",
                detalle=f"Tarifa recibida: {tarifa_base}"
            )

        self._nombre: str = nombre.strip()
        self._tarifa_base: float = float(tarifa_base)
        self._disponible: bool = bool(disponible)

    @property
    def id_servicio(self) -> str:
        """Identificador único del servicio."""
        return self._id

    @property
    def nombre(self) -> str:
        """Nombre descriptivo del servicio."""
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str) -> None:
        """Establece un nuevo nombre para el servicio."""
        if not isinstance(nuevo_nombre, str) or not nuevo_nombre.strip():
            raise ServicioInvalidoError("El nuevo nombre del servicio no puede estar vacío.")
        self._nombre = nuevo_nombre.strip()

    @property
    def tarifa_base(self) -> float:
        """Tarifa base asignada al servicio."""
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, nueva_tarifa: float) -> None:
        """Actualiza la tarifa base garantizando que sea positiva."""
        if not isinstance(nueva_tarifa, (int, float)) or nueva_tarifa <= 0:
            raise ServicioInvalidoError(
                "La nueva tarifa base debe ser un número positivo.",
                detalle=f"Valor recibido: {nueva_tarifa}"
            )
        self._tarifa_base = float(nueva_tarifa)

    @property
    def disponible(self) -> bool:
        """Indica si el servicio está operativo para ser reservado."""
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        """Modifica el estado de disponibilidad del servicio."""
        self._disponible = bool(estado)

    def validar(self) -> bool:
        """Valida las invariantes fundamentales del servicio."""
        if self._tarifa_base <= 0:
            raise ServicioInvalidoError("Inconsistencia en tarifa base: no puede ser menor o igual a cero.")
        return True

    @abstractmethod
    def describir_servicio(self) -> str:
        """
        Método polimórfico: retorna la descripción detallada del servicio y sus especificaciones.
        """
        pass

    @abstractmethod
    def calcular_costo(self, duracion: float, **kwargs) -> float:
        """
        Método polimórfico: calcula el costo bruto del servicio según la duración y atributos específicos.
        """
        pass

    @abstractmethod
    def validar_parametros(self, duracion: float, **kwargs) -> bool:
        """
        Método polimórfico: valida que los parámetros particulares de la solicitud sean congruentes.
        """
        pass

    def calcular_costo_total(
        self,
        duracion: float,
        descuento: float = 0.0,
        impuesto: float = 0.19,
        es_vip: bool = False,
        recargo_adicional: float = 0.0,
        **kwargs
    ) -> float:
        """
        Método sobrecargado (vía parámetros opcionales y flexibles) para calcular el costo liquidado.
        Soporta:
        1. Cálculo estándar: solo duración.
        2. Cálculo con descuento porcentual (0.0 a 1.0).
        3. Cálculo con descuento VIP preferencial (10% adicional).
        4. Cálculo con tasa impositiva parametrizable (IVA por defecto 19%).
        5. Cálculo con recargo complementario.
        """
        # Validación de parámetros numéricos
        if not isinstance(descuento, (int, float)) or not (0.0 <= descuento <= 1.0):
            raise CalculoFinancieroError(
                "El porcentaje de descuento debe estar comprendido en el intervalo [0.0, 1.0].",
                detalle=f"Descuento recibido: {descuento}"
            )

        if not isinstance(impuesto, (int, float)) or impuesto < 0.0:
            raise CalculoFinancieroError(
                "La tasa de impuesto no puede ser negativa.",
                detalle=f"Impuesto recibido: {impuesto}"
            )

        # Invocación polimórfica del costo bruto según el tipo específico de servicio
        costo_bruto = self.calcular_costo(duracion, **kwargs)

        # Aplicación de bonificación adicional si el cliente ostenta estatus VIP
        descuento_aplicable = descuento
        if es_vip:
            descuento_aplicable = min(1.0, descuento_aplicable + 0.10)

        subtotal_con_descuento = costo_bruto * (1.0 - descuento_aplicable)
        subtotal_con_recargo = subtotal_con_descuento + recargo_adicional
        valor_impuesto = subtotal_con_recargo * impuesto
        costo_final = round(subtotal_con_recargo + valor_impuesto, 2)

        if costo_final < 0:
            raise CalculoFinancieroError(
                "El cálculo final del servicio resultó en un valor monetario negativo inadmisible.",
                detalle=f"Costo liquidado: {costo_final}"
            )

        return costo_final

    def a_diccionario(self) -> Dict[str, Any]:
        """Serializa los atributos de la entidad a un diccionario."""
        return {
            "id_servicio": self._id,
            "nombre": self._nombre,
            "tipo_servicio": self.__class__.__name__,
            "tarifa_base": self._tarifa_base,
            "disponible": self._disponible,
            "descripcion": self.describir_servicio()
        }
