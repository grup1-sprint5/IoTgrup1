"""
Rutes per al control de l'actuador LED de la Raspberry Pi.

Endpoints:
  POST /api/actuator          → Envia una ordre ON/OFF al LED de la Raspberry Pi
  GET  /api/actuator/status   → Consulta l'estat actual del LED
"""

import os
import httpx
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, field_validator

router = APIRouter(prefix="/api/actuator", tags=["Actuator"])

# URL base de l'API Flask que corre a la Raspberry Pi
RASPI_API_URL = os.getenv("RASPI_API_URL", "http://raspberrypi.local:5000")


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class ActuatorCommand(BaseModel):
    """Payload per a canviar l'estat del LED."""
    state: str

    @field_validator("state")
    @classmethod
    def validate_state(cls, value: str) -> str:
        upper = value.upper()
        if upper not in ("ON", "OFF"):
            raise ValueError("state must be 'ON' or 'OFF'")
        return upper


class ActuatorResponse(BaseModel):
    """Resposta genèrica de l'actuador."""
    success: bool
    message: str
    current_state: str | None = None


# ---------------------------------------------------------------------------
# POST  /api/actuator
# ---------------------------------------------------------------------------

@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ActuatorResponse,
    summary="Canvia l'estat del LED (ON / OFF)"
)
async def set_actuator_state(command: ActuatorCommand):
    """
    Reenvia l'ordre ON/OFF a l'API Flask de la Raspberry Pi.
    La Raspberry Pi activa o apaga el LED físic i retorna l'estat actual.
    """
    url = f"{RASPI_API_URL}/actuator"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(url, json={"state": command.state})
    except httpx.ConnectError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"No s'ha pogut connectar amb la Raspberry Pi a {RASPI_API_URL}"
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="La Raspberry Pi no ha respost a temps"
        )

    raspi_data = response.json()

    if response.status_code != 200 or not raspi_data.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=raspi_data.get("message", "Error desconegut a la Raspberry Pi")
        )

    return ActuatorResponse(
        success=True,
        message=f"LED canviat a {command.state}",
        current_state=raspi_data.get("current_state"),
    )


# ---------------------------------------------------------------------------
# GET  /api/actuator/status
# ---------------------------------------------------------------------------

@router.get(
    "/status",
    status_code=status.HTTP_200_OK,
    response_model=ActuatorResponse,
    summary="Consulta l'estat actual del LED"
)
async def get_actuator_status():
    """
    Consulta l'API Flask de la Raspberry Pi per obtenir l'estat actual del LED.
    """
    url = f"{RASPI_API_URL}/status"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
    except httpx.ConnectError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"No s'ha pogut connectar amb la Raspberry Pi a {RASPI_API_URL}"
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="La Raspberry Pi no ha respost a temps"
        )

    raspi_data = response.json()

    return ActuatorResponse(
        success=True,
        message="Estat obtingut correctament",
        current_state=raspi_data.get("current_state"),
    )
