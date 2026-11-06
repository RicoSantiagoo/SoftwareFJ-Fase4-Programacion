"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas — Software FJ S.A.S.
Universidad Nacional Abierta y a Distancia (UNAD)
Curso: Programación (Código: 213023) — Fase 4: Componente Práctico (Prácticas Simuladas)

Módulo 1 y 2: Arquitectura Base, Jerarquía de Excepciones y Gestión de Clientes
Desarrollador: Santiago Rico Hernández (Líder de Repositorio)
"""
import sys
from src.utils.logger import logger_sistema as logger
from src.models.cliente import Cliente
from src.exceptions.custom_exceptions import ClienteInvalidoError, SoftwareFJError


def encabezado():
    print("=" * 80)
    print("      SOFTWARE FJ S.A.S. — GESTIÓN CORPORATIVA DE SERVICIOS Y CLIENTES")
    print("          UNAD | CURSO DE PROGRAMACIÓN (213023) | FASE 4 - PRÁCTICAS")
    print("      Módulo: Arquitectura Base, Excepciones y Clientes (Encapsulación)")
    print("      Desarrollador: Santiago Rico Hernández")
    print("=" * 80)
    print()


def simular_modulo_clientes():
    """Ejecuta una serie de casos de prueba controlados para demostrar el funcionamiento del módulo."""
    logger.info("=== Inicio de simulación del Módulo de Clientes — Santiago Rico Hernández ===")

    # 1. Registro exitoso de cliente estándar
    print(">>> Caso 1 [VÁLIDO]: Registro de Cliente Estándar con datos correctos")
    try:
        cliente_1 = Cliente(
            id_cliente="CLI-101",
            nombre="Laura Camila Benavides",
            correo="laura.benavides@techcorp.com",
            telefono="3101234567",
            es_frecuente=False,
        )
    except ClienteInvalidoError as error:
        logger.error(f"Error inesperado al crear cliente válido: {error}")
        print(f"  [ERROR] {error}")
    else:
        logger.info(f"Cliente registrado con éxito: {cliente_1}")
        print(f"  [+] ÉXITO: {cliente_1}")
    finally:
        print("  [*] Verificación de flujo completada (finally ejecutado).\n")

    # 2. Registro exitoso de cliente frecuente / VIP
    print(">>> Caso 2 [VÁLIDO]: Registro de Cliente Frecuente (VIP)")
    try:
        cliente_2 = Cliente(
            id_cliente="CLI-102",
            nombre="Santiago Rico Hernández",
            correo="santiagorico413@gmail.com",
            telefono="3009876543",
            es_frecuente=True,
        )
    except ClienteInvalidoError as error:
        logger.error(f"Error inesperado: {error}")
        print(f"  [ERROR] {error}")
    else:
        logger.info(f"Cliente VIP registrado con éxito: {cliente_2}")
        print(f"  [+] ÉXITO: {cliente_2}")
    finally:
        print("  [*] Registro en bitácora software_fj.log completado.\n")

    # 3. Caso Inválido: Correo con formato erróneo
    print(">>> Caso 3 [INVÁLIDO - CONTROLADO]: Validación estricta de correo electrónico (RFC 5322)")
    try:
        print("  [*] Intentando registrar cliente con correo: 'correo_invalido_sin_arroba'...")
        Cliente(
            id_cliente="CLI-103",
            nombre="Pedro Pablo Perez",
            correo="correo_invalido_sin_arroba",
            telefono="3150001122",
        )
    except ClienteInvalidoError as err:
        logger.warning(f"Excepción controlada capturada: {err}")
        print(f"  [OK - EXCEPCIÓN CONTROLADA] Tipo: {err.__class__.__name__}")
        print(f"      Mensaje: {err}")
        print("      Estado del sistema: ESTABLE y en ejecución.")
    else:
        print("  [FALLO] No se detectó el error de correo.")
    finally:
        print("  [*] Bloque finally: Evento de validación registrado.\n")

    # 4. Caso Inválido: Teléfono que no cumple 10 dígitos numéricos
    print(">>> Caso 4 [INVÁLIDO - CONTROLADO]: Validación estricta de longitud telefónica (10 dígitos)")
    try:
        print("  [*] Intentando registrar cliente con teléfono incompleto: '12345'...")
        Cliente(
            id_cliente="CLI-104",
            nombre="Mariana Gomez",
            correo="mariana@empresa.com",
            telefono="12345",  # Longitud inválida
        )
    except ClienteInvalidoError as err:
        logger.warning(f"Excepción controlada capturada: {err}")
        print(f"  [OK - EXCEPCIÓN CONTROLADA] Tipo: {err.__class__.__name__}")
        print(f"      Mensaje: {err}")
        print("      Estado del sistema: ESTABLE y en ejecución.")
    else:
        print("  [FALLO] No se detectó el error de teléfono.")
    finally:
        print("  [*] Bloque finally: Evento de validación registrado.\n")

    # 5. Encapsulación y modificación mediante Setters
    print(">>> Caso 5 [VÁLIDO]: Prueba de encapsulación (@property y @setter)")
    print(f"  [*] Teléfono original de {cliente_1.nombre}: {cliente_1.telefono}")
    cliente_1.telefono = "3209998877"
    cliente_1.es_frecuente = True
    print(f"  [+] Teléfono actualizado por setter: {cliente_1.telefono}")
    print(f"  [+] Nuevo estado de fidelización: {'VIP' if cliente_1.es_frecuente else 'Estándar'}")
    print(f"  [+] Diccionario serializado: {cliente_1.a_diccionario()}\n")

    print("=" * 80)
    print("ESTADO DEL PROYECTO COLABORATIVO — FASE 4:")
    print("  [✓] Módulo 1: Arquitectura Base y Excepciones (Completado - Santiago Rico)")
    print("  [✓] Módulo 2: Modelo Cliente y Encapsulación (Completado - Santiago Rico)")
    print("  [ ] Módulo 3: Catálogo de Servicios y Polimorfismo (Pendiente - Integrante 2)")
    print("  [ ] Módulo 4: Máquina de Estados de Reservas (Pendiente - Integrante 3)")
    print("  [ ] Módulo 5: Orquestador en Memoria sin Base de Datos (Pendiente - Integrante 4)")
    print("  [ ] Módulo 6: Pruebas Unitarias Integradas y Simulaciones QA (Pendiente - Integrante 5)")
    print("=" * 80)


if __name__ == "__main__":
    encabezado()
    simular_modulo_clientes()
