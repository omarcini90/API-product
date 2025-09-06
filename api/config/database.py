import requests
import time
from loguru import logger
from opentelemetry import trace
from pymongo import MongoClient
from config.core import settings


def get_mongo_client():
    """
    Get a MongoDB client instance.
    
    Returns:
        MongoDB client
    """
    try:
        if not settings.MONGO_URI:
            raise Exception("MONGO_URI environment variable is not set. Please configure it in your .env file.")
        
        uri = settings.MONGO_URI
        if 'authSource' not in uri:
            if '?' in uri:
                uri += '&authSource=admin'
            else:
                uri += '?authSource=admin'
        
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        
        return client
    except Exception as e:
        raise Exception(f"Could not connect to MongoDB: {e}")
    

def insert_document(collection_name, document):
    """
    Insert a document into a specified MongoDB collection.
    
    Args:
        collection_name: Name of the collection
        document: Document to insert
        
    Returns:
        Inserted document ID as string
    """
    client = None
    try:
        client = get_mongo_client()
        db = client[settings.MONGO_DB_NAME]
        collection = db[collection_name]
        result = collection.insert_one(document)
        return str(result.inserted_id)
    except Exception as e:
        raise Exception(f"Could not insert document: {e}")
    finally:
        if client:
            client.close()


def find_documents(collection_name, query):
    """
    Find documents in a specified MongoDB collection based on a query.
    
    Args:
        collection_name: Name of the collection
        query: Query to filter documents
        
    Returns:
        List of documents matching the query
    """
    client = None
    try:
        client = get_mongo_client()
        db = client[settings.MONGO_DB_NAME]
        collection = db[collection_name]
        documents = list(collection.find(query))
        return documents
    except Exception as e:
        raise Exception(f"Could not find documents: {e}")
    finally:
        if client:
            client.close()
    

def update_document(collection_name, query, update):
    """
    Update documents in a specified MongoDB collection based on a query.
    
    Args:
        collection_name: Name of the collection
        query: Query to filter documents
        update: Update operations to apply
        
    Returns:
        Number of modified documents
    """
    client = None
    try:
        client = get_mongo_client()
        db = client[settings.MONGO_DB_NAME]
        collection = db[collection_name]
        result = collection.update_many(query, update)
        return result.modified_count
    except Exception as e:
        raise Exception(f"Could not update documents: {e}")
    finally:
        if client:
            client.close()


def get_collection(collection_name: str):
    """
    Obtiene una colección de MongoDB.
    
    Args:
        collection_name: Nombre de la colección
        
    Returns:
        Colección de MongoDB
    """
    try:
        client = get_mongo_client()
        db = client[settings.MONGO_DB_NAME]
        return db[collection_name]
    except Exception as e:
        raise Exception(f"Error al obtener colección {collection_name}: {str(e)}")
