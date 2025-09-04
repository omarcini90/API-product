# 🚀 Guía de Ejecución - API de Productos

Esta guía te llevará paso a paso para ejecutar la API de Productos en tu entorno local.

## 📋 Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

- **Docker** y **Docker Compose** (Recomendado - Opción más fácil)
- O alternativamente:
  - **Python 3.11+**
  - **MongoDB** (local o remoto)

## 🐳 Opción 1: Ejecución con Docker (Recomendado)

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/omarcini90/API-product.git
cd API-product/api
```

### Paso 2: Construir y levantar todos los servicios
```bash
# Construir las imágenes
docker-compose build

# Levantar todos los servicios
docker-compose up -d
```

Este comando iniciará:
- **API**: Puerto 8000
- **MongoDB**: Puerto 27017  
- **Mongo Express**: Puerto 8081 (Admin UI)

### Paso 3: Verificar que todo funciona
Abre tu navegador en:
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health
- **Mongo Admin**: http://localhost:8081

### Comandos adicionales útiles:
```bash
# Construir imágenes (si hay cambios en el código)
docker-compose build

# Ver logs en tiempo real
docker-compose logs -f

# Ejecutar tests (dentro del contenedor)
docker-compose exec api pytest tests/ -v

# Parar servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Reconstruir y levantar (útil después de cambios)
docker-compose up -d --build

# Limpiar todo (incluye datos)
docker-compose down -v
docker system prune -f
```

---

## 🐍 Opción 2: Ejecución con Python local

### Paso 1: Clonar y navegar al directorio
```bash
git clone https://github.com/omarcini90/API-product.git
cd API-product/api
```

### Paso 2: Crear entorno virtual
```bash
python -m venv venv

# En macOS/Linux:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Configurar MongoDB
Asegúrate de tener MongoDB ejecutándose en tu sistema:

```bash
# macOS (con Homebrew):
brew services start mongodb-community

# Ubuntu/Debian:
sudo systemctl start mongod

# Windows:
# Iniciar MongoDB desde Services o ejecutar mongod.exe
```

### Paso 5: Configurar variables de entorno (opcional)
Crea un archivo `.env` en el directorio `api/`:
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=products_db
LOG_LEVEL=INFO
```

### Paso 6: Ejecutar la aplicación
```bash
python main.py
```

O usando uvicorn directamente:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Paso 7: Verificar funcionamiento
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 🧪 Ejecutar Tests

### Con Docker:
```bash
# Ejecutar tests dentro del contenedor
docker-compose exec api pytest tests/ -v

# O crear un contenedor temporal para tests
docker-compose run --rm api pytest tests/ -v
```

### Con Python local:
```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio httpx

# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar con cobertura
pytest tests/ --cov=. --cov-report=html

# Ejecutar tests específicos
pytest tests/test_products_endpoints.py -v
```

---

## 📊 Verificación de la API

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Listar productos
```bash
curl http://localhost:8000/api/products/
```

### 3. Crear un producto
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Product",
    "brand": "Test Brand",
    "price": 99.99,
    "category": "Electronics",
    "rating": 4.5
  }'
```

### 4. Comparar productos (necesita IDs válidos)
```bash
curl -X POST http://localhost:8000/api/products/compare \
  -H "Content-Type: application/json" \
  -d '{
    "product_ids": ["id1", "id2", "id3"]
  }'
```

---

## 🌐 URLs Importantes

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Swagger UI** | http://localhost:8000/docs | Documentación interactiva |
| **Redoc** | http://localhost:8000/redoc | Documentación alternativa |
| **Health Check** | http://localhost:8000/health | Estado del sistema |
| **Root** | http://localhost:8000/ | Información básica |
| **Mongo Express** | http://localhost:8081 | Admin MongoDB (solo Docker) |

### Credenciales MongoDB (Docker):
- **Usuario**: admin
- **Contraseña**: password123

### Credenciales Mongo Express (Docker):
- **Usuario**: admin
- **Contraseña**: admin123

---

## 🔧 Solución de Problemas

### Error: Puerto 8000 ocupado
```bash
# Cambiar puerto en docker-compose.yml o main.py
# O liberar el puerto:
lsof -ti:8000 | xargs kill -9
```

### Error: MongoDB connection refused
```bash
# Verificar que MongoDB está ejecutándose
docker ps  # Si usas Docker
brew services list | grep mongodb  # macOS
systemctl status mongod  # Linux
```

### Error: Módulos no encontrados
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Ver logs de la aplicación
```bash
# Docker
docker-compose logs api

# Python local
tail -f app.log  # Si existe el archivo de log
```

---

## 🎯 Datos de Prueba

La aplicación se inicializa automáticamente con 5 productos de ejemplo:

1. **Samsung Galaxy S23** - $999.99 (Smartphones)
2. **iPhone 15** - $1,199.99 (Smartphones)  
3. **MacBook Air M2** - $1,499.99 (Laptops)
4. **Google Pixel 8** - $899.99 (Smartphones)
5. **Dell XPS 13** - $1,299.99 (Laptops)

Puedes usar estos productos para probar la funcionalidad de comparación.

---

## 💡 Consejos Adicionales

- **Desarrollo**: Usa la **Opción 1 (Docker)** para un setup más rápido
- **Producción**: Configura variables de entorno apropiadas
- **Testing**: Ejecuta tests regularmente durante el desarrollo
- **Debugging**: Usa `/docs` para probar endpoints interactivamente
- **Monitoreo**: Verifica `/health` para estado del sistema

¡Ya estás listo para usar la API de Productos! 🎉
