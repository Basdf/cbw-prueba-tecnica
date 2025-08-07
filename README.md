
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
    controllers/   # Controladores de la API
    repositories/  # Implementaciones de repositorios
    routes/        # Definición de rutas
  config/          # Configuración y utilidades
  domains/
    models/        # Modelos de dominio
    ports/         # Interfaces (puertos)
    services/      # Servicios de dominio
  main.py          # Punto de entrada de la aplicación
docker/
  Dockerfile
  Docker-compose.dev.yml
README.md
pyproject.toml
```

## Pasos para correr el proyecto en local con Docker Compose

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

   Si deseas levantar un servicio específico, puedes usar:
   ```sh
   docker compose -f docker/docker-compose.dev.yml up <servicio>
   ```
   Por ejemplo:
   ```sh
   docker compose -f docker/docker-compose.dev.yml up cbw-api
   docker compose -f docker/docker-compose.dev.yml up cbw-worker-beat
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

## Notas

- El proyecto incluye configuración para desarrollo y pruebas.
- Puedes modificar los servicios en `docker-compose.yml` según tus necesidades.

---
Para dudas o soporte, contacta al equipo de CBW.
