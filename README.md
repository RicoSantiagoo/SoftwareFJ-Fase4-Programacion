# Sistema Integral de Gestión de Clientes, Servicios y Reservas — Software FJ

**Universidad Nacional Abierta y a Distancia (UNAD)**  
**Escuela de Ciencias Básicas, Tecnología e Ingeniería (ECBTI)**  
**Programa:** Ingeniería de Sistemas  
**Curso:** Programación (Código: 213023)  
**Actividad:** Fase 4 — Componente Práctico (Prácticas Simuladas)  
**Líder y Creador del Repositorio:** Santiago Rico Hernández  

---

## 1. Descripción del Proyecto

El presente proyecto corresponde al desarrollo colaborativo de una solución de software orientada a objetos en **Python 3** para la empresa tecnológica corporativa **Software FJ**, la cual suministra:
1. **Reservas de salas** físicas para juntas, capacitaciones y conferencias.
2. **Alquiler de hardware y equipamiento** tecnológico (servidores, kits audiovisuales, estaciones de trabajo).
3. **Asesorías especializadas** de consultoría informática (arquitectura cloud, ciberseguridad, IA).

### Directriz Académica Central (Sin Motores de Bases de Datos)
En estricto cumplimiento con la guía de actividades de la UNAD, el sistema **no utiliza ningún motor de base de datos relacional ni NoSQL**. Toda la gestión se ejecuta **en memoria mediante listas nativas y objetos del dominio**. El acceso al sistema de archivos se reserva única y exclusivamente para la bitácora persistente de eventos y auditoría de excepciones (`software_fj.log`).

---

## 2. Distribución de Responsabilidades y Roles del Equipo

Con el propósito de garantizar un desarrollo colaborativo equilibrado y modular conforme a la rúbrica de evaluación, se establecen los siguientes frentes de trabajo:

| Módulo / Componente | Integrante Responsable | Rol Técnico | Estado |
| :--- | :--- | :--- | :---: |
| **Módulo 1 & 2:** Arquitectura Base, Jerarquía de Excepciones y Modelo `Cliente` | **Santiago Rico Hernández** | Creador de Repositorio & Arquitecto Base | **Completado** |
| **Módulo 3:** Catálogo de Servicios y Polimorfismo (`Servicio`, `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`) | *Pendiente por asignar* | Desarrollador de Servicios | *Por Iniciar* |
| **Módulo 4:** Máquina de Estados de Reservas (`Reserva`, confirmación, cancelación) | *Pendiente por asignar* | Desarrollador de Reservas | *Por Iniciar* |
| **Módulo 5:** Orquestador Central en Memoria (`SistemaGestionFJ` y listas nativas) | *Pendiente por asignar* | Desarrollador de Lógica de Negocio | *Por Iniciar* |
| **Módulo 6:** Suite de Pruebas Unitarias Integradas y QA (`tests/test_sistema.py`) | *Pendiente por asignar* | Ingeniero de Calidad (QA) | *Por Iniciar* |

---

## 3. Estado Actual de la Implementación (Aporte de Santiago Rico Hernández)

En esta fase inicial, he dejado configurada la base estructural del proyecto y completado los dos primeros módulos:

1. **Abstracción Base (`src/models/base.py`)**:
   - Clase abstracta `EntidadSistema` con atributos protegidos (`_id`, `_fecha_creacion`), decoradores `@property`, y contratos abstractos `@abstractmethod` para `validar()` y `a_diccionario()`.

2. **Jerarquía Completa de Excepciones Personalizadas (`src/exceptions/custom_exceptions.py`)**:
   - Clase raíz `SoftwareFJError` y subclases específicas: `ValidacionError`, `ClienteInvalidoError`, `ServicioInvalidoError`, `ParametroInvalidoError`, `DisponibilidadError`, `ServicioNoDisponibleError`, `CapacidadExcedidaError`, `OperacionNoPermitidaError`, `EstadoReservaInvalidoError`, `EntidadNoEncontradaError` y `CalculoFinancieroError`.

3. **Módulo de Clientes con Encapsulación Rigurosa (`src/models/cliente.py`)**:
   - Atributos privados protegidos (`_nombre`, `_correo`, `_telefono`, `_es_frecuente`).
   - Validación estricta de correo electrónico bajo estándar **RFC 5322** mediante expresiones regulares (`re`).
   - Validación de número telefónico móvil nacional (exactamente 10 dígitos numéricos).
   - Métodos `@property` y `@setter` que impiden la inyección de estados inconsistentes.

4. **Sistema de Auditoría y Logging (`src/utils/logger.py`)**:
   - Registro automático en archivo persistente `software_fj.log` en formato UTF-8 y consola.

5. **Pruebas Unitarias Automatizadas (`tests/test_cliente.py`)**:
   - 7 pruebas unitarias con `unittest` que certifican la encapsulación, excepciones y serialización a diccionario.

---

## 4. Guía para los Compañeros de Equipo (Cómo Colaborar)

Estimados compañeros, sigan estos pasos para integrar sus módulos en GitHub:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/RicoSantiagoo/SoftwareFJ-Fase4-Programacion.git
   cd SoftwareFJ-Fase4-Programacion
   ```

2. **Crear una rama para tu módulo asignado (ejemplo para Módulo 3):**
   ```bash
   git checkout -b feature/servicios-polimorfismo
   ```

3. **Desarrollar el código correspondiente** asegurando documentar cada función y clase, e implementar el manejo de excepciones personalizadas.

4. **Hacer commits descriptivos de tu avance:**
   ```bash
   git add .
   git commit -m "feat(servicios): implementacion de clase abstracta Servicio y servicios derivados"
   ```

5. **Subir tu rama al repositorio remoto:**
   ```bash
   git push origin feature/servicios-polimorfismo
   ```

6. **Abrir un Pull Request** en GitHub para integrar tu aporte a la rama principal.

---

## 5. Instrucciones de Ejecución

Para ejecutar la simulación demostrativa del módulo de Clientes:
```bash
python main.py
```

Para correr la suite de pruebas unitarias:
```bash
python -m unittest tests/test_cliente.py
```
