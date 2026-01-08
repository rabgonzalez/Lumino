---
icon: lucide/cloud-upload
---

# Despliegue
Lumino está concebido para desplegarse en un **servidor en la nube** (por ejemplo, Azure), lo que permite garantizar disponibilidad, escalabilidad y un entorno de ejecución controlado. Este despliegue se apoya en una estrategia de **integración y despliegue continuo (CI/CD)**, orientada a mantener altos estándares de calidad en cada versión del sistema.

Cada vez que se realiza un **commit** en el repositorio, se ejecuta de forma automática un **pipeline de validación** que analiza el estado del proyecto antes de permitir su despliegue. Como parte de este proceso, se utiliza **SonarQube** para evaluar la calidad del código, revisando aspectos como:

* Calidad y mantenibilidad del código.
* Posibles vulnerabilidades y riesgos de seguridad.
* Cumplimiento de buenas prácticas y estándares definidos.

Solo si el código **cumple los umbrales de calidad establecidos**, el sistema permite continuar con el despliegue automático al servidor. De este modo, Lumino garantiza que cada versión publicada ha pasado un control exhaustivo, reduciendo errores en producción y asegurando una evolución estable y segura de la plataforma.

A continuación se detallan los **aspectos necesarios para desplegar Lumino en un servidor**, junto con **estrategias de gestión de errores** y **buenas prácticas para mantener un entorno de producción sostenible**, manteniendo coherencia con la arquitectura y objetivos del proyecto.

---

## Configuración necesaria para el despliegue

Para desplegar Lumino en un servidor (por ejemplo, Azure), sería necesaria la siguiente configuración:

### Infraestructura y entorno

* **Servidor Linux** (máquina virtual o servicio gestionado).
* **Python** y entorno virtual para aislar dependencias.
* **Servidor web** (Nginx o similar) como proxy inverso.
* **Servidor WSGI** (Gunicorn o uWSGI) para ejecutar Django.
* **Base de datos externa** (por ejemplo, PostgreSQL) para producción.
* **Redis** como backend para tareas asíncronas con `django-rq`.

### Configuración de Django

* Variables de entorno para credenciales y claves sensibles.
* `DEBUG = False` y configuración adecuada de `ALLOWED_HOSTS`.
* Gestión de archivos estáticos y media.
* Configuración de correo transaccional (Brevo).
* Integración con el sistema de colas para tareas en segundo plano.

---

## Estrategias para la gestión de errores

Para manejar errores de forma eficaz, se pueden aplicar varias estrategias complementarias:

* **Logs estructurados**, diferenciando niveles (info, warning, error).
* **Captura de excepciones** en vistas críticas para evitar fallos no controlados.
* **Páginas de error personalizadas** (404, 500) para mejorar la experiencia del usuario.
* **Monitorización de errores en producción**, detectando incidencias en tiempo real.
* Uso de **tests automatizados** para prevenir regresiones antes del despliegue.

Estas estrategias permiten detectar, diagnosticar y corregir errores con rapidez, reduciendo el impacto en los usuarios.

---

## Sostenibilidad del entorno de producción

Para que el entorno de producción sea sostenible a largo plazo, se deben aplicar buenas prácticas de mantenimiento y escalabilidad:

* **Integración y despliegue continuo (CI/CD)** para automatizar pruebas y despliegues.
* **Control de calidad del código** mediante herramientas como SonarQube.
* **Escalado horizontal o vertical** según el crecimiento de la plataforma.
* **Backups periódicos** de la base de datos y datos críticos.
* **Documentación técnica actualizada** para facilitar el mantenimiento.

Aplicando estas estrategias, Lumino puede mantenerse como una plataforma estable, segura y preparada para evolucionar sin comprometer su rendimiento ni su calidad.
