
"""
Pruebas unitarias del Modulo 3 - Catalogo de Servicios
Proyecto: SoftwareFJ - Fase 4
Responsable: Andres Felipe Nieves Leon
"""

import unittest
from inspect import isabstract

from src.models.servicio import (
    Servicio,
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada
)

from src.exceptions.custom_exceptions import (
    ServicioInvalidoError,
    ParametroInvalidoError,
    CapacidadExcedidaError,
    ServicioNoDisponibleError,
    CalculoFinancieroError
)


class TestServicios(unittest.TestCase):
    """Pruebas de las clases del catalogo de servicios."""

    def test_servicio_es_clase_abstracta(self):
        """Verifica que Servicio no pueda instanciarse directamente."""
        self.assertTrue(isabstract(Servicio))

    def test_crear_reserva_sala_correctamente(self):
        """Verifica la creación de una sala con datos válidos."""
        sala = ReservaSala(
            "S001", "Sala reuniones",
            "Sala empresarial", 50000, 20
        )

        self.assertEqual(sala.id, "S001")
        self.assertEqual(sala.nombre, "Sala reuniones")
        self.assertEqual(sala.capacidad_maxima, 20)
        self.assertTrue(sala.validar())

    def test_calcular_costo_reserva_sala(self):
        """Verifica el cálculo del costo de una sala."""
        sala = ReservaSala(
            "S002", "Sala reuniones",
            "Sala empresarial", 50000, 20
        )

        self.assertEqual(sala.calcular_costo(3, 15, 10), 135000)

    def test_capacidad_sala_excedida(self):
        """Verifica que no se supere la capacidad máxima."""
        sala = ReservaSala(
            "S003", "Sala pequeña",
            "Sala empresarial", 50000, 20
        )

        with self.assertRaises(CapacidadExcedidaError):
            sala.calcular_costo(3, 25)

    def test_crear_alquiler_equipo_correctamente(self):
        """Verifica la creación de un alquiler de equipo."""
        equipo = AlquilerEquipo(
            "E001", "Alquiler equipos",
            "Equipos tecnologicos", 40000, "Computador"
        )

        self.assertEqual(equipo.equipo, "Computador")
        self.assertTrue(equipo.validar())

    def test_calcular_costo_alquiler_equipo(self):
        """Verifica el cálculo del alquiler por días y unidades."""
        equipo = AlquilerEquipo(
            "E002", "Alquiler equipos",
            "Equipos tecnologicos", 40000, "Computador"
        )

        self.assertEqual(equipo.calcular_costo(3, 2, 10), 216000)

    def test_cantidad_alquiler_invalida(self):
        """Verifica que no se acepten cantidades menores que uno."""
        equipo = AlquilerEquipo(
            "E003", "Alquiler equipos",
            "Equipos tecnologicos", 40000, "Computador"
        )

        with self.assertRaises(ParametroInvalidoError):
            equipo.calcular_costo(3, 0)

    def test_crear_asesoria_correctamente(self):
        """Verifica la creación de una asesoría especializada."""
        asesoria = AsesoriaEspecializada(
            "A001", "Asesoria programacion",
            "Orientacion en software", 60000, "Programacion"
        )

        self.assertEqual(asesoria.especialidad, "Programacion")
        self.assertTrue(asesoria.validar())

    def test_calcular_costo_asesoria(self):
        """Verifica el cálculo del costo de una asesoría."""
        asesoria = AsesoriaEspecializada(
            "A002", "Asesoria programacion",
            "Orientacion en software", 60000, "Programacion"
        )

        self.assertEqual(asesoria.calcular_costo(4, 5), 228000)

    def test_descuento_fuera_de_rango(self):
        """Verifica que no se permita un descuento superior al 100%."""
        asesoria = AsesoriaEspecializada(
            "A003", "Asesoria programacion",
            "Orientacion en software", 60000, "Programacion"
        )

        with self.assertRaises(ParametroInvalidoError):
            asesoria.calcular_costo(4, 101)

    def test_servicio_no_disponible(self):
        """Verifica que no se pueda calcular un servicio desactivado."""
        sala = ReservaSala(
            "S004", "Sala no disponible",
            "Sala empresarial", 50000, 20, False
        )

        with self.assertRaises(ServicioNoDisponibleError):
            sala.calcular_costo(2, 10)

    def test_nombre_servicio_vacio(self):
        """Verifica que no se acepte un nombre de servicio vacío."""
        with self.assertRaises(ServicioInvalidoError):
            ReservaSala(
                "S005", "", "Sala empresarial", 50000, 20
            )

    def test_tarifa_base_negativa(self):
        """Verifica que no se acepte una tarifa negativa."""
        with self.assertRaises(ParametroInvalidoError):
            ReservaSala(
                "S006", "Sala reuniones",
                "Sala empresarial", -50000, 20
            )

    def test_convertir_servicio_a_diccionario(self):
        """Verifica la conversión de los servicios a diccionario."""
        sala = ReservaSala(
            "S007", "Sala reuniones",
            "Sala empresarial", 50000, 20
        )

        datos = sala.a_diccionario()

        self.assertEqual(datos["id"], "S007")
        self.assertEqual(datos["tipo_servicio"], "ReservaSala")
        self.assertEqual(datos["capacidad_maxima"], 20)
    def test_calcular_costo_seguro_correctamente(self):
        """Verifica el cálculo seguro de un servicio."""

        sala = ReservaSala(
            "S008", "Sala reuniones",
            "Sala empresarial", 50000, 20
        )

        resultado = sala.calcular_costo_seguro(3, 15, 10)

        self.assertEqual(resultado, 135000)

    def test_calcular_costo_seguro_controla_error(self):
        """Verifica que el cálculo seguro conserve errores personalizados."""

        sala = ReservaSala(
            "S009", "Sala reuniones",
            "Sala empresarial", 50000, 20
        )

        with self.assertRaises(ParametroInvalidoError):
            sala.calcular_costo_seguro(0, 15)

    def test_calcular_costo_seguro_encadena_error(self):
        """Verifica el encadenamiento de errores inesperados."""

        sala = ReservaSala(
            "S010", "Sala reuniones",
            "Sala empresarial", 50000, 20
        )

        sala.calcular_costo = lambda *args, **kwargs: (
            1 / 0
        )

        with self.assertRaises(CalculoFinancieroError) as contexto:
            sala.calcular_costo_seguro(3, 15)

        self.assertIsInstance(
            contexto.exception.__cause__,
            ZeroDivisionError
        )

if __name__ == "__main__":
    unittest.main()

