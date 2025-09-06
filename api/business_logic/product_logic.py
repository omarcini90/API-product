from typing import List, Optional, Dict
from models.product import ProductDetail, ProductCompareRequest, ProductCompareResponse
from repository.product_repository import get_products, get_product_by_id, create_product, create_product


def list_products() -> List[ProductDetail]:
    """
    Obtiene todos los productos disponibles.
    
    Returns:
        List[ProductDetail]: Lista de productos
    """
    try:
        products = get_products()
        return products
    except Exception as e:
        raise Exception(f"Error al obtener productos: {str(e)}")


def get_product_details(product_id: str) -> Optional[ProductDetail]:
    """
    Obtiene detalles de un producto específico.
    
    Args:
        product_id: ID del producto
        
    Returns:
        Optional[ProductDetail]: Detalles del producto o None si no existe
    """
    if not product_id:
        raise ValueError("ID de producto requerido")
    
    try:
        product = get_product_by_id(product_id)
        return product
    except Exception as e:
        raise Exception(f"Error al obtener producto {product_id}: {str(e)}")


def compare_products(compare_request: ProductCompareRequest) -> ProductCompareResponse:
    """
    Compara múltiples productos y retorna sus detalles con un resumen.
    
    Args:
        compare_request: Request con IDs de productos a comparar
        
    Returns:
        ProductCompareResponse: Respuesta con productos comparados y resumen
    """
    product_ids = compare_request.product_ids
    
    if len(product_ids) < 2:
        raise ValueError("Se requieren al menos 2 productos para comparar")
    if len(product_ids) > 5:
        raise ValueError("Se pueden comparar máximo 5 productos")
    
    try:
        products = []
        not_found = []
        
        for product_id in product_ids:
            product = get_product_by_id(product_id)
            if product:
                products.append(product)
            else:
                not_found.append(product_id)
        
        if not_found:
            raise Exception(f"Productos no encontrados: {', '.join(not_found)}")
        
        comparison_summary = _generate_comparison_summary(products)
        
        return ProductCompareResponse(
            message=f"Comparación de {len(products)} productos completada",
            products=products,
            comparison_summary=comparison_summary
        )
        
    except Exception as e:
        raise Exception(f"Error al comparar productos: {str(e)}")


def _generate_comparison_summary(products: List[ProductDetail]) -> Dict[str, str]:
    """
    Genera un resumen de comparación entre productos.
    
    Args:
        products: Lista de productos a comparar
        
    Returns:
        Dict[str, str]: Diccionario con resumen de comparación
    """
    if not products:
        return {}
    
    cheapest = min(products, key=lambda p: p.price)
    most_expensive = max(products, key=lambda p: p.price)
    
    best_rated = None
    if any(p.rating for p in products if p.rating):
        best_rated = max([p for p in products if p.rating], key=lambda p: p.rating)
    
    summary = {
        "total_products": str(len(products)),
        "cheapest_product": f"{cheapest.name} - ${cheapest.price}",
        "most_expensive_product": f"{most_expensive.name} - ${most_expensive.price}",
        "price_range": f"${cheapest.price} - ${most_expensive.price}"
    }
    
    if best_rated:
        summary["best_rated"] = f"{best_rated.name} - {best_rated.rating}/5"
    
    brands = list(set(p.brand for p in products))
    summary["brands_compared"] = ", ".join(brands)
    
    return summary


def create_product_logic(product_request: dict) -> ProductDetail:
    """
    Crea un nuevo producto.
    
    Args:
        product_request: Datos del producto a crear
        
    Returns:
        ProductDetail: Producto creado
    """
    if not product_request.get("name"):
        raise ValueError("El nombre del producto es requerido")
    
    if not product_request.get("brand"):
        raise ValueError("La marca del producto es requerida")
    
    if not product_request.get("price") or product_request.get("price") <= 0:
        raise ValueError("El precio debe ser mayor a 0")
    
    if not product_request.get("category"):
        raise ValueError("La categoría del producto es requerida")
    
    try:
        created_product = create_product(product_request)
        return created_product
    except Exception as e:
        raise Exception(f"Error al crear producto: {str(e)}")