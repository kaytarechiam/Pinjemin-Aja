class Alat:
    """Entity class — C-05 / CD-09"""

    def __init__(self, id_alat: int, id_pemilik: int, nama_pemilik: str,
                 nama_alat: str, deskripsi: str, kategori: str,
                 harga_sewa: float, kondisi_alat: str, status_ketersediaan: str):
        self._id_alat             = id_alat
        self._id_pemilik          = id_pemilik
        self._nama_pemilik        = nama_pemilik
        self._nama_alat           = nama_alat
        self._deskripsi           = deskripsi
        self._kategori            = kategori
        self._harga_sewa          = harga_sewa
        self._kondisi_alat        = kondisi_alat
        self._status_ketersediaan = status_ketersediaan

    def get_id_alat(self) -> int:
        return self._id_alat

    def get_id_pemilik(self) -> int:
        return self._id_pemilik

    def get_nama_pemilik(self) -> str:
        return self._nama_pemilik

    def get_nama_alat(self) -> str:
        return self._nama_alat

    def get_deskripsi(self) -> str:
        return self._deskripsi or ""

    def get_kategori(self) -> str:
        return self._kategori

    def get_harga_sewa(self) -> float:
        return self._harga_sewa

    def get_kondisi_alat(self) -> str:
        return self._kondisi_alat

    def get_status_ketersediaan(self) -> str:
        return self._status_ketersediaan

    def set_status_ketersediaan(self, status: str):
        self._status_ketersediaan = status

    def set_harga_sewa(self, harga: float):
        self._harga_sewa = harga

    def set_deskripsi(self, deskripsi: str):
        self._deskripsi = deskripsi
