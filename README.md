
# cbw-prueba-tecnica

Prueba técnica para el puesto de Back-End Developer en CBW.

Este proyecto es una API desarrollada en Python siguiendo la arquitectura hexagonal. Utiliza FastAPI para la capa de presentación, Celery para tareas asíncronas y MongoDB como base de datos principal.

## Tecnologías principales

- Python 3.13+
- FastAPI
- Celery
- MongoDB
- Uvicorn
- Docker & Docker Compose


## Estructura del proyecto

```
app/
  adapters/
    controllers/      # Controladores de la API
    repositories/
      mongo/          # Repositorios para MongoDB
      workers/        # Repositorios para workers
    routes/           # Definición de rutas
  configs/
    celery.py         # Configuración de Celery
    debugger.py       # Configuración de depuración
    logging.py        # Configuración de logging
    mongo.py          # Configuración de MongoDB
    settings.py       # Configuración general
  domains/
    models/           # Modelos de dominio
    ports/            # Interfaces (puertos)
    services/         # Servicios de dominio
  workers/
    notify_due_task.py    # Worker para notificar tareas próximas a vencer
    report.py              # Worker para generar reportes de tareas
    review_task_status.py  # Worker para revisar el estado de tareas
  main.py              # Punto de entrada de la aplicación
docker/
  Dockerfile.api
  Dockerfile.worker
  Docker-compose.dev.yml
README.md
pyproject.toml
uv.lock
whitelist.py
```


## Endpoints expuestos

Todos los endpoints están bajo el prefijo `/api/v1/tasks`:

- `GET /api/v1/tasks` — Obtiene todas las tareas, permite filtrar por título, descripción, estado, asignado y rangos de fechas.
- `GET /api/v1/tasks/{id}` — Obtiene una tarea por su ID.
- `GET /api/v1/tasks/status/{status}` — Obtiene todas las tareas por estado (`pending`, `in_progress`, `completed`, `cancelled`).
- `POST /api/v1/tasks` — Crea una nueva tarea.
- `PUT /api/v1/tasks/{id}` — Actualiza completamente una tarea existente.
- `PATCH /api/v1/tasks/{id}` — Actualiza parcialmente una tarea.
- `DELETE /api/v1/tasks/{id}` — Elimina una tarea por su ID.
- `POST /api/v1/tasks/report` — Genera un reporte de tareas según filtros de estado, asignado y rango de fechas (ejecuta el worker - **report.py**).
- `POST /api/v1/tasks/review/{id}` — Revisa el estado de una tarea específica (ejecuta el worker - **review_task_status.py**).

## Workers habilitados

El proyecto cuenta con 3 workers principales gestionados por Celery:

- **notify_due_task.py**: Notifica a los usuarios sobre tareas próximas a vencer. Se ejecuta periódicamente y busca tareas con fecha de vencimiento cercana.
- **report.py**: Genera reportes de tareas según los filtros definidos.
- **review_task_status.py**: Revisa el estado de las tareas.

Cada worker está configurado en su propio archivo dentro de `app/workers/` y se ejecuta como tarea asíncrona mediante Celery.


## Configuración del archivo .env

Antes de levantar los servicios, debes crear un archivo `.env` en la raíz del proyecto con las siguientes variables y valores (según el docker compose):

```env
TITLE=CBW Prueba Técnica
DESCRIPTION=API para la gestión de tareas
VERSION=1.0.0
ENVIRONMENT=dev
DEBUGGER=True
MONGO_URI=mongodb://cbw:cbw@cbw-mongo:27017
MONGO_DB_NAME=cbw_db
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=rpc://guest:guest@rabbitmq:5672//
```

Puedes copiar y pegar este bloque en tu archivo `.env`. Si necesitas cambiar algún valor (por ejemplo, credenciales o nombres de base de datos), modifícalo según tu entorno.

---



## Instalación de dependencias con uv

Este proyecto utiliza [uv](https://github.com/astral-sh/uv) para la gestión rápida de dependencias en Python.

Consulta la documentación oficial de instalación de uv aquí: https://docs.astral.sh/uv/getting-started/installation/

1. Instala las dependencias del proyecto:
  ```sh
  uv sync.
  ```

2. Si usas un entorno virtual, actívalo antes de instalar:
  ```sh
  python -m venv .venv
  source .venv/bin/activate  # En Linux/Mac
  .venv\Scripts\activate    # En Windows
  ```

---

1. Clona el repositorio:
   ```sh
   git clone https://github.com/Basdf/cbw-prueba-tecnica.git
   cd cbw-prueba-tecnica
   ```

2. Levanta los servicios con Docker Compose:
   ```sh
   docker compose -f docker/docker-compose.dev.yml up --build
   ```


3. Accede a la API en [http://localhost:8001](http://localhost:8001)

  - El puerto 8001 es el expuesto por el servicio cbw-api.
  - El puerto 27017 es el expuesto por MongoDB.
  - El puerto 10007 está disponible para depuración remota.

  Puedes consultar la documentación interactiva (Swagger UI) en:
  [http://localhost:8001/docs](http://localhost:8001/docs)

   Si deseas levantar un servicio específico, puedes usar:
   ```sh
   docker compose -f docker/docker-compose.dev.yml up <servicio>
   ```
   Por ejemplo:
   ```sh
   docker compose -f docker/docker-compose.dev.yml up cbw-api
   docker compose -f docker/docker-compose.dev.yml up cbw-worker-report
   docker compose -f docker/docker-compose.dev.yml up cbw-worker-notify-due-tasks
   docker compose -f docker/docker-compose.dev.yml up cbw-worker-review-task-status
   docker compose -f docker/docker-compose.dev.yml up cbw-mongo
   docker compose -f docker/docker-compose.dev.yml up rabbitmq
   ```

4. Modo Debug (opcional):

   Para utilizar el modo debug en VS Code:
   - Asegúrate de que la variable de entorno `DEBUGGER` esté en `true` al levantar el Docker Compose (ya está configurada en el archivo de ejemplo).
   - Usa la configuración de `launch.json` incluida para conectar el depurador remoto a la API en el puerto `10007`.
   - Inicia el contenedor normalmente y luego selecciona "Python Debugger: Remote Attach" en el menú de ejecución de VS Code.
   - Esto te permitirá depurar la aplicación mientras se ejecuta dentro del contenedor Docker.

---
