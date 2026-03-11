from pydantic import BaseModel


class FilterPreset(BaseModel):
    id: str
    label: str
    filter: str
    description: str
    thumbnailGradient: str


class FilterPresetListResponse(BaseModel):
    presets: list[FilterPreset]


class AppConfigResponse(BaseModel):
    brandName: str
    eventLabel: str
    watermarkText: str


class HealthResponse(BaseModel):
    status: str
    local_processing_only: bool