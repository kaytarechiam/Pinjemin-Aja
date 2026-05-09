"""PeminjamanView — CD-12 / UC16, UC17
Combines Detail Alat (Layar 4b) + Peminjaman form (Layar 8).
"""
from __future__ import annotations
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSpinBox, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap

from controllers.alat_controller import AlatController
from controllers.transaksi_controller import TransaksiController
from session import Session
import views.ui_helper as UI


class PeminjamanView(QScrollArea):
    """Layar 4b + Layar 8 — Detail Alat & Peminjaman (UC16, UC17)."""

    go_back    = pyqtSignal()       # back to KatalogView
    go_riwayat = pyqtSignal()       # after successful rent → RiwayatView

    def __init__(self, id_alat: int, parent=None):
        super().__init__(parent)
        self._id_alat = id_alat
        self._alat_ctrl = AlatController()
        self._txn_ctrl  = TransaksiController()
        self._setup_ui()

    def _setup_ui(self):
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet(f"background: {UI.LIGHT_BG}; border: none;")

        alat = self._alat_ctrl.get_detail_alat(self._id_alat)
        if alat is None:
            w = QWidget()
            QVBoxLayout(w).addWidget(QLabel("Alat tidak ditemukan."))
            self.setWidget(w)
            return

        root = QWidget()
        root.setStyleSheet(f"background: {UI.LIGHT_BG};")
        layout = QVBoxLayout(root)
        layout.setContentsMargins(40, 24, 40, 40)
        layout.setSpacing(20)

        # Breadcrumb
        bc = QHBoxLayout()
        btn_back = QPushButton("← Explore Items")
        btn_back.setStyleSheet(
            f"background: transparent; color: {UI.BLUE}; border: none; font-size: 13px;"
        )
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.clicked.connect(self.go_back)
        bc.addWidget(btn_back)
        bc.addStretch()
        layout.addLayout(bc)

        # Main content
        content = QHBoxLayout()
        content.setSpacing(40)
        content.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ── Image box ──────────────────────────────────────────────────────
        img_box = QLabel()
        img_box.setFixedSize(400, 300)
        img_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bg = UI.category_color(alat.get_kategori())
        img_box.setStyleSheet(
            f"background: {bg}; border-radius: 16px; font-size: 80px;"
        )
        pm = UI.get_item_pixmap(alat.get_nama_alat(), 400, 300)
        if pm:
            img_box.setPixmap(pm)
            img_box.setScaledContents(True)
        else:
            img_box.setText(UI.category_emoji(alat.get_kategori()))

        content.addWidget(img_box)

        # ── Info panel ─────────────────────────────────────────────────────
        info = QVBoxLayout()
        info.setSpacing(14)
        info.setAlignment(Qt.AlignmentFlag.AlignTop)

        name_lbl = QLabel(alat.get_nama_alat())
        name_lbl.setStyleSheet(
            f"font-size: 26px; font-weight: 700; color: {UI.TEXT_DARK};"
        )
        name_lbl.setWordWrap(True)

        badges_row = QHBoxLayout()
        badges_row.setSpacing(8)
        status_badge = (UI.available_badge() if alat.get_status_ketersediaan() == "Tersedia"
                        else UI.unavailable_badge())
        cat_badge = UI.badge(alat.get_kategori(), UI.category_color(alat.get_kategori()), UI.TEXT_MID)
        cond_badge = UI.badge(alat.get_kondisi_alat(), UI.LIGHT_BG, UI.TEXT_GRAY)
        badges_row.addWidget(status_badge)
        badges_row.addWidget(cat_badge)
        badges_row.addWidget(cond_badge)
        badges_row.addStretch()

        price_lbl = QLabel(UI.format_rupiah(alat.get_harga_sewa()) + " / hari")
        price_lbl.setStyleSheet(f"font-size: 22px; font-weight: 700; color: {UI.BLUE};")

        # Owner
        owner_row = QHBoxLayout()
        owner_icon = QLabel("👤")
        owner_icon.setStyleSheet("font-size: 16px;")
        owner_name = QLabel(alat.get_nama_pemilik())
        owner_name.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {UI.TEXT_DARK};")
        owner_row.addWidget(owner_icon)
        owner_row.addWidget(owner_name)
        owner_row.addStretch()

        sep1 = UI.separator()

        # Description
        desc_title = QLabel("Deskripsi")
        desc_title.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {UI.TEXT_DARK};")
        desc_text = QLabel(alat.get_deskripsi() or "Tidak ada deskripsi.")
        desc_text.setStyleSheet(f"font-size: 13px; color: {UI.TEXT_MID}; line-height: 1.5;")
        desc_text.setWordWrap(True)
        desc_text.setMaximumWidth(400)

        sep2 = UI.separator()

        # Duration input (TF_Durasi — Layar 8)
        dur_title = QLabel("Durasi Peminjaman")
        dur_title.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {UI.TEXT_DARK};")

        dur_row = QHBoxLayout()
        self._spin_durasi = QSpinBox()
        self._spin_durasi.setMinimum(1)
        self._spin_durasi.setMaximum(365)
        self._spin_durasi.setValue(1)
        self._spin_durasi.setSuffix(" hari")
        self._spin_durasi.setStyleSheet(
            f"background: white; border: 1.5px solid {UI.BORDER}; border-radius: 8px;"
            f"padding: 8px 12px; font-size: 13px; color: {UI.TEXT_DARK};"
        )
        self._spin_durasi.setFixedHeight(42)
        self._spin_durasi.setFixedWidth(160)
        self._spin_durasi.valueChanged.connect(self._update_total)
        dur_row.addWidget(self._spin_durasi)
        dur_row.addStretch()

        # Total biaya & saldo (LabelTotalBiaya, LabelSaldoTersedia)
        self._lbl_total = QLabel()
        self._lbl_total.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {UI.BLUE};")

        saldo_now = 0.0
        user = Session.get_current_user()
        if user:
            from controllers.pengguna_controller import PenggunaController
            pc = PenggunaController()
            saldo_now = pc.lihat_saldo(user.get_id_pengguna())
        self._lbl_saldo = QLabel(f"Saldo tersedia: {UI.format_rupiah(saldo_now)}")
        self._lbl_saldo.setStyleSheet(f"font-size: 13px; color: {UI.TEXT_MID};")

        self._lbl_error = QLabel()
        self._lbl_error.setStyleSheet(f"color: {UI.RED}; font-size: 12px;")
        self._lbl_error.setWordWrap(True)
        self._lbl_error.hide()

        # Rent button / disabled
        if alat.get_status_ketersediaan() == "Tersedia":
            self._btn_pinjam = UI.primary_button("🛒  Konfirmasi Peminjaman")
            self._btn_pinjam.setFixedHeight(50)
            self._btn_pinjam.clicked.connect(self._on_pinjam)
        else:
            self._btn_pinjam = QPushButton("Alat Sedang Dipinjam")
            self._btn_pinjam.setStyleSheet(
                "background: #9CA3AF; color: white; border-radius: 8px;"
                "padding: 10px 20px; font-size: 14px; border: none;"
            )
            self._btn_pinjam.setEnabled(False)
            self._btn_pinjam.setFixedHeight(50)

        btn_batal = UI.outline_button("Batal")
        btn_batal.clicked.connect(self.go_back)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self._btn_pinjam)
        btn_row.addWidget(btn_batal)
        btn_row.addStretch()

        info.addWidget(name_lbl)
        info.addLayout(badges_row)
        info.addWidget(price_lbl)
        info.addLayout(owner_row)
        info.addWidget(sep1)
        info.addWidget(desc_title)
        info.addWidget(desc_text)
        info.addWidget(sep2)
        info.addWidget(dur_title)
        info.addLayout(dur_row)
        info.addWidget(self._lbl_total)
        info.addWidget(self._lbl_saldo)
        info.addWidget(self._lbl_error)
        info.addLayout(btn_row)

        content.addLayout(info)
        layout.addLayout(content)

        self._alat = alat
        self._update_total()
        self.setWidget(root)

    # ── Actions ───────────────────────────────────────────────────────────────

    def showFormPeminjaman(self):
        self._spin_durasi.setValue(1)
        self._lbl_error.hide()

    def _update_total(self):
        durasi = self._spin_durasi.value()
        total = self._alat.get_harga_sewa() * durasi
        self._lbl_total.setText(f"Total: {UI.format_rupiah(total)}  ({durasi} hari)")

    def showPesanSukses(self):
        UI.show_alert("Berhasil! 🎉", "Peminjaman berhasil dicatat.", self)

    def showPesanError(self, pesan: str):
        self._lbl_error.setText(pesan)
        self._lbl_error.show()

    def _on_pinjam(self):
        user = Session.get_current_user()
        if user is None:
            return
        if self._alat.get_id_pemilik() == user.get_id_pengguna():
            self.showPesanError("Anda tidak bisa meminjam alat milik sendiri.")
            return
        durasi = self._spin_durasi.value()
        total  = self._alat.get_harga_sewa() * durasi
        if not UI.show_confirm(
            f"Konfirmasi peminjaman:\n\n"
            f"Alat   : {self._alat.get_nama_alat()}\n"
            f"Durasi : {durasi} hari\n"
            f"Total  : {UI.format_rupiah(total)}", self
        ):
            return

        ok = self._txn_ctrl.proses_peminjaman(
            user.get_id_pengguna(), self._id_alat, durasi
        )
        if ok:
            self.showPesanSukses()
            self.go_riwayat.emit()
        else:
            if not self._txn_ctrl.cek_ketersediaan_alat(self._id_alat):
                self.showPesanError("Alat sedang tidak tersedia.")
            else:
                self.showPesanError("Saldo tidak mencukupi untuk melakukan peminjaman.")
