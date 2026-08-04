from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings, yaml_config

app = FastAPI(
    title=yaml_config["app"]["name"],
    description=yaml_config["app"]["description"],
    version=yaml_config["app"]["version"],
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": yaml_config["app"]["name"],
        "version": yaml_config["app"]["version"],
        "environment": settings.app_env,
    }


@app.get("/")
async def root():
    return {"message": "NutriAgent API is running"}
