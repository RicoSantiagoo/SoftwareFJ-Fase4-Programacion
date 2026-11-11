# Proyecto Software FJ - Fase 4 (Programación UNAD)

**Curso:** Programación (Código: 213023)  
**Grupo:** Colaborativo  
**Fase:** Fase 4 - Componente Práctico (Prácticas Simuladas)  
**Integrantes vinculados:**  
* Santiago Rico Hernández (Líder de Repositorio / Compilador)  
* Yojhan Estiven Castaño Santa (Módulo 4: Reservas)  

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
| **Módulo 3** | Clase abstracta Servicio y servicios derivados (ReservaSala, AlquilerEquipo, AsesoriaEspecializada) con polimorfismo. | *Pendiente compañero 2* | Por hacer |
| **Módulo 4** | Clase Reserva con estados (creada, confirmada, cancelada) y control de excepciones. | Yojhan Estiven Castaño Santa | **En desarrollo** |
| **Módulo 5** | Fachada/orquestador del sistema en memoria con listas nativas (`SistemaGestionFJ`). | *Pendiente compañero 4* | Por hacer |
| **Módulo 6** | Pruebas unitarias completas y batería de simulaciones en `main.py`. | *Pendiente compañero 5* | Por hacer |

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

Sigan estos pasos sencillos para que no se enreden con Git:

### Paso 1: Clonar el proyecto en su computador
Abran la terminal (PowerShell o Git Bash) en su computador y ejecuten:
```bash
git clone https://github.com/RicoSantiagoo/SoftwareFJ-Fase4-Programacion.git
cd SoftwareFJ-Fase4-Programacion
```

### Paso 2: Crear su rama de trabajo (No modificar 'main' directamente)
Según el módulo que les tocó, ejecuten el comando correspondiente para crear su rama:
* **Si vas hacer el Módulo 4 (Reservas):**
  ```bash
  git checkout -b feature/gestion-reservas
  ```
* **Si vas a hacer el Módulo 3 (Servicios y Polimorfismo):**
  ```bash
  git checkout -b feature/modulo-servicios
  ```
* **Si vas a hacer el Módulo 5 (Orquestador en memoria):**
  ```bash
  git checkout -b feature/orquestador-sistema
  ```
* **Si vas a hacer el Módulo 6 (Pruebas globales y QA):**
  ```bash
  git checkout -b feature/simulaciones-qa
  ```

### Paso 3: ¿Dónde deben crear su archivo de código?
Para mantener el proyecto ordenado, cada módulo va en una carpeta específica:
* **Módulo 3:** Creas el archivo en `src/models/servicio.py`.
* **Módulo 4 (Yojhan):** Creas el archivo en `src/models/reserva.py`.
* **Módulo 5:** Creas el archivo en `src/services/sistema_gestion.py`.
* **Módulo 6:** Trabajas sobre `main.py` y creas tus pruebas en `tests/`.

### Paso 4: Guardar y subir sus cambios
Cuando terminen de escribir o probar su código, ejecutan estos 3 comandos en su terminal:
```bash
git add .
git commit -m "Aporte de mi modulo para el proyecto"
git push origin NOMBRE_DE_SU_RAMA
```
*(Reemplacen `NOMBRE_DE_SU_RAMA` por el nombre de la rama que crearon en el Paso 2, por ejemplo: `git push origin feature/gestion-reservas`).*

### Paso 5: Abrir el Pull Request en GitHub
1. Entren a la página de este repositorio en GitHub: https://github.com/RicoSantiagoo/SoftwareFJ-Fase4-Programacion
2. Les aparecerá arriba una franja amarilla con un botón verde que dice **"Compare & pull request"**.
3. Le dan clic a ese botón, escriben un título corto y presionan el botón verde **"Create pull request"**.
4. ¡Listo! Yo como líder de repositorio me encargo de revisar los cambios y fusionarlos a la rama principal.

---

## Cómo probar lo que está hecho actualmente

* Para ejecutar la prueba en consola del módulo de clientes:
  ```bash
  python main.py
  ```

* Para ejecutar las pruebas unitarias automáticas:
  ```bash
  python -m unittest tests/test_cliente.py
  ```
  ```bash
  python -m unittest tests/test_cliente.py
  ```
