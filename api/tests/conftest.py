import pytest
from fastapi.testclient import TestClient
import sys
import os

# Agregar el directorio padre al path para importar los módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from models.product import ProductDetail


@pytest.fixture
def client():
    """Cliente de prueba para FastAPI."""
    return TestClient(app)


@pytest.fixture
def sample_product():
    """Producto de ejemplo para comparación."""
    return ProductDetail(
        id="64f1a2b3c4d5e6f7a8b9c0d1",
        name="Samsung Galaxy S23",
        brand="Samsung", 
        price=999.99,
        image_url="https://example.com/samsung-s23.jpg",
        description="Smartphone premium con cámara de 50MP",
        category="Smartphones",
        rating=4.5,
        specs={
            "screen_size": "6.1 inches",
            "storage": "128GB", 
            "ram": "8GB",
            "camera": "50MP"
        }
    )


@pytest.fixture
def sample_products_list():
    """Lista de productos para comparación."""
    return [
        ProductDetail(
            id="64f1a2b3c4d5e6f7a8b9c0d1",
            name="Samsung Galaxy S23",
            brand="Samsung",
            price=999.99,
            image_url="https://example.com/samsung-s23.jpg",
            description="Smartphone premium con cámara de 50MP",
            category="Smartphones",
            rating=4.5,
            specs={"screen_size": "6.1 inches", "storage": "128GB"}
        ),
        ProductDetail(
            id="64f1a2b3c4d5e6f7a8b9c0d2", 
            name="iPhone 15",
            brand="Apple",
            price=1199.99,
            image_url="https://example.com/iphone-15.jpg",
            description="iPhone con chip A17 Pro",
            category="Smartphones",
            rating=4.7,
            specs={"screen_size": "6.1 inches", "storage": "128GB"}
        )
    ]


@pytest.fixture
def create_product_request():
    """Request de ejemplo para crear producto."""
    return {
        "name": "Nuevo Producto",
        "brand": "MiBrand",
        "price": 299.99,
        "category": "Electronics", 
        "image_url": "https://example.com/nuevo.jpg",
        "description": "Producto de ejemplo para testing",
        "rating": 4.0,
        "specs": {"color": "black", "warranty": "1 year"}
    }
