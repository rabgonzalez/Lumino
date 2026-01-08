---
icon: lucide/book
---

# Conclusiones y futuro

## Estado actual del proyecto
En su estado actual, Lumino se encuentra en fase de desarrollo local, con las funcionalidades principales ya implementadas y validadas, pero aún sin un despliegue definitivo en producción.

A día de hoy, el proyecto presenta las siguientes características:

- [x] Arquitectura base completada, siguiendo el patrón MTV[^1] de Django.
- [x] Sistema de usuarios y roles `(alumnos y profesores)` plenamente operativo.
- [x] Gestión de asignaturas, incluyendo matrícula de alumnos y asignación de profesores.
- [x] Temarios dinámicos, editables por profesores y visualizables por alumnos.
- [x] Sistema de calificaciones funcional, con control de acceso por rol.
- [x] Generación y envío de certificados en PDF, automatizada mediante tareas en segundo plano.
- [x] Cobertura de tests definida, con un enfoque TDD[^2] que valida los flujos críticos de la aplicación.

Actualmente, el proyecto se ejecuta y prueba en un entorno local, lo que permite iterar rápidamente sobre nuevas funcionalidades, mejorar la calidad del código y ampliar la cobertura de pruebas antes de abordar el despliegue en un entorno cloud con integración continua.

Este estado facilita la consolidación del sistema y sienta las bases para su futura escalabilidad y puesta en producción.

[^1]: Model - Template - View
[^2]: Test-Driven Development

## Futuras actualizaciones
El futuro de Lumino pasa por reforzar su solidez técnica, funcional y organizativa, permitiendo que la plataforma evolucione hacia un campus virtual más completo y escalable.

<div class="grid cards" markdown>

- ### :fontawesome-solid-compass-drafting: Punto de vista técnico

    ---
    - [ ] Una arquitectura desacoplada basada en APIs, facilitando la integración con aplicaciones externas y clientes móviles.
    - [ ] Una base de datos externa y escalable, preparada para soportar un mayor volumen de usuarios y concurrencia.
    - [ ] Sistemas avanzados de monitorización y logging, que permitan detectar errores y analizar el rendimiento en producción.

- ### :fontawesome-solid-gear: A nivel funcional
  
    ---
    - [ ] Un sistema de mensajería interna entre profesores y alumnos.
    - [ ] Notificaciones en tiempo real para eventos relevantes `(nuevas notas, cambios en temarios)`.
    - [ ] Historial académico y seguimiento del progreso del alumno.

- ### :fontawesome-solid-lock: Seguridad y calidad

    ---
    - [ ] Autenticación reforzada `(por ejemplo, doble factor)`.
    - [ ] Mayor cobertura de tests y análisis de seguridad automatizados.
    - [ ] Políticas de permisos más granulares.
</div>

Estas mejoras permitirían que Lumino evolucionase de un proyecto funcional y educativo a una plataforma robusta, escalable y preparada para un uso real en entornos académicos exigentes.

## Lecciones aprendidas
El desarrollo de Lumino ha supuesto una experiencia formativa clave en el proceso de aprendizaje de **Python**, permitiendo aplicar de forma práctica los conocimientos teóricos adquiridos durante el estudio del lenguaje.

A través del proyecto se ha aprendido a:

* Utilizar **Python** en un entorno real de desarrollo web.
* Trabajar con **Django** como framework principal, comprendiendo su arquitectura y flujo de trabajo.
* Diseñar una aplicación con **roles diferenciados**, control de permisos y gestión de usuarios.
* Integrar librerías externas para resolver necesidades concretas, como la generación de PDFs, el envío de correos o el renderizado de contenido dinámico.
* Aplicar buenas prácticas de desarrollo, incluyendo **tests automatizados**, control de calidad y despliegue continuo.

!!! quote "Conclusión"
    Lumino no solo ha servido como producto funcional, sino también como una herramienta de aprendizaje que ha permitido consolidar conocimientos, adquirir experiencia práctica y comprender cómo se estructura y mantiene una aplicación profesional desarrollada en Python.
