"""
Connexió a MongoDB Atlas mitjançant Motor (driver async per a FastAPI).
La URI de connexió es llegeix des de la variable d'entorn MONGODB_URI.
"""

import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI: str = os.getenv("MONGODB_URI", "")
DB_NAME: str = os.getenv("DB_NAME", "iot_lightcar")

if not MONGODB_URI:
    raise ValueError("❌ Cal definir MONGODB_URI al fitxer .env")

# Client global reutilitzable (es crea una sola vegada en arrencar l'app)
client: AsyncIOMotorClient = AsyncIOMotorClient(MONGODB_URI)
database = client[DB_NAME]


def get_collection(name: str):
    """Retorna una col·lecció de la base de dades."""
    return database[name]
