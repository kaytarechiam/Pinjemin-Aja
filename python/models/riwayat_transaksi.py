from __future__ import annotations
from typing import List
from models.transaksi import Transaksi


class RiwayatTransaksi:
    """Entity class — C-10 / CD-16"""

    def __init__(self, id_pengguna: int, daftar_transaksi: List[Transaksi]):
        self._id_pengguna       = id_pengguna
        self._daftar_transaksi  = daftar_transaksi

    def get_daftar_transaksi(self) -> List[Transaksi]:
        return self._daftar_transaksi

    def filter_riwayat(self, jenis: str) -> List[Transaksi]:
        """jenis: 'peminjam' | 'penyedia'"""
        if jenis == "peminjam":
            return [t for t in self._daftar_transaksi
                    if t.get_id_peminjam() == self._id_pengguna]
        elif jenis == "penyedia":
            return [t for t in self._daftar_transaksi
                    if t.get_id_penyedia() == self._id_pengguna]
        return self._daftar_transaksi
