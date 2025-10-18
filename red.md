kraken-viewer/
├── [ C L I ] --------------------------------------------
│   └── cli/
│       └── Interfaz de línea de comandos (menús, controladores de consola).
|
├── [ A P P ] --------------------------------------------
│   └── app/
│       └── Servicios de aplicación (casos de uso, orquestación, validaciones de flujo).
|
├── [ D O M A I N ] - El Corazón del Negocio -------------
│   └── domain/
│       ├── model/
│       │   └── Entidades y Value Objects.
│       ├── repository/
│       │   └── Interfaces de Repositorio (Contratos/Puertos de la capa de Dominio).
│       └── rules/
│           └── Reglas y Servicios de Dominio.
|
├── [ I N F R A ] - Implementaciones y Adaptadores -------
│   └── infra/
│       ├── persistence/
│       │   └── Implementaciones concretas de Repositorios (e.g., JDBC).
│       ├── tx/
│       │   └── TransactionManager (manejo de commit/rollback).
│       ├── config/
│       │   └── Configuración de conexiones (DataSourceFactory).
│       └── mapper/
│           └── Conversión de datos (e.g., ResultSet -> Entidades de Dominio).
|
└── [ S H A R E D ] - Componentes Transversales ----------
    └── shared/
        ├── dto/
        │   └── Objetos de transferencia de datos entre capas.
        ├── errors/
        │   └── Excepciones y códigos de error comunes.
        └── utils/
            └── Funciones de ayuda, validaciones y formateo general.