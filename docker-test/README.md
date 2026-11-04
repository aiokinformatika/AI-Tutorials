# Docker and FastAPI — Development Environment Test

This project verifies that Docker Engine and Docker Compose can build and run a Python FastAPI application on Debian 13. It accompanies the article **Building a Clean AI Development Environment with Debian 13, Docker and PyCharm**.

## Prerequisites

- Debian 13 or another Docker-compatible Linux distribution
- Docker Engine running and Docker Compose available
- Permission to access the Docker daemon (the `docker` group grants root-equivalent privileges)
- Local port 8000 available

Python does not need to be installed on the host: it runs inside the container.

## Project structure

```text
docker-test/
├── README.md
├── Dockerfile
├── compose.yaml
├── requirements.txt
└── app/
    └── main.py
```

## Build and run

From the `docker-test` directory:

```bash
docker compose config --quiet
docker compose build
docker compose up -d
docker compose ps
```

The service should be running and port 8000 should be published on `127.0.0.1` only.

## Test the endpoints

```bash
curl -fsS http://127.0.0.1:8000/
echo
curl -fsS http://127.0.0.1:8000/health
echo
```

Expected responses:

```json
{"message":"Docker and FastAPI are working!","status":"ok"}
```

```json
{"status":"healthy"}
```

Interactive API documentation is available at <http://127.0.0.1:8000/docs> while the service is running.

## Inspect logs

```bash
docker compose logs --tail=30 web
```

Look for Uvicorn startup messages and HTTP `200 OK` responses.

## How the configuration works

The `Dockerfile` uses `python:3.12-slim`, installs pinned FastAPI and Uvicorn dependencies, copies `app/main.py` to `/app/main.py`, and starts `uvicorn main:app` on port 8000.

The `compose.yaml` builds the image locally, publishes container port 8000 only to host `127.0.0.1:8000`, and bind-mounts `./app:/app`. This single `app` directory is intentional: the host's `app/` maps directly to the container's `/app` directory.

The bind mount makes source changes visible in the container, but Uvicorn is **not** configured for automatic reload. After editing Python files, run:

```bash
docker compose restart web
```

This is a local development demonstration, not a production deployment.

## Stop and restart

```bash
docker compose down
```

This removes the Compose-managed containers and network but preserves the source code and built image. Restart with:

```bash
docker compose up -d
```

Do not use `docker compose down -v` unless you specifically intend to remove project volumes.

## Troubleshooting

**Docker service unavailable**

```bash
sudo systemctl is-active docker
docker info
```

**Port 8000 occupied**

```bash
sudo ss -ltnp '( sport = :8000 )'
```

**Container fails to start**

```bash
docker compose ps
docker compose logs web
```

**Dependency installation fails**

Check network connectivity and the versions pinned in `requirements.txt`. A successful image build confirms that the listed dependencies were installable in the tested environment, not that they will remain available indefinitely.

## Scope

This example does not require GPU drivers, an external database, cloud services, or host-installed Python. See the accompanying blog article for the broader Debian 13, Docker, and PyCharm installation walkthrough.
