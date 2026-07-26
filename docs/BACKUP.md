# LN-NeU Backup & Restore Guide

## Overview

Dokumen ini menjelaskan prosedur backup dan restore untuk LN-NeU Production.

---

# PostgreSQL Backup

Jalankan:

```bash
./scripts/backup_postgres.sh
```

Hasil backup disimpan di:

```
backups/postgres/
```

Contoh:

```
backups/postgres/postgres_20260726_185820.sql
```

---

# PostgreSQL Restore

Pastikan environment telah dimuat:

```bash
export POSTGRES_USER=lnneu
export POSTGRES_PASSWORD=YOUR_PASSWORD
export POSTGRES_DB=lnneu
```

Restore:

```bash
./scripts/restore_postgres.sh backups/postgres/postgres_20260726_185820.sql
```

Jika berhasil akan muncul:

```
Restore completed.
```

---

# Redis Backup

Jalankan:

```bash
./scripts/backup_redis.sh
```

Output:

```
backups/redis/redis_YYYYMMDD_HHMMSS.rdb
```

---

# Docker Volume Backup

Jalankan:

```bash
./scripts/backup_volumes.sh
```

Output:

```
backups/volumes/postgres_volume_YYYYMMDD_HHMMSS.tar.gz
```

---

# Backup Directory Structure

```
backups/
├── postgres/
├── redis/
└── volumes/
```

---

# Recommended Backup Schedule

| Component | Frequency |
|-----------|-----------|
| PostgreSQL | Daily |
| Redis | Daily |
| Docker Volume | Weekly |

---

# Recovery Order

1. Restore PostgreSQL database
2. Restore Redis dump (jika diperlukan)
3. Restore Docker volume (jika diperlukan)
4. Jalankan kembali seluruh container

---

# Verification

Setelah restore:

```bash
docker compose -f docker-compose.production.yml ps
```

Periksa health endpoint:

```bash
curl http://localhost:8100/health
```

Periksa monitoring:

```bash
curl http://localhost:8100/monitoring/dashboard
```

Seluruh service harus berstatus healthy sebelum sistem digunakan kembali.

---

# Notes

- Simpan backup di lokasi terpisah dari server production.
- Lakukan uji restore secara berkala.
- Jangan menyimpan file backup yang berisi data sensitif di repository Git.
- Gunakan `.env.production` yang sesuai saat menjalankan proses backup maupun restore.
