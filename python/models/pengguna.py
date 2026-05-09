class Pengguna:
    """Entity class — C-02 / CD-02"""

    def __init__(self, id_pengguna: int, nama_lengkap: str, no_wa: str,
                 alamat: str, kata_sandi: str):
        self._id_pengguna  = id_pengguna
        self._nama_lengkap = nama_lengkap
        self._no_wa        = no_wa
        self._alamat       = alamat
        self._kata_sandi   = kata_sandi

    def get_id_pengguna(self) -> int:
        return self._id_pengguna

    def get_nama_lengkap(self) -> str:
        return self._nama_lengkap

    def get_no_wa(self) -> str:
        return self._no_wa

    def get_alamat(self) -> str:
        return self._alamat

    def get_kata_sandi(self) -> str:
        return self._kata_sandi

    def set_nama_lengkap(self, nama: str):
        self._nama_lengkap = nama

    def set_no_wa(self, no_wa: str):
        self._no_wa = no_wa

    def set_alamat(self, alamat: str):
        self._alamat = alamat

    def set_kata_sandi(self, hash_sandi: str):
        self._kata_sandi = hash_sandi
