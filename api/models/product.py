from typing import Optional, Dict, List
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Modelo base para productos."""
    name: str = Field(..., description="Nombre del producto")
    brand: str = Field(..., description="Marca del producto")
    price: float = Field(..., gt=0, description="Precio del producto")
    image_url: Optional[str] = Field(None, description="URL de la imagen del producto")
    description: Optional[str] = Field(None, description="Descripción del producto")


class ProductDetail(ProductBase):
    """Modelo completo de producto con todos los detalles."""
    id: str = Field(..., description="ID único del producto")
    category: str = Field(..., description="Categoría del producto")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Calificación de 0 a 5")
    specs: Dict[str, str] = Field(default_factory=dict, description="Especificaciones técnicas")


class ProductCreateRequest(ProductBase):
    """Request para crear un nuevo producto."""
    category: str
    rating: Optional[float] = Field(None, ge=0, le=5)
    specs: Optional[Dict[str, str]] = Field(default_factory=dict)
    

class ProductUpdateRequest(BaseModel):
    """Request para actualizar un producto existente."""
    name: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    image_url: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    specs: Optional[Dict[str, str]] = None


class ProductCompareRequest(BaseModel):
    """Request para comparar múltiples productos."""
    product_ids: List[str] = Field(..., min_items=2, max_items=5, description="IDs de productos a comparar (2-5 productos)")


class ProductCompareResponse(BaseModel):
    """Respuesta de comparación de productos."""
    message: str
    products: List[ProductDetail]
    comparison_summary: Dict[str, str]