∏# 📱 API de Productos - Comparador

API REST para gestionar y comparar productos con FastAPI, MongoDB y Docker.

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Cliente     │    │   FastAPI API   │    │    MongoDB      │
│   (Frontend)    │◄──►│  Puerto: 8000   │◄──►│  Puerto: 27017  │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Componentes:
- **API REST**: FastAPI con endpoints para CRUD y comparación
- **Base de Datos**: MongoDB para almacenar productos
- **Containerización**: Docker + Docker Compose
- **Admin Interface**: Mongo Express para gestionar la BD

---

## 🎯 Diseño del Código

### 1. **Models** (`models/product.py`)
Modelos de datos usando Pydantic para validación automática:

```python
ProductDetail          # Producto completo con ID
ProductCreateRequest   # Datos para crear producto
ProductCompareRequest  # Request para comparar productos
ProductCompareResponse # Respuesta con comparación
```

**Campos principales:**
- `name, brand, price` (requeridos)
- `category, rating, image_url` 
- `specs` (especificaciones técnicas)

### 2. **Business Logic** (`business_logic/product_logic.py`)
Lógica de negocio sin dependencias de BD:

```python
list_products()              # Obtener todos los productos
get_product_details(id)      # Obtener producto específico  
compare_products(request)    # Comparar múltiples productos
create_product_logic(data)   # Crear nuevo producto
```

**Funcionalidad de comparación:**
- Encuentra el más barato/caro
- Identifica el mejor calificado
- Agrupa por marcas disponibles
- Calcula rango de precios

### 3. **Repository** (`repository/product_repository.py`)
Acceso a datos MongoDB:

```python
get_products()           # SELECT * FROM products
get_product_by_id(id)    # SELECT WHERE id = ?
create_product(data)     # INSERT INTO products
```

**Características:**
- Convierte ObjectId a string automáticamente
- Manejo de errores de BD
- Validación de IDs de MongoDB

### 4. **Router** (`router/router.py`)  
Endpoints REST con documentación automática:

```python
GET    /api/products/           # Listar productos
GET    /api/products/{id}       # Producto específico
POST   /api/products/           # Crear producto
POST   /api/products/compare    # Comparar productos
GET    /api/products/category/{cat} # Filtrar por categoría
```

### 5. **Config** (`config/`)
Configuración centralizada:

```python
database.py    # Conexión a MongoDB
core.py        # Variables de entorno
```

---

## 🧪 Pruebas

### Estructura de Tests:
```
tests/
├── conftest.py              # Fixtures compartidas
├── test_business_logic.py   # Tests de lógica de negocio
└── test_products_endpoints.py # Tests de endpoints
```

### Tipos de Pruebas:

**1. Business Logic Tests:**
- Validación de datos de entrada
- Lógica de comparación de productos
- Manejo de errores

**2. Endpoint Tests:**
- Respuestas HTTP correctas (200, 201, 400, 404)
- Validación de JSON requests/responses
- Integración con mocks

### Ejecutar Tests:
```bash
# Con pytest directamente
pytest tests/ -v

# Con script incluido
./run_tests.sh
./run_tests.sh -c          # Con cobertura
./run_tests.sh -f endpoints # Archivo específico
```

---

## 🐳 Scripts Docker

### Inicio Rápido:
```bash
# 1. Hacer script ejecutable
chmod +x docker-scripts.sh

# 2. Levantar todos los servicios
./docker-scripts.sh up
```

### Comandos Principales:

**Gestión de Servicios:**
```bash
./docker-scripts.sh up       # Levantar servicios
./docker-scripts.sh down     # Bajar servicios
./docker-scripts.sh restart  # Reiniciar
./docker-scripts.sh status   # Ver estado
```

**Desarrollo:**
```bash
./docker-scripts.sh build    # Construir imágenes
./docker-scripts.sh logs     # Ver logs
./docker-scripts.sh test     # Ejecutar tests
```

**Mantenimiento:**
```bash
./docker-scripts.sh clean    # Limpiar contenedores
./docker-scripts.sh reset    # Reset completo (borra datos)
```

### Servicios Levantados:

| Servicio | Puerto | URL | Credenciales |
|----------|--------|-----|--------------|
| API | 8000 | http://localhost:8000 | - |
| Docs | 8000 | http://localhost:8000/docs | - |
| MongoDB | 27017 | localhost:27017 | admin/password123 |
| Mongo Admin | 8081 | http://localhost:8081 | admin/admin123 |

### Datos de Prueba:
La BD se inicializa automáticamente con 5 productos:
- Samsung Galaxy S23 ($999.99)
- iPhone 15 ($1,199.99)  
- MacBook Air M2 ($1,499.99)
- Google Pixel 8 ($899.99)
- Dell XPS 13 ($1,299.99)

---

## 🚀 Uso de la API

### Crear Producto:
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPad Pro",
    "brand": "Apple",
    "price": 1099.99,
    "category": "Tablets",
    "rating": 4.7
  }'
```

### Comparar Productos:
```bash
curl -X POST http://localhost:8000/api/products/compare \
  -H "Content-Type: application/json" \
  -d '{"product_ids": ["id1", "id2", "id3"]}'
```

### Ver Documentación:
- Abrir: http://localhost:8000/docs
- Interface interactiva con Swagger UI
- Probar endpoints directamente

---

## 📁 Estructura del Proyecto

```
api/
├── business_logic/         # Lógica de negocio
├── config/                # Configuración
├── models/                # Modelos de datos
├── repository/            # Acceso a datos
├── router/                # Endpoints REST
├── tests/                 # Pruebas
├── docker-compose.yml     # Orquestación Docker
├── Dockerfile            # Imagen de la API
├── docker-scripts.sh     # Scripts de gestión
└── requirements.txt      # Dependencias Python
```

## 🛠️ Tecnologías

- **Backend**: FastAPI 0.104+
- **Base de Datos**: MongoDB 7.0
- **Testing**: pytest + httpx
- **Containerización**: Docker + Docker Compose
- **Documentación**: OpenAPI automática

Este proyecto demuestra una API REST funcional con arquitectura limpia, tests completos y deployment containerizado - ideal para entrevistas técnicas de nivel senior.
