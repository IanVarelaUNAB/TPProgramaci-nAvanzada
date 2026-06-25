# Sistema de Gestión Académica

## Descripción

Este proyecto consiste en un sistema de gestión académica desarrollado en Python utilizando Programación Orientada a Objetos (POO).

La aplicación permite administrar estudiantes, docentes, cursos e inscripciones mediante una interfaz de consola.

### Funcionalidades principales

* Alta de estudiantes.
* Alta de docentes.
* Alta de cursos.
* Inscripción de estudiantes en cursos.
* Búsqueda de estudiantes por ID, nombre o correo electrónico.
* Listado de estudiantes, docentes, cursos e inscripciones.
* Eliminación de registros con validaciones de integridad.

---

![Uploading DiagramaUML_PA.png…]()

---

## Tecnologías utilizadas

* Python 3
* Programación Orientada a Objetos (POO)
* JSON
* Biblioteca estándar de Python (`dataclasses`, `json`, `pathlib`, `abc`, `datetime`)

---

## Estructura del proyecto

```text
Proyecto/
│
├── main.py
├── modelos.py
├── repositorios.py
├── busqueda.py
├── data.json
└── README.md
```

### Descripción de los archivos

* **main.py**: interfaz de usuario y menú principal.
* **modelos.py**: entidades del dominio (Persona, Estudiante, Docente, Curso e Inscripción).
* **repositorios.py**: lógica de negocio, validaciones y persistencia.
* **busqueda.py**: implementación de estrategias de búsqueda.
* **data.json**: almacenamiento de los datos.
* **README.md**: documentación del proyecto.

---

## Ejecución del proyecto

### Requisitos

* Python 3.10 o superior.

### Ejecutar la aplicación

Desde una terminal ubicada en la carpeta del proyecto:

```bash
python main.py
```
---

## Conceptos de POO aplicados

* Herencia
* Polimorfismo
* Abstracción
* Encapsulamiento
* Agregación
* Patrón de diseño Strategy

---

## Persistencia

La información se almacena en el archivo `data.json`.

Al iniciar la aplicación, los datos se cargan automáticamente desde dicho archivo. Al salir, los cambios realizados se guardan nuevamente para mantener la información entre ejecuciones.
