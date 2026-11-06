"""
Programa principal de prueba - Módulo Clientes y Excepciones
Estudiante: Santiago Rico Hernández
Curso: Programación (213023) - UNAD - Fase 4
"""

from src.utils.logger import logger_sistema
from src.models.cliente import Cliente
from src.exceptions.custom_exceptions import ClienteInvalidoError


def main():
    print("====================================================")
    print("      SOFTWARE FJ - FASE 4: PRÁCTICAS SIMULADAS     ")
    print("      Aporte: Módulo Clientes y Excepciones         ")
    print("      Estudiante: Santiago Rico Hernández           ")
    print("====================================================\n")

    logger_sistema.info("Iniciando pruebas del módulo de clientes...")

    # 1. Crear un cliente válido
    print("1. Creando un cliente con datos válidos...")
    try:
        cliente1 = Cliente(
            id_cliente="CLI-101",
            nombre="Laura Camila Benavides",
            correo="laura.benavides@empresa.com",
            telefono="3101234567",
            es_frecuente=False
        )
    except ClienteInvalidoError as error:
        print(f"   [Error]: {error}")
    else:
        logger_sistema.info(f"Cliente registrado con éxito: {cliente1.nombre}")
        print(f"   [OK] Cliente creado: {cliente1}")
    finally:
        print("   -> Fin intento de registro 1.\n")

    # 2. Crear cliente frecuente (VIP)
    print("2. Creando un cliente frecuente (VIP)...")
    try:
        cliente2 = Cliente(
            id_cliente="CLI-102",
            nombre="Santiago Rico Hernández",
            correo="santiagorico413@gmail.com",
            telefono="3009876543",
            es_frecuente=True
        )
    except ClienteInvalidoError as error:
        print(f"   [Error]: {error}")
    else:
        logger_sistema.info(f"Cliente VIP registrado: {cliente2.nombre}")
        print(f"   [OK] Cliente VIP creado: {cliente2}")
    finally:
        print("   -> Fin intento de registro 2.\n")

    # 3. Probar validación con correo inválido
    print("3. Probando validación con un correo sin formato correcto...")
    try:
        print("   Intentando registrar con correo: 'correo_sin_arroba'...")
        Cliente("CLI-103", "Pedro Perez", "correo_sin_arroba", "3150001122")
    except ClienteInvalidoError as error:
        logger_sistema.warning(f"Excepción capturada correctamente: {error}")
        print(f"   [OK - Excepción atrapada]: {error}")
        print("   -> El sistema sigue funcionando con normalidad.")
    finally:
        print("   -> Fin intento de registro 3.\n")

    # 4. Probar validación con teléfono que no tiene 10 dígitos
    print("4. Probando validación con un teléfono incompleto...")
    try:
        print("   Intentando registrar con teléfono: '12345'...")
        Cliente("CLI-104", "Mariana Gomez", "mariana@gmail.com", "12345")
    except ClienteInvalidoError as error:
        logger_sistema.warning(f"Excepción capturada correctamente: {error}")
        print(f"   [OK - Excepción atrapada]: {error}")
        print("   -> El sistema sigue funcionando con normalidad.")
    finally:
        print("   -> Fin intento de registro 4.\n")

    # 5. Probar getters, setters y exportar a diccionario
    print("5. Probando encapsulación (@property y @setter)...")
    print(f"   Teléfono inicial de {cliente1.nombre}: {cliente1.telefono}")
    cliente1.telefono = "3209998877"
    cliente1.es_frecuente = True
    print(f"   Nuevo teléfono (actualizado con setter): {cliente1.telefono}")
    print(f"   Datos exportados a diccionario: {cliente1.a_diccionario()}\n")

    print("====================================================")
    print("Estado del grupo colaborativo:")
    print("  [X] Módulo 1 y 2: Base, Excepciones y Clientes (Hecho por Santiago Rico)")
    print("  [ ] Módulo 3: Servicios y Polimorfismo (Pendiente compañero 2)")
    print("  [ ] Módulo 4: Reservas y Estados (Pendiente compañero 3)")
    print("  [ ] Módulo 5: Orquestador en memoria (Pendiente compañero 4)")
    print("  [ ] Módulo 6: Pruebas globales y simulaciones (Pendiente compañero 5)")
    print("====================================================")


if __name__ == "__main__":
    main()
