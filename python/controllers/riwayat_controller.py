from __future__ import annotations
from typing import List, Optional
from database.database import get_connection
from models.transaksi import Transaksi
from models.riwayat_transaksi import RiwayatTransaksi
from controllers.alat_controller import AlatController


def _row_to_transaksi(row) -> Transaksi:
    return Transaksi(
        row["id_transaksi"], row["id_peminjam"], row["id_penyedia"],
        row["id_alat"], row["nama_alat"], row["nama_peminjam"], row["nama_penyedia"],
        row["tanggal_transaksi"], row["durasi"], row["total_biaya"], row["status"]
    )


_JOIN_SQL = """
    SELECT t.*, a.nama_alat,
           pm.nama_lengkap AS nama_peminjam,
           py.nama_lengkap AS nama_penyedia
    FROM transaksi t
    JOIN alat     a  ON t.id_alat     = a.id_alat
    JOIN pengguna pm ON t.id_peminjam = pm.id_pengguna
    JOIN pengguna py ON t.id_penyedia = py.id_pengguna
"""


class RiwayatController:
    """Controller — C-09 / CD-15
    Handles UC18, UC19, UC20, UC21
    """

    def __init__(self):
        self._current_id_pengguna: int = 0
        self._status: str = ""

    # ── UC19: Melihat Riwayat ────────────────────────────────────────────────

    def load_riwayat(self, id_pengguna: int) -> RiwayatTransaksi:
        with get_connection() as conn:
            rows = conn.execute(
                _JOIN_SQL + " WHERE t.id_peminjam=? OR t.id_penyedia=?"
                            " ORDER BY t.tanggal_transaksi DESC",
                (id_pengguna, id_pengguna)
            ).fetchall()
        daftar = [_row_to_transaksi(r) for r in rows]
        return RiwayatTransaksi(id_pengguna, daftar)

    # ── UC20: Filter Riwayat ─────────────────────────────────────────────────

    def proses_filter(self, riwayat: RiwayatTransaksi, jenis: str) -> List[Transaksi]:
        return riwayat.filter_riwayat(jenis)

    # ── UC21: Detail Transaksi ───────────────────────────────────────────────

    def load_detail_transaksi(self, id_transaksi: int) -> Optional[Transaksi]:
        with get_connection() as conn:
            row = conn.execute(
                _JOIN_SQL + " WHERE t.id_transaksi = ?", (id_transaksi,)
            ).fetchone()
        return _row_to_transaksi(row) if row else None

    # ── UC18: Konfirmasi Pengembalian (oleh penyedia) ────────────────────────

    def konfirmasi_pengembalian(self, id_transaksi: int) -> bool:
        t = self.load_detail_transaksi(id_transaksi)
        if t is None or t.get_status() == "Selesai":
            return False
        with get_connection() as conn:
            conn.execute(
                "UPDATE transaksi SET status='Selesai' WHERE id_transaksi=?",
                (id_transaksi,)
            )
        alat_ctrl = AlatController()
        alat_ctrl.set_status(t.get_id_alat(), "Tersedia")
        self._status = "Selesai"
        return True
