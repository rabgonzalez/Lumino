---
icon: lucide/book-open
---

# Introducción
## Objetivos de la documentación
La documentación busca dar información específica sobre algo `(en nuestro caso un programa)`, ya sea para poder entender como funciona ese programa, que funciones realiza, cómo está hecho, etc.

Es una manera de ofrecerle al resto de usuarios información que el proyecto no da por si solo.

## Alcance de la documentación
El alcance de la documentación varía dependiendo del nivel de profundidad de esa documentación.

=== "Documentación básica"
    Si haces un programa acerca de un **campus virtual**, es necesario realizar una documentación para cualquier usuario que quiera a utilizar la plataforma acerca de qué ofrece y cómo se utiliza.

=== "Documentación específica" 
    Si quieres contratar empleados para que trabajen desarrollando la plataforma, necesitarán una documentación más precisa sobre que herramientas se utilizan y cómo se estructura el proyecto, pero esa información quizás no deba de ser pública.

???+ nota
    El nivel de profundidad de la documentación también determinará cómo se comparte esa documentación, habrá casos en los que la documentación será de acceso público `(como este)`, y otros casos en los que la información será privada y el acceso estará restringido.

## Software
Lumino está desarrollado en Python utilizando el framework **Django**, que proporciona una arquitectura robusta basada en el patrón MTV[^1]. **Django** facilita la gestión de usuarios, autenticación, control de permisos y la interacción con la base de datos `(En nuestro caso local)`, lo que resulta especialmente adecuado para un campus virtual con distintos roles (alumnos y profesores) y flujos bien definidos.

## Librerías
<div class="grid cards" markdown>

-   ### :fontawesome-regular-image: Sorl Thumbnail

    ---
    Generación y gestión eficiente de miniaturas para los avatares de los perfiles de usuario.

-   ### :fontawesome-brands-html5: Django Markdownify

    ---
    Renderizado de contenido Markdown a HTML, utilizado para los temarios de las asignaturas.

-   ### :fontawesome-regular-envelope: Brevo

    ---
    Envío de correos electrónicos transaccionales, como notificaciones y certificados.

-   ### :fontawesome-brands-stack-overflow: Django RQ

    ---
    Ejecución de tareas en segundo plano (por ejemplo, envío de correos) mediante colas desacopladas.

-   ### :fontawesome-solid-shield: Prettyconf

    ---
    Gestión segura de variables de entorno y credenciales, como las claves de acceso a [Brevo](#brevo).

-   ### :fontawesome-solid-file-pdf: Weasyprint

    ---
    Generación de documentos PDF a partir de HTML[^2] y CSS[^3], utilizada para los certificados académicos.
</div>

Esta combinación de tecnologías permite que Lumino sea una plataforma modular, escalable y mantenible.

[^1]: Model - Template - View
[^2]: HyperText Markup Language
[^3]: Cascading Style Sheets

## Audiencia objetiva
Esta documentación no está orientada a un único perfil, sino que está diseñada para varios tipos de audiencia, cada uno con un propósito distinto. No obstante, no todos los perfiles consumirán todas las secciones.

=== "Audiencia principal (Desarrolladores)"
    Son los principales destinatarios. Utilizarán la documentación para:

    - [Comprender el diseño y la arquitectura de la aplicación](./design.md){ data-preview }.
    - [Conocer las decisiones técnicas y patrones utilizados](./implementation.md){ data-preview }.
    - [Entender la estructura del código, herramientas y dependencias](./requirement.md){ data-preview }.
    - [Configurar entornos de desarrollo y despliegue](./deploy.md){ data-preview }.

=== "Audiencias secundarias (Testers)"
    Harán uso principalmente de:

    - [La documentación de tests](./test.md){ data-preview }.
    - [Casos de uso y flujos funcionales](./design.md){ data-preview }.
    - [Guías para validar el comportamiento de la aplicación en distintos escenarios](./maintenance.md){ data-preview }.

=== "Usuarios finales (alumnos y profesores)"
    Su interacción con la documentación es parcial y guiada, centrada en:

    - [Manuales de usuario](./manual.md){ data-preview }.
    - Explicaciones funcionales del sistema.
    - Procedimientos habituales dentro de la plataforma.