import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pinjeminaja.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize():
    """Create all tables if they don't exist yet."""
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS pengguna (
                id_pengguna   INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_lengkap  TEXT    NOT NULL,
                no_wa         TEXT    NOT NULL UNIQUE,
                alamat        TEXT    NOT NULL,
                kata_sandi    TEXT    NOT NULL
            );

            CREATE TABLE IF NOT EXISTS dompet_digital (
                id_dompet   INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pengguna INTEGER NOT NULL UNIQUE REFERENCES pengguna(id_pengguna),
                saldo       REAL    NOT NULL DEFAULT 0.0
            );

            CREATE TABLE IF NOT EXISTS alat (
                id_alat             INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pengguna         INTEGER NOT NULL REFERENCES pengguna(id_pengguna),
                nama_alat           TEXT    NOT NULL,
                deskripsi           TEXT,
                kategori            TEXT    NOT NULL,
                harga_sewa          REAL    NOT NULL,
                kondisi_alat        TEXT    NOT NULL,
                status_ketersediaan TEXT    NOT NULL DEFAULT 'Tersedia'
            );

            CREATE TABLE IF NOT EXISTS transaksi (
                id_transaksi       INTEGER PRIMARY KEY AUTOINCREMENT,
                id_peminjam        INTEGER NOT NULL REFERENCES pengguna(id_pengguna),
                id_penyedia        INTEGER NOT NULL REFERENCES pengguna(id_pengguna),
                id_alat            INTEGER NOT NULL REFERENCES alat(id_alat),
                tanggal_transaksi  TEXT    NOT NULL,
                durasi             INTEGER NOT NULL,
                total_biaya        REAL    NOT NULL,
                status             TEXT    NOT NULL DEFAULT 'Berjalan'
            );
        """)
