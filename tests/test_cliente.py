"""Pruebas unitarias para el módulo de Clientes y Excepciones.

Desarrollado por: Santiago Rico Hernández
Curso: Programación (213023) — UNAD
Fase 4: Componente Práctico
"""
import unittest
from src.models.cliente import Cliente
from src.exceptions.custom_exceptions import ClienteInvalidoError


class TestModuloCliente(unittest.TestCase):
    """Batería de pruebas unitarias para validar encapsulación y manejo de errores en Cliente."""

    def test_creacion_cliente_valido(self):
        """Verifica que un cliente con datos legítimos se instancie correctamente."""
        cliente = Cliente(
            id_cliente="CLI-001",
            nombre="Santiago Rico Hernández",
            correo="santiagorico413@gmail.com",
            telefono="3001234567",
            es_frecuente=True,
        )
        self.assertEqual(cliente.id, "CLI-001")
        self.assertEqual(cliente.nombre, "Santiago Rico Hernández")
        self.assertEqual(cliente.correo, "santiagorico413@gmail.com")
        self.assertEqual(cliente.telefono, "3001234567")
        self.assertTrue(cliente.es_frecuente)
        self.assertTrue(cliente.validar())

    def test_cliente_correo_invalido_lanza_excepcion(self):
        """Verifica que un correo sin formato RFC lance ClienteInvalidoError."""
        with self.assertRaises(ClienteInvalidoError) as contexto:
            Cliente(
                id_cliente="CLI-002",
                nombre="Usuario Invalido",
                correo="correo_sin_arroba.com",
                telefono="3109876543",
            )
        self.assertIn("correo electrónico no posee un formato válido", str(contexto.exception))

    def test_cliente_telefono_invalido_lanza_excepcion(self):
        """Verifica que un teléfono que no tenga exactamente 10 dígitos lance ClienteInvalidoError."""
        with self.assertRaises(ClienteInvalidoError) as contexto:
            Cliente(
                id_cliente="CLI-003",
                nombre="Usuario Telefono Corto",
                correo="usuario@valido.com",
                telefono="12345",  # Menos de 10 dígitos
            )
        self.assertIn("10 dígitos numéricos", str(contexto.exception))

    def test_cliente_nombre_con_numeros_lanza_excepcion(self):
        """Verifica que un nombre con dígitos lance ClienteInvalidoError."""
        with self.assertRaises(ClienteInvalidoError) as contexto:
            Cliente(
                id_cliente="CLI-004",
                nombre="Santiago 123",
                correo="usuario@valido.com",
                telefono="3001234567",
            )
        self.assertIn("no puede contener dígitos", str(contexto.exception))

    def test_cliente_modificacion_setter_valido(self):
        """Verifica que los decoradores @property y setter permitan actualización con datos válidos."""
        cliente = Cliente("CLI-005", "Carlos Lopez", "carlos@empresa.com", "3201112233")
        cliente.telefono = "3159998877"
        cliente.correo = "carlos.nuevo@empresa.com"
        cliente.es_frecuente = True

        self.assertEqual(cliente.telefono, "3159998877")
        self.assertEqual(cliente.correo, "carlos.nuevo@empresa.com")
        self.assertTrue(cliente.es_frecuente)

    def test_cliente_modificacion_setter_invalido_lanza_excepcion(self):
        """Verifica que la asignación por setter aplique validación estricta."""
        cliente = Cliente("CLI-006", "Maria Torres", "maria@empresa.com", "3004445566")
        with self.assertRaises(ClienteInvalidoError):
            cliente.correo = "correo_invalido"

    def test_cliente_a_diccionario(self):
        """Verifica la serialización correcta del objeto Cliente a estructura de diccionario."""
        cliente = Cliente("CLI-007", "Ana Gomez", "ana@empresa.com", "3112223344", es_frecuente=False)
        dicc = cliente.a_diccionario()
        self.assertEqual(dicc["id_cliente"], "CLI-007")
        self.assertEqual(dicc["nombre"], "Ana Gomez")
        self.assertFalse(dicc["es_frecuente"])


if __name__ == "__main__":
    unittest.main()
