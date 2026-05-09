from __future__ import annotations
from typing import Optional
from database.database import get_connection
from models.pengguna import Pengguna
from models.dompet_digital import DompetDigital


class PenggunaController:
    """Controller — C-03 / CD-03
    Handles UC01, UC02, UC03, UC04, UC05, UC06, UC07, UC08
    """

    def __init__(self):
        self._pengguna:      Optional[Pengguna]      = None
        self._dompet:        Optional[DompetDigital] = None
        self._is_registered: bool = False
        self._is_logged_in:  bool = False
        self._is_edit_success: bool = False

    # ── Registrasi (UC01) ────────────────────────────────────────────────────

    def validasi_input(self, data: dict) -> bool:
        required = ["nama_lengkap", "no_wa", "alamat", "kata_sandi", "konfirmasi_sandi"]
        for k in required:
            if not data.get(k, "").strip():
                return False
        if data["kata_sandi"] != data["konfirmasi_sandi"]:
            return False
        return True

    def proses_registrasi(self, data: dict) -> bool:
        if not self.validasi_input(data):
            return False
        with get_connection() as conn:
            existing = conn.execute(
                "SELECT COUNT(*) FROM pengguna WHERE no_wa = ?", (data["no_wa"],)
            ).fetchone()[0]
            if existing:
                return False  # nomor WA sudah terdaftar
            cur = conn.execute(
                "INSERT INTO pengguna (nama_lengkap, no_wa, alamat, kata_sandi) VALUES (?,?,?,?)",
                (data["nama_lengkap"], data["no_wa"], data["alamat"], data["kata_sandi"])
            )
            id_baru = cur.lastrowid
            conn.execute(
                "INSERT INTO dompet_digital (id_pengguna, saldo) VALUES (?, 0.0)", (id_baru,)
            )
        self._is_registered = True
        return True

    # ── Login (UC02) ─────────────────────────────────────────────────────────

    def verifikasi_kredensial(self, no_wa: str, sandi: str) -> bool:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT kata_sandi FROM pengguna WHERE no_wa = ?", (no_wa,)
            ).fetchone()
        if row is None:
            return False
        return row["kata_sandi"] == sandi

    def proses_login(self, no_wa: str, sandi: str) -> bool:
        if not self.verifikasi_kredensial(no_wa, sandi):
            return False
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM pengguna WHERE no_wa = ?", (no_wa,)
            ).fetchone()
        if row is None:
            return False
        self._pengguna = Pengguna(
            row["id_pengguna"], row["nama_lengkap"],
            row["no_wa"], row["alamat"], row["kata_sandi"]
        )
        self._is_logged_in = True
        return True

    # ── Profil (UC03, UC04, UC05) ────────────────────────────────────────────

    def ambil_data_profil(self, id_pengguna: int) -> Optional[Pengguna]:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM pengguna WHERE id_pengguna = ?", (id_pengguna,)
            ).fetchone()
        if row is None:
            return None
        return Pengguna(
            row["id_pengguna"], row["nama_lengkap"],
            row["no_wa"], row["alamat"], row["kata_sandi"]
        )

    def update_profil(self, id_pengguna: int, data: dict) -> bool:
        with get_connection() as conn:
            conn.execute(
                "UPDATE pengguna SET nama_lengkap=?, no_wa=?, alamat=? WHERE id_pengguna=?",
                (data["nama_lengkap"], data["no_wa"], data["alamat"], id_pengguna)
            )
        self._is_edit_success = True
        return True

    def ubah_kata_sandi(self, id_pengguna: int, sandi_lama: str, sandi_baru: str) -> bool:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT kata_sandi FROM pengguna WHERE id_pengguna = ?", (id_pengguna,)
            ).fetchone()
        if row is None or row["kata_sandi"] != sandi_lama:
            return False
        with get_connection() as conn:
            conn.execute(
                "UPDATE pengguna SET kata_sandi=? WHERE id_pengguna=?",
                (sandi_baru, id_pengguna)
            )
        return True

    # ── Dompet Digital (UC06, UC07, UC08) ────────────────────────────────────

    def lihat_saldo(self, id_pengguna: int) -> float:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT saldo FROM dompet_digital WHERE id_pengguna = ?", (id_pengguna,)
            ).fetchone()
        return row["saldo"] if row else 0.0

    def proses_isi_ulang(self, id_pengguna: int, nominal: float) -> bool:
        if nominal <= 0:
            return False
        with get_connection() as conn:
            conn.execute(
                "UPDATE dompet_digital SET saldo = saldo + ? WHERE id_pengguna = ?",
                (nominal, id_pengguna)
            )
        return True

    def proses_tarik_dana(self, id_pengguna: int, nominal: float) -> bool:
        if nominal <= 0:
            return False
        saldo = self.lihat_saldo(id_pengguna)
        if saldo < nominal:
            return False
        with get_connection() as conn:
            conn.execute(
                "UPDATE dompet_digital SET saldo = saldo - ? WHERE id_pengguna = ?",
                (nominal, id_pengguna)
            )
        return True

    # ── Convenience shorthands (dipakai views) ────────────────────────────────

    def login(self, no_wa: str, sandi: str) -> Optional[Pengguna]:
        """Shorthand: proses_login + return Pengguna object (None jika gagal)."""
        if self.proses_login(no_wa, sandi):
            return self._pengguna
        return None

    def registrasi(self, data: dict) -> bool:
        """Shorthand: proses_registrasi tanpa perlu konfirmasi_sandi di dict."""
        data_lengkap = {**data, "konfirmasi_sandi": data.get("kata_sandi", "")}
        return self.proses_registrasi(data_lengkap)
