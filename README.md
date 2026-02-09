# Flight Booking System

Simple distributed flight booking app with:
- `client` (React + Vite)
- `server` (Flask)
- `flight-service` (Flask microservice)
- `db1`, `db2` (MySQL)
- `redis`

## Prerequisites
- Docker Desktop
- Docker Compose

## Quick Start (Windows)
From project root (`drs_tim2_`):

```powershell
.\start.bat
```

If services were already running and you want restart:

```powershell
.\RESTART.bat
```

## First Run Note
If you get error about missing env file:

`server/.env not found`

create it from template:

```powershell
Copy-Item .env.example server\.env
```

then start again.

## App URLs
- Frontend: http://localhost:5173
- Server API: http://localhost:5000
- Flight Service API: http://localhost:5001

## Useful Commands
Check status:

```powershell
docker-compose -p drs_tim2 ps
```

See logs:

```powershell
docker-compose -p drs_tim2 logs -f
```

Stop everything:

```powershell
docker-compose -p drs_tim2 down
```

Rebuild and start:

```powershell
docker-compose -p drs_tim2 up --build -d
```

## Project Structure
- `client/` - frontend
- `server/` - main backend
- `flight-service/` - flights microservice
- `docker-compose.yml` - all services

## Notes
- Project is configured to use Gmail SMTP from `server/.env`.
- `version` warning in `docker-compose.yml` is non-blocking.
