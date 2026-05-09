"""KatalogSayaView — CD-11 / UC10, UC11, UC12, UC13"""
from __future__ import annotations
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QDialogButtonBox, QFormLayout, QMessageBox,
    QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from controllers.alat_controller import AlatController
from models.alat import Alat
from session import Session
import views.ui_helper as UI

CATEGORIES = ["Kitchen", "Tools", "Cleaning", "Electronics", "Gardening"]
CONDITIONS  = ["Good", "Cukup Baik", "Perlu Perbaikan"]


class KatalogSayaView(QWidget):
    """Layar 5 — Katalog Saya (UC10, UC11, UC12, UC13)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ctrl = AlatController()
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"background: {UI.LIGHT_BG};")
        root = QVBoxLayout(self)
        root.setContentsMargins(30, 24, 30, 24)
        root.setSpacing(16)

        # Header
        hdr = QHBoxLayout()
        hdr.addWidget(UI.heading("Katalog Saya"))
        hdr.addStretch()
        btn_tambah = UI.primary_button("+ Tambah Alat")
        btn_tambah.clicked.connect(self._show_form_tambah)
        hdr.addWidget(btn_tambah)
        root.addLayout(hdr)

        # Card — use ShadowCard
        card = UI.ShadowCard(12)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(12)

        # Table (ListAlatSaya)
        self._table = QTableWidget()
        self._table.setColumnCount(6)
        self._table.setHorizontalHeaderLabels(["Nama Alat", "Kategori", "Harga/hari", "Kondisi", "Status", "Aksi"])
        self._table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self._table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self._table.setColumnWidth(5, 150)
        self._table.verticalHeader().setVisible(False)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setStyleSheet(
            f"QTableWidget {{ border: none; font-size: 13px; color: {UI.TEXT_DARK}; }}"
            f"QHeaderView::section {{ background: {UI.LIGHT_BG}; font-weight: 600; padding: 8px; border: none; }}"
        )
        self._table.setMinimumHeight(400)

        card_layout.addWidget(self._table)
        root.addWidget(card)

        self.showKatalogSaya()

    # ── Public API ────────────────────────────────────────────────────────────

    def showKatalogSaya(self, daftar: list[Alat] | None = None):
        user = Session.get_current_user()
        if user is None:
            return
        if daftar is None:
            daftar = self._ctrl.get_alat_from_pengguna(user.get_id_pengguna())
        self._render_table(daftar)

    def showFormTambahAlat(self):
        self._show_form_tambah()

    def showFormEditAlat(self, alat: Alat):
        self._show_form_edit(alat)

    def showDialogHapus(self, id_alat: int):
        self._confirm_hapus(id_alat)

    def showPesanSukses(self, pesan: str):
        UI.show_toast(pesan, self, "success")

    def showPesanError(self, pesan: str):
        UI.show_toast(pesan, self, "error")

    # ── Internal ──────────────────────────────────────────────────────────────

    def _render_table(self, daftar: list[Alat]):
        self._table.setRowCount(0)
        for alat in daftar:
            row = self._table.rowCount()
            self._table.insertRow(row)
            self._table.setItem(row, 0, QTableWidgetItem(alat.get_nama_alat()))
            self._table.setItem(row, 1, QTableWidgetItem(alat.get_kategori()))
            self._table.setItem(row, 2, QTableWidgetItem(UI.format_rupiah(alat.get_harga_sewa())))
            self._table.setItem(row, 3, QTableWidgetItem(alat.get_kondisi_alat()))
            status_item = QTableWidgetItem(alat.get_status_ketersediaan())
            if alat.get_status_ketersediaan() == "Tersedia":
                status_item.setForeground(QColor("#065F46"))
            else:
                status_item.setForeground(QColor("#991B1B"))
            self._table.setItem(row, 4, status_item)

            # Action buttons
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(4, 2, 4, 2)
            btn_layout.setSpacing(6)

            btn_edit = QPushButton("Edit")
            btn_edit.setStyleSheet(
                f"background: {UI.BLUE_LIGHT}; color: {UI.BLUE}; border-radius: 6px;"
                f"padding: 4px 12px; font-size: 12px; border: none; font-weight: 600;"
            )
            btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)

            btn_hapus = QPushButton("Hapus")
            btn_hapus.setStyleSheet(
                f"background: {UI.RED_LIGHT}; color: {UI.RED}; border-radius: 6px;"
                f"padding: 4px 12px; font-size: 12px; border: none; font-weight: 600;"
            )
            btn_hapus.setCursor(Qt.CursorShape.PointingHandCursor)

            _alat = alat  # capture
            btn_edit.clicked.connect(lambda _, a=_alat: self.showFormEditAlat(a))
            btn_hapus.clicked.connect(lambda _, aid=alat.get_id_alat(): self._confirm_hapus(aid))

            btn_layout.addWidget(btn_edit)
            btn_layout.addWidget(btn_hapus)
            self._table.setCellWidget(row, 5, btn_widget)
            self._table.setRowHeight(row, 46)

    def _show_form_tambah(self):
        dlg = _AlatFormDialog("Tambah Alat", parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            user = Session.get_current_user()
            if user:
                data["id_pengguna"] = user.get_id_pengguna()
                if self._ctrl.tambah_alat(data):
                    self.showPesanSukses("Alat berhasil ditambahkan ke katalog.")
                    self.showKatalogSaya()
                else:
                    self.showPesanError("Gagal menambahkan alat.")

    def _show_form_edit(self, alat: Alat):
        dlg = _AlatFormDialog("Edit Alat", alat=alat, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            if self._ctrl.update_alat(alat.get_id_alat(), data):
                self.showPesanSukses("Informasi alat berhasil diperbarui.")
                self.showKatalogSaya()
            else:
                self.showPesanError("Gagal memperbarui alat.")

    def _confirm_hapus(self, id_alat: int):
        if UI.show_confirm("Yakin ingin menghapus alat ini dari katalog?", self):
            if self._ctrl.hapus_alat(id_alat):
                self.showPesanSukses("Alat berhasil dihapus dari katalog.")
                self.showKatalogSaya()
            else:
                self.showPesanError("Alat tidak dapat dihapus karena sedang dipinjam.")


class _AlatFormDialog(QDialog):
    """Internal dialog for Tambah/Edit Alat."""

    def __init__(self, title: str, alat: Alat | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(440)
        self._alat = alat
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        form = QFormLayout()
        form.setSpacing(10)

        self._tf_nama = UI.styled_input("Nama alat")
        self._tf_harga = UI.styled_input("Harga sewa / hari (Rp)")
        self._ddl_kategori = QComboBox()
        self._ddl_kategori.addItems(CATEGORIES)
        self._ddl_kategori.setStyleSheet(UI.input_style())
        self._ddl_kategori.setFixedHeight(42)

        self._ddl_kondisi = QComboBox()
        self._ddl_kondisi.addItems(CONDITIONS)
        self._ddl_kondisi.setStyleSheet(UI.input_style())
        self._ddl_kondisi.setFixedHeight(42)

        self._tf_deskripsi = UI.styled_textarea("Deskripsi alat...")
        self._tf_deskripsi.setFixedHeight(80)

        if self._alat:
            self._tf_nama.setText(self._alat.get_nama_alat())
            self._tf_harga.setText(str(int(self._alat.get_harga_sewa())))
            idx = self._ddl_kategori.findText(self._alat.get_kategori())
            if idx >= 0:
                self._ddl_kategori.setCurrentIndex(idx)
            idx2 = self._ddl_kondisi.findText(self._alat.get_kondisi_alat())
            if idx2 >= 0:
                self._ddl_kondisi.setCurrentIndex(idx2)
            self._tf_deskripsi.setPlainText(self._alat.get_deskripsi())

        form.addRow("Nama Alat", self._tf_nama)
        form.addRow("Harga / hari (Rp)", self._tf_harga)
        form.addRow("Kategori", self._ddl_kategori)
        form.addRow("Kondisi", self._ddl_kondisi)
        form.addRow("Deskripsi", self._tf_deskripsi)

        self._lbl_error = QLabel()
        self._lbl_error.setStyleSheet(f"color: {UI.RED}; font-size: 12px;")
        self._lbl_error.hide()

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self._validate)
        btns.rejected.connect(self.reject)

        layout.addLayout(form)
        layout.addWidget(self._lbl_error)
        layout.addWidget(btns)

    def _validate(self):
        if not self._tf_nama.text().strip():
            self._lbl_error.setText("Nama alat tidak boleh kosong.")
            self._lbl_error.show()
            return
        try:
            float(self._tf_harga.text().strip())
        except ValueError:
            self._lbl_error.setText("Harga harus berupa angka.")
            self._lbl_error.show()
            return
        self.accept()

    def get_data(self) -> dict:
        return {
            "nama_alat":    self._tf_nama.text().strip(),
            "harga_sewa":   float(self._tf_harga.text().strip()),
            "kategori":     self._ddl_kategori.currentText(),
            "kondisi_alat": self._ddl_kondisi.currentText(),
            "deskripsi":    self._tf_deskripsi.toPlainText().strip(),
        }
