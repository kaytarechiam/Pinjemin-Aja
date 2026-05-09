"""RiwayatView — CD-15 / UC18, UC19, UC20, UC21"""
from __future__ import annotations
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QScrollArea, QDialog, QDialogButtonBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from controllers.riwayat_controller import RiwayatController
from models.transaksi import Transaksi
from session import Session
import views.ui_helper as UI


class RiwayatView(QWidget):
    """Layar 9 — Riwayat Transaksi (UC18, UC19, UC20, UC21)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ctrl = RiwayatController()
        self._riwayat = None   # RiwayatTransaksi object
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"background: {UI.LIGHT_BG};")
        root = QVBoxLayout(self)
        root.setContentsMargins(30, 24, 30, 24)
        root.setSpacing(16)

        # Header
        hdr = QHBoxLayout()
        hdr.addWidget(UI.heading("Riwayat Transaksi"))
        hdr.addStretch()

        # Filter dropdown (UC20)
        self._ddl_filter = QComboBox()
        self._ddl_filter.addItems(["Semua", "Sebagai Peminjam", "Sebagai Penyedia"])
        self._ddl_filter.setStyleSheet(
            f"background: white; border: 1.5px solid {UI.BORDER}; border-radius: 8px;"
            f"padding: 8px 12px; font-size: 13px; color: {UI.TEXT_DARK};"
        )
        self._ddl_filter.setFixedHeight(40)
        self._ddl_filter.setFixedWidth(200)
        self._ddl_filter.currentIndexChanged.connect(self._on_filter)
        hdr.addWidget(self._ddl_filter)
        root.addLayout(hdr)

        # Card
        card = QWidget()
        card.setStyleSheet(f"background: white; border-radius: 12px; border: 1px solid {UI.BORDER};")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(12)

        # Table
        self._table = QTableWidget()
        self._table.setColumnCount(8)
        self._table.setHorizontalHeaderLabels([
            "ID", "Alat", "Peminjam", "Penyedia",
            "Durasi", "Total Biaya", "Status", "Aksi"
        ])
        self._table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self._table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        self._table.setColumnWidth(0, 40)
        self._table.setColumnWidth(4, 70)
        self._table.setColumnWidth(5, 120)
        self._table.setColumnWidth(6, 100)
        self._table.setColumnWidth(7, 180)
        self._table.verticalHeader().setVisible(False)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setStyleSheet(
            f"QTableWidget {{ border: none; font-size: 12px; color: {UI.TEXT_DARK}; }}"
            f"QHeaderView::section {{ background: {UI.LIGHT_BG}; font-weight: 600;"
            f"padding: 8px; border: none; font-size: 12px; }}"
        )
        self._table.setMinimumHeight(420)

        self._lbl_feedback = QLabel()
        self._lbl_feedback.setWordWrap(True)
        self._lbl_feedback.setStyleSheet(f"color: {UI.RED}; font-size: 12px;")
        self._lbl_feedback.hide()

        card_layout.addWidget(self._table)
        card_layout.addWidget(self._lbl_feedback)
        root.addWidget(card)

        self.showRiwayat()

    # ── Public API ────────────────────────────────────────────────────────────

    def showRiwayat(self, riwayat=None):
        """UC19 — Lihat Riwayat."""
        user = Session.get_current_user()
        if user is None:
            return
        if riwayat is None:
            self._riwayat = self._ctrl.load_riwayat(user.get_id_pengguna())
        else:
            self._riwayat = riwayat
        self._render_table(self._riwayat.get_daftar_transaksi() if self._riwayat else [])

    def showFilterRiwayat(self, jenis: str):
        """UC20 — Filter Riwayat."""
        if self._riwayat is None:
            return
        filtered = self._ctrl.proses_filter(self._riwayat, jenis)
        self._render_table(filtered)

    def showDetailTransaksi(self, id_transaksi: int):
        """UC21 — Detail Transaksi."""
        txn = self._ctrl.load_detail_transaksi(id_transaksi)
        if txn is None:
            UI.show_error("Error", "Data transaksi tidak ditemukan.", self)
            return
        dlg = _DetailDialog(txn, parent=self)
        dlg.exec()

    def showPesanSukses(self, pesan: str):
        self._lbl_feedback.setStyleSheet(f"color: {UI.GREEN}; font-size: 12px;")
        self._lbl_feedback.setText(pesan)
        self._lbl_feedback.show()

    def showPesanError(self, pesan: str):
        self._lbl_feedback.setStyleSheet(f"color: {UI.RED}; font-size: 12px;")
        self._lbl_feedback.setText(pesan)
        self._lbl_feedback.show()

    # ── Internal ──────────────────────────────────────────────────────────────

    def _on_filter(self, index: int):
        mapping = {0: "semua", 1: "peminjam", 2: "penyedia"}
        self.showFilterRiwayat(mapping.get(index, "semua"))

    def _render_table(self, daftar: list[Transaksi]):
        user = Session.get_current_user()
        self._table.setRowCount(0)
        for txn in daftar:
            row = self._table.rowCount()
            self._table.insertRow(row)

            self._table.setItem(row, 0, QTableWidgetItem(str(txn.get_id_transaksi())))
            self._table.setItem(row, 1, QTableWidgetItem(txn.get_nama_alat()))
            self._table.setItem(row, 2, QTableWidgetItem(txn.get_nama_peminjam()))
            self._table.setItem(row, 3, QTableWidgetItem(txn.get_nama_penyedia()))
            self._table.setItem(row, 4, QTableWidgetItem(f"{txn.get_durasi()} hari"))
            self._table.setItem(row, 5, QTableWidgetItem(UI.format_rupiah(txn.get_total_biaya())))

            status_item = QTableWidgetItem(txn.get_status())
            if txn.get_status() == "Selesai":
                status_item.setForeground(QColor("#065F46"))
                status_item.setBackground(QColor("#D1FAE5"))
            else:
                status_item.setForeground(QColor("#92400E"))
                status_item.setBackground(QColor("#FEF3C7"))
            self._table.setItem(row, 6, status_item)

            # Action buttons
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(4, 2, 4, 2)
            btn_layout.setSpacing(6)

            # Detail button (UC21)
            btn_detail = QPushButton("Detail")
            btn_detail.setStyleSheet(
                f"background: {UI.BLUE_LIGHT}; color: {UI.BLUE}; border-radius: 6px;"
                f"padding: 4px 10px; font-size: 11px; border: none; font-weight: 600;"
            )
            btn_detail.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_detail.clicked.connect(
                lambda _, tid=txn.get_id_transaksi(): self.showDetailTransaksi(tid)
            )
            btn_layout.addWidget(btn_detail)

            # Konfirmasi Pengembalian (UC18) — only for penyedia when status is Berjalan
            if (user and
                txn.get_id_penyedia() == user.get_id_pengguna() and
                txn.get_status() == "Berjalan"):
                btn_konfirmasi = QPushButton("✓ Selesai")
                btn_konfirmasi.setStyleSheet(
                    f"background: {UI.GREEN_LIGHT}; color: {UI.GREEN}; border-radius: 6px;"
                    f"padding: 4px 10px; font-size: 11px; border: none; font-weight: 600;"
                )
                btn_konfirmasi.setCursor(Qt.CursorShape.PointingHandCursor)
                btn_konfirmasi.clicked.connect(
                    lambda _, tid=txn.get_id_transaksi(): self._on_konfirmasi(tid)
                )
                btn_layout.addWidget(btn_konfirmasi)

            self._table.setCellWidget(row, 7, btn_widget)
            self._table.setRowHeight(row, 46)

    def _on_konfirmasi(self, id_transaksi: int):
        """UC18 — Konfirmasi Pengembalian."""
        if not UI.show_confirm(
            "Konfirmasi bahwa alat telah dikembalikan oleh peminjam?\n"
            "Status transaksi akan diubah menjadi Selesai.", self
        ):
            return
        ok = self._ctrl.konfirmasi_pengembalian(id_transaksi)
        if ok:
            self.showPesanSukses("Pengembalian dikonfirmasi. Status transaksi: Selesai.")
            self.showRiwayat()
        else:
            self.showPesanError("Gagal mengkonfirmasi pengembalian.")


class _DetailDialog(QDialog):
    """Dialog detail transaksi (UC21)."""

    def __init__(self, txn: Transaksi, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Detail Transaksi #{txn.get_id_transaksi()}")
        self.setMinimumWidth(420)
        self._setup_ui(txn)

    def _setup_ui(self, txn: Transaksi):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(28, 28, 28, 28)

        # Title
        title = QLabel(f"Transaksi #{txn.get_id_transaksi()}")
        title.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {UI.TEXT_DARK};")
        layout.addWidget(title)

        layout.addWidget(UI.separator())

        rows = [
            ("Nama Alat",    txn.get_nama_alat()),
            ("Peminjam",     txn.get_nama_peminjam()),
            ("Penyedia",     txn.get_nama_penyedia()),
            ("Durasi",       f"{txn.get_durasi()} hari"),
            ("Total Biaya",  UI.format_rupiah(txn.get_total_biaya())),
            ("Tanggal",      str(txn.get_tanggal_transaksi())),
            ("Status",       txn.get_status()),
        ]
        for label, value in rows:
            row_w = QHBoxLayout()
            lbl_k = QLabel(label)
            lbl_k.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {UI.TEXT_MID}; min-width: 100px;")
            lbl_v = QLabel(value)
            lbl_v.setStyleSheet(f"font-size: 13px; color: {UI.TEXT_DARK};")
            lbl_v.setWordWrap(True)
            row_w.addWidget(lbl_k)
            row_w.addWidget(lbl_v)
            row_w.addStretch()
            layout.addLayout(row_w)

        layout.addWidget(UI.separator())

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)
