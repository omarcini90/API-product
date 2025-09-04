import pytest
from unittest.mock import patch
from fastapi import status


class TestCompareProductsEndpoint:
    """Pruebas para POST /api/products/compare"""
    
    @patch('router.router.compare_products_logic')
    def test_compare_products_success(self, mock_compare, client, sample_products_list):
        """Test exitoso para comparar productos."""
        # Arrange
        mock_compare.return_value = sample_products_list
        compare_request = {
            "product_ids": ["64f1a2b3c4d5e6f7a8b9c0d1", "64f1a2b3c4d5e6f7a8b9c0d2"]
        }
        
        # Act
        response = client.post("/api/products/compare", json=compare_request)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Samsung Galaxy S23"
        assert data[1]["name"] == "iPhone 15"
        mock_compare.assert_called_once()
    
    @patch('router.router.compare_products_logic')
    def test_compare_products_validation_error(self, mock_compare, client):
        """Test para error de validación - menos de 2 productos."""
        # Arrange
        mock_compare.side_effect = ValueError("Debe proporcionar al menos 2 productos para comparar")
        compare_request = {
            "product_ids": ["64f1a2b3c4d5e6f7a8b9c0d1"]  # Solo 1 producto
        }
        
        # Act
        response = client.post("/api/products/compare", json=compare_request)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "al menos 2 productos" in data["detail"]


class TestCreateProductEndpoint:
    """Pruebas para POST /api/products/"""
    
    @patch('router.router.get_product_details')
    @patch('router.router.create_product_logic')
    def test_create_product_success(self, mock_create, mock_get_details, client, 
                                   create_product_request, sample_product):
        """Test exitoso para crear producto."""
        # Arrange
        new_product_id = "64f1a2b3c4d5e6f7a8b9c0d3"
        mock_create.return_value = new_product_id
        mock_get_details.return_value = sample_product
        
        # Act
        response = client.post("/api/products/", json=create_product_request)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["message"] == "Producto creado exitosamente"
        assert data["product"]["name"] == "Samsung Galaxy S23"
        mock_create.assert_called_once()
        mock_get_details.assert_called_once_with(new_product_id)
    
    def test_create_product_invalid_data(self, client):
        """Test para datos inválidos al crear producto."""
        # Arrange
        invalid_request = {
            "name": "Test Product"
            # Faltan campos requeridos: brand, price, category, specs
        }
        
        # Act
        response = client.post("/api/products/", json=invalid_request)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestUpdateProductEndpoint:
    """Pruebas para PUT /api/products/{product_id}"""
    
    @patch('router.router.get_product_details')
    @patch('router.router.update_product_logic')
    def test_update_product_success(self, mock_update, mock_get_details, client,
                                   update_product_request, sample_product):
        """Test exitoso para actualizar producto."""
        # Arrange
        product_id = "64f1a2b3c4d5e6f7a8b9c0d1"
        mock_update.return_value = True
        updated_product = sample_product.model_copy()
        updated_product.name = "Producto Actualizado"
        updated_product.price = 399.99
        mock_get_details.return_value = updated_product
        
        # Act
        response = client.put(f"/api/products/{product_id}", json=update_product_request)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "Producto actualizado exitosamente"
        assert data["product"]["name"] == "Producto Actualizado"
        mock_update.assert_called_once()
        mock_get_details.assert_called_once_with(product_id)
    
    @patch('router.router.update_product_logic')
    def test_update_product_not_found(self, mock_update, client, update_product_request):
        """Test para producto no encontrado al actualizar."""
        # Arrange
        product_id = "64f1a2b3c4d5e6f7a8b9c0d1"
        mock_update.side_effect = Exception("Producto no encontrado")
        
        # Act
        response = client.put(f"/api/products/{product_id}", json=update_product_request)
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "no encontrado" in data["detail"]
