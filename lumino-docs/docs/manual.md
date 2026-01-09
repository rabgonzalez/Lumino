---
icon: lucide/file-user
---

# Manuales de usuario
Todos los usuarios acceden a **Lumino** a través de una **pantalla de inicio de sesión** común, que actúa como punto de entrada seguro a la plataforma. En esta pantalla, el usuario debe introducir su **nombre de usuario y contraseña**, los cuales son validados por el sistema de autenticación de Django. Este proceso garantiza que únicamente usuarios registrados y autorizados puedan acceder a la aplicación y a la información académica asociada a su perfil.

Una vez completado el inicio de sesión correctamente, el usuario es redirigido al **panel principal** de Lumino. Este panel funciona como un espacio central desde el que se puede consultar la información más relevante, mostrando de forma clara las **asignaturas asociadas al perfil del usuario**, ya sea como alumno matriculado o como profesor responsable. Desde este punto se accede al contenido específico de cada asignatura y a las distintas funcionalidades disponibles.

El sistema adapta automáticamente el contenido visible y las acciones permitidas en función del **rol del usuario**:

- [Manuales de usuario](#manuales-de-usuario)
  - [Manual para Alumnos](#manual-para-alumnos)
  - [Manual para Profesores](#manual-para-profesores)
  - [Manual para Administradores](#manual-para-administradores)
  - [Consideraciones finales](#consideraciones-finales)

??? Bug "Sistema de roles"
    Todos los roles acceden a la misma plataforma, pero disponen de **permisos y opciones diferentes**, lo que asegura una experiencia personalizada, coherente y segura para cada tipo de usuario.


## Manual para Alumnos
<div class="grid cards" markdown>

- ### Registro y baja de usuario

    ---
    - El alumno puede registrarse en la plataforma desde el formulario de alta.
    - En cualquier momento puede eliminar su cuenta, lo que implica la baja completa del sistema y la pérdida de acceso.

- ### Gestión de asignaturas

    ---
    - Desde su panel personal, el alumno puede:
    - Añadirse a nuevas asignaturas disponibles.
    - Eliminarse de asignaturas en las que esté inscrito.
    - La lista de asignaturas activas se muestra siempre en su perfil.

- ### Consulta de temarios

    ---
    - Cada asignatura incluye un temario estructurado.
    - El contenido se presenta de forma clara y navegable.
    - Los temarios son de solo lectura para los alumnos.

- ### Consulta de calificaciones

    ---
    - Si una asignatura tiene nota asignada, el alumno puede visualizarla desde la vista de la asignatura.
    - Las asignaturas sin nota aparecerán como pendientes de evaluación.

- ### Solicitud de certificado académico

    ---
    - Cuando el alumno tiene todas las asignaturas calificadas, puede solicitar un certificado académico.
    - El sistema genera automáticamente un PDF con sus datos y calificaciones.
    - El certificado se envía al correo electrónico del alumno.
</div>

## Manual para Profesores
<div class="grid cards" markdown>

- ### Acceso a asignaturas

    ---
    - El profesor visualiza en su panel:
    - Las asignaturas que imparte.
    - El listado de alumnos matriculados en cada una.

- ### Edición de temarios

    ---
    - El profesor puede crear y editar el contenido de los temarios.
    - El contenido se redacta en Markdown, permitiendo una estructura clara y flexible.
    - Los cambios son visibles de forma inmediata para los alumnos.

- ### Gestión de calificaciones

    ---
    - El profesor puede asignar y modificar notas de los alumnos en cada asignatura.
    - Las calificaciones se guardan por alumno y asignatura.
    - Una vez asignada la nota, el alumno puede consultarla desde su perfil.
</div>

## Manual para Administradores
El rol de administrador utiliza el panel de administración de Django, destinado a tareas de gestión avanzada y mantenimiento.
<div class="grid cards" markdown>

- ### Gestión de usuarios

    ---
    - Desde el panel de administración se puede:
    - Crear, editar y eliminar usuarios.
    - Asignar roles (alumno o profesor).
    - Gestionar perfiles y avatares.

- ### Gestión de asignaturas

    ---
- El administrador puede:
- Crear y eliminar asignaturas.
- Asignar profesores a asignaturas.
- Supervisar la relación entre alumnos y asignaturas.
  
- ### Supervisión de contenidos y notas

    ---
    - Visualizar temarios creados por los profesores.
    - Consultar y, si es necesario, corregir calificaciones.
    - Ver el estado académico de los alumnos.

- ### Gestión técnica

    ---
    - El administrador también puede:
    - Supervisar tareas en segundo plano (envío de correos).
    - Verificar la correcta generación de certificados PDF.
    - Gestionar configuraciones internas del sistema.
</div>

## Consideraciones finales
Lumino está diseñado para que:

- [x] Los alumnos tengan una experiencia clara y autónoma.
- [x] Los profesores dispongan de herramientas directas para la docencia.
- [x] Los administradores mantengan el control y la estabilidad de la plataforma.
- [x] La separación por roles garantiza seguridad, simplicidad de uso y una gestión académica coherente.