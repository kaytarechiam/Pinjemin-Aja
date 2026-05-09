from __future__ import annotations
from typing import List, Optional
from database.database import get_connection
from models.alat import Alat


def _row_to_alat(row) -> Alat:
    return Alat(
        row["id_alat"], row["id_pengguna"], row["nama_pemilik"],
        row["nama_alat"], row["deskripsi"], row["kategori"],
        row["harga_sewa"], row["kondisi_alat"], row["status_ketersediaan"]
    )


_BASE_SQL = """
    SELECT a.*, p.nama_lengkap AS nama_pemilik
    FROM alat a JOIN pengguna p ON a.id_pengguna = p.id_pengguna
"""


class AlatController:
    """Controller — C-06 / CD-10
    Handles UC09, UC10, UC11, UC12, UC13, UC14, UC15, UC16
    """

    def __init__(self):
        self._current_id_pengguna: int = 0

    # ── UC09: Melihat Katalog ────────────────────────────────────────────────

    def get_semua_alat(self) -> List[Alat]:
        with get_connection() as conn:
            rows = conn.execute(
                _BASE_SQL + " WHERE a.status_ketersediaan != 'Dihapus' ORDER BY a.nama_alat ASC"
            ).fetchall()
        return [_row_to_alat(r) for r in rows]

    # ── UC14: Mencari Alat ───────────────────────────────────────────────────

    def cari_alat(self, keyword: str) -> List[Alat]:
        if not keyword or not keyword.strip():
            return self.get_semua_alat()
        kw = f"%{keyword.lower()}%"
        with get_connection() as conn:
            rows = conn.execute(
                _BASE_SQL + " WHERE a.status_ketersediaan != 'Dihapus'"
                            " AND (LOWER(a.nama_alat) LIKE ? OR LOWER(a.deskripsi) LIKE ?)"
                            " ORDER BY a.nama_alat ASC",
                (kw, kw)
            ).fetchall()
        return [_row_to_alat(r) for r in rows]

    # ── UC15: Filter Alat ────────────────────────────────────────────────────

    def filter_alat(self, kategori: str) -> List[Alat]:
        if not kategori or kategori == "Semua":
            return self.get_semua_alat()
        with get_connection() as conn:
            rows = conn.execute(
                _BASE_SQL + " WHERE a.status_ketersediaan != 'Dihapus' AND a.kategori = ?"
                            " ORDER BY a.nama_alat ASC",
                (kategori,)
            ).fetchall()
        return [_row_to_alat(r) for r in rows]

    def cari_dan_filter(self, keyword: str, kategori: str) -> List[Alat]:
        if not keyword and (not kategori or kategori == "Semua"):
            return self.get_semua_alat()
        if not keyword:
            return self.filter_alat(kategori)
        if not kategori or kategori == "Semua":
            return self.cari_alat(keyword)
        kw = f"%{keyword.lower()}%"
        with get_connection() as conn:
            rows = conn.execute(
                _BASE_SQL + " WHERE a.status_ketersediaan != 'Dihapus' AND a.kategori = ?"
                            " AND (LOWER(a.nama_alat) LIKE ? OR LOWER(a.deskripsi) LIKE ?)"
                            " ORDER BY a.nama_alat ASC",
                (kategori, kw, kw)
            ).fetchall()
        return [_row_to_alat(r) for r in rows]

    # ── UC16: Detail Alat ────────────────────────────────────────────────────

    def get_detail_alat(self, id_alat: int) -> Optional[Alat]:
        with get_connection() as conn:
            row = conn.execute(
                _BASE_SQL + " WHERE a.id_alat = ?", (id_alat,)
            ).fetchone()
        return _row_to_alat(row) if row else None

    # ── UC10: Katalog Saya ───────────────────────────────────────────────────

    def get_alat_from_pengguna(self, id_pengguna: int) -> List[Alat]:
        with get_connection() as conn:
            rows = conn.execute(
                _BASE_SQL + " WHERE a.id_pengguna = ? AND a.status_ketersediaan != 'Dihapus'"
                            " ORDER BY a.nama_alat ASC",
                (id_pengguna,)
            ).fetchall()
        return [_row_to_alat(r) for r in rows]

    # ── UC11: Tambah Alat ────────────────────────────────────────────────────

    def tambah_alat(self, data: dict) -> bool:
        data["status_ketersediaan"] = "Tersedia"
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO alat (id_pengguna, nama_alat, deskripsi, kategori, harga_sewa, kondisi_alat, status_ketersediaan)"
                " VALUES (:id_pengguna, :nama_alat, :deskripsi, :kategori, :harga_sewa, :kondisi_alat, :status_ketersediaan)",
                data
            )
        return True

    # ── UC13: Edit Alat ──────────────────────────────────────────────────────

    def update_alat(self, id_alat: int, data: dict) -> bool:
        with get_connection() as conn:
            conn.execute(
                "UPDATE alat SET nama_alat=:nama_alat, deskripsi=:deskripsi, kategori=:kategori,"
                " harga_sewa=:harga_sewa, kondisi_alat=:kondisi_alat WHERE id_alat=:id_alat",
                {**data, "id_alat": id_alat}
            )
        return True

    # ── UC12: Hapus Alat ─────────────────────────────────────────────────────

    def hapus_alat(self, id_alat: int) -> bool:
        alat = self.get_detail_alat(id_alat)
        if alat and alat.get_status_ketersediaan() == "Sedang Dipinjam":
            return False  # tidak bisa dihapus saat dipinjam
        with get_connection() as conn:
            conn.execute(
                "UPDATE alat SET status_ketersediaan='Dihapus' WHERE id_alat=?", (id_alat,)
            )
        return True

    # ── Status ───────────────────────────────────────────────────────────────

    def set_status(self, id_alat: int, status: str) -> bool:
        with get_connection() as conn:
            conn.execute(
                "UPDATE alat SET status_ketersediaan=? WHERE id_alat=?", (status, id_alat)
            )
        return True
