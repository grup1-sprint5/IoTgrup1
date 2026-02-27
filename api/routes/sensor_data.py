"""
Rutes per a la gestió de dades de sensors.

Endpoints:
  POST /api/sensor-data        → Rep i desa una lectura de sensor
  GET  /api/sensor-data        → Retorna les últimes N lectures (per a Laravel / front-end)
  GET  /api/sensor-data/{id}   → Retorna una lectura concreta per ID
  GET  /api/sensor-data/device/{device_id} → Filtra per dispositiu
"""

from fastapi import APIRouter, HTTPException, Query, status
from datetime import datetime, timezone
from bson import ObjectId
from bson.errors import InvalidId

from api.models import SensorDataIn, APIResponse
from api.database import get_collection

router = APIRouter(prefix="/api/sensor-data", tags=["Sensor Data"])

COLLECTION_NAME = "sensor_readings"


def _doc_to_dict(doc: dict) -> dict:
    """Converteix un document MongoDB a un diccionari serialitzable (ObjectId → str)."""
    doc["id"] = str(doc.pop("_id"))
    return doc


# ---------------------------------------------------------------------------
# POST  /api/sensor-data
# ---------------------------------------------------------------------------
@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=APIResponse,
    summary="Insereix una nova lectura de sensor"
)
async def create_sensor_data(payload: SensorDataIn):
    """
    Endpoint que crida la Raspberry Pi cada 2 segons.
    Valida el payload i el desa a la col·lecció `sensor_readings` de MongoDB Atlas.
    """
    collection = get_collection(COLLECTION_NAME)

    # Si la Raspberry no envia timestamp, el generem aquí
    timestamp_str = payload.timestamp or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    document = {
        "device_id":   payload.device_id,
        "sensor_type": payload.sensor_type,
        "value":       payload.value,
        "unit":        payload.unit,
        "timestamp":   timestamp_str,
        "created_at":  datetime.now(timezone.utc),
    }

    result = await collection.insert_one(document)

    return APIResponse(
        success=True,
        message="Lectura desada correctament",
        data={
            "id":          str(result.inserted_id),
            "device_id":   payload.device_id,
            "sensor_type": payload.sensor_type,
            "value":       payload.value,
            "unit":        payload.unit,
            "timestamp":   timestamp_str,
        }
    )


# ---------------------------------------------------------------------------
# GET  /api/sensor-data
# ---------------------------------------------------------------------------
@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=APIResponse,
    summary="Obté les últimes lectures (per a Laravel)"
)
async def get_sensor_data(
    limit: int = Query(default=50, ge=1, le=500, description="Nombre màxim de resultats"),
    device_id: str = Query(default=None, description="Filtra per device_id (opcional)"),
    sensor_type: str = Query(default=None, description="Filtra per sensor_type (opcional)")
):
    """
    Retorna les últimes lectures ordenades per data descendent.
    Laravel pot cridar aquest endpoint per obtenir dades i servir-les al front-end.
    """
    collection = get_collection(COLLECTION_NAME)

    query: dict = {}
    if device_id:
        query["device_id"] = device_id
    if sensor_type:
        query["sensor_type"] = sensor_type

    cursor = collection.find(query).sort("created_at", -1).limit(limit)
    readings = [_doc_to_dict(doc) async for doc in cursor]

    return APIResponse(
        success=True,
        message=f"{len(readings)} lectures trobades",
        data={"readings": readings, "total": len(readings)}
    )


# ---------------------------------------------------------------------------
# GET  /api/sensor-data/device/{device_id}/latest
# ---------------------------------------------------------------------------
@router.get(
    "/device/{device_id}/latest",
    status_code=status.HTTP_200_OK,
    response_model=APIResponse,
    summary="Última lectura d'un dispositiu concret"
)
async def get_latest_by_device(device_id: str):
    """Retorna l'última lectura d'un dispositiu (útil per a mostrar l'estat actual al dashboard)."""
    collection = get_collection(COLLECTION_NAME)

    doc = await collection.find_one(
        {"device_id": device_id},
        sort=[("created_at", -1)]
    )

    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No s'han trobat lectures per al dispositiu '{device_id}'"
        )

    return APIResponse(
        success=True,
        message="Última lectura trobada",
        data=_doc_to_dict(doc)
    )


# ---------------------------------------------------------------------------
# GET  /api/sensor-data/{id}
# ---------------------------------------------------------------------------
@router.get(
    "/{reading_id}",
    status_code=status.HTTP_200_OK,
    response_model=APIResponse,
    summary="Obté una lectura per ID de MongoDB"
)
async def get_sensor_data_by_id(reading_id: str):
    """Retorna un document concret de MongoDB per ObjectId."""
    collection = get_collection(COLLECTION_NAME)

    try:
        object_id = ObjectId(reading_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'ID proporcionat no és un ObjectId vàlid de MongoDB"
        )

    doc = await collection.find_one({"_id": object_id})

    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No s'ha trobat cap lectura amb l'ID '{reading_id}'"
        )

    return APIResponse(
        success=True,
        message="Lectura trobada",
        data=_doc_to_dict(doc)
    )
