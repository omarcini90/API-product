import pytest
from unittest.mock import patch
from fastapi import status


def test_get_all_products_success(client):
    """Test endpoint obtener todos los productos."""
    with patch('router.router.list_products') as mock_list:
        # Arrange
        mock_list.return_value = [
            {"id": "1", "name": "Samsung S23", "brand": "Samsung", "price": 999.99,
             "category": "Smartphones", "rating": 4.5, "specs": {}}
        ]
        
        # Act
        response = client.get("/api/products/")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Samsung S23"


def test_get_product_by_id_success(client):
    """Test endpoint obtener producto por ID."""
    with patch('router.router.get_product_details') as mock_get:
        # Arrange
        product_id = "64f1a2b3c4d5e6f7a8b9c0d1"
        mock_get.return_value = {
            "id": product_id, "name": "iPhone 15", "brand": "Apple",
            "price": 1199.99, "category": "Smartphones", "rating": 4.7,
            "image_url": "https://example.com/iphone.jpg",
            "description": "iPhone con chip A17 Pro", "specs": {"camera": "48MP"}
        }
        
        # Act
        response = client.get(f"/api/products/{product_id}")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "iPhone 15"
        assert data["id"] == product_id


def test_get_product_by_id_not_found(client):
    """Test endpoint producto no encontrado."""
    with patch('router.router.get_product_details') as mock_get:
        # Arrange
        mock_get.return_value = None
        
        # Act
        response = client.get("/api/products/invalid_id")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND


def test_compare_products_success(client):
    """Test endpoint comparar productos exitosamente."""
    with patch('router.router.compare_products') as mock_compare:
        # Arrange
        mock_compare.return_value = {
            "message": "Comparación de 2 productos completada",
            "products": [
                {"id": "1", "name": "Samsung S23", "brand": "Samsung", "price": 999.99,
                 "category": "Smartphones", "rating": 4.5, "specs": {}},
                {"id": "2", "name": "iPhone 15", "brand": "Apple", "price": 1199.99,
                 "category": "Smartphones", "rating": 4.7, "specs": {}}
            ],
            "comparison_summary": {
                "cheapest_product": "Samsung S23 - $999.99",
                "most_expensive_product": "iPhone 15 - $1199.99"
            }
        }
        
        # Act
        response = client.post("/api/products/compare", json={
            "product_ids": ["1", "2"]
        })
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["products"]) == 2
        assert "Samsung S23" in data["comparison_summary"]["cheapest_product"]


def test_compare_products_validation_error(client):
    """Test endpoint comparar productos - error de validación."""
    # Act - intentar comparar solo 1 producto
    response = client.post("/api/products/compare", json={
        "product_ids": ["1"]
    })
    
    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_products_by_category(client):
    """Test endpoint filtrar productos por categoría."""
    with patch('router.router.list_products') as mock_list:
        # Arrange
        mock_list.return_value = [
            {"id": "1", "name": "Samsung S23", "brand": "Samsung", "price": 999.99,
             "category": "Smartphones", "rating": 4.5, "specs": {}},
            {"id": "2", "name": "iPhone 15", "brand": "Apple", "price": 1199.99,
             "category": "Smartphones", "rating": 4.7, "specs": {}}
        ]
        
        # Act
        response = client.get("/api/products/category/Smartphones")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        for product in data:
            assert product["category"] == "Smartphones"


def test_create_product_endpoint_success(client):
    """Test endpoint crear producto exitosamente."""
    with patch('router.router.create_product_logic') as mock_create:
        # Arrange
        mock_create.return_value = {
            "id": "64f1a2b3c4d5e6f7a8b9c0d3",
            "name": "Nuevo Producto",
            "brand": "MiBrand",
            "price": 299.99,
            "category": "Electronics",
            "image_url": "https://example.com/nuevo.jpg",
            "description": "Producto de ejemplo",
            "rating": 4.0,
            "specs": {"color": "black", "warranty": "1 year"}
        }
        
        product_request = {
            "name": "Nuevo Producto",
            "brand": "MiBrand",
            "price": 299.99,
            "category": "Electronics", 
            "image_url": "https://example.com/nuevo.jpg",
            "description": "Producto de ejemplo",
            "rating": 4.0,
            "specs": {"color": "black", "warranty": "1 year"}
        }
        
        # Act
        response = client.post("/api/products/", json=product_request)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Nuevo Producto"
        assert data["price"] == 299.99
        mock_create.assert_called_once()


def test_create_product_endpoint_validation_error(client):
    """Test endpoint crear producto - error de validación."""
    # Arrange - producto sin nombre requerido
    invalid_product = {
        "brand": "MiBrand",
        "price": 299.99,
        "category": "Electronics"
    }
    
    # Act
    response = client.post("/api/products/", json=invalid_product)
    
    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_product_endpoint_price_validation(client):
    """Test endpoint crear producto - precio inválido."""
    # Arrange - producto con precio negativo  
    invalid_product = {
        "name": "Producto Test",
        "brand": "MiBrand",
        "price": -100.0,
        "category": "Electronics"
    }
    
    # Act
    response = client.post("/api/products/", json=invalid_product)
    
    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
