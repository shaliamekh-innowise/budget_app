from app import app
from routes import healthcheck

app.include_router(healthcheck.router, tags=["Healthcheck"])

