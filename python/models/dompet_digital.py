class DompetDigital:
    """Entity class — C-04 / CD-04"""

    def __init__(self, id_dompet: int, id_pengguna: int, saldo: float):
        self._id_dompet   = id_dompet
        self._id_pengguna = id_pengguna
        self._saldo       = saldo

    def get_id_dompet(self) -> int:
        return self._id_dompet

    def get_id_pengguna(self) -> int:
        return self._id_pengguna

    def get_saldo(self) -> float:
        return self._saldo

    def tambah_saldo(self, nominal: float):
        self._saldo += nominal

    def kurangi_saldo(self, nominal: float):
        self._saldo -= nominal

    def is_saldo_cukup(self, nominal: float) -> bool:
        return self._saldo >= nominal
