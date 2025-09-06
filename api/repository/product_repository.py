from bson import ObjectId
from typing import List, Optional
from config.database import get_collection
from models.product import ProductDetail


def get_products() -> List[ProductDetail]:
    """
    Obtiene todos los productos de la base de datos.
    
    Returns:
        List[ProductDetail]: Lista de productos
    """
    try:
        collection = get_collection("products")
        documents = list(collection.find())
        
        products = []
        for doc in documents:
            if '_id' in doc:
                doc['id'] = str(doc['_id'])
                del doc['_id']
            products.append(ProductDetail(**doc))
        
        return products
    except Exception as e:
        raise Exception(f"Error al obtener productos de la base de datos: {str(e)}")


def get_product_by_id(product_id: str) -> Optional[ProductDetail]:
    """
    Obtiene un producto específico por su ID.
    
    Args:
        product_id: ID del producto (string)
        
    Returns:
        Optional[ProductDetail]: Producto encontrado o None si no existe
    """
    try:
        try:
            obj_id = ObjectId(product_id)
        except Exception:
            return None
        
        collection = get_collection("products")
        document = collection.find_one({"_id": obj_id})
        
        if not document:
            return None
        
        document['id'] = str(document['_id'])
        del document['_id']
        
        return ProductDetail(**document)
        
    except Exception as e:
        raise Exception(f"Error al obtener producto {product_id}: {str(e)}")


def create_product(product_data: dict) -> ProductDetail:
    """
    Crea un nuevo producto en la base de datos.
    
    Args:
        product_data: Datos del producto
        
    Returns:
        ProductDetail: Producto creado
    """
    try:
        collection = get_collection("products")
        
        result = collection.insert_one(product_data)
        created_product = collection.find_one({"_id": result.inserted_id})
        
        created_product['id'] = str(created_product['_id'])
        del created_product['_id']
        
        return ProductDetail(**created_product)
        
    except Exception as e:
        raise Exception(f"Error al crear producto: {str(e)}")


def create_sample_products():
    """
    Crea productos de ejemplo en la base de datos.
    
    Returns:
        None
    """
    sample_products = [
        {
            "name": "Samsung Galaxy S23",
            "brand": "Samsung",
            "price": 999.99,
            "image_url": "https://example.com/samsung-s23.jpg",
            "description": "Smartphone premium con cámara de 50MP y pantalla AMOLED de 6.1 pulgadas",
            "category": "Smartphones",
            "rating": 4.5,
            "specs": {
                "screen_size": "6.1 inches",
                "storage": "128GB",
                "ram": "8GB",
                "camera": "50MP",
                "battery": "3900mAh"
            }
        },
        {
            "name": "iPhone 15",
            "brand": "Apple",
            "price": 1199.99,
            "image_url": "https://example.com/iphone-15.jpg",
            "description": "iPhone con chip A17 Pro y cámara principal de 48MP",
            "category": "Smartphones",
            "rating": 4.7,
            "specs": {
                "screen_size": "6.1 inches",
                "storage": "128GB",
                "ram": "8GB",
                "camera": "48MP",
                "battery": "3349mAh"
            }
        },
        {
            "name": "MacBook Air M2",
            "brand": "Apple",
            "price": 1499.99,
            "image_url": "https://example.com/macbook-air-m2.jpg",
            "description": "Laptop ultradelgada con chip M2 y pantalla Liquid Retina de 13.6 pulgadas",
            "category": "Laptops",
            "rating": 4.8,
            "specs": {
                "screen_size": "13.6 inches",
                "storage": "256GB SSD",
                "ram": "8GB",
                "processor": "Apple M2",
                "battery": "18 hours"
            }
        }
    ]
    
    try:
        collection = get_collection("products")
        if collection.count_documents({}) == 0:
            collection.insert_many(sample_products)
            print("Productos de ejemplo creados exitosamente")
    except Exception as e:
        print(f"Error al crear productos de ejemplo: {str(e)}")
