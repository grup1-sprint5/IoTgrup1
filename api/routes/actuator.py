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

def raspi_api_url() -> str:
        """URL base de l'API Flask que corre a la Raspberry Pi.

        IMPORTANT: dins Docker, `raspberrypi.local` sovint no resol. Configura-ho via env:
            - RASPI_API_URL=http://192.168.x.x:5000
        """
        base = os.getenv("RASPI_API_URL") or os.getenv("ACTUATOR_URL") or "http://raspberrypi.local:5000"
        return base.rstrip("/")


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
    base = raspi_api_url()
    url = f"{base}/actuator"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json={"state": command.state})
    except httpx.ConnectError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"No s'ha pogut connectar amb la Raspberry Pi a {base}"
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="La Raspberry Pi no ha respost a temps"
        )

    try:
        raspi_data = response.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Resposta invàlida de la Raspberry Pi (no és JSON)"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=raspi_data.get("message") or f"Raspberry Pi error ({response.status_code})"
        )

    if not raspi_data.get("success"):
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
    base = raspi_api_url()
    url = f"{base}/status"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
    except httpx.ConnectError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"No s'ha pogut connectar amb la Raspberry Pi a {base}"
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="La Raspberry Pi no ha respost a temps"
        )

    try:
        raspi_data = response.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Resposta invàlida de la Raspberry Pi (no és JSON)"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=raspi_data.get("message") or f"Raspberry Pi error ({response.status_code})"
        )

    return ActuatorResponse(
        success=True,
        message="Estat obtingut correctament",
        current_state=raspi_data.get("current_state"),
    )
