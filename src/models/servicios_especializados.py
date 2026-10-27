"""
Módulo de Servicios Especializados de Software FJ.
Implementa las clases concretas que heredan de Servicio, evidenciando polimorfismo,
sobreescritura de métodos y validaciones específicas de cada unidad de negocio.
"""

from typing import Any, Dict
from src.models.servicio import Servicio
from src.exceptions.custom_exceptions import (
    ParametroInvalidoError,
    CapacidadExcedidaError,
    ServicioInvalidoError,
)


class ReservaSala(Servicio):
    """
    Servicio especializado en la asignación y gestión de salas físicas corporativas.
    """

    FACTORES_TIPO_SALA = {
        "reuniones": 1.0,
        "capacitacion": 1.25,
        "conferencias": 1.50
    }

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        tarifa_base_hora: float,
        capacidad_maxima: int,
        tipo_sala: str = "reuniones",
        incluye_proyector: bool = True,
        disponible: bool = True
    ):
        """Inicializa la sala con capacidades físicas y dotación audiovisual."""
        super().__init__(id_servicio, nombre, tarifa_base_hora, disponible)

        if not isinstance(capacidad_maxima, int) or capacidad_maxima <= 0:
            raise ServicioInvalidoError(
                "La capacidad máxima de la sala debe ser un entero positivo.",
                detalle=f"Capacidad recibida: {capacidad_maxima}"
            )

        tipo_normalizado = tipo_sala.lower().strip()
        if tipo_normalizado not in self.FACTORES_TIPO_SALA:
            raise ServicioInvalidoError(
                f"El tipo de sala '{tipo_sala}' no es válido. Opciones: {list(self.FACTORES_TIPO_SALA.keys())}"
            )

        self._capacidad_maxima: int = capacidad_maxima
        self._tipo_sala: str = tipo_normalizado
        self._incluye_proyector: bool = bool(incluye_proyector)

    @property
    def capacidad_maxima(self) -> int:
        return self._capacidad_maxima

    @property
    def tipo_sala(self) -> str:
        return self._tipo_sala

    @property
    def incluye_proyector(self) -> bool:
        return self._incluye_proyector

    def describir_servicio(self) -> str:
        """Sobrescritura polimórfica de descripción."""
        audiovisual = "Con proyector 4K y sonido" if self._incluye_proyector else "Básica sin proyección"
        return (
            f"Sala de {self._tipo_sala.title()} '{self._nombre}' | Capacidad: {self._capacidad_maxima} personas | "
            f"Dotación: {audiovisual} | Tarifa: ${self._tarifa_base:,.2f}/hora"
        )

    def validar_parametros(self, duracion: float, **kwargs) -> bool:
        """Valida que la duración en horas y el número de asistentes respeten los límites de la sala."""
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ParametroInvalidoError(
                "La duración de la reserva de sala debe ser mayor a 0 horas.",
                detalle=f"Duración: {duracion}"
            )

        if duracion > 12:
            raise ParametroInvalidoError(
                "No se permite reservar una sala por más de 12 horas continuas por política interna.",
                detalle=f"Horas solicitadas: {duracion}"
            )

        asistentes = kwargs.get("asistentes", 1)
        if not isinstance(asistentes, int) or asistentes <= 0:
            raise ParametroInvalidoError(
                "La cantidad de asistentes debe ser un número entero mayor a cero.",
                detalle=f"Asistentes recibidos: {asistentes}"
            )

        if asistentes > self._capacidad_maxima:
            raise CapacidadExcedidaError(
                f"El aforo solicitado ({asistentes} personas) sobrepasa la capacidad máxima ({self._capacidad_maxima} personas).",
                detalle=f"Sala: {self._nombre}"
            )

        return True

    def calcular_costo(self, duracion: float, **kwargs) -> float:
        """Cálculo específico de costo horario ponderado por tipo de sala y accesorios."""
        self.validar_parametros(duracion, **kwargs)
        factor = self.FACTORES_TIPO_SALA.get(self._tipo_sala, 1.0)
        costo_base = self._tarifa_base * duracion * factor
        costo_adicionales = 25000.0 if self._incluye_proyector else 0.0
        return round(costo_base + costo_adicionales, 2)


class AlquilerEquipo(Servicio):
    """
    Servicio de arrendamiento de hardware tecnológico especializado por días.
    """

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        tarifa_base_dia: float,
        tipo_equipo: str,
        deposito_garantia: float = 150000.0,
        tarifa_seguro_diario: float = 20000.0,
        disponible: bool = True
    ):
        """Inicializa los términos de arrendamiento de equipo."""
        super().__init__(id_servicio, nombre, tarifa_base_dia, disponible)

        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ServicioInvalidoError("El tipo de equipo no puede ser vacío.")

        if deposito_garantia < 0 or tarifa_seguro_diario < 0:
            raise ServicioInvalidoError("El depósito y seguro deben ser valores no negativos.")

        self._tipo_equipo: str = tipo_equipo.strip()
        self._deposito_garantia: float = float(deposito_garantia)
        self._tarifa_seguro_diario: float = float(tarifa_seguro_diario)

    @property
    def tipo_equipo(self) -> str:
        return self._tipo_equipo

    @property
    def deposito_garantia(self) -> float:
        return self._deposito_garantia

    def describir_servicio(self) -> str:
        """Sobrescritura polimórfica de descripción."""
        return (
            f"Alquiler de {self._tipo_equipo.title()} '{self._nombre}' | "
            f"Tarifa: ${self._tarifa_base:,.2f}/día | Depósito Garantía: ${self._deposito_garantia:,.2f}"
        )

    def validar_parametros(self, duracion: float, **kwargs) -> bool:
        """Valida que los días de alquiler sean coherentes (mínimo 1 día, máximo 30 días)."""
        if not isinstance(duracion, (int, float)) or duracion < 1:
            raise ParametroInvalidoError(
                "El alquiler de equipo requiere un plazo mínimo de 1 día entero.",
                detalle=f"Días solicitados: {duracion}"
            )
        if duracion > 30:
            raise ParametroInvalidoError(
                "El alquiler individual de equipo no puede superar 30 días calendario continuos.",
                detalle=f"Días solicitados: {duracion}"
            )
        return True

    def calcular_costo(self, duracion: float, **kwargs) -> float:
        """Calcula el canon de arrendamiento multiplicando tarifa diaria e incluyendo cobertura de seguro."""
        self.validar_parametros(duracion, **kwargs)
        incluir_seguro = kwargs.get("incluir_seguro", True)
        seguro_total = (self._tarifa_seguro_diario * duracion) if incluir_seguro else 0.0
        return round((self._tarifa_base * duracion) + seguro_total, 2)


class AsesoriaEspecializada(Servicio):
    """
    Servicio de consultoría tecnológica especializada por horas brindada por expertos.
    """

    MULTIPLICADORES_NIVEL = {
        "junior": 1.0,
        "senior": 1.75,
        "master": 2.50
    }

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        tarifa_base_hora: float,
        area_especialidad: str,
        nivel_consultor: str = "senior",
        consultor_asignado: str = "Ing. Especialista Asignado",
        disponible: bool = True
    ):
        """Inicializa el servicio de consultoría con el perfil del especialista."""
        super().__init__(id_servicio, nombre, tarifa_base_hora, disponible)

        nivel_normalizado = nivel_consultor.lower().strip()
        if nivel_normalizado not in self.MULTIPLICADORES_NIVEL:
            raise ServicioInvalidoError(
                f"Nivel de consultor inválido: '{nivel_consultor}'. Opciones: {list(self.MULTIPLICADORES_NIVEL.keys())}"
            )

        self._area_especialidad: str = area_especialidad.strip()
        self._nivel_consultor: str = nivel_normalizado
        self._consultor_asignado: str = consultor_asignado.strip()

    @property
    def area_especialidad(self) -> str:
        return self._area_especialidad

    @property
    def nivel_consultor(self) -> str:
        return self._nivel_consultor

    @property
    def consultor_asignado(self) -> str:
        return self._consultor_asignado

    def describir_servicio(self) -> str:
        """Sobrescritura polimórfica de descripción."""
        return (
            f"Asesoría en {self._area_especialidad} '{self._nombre}' | Consultor {self._nivel_consultor.upper()}: "
            f"{self._consultor_asignado} | Tarifa Base: ${self._tarifa_base:,.2f}/hora"
        )

    def validar_parametros(self, duracion: float, **kwargs) -> bool:
        """Valida que las horas de asesoría estén en el rango de 1 a 40 horas."""
        if not isinstance(duracion, (int, float)) or duracion < 1:
            raise ParametroInvalidoError(
                "La duración mínima para una sesión de asesoría es de 1 hora.",
                detalle=f"Horas indicadas: {duracion}"
            )
        if duracion > 40:
            raise ParametroInvalidoError(
                "Una reserva de asesoría no puede exceder 40 horas en un único bloque de contratación.",
                detalle=f"Horas indicadas: {duracion}"
            )
        return True

    def calcular_costo(self, duracion: float, **kwargs) -> float:
        """Calcula el costo en base a las horas, nivel del consultor y recargo de urgencia opcional."""
        self.validar_parametros(duracion, **kwargs)
        multiplicador = self.MULTIPLICADORES_NIVEL.get(self._nivel_consultor, 1.0)
        es_urgente = kwargs.get("es_urgente", False)
        recargo_urgencia = 1.30 if es_urgente else 1.0

        costo_hora_ajustado = self._tarifa_base * multiplicador * recargo_urgencia
        return round(costo_hora_ajustado * duracion, 2)
