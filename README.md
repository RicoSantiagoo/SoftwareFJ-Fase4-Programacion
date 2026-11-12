# Proyecto Software FJ - Fase 4 (Programación UNAD)

**Curso:** Programación (Código: 213023)  
**Grupo:** Colaborativo  
**Fase:** Fase 4 - Componente Práctico (Prácticas Simuladas)  
**Integrantes vinculados:**  
* Santiago Rico Hernández (Líder de Repositorio / Compilador)  
* Yojhan Estiven Castaño Santa (Módulo 4: Reservas)  
* Andrés Nieves (Módulo 3: Servicios)  

---

## ¿De qué trata el proyecto?

El objetivo de esta actividad es desarrollar una aplicación orientada a objetos en **Python 3** para la empresa **Software FJ**, la cual se encarga de gestionar:
* Reservas de salas de juntas y conferencias.
* Alquiler de equipos tecnológicos (servidores, portátiles, etc.).
* Asesorías técnicas especializadas.

### Regla principal de la guía
La guía del curso indica que **no debemos usar bases de datos** (ni SQL ni NoSQL). Toda la información se administra en memoria mediante listas y objetos, y el registro de eventos y errores se guarda en el archivo de texto `software_fj.log`.

---

## Reparto de módulos del grupo

Para organizar el trabajo colaborativo de los 5 integrantes, dividí el proyecto en los siguientes componentes:

| Módulo | Descripción | Responsable | Estado |
| :--- | :--- | :--- | :---: |
| **Módulo 1 y 2** | Arquitectura base, excepciones personalizadas y clase Cliente con validaciones. | Santiago Rico Hernández | **Listo** |
| **Módulo 3** | Clase abstracta Servicio y servicios derivados (ReservaSala, AlquilerEquipo, AsesoriaEspecializada) con polimorfismo. | Andrés Nieves | **Asignado** |
| **Módulo 4** | Clase Reserva con estados (creada, confirmada, cancelada) y control de excepciones. | Yojhan Estiven Castaño Santa | **Listo** |
| **Módulo 5** | Fachada/orquestador del sistema en memoria con listas nativas (`SistemaGestionFJ`). | *Por definir* | Pendiente |
| **Módulo 6** | Pruebas unitarias completas y batería de simulaciones en `main.py`. | *Por definir* | Pendiente |

---

## Mi aporte inicial (Santiago Rico Hernández)

En esta primera entrega dejo montada la estructura del proyecto y el módulo de clientes:

1. **`src/models/base.py`:** Clase abstracta `EntidadSistema` con el ID y fecha de creación para que las demás clases hereden de ella.
2. **`src/exceptions/custom_exceptions.py`:** Jerarquía de excepciones personalizadas (`SoftwareFJError`, `ClienteInvalidoError`, etc.) para atrapar errores sin que el programa se cierre.
3. **`src/models/cliente.py`:** Clase `Cliente` con getters y setters (`@property`). Valida que el correo tenga formato correcto (`nombre@correo.com`) y que el teléfono celular tenga exactamente 10 dígitos.
4. **`src/utils/logger.py`:** Configuración para guardar los eventos en `software_fj.log`.
5. **`tests/test_cliente.py`:** 7 pruebas unitarias con `unittest` para verificar que las validaciones funcionen.

---

## Guía paso a paso para los compañeros (Cómo subir su parte)

Sigan estos pasos sencillos para subir su código al repositorio sin complicaciones:

### Paso 1: Clonar o actualizar el proyecto en su computador
Abran la terminal (PowerShell o Git Bash) en su computador y ejecuten:
```bash
git clone https://github.com/RicoSantiagoo/SoftwareFJ-Fase4-Programacion.git
cd SoftwareFJ-Fase4-Programacion
```
*(Si ya lo tenían clonado, simplemente ejecuten `git pull origin main` para descargar los últimos cambios).*

### Paso 2: ¿Dónde deben crear o editar su archivo?
Para mantener el proyecto ordenado, cada módulo va en su ruta correspondiente:
* **Módulo 3 (Andrés):** Creas tu código en `src/models/servicio.py`.
* **Módulo 4 (Yojhan):** Ya integrado en `src/models/reserva.py`.
* **Módulo 5:** Creas tu código en `src/services/sistema_gestion.py`.
* **Módulo 6:** Pruebas en `tests/` y simulaciones en `main.py`.

### Paso 3: Guardar y subir sus cambios
Cuando terminen de escribir o probar su código, ejecutan estos comandos en su terminal:
```bash
git add .
git commit -m "feat: aporte modulo - nombre del companero"
git push origin main
```
¡Y listo! Con eso su aporte queda sincronizado directamente en la rama principal con su autoría en GitHub.

---

## Cómo probar lo que está hecho actualmente

* Para ejecutar la prueba en consola del sistema:
  ```bash
  python main.py
  ```

* Para ejecutar las pruebas unitarias automáticas:
  ```bash
  python -m unittest discover tests
  ```
