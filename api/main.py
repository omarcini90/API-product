from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import sys
import os
import yaml
from loguru import logger

# Agregar el directorio actual al path para los imports
sys.path.append(os.path.dirname(__file__))

from router.router import router as products_router
from config.core import settings
from config.database import get_mongo_client


# Configurar logging
logger.add("app.log", rotation="500 MB", level=settings.LOG_LEVEL)

# Cargar especificación OpenAPI desde archivo YAML
def load_openapi_spec():
    """Carga la especificación OpenAPI desde el archivo YAML."""
    try:
        with open("openapi.yaml", "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logger.warning("Archivo openapi.yaml no encontrado, usando especificación por defecto")
        return None
    except Exception as e:
        logger.error(f"Error al cargar openapi.yaml: {e}")
        return None

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Productos - Comparador",
    description="""
    API REST para gestionar y comparar productos con FastAPI, MongoDB y Docker.
    
    ## Características principales:
    - CRUD completo de productos
    - Comparación inteligente de productos
    - Validación automática de datos
    - Documentación interactiva
    - Containerización con Docker
    
    ## Funcionalidades:
    * **Listar productos** - Obtener todos los productos disponibles
    * **Obtener detalles** - Información completa de un producto específico
    * **Crear productos** - Agregar nuevos productos a la base de datos
    * **Comparar productos** - Análisis comparativo de múltiples productos
    * **Filtrar por categoría** - Productos agrupados por tipo
    
    ## Comparación de productos:
    La funcionalidad de comparación incluye:
    - Producto más barato y más caro
    - Producto con mejor calificación
    - Marcas disponibles
    - Rango de precios
    
    ## Tecnologías:
    - FastAPI 0.104+ para la API REST
    - MongoDB 7.0 para almacenamiento
    - Pydantic para validación de datos
    - Docker para containerización
    """,
    version="1.0.0",
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Servidor de desarrollo local"
        }
    ]
)

# Cargar especificación OpenAPI personalizada
openapi_spec = load_openapi_spec()
if openapi_spec:
    # Sobrescribir la especificación OpenAPI generada automáticamente
    app.openapi_schema = openapi_spec
    logger.info("Especificación OpenAPI cargada desde openapi.yaml")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(products_router)

# Endpoint de health check
@app.get("/", tags=["Health"])
async def root():
    """
    Endpoint de verificación de estado de la API.
    """
    return {
        "message": "🚀 MELI Test - Products API está funcionando correctamente",
        "status": "healthy",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Verificación detallada de la salud del sistema.
    """
    health_status = {
        "status": "healthy",
        "timestamp": "2025-09-03T00:00:00Z",
        "version": "1.0.0",
        "components": {}
    }
    
    # Verificar MongoDB
    try:
        client = get_mongo_client()
        client.admin.command('ping')
        health_status["components"]["mongodb"] = {
            "status": "up",
            "details": "Conexión establecida correctamente"
        }
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["components"]["mongodb"] = {
            "status": "down",
            "details": f"Error de conexión: {str(e)}"
        }
    
    return health_status


# Manejo global de errores
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Recurso no encontrado",
            "path": str(request.url.path),
            "method": request.method
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Error interno del servidor: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error interno del servidor",
            "message": "Por favor, contacte al administrador del sistema"
        }
    )


# Función para ejecutar la aplicación
def start_server():
    """
    Función para iniciar el servidor con configuración optimizada.
    """
    logger.info("🔧 Configurando servidor...")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,  # Solo para desarrollo
        reload_dirs=["."],  # Directorio actual para recarga automática
        log_level="info",
        access_log=True,
        use_colors=True,
    )


if __name__ == "__main__":
    logger.info("🎯 Iniciando MELI Test - Products API...")
    start_server()