# Python Web API with MongoDB

Bu proje, MongoDB veritabanı kullanarak JWT tabanlı kimlik doğrulama ile Products ve Users için CRUD işlemleri sağlayan modern bir Python web API'sidir.

## 🚀 Özellikler

- **FastAPI Framework**: Modern, hızlı ve yüksek performanslı web framework
- **MongoDB Integration**: Motor (async MongoDB driver) ile NoSQL veritabanı desteği
- **JWT Authentication**: Güvenli token tabanlı kimlik doğrulama sistemi
- **CRUD Operations**: Users ve Products için tam CRUD işlemleri
- **Data Validation**: Pydantic ile güçlü veri doğrulama
- **Async/Await**: Asenkron programlama ile yüksek performans
- **Comprehensive Testing**: Kapsamlı test suite
- **API Documentation**: Otomatik Swagger/OpenAPI dokümantasyonu

## 📁 Proje Yapısı

```
python-web-api/
├── app/                        # Ana uygulama paketi
│   ├── __init__.py
│   ├── main.py                 # FastAPI uygulama giriş noktası
│   ├── config/                 # Konfigürasyon dosyaları
│   │   ├── __init__.py
│   │   ├── database.py         # MongoDB bağlantı konfigürasyonu
│   │   └── settings.py         # Uygulama ayarları
│   ├── models/                 # Veri modelleri
│   │   ├── __init__.py
│   │   ├── user.py            # User Pydantic modelleri
│   │   └── product.py         # Product Pydantic modelleri
│   ├── repositories/          # Veritabanı işlemleri
│   │   ├── __init__.py
│   │   ├── base.py            # Temel repository sınıfı
│   │   ├── user_repository.py  # User veritabanı işlemleri
│   │   └── product_repository.py # Product veritabanı işlemleri
│   ├── services/              # İş mantığı servisleri
│   │   ├── __init__.py
│   │   ├── auth_service.py     # Kimlik doğrulama iş mantığı
│   │   ├── user_service.py     # User iş mantığı
│   │   └── product_service.py  # Product iş mantığı
│   ├── routes/                # API endpoint'leri
│   │   ├── __init__.py
│   │   ├── auth.py            # Kimlik doğrulama endpoint'leri
│   │   ├── users.py           # User CRUD endpoint'leri
│   │   └── products.py        # Product CRUD endpoint'leri
│   ├── middleware/            # Middleware bileşenleri
│   │   ├── __init__.py
│   │   └── auth_middleware.py  # JWT kimlik doğrulama middleware
│   └── utils/                 # Yardımcı fonksiyonlar
│       ├── __init__.py
│       ├── security.py        # Şifre hash ve JWT utilities
│       └── dependencies.py    # FastAPI dependencies
├── tests/                     # Test dosyaları
│   ├── __init__.py
│   ├── test_auth.py          # Kimlik doğrulama testleri
│   ├── test_users.py         # User CRUD testleri
│   └── test_products.py      # Product CRUD testleri
├── requirements.txt          # Python bağımlılıkları
├── .env.example             # Örnek environment değişkenleri
├── .gitignore              # Git ignore dosyası
├── README.md               # Bu dosya
└── DATABASE_SETUP.md       # MongoDB kurulum rehberi
```

## 🛠️ Kurulum

### 1. Projeyi Klonlayın

```bash
git clone git@github.com:sefayilmaz2/python_with_mongodb.git
cd python-web-api
```

### 2. Virtual Environment Oluşturun

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows
```

### 3. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 4. Environment Değişkenlerini Ayarlayın

```bash
cp .env.example .env
```

`.env` dosyasını düzenleyin:

```env
# Database Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=python_web_api

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
DEBUG=True
API_V1_STR=/api/v1
PROJECT_NAME=Python Web API with MongoDB
```

### 5. MongoDB'yi Başlatın

MongoDB kurulumu ve konfigürasyonu için `DATABASE_SETUP.md` dosyasına bakın.

### 6. Uygulamayı Çalıştırın

```bash
# Development modunda
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Veya direkt Python ile
python -m app.main
```

## 📚 API Dokümantasyonu

Uygulama çalıştıktan sonra aşağıdaki URL'lerden API dokümantasyonuna erişebilirsiniz:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔐 Kimlik Doğrulama

API, JWT (JSON Web Token) tabanlı kimlik doğrulama kullanır. Tüm endpoint'ler (login hariç) kimlik doğrulama gerektirir.

### Login

```bash
# Form data ile login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your_username&password=your_password"

# JSON ile login
curl -X POST "http://localhost:8000/api/v1/auth/login-json" \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

### Token Kullanımı

```bash
curl -X GET "http://localhost:8000/api/v1/users/" \
  -H "Authorization: Bearer your_jwt_token_here"
```

## 📋 API Endpoint'leri

### Authentication
- `POST /api/v1/auth/login` - Form data ile login
- `POST /api/v1/auth/login-json` - JSON ile login

### Users
- `POST /api/v1/users/` - Yeni user oluştur
- `GET /api/v1/users/` - Tüm user'ları listele
- `GET /api/v1/users/{user_id}` - Belirli user'ı getir
- `PUT /api/v1/users/{user_id}` - User güncelle
- `DELETE /api/v1/users/{user_id}` - User sil
- `GET /api/v1/users/me/profile` - Mevcut user profilini getir

### Products
- `POST /api/v1/products/` - Yeni product oluştur
- `GET /api/v1/products/` - Tüm product'ları listele
- `GET /api/v1/products/{product_id}` - Belirli product'ı getir
- `PUT /api/v1/products/{product_id}` - Product güncelle
- `DELETE /api/v1/products/{product_id}` - Product sil
- `GET /api/v1/products/category/{category}` - Kategoriye göre product'ları getir
- `GET /api/v1/products/search/{search_term}` - Product ara

## 🧪 Testleri Çalıştırma

```bash
# Tüm testleri çalıştır
pytest

# Verbose output ile
pytest -v

# Belirli bir test dosyasını çalıştır
pytest tests/test_users.py

# Coverage ile
pytest --cov=app tests/
```

## 📊 Veri Modelleri

### User Model
```json
{
  "id": "string",
  "username": "string",
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2023-01-01T00:00:00"
}
```

### Product Model
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "price": 0.0,
  "category": "string",
  "stock_quantity": 0,
  "is_active": true,
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

## 🔧 Geliştirme

### Yeni Endpoint Ekleme

1. `models/` klasöründe gerekli Pydantic modellerini oluşturun
2. `repositories/` klasöründe veritabanı işlemlerini tanımlayın
3. `services/` klasöründe iş mantığını implement edin
4. `routes/` klasöründe endpoint'leri oluşturun
5. `main.py` dosyasında router'ı register edin

### Code Style

Proje PEP 8 standartlarını takip eder. Code formatting için:

```bash
# Black formatter
black app/ tests/

# Import sorting
isort app/ tests/

# Linting
flake8 app/ tests/
```

## 🚀 Production Deployment

### Docker ile Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables (Production)

```env
DEBUG=False
SECRET_KEY=very-secure-secret-key-for-production
MONGODB_URL=mongodb://production-mongodb-url:27017
DATABASE_NAME=production_db
```

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🆘 Destek

Herhangi bir sorun yaşarsanız:

1. GitHub Issues'da yeni bir issue oluşturun
2. Detaylı hata mesajları ve adımları ekleyin
3. Environment bilgilerinizi paylaşın

## 📈 Performans

- Async/await kullanımı ile yüksek concurrency
- MongoDB connection pooling
- Pydantic ile hızlı serialization
- JWT token caching
- Response compression desteği

## 🔒 Güvenlik

- Bcrypt ile güvenli password hashing
- JWT token expiration
- Input validation ve sanitization
- CORS konfigürasyonu
- Rate limiting (opsiyonel)

---

**Not**: Bu proje eğitim ve geliştirme amaçlıdır. Production kullanımı için ek güvenlik önlemleri alınmalıdır.