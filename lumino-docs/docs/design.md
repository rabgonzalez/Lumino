---
icon: lucide/palette
---

# Diseño del sistema

## Arquitectura del sistema

## Modelo de datos
```mermaid
flowchart LR
P[Profile] --> |1:1| h{has};
h --> |1:1| U[User];
U --> |0:N| t{teaches};
t --> |1:1| S[Subject];

subgraph E[Enrollment]
    direction TB
    e{enrolls} --> m([mark])
    e{enrolls} --> en([enrolled_at])
end

U --> |0:N| e;
e --> |0:N| S;
S --> |0:N| c{contains};
c --> |1:1| L[Lesson];
```

## Diagramas

### Diagrama de Clases

### Diagrama de Secuencia


## Decisiones de diseño