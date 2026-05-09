from __future__ import annotations
from typing import Optional
from datetime import date
from database.database import get_connection
from models.transaksi import Transaksi
from controllers.alat_controller import AlatController


class TransaksiController:
    """Controller — C-08 / CD-14  — UC17"""

    def __init__(self):
        self._total_biaya: float = 0.0

    # ── UC17 helpers ─────────────────────────────────────────────────────────

    def hitung_biaya(self, id_alat: int, durasi: int) -> float:
        alat_ctrl = AlatController()
        alat = alat_ctrl.get_detail_alat(id_alat)
        if alat is None:
            return 0.0
        self._total_biaya = alat.get_harga_sewa() * durasi
        return self._total_biaya

    def cek_ketersediaan_alat(self, id_alat: int) -> bool:
        alat_ctrl = AlatController()
        alat = alat_ctrl.get_detail_alat(id_alat)
        return alat is not None and alat.get_status_ketersediaan() == "Tersedia"

    def validasi_saldo(self, id_pengguna: int, total_biaya: float) -> bool:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT saldo FROM dompet_digital WHERE id_pengguna=?", (id_pengguna,)
            ).fetchone()
        return row is not None and row["saldo"] >= total_biaya

    def proses_pembayaran(self, id_peminjam: int, id_penyedia: int, total_biaya: float) -> bool:
        with get_connection() as conn:
            conn.execute(
                "UPDATE dompet_digital SET saldo = saldo - ? WHERE id_pengguna = ?",
                (total_biaya, id_peminjam)
            )
            conn.execute(
                "UPDATE dompet_digital SET saldo = saldo + ? WHERE id_pengguna = ?",
                (total_biaya, id_penyedia)
            )
        return True

    def buat_transaksi(self, id_peminjam: int, id_alat: int, durasi: int) -> Optional[Transaksi]:
        alat_ctrl = AlatController()
        alat = alat_ctrl.get_detail_alat(id_alat)
        if alat is None:
            return None
        total = alat.get_harga_sewa() * durasi
        tgl = date.today().isoformat()
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO transaksi (id_peminjam, id_penyedia, id_alat, tanggal_transaksi, durasi, total_biaya, status)"
                " VALUES (?,?,?,?,?,?,'Berjalan')",
                (id_peminjam, alat.get_id_pemilik(), id_alat, tgl, durasi, total)
            )
            id_baru = cur.lastrowid
        return self.get_transaksi_by_id(id_baru)

    def ubah_status_alat(self, id_alat: int, status: str):
        alat_ctrl = AlatController()
        alat_ctrl.set_status(id_alat, status)

    def proses_peminjaman(self, id_pengguna: int, id_alat: int, durasi: int) -> bool:
        """Koordinasi penuh UC17 (Algo-006)."""
        if not self.cek_ketersediaan_alat(id_alat):
            return False
        total = self.hitung_biaya(id_alat, durasi)
        if not self.validasi_saldo(id_pengguna, total):
            return False
        alat_ctrl = AlatController()
        alat = alat_ctrl.get_detail_alat(id_alat)
        if alat is None:
            return False
        try:
            self.proses_pembayaran(id_pengguna, alat.get_id_pemilik(), total)
            self.buat_transaksi(id_pengguna, id_alat, durasi)
            self.ubah_status_alat(id_alat, "Sedang Dipinjam")
            return True
        except Exception:
            return False

    def get_transaksi_by_id(self, id_transaksi: int) -> Optional[Transaksi]:
        with get_connection() as conn:
            row = conn.execute(
                """SELECT t.*, a.nama_alat,
                          pm.nama_lengkap AS nama_peminjam,
                          py.nama_lengkap AS nama_penyedia
                   FROM transaksi t
                   JOIN alat     a  ON t.id_alat     = a.id_alat
                   JOIN pengguna pm ON t.id_peminjam = pm.id_pengguna
                   JOIN pengguna py ON t.id_penyedia = py.id_pengguna
                   WHERE t.id_transaksi = ?""",
                (id_transaksi,)
            ).fetchone()
        if row is None:
            return None
        return Transaksi(
            row["id_transaksi"], row["id_peminjam"], row["id_penyedia"],
            row["id_alat"], row["nama_alat"], row["nama_peminjam"], row["nama_penyedia"],
            row["tanggal_transaksi"], row["durasi"], row["total_biaya"], row["status"]
        )
