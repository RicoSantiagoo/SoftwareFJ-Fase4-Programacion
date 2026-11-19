"""
Programa principal - Software FJ (Fase 4: Prácticas Simuladas)
Curso: Programación (Código: 213023) - UNAD

Integrantes del Grupo Colaborativo:
- Santiago Rico Hernández (Líder / Módulos 1 y 2: Arquitectura, Excepciones y Clientes)
- Yojhan Estiven Castaño Santa (Módulo 4: Reservas y Estados)
- Andrés Felipe Nieves León (Módulo 3: Catálogo de Servicios y Polimorfismo)
"""

from src.utils.logger import logger_sistema
from src.models.cliente import Cliente
from src.models.reserva import Reserva
from src.models.servicio import (
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada
)
from src.services.sistema_gestion import SistemaGestionFJ
from src.exceptions.custom_exceptions import (
    ClienteInvalidoError,
    CapacidadExcedidaError,
    ParametroInvalidoError
)


def main():
    print("====================================================")
    print("      SOFTWARE FJ - FASE 4: PRÁCTICAS SIMULADAS     ")
    print("  Curso: Programación (213023) - Grupo Colaborativo ")
    print("  Integrantes:")
    print("    - Santiago Rico Hernández (Líder / Módulos 1 y 2)")
    print("    - Yojhan Estiven Castaño Santa (Módulo 4)")
    print("    - Andrés Felipe Nieves León (Módulo 3)")
    print("====================================================\n")

    logger_sistema.info("Iniciando ejecución integrada de demostración Software FJ...")

    # ---------------------------------------------------------
    # BLOQUE 1: MÓDULO CLIENTES (Aporte: Santiago Rico)
    # ---------------------------------------------------------
    print("--- BLOQUE 1: GESTIÓN DE CLIENTES (Aporte: Santiago Rico) ---")

    # 1. Crear un cliente estándar válido
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

    # 3. Control de excepciones: correo inválido
    print("3. Probando validación con correo sin formato correcto...")
    try:
        print("   Intentando registrar con correo: 'correo_sin_arroba'...")
        Cliente("CLI-103", "Pedro Perez", "correo_sin_arroba", "3150001122")
    except ClienteInvalidoError as error:
        logger_sistema.warning(f"Excepción capturada correctamente: {error}")
        print(f"   [OK - Excepción atrapada]: {error}")
        print("   -> El sistema sigue funcionando con normalidad.")
    finally:
        print("   -> Fin intento de registro 3.\n")

    # 4. Control de excepciones: teléfono no celular
    print("4. Probando validación con teléfono de longitud incorrecta...")
    try:
        print("   Intentando registrar con teléfono: '12345'...")
        Cliente("CLI-104", "Mariana Gomez", "mariana@gmail.com", "12345")
    except ClienteInvalidoError as error:
        logger_sistema.warning(f"Excepción capturada correctamente: {error}")
        print(f"   [OK - Excepción atrapada]: {error}")
        print("   -> El sistema sigue funcionando con normalidad.")
    finally:
        print("   -> Fin intento de registro 4.\n")

    # 5. Encapsulación estricta (@property / @setter)
    print("5. Probando encapsulación (@property y @setter)...")
    print(f"   Teléfono inicial de {cliente1.nombre}: {cliente1.telefono}")
    cliente1.telefono = "3209998877"
    cliente1.es_frecuente = True
    print(f"   Nuevo teléfono (actualizado con setter): {cliente1.telefono}")
    print(f"   Datos exportados a diccionario: {cliente1.a_diccionario()}\n")

    # ---------------------------------------------------------
    # BLOQUE 2: MÓDULO SERVICIOS Y POLIMORFISMO (Aporte: Andrés Nieves)
    # ---------------------------------------------------------
    print("--- BLOQUE 2: CATÁLOGO DE SERVICIOS (Aporte: Andrés Nieves) ---")

    # 6. Servicio de Sala de Conferencias
    print("6. Creando servicio de Sala de Conferencias (ReservaSala)...")
    sala_ejecutiva = ReservaSala(
        identificador="SERV-SALA-01",
        nombre="Sala Ejecutiva Innovación",
        descripcion="Sala climatizada con proyector 4K y videoconferencia",
        tarifa_base=50000.0,
        capacidad_maxima=12
    )
    costo_sala = sala_ejecutiva.calcular_costo(horas=4, cantidad_personas=8, descuento=10.0)
    print(f"   [OK] Sala instanciada: {sala_ejecutiva.nombre} (Capacidad: {sala_ejecutiva.capacidad_maxima} personas)")
    print(f"   [OK] Costo calculado (4 horas con 10% desc): ${costo_sala:,.2f}\n")

    # 7. Servicio de Alquiler de Equipos Tecnológicos
    print("7. Creando servicio de Alquiler de Equipos (AlquilerEquipo)...")
    servidor_dedicado = AlquilerEquipo(
        identificador="SERV-EQ-01",
        nombre="Alquiler Servidor Blade",
        descripcion="Servidor rack para procesamiento masivo y bases de datos",
        tarifa_base=120000.0,
        equipo="Servidor Dell PowerEdge R750",
        disponible=True
    )
    costo_equipo = servidor_dedicado.calcular_costo(dias=5, cantidad=2, descuento=5.0)
    print(f"   [OK] Equipo instanciado: {servidor_dedicado.equipo}")
    print(f"   [OK] Costo calculado (2 unidades x 5 días con 5% desc): ${costo_equipo:,.2f}\n")

    # 8. Servicio de Asesoría Especializada con cálculo seguro (try/except/else/finally)
    print("8. Creando servicio de Asesoría Especializada con cálculo seguro...")
    asesoria_cloud = AsesoriaEspecializada(
        identificador="SERV-AS-01",
        nombre="Consultoría Cloud",
        descripcion="Diseño de infraestructura segura y escalable en la nube",
        tarifa_base=95000.0,
        especialidad="Arquitectura AWS y Ciberseguridad",
        disponible=True
    )
    costo_asesoria = asesoria_cloud.calcular_costo_seguro(horas=6, descuento=0.0)
    print(f"   [OK] Asesoría instanciada: {asesoria_cloud.nombre} (Especialidad: {asesoria_cloud.especialidad})")
    print(f"   [OK] Costo cálculo seguro (6 horas): ${costo_asesoria:,.2f}\n")

    # 9. Control de excepción en Servicios: Capacidad de sala excedida
    print("9. Probando validación de capacidad excedida en sala...")
    try:
        print("   Intentando agendar 18 personas en sala con capacidad para 12...")
        sala_ejecutiva.calcular_costo(horas=2, cantidad_personas=18)
    except CapacidadExcedidaError as error:
        logger_sistema.warning(f"Excepción de capacidad capturada: {error}")
        print(f"   [OK - Excepción atrapada]: {error}")
        print("   -> Validación de negocio aprobada con éxito.")
    finally:
        print("   -> Fin intento de sobrecupo en sala.\n")

    # ---------------------------------------------------------
    # BLOQUE 3: MÓDULO RESERVAS (Aporte: Yojhan Castaño)
    # ---------------------------------------------------------
    print("--- BLOQUE 3: GESTIÓN DE RESERVAS (Aporte: Yojhan Castaño) ---")

    # 10. Reserva vinculando Cliente y Servicio
    print("10. Creando una reserva vinculada...")
    reserva1 = Reserva(
        id_reserva="RES-001",
        cliente=cliente1.nombre,
        servicio=sala_ejecutiva.nombre,
        fecha="2026-11-20",
        hora="09:00"
    )
    print(f"   [OK] Reserva instanciada: {reserva1}")
    resultado_conf = reserva1.confirmar()
    print(f"   [OK] Estado confirmado: {resultado_conf}")
    resultado_cambio = reserva1.cambiar_fecha("2026-11-21", "14:00")
    print(f"   [OK] Reprogramación: {resultado_cambio}")
    print(f"   [OK] Información final consolidada: {reserva1.mostrar_info()}\n")

    # ---------------------------------------------------------
    # BLOQUE 4: MÓDULO 5 Y 6 - ORQUESTADOR EN MEMORIA Y QA (Aporte: Santiago Rico)
    # ---------------------------------------------------------
    print("--- BLOQUE 4: ORQUESTACIÓN EN MEMORIA Y QA (Aporte: Santiago Rico) ---")
    sistema = SistemaGestionFJ("Software FJ S.A.S.")

    # 11. Registrar entidades a través del orquestador central
    print("11. Orquestando registro de entidades en memoria...")
    sistema.registrar_cliente(
        id_cliente="CLI-500",
        nombre="Carlos Valderrama",
        correo="carlos.v@correo.com",
        telefono="3007654321",
        es_frecuente=True
    )
    sistema.agregar_servicio(sala_ejecutiva)
    sistema.crear_reserva(
        id_reserva="RES-500",
        id_cliente="CLI-500",
        id_servicio="SERV-SALA-01",
        fecha="2026-11-22",
        hora="15:00"
    )
    sistema.confirmar_reserva("RES-500")
    print("   [OK] Entidades orquestadas en memoria con éxito.")

    # 12. Métricas y resumen operativo del sistema
    print("12. Generando resumen operativo en memoria...")
    resumen = sistema.obtener_resumen_operativo()
    print(f"   [OK] Total Clientes en memoria : {resumen['total_clientes']}")
    print(f"   [OK] Total Servicios en catálogo: {resumen['total_servicios']}")
    print(f"   [OK] Total Reservas activas     : {resumen['total_reservas']}")
    print(f"   [OK] Distribución de estados    : {resumen['distribucion_estados']}\n")

    # ---------------------------------------------------------
    # RESUMEN CONSOLIDADO DEL GRUPO COLABORATIVO
    # ---------------------------------------------------------
    print("====================================================")
    print("RESUMEN DE PARTICIPACIÓN COLABORATIVA (FASE 4 - UNAD):")
    print("  [X] Módulo 1 y 2: Arquitectura y Clientes -> Santiago Rico Hernández [LISTO]")
    print("  [X] Módulo 3: Servicios y Polimorfismo   -> Andrés Felipe Nieves León [LISTO]")
    print("  [X] Módulo 4: Reservas y Estados        -> Yojhan Estiven Castaño Santa [LISTO]")
    print("  [X] Módulo 5: Orquestador en memoria     -> Santiago Rico Hernández [LISTO]")
    print("  [X] Módulo 6: Batería QA (33 tests)     -> Santiago Rico Hernández [LISTO]")
    print("====================================================")


if __name__ == "__main__":
    main()
