# MongoDB Kurulum ve Konfigürasyon Rehberi

Bu dokümanda Python Web API projesi için MongoDB veritabanının kurulumu ve konfigürasyonu anlatılmaktadır.

## 📋 İçindekiler

1. [MongoDB Kurulumu](#mongodb-kurulumu)
2. [Veritabanı Konfigürasyonu](#veritabanı-konfigürasyonu)
3. [Bağlantı Ayarları](#bağlantı-ayarları)
4. [İndeksler ve Optimizasyon](#indeksler-ve-optimizasyon)
5. [Backup ve Restore](#backup-ve-restore)
6. [Troubleshooting](#troubleshooting)

## 🛠️ MongoDB Kurulumu

### Windows

1. **MongoDB Community Server İndirin**
   - [MongoDB Download Center](https://www.mongodb.com/try/download/community) adresine gidin
   - Windows için MongoDB Community Server'ı indirin
   - MSI installer'ı çalıştırın

2. **Kurulum Adımları**
   ```cmd
   # MongoDB servisini başlatın
   net start MongoDB
   
   # MongoDB shell'e bağlanın
   mongo
   ```

3. **MongoDB Compass (GUI) Kurulumu**
   - MongoDB Compass'ı [buradan](https://www.mongodb.com/products/compass) indirin
   - Kurulum dosyasını çalıştırın

### macOS

1. **Homebrew ile Kurulum**
   ```bash
   # Homebrew ile MongoDB'yi kurun
   brew tap mongodb/brew
   brew install mongodb-community
   
   # MongoDB servisini başlatın
   brew services start mongodb/brew/mongodb-community
   ```

2. **Manuel Kurulum**
   - [MongoDB Download Center](https://www.mongodb.com/try/download/community) adresine gidin
   - macOS için .tgz dosyasını indirin
   - Kurulum talimatlarını takip edin

### Linux (Ubuntu/Debian)

1. **Resmi Repository Ekleme**
   ```bash
   # GPG key'i import edin
   wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
   
   # Repository ekleyin
   echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
   
   # Package listesini güncelleyin
   sudo apt-get update
   
   # MongoDB'yi kurun
   sudo apt-get install -y mongodb-org
   ```

2. **Servisi Başlatma**
   ```bash
   # MongoDB servisini başlatın
   sudo systemctl start mongod
   
   # Sistem başlangıcında otomatik başlatma
   sudo systemctl enable mongod
   
   # Servis durumunu kontrol edin
   sudo systemctl status mongod
   ```

### Docker ile Kurulum

```bash
# MongoDB container'ını çalıştırın
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  -v mongodb_data:/data/db \
  mongo:latest

# Container'ın çalıştığını kontrol edin
docker ps
```

## ⚙️ Veritabanı Konfigürasyonu

### 1. Veritabanı ve Koleksiyonlar Oluşturma

```javascript
// MongoDB shell'e bağlanın
mongo

// Veritabanını seçin (otomatik oluşturulur)
use python_web_api

// Users koleksiyonu için örnek döküman ekleyin
db.users.insertOne({
  "username": "admin",
  "email": "admin@example.com",
  "hashed_password": "$2b$12$example_hashed_password",
  "is_active": true,
  "created_at": new Date()
})

// Products koleksiyonu için örnek döküman ekleyin
db.products.insertOne({
  "name": "Sample Product",
  "description": "This is a sample product",
  "price": 29.99,
  "category": "Electronics",
  "stock_quantity": 100,
  "is_active": true,
  "created_at": new Date()
})
```

### 2. Kullanıcı ve Yetkilendirme Ayarları

```javascript
// Admin kullanıcısı oluşturun
use admin
db.createUser({
  user: "api_admin",
  pwd: "secure_password_here",
  roles: [
    { role: "readWrite", db: "python_web_api" },
    { role: "dbAdmin", db: "python_web_api" }
  ]
})

// Uygulama için özel kullanıcı oluşturun
use python_web_api
db.createUser({
  user: "api_user",
  pwd: "api_password_here",
  roles: [
    { role: "readWrite", db: "python_web_api" }
  ]
})
```

## 🔗 Bağlantı Ayarları

### Environment Variables

`.env` dosyanızda aşağıdaki ayarları yapın:

```env
# Yerel MongoDB (authentication olmadan)
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=python_web_api

# Authentication ile
MONGODB_URL=mongodb://api_user:api_password_here@localhost:27017/python_web_api

# MongoDB Atlas (Cloud)
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/python_web_api?retryWrites=true&w=majority

# Replica Set ile
MONGODB_URL=mongodb://user:password@host1:27017,host2:27017,host3:27017/python_web_api?replicaSet=myReplicaSet
```

### Connection String Parametreleri

```env
# Gelişmiş bağlantı ayarları
MONGODB_URL=mongodb://localhost:27017/python_web_api?maxPoolSize=20&minPoolSize=5&maxIdleTimeMS=30000&serverSelectionTimeoutMS=5000&socketTimeoutMS=30000
```

## 📊 İndeksler ve Optimizasyon

### Gerekli İndeksler

```javascript
// Users koleksiyonu için indeksler
use python_web_api

// Username için unique index
db.users.createIndex({ "username": 1 }, { unique: true })

// Email için unique index
db.users.createIndex({ "email": 1 }, { unique: true })

// Active users için compound index
db.users.createIndex({ "is_active": 1, "created_at": -1 })

// Products koleksiyonu için indeksler
// Product name için unique index
db.products.createIndex({ "name": 1 }, { unique: true })

// Category için index
db.products.createIndex({ "category": 1 })

// Price range queries için index
db.products.createIndex({ "price": 1 })

// Active products için compound index
db.products.createIndex({ "is_active": 1, "category": 1 })

// Text search için index
db.products.createIndex({ 
  "name": "text", 
  "description": "text" 
}, {
  weights: { "name": 10, "description": 5 }
})

// Stock quantity için index
db.products.createIndex({ "stock_quantity": 1 })
```

### Performans Optimizasyonu

```javascript
// İndeks kullanımını kontrol edin
db.users.find({ "username": "testuser" }).explain("executionStats")

// Koleksiyon istatistiklerini görüntüleyin
db.users.stats()
db.products.stats()

// Yavaş sorguları loglamak için profiling açın
db.setProfilingLevel(2, { slowms: 100 })

// Profiling sonuçlarını görüntüleyin
db.system.profile.find().limit(5).sort({ ts: -1 }).pretty()
```

## 💾 Backup ve Restore

### Backup Alma

```bash
# Tüm veritabanını backup alın
mongodump --db python_web_api --out /backup/mongodb/

# Belirli koleksiyonu backup alın
mongodump --db python_web_api --collection users --out /backup/mongodb/

# Compressed backup
mongodump --db python_web_api --gzip --out /backup/mongodb/

# Authentication ile backup
mongodump --host localhost:27017 --username api_user --password api_password_here --db python_web_api --out /backup/mongodb/
```

### Restore İşlemi

```bash
# Veritabanını restore edin
mongorestore --db python_web_api /backup/mongodb/python_web_api/

# Compressed backup'tan restore
mongorestore --gzip --db python_web_api /backup/mongodb/python_web_api/

# Authentication ile restore
mongorestore --host localhost:27017 --username api_user --password api_password_here --db python_web_api /backup/mongodb/python_web_api/
```

### Otomatik Backup Script

```bash
#!/bin/bash
# backup_mongodb.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/mongodb/$DATE"
DB_NAME="python_web_api"

# Backup dizinini oluştur
mkdir -p $BACKUP_DIR

# Backup al
mongodump --db $DB_NAME --gzip --out $BACKUP_DIR

# 7 günden eski backup'ları sil
find /backup/mongodb/ -type d -mtime +7 -exec rm -rf {} \;

echo "Backup completed: $BACKUP_DIR"
```

## 🔧 Troubleshooting

### Yaygın Sorunlar ve Çözümleri

#### 1. Bağlantı Sorunları

```bash
# MongoDB servisinin çalışıp çalışmadığını kontrol edin
# Windows
net start MongoDB

# Linux/macOS
sudo systemctl status mongod
brew services list | grep mongodb

# Port'un açık olup olmadığını kontrol edin
netstat -an | grep 27017
```

#### 2. Authentication Sorunları

```javascript
// Kullanıcı listesini kontrol edin
use admin
db.system.users.find()

// Kullanıcı yetkilerini kontrol edin
use python_web_api
db.runCommand({usersInfo: "api_user"})
```

#### 3. Performans Sorunları

```javascript
// Yavaş sorguları bulun
db.system.profile.find({millis: {$gt: 100}}).sort({ts: -1})

// İndeks kullanımını kontrol edin
db.users.find({username: "test"}).explain("executionStats")

// Koleksiyon boyutlarını kontrol edin
db.stats()
```

#### 4. Disk Alanı Sorunları

```bash
# MongoDB log dosyalarını kontrol edin
tail -f /var/log/mongodb/mongod.log

# Disk kullanımını kontrol edin
df -h
du -sh /var/lib/mongodb/

# Log rotation ayarlayın
logrotate /etc/logrotate.d/mongodb
```

### Log Dosyaları

```bash
# MongoDB log dosyası konumları
# Linux
/var/log/mongodb/mongod.log

# macOS (Homebrew)
/usr/local/var/log/mongodb/mongo.log

# Windows
C:\Program Files\MongoDB\Server\6.0\log\mongod.log
```

### Monitoring

```javascript
// Gerçek zamanlı operasyonları görüntüleyin
db.currentOp()

// Veritabanı istatistikleri
db.serverStatus()

// Bağlantı sayısını kontrol edin
db.serverStatus().connections
```

## 🚀 Production Ayarları

### Replica Set Kurulumu

```javascript
// Replica set başlatın
rs.initiate({
  _id: "myReplicaSet",
  members: [
    { _id: 0, host: "mongodb1:27017" },
    { _id: 1, host: "mongodb2:27017" },
    { _id: 2, host: "mongodb3:27017" }
  ]
})

// Replica set durumunu kontrol edin
rs.status()
```

### Security Ayarları

```yaml
# mongod.conf
security:
  authorization: enabled
  keyFile: /etc/mongodb/keyfile

net:
  bindIp: 127.0.0.1,10.0.0.1
  port: 27017

storage:
  dbPath: /var/lib/mongodb
  journal:
    enabled: true

systemLog:
  destination: file
  path: /var/log/mongodb/mongod.log
  logAppend: true
```

---

**Not**: Production ortamında mutlaka güvenlik ayarlarını yapın, regular backup alın ve monitoring sistemleri kurun.