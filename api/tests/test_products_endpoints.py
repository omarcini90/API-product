import pytest
from unittest.mock import patch
from fastapi import status


def test_get_all_products_endpoint(client):
    """Test básico para GET /api/products/ - Obtener todos los productos."""
    with patch('business_logic.product_logic.list_products') as mock_list:
        mock_list.return_value = []
        
        response = client.get("/api/products/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


def test_get_product_by_id_endpoint(client):
    """Test básico para GET /api/products/{id} - Obtener producto por ID."""
    with patch('business_logic.product_logic.get_product_details') as mock_get:
        mock_get.return_value = None
        
        response = client.get("/api/products/test-id-123")
        
        assert response.status_code == 404


def test_get_products_by_category_endpoint(client):
    """Test básico para GET /api/products/category/{category} - Filtrar por categoría."""
    with patch('business_logic.product_logic.list_products') as mock_list:
        mock_list.return_value = []
        
        response = client.get("/api/products/category/Smartphones")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


def test_compare_products_endpoint_validation(client):
    """Test básico para POST /api/products/compare - Validación de entrada."""
    invalid_request = {
        "product_ids": ["single-product-id"]
    }
    
    response = client.post("/api/products/compare", json=invalid_request)
    
    assert response.status_code in [400, 422]


def test_create_product_endpoint_validation(client):
    """Test básico para POST /api/products/ - Validación de datos requeridos."""
    invalid_request = {
        "name": "Producto Test"
    }
    
    response = client.post("/api/products/", json=invalid_request)
    
    assert response.status_code == 422


def test_health_check_docs_endpoint(client):
    """Test básico - Verificar que la aplicación está corriendo."""
    response = client.get("/docs")
    
    assert response.status_code in [200, 307, 404]


def test_health_check_openapi_endpoint(client):
    """Test básico - Verificar que OpenAPI está disponible.""" 
    response = client.get("/openapi.json")
    
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data
