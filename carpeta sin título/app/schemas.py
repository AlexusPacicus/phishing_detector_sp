# app/schemas.py
from pydantic import BaseModel, Field
from typing import Dict, Any

class PredictRequest(BaseModel):
    url: str = Field(
        ...,
        description="URL a analizar (ejemplo: https://banco.es/login)"
    )

class PredictResponse(BaseModel):
    label: int = Field(
        ...,
        description="Etiqueta de predicción (0 = legítima, 1 = phishing)"
    )
    probability: float = Field(
        ...,
        description="Probabilidad estimada de que la URL sea phishing"
    )
    threshold: float = Field(
        ...,
        description="Umbral de decisión usado por el modelo"
    )
    features: Dict[str, Any] = Field(
        ...,
        description="Diccionario con las 10 features extraídas de la URL"
    )
