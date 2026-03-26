import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'training_project.settings')
django.setup()

from webshop.models import Manufacturer, Product


manufacturers = [
    {"name": "Apple", "country": "USA", "founded_year": 1976},
    {"name": "Samsung", "country": "South Korea", "founded_year": 1938},
    {"name": "Sony", "country": "Japan", "founded_year": 1946},
    {"name": "LG", "country": "South Korea", "founded_year": 1958},
    {"name": "Huawei", "country": "China", "founded_year": 1987},
    {"name": "Dell", "country": "USA", "founded_year": 1984},
    {"name": "HP", "country": "USA", "founded_year": 1939},
    {"name": "Lenovo", "country": "China", "founded_year": 1984},
    {"name": "Asus", "country": "Taiwan", "founded_year": 1989},
    {"name": "Acer", "country": "Taiwan", "founded_year": 1976},
    {"name": "Xiaomi", "country": "China", "founded_year": 2010},
    {"name": "Microsoft", "country": "USA", "founded_year": 1975},
    {"name": "Google", "country": "USA", "founded_year": 1998},
    {"name": "Panasonic", "country": "Japan", "founded_year": 1918},
    {"name": "Philips", "country": "Netherlands", "founded_year": 1891},
    {"name": "Toshiba", "country": "Japan", "founded_year": 1939},
    {"name": "Nokia", "country": "Finland", "founded_year": 1865},
    {"name": "Motorola", "country": "USA", "founded_year": 1928},
    {"name": "OnePlus", "country": "China", "founded_year": 2013},
    {"name": "Realme", "country": "China", "founded_year": 2018},
]

for m in manufacturers:
    Manufacturer.objects.get_or_create(**m)


products = [
    {"name": "iPhone 14 Pro", "manufacturer": "Apple", "sku": "APL-IP14P", "description": "Флагманский смартфон Apple", "price": 1299.99, "stock_quantity": 25},
    {"name": "MacBook Air M2", "manufacturer": "Apple", "sku": "APL-MBAIR-M2", "description": "Ультрабук с процессором M2", "price": 1499.99, "stock_quantity": 15},
    {"name": "Galaxy S23 Ultra", "manufacturer": "Samsung", "sku": "SMSNG-S23U", "description": "Флагман Samsung с 200MP камерой", "price": 1399.99, "stock_quantity": 30},
    {"name": "Galaxy Tab S9", "manufacturer": "Samsung", "sku": "SMSNG-TABS9", "description": "Планшет для работы и развлечений", "price": 799.99, "stock_quantity": 10},
    {"name": "PlayStation 5", "manufacturer": "Sony", "sku": "SONY-PS5", "description": "Игровая консоль нового поколения", "price": 499.99, "stock_quantity": 50},
    {"name": "Sony WH-1000XM5", "manufacturer": "Sony", "sku": "SONY-WHXM5", "description": "Наушники с шумоподавлением", "price": 349.99, "stock_quantity": 40},
    {"name": "LG OLED55", "manufacturer": "LG", "sku": "LG-OLED55", "description": "55-дюймовый OLED телевизор", "price": 1199.99, "stock_quantity": 5},
    {"name": "Huawei MateBook X", "manufacturer": "Huawei", "sku": "HUA-MBX", "description": "Стильный ноутбук от Huawei", "price": 999.99, "stock_quantity": 8},
    {"name": "Dell XPS 13", "manufacturer": "Dell", "sku": "DELL-XPS13", "description": "Премиум ультрабук", "price": 1399.99, "stock_quantity": 12},
    {"name": "HP Spectre x360", "manufacturer": "HP", "sku": "HP-SPX360", "description": "Трансформируемый ноутбук", "price": 1249.99, "stock_quantity": 10},
    {"name": "Lenovo Legion 5", "manufacturer": "Lenovo", "sku": "LNV-LEG5", "description": "Игровой ноутбук Lenovo", "price": 1099.99, "stock_quantity": 18},
    {"name": "Asus ROG Strix", "manufacturer": "Asus", "sku": "ASUS-ROGSTRIX", "description": "Игровой ноутбук ROG", "price": 1499.99, "stock_quantity": 14},
    {"name": "Acer Swift 3", "manufacturer": "Acer", "sku": "ACER-SWIFT3", "description": "Лёгкий ноутбук для учёбы", "price": 699.99, "stock_quantity": 22},
    {"name": "Xiaomi Mi 13", "manufacturer": "Xiaomi", "sku": "XMI-MI13", "description": "Флагман Xiaomi", "price": 899.99, "stock_quantity": 35},
    {"name": "Surface Pro 9", "manufacturer": "Microsoft", "sku": "MS-SURFPRO9", "description": "Гибрид планшета и ноутбука", "price": 1199.99, "stock_quantity": 9},
    {"name": "Google Pixel 7", "manufacturer": "Google", "sku": "GOOG-PXL7", "description": "Флагман Google с чистым Android", "price": 799.99, "stock_quantity": 20},
    {"name": "Panasonic Lumix GH6", "manufacturer": "Panasonic", "sku": "PAN-GH6", "description": "Профессиональная камера", "price": 1499.99, "stock_quantity": 6},
    {"name": "Philips Hue Starter Kit", "manufacturer": "Philips", "sku": "PH-HUEKIT", "description": "Умное освещение", "price": 199.99, "stock_quantity": 50},
    {"name": "Toshiba External HDD 2TB", "manufacturer": "Toshiba", "sku": "TOSH-2TBHDD", "description": "Надёжный внешний диск", "price": 89.99, "stock_quantity": 60},
    {"name": "Nokia G22", "manufacturer": "Nokia", "sku": "NOK-G22", "description": "Смартфон с возможностью самостоятельного ремонта", "price": 249.99, "stock_quantity": 40},
    {"name": "Moto G Power", "manufacturer": "Motorola", "sku": "MOTO-GPWR", "description": "Телефон с мощной батареей", "price": 199.99, "stock_quantity": 25},
    {"name": "OnePlus 11", "manufacturer": "OnePlus", "sku": "OP-11", "description": "Флагман с Oxygen OS", "price": 799.99, "stock_quantity": 15},
    {"name": "Realme GT Neo 5", "manufacturer": "Realme", "sku": "REAL-NEO5", "description": "Быстрый смартфон с зарядкой 240 Вт", "price": 499.99, "stock_quantity": 30},
    {"name": "Mac Studio", "manufacturer": "Apple", "sku": "APL-MACSTUDIO", "description": "Профессиональный мини-ПК", "price": 1999.99, "stock_quantity": 4},
    {"name": "AirPods Pro 2", "manufacturer": "Apple", "sku": "APL-APPRO2", "description": "Беспроводные наушники с шумоподавлением", "price": 249.99, "stock_quantity": 60},
    {"name": "Samsung Galaxy Watch 6", "manufacturer": "Samsung", "sku": "SMSNG-GW6", "description": "Умные часы от Samsung", "price": 349.99, "stock_quantity": 45},
    {"name": "Sony Xperia 1 V", "manufacturer": "Sony", "sku": "SONY-XP1V", "description": "Смартфон с 4K экраном", "price": 1199.99, "stock_quantity": 10},
    {"name": "LG Gram 17", "manufacturer": "LG", "sku": "LG-GRAM17", "description": "Лёгкий ноутбук 17\"", "price": 1399.99, "stock_quantity": 7},
    {"name": "Huawei P60 Pro", "manufacturer": "Huawei", "sku": "HUA-P60PRO", "description": "Камерафон с уникальной оптикой", "price": 1099.99, "stock_quantity": 16},
    {"name": "Dell Inspiron 15", "manufacturer": "Dell", "sku": "DELL-INSP15", "description": "Бюджетный ноутбук", "price": 549.99, "stock_quantity": 20},
    {"name": "HP Pavilion x360", "manufacturer": "HP", "sku": "HP-PAVX360", "description": "Универсальный ноутбук", "price": 679.99, "stock_quantity": 19},
    {"name": "Lenovo ThinkPad X1", "manufacturer": "Lenovo", "sku": "LNV-TPX1", "description": "Бизнес-ноутбук с защитой", "price": 1499.99, "stock_quantity": 11},
    {"name": "Asus VivoBook", "manufacturer": "Asus", "sku": "ASUS-VIVO", "description": "Лёгкий и стильный", "price": 599.99, "stock_quantity": 18},
    {"name": "Acer Predator Helios", "manufacturer": "Acer", "sku": "ACER-PRHEL", "description": "Игровой зверь от Acer", "price": 1699.99, "stock_quantity": 13},
    {"name": "Xiaomi Pad 6", "manufacturer": "Xiaomi", "sku": "XMI-PAD6", "description": "Планшет с высоким FPS", "price": 449.99, "stock_quantity": 28},
    {"name": "Surface Laptop 5", "manufacturer": "Microsoft", "sku": "MS-SLAP5", "description": "Тонкий и мощный ноутбук", "price": 1299.99, "stock_quantity": 9},
    {"name": "Google Nest Hub", "manufacturer": "Google", "sku": "GOOG-NEST", "description": "Умный экран для дома", "price": 99.99, "stock_quantity": 50},
    {"name": "Philips Airfryer XXL", "manufacturer": "Philips", "sku": "PH-AIRXXL", "description": "Фритюрница без масла", "price": 179.99, "stock_quantity": 35},
    {"name": "Toshiba Smart TV 43\"", "manufacturer": "Toshiba", "sku": "TOSH-TV43", "description": "Умный телевизор для дома", "price": 349.99, "stock_quantity": 14},
]

for p in products:
    manufacturer = Manufacturer.objects.get(name=p.pop('manufacturer'))
    Product.objects.get_or_create(manufacturer=manufacturer, **p)

print('Done!')
