"""
Programa principal - Software FJ (Fase 4: Prácticas Simuladas)
Curso: Programación (213023) - UNAD

Integrantes del Grupo:
- Santiago Rico Hernández (Módulo 1 y 2: Arquitectura, Excepciones y Clientes)
- Yojhan Estiven Castaño Santa (Módulo 4: Reservas)
- Andrés Nieves (Módulo 3: Servicios)
"""

from src.utils.logger import logger_sistema
from src.models.cliente import Cliente
from src.models.reserva import Reserva
from src.exceptions.custom_exceptions import ClienteInvalidoError


def main():
    print("====================================================")
    print("      SOFTWARE FJ - FASE 4: PRÁCTICAS SIMULADAS     ")
    print("  Curso: Programación (213023) - Grupo Colaborativo ")
    print("  Integrantes:")
    print("    - Santiago Rico Hernández (Líder / Módulos 1 y 2)")
    print("    - Yojhan Estiven Castaño Santa (Módulo 4)")
    print("    - Andrés Nieves (Módulo 3)")
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

    # 6. Demostración del Módulo Reservas (Aporte de Yojhan Castaño)
    print("6. Probando Módulo Reservas (Aporte: Yojhan Castaño)...")
    reserva1 = Reserva(
        id_reserva="RES-001",
        cliente=cliente1.nombre,
        servicio="Alquiler Servidor Dedicado",
        fecha="2026-11-20",
        hora="09:00"
    )
    print(f"   [OK] Reserva instanciada: {reserva1}")
    resultado_conf = reserva1.confirmar()
    print(f"   [OK] {resultado_conf}")
    resultado_cambio = reserva1.cambiar_fecha("2026-11-21", "10:30")
    print(f"   [OK] {resultado_cambio}")
    print(f"   [OK] Información final: {reserva1.mostrar_info()}\n")

    print("====================================================")
    print("Estado del grupo colaborativo:")
    print("  [X] Módulo 1 y 2: Base, Excepciones y Clientes (Santiago Rico Hernández)")
    print("  [X] Módulo 4: Reservas y Estados (Yojhan Estiven Castaño Santa)")
    print("  [/] Módulo 3: Servicios y Polimorfismo (Asignado a Andrés Nieves)")
    print("  [ ] Módulo 5: Orquestador en memoria (Por definir)")
    print("  [ ] Módulo 6: Pruebas globales y simulaciones (Por definir)")
    print("====================================================")


if __name__ == "__main__":
    main()
