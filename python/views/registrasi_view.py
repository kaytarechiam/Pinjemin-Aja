"""RegistrasiView — CD-01 / UC01"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QTextEdit, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QLinearGradient, QPainter, QColor, QBrush, QPalette

from controllers.pengguna_controller import PenggunaController
import views.ui_helper as UI


class RegistrasiView(QWidget):
    """Layar 1 — Registrasi Akun (UC01)."""

    go_login = pyqtSignal()   # navigate to LoginView

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ctrl = PenggunaController()
        self._setup_ui()

    # ── UI ───────────────────────────────────────────────────────────────────

    def _setup_ui(self):
        self.setStyleSheet(f"background: {UI.LIGHT_BG};")
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Left gradient panel
        left = self._build_left_panel()
        root.addWidget(left, 4)

        # Right form panel
        right = self._build_right_panel()
        root.addWidget(right, 6)

    def _build_left_panel(self) -> QWidget:
        panel = QWidget()
        panel.setStyleSheet(
            f"background: qlineargradient(x1:0,y1:0,x2:1,y2:1,"
            f"stop:0 {UI.BLUE}, stop:1 {UI.BLUE_DARK});"
        )
        layout = QVBoxLayout(panel)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(16)

        icon = QLabel("🏠")
        icon.setStyleSheet("font-size: 56px; background: transparent;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Pinjemin Aja!")
        title.setStyleSheet("font-size: 28px; font-weight: 700; color: white; background: transparent;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sub = QLabel("Berbagi Alat, Hemat Bersama")
        sub.setStyleSheet("font-size: 14px; color: rgba(255,255,255,0.8); background: transparent;")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for feat in ["✅  Daftar gratis, langsung pakai",
                     "🔒  Data aman & terenkripsi",
                     "💳  Dompet digital terintegrasi"]:
            lbl = QLabel(feat)
            lbl.setStyleSheet("font-size: 13px; color: rgba(255,255,255,0.9); background: transparent; padding: 4px 0;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl)

        layout.insertWidget(0, icon)
        layout.insertWidget(1, title)
        layout.insertWidget(2, sub)
        layout.insertWidget(3, UI.separator())
        return panel

    def _build_right_panel(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: white; border: none;")

        inner = QWidget()
        inner.setStyleSheet("background: white;")
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(60, 50, 60, 50)
        layout.setSpacing(14)

        title = QLabel("Sign Up")
        title.setStyleSheet(f"font-size: 26px; font-weight: 700; color: {UI.TEXT_DARK};")

        sub = QLabel("Buat akun baru untuk mulai meminjam & menyewakan alat.")
        sub.setStyleSheet(f"font-size: 13px; color: {UI.TEXT_GRAY};")
        sub.setWordWrap(True)

        # Fields
        self._tf_nama   = UI.styled_input("Full Name")
        self._tf_no_wa  = UI.styled_input("WhatsApp Number (e.g. 08123456789)")
        self._tf_alamat = UI.styled_textarea("Address")
        self._tf_alamat.setFixedHeight(80)
        self._tf_pass   = UI.styled_password("Password")
        self._tf_konfirmasi = UI.styled_password("Confirm Password")

        self._lbl_error = QLabel()
        self._lbl_error.setStyleSheet(f"color: {UI.RED}; font-size: 12px;")
        self._lbl_error.setWordWrap(True)
        self._lbl_error.hide()

        btn_daftar = UI.primary_button("Sign Up")
        btn_daftar.setFixedHeight(48)
        btn_daftar.clicked.connect(self._on_daftar)

        link_login = QPushButton("Already have an account? Log In")
        link_login.setStyleSheet(
            f"background: transparent; color: {UI.BLUE}; border: none;"
            f"font-size: 13px; text-decoration: underline;"
        )
        link_login.setCursor(Qt.CursorShape.PointingHandCursor)
        link_login.clicked.connect(self.go_login)

        for lbl_text, widget in [
            ("Full Name", self._tf_nama),
            ("WhatsApp Number", self._tf_no_wa),
            ("Address", self._tf_alamat),
            ("Password", self._tf_pass),
            ("Confirm Password", self._tf_konfirmasi),
        ]:
            lbl = QLabel(lbl_text)
            lbl.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {UI.TEXT_MID};")
            layout.addWidget(lbl)
            layout.addWidget(widget)

        layout.insertWidget(0, title)
        layout.insertWidget(1, sub)
        layout.insertSpacing(2, 8)
        layout.addWidget(self._lbl_error)
        layout.addSpacing(4)
        layout.addWidget(btn_daftar)
        layout.addWidget(link_login, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        scroll.setWidget(inner)
        return scroll

    # ── Actions ───────────────────────────────────────────────────────────────

    def showFormRegistrasi(self):
        """UC01 — called when this view is shown."""
        self._tf_nama.clear()
        self._tf_no_wa.clear()
        self._tf_alamat.clear()
        self._tf_pass.clear()
        self._tf_konfirmasi.clear()
        self._lbl_error.hide()

    def getInputData(self) -> dict:
        return {
            "nama_lengkap":     self._tf_nama.text().strip(),
            "no_wa":            self._tf_no_wa.text().strip(),
            "alamat":           self._tf_alamat.toPlainText().strip(),
            "kata_sandi":       self._tf_pass.text(),
            "konfirmasi_sandi": self._tf_konfirmasi.text(),
        }

    def showPesanError(self, pesan: str):
        self._lbl_error.setText(pesan)
        self._lbl_error.show()

    def showPesanSukses(self):
        UI.show_alert("Registrasi Berhasil ✓",
                      "Akun berhasil dibuat. Silakan login.", self)

    def _on_daftar(self):
        data = self.getInputData()
        if not data["nama_lengkap"] or not data["no_wa"] or not data["alamat"]:
            self.showPesanError("Semua kolom harus diisi.")
            return
        if not data["kata_sandi"]:
            self.showPesanError("Password tidak boleh kosong.")
            return
        if data["kata_sandi"] != data["konfirmasi_sandi"]:
            self.showPesanError("Password dan konfirmasi tidak cocok.")
            return

        ok = self._ctrl.proses_registrasi(data)
        if ok:
            self.showPesanSukses()
            self.go_login.emit()
        else:
            self.showPesanError("Nomor WhatsApp sudah terdaftar atau data tidak valid.")
