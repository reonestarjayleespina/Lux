from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .data import APP_CONFIG, FILTER_PRESETS
from .schemas import AppConfigResponse, FilterPresetListResponse, HealthResponse


app = FastAPI(
    title="LUX API",
    version="0.1.0",
    summary="Minimal backend for local-first photobooth configuration.",
    description=(
        "This API intentionally avoids image upload or persistence endpoints. "
        "Captures are processed and saved only in the browser."
    ),
)

# CORS configuration from environment
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/", tags=["meta"])
def read_root() -> dict[str, str]:
    return {
        "name": "LUX API",
        "message": "Local-first photostrip capture. No server-side image storage.",
    }


@app.get("/api/health", response_model=HealthResponse, tags=["meta"])
def healthcheck() -> HealthResponse:
    return HealthResponse(status="ok", local_processing_only=True)


@app.get("/api/config", response_model=AppConfigResponse, tags=["meta"])
def get_app_config() -> AppConfigResponse:
    return AppConfigResponse(**APP_CONFIG)


@app.get(
    "/api/filter-presets",
    response_model=FilterPresetListResponse,
    tags=["filters"],
)
def list_filter_presets() -> FilterPresetListResponse:
    return FilterPresetListResponse(presets=FILTER_PRESETS)