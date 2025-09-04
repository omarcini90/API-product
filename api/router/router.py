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
        Lista de productos con sus detalles completos
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
        Detalles completos del producto incluyendo:
        - nombre, marca, precio
        - URL de imagen y descripción  
        - calificación y especificaciones
    """
    try:
        # Validación básica del ID
        if not product_id or len(product_id.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de producto inválido"
            )
        
        product = get_product_details(product_id.strip())
        
        # Verificar que el producto existe
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {product_id} no encontrado"
            )
            
        return product
        
    except HTTPException:
        # Re-raise HTTPExceptions tal como están
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
    
    Esta función permite comparar entre 2 y 5 productos simultáneamente,
    proporcionando información detallada de cada producto y un resumen 
    que incluye precios, calificaciones y especificaciones.
    
    Args:
        compare_request: Objeto con lista de IDs de productos a comparar
        
    Returns:
        Respuesta con:
        - Lista de productos con todos sus detalles
        - Resumen de comparación (más barato, más caro, mejor calificado)
        - Información agregada útil para la decisión de compra
        
    Raises:
        400: Si la cantidad de productos no está entre 2 y 5
        404: Si alguno de los productos no existe
        500: Error interno del servidor
    """
    try:
        # La validación de cantidad se maneja en la lógica de negocio
        comparison_result = compare_products(compare_request)
        return comparison_result
        
    except ValueError as e:
        # Errores de validación (cantidad de productos, etc.)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Verificar si es un error de productos no encontrados
        if "no encontrados" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        # Otros errores internos
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


# Endpoint adicional para obtener productos por categoría (útil para comparaciones)
@router.get("/category/{category}", response_model=List[ProductDetail])
async def get_products_by_category(category: str):
    """
    Obtiene productos filtrados por categoría.
    
    Útil para encontrar productos similares que se puedan comparar.
    
    Args:
        category: Nombre de la categoría
        
    Returns:
        Lista de productos de la categoría especificada
    """
    try:
        # Obtener todos los productos
        all_products = list_products()
        
        # Filtrar por categoría (case-insensitive)
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
    
    Este endpoint permite crear productos con toda la información necesaria
    para comparaciones posteriores, incluyendo especificaciones técnicas.
    
    Args:
        product_request: Datos del producto a crear con campos:
        - name: Nombre del producto (requerido)
        - brand: Marca del producto (requerido) 
        - price: Precio del producto > 0 (requerido)
        - category: Categoría del producto (requerido)
        - image_url: URL de la imagen (opcional)
        - description: Descripción del producto (opcional)
        - rating: Calificación 0-5 (opcional)
        - specs: Especificaciones técnicas (opcional)
        
    Returns:
        Producto creado con ID asignado automáticamente
        
    Raises:
        400: Si los datos son inválidos (campos requeridos faltantes, precio <= 0)
        500: Error interno del servidor
    """
    try:
        # Convertir request a diccionario para la lógica de negocio
        product_data = product_request.dict()
        
        # Crear producto usando lógica de negocio
        created_product = create_product_logic(product_data)
        
        return created_product
        
    except ValueError as e:
        # Errores de validación
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Errores internos
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

