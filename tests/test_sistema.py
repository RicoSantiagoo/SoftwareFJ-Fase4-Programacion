"""
Suite de Pruebas Unitarias para Software FJ.
Verifica:
1. Encapsulación y validación de datos en Cliente.
2. Polimorfismo y sobrecarga en jerarquía de Servicios.
3. Máquina de estados y manejo de excepciones en Reserva.
4. Integridad del orquestador SistemaGestionFJ.
5. Captura y encadenamiento de excepciones personalizadas.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.cliente import Cliente
from src.models.servicios_especializados import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from src.models.reserva import Reserva
from src.services.sistema_gestion import SistemaGestionFJ
from src.exceptions.custom_exceptions import (
    ClienteInvalidoError,
    ServicioInvalidoError,
    ParametroInvalidoError,
    CapacidadExcedidaError,
    ServicioNoDisponibleError,
    EstadoReservaInvalidoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
    ValidacionError,
    CalculoFinancieroError
)


class TestClienteModel(unittest.TestCase):
    """Pruebas unitarias para la entidad Cliente y su encapsulación."""

    def test_creacion_cliente_valido(self):
        cliente = Cliente("C-01", "Ana Maria Rios", "ana.rios@correo.com", "3001234567", es_frecuente=True)
        self.assertEqual(cliente.id_cliente, "C-01")
        self.assertEqual(cliente.nombre, "Ana Maria Rios")
        self.assertEqual(cliente.correo, "ana.rios@correo.com")
        self.assertEqual(cliente.telefono, "3001234567")
        self.assertTrue(cliente.es_frecuente)

    def test_cliente_correo_invalido(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente("C-02", "Pedro Perez", "correo_sin_arroba", "3001234567")

    def test_cliente_telefono_longitud_incorrecta(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente("C-03", "Maria Lopez", "maria@correo.com", "12345")

    def test_cliente_nombre_con_numeros(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente("C-04", "Juan123 Perez", "juan@correo.com", "3001112233")


class TestServiciosPolimorfismo(unittest.TestCase):
    """Pruebas para los servicios y polimorfismo de costos."""

    def setUp(self):
        self.sala = ReservaSala("SRV-1", "Sala Magna", 100000.0, 20, "conferencias", incluye_proyector=True)
        self.equipo = AlquilerEquipo("SRV-2", "Portatil Dev", 50000.0, "laptop", tarifa_seguro_diario=10000.0)
        self.asesoria = AsesoriaEspecializada("SRV-3", "DevOps", 150000.0, "Cloud", "senior")

    def test_polimorfismo_descripcion(self):
        desc_sala = self.sala.describir_servicio()
        desc_eq = self.equipo.describir_servicio()
        desc_ase = self.asesoria.describir_servicio()

        self.assertIn("Sala Magna", desc_sala)
        self.assertIn("Portatil Dev", desc_eq)
        self.assertIn("DevOps", desc_ase)

    def test_calculo_costo_sobrecargado_con_descuento_vip(self):
        # Duración 2 horas en sala conferencia: (100000 * 2 * 1.5) + 25000 = 325,000 bruto
        # Con VIP (10% descuento): subtotal = 292,500; IVA 19% = 55,575; Total = 348,075
        costo_vip = self.sala.calcular_costo_total(2.0, es_vip=True)
        costo_estandar = self.sala.calcular_costo_total(2.0, es_vip=False)
        self.assertLess(costo_vip, costo_estandar)

    def test_aforo_excedido_en_sala(self):
        with self.assertRaises(CapacidadExcedidaError):
            self.sala.validar_parametros(duracion=3.0, asistentes=50)

    def test_tarifa_base_negativa_invalida(self):
        with self.assertRaises(ServicioInvalidoError):
            ReservaSala("ERR", "Sala Falsa", -10.0, 10)


class TestReservaStateMachine(unittest.TestCase):
    """Pruebas de la máquina de estados y transiciones en Reserva."""

    def setUp(self):
        self.cliente = Cliente("C-01", "Diana Gomez", "diana@test.com", "3114445566")
        self.servicio = ReservaSala("S-01", "Sala A", 80000.0, 10, "reuniones")
        self.reserva = Reserva("RES-01", self.cliente, self.servicio, duracion=2.0)

    def test_flujo_confirmacion_y_cancelacion(self):
        self.assertEqual(self.reserva.estado, "CREADA")
        self.reserva.confirmar()
        self.assertEqual(self.reserva.estado, "CONFIRMADA")
        self.assertGreater(self.reserva.costo_total, 0)

        self.reserva.cancelar("Cliente solicitó cancelación")
        self.assertEqual(self.reserva.estado, "CANCELADA")

    def test_cancelacion_duplicada_lanza_excepcion(self):
        self.reserva.confirmar()
        self.reserva.cancelar("Motivo 1")
        with self.assertRaises(EstadoReservaInvalidoError):
            self.reserva.cancelar("Motivo 2")

    def test_reserva_servicio_no_disponible_encadena_excepcion(self):
        self.servicio.disponible = False
        with self.assertRaises(OperacionNoPermitidaError) as ctx:
            self.reserva.procesar()
        self.assertIsInstance(ctx.exception.__cause__, ServicioNoDisponibleError)


class TestSistemaGestionFJ(unittest.TestCase):
    """Pruebas funcionales de extremo a extremo en el orquestador en memoria."""

    def setUp(self):
        self.sistema = SistemaGestionFJ("Pruebas Unitarias")

    def test_registro_cliente_duplicado(self):
        self.sistema.registrar_cliente("CLI-A", "Carlos Ruiz", "carlos@test.com", "3201112233")
        with self.assertRaises(ValidacionError):
            self.sistema.registrar_cliente("CLI-A", "Carlos Ruiz", "carlos@test.com", "3201112233")

    def test_busqueda_entidad_no_encontrada(self):
        with self.assertRaises(EntidadNoEncontradaError):
            self.sistema.buscar_cliente("NO-EXISTE")

    def test_flujo_reserva_completo_en_memoria(self):
        self.sistema.registrar_cliente("CLI-B", "Elena Rojas", "elena@test.com", "3154443322", es_frecuente=True)
        equipo = AlquilerEquipo("EQ-10", "Laptop Core i7", 40000.0, "laptop")
        self.sistema.agregar_servicio(equipo)

        reserva = self.sistema.crear_reserva("RES-10", "CLI-B", "EQ-10", duracion=3.0)
        self.assertEqual(reserva.estado, "CONFIRMADA")
        self.assertGreater(reserva.costo_total, 0)

        resumen = self.sistema.obtener_resumen_operativo()
        self.assertEqual(resumen["total_clientes"], 1)
        self.assertEqual(resumen["total_servicios"], 1)
        self.assertEqual(resumen["total_reservas"], 1)


if __name__ == "__main__":
    unittest.main()
