"""LoginView — CD-05 / UC02"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal

from controllers.pengguna_controller import PenggunaController
from models.pengguna import Pengguna
from session import Session
import views.ui_helper as UI


class LoginView(QWidget):
    """Layar 2 — Login ke Sistem (UC02)."""

    login_success = pyqtSignal(object)   # emits Pengguna
    go_register   = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ctrl = PenggunaController()
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"background: {UI.LIGHT_BG};")
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self._build_left_panel(), 4)
        root.addWidget(self._build_right_panel(), 6)

    def _build_left_panel(self) -> QWidget:
        panel = QWidget()
        panel.setStyleSheet(
            f"background: qlineargradient(x1:0,y1:0,x2:1,y2:1,"
            f"stop:0 {UI.BLUE}, stop:1 {UI.BLUE_DARK});"
        )
        layout = QVBoxLayout(panel)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(14)

        icon = QLabel("🏠")
        icon.setStyleSheet("font-size: 64px; background: transparent;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Pinjemin Aja!")
        title.setStyleSheet("font-size: 30px; font-weight: 700; color: white; background: transparent;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sub = QLabel("Platform Berbagi Alat Rumah Tangga\ndalam Komunitas Anda")
        sub.setStyleSheet("font-size: 13px; color: rgba(255,255,255,0.85); background: transparent;")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setWordWrap(True)

        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(sub)
        return panel

    def _build_right_panel(self) -> QWidget:
        panel = QWidget()
        panel.setStyleSheet("background: white;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(80, 0, 80, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        title = QLabel("Log In")
        title.setStyleSheet(f"font-size: 26px; font-weight: 700; color: {UI.TEXT_DARK};")

        sub = QLabel("Masuk ke akun Pinjemin Aja! Anda.")
        sub.setStyleSheet(f"font-size: 13px; color: {UI.TEXT_GRAY};")

        lbl_wa   = QLabel("WhatsApp Number")
        lbl_wa.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {UI.TEXT_MID};")
        self._tf_no_wa = UI.styled_input("Nomor WhatsApp terdaftar")

        lbl_pass = QLabel("Password")
        lbl_pass.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {UI.TEXT_MID};")
        self._tf_pass  = UI.styled_password("Kata sandi")

        self._lbl_error = QLabel()
        self._lbl_error.setStyleSheet(f"color: {UI.RED}; font-size: 12px;")
        self._lbl_error.setWordWrap(True)
        self._lbl_error.hide()

        btn_masuk = UI.primary_button("Log In")
        btn_masuk.setFixedHeight(48)
        btn_masuk.clicked.connect(self._on_masuk)

        link_daftar = QPushButton("Don't have an account? Sign Up")
        link_daftar.setStyleSheet(
            f"background: transparent; color: {UI.BLUE}; border: none;"
            f"font-size: 13px; text-decoration: underline;"
        )
        link_daftar.setCursor(Qt.CursorShape.PointingHandCursor)
        link_daftar.clicked.connect(self.go_register)

        layout.addWidget(title)
        layout.addWidget(sub)
        layout.addSpacing(10)
        layout.addWidget(lbl_wa)
        layout.addWidget(self._tf_no_wa)
        layout.addWidget(lbl_pass)
        layout.addWidget(self._tf_pass)
        layout.addWidget(self._lbl_error)
        layout.addSpacing(6)
        layout.addWidget(btn_masuk)
        layout.addWidget(link_daftar, alignment=Qt.AlignmentFlag.AlignCenter)
        return panel

    # ── Actions ───────────────────────────────────────────────────────────────

    def showFormLogin(self):
        self._tf_no_wa.clear()
        self._tf_pass.clear()
        self._lbl_error.hide()

    def getInputLogin(self) -> dict:
        return {
            "no_wa":      self._tf_no_wa.text().strip(),
            "kata_sandi": self._tf_pass.text(),
        }

    def showPesanError(self, pesan: str):
        self._lbl_error.setText(pesan)
        self._lbl_error.show()

    def _on_masuk(self):
        data = self.getInputLogin()
        if not data["no_wa"] or not data["kata_sandi"]:
            self.showPesanError("Nomor WA dan kata sandi harus diisi.")
            return
        ok = self._ctrl.proses_login(data["no_wa"], data["kata_sandi"])
        if ok:
            pengguna = self._ctrl.ambil_data_profil(
                self._ctrl._pengguna.get_id_pengguna()
            )
            Session.login(pengguna)
            self._lbl_error.hide()
            self.login_success.emit(pengguna)
        else:
            self.showPesanError("Nomor WA atau kata sandi salah.")
