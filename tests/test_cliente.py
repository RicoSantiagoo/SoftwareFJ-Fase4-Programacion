"""
Pruebas unitarias para la clase Cliente y sus validaciones.
Estudiante: Santiago Rico Hernández
Curso: Programación (213023) - UNAD
"""

import unittest
from src.models.cliente import Cliente
from src.exceptions.custom_exceptions import ClienteInvalidoError


class TestCliente(unittest.TestCase):

    def test_crear_cliente_correcto(self):
        """Verifica que se cree el cliente si los datos son correctos."""
        cliente = Cliente("CLI-001", "Santiago Rico", "santiagorico413@gmail.com", "3001234567", es_frecuente=True)
        self.assertEqual(cliente.id, "CLI-001")
        self.assertEqual(cliente.nombre, "Santiago Rico")
        self.assertEqual(cliente.correo, "santiagorico413@gmail.com")
        self.assertEqual(cliente.telefono, "3001234567")
        self.assertTrue(cliente.es_frecuente)
        self.assertTrue(cliente.validar())

    def test_correo_sin_formato_lanza_error(self):
        """Si el correo no tiene arroba o dominio, debe lanzar ClienteInvalidoError."""
        with self.assertRaises(ClienteInvalidoError):
            Cliente("CLI-002", "Juan Perez", "correomal", "3101234567")

    def test_telefono_longitud_incorrecta(self):
        """El teléfono celular debe tener exactamente 10 dígitos."""
        with self.assertRaises(ClienteInvalidoError):
            Cliente("CLI-003", "Maria Lopez", "maria@gmail.com", "12345")

    def test_nombre_con_numeros_lanza_error(self):
        """El nombre no debe permitir números."""
        with self.assertRaises(ClienteInvalidoError):
            Cliente("CLI-004", "Santiago123", "santi@gmail.com", "3001234567")

    def test_actualizar_telefono_con_setter(self):
        """Prueba que el setter permita cambiar el teléfono si es válido."""
        cliente = Cliente("CLI-005", "Carlos Gómez", "carlos@gmail.com", "3001112233")
        cliente.telefono = "3154445566"
        self.assertEqual(cliente.telefono, "3154445566")

    def test_actualizar_correo_invalido_con_setter(self):
        """Prueba que el setter rechace un correo inválido al intentar modificarlo."""
        cliente = Cliente("CLI-006", "Ana Ruiz", "ana@gmail.com", "3201112233")
        with self.assertRaises(ClienteInvalidoError):
            cliente.correo = "correo_no_valido"

    def test_convertir_a_diccionario(self):
        """Verifica que la función a_diccionario retorne los datos esperados."""
        cliente = Cliente("CLI-007", "Laura Castro", "laura@gmail.com", "3129998877", es_frecuente=False)
        datos = cliente.a_diccionario()
        self.assertEqual(datos["id_cliente"], "CLI-007")
        self.assertEqual(datos["nombre"], "Laura Castro")
        self.assertFalse(datos["es_frecuente"])


if __name__ == "__main__":
    unittest.main()
