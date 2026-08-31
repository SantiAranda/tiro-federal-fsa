# Sistema Web de Gestión y Portal Institucional – Tiro Federal Formosa

Sistema web integral diseñado para digitalizar, centralizar y optimizar la administración interna del **Tiro Federal Formosa**, así como para brindar un portal institucional público accesible para la comunidad.

Este proyecto se desarrolla en el marco de la cátedra **Ingeniería de Software III** de la carrera **Licenciatura en Sistemas de Información** en la **Universidad de la Cuenca del Plata (Sede Formosa)**.

---

## 👥 Integrantes y Cátedra

* **Docente a cargo:** Dr. Marcelo Toledo
* **Equipo de Desarrollo:**
  * Santiago Nicolas Aranda – DNI 45.901.018
  * Lourdes Antonella Bordón Sbardella – DNI 42.993.948
  * Sofia Antonela Lujan – DNI 44.464.918

---

## 🎯 Contexto y Problemática

El **Tiro Federal Formosa** (fundado el 1 de septiembre de 1911) es una institución histórica con más de 100 socios. Actualmente, la organización gestiona sus registros administrativos, asistencias, cobros de cuotas y asignación de turnos de tiro de manera manual mediante planillas en papel y cuadernos.

### Objetivos del Sistema

1. **Portal Institucional:** Difundir la historia, normativas de seguridad, cursos de tiro, eventos y vías de contacto del club hacia la comunidad.
2. **Sistema de Gestión Administrativa:** Digitalizar el padrón de socios, control de cuotas/pagos, agenda de turnos en líneas de tiro, asignación de instructores matriculados y validación de Legítimos Usuarios.

---

## 🚀 Funcionalidades Principales

* **Portal Público:** Información institucional, historia, ubicación del predio (Ruta Nacional N.° 11, Km 1134), cursos disponibles y decálogo de seguridad para usuarios.
* **Gestión de Socios y Roles:** Registro y control de estados de membresías, roles diferenciados (Presidente/Administrador, Socio, Instructor y Usuario General) y seguimiento de condición de Legítimo Usuario (normativas ANMaC/RENAR).
* **Turnero y Asignación de Instructores:** Reserva de líneas de tiro (edificio principal y tiro práctico), asignación personalizada de instructores y módulo de feedback/evaluación del servicio.
* **Gestión de Pagos:** Registro de inscripciones, cuotas mensuales, pases diarios y consulta de estados de pago.
* **Eventos y Cursos:** Publicación y administración de torneos, cursos de capacitación e inscripciones online.

---

## 🛠️ Stack Tecnológico y Herramientas

* **Backend:** Python con **FastAPI** (arquitectura modular orientada a objetos, endpoints RESTful y validaciones con Pydantic).
* **Base de Datos:** **SQLite** (persistencia relacional transaccional local con SQLAlchemy 2.0).
* **Frontend:** **HTML5, CSS3 y JavaScript** nativo (diseño responsivo, ligero y de carga rápida).
* **Contenerización y Despliegue:** **Docker** y **Docker Compose** (`compose.yml`).
* **Control de Versiones y Metodología:** **Git / GitHub** en estructura Monorepo, gestionado bajo la metodología ágil **Extreme Programming (XP)** y tableros en **Trello**.
* **Tooling y Entorno:** Gestor de paquetes y entornos con **`uv`**, linter/formateador con **`ruff`** y comprobación de tipos con **`mypy`**.

---

## 📁 Estructura del Repositorio (Monorepo)

```text
fsa-formosa/
├── .env.example               # Plantilla de variables de entorno del proyecto
├── compose.yml                # Orquestación de servicios para contenedores Docker
├── README.md                  # Documentación principal del repositorio
│
├── backend/                   # Módulo de backend (API REST con FastAPI)
│   ├── app/
│   │   ├── api/               # Definición y registro de rutas de la API
│   │   │   ├── modules/       # Módulos organizados por dominio (socios, turnos, pagos, etc.)
│   │   │   └── main.py        # Agrupador central de routers
│   │   ├── core/              # Configuraciones de entorno (config.py), seguridad y DB (db.py)
│   │   └── main.py            # Punto de entrada de la aplicación FastAPI (CORS, lifespan, app)
│   ├── tests/                 # Suite de pruebas unitarias y de integración (Pytest)
│   ├── Dockerfile             # Imagen Docker para el entorno de backend
│   ├── pyproject.toml         # Configuración de dependencias, scripts, ruff y mypy
│   ├── uv.lock                # Bloqueo de dependencias reproducibles con uv
│   └── README.md              # Guía de arquitectura y desarrollo del backend
│
└── frontend/                  # Módulo de frontend (Portal Institucional y Paneles)
    ├── Dockerfile             # Imagen Docker para servir el frontend
    └── ...                    # Vistas HTML, estilos CSS y scripts JS
```

---

## ⚡ Instalación y Puesta en Marcha

### Prerrequisitos

* Python `>= 3.11`
* Gestor de paquetes [`uv`](https://docs.astral.sh/uv/) (o Docker instalado)

### 1. Clonar el Repositorio

```bash
git clone https://github.com/usuario/tiro-federal.git
cd tiro-federal
```

### 2. Configurar Variables de Entorno

Copiar el archivo de ejemplo para configurar las variables necesarias:

```bash
cp .env.example .env
```

### 3. Configurar el Entorno del Backend con `uv`

Accede a la carpeta `backend` e instala las dependencias (incluyendo herramientas de desarrollo y testing):

```bash
cd backend
uv sync --all-extras
```

### 4. Ejecutar el Servidor en Desarrollo

Desde el directorio `backend`:

```bash
uv run uvicorn app.main:app --reload
```

O directamente desde la raíz del repositorio:

```bash
uv run --directory backend uvicorn app.main:app --reload
```

La aplicación estará disponible en:
* API y Frontend: `http://localhost:8000`
* Documentación interactiva Swagger UI: `http://localhost:8000/docs`
* Documentación ReDoc: `http://localhost:8000/redoc`

### 5. Ejecución con Docker

Para levantar todos los servicios con Docker Compose:

```bash
docker compose up --build
```

---

## 🧪 Pruebas y Calidad de Código

Desde el directorio `backend` (o usando `--directory backend`):

```bash
# Ejecutar suite de pruebas
uv run pytest

# Formateo y análisis estático con Ruff
uv run ruff check --fix .
uv run ruff format .

# Verificación de tipos estáticos con Mypy
uv run mypy app
```