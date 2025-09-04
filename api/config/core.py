import os
import json
from types import SimpleNamespace
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Validate required environment variables
mongo_uri = os.getenv("MONGO_URI")
mongo_db_name = os.getenv("MONGO_DB_NAME", "meli_test")  # Default database name

if not mongo_uri:
    print("WARNING: MONGO_URI environment variable is not set. Please create a .env file with the required configuration.")
    print("You can copy .env.example to .env and modify the values as needed.")

settings = {
    "MONGO_URI": mongo_uri,
    "MONGO_DB_NAME": mongo_db_name,
    "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
    "HOST": os.getenv("HOST", "0.0.0.0"),
    "PORT": int(os.getenv("PORT", 8000)),
    "RELOAD": os.getenv("RELOAD", "True").lower() == "true",
}

settings = SimpleNamespace(**settings)
