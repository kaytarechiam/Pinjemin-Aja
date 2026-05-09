"""RegistrasiView — UC01 — two-panel layout matching Java design."""
from __future__ import annotations
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton,
    QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QRectF
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QLinearGradient

from controllers.pengguna_controller import PenggunaController
import views.ui_helper as UI
from views.login_view import _LeftPanel, _FormCard


class RegistrasiView(QWidget):
    """Layar 3 — Registrasi Akun Baru (UC01)."""

    go_login = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ctrl = PenggunaController()
        self._setup_ui()

    def _setup_ui(self):
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        outer.addWidget(_LeftPanel())

        # Right: scrollable form
        right = QWidget()
        right.setStyleSheet(f"background: {UI.LIGHT_BG};")
        right_layout = QVBoxLayout(right)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.setContentsMargins(48, 32, 48, 32)

        card = _FormCard()
        card.setFixedWidth(420)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 36, 40, 36)
        card_layout.setSpacing(0)

        # Title
        lbl_title = QLabel("Create an account ✨")
        lbl_title.setStyleSheet(
            f"font-size: 20px; font-weight: 700; color: {UI.TEXT_DARK}; background: transparent;"
        )
        lbl_sub = QLabel("Bergabung dengan komunitas Pinjemin Aja!")
        lbl_sub.setStyleSheet(
            f"font-size: 12px; color: {UI.TEXT_GRAY}; background: transparent;"
        )
        card_layout.addWidget(lbl_title)
        card_layout.addSpacing(4)
        card_layout.addWidget(lbl_sub)
        card_layout.addSpacing(20)

        # Fields
        self._tf_nama     = UI.styled_input("Nama lengkap")
        self._tf_no_wa    = UI.styled_input("Nomor WhatsApp")
        self._tf_alamat   = UI.styled_textarea("Alamat lengkap")
        self._tf_alamat.setFixedHeight(72)
        self._tf_password = UI.styled_password("Kata sandi (min. 6 karakter)")
        self._tf_konfirm  = UI.styled_password("Konfirmasi kata sandi")

        for label, widget in [
            ("Nama Lengkap",       self._tf_nama),
            ("Nomor WhatsApp",     self._tf_no_wa),
            ("Alamat",             self._tf_alamat),
            ("Password",           self._tf_password),
            ("Konfirmasi Password", self._tf_konfirm),
        ]:
            lbl = QLabel(label)
            lbl.setStyleSheet(
                f"font-size: 12px; font-weight: 600; color: {UI.TEXT_MID}; background: transparent;"
            )
            card_layout.addWidget(lbl)
            card_layout.addSpacing(5)
            card_layout.addWidget(widget)
            card_layout.addSpacing(12)

        # Error
        self._lbl_error = QLabel("")
        self._lbl_error.setStyleSheet(f"color: {UI.RED}; font-size: 12px; background: transparent;")
        self._lbl_error.setWordWrap(True)
        self._lbl_error.hide()
        card_layout.addWidget(self._lbl_error)
        card_layout.addSpacing(16)

        # Register button
        btn_daftar = UI.primary_button("Create Account")
        btn_daftar.setFixedHeight(46)
        btn_daftar.clicked.connect(self._on_daftar)
        card_layout.addWidget(btn_daftar)
        card_layout.addSpacing(14)

        # Login link
        link_masuk = QPushButton("Already have an account? Log In →")
        link_masuk.setCursor(Qt.CursorShape.PointingHandCursor)
        link_masuk.setStyleSheet(
            "QPushButton {"
            f"  background: transparent; color: {UI.TEXT_GRAY};"
            "  border: none; font-size: 12px;"
            "}"
            f"QPushButton:hover {{ color: {UI.BLUE}; }}"
        )
        link_masuk.clicked.connect(self.go_login)
        card_layout.addWidget(link_masuk, alignment=Qt.AlignmentFlag.AlignCenter)

        right_layout.addWidget(card)
        outer.addWidget(right, 1)

    # ── Public API ────────────────────────────────────────────────────────────

    def showFormRegistrasi(self):
        for w in (self._tf_nama, self._tf_no_wa, self._tf_password, self._tf_konfirm):
            w.clear()
        self._tf_alamat.clear()
        self._lbl_error.hide()

    def showPesanError(self, pesan: str):
        self._lbl_error.setText(pesan)
        self._lbl_error.show()

    # ── Internal ──────────────────────────────────────────────────────────────

    def _on_daftar(self):
        self._lbl_error.hide()
        nama      = self._tf_nama.text().strip()
        no_wa     = self._tf_no_wa.text().strip()
        alamat    = self._tf_alamat.toPlainText().strip()
        password  = self._tf_password.text()
        konfirm   = self._tf_konfirm.text()

        if not all([nama, no_wa, alamat, password]):
            self.showPesanError("Semua kolom harus diisi.")
            return
        if len(password) < 6:
            self.showPesanError("Password minimal 6 karakter.")
            return
        if password != konfirm:
            self.showPesanError("Konfirmasi password tidak cocok.")
            return

        ok = self._ctrl.registrasi({
            "nama_lengkap": nama,
            "no_wa":        no_wa,
            "alamat":       alamat,
            "kata_sandi":   password,
        })
        if ok:
            UI.show_alert("Berhasil", "Akun berhasil dibuat. Silakan login.", self)
            self.go_login.emit()
        else:
            self.showPesanError("Nomor WhatsApp sudah terdaftar.")
