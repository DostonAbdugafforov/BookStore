# 📚 BookStore API

Django REST Framework asosida qurilgan kitob do'koni API si.

## 🛠 Texnologiyalar

- Python 3.12
- Django 6.0
- Django REST Framework
- PostgreSQL 16
- Redis 7
- Docker & Docker Compose
- JWT Authentication

## 🚀 Ishga tushirish

### 1. Reponi clone qiling

git clone https://github.com/username/bookstore.git
cd bookstore


### 2. `.env` fayl yarating

`.env.example` dan nusxa oling:

cp .env.example .env


`.env` faylni tahrirlang:

```env
SECRET_KEY="your-secret-key"
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

DB_NAME=bookstore
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=db
DB_PORT=5432

REDIS_URL=redis://redis:6379/1

ACCESS_TOKEN_LIFETIME_DAYS=5
REFRESH_TOKEN_LIFETIME_DAYS=10

BOOK_CACHE_TTL=300
```

### 3. Docker orqali ishga tushiring

docker-compose up --build -d


### 4. Superuser yarating

docker exec -it bookstore_app python manage.py createsuperuser


### 5. API ga kiring

- Swagger: http://127.0.0.1:8000/swagger/
- Admin: http://127.0.0.1:8000/admin/

## ⚙️ Containerni to'xtatish

docker-compose down
