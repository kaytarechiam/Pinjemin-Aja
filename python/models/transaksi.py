class Transaksi:
    """Entity class — C-07 / CD-13"""

    def __init__(self, id_transaksi: int, id_peminjam: int, id_penyedia: int,
                 id_alat: int, nama_alat: str, nama_peminjam: str, nama_penyedia: str,
                 tanggal_transaksi: str, durasi: int, total_biaya: float, status: str):
        self._id_transaksi      = id_transaksi
        self._id_peminjam       = id_peminjam
        self._id_penyedia       = id_penyedia
        self._id_alat           = id_alat
        self._nama_alat         = nama_alat
        self._nama_peminjam     = nama_peminjam
        self._nama_penyedia     = nama_penyedia
        self._tanggal_transaksi = tanggal_transaksi
        self._durasi            = durasi
        self._total_biaya       = total_biaya
        self._status            = status

    def get_id_transaksi(self) -> int:
        return self._id_transaksi

    def get_id_peminjam(self) -> int:
        return self._id_peminjam

    def get_id_penyedia(self) -> int:
        return self._id_penyedia

    def get_id_alat(self) -> int:
        return self._id_alat

    def get_nama_alat(self) -> str:
        return self._nama_alat

    def get_nama_peminjam(self) -> str:
        return self._nama_peminjam

    def get_nama_penyedia(self) -> str:
        return self._nama_penyedia

    def get_tanggal_transaksi(self) -> str:
        return self._tanggal_transaksi

    def get_durasi(self) -> int:
        return self._durasi

    def get_total_biaya(self) -> float:
        return self._total_biaya

    def get_status(self) -> str:
        return self._status

    def set_status(self, status: str):
        self._status = status

    def get_detail(self) -> str:
        return (f"Transaksi #{self._id_transaksi} | Alat: {self._nama_alat} | "
                f"Durasi: {self._durasi} hari | Total: Rp {self._total_biaya:,.0f} | "
                f"Status: {self._status}")
