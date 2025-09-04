import pytest
from unittest.mock import patch, Mock
from business_logic.product_logic import list_products, get_product_details, compare_products, create_product_logic
from models.product import ProductDetail, ProductCompareRequest


def test_list_products_success():
    """Test obtener lista de productos exitosamente."""
    with patch('business_logic.product_logic.get_products') as mock_get:
        # Arrange - preparar datos de prueba
        mock_products = [
            ProductDetail(
                id="1", name="Samsung S23", brand="Samsung", price=999.99,
                category="Smartphones", rating=4.5, specs={"storage": "128GB"}
            )
        ]
        mock_get.return_value = mock_products
        
        # Act - ejecutar función
        result = list_products()
        
        # Assert - verificar resultados
        assert len(result) == 1
        assert result[0].name == "Samsung S23"
        mock_get.assert_called_once()


def test_get_product_details_success():
    """Test obtener producto específico exitosamente."""
    with patch('business_logic.product_logic.get_product_by_id') as mock_get:
        # Arrange
        product_id = "64f1a2b3c4d5e6f7a8b9c0d1"
        mock_product = ProductDetail(
            id=product_id, name="iPhone 15", brand="Apple", price=1199.99,
            category="Smartphones", rating=4.7, specs={"camera": "48MP"}
        )
        mock_get.return_value = mock_product
        
        # Act
        result = get_product_details(product_id)
        
        # Assert
        assert result.name == "iPhone 15"
        assert result.id == product_id
        mock_get.assert_called_once_with(product_id)


def test_get_product_details_not_found():
    """Test producto no encontrado."""
    with patch('business_logic.product_logic.get_product_by_id') as mock_get:
        # Arrange
        mock_get.return_value = None
        
        # Act
        result = get_product_details("invalid_id")
        
        # Assert
        assert result is None


def test_compare_products_success():
    """Test comparar productos exitosamente."""
    with patch('business_logic.product_logic.get_product_by_id') as mock_get:
        # Arrange
        products = [
            ProductDetail(id="1", name="Samsung S23", brand="Samsung", price=999.99, category="Smartphones", rating=4.5, specs={}),
            ProductDetail(id="2", name="iPhone 15", brand="Apple", price=1199.99, category="Smartphones", rating=4.7, specs={})
        ]
        mock_get.side_effect = products
        
        request = ProductCompareRequest(product_ids=["1", "2"])
        
        # Act
        result = compare_products(request)
        
        # Assert
        assert len(result.products) == 2
        assert "Samsung S23" in result.comparison_summary["cheapest_product"]
        assert "iPhone 15" in result.comparison_summary["most_expensive_product"]


def test_compare_products_validation_error():
    """Test error de validación - pocos productos."""
    # Arrange
    request = ProductCompareRequest(product_ids=["1"])  # Solo un producto
    
    # Act & Assert
    with pytest.raises(ValueError, match="al menos 2 productos"):
        compare_products(request)


@patch('business_logic.product_logic.create_product')
def test_create_product_success(mock_create):
    """Test crear producto exitosamente."""
    # Arrange
    product_data = {
        "name": "Nuevo Producto",
        "brand": "MiBrand",
        "price": 299.99,
        "category": "Electronics",
        "image_url": "https://example.com/nuevo.jpg",
        "description": "Producto de ejemplo",
        "rating": 4.0,
        "specs": {"color": "black", "warranty": "1 year"}
    }
    
    expected_product = ProductDetail(
        id="64f1a2b3c4d5e6f7a8b9c0d3",
        name="Nuevo Producto",
        brand="MiBrand", 
        price=299.99,
        category="Electronics",
        rating=4.0,
        specs={"color": "black", "warranty": "1 year"}
    )
    mock_create.return_value = expected_product
    
    # Act
    result = create_product_logic(product_data)
    
    # Assert
    assert result.name == "Nuevo Producto"
    assert result.price == 299.99
    mock_create.assert_called_once_with(product_data)


def test_create_product_validation_no_name():
    """Test error de validación - nombre faltante."""
    # Arrange
    product_data = {
        "brand": "MiBrand",
        "price": 299.99,
        "category": "Electronics"
    }
    
    # Act & Assert
    with pytest.raises(ValueError, match="nombre del producto es requerido"):
        create_product_logic(product_data)


def test_create_product_validation_invalid_price():
    """Test error de validación - precio inválido."""
    # Arrange
    product_data = {
        "name": "Test Product",
        "brand": "MiBrand", 
        "price": -100.0,
        "category": "Electronics"
    }
    
    # Act & Assert
    with pytest.raises(ValueError, match="precio debe ser mayor a 0"):
        create_product_logic(product_data)
