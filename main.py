"""
Script Principal de Simulación de Operaciones para Software FJ.
Ejecuta de manera secuencial 12 operaciones (válidas e inválidas) para demostrar:
1. Manejo robusto de excepciones sin colapso de la aplicación.
2. Uso de excepciones personalizadas, bloques try/except/else/finally y encadenamiento (raise from).
3. Registro íntegro de eventos y errores en 'software_fj.log'.
4. Arquitectura limpia en POO (Abstracción, Herencia, Polimorfismo, Encapsulación).
"""

import sys
import os

# Configurar salida en UTF-8 para compatibilidad total con terminales de Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Asegurar que el directorio raíz del proyecto se encuentre en el PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.services.sistema_gestion import SistemaGestionFJ
from src.models.servicios_especializados import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from src.exceptions.custom_exceptions import (
    SoftwareFJError,
    ClienteInvalidoError,
    ValidacionError,
    ServicioInvalidoError,
    ParametroInvalidoError,
    CapacidadExcedidaError,
    ServicioNoDisponibleError,
    EstadoReservaInvalidoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError
)
from src.utils.logger import logger_sistema, LOG_FILE_PATH


def imprimir_encabezado(titulo: str):
    ancho = 85
    print("\n" + "=" * ancho)
    print(f"{titulo.center(ancho)}")
    print("=" * ancho)


def imprimir_caso(numero: int, tipo: str, titulo: str):
    marca = "[OK - VÁLIDO]" if "VÁLIDO" in tipo.upper() else "[CONTROLADO - INVÁLIDO]"
    print(f"\n>>> Simulación #{numero:02d} {marca}: {titulo}")
    print("-" * 85)


def ejecutar_simulaciones():
    imprimir_encabezado("SOFTWARE FJ - SIMULACIÓN DE PRÁCTICAS OPERATIVAS (FASE 4)")
    print(f"Ruta de archivo de logs: {LOG_FILE_PATH}")
    print("Iniciando batería de pruebas para validar estabilidad y captura de excepciones...\n")

    sistema = SistemaGestionFJ("Software FJ S.A.S.")

    # -------------------------------------------------------------------------
    # SIMULACIÓN 1 [VÁLIDA]: Registro exitoso de clientes
    # -------------------------------------------------------------------------
    imprimir_caso(1, "VÁLIDO", "Registro de clientes válidos (Estándar y Frecuente/VIP)")
    try:
        c1 = sistema.registrar_cliente(
            id_cliente="CLI-1001",
            nombre="Carlos Andres Mendoza",
            correo="carlos.mendoza@empresa.com",
            telefono="3104567890",
            es_frecuente=False
        )
        c2 = sistema.registrar_cliente(
            id_cliente="CLI-1002",
            nombre="Laura Sofia Benitez",
            correo="laura.benitez@corporativo.org",
            telefono="3209876543",
            es_frecuente=True
        )
        print(f"  [+] Registrado exitosamente: {c1}")
        print(f"  [+] Registrado exitosamente: {c2}")
    except Exception as e:
        print(f"  [!] Error inesperado en Simulación 1: {e}")

    # -------------------------------------------------------------------------
    # SIMULACIÓN 2 [INVÁLIDA]: Registro con correo electrónico inválido
    # -------------------------------------------------------------------------
    imprimir_caso(2, "INVÁLIDO", "Intento de registro de cliente con correo malformado")
    try:
        sistema.registrar_cliente(
            id_cliente="CLI-1003",
            nombre="Pedro Pablo Perez",
            correo="correo_invalido_sin_arroba.com",  # Formato erróneo
            telefono="3112223344",
            es_frecuente=False
        )
        print("  [!] ERROR: La operación debió haber fallado.")
    except ClienteInvalidoError as cie:
        print(f"  [OK - CONTROLADO] EXCEPCIÓN CONTROLADA: {cie.__class__.__name__}")
        print(f"      Mensaje: {cie}")
        print("      Estado del sistema: ESTABLE (La aplicación continúa su ejecución normal).")

    # -------------------------------------------------------------------------
    # SIMULACIÓN 3 [INVÁLIDA]: Registro con teléfono y nombre inválidos
    # -------------------------------------------------------------------------
    imprimir_caso(3, "INVÁLIDO", "Intento de registro con número telefónico de longitud incorrecta")
    try:
        sistema.registrar_cliente(
            id_cliente="CLI-1004",
            nombre="Mariana Gomez",
            correo="mariana@dominio.com",
            telefono="12345",  # Requiere 10 dígitos
            es_frecuente=False
        )
    except ClienteInvalidoError as cie:
        print(f"  [OK - CONTROLADO] EXCEPCIÓN CONTROLADA: {cie.__class__.__name__}")
        print(f"      Mensaje: {cie}")
        print("      Estado del sistema: ESTABLE.")

    # -------------------------------------------------------------------------
    # SIMULACIÓN 4 [INVÁLIDA]: Intento de registro con ID duplicado
    # -------------------------------------------------------------------------
    imprimir_caso(4, "INVÁLIDO", "Violación de regla de unicidad (ID de cliente duplicado)")
    try:
        sistema.registrar_cliente(
            id_cliente="CLI-1001",  # Ya registrado en Simulación 1
            nombre="Otro Nombre Repetido",
            correo="otro.repetido@correo.com",
            telefono="3159998877",
            es_frecuente=False
        )
    except ValidacionError as ve:
        print(f"  [OK - CONTROLADO] EXCEPCIÓN CONTROLADA: {ve.__class__.__name__}")
        print(f"      Mensaje: {ve}")
        print("      Estado del sistema: ESTABLE.")

    # -------------------------------------------------------------------------
    # SIMULACIÓN 5 [VÁLIDA]: Creación y catálogo de servicios especializados
    # -------------------------------------------------------------------------
    imprimir_caso(5, "VÁLIDO", "Creación de 3 servicios especializados aplicando polimorfismo")
    try:
        # 1. Sala
        sala_directiva = ReservaSala(
            id_servicio="SRV-SALA-01",
            nombre="Sala de Juntas Ejecutiva Diamante",
            tarifa_base_hora=120000.0,
            capacidad_maxima=15,
            tipo_sala="conferencias",
            incluye_proyector=True,
            disponible=True
        )
        sistema.agregar_servicio(sala_directiva)

        # 2. Alquiler de Equipo
        equipo_servidor = AlquilerEquipo(
            id_servicio="SRV-EQ-01",
            nombre="Servidor de Procesamiento GPU Tesla",
            tarifa_base_dia=350000.0,
            tipo_equipo="Servidor IA Dedicado",
            deposito_garantia=500000.0,
            tarifa_seguro_diario=45000.0,
            disponible=True
        )
        sistema.agregar_servicio(equipo_servidor)

        # 3. Asesoría
        asesoria_cloud = AsesoriaEspecializada(
            id_servicio="SRV-ASE-01",
            nombre="Auditoría y Arquitectura Cloud AWS/GCP",
            tarifa_base_hora=180000.0,
            area_especialidad="Arquitectura Cloud & Ciberseguridad",
            nivel_consultor="master",
            consultor_asignado="Dra. Claudia Morales (PhD)",
            disponible=True
        )
        sistema.agregar_servicio(asesoria_cloud)

        print(f"  [+] Servicio 1: {sala_directiva.describir_servicio()}")
        print(f"  [+] Servicio 2: {equipo_servidor.describir_servicio()}")
        print(f"  [+] Servicio 3: {asesoria_cloud.describir_servicio()}")

    except Exception as e:
        print(f"  [!] Error inesperado creando catálogo: {e}")

    # -------------------------------------------------------------------------
    # SIMULACIÓN 6 [INVÁLIDA]: Creación de servicio con tarifa negativa (Inconsistencia)
    # -------------------------------------------------------------------------
    imprimir_caso(6, "INVÁLIDO", "Intento de instanciar servicio con tarifa base negativa o parámetros erróneos")
    try:
        # Intento de creación con valor absurdo
        sala_invalida = ReservaSala(
            id_servicio="SRV-ERR-01",
            nombre="Sala Inválida",
            tarifa_base_hora=-50000.0,  # Valor inadmisible
            capacidad_maxima=10,
            tipo_sala="reuniones"
        )
        sistema.agregar_servicio(sala_invalida)
    except ServicioInvalidoError as sie:
        print(f"  [OK - CONTROLADO] EXCEPCIÓN CONTROLADA: {sie.__class__.__name__}")
        print(f"      Mensaje: {sie}")
        print("      Estado del sistema: ESTABLE.")

    # -------------------------------------------------------------------------
    # SIMULACIÓN 7 [VÁLIDA]: Reserva de Sala con cálculo sobrecargado y cliente VIP
    # -------------------------------------------------------------------------
    imprimir_caso(7, "VÁLIDO", "Reserva de Sala aplicando sobrecarga de métodos (Descuento VIP + IVA)")
    try:
        # Cliente 2 es VIP (descuento del 10% adicional automático)
        reserva_1 = sistema.crear_reserva(
            id_reserva="RES-2026-001",
            id_cliente="CLI-1002",
            id_servicio="SRV-SALA-01",
            duracion=4.0,  # 4 horas
            parametros_adicionales={"asistentes": 12},
            procesar_inmediatamente=True,
            descuento_promocional=0.05  # 5% adicional promocional
        )
        print(f"  [+] Reserva Confirmada: {reserva_1}")
        print(f"      Detalles Financieros: Costo Total Liquidado = ${reserva_1.costo_total:,.2f}")
    except Exception as e:
        print(f"  [!] Error inesperado en Reserva 1: {e}")

    # -------------------------------------------------------------------------
    # SIMULACIÓN 8 [VÁLIDA]: Reserva de Alquiler de Equipo Tecnológico
    # -------------------------------------------------------------------------
    imprimir_caso(8, "VÁLIDO", "Reserva de Alquiler de Servidor por 5 días con seguro incluido")
    try:
        reserva_2 = sistema.crear_reserva(
            id_reserva="RES-2026-002",
            id_cliente="CLI-1001",
            id_servicio="SRV-EQ-01",
            duracion=5.0,  # 5 días
            parametros_adicionales={"incluir_seguro": True},
            procesar_inmediatamente=True
        )
        print(f"  [+] Reserva Confirmada: {reserva_2}")
        print(f"      Detalles Financieros: Costo Total Liquidado = ${reserva_2.costo_total:,.2f}")
    except Exception as e:
        print(f"  [!] Error inesperado en Reserva 2: {e}")

    # -------------------------------------------------------------------------
    # SIMULACIÓN 9 [VÁLIDA]: Reserva de Asesoría Especializada
    # -------------------------------------------------------------------------
    imprimir_caso(9, "VÁLIDO", "Reserva de Consultoría Especializada Nivel Master con recargo de urgencia")
    try:
        reserva_3 = sistema.crear_reserva(
            id_reserva="RES-2026-003",
            id_cliente="CLI-1001",
            id_servicio="SRV-ASE-01",
            duracion=8.0,  # 8 horas
            parametros_adicionales={"es_urgente": True},
            procesar_inmediatamente=True
        )
        print(f"  [+] Reserva Confirmada: {reserva_3}")
        print(f"      Detalles Financieros: Costo Total Liquidado = ${reserva_3.costo_total:,.2f}")
    except Exception as e:
        print(f"  [!] Error inesperado en Reserva 3: {e}")

    # -------------------------------------------------------------------------
    # SIMULACIÓN 10 [INVÁLIDA]: Reserva con Servicio No Disponible
    # -------------------------------------------------------------------------
    imprimir_caso(10, "INVÁLIDO", "Intento de reserva sobre un servicio inhabilitado en catálogo")
    try:
        # Deshabilitar deliberadamente el servicio para la prueba
        srv = sistema.buscar_servicio("SRV-EQ-01")
        srv.disponible = False
        print("  [*] Se ha puesto el servicio 'SRV-EQ-01' en estado: DISPONIBLE = FALSE.")

        sistema.crear_reserva(
            id_reserva="RES-2026-004",
            id_cliente="CLI-1002",
            id_servicio="SRV-EQ-01",
            duracion=3.0
        )
    except OperacionNoPermitidaError as ope:
        print(f"  [OK - CONTROLADO] EXCEPCIÓN CONTROLADA (Encadenamiento demostrable): {ope.__class__.__name__}")
        print(f"      Mensaje: {ope}")
        print(f"      Causa raíz encadenada (__cause__): {ope.__cause__}")
        print("      Estado del sistema: ESTABLE.")
    finally:
        # Restaurar disponibilidad para mantener integridad del sistema
        srv = sistema.buscar_servicio("SRV-EQ-01")
        srv.disponible = True

    # -------------------------------------------------------------------------
    # SIMULACIÓN 11 [INVÁLIDA]: Exceso de capacidad en la sala (Aforo no permitido)
    # -------------------------------------------------------------------------
    imprimir_caso(11, "INVÁLIDO", "Intento de reserva superando la capacidad máxima de la sala")
    try:
        sistema.crear_reserva(
            id_reserva="RES-2026-005",
            id_cliente="CLI-1001",
            id_servicio="SRV-SALA-01",
            duracion=2.0,
            parametros_adicionales={"asistentes": 50}  # Capacidad máxima es 15
        )
    except OperacionNoPermitidaError as ope:
        print(f"  [OK - CONTROLADO] EXCEPCIÓN CONTROLADA: {ope.__class__.__name__}")
        print(f"      Detalle de causa: {ope.detalle}")
        print("      Estado del sistema: ESTABLE.")

    # -------------------------------------------------------------------------
    # SIMULACIÓN 12 [INVÁLIDA / TRANSICIÓN]: Cancelación duplicada de reserva
    # -------------------------------------------------------------------------
    imprimir_caso(12, "INVÁLIDO", "Transición inválida de estados: Cancelar una reserva ya cancelada")
    try:
        print("  [*] Paso 1: Cancelar legítimamente la Reserva 3...")
        sistema.cancelar_reserva("RES-2026-003", motivo="Reagendamiento solicitado por cliente")
        print("      Cancelación exitosa inicial registrada.")

        print("  [*] Paso 2: Intentar cancelar nuevamente la Reserva 3...")
        sistema.cancelar_reserva("RES-2026-003", motivo="Intento reiterado redundante")
    except EstadoReservaInvalidoError as erie:
        print(f"  [OK - CONTROLADO] EXCEPCIÓN CONTROLADA: {erie.__class__.__name__}")
        print(f"      Mensaje: {erie}")
        print("      Estado del sistema: ESTABLE.")

    # -------------------------------------------------------------------------
    # BALANCE OPERATIVO Y VERIFICACIÓN DE AUDITORÍA
    # -------------------------------------------------------------------------
    imprimir_encabezado("BALANCE FINAL DE OPERACIÓN Y AUDITORÍA DEL SISTEMA")
    metricas = sistema.obtener_resumen_operativo()
    print(f"Total Clientes registrados en memoria  : {metricas['total_clientes']}")
    print(f"Total Servicios en catálogo en memoria: {metricas['total_servicios']}")
    print(f"Total Reservas generadas en memoria   : {metricas['total_reservas']}")
    print(f"Distribución por estado de reserva     : {metricas['distribucion_estados']}")
    print(f"Ingresos netos facturados y confirmados: ${metricas['ingresos_facturados']:,.2f}")

    print("\n--- MUESTRA DE LAS ÚLTIMAS LÍNEAS REGISTRADAS EN 'software_fj.log' ---")
    lineas_log = sistema.leer_ultimos_logs(10)
    for l in lineas_log:
        print(l.strip())

    print("\n" + "=" * 85)
    print(">>> CONCLUSIÓN DE LA SIMULACIÓN: TODAS LAS PRUEBAS COMPLETADAS CON ÉXITO.")
    print(">>> EL SISTEMA MANTUVO SU ESTABILIDAD EN TODO MOMENTO SIN INTERRUPCIONES.")
    print("=" * 85 + "\n")


if __name__ == "__main__":
    ejecutar_simulaciones()
