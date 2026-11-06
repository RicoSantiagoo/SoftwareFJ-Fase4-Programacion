# Proyecto Software FJ - Fase 4 (Programación UNAD)

**Curso:** Programación (Código: 213023)  
**Grupo:** Colaborativo  
**Fase:** Fase 4 - Componente Práctico (Prácticas Simuladas)  
**Estudiante:** Santiago Rico Hernández  

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
| **Módulo 4** | Clase Reserva con estados (creada, confirmada, cancelada) y control de excepciones. | *Pendiente compañero 3* | Por hacer |
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

## Instrucciones para los compañeros del grupo

Para unirse y subir su parte:

1. Clonar el repositorio en su computador:
   ```bash
   git clone https://github.com/RicoSantiagoo/SoftwareFJ-Fase4-Programacion.git
   cd SoftwareFJ-Fase4-Programacion
   ```

2. Crear su propia rama de trabajo (por ejemplo para el módulo 3):
   ```bash
   git checkout -b feature/servicios-polimorfismo
   ```

3. Desarrollar su módulo, documentar el código y hacer commit:
   ```bash
   git add .
   git commit -m "Implementando modulo de servicios con polimorfismo"
   ```

4. Subir la rama a GitHub:
   ```bash
   git push origin feature/servicios-polimorfismo
   ```

5. Abrir el Pull Request en GitHub para revisar y fusionar los cambios.

---

## Cómo probar lo que está hecho

* Para correr la demostración del módulo de clientes:
  ```bash
  python main.py
  ```

* Para ejecutar las pruebas unitarias:
  ```bash
  python -m unittest tests/test_cliente.py
  ```
