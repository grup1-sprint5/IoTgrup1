"""
Esquemes Pydantic per a validar les dades que envien els sensors
i les respostes que retorna l'API.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SensorDataIn(BaseModel):
    """
    Model que representa el payload que envia la Raspberry Pi.
    Coincideix exactament amb el JSON que envia sensor_client.py.
    """
    device_id: str = Field(..., example="lightcar_01", description="Identificador únic del dispositiu")
    sensor_type: str = Field(..., example="ultrasonic", description="Tipus de sensor (ultrasonic, temperature, etc.)")
    value: float = Field(..., example=23.5, description="Valor llegit pel sensor")
    unit: str = Field(..., example="cm", description="Unitat de mesura")
    timestamp: Optional[str] = Field(
        default=None,
        example="2026-02-26 12:00:00",
        description="Marca de temps en format YYYY-MM-DD HH:MM:SS. Si no s'envia, es genera automàticament."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "device_id": "lightcar_01",
                "sensor_type": "ultrasonic",
                "value": 45.32,
                "unit": "cm",
                "timestamp": "2026-02-26 12:00:00"
            }
        }


class SensorDataOut(BaseModel):
    """
    Model de resposta després d'inserir un document a MongoDB.
    """
    id: str = Field(..., description="ObjectId de MongoDB convertit a string")
    device_id: str
    sensor_type: str
    value: float
    unit: str
    timestamp: str
    created_at: datetime

    class Config:
        populate_by_name = True


class APIResponse(BaseModel):
    """Resposta genèrica de l'API."""
    success: bool
    message: str
    data: Optional[dict] = None
