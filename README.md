
### News Crawler

News Crawler adalah aplikasi FastAPI yang dirancang untuk mengambil berita dari berbagai sumber online dan menyimpannya dalam database MySQL/PostgreSQL. Aplikasi ini menggunakan Alembic untuk manajemen migrasi database dan PyMySQL/Psycopg2 sebagai database driver.

### Features

- Automatic News Crawling   : Mengambil berita secara otomatis dari situs yang telah ditentukan.
- API Endpoints             : Menyediakan API untuk mengakses berita yang telah di-crawl dan disimpan.
- Database Integration      : Menggunakan MySQL/PostgreSQL untuk menyimpan hasil crawl.
- Data Migration            : Menggunakan Alembic untuk migrasi database.

### Installation

Sebelum menjalankan aplikasi, pastikan Docker & database container mysql/postgresql sudah terinstal pada sistem Anda. 

### Step 1: Start the Application

Untuk memulai aplikasi, buka terminal dan jalankan perintah berikut:

```bash
docker-compose up -d
```

Perintah ini akan membangun dan menjalankan semua container yang diperlukan secara background.

### Step 2: Run Database Migrations

Jika menggunakan database PostgreSQL, sesuaikan value `DB_DIALECT` di file `.env` ke `postgresql`. Secara default, aplikasi ini dikonfigurasi menggunakan database MySQL.

Setelah container berjalan, eksekusi migrasi database untuk mempersiapkan skema database yang diperlukan:

```bash
alembic upgrade head
```

### Step 3: Crawling Data

Untuk memulai proses crawling dan menyimpan data ke dalam database, jalankan:

```bash
python app/scripts/crawler_script.py
```

## Cleanup Data Berita
```bash
python app/scripts/news_cleanup_script.py
```

Berita akan dibersihkan, dan dipertahankan sampai 7 hari ke belakang dari hari ini.

## API Usage

Setelah data berhasil di-crawl dan disimpan, Anda dapat mengakses API endpoints untuk mengambil atau mencari berita. Beberapa endpoints yang tersedia termasuk:

- `GET /news`: Mengembalikan semua berita yang tersimpan.

## Contributing

Kontribusi selalu terbuka! Jika Anda ingin berkontribusi pada proyek ini, silakan fork repositori ini, buat perubahan Anda, dan kirimkan pull request.
