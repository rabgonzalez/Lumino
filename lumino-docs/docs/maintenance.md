---
icon: lucide/wrench
---

# Mantenimiento y actualización
Lumino ha sido diseñado con una arquitectura sencilla y eficiente, adecuada para entornos educativos de pequeño y mediano tamaño. No obstante, en caso de que la plataforma experimente un crecimiento significativo en número de usuarios, asignaturas o volumen de datos, será necesario **evolucionar su arquitectura técnica**.

---

## Plan de Escalabilidad
En una fase inicial, Lumino puede operar con una base de datos integrada y acoplada a la aplicación. Sin embargo, ante un aumento de carga, se recomienda **migrar a una base de datos externa y dedicada** (por ejemplo, PostgreSQL o MySQL gestionados), lo que permitiría:

* Mejorar el rendimiento y la concurrencia.
* Aumentar la disponibilidad y la tolerancia a fallos.
* Facilitar copias de seguridad y escalado independiente.

El acceso a la información debería realizarse mediante **APIs bien definidas**, desacoplando la capa de datos de la lógica de presentación y permitiendo una arquitectura más modular y mantenible.

---

## Futuras actualizaciones
Como línea de evolución funcional, está previsto incorporar un **sistema de mensajería interna** que permita la comunicación directa entre profesores y alumnos. Este sistema facilitará:

* Resolución de dudas académicas dentro de la plataforma.
* Comunicación contextual asociada a asignaturas concretas.
* Reducción de la dependencia de herramientas externas de mensajería.

Esta funcionalidad reforzará la interacción entre usuarios y mejorará la experiencia educativa, alineándose con el objetivo de Lumino de ofrecer un entorno académico completo y centralizado.

---

Estas mejoras permitirán que Lumino evolucione de una solución funcional y compacta a una plataforma **escalable, modular y preparada para el crecimiento futuro**.
