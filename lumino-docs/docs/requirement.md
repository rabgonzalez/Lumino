---
icon: lucide/shield-alert
---

# Requisitos del proyecto

## Requisitos funcionales

## Requisitos no funcionales

## Restricciones
El desarrollo de **Lumino** no se ve condicionado únicamente por decisiones técnicas, sino también por una combinación de factores **económicos, legales, organizativos y tecnológicos** que influyen de forma directa y, en muchos casos, **limitante** en su evolución.

Desde el punto de vista **técnico**, el uso de una arquitectura relativamente sencilla y de un único proyecto Django responde tanto a las necesidades actuales como a las limitaciones de recursos. Aunque esta decisión facilita el desarrollo inicial, también impone restricciones cuando se plantea la escalabilidad. La ausencia de una arquitectura desacoplada o de microservicios obliga a replantear partes significativas del sistema si el número de usuarios crece, lo que puede ralentizar el desarrollo y aumentar la deuda técnica. Además, la dependencia de librerías externas y servicios de terceros introduce riesgos adicionales, ya que cambios en sus APIs, costes o disponibilidad pueden afectar al funcionamiento de la plataforma sin que el equipo tenga control directo sobre ellos.

En el ámbito **económico**, el presupuesto disponible condiciona de manera significativa el alcance del proyecto. El uso de servicios en la nube, herramientas de monitorización, sistemas de análisis de calidad o infraestructuras redundantes implica costes recurrentes que no siempre pueden asumirse. Esta limitación obliga a priorizar funcionalidades básicas frente a mejoras avanzadas, y retrasa la implementación de medidas que aumentarían la robustez y la seguridad del sistema. Asimismo, un presupuesto ajustado suele traducirse en un equipo de desarrollo reducido, lo que incrementa la carga de trabajo individual y limita la velocidad de evolución del proyecto.

Los **factores temporales** también afectan negativamente al desarrollo. Los plazos de entrega, especialmente en un contexto académico o formativo, obligan a tomar decisiones rápidas que no siempre son las óptimas desde el punto de vista técnico. Esto puede derivar en soluciones funcionales pero poco escalables, o en una menor cobertura de pruebas en determinadas áreas. La falta de tiempo también dificulta la refactorización continua del código, lo que aumenta el riesgo de acumulación de errores y complejidad innecesaria a largo plazo.

En cuanto a los **aspectos legales**, Lumino gestiona datos personales sensibles, como información académica y calificaciones. El cumplimiento de normativas de protección de datos impone restricciones estrictas sobre cómo se almacenan, procesan y transmiten estos datos. Implementar correctamente estas medidas requiere tiempo, conocimientos específicos y, en algunos casos, servicios adicionales, lo que incrementa la complejidad del desarrollo. Cualquier error en este ámbito puede tener consecuencias legales, lo que obliga a extremar la cautela y ralentiza la incorporación de nuevas funcionalidades.

Por último, desde una perspectiva **organizativa y de negocio**, la necesidad de mantener una plataforma estable mientras se siguen añadiendo mejoras genera una tensión constante entre innovación y mantenimiento. Cada nueva funcionalidad debe evaluarse no solo por su utilidad, sino por el impacto que tendrá en la estabilidad del sistema y en el esfuerzo de mantenimiento futuro. Esta realidad limita la velocidad de crecimiento del proyecto y obliga a tomar decisiones conservadoras, especialmente cuando los recursos humanos y técnicos son limitados.

En conjunto, estos factores no impiden el desarrollo de Lumino, pero sí **condicionan su ritmo, su alcance y sus decisiones técnicas**, obligando a priorizar la fiabilidad y la sostenibilidad frente a una expansión rápida o ambiciosa.

## Casos de uso