// Script de inicialización para MongoDB
// Crea la base de datos y inserta productos de ejemplo

// Cambiar a la base de datos de productos
db = db.getSiblingDB('products_db');

// Crear colección de productos con datos de ejemplo
db.products.insertMany([
  {
    name: "Samsung Galaxy S23",
    brand: "Samsung",
    price: 999.99,
    image_url: "https://images.samsung.com/is/image/samsung/p6pim/ar/2302/gallery/ar-galaxy-s23-s911-sm-s911bzaaaro-534851967",
    description: "Smartphone premium con cámara de 50MP y pantalla AMOLED de 6.1 pulgadas",
    category: "Smartphones",
    rating: 4.5,
    specs: {
      screen_size: "6.1 inches",
      storage: "128GB",
      ram: "8GB",
      camera: "50MP",
      battery: "3900mAh",
      processor: "Snapdragon 8 Gen 2"
    }
  },
  {
    name: "iPhone 15",
    brand: "Apple",
    price: 1199.99,
    image_url: "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-finish-select-202309-6-1inch-blue",
    description: "iPhone con chip A17 Pro y cámara principal de 48MP",
    category: "Smartphones", 
    rating: 4.7,
    specs: {
      screen_size: "6.1 inches",
      storage: "128GB",
      ram: "8GB", 
      camera: "48MP",
      battery: "3349mAh",
      processor: "A17 Pro"
    }
  },
  {
    name: "MacBook Air M2",
    brand: "Apple",
    price: 1499.99,
    image_url: "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/macbook-air-midnight-select-20220606",
    description: "Laptop ultradelgada con chip M2 y pantalla Liquid Retina de 13.6 pulgadas",
    category: "Laptops",
    rating: 4.8,
    specs: {
      screen_size: "13.6 inches",
      storage: "256GB SSD",
      ram: "8GB",
      processor: "Apple M2",
      battery: "18 hours",
      weight: "1.24 kg"
    }
  },
  {
    name: "Google Pixel 8",
    brand: "Google",
    price: 899.99,
    image_url: "https://lh3.googleusercontent.com/RMkx7Ap8nZhGHqDv8C_a5c8oEjnM_Zqp5GVRU1v7o2g",
    description: "Smartphone con IA avanzada y cámara computacional",
    category: "Smartphones",
    rating: 4.4,
    specs: {
      screen_size: "6.2 inches",
      storage: "128GB",
      ram: "8GB",
      camera: "50MP",
      battery: "4575mAh",
      processor: "Tensor G3"
    }
  },
  {
    name: "Dell XPS 13",
    brand: "Dell",
    price: 1299.99,
    image_url: "https://i.dell.com/is/image/DellContent/content/dam/ss2/product-images/dell-client-products/notebooks/xps-notebooks/xps-13-9315",
    description: "Laptop ultraportátil con pantalla InfinityEdge y procesador Intel",
    category: "Laptops",
    rating: 4.3,
    specs: {
      screen_size: "13.4 inches",
      storage: "512GB SSD",
      ram: "16GB",
      processor: "Intel i7-1250U",
      battery: "12 hours",
      weight: "1.17 kg"
    }
  }
]);

// Crear índices para mejorar performance
db.products.createIndex({ "name": 1 });
db.products.createIndex({ "brand": 1 });
db.products.createIndex({ "category": 1 });
db.products.createIndex({ "price": 1 });

print("✅ Base de datos inicializada con productos de ejemplo");
print("📊 Productos insertados:", db.products.countDocuments());
print("🏷️ Categorías disponibles:", db.products.distinct("category"));
print("🏢 Marcas disponibles:", db.products.distinct("brand"));
