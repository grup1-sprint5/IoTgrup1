"""
Punt d'entrada principal del microservei FastAPI per al subsistema IoT LightCar.

Inicia el servidor amb:
    uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

Documentació Swagger disponible a:
    http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.database import client
from api.routes.sensor_data import router as sensor_router


# ---------------------------------------------------------------------------
# Lifecycle: obre / tanca la connexió amb MongoDB Atlas
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestió del cicle de vida: connexió a MongoDB en arrencar, tancament en aturar."""
    print("🚀 Microservei IoT arrencant... Connectant amb MongoDB Atlas")
    yield
    print("🛑 Microservei IoT aturant... Tancant connexió MongoDB")
    client.close()


# ---------------------------------------------------------------------------
# Instància de l'aplicació
# ---------------------------------------------------------------------------
app = FastAPI(
    title="IoT LightCar – API Microservice",
    description=(
        "Microservei que rep les dades dels sensors de la Raspberry Pi "
        "i les desa a MongoDB Atlas. Laravel consumeix aquest API per a "
        "servir les dades al front-end."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS – permet peticions des de Laravel i del front-end
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # En producció: restringir als dominis de Laravel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Rutes
# ---------------------------------------------------------------------------
app.include_router(sensor_router)


# ---------------------------------------------------------------------------
# Health-check
# ---------------------------------------------------------------------------
@app.get("/health", tags=["Health"])
async def health_check():
    """Comprova que el servei és accessible (útil per a monitoratge)."""
    return {"status": "ok", "service": "IoT LightCar API"}
