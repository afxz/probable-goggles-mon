# Koyeb Free Plan Deployment Guide

## You only need these two Dockerfiles:
- `Dockerfile` (for API/webapp)
- `Dockerfile.bot` (for the Telegram bot)

## How to deploy:

### 1. API/Webapp Service
- Use `Dockerfile` (default name, Koyeb will pick it automatically)
- Expose port 8000
- Set env vars: `BOT_TOKEN`, `WEBAPP_URL`, `MONGO_URI`, `MONGO_DB`

### 2. Bot Service
- Use `Dockerfile.bot` (specify this file in Koyeb's advanced Docker settings)
- No port needs to be exposed
- Set the same env vars as above

### 3. Delete any extra Dockerfiles (like Dockerfile.api)

---

This setup ensures you never have duplicate bot instances and redeploys are smooth.
