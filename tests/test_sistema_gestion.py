"""
Módulo 6 - Batería de Pruebas Unitarias Integradas y QA
Autor: Santiago Rico Hernández - Líder de Repositorio
Proyecto: Software FJ - Fase 4 (Programación UNAD)

Evalúa la orquestación central en memoria del SistemaGestionFJ, verificando unicidad,
búsquedas, vinculación de entidades y transiciones de estado de reservas.
"""

import unittest
from src.services.sistema_gestion import SistemaGestionFJ
from src.models.servicio import ReservaSala, AlquilerEquipo
from src.exceptions.custom_exceptions import (
    ValidacionError,
    ClienteInvalidoError,
    ServicioInvalidoError,
    EntidadNoEncontradaError
)


class TestSistemaGestionFJ(unittest.TestCase):
    """Suite de pruebas unitarias para el controlador central en memoria."""

    def setUp(self):
        """Inicializa una instancia fresca del orquestador antes de cada prueba."""
        self.sistema = SistemaGestionFJ("Software FJ - Test")

    def test_inicializar_sistema_vacio(self):
        """Verifica que el sistema comience sin entidades en memoria."""
        self.assertEqual(self.sistema.total_clientes, 0)
        self.assertEqual(self.sistema.total_servicios, 0)
        self.assertEqual(self.sistema.total_reservas, 0)

    def test_registrar_cliente_exitoso(self):
        """Verifica el registro válido de un cliente en memoria."""
        cliente = self.sistema.registrar_cliente(
            id_cliente="CLI-001",
            nombre="Carlos Restrepo",
            correo="carlos@dominio.com",
            telefono="3001234567"
        )
        self.assertEqual(self.sistema.total_clientes, 1)
        self.assertEqual(cliente.nombre, "Carlos Restrepo")

    def test_registrar_cliente_duplicado_lanza_error(self):
        """Verifica que no se permitan identificadores de cliente duplicados."""
        self.sistema.registrar_cliente(
            id_cliente="CLI-001",
            nombre="Carlos Restrepo",
            correo="carlos@dominio.com",
            telefono="3001234567"
        )
        with self.assertRaises(ValidacionError):
            self.sistema.registrar_cliente(
                id_cliente="CLI-001",
                nombre="Otro Carlos",
                correo="otro@dominio.com",
                telefono="3119876543"
            )

    def test_buscar_cliente_no_existente_lanza_error(self):
        """Comprueba que buscar un cliente inexistente lance EntidadNoEncontradaError."""
        with self.assertRaises(EntidadNoEncontradaError):
            self.sistema.buscar_cliente("CLI-999")

    def test_agregar_servicio_exitoso(self):
        """Verifica la incorporación legítima de un servicio al portafolio."""
        sala = ReservaSala(
            identificador="SALA-10",
            nombre="Sala Innovación",
            descripcion="Sala de reuniones ejecutivas",
            tarifa_base=45000.0,
            capacidad_maxima=8
        )
        self.sistema.agregar_servicio(sala)
        self.assertEqual(self.sistema.total_servicios, 1)
        encontrado = self.sistema.buscar_servicio("SALA-10")
        self.assertEqual(encontrado.nombre, "Sala Innovación")

    def test_agregar_servicio_duplicado_lanza_error(self):
        """Comprueba que identificadores de servicios duplicados sean rechazados."""
        sala1 = ReservaSala("SALA-10", "Sala A", "Desc A", 40000.0, 6)
        sala2 = ReservaSala("SALA-10", "Sala B", "Desc B", 50000.0, 10)
        self.sistema.agregar_servicio(sala1)
        with self.assertRaises(ServicioInvalidoError):
            self.sistema.agregar_servicio(sala2)

    def test_crear_reserva_vinculada_exitosa(self):
        """Verifica la creación orquestada de una reserva conectando cliente y servicio."""
        self.sistema.registrar_cliente("CLI-10", "Ana Rojas", "ana@correo.com", "3154567890")
        self.sistema.agregar_servicio(ReservaSala("SALA-01", "Sala Directiva", "Sala VIP", 60000.0, 15))

        reserva = self.sistema.crear_reserva(
            id_reserva="RES-100",
            id_cliente="CLI-10",
            id_servicio="SALA-01",
            fecha="2026-11-25",
            hora="10:00"
        )
        self.assertEqual(self.sistema.total_reservas, 1)
        self.assertEqual(reserva.estado, "pendiente")
        self.assertEqual(reserva.cliente, "Ana Rojas")

    def test_confirmar_y_cancelar_reserva(self):
        """Comprueba las transiciones de estado de una reserva."""
        self.sistema.registrar_cliente("CLI-20", "Julian Soto", "julian@correo.com", "3201112233")
        self.sistema.agregar_servicio(ReservaSala("SALA-02", "Sala Juntas", "Desc", 35000.0, 5))
        self.sistema.crear_reserva("RES-200", "CLI-20", "SALA-02", "2026-11-26", "11:00")

        self.sistema.confirmar_reserva("RES-200")
        reserva = self.sistema.buscar_reserva("RES-200")
        self.assertEqual(reserva.estado, "confirmada")

        self.sistema.cancelar_reserva("RES-200")
        self.assertEqual(reserva.estado, "cancelada")

    def test_obtener_resumen_operativo(self):
        """Valida las métricas cuantitativas generadas por el sistema."""
        self.sistema.registrar_cliente("CLI-30", "Marta Gómez", "marta@correo.com", "3103334455")
        resumen = self.sistema.obtener_resumen_operativo()
        self.assertEqual(resumen["total_clientes"], 1)
        self.assertEqual(resumen["total_servicios"], 0)
        self.assertEqual(resumen["total_reservas"], 0)


if __name__ == "__main__":
    unittest.main()
