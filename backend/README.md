# Backend – Sistema de Gestión y Portal Institucional (Tiro Federal Formosa)

Este módulo contiene el backend del sistema, implementado como una API RESTful asíncrona y modular utilizando **FastAPI**, **SQLAlchemy 2.0**, **Pydantic v2** y **SQLite** (con soporte para PostgreSQL/otros motores relacionales si se requiere).

---

## 🏛️ Arquitectura y Principios de Diseño

El backend sigue una arquitectura modular y orientada a capas basada en el dominio de negocio, promoviendo alta cohesión y bajo acoplamiento:

```text
backend/
├── app/
│   ├── api/
│   │   ├── modules/           # Módulos organizados por dominio funcional
│   │   │   ├── auth/          # Autenticación, tokens JWT, login y hashing
│   │   │   ├── users/         # Gestión de usuarios, perfiles y roles
│   │   │   ├── members/       # Socios, membresías y validación ANMaC (Legítimo Usuario)
│   │   │   ├── shifts/        # Turnero, reserva de líneas de tiro y asignación
│   │   │   ├── instructors/   # Instructores, habilitaciones y feedback
│   │   │   ├── payments/      # Cuotas, pagos de inscripciones, pases diarios
│   │   │   └── events/        # Torneos, cursos y actividades
│   │   └── main.py            # Enrutador central que integra todos los submódulos
│   ├── core/
│   │   ├── config.py          # Configuración global y variables de entorno (Pydantic Settings)
│   │   ├── db.py              # Configuración de base de datos, motor y sesión de SQLAlchemy
│   │   └── security.py        # Utilidades criptográficas, hashing de contraseñas y JWT
│   └── main.py                # Instancia principal de FastAPI, CORS, middlewares y ciclo de vida
├── tests/                     # Pruebas automatizadas (unitarias, integración y e2e)
├── Dockerfile                 # Contenedor para producción y entornos aislados
├── pyproject.toml             # Manifiesto de dependencias, scripts y configuración de herramientas
├── uv.lock                    # Archivo de bloqueo de versiones deterministas
└── README.md                  # Este documento
```

---

## 🧩 Estructura Interna de un Módulo (`app/api/modules/<dominio>/`)

Cada módulo de dominio se organiza internamente en capas bien definidas:

1. **`models.py` (Capa de Datos / ORM):**
   * Definición de entidades de base de datos utilizando el sistema declarativo moderno de SQLAlchemy 2.0 (`Mapped`, `mapped_column`, `relationship`).
2. **`schemas.py` (Capa de Validación y DTOs):**
   * Esquemas de Pydantic v2 para validación de entrada (`Create`, `Update`) y serialización de salida (`Response`, `Public`, `InDB`).
3. **`service.py` (Capa de Lógica de Negocio):**
   * Clases y funciones con la lógica de negocio pura (POO), reglas de validación (por ejemplo: vencimiento de credencial CLU/ANMaC, superposición de turnos en líneas de tiro, estado de cuotas societarias) e interacción con la sesión de base de datos.
4. **`router.py` (Capa de Controladores / Endpoints):**
   * Endpoints FastAPI (`APIRouter`) que reciben las peticiones HTTP, inyectan dependencias (`Depends`), gestionan permisos/roles e invocan los servicios correspondientes.

---

## ⚙️ Componentes Principales

### 1. Configuración y Entorno (`app/core/config.py`)
* Gestionado mediante `pydantic-settings`.
* Carga variables de entorno desde el archivo `.env` en la raíz del proyecto.
* Valida configuraciones críticas (como `SECRET_KEY`, `FIRST_SUPERUSER`, `SQLALCHEMY_DATABASE_URI`, orígenes CORS permitidos y modo `ENVIRONMENT`).

### 2. Base de Datos y Sesiones (`app/core/db.py`)
* Utiliza **SQLAlchemy 2.0** con `create_engine` y `sessionmaker`.
* Provee la dependencia `get_db()` para inyectar sesiones transaccionales seguras (`Session`) en cada endpoint mediante generadores (`yield`) con cierre automático.
* Por defecto utiliza **SQLite** para persistencia local transaccional rápida y liviana sin dependencias externas obligatorias.

### 3. Seguridad y Control de Acceso (`app/core/security.py`)
* **Hashing:** `passlib` con algoritmo `bcrypt` para almacenamiento seguro de contraseñas.
* **Tokens de Acceso:** `python-jose` para generación y verificación de tokens JWT firmados (OAuth2 Password Flow).
* **Control de Roles (RBAC):** Dependencias de FastAPI (`current_user`, `require_role`) para restringir el acceso a administradores, socios, instructores o usuarios públicos según corresponda.

---

## 🚀 Guía de Desarrollo y Puesta en Marcha

### Prerrequisitos

* **Python 3.11 o superior**
* **`uv`** como gestor ultrarrápido de paquetes y entornos virtuales.

### 1. Instalación de Dependencias

Desde el directorio `backend`:

```bash
# Crear entorno virtual y sincronizar dependencias de producción y desarrollo
uv sync --all-extras
```

### 2. Variables de Entorno

Asegúrate de contar con el archivo `.env` configurado en la raíz del proyecto (basado en `.env.example`):

```bash
cp ../.env.example ../.env
```

### 3. Ejecución del Servidor en Modo Desarrollo

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

* **Swagger UI:** `http://localhost:8000/docs`
* **ReDoc:** `http://localhost:8000/redoc`
* **OpenAPI JSON:** `http://localhost:8000/openapi.json`

---

## 🧪 Pruebas, Calidad de Código y Estándares

El proyecto sigue la metodología ágil **Extreme Programming (XP)**, enfatizando pruebas continuas, refactorización y alta calidad de código:

### Ejecutar Pruebas Automatizadas con Pytest

```bash
uv run pytest
```

Para ejecutar con cobertura:

```bash
uv run pytest --cov=app tests/
```

### Linter y Formateo con Ruff

```bash
# Verificar código y aplicar correcciones automáticas
uv run ruff check --fix .

# Formatear el código según las convenciones del proyecto
uv run ruff format .
```

### Verificación de Tipos con Mypy

```bash
uv run mypy app
```

---

## 📋 Flujo de Trabajo para Nuevas Funcionalidades

1. **Definir el modelo ORM** en `app/api/modules/<dominio>/models.py` asegurando las relaciones necesarias.
2. **Definir los esquemas Pydantic** en `app/api/modules/<dominio>/schemas.py` para peticiones y respuestas.
3. **Implementar la lógica de negocio** en `app/api/modules/<dominio>/service.py` cubriendo casos de error y validaciones de negocio.
4. **Exponer los endpoints** en `app/api/modules/<dominio>/router.py` con sus respectivas dependencias de autenticación y permisos.
5. **Registrar el router** en `app/api/main.py` mediante `api_router.include_router(...)`.
6. **Escribir pruebas** en `tests/` para validar el comportamiento esperado y los casos borde.
