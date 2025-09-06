from fastapi import APIRouter, HTTPException, status
from typing import List
from models.product import (
    ProductDetail, 
    ProductCompareRequest,
    ProductCompareResponse,
    ProductCreateRequest
)
from business_logic.product_logic import (
    list_products,
    get_product_details,
    compare_products,
    create_product_logic
)

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("/", response_model=List[ProductDetail])
async def get_all_products():
    """
    Obtiene todos los productos disponibles.
    
    Returns:
        List[ProductDetail]: Lista de productos con sus detalles completos
    """
    try:
        products = list_products()
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/{product_id}", response_model=ProductDetail)
async def get_product_by_id(product_id: str):
    """
    Obtiene los detalles de un producto específico.
    
    Args:
        product_id: ID único del producto
        
    Returns:
        ProductDetail: Detalles completos del producto
    """
    try:
        if not product_id or len(product_id.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de producto inválido"
            )
        
        product = get_product_details(product_id.strip())
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {product_id} no encontrado"
            )
            
        return product
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.post("/compare", response_model=ProductCompareResponse)
async def compare_products_endpoint(compare_request: ProductCompareRequest):
    """
    Compara múltiples productos y devuelve sus detalles con un resumen de comparación.
    
    Args:
        compare_request: Objeto con lista de IDs de productos a comparar
        
    Returns:
        ProductCompareResponse: Respuesta con lista de productos y resumen de comparación
    """
    try:
        comparison_result = compare_products(compare_request)
        return comparison_result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        if "no encontrados" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/category/{category}", response_model=List[ProductDetail])
async def get_products_by_category(category: str):
    """
    Obtiene productos filtrados por categoría.
    
    Args:
        category: Nombre de la categoría
        
    Returns:
        List[ProductDetail]: Lista de productos de la categoría especificada
    """
    try:
        all_products = list_products()
        
        filtered_products = [
            product for product in all_products 
            if product.category.lower() == category.lower()
        ]
        
        return filtered_products
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.post("/", response_model=ProductDetail, status_code=status.HTTP_201_CREATED)
async def create_product_endpoint(product_request: ProductCreateRequest):
    """
    Crea un nuevo producto en el sistema.
    
    Args:
        product_request: Datos del producto a crear
        
    Returns:
        ProductDetail: Producto creado con ID asignado automáticamente
    """
    try:
        product_data = product_request.dict()
        created_product = create_product_logic(product_data)
        return created_product
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

