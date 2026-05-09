"""LoginView — UC02 — two-panel layout matching Java design."""
from __future__ import annotations
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QLinearGradient

from controllers.pengguna_controller import PenggunaController
from session import Session
import views.ui_helper as UI


class _LeftPanel(QWidget):
    """Gradient blue branding panel — left side of auth screens."""

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        grad = QLinearGradient(0, 0, self.width(), self.height())
        grad.setColorAt(0.0, QColor("#3D5AF1"))
        grad.setColorAt(1.0, QColor("#6B8EFF"))
        p.fillRect(self.rect(), grad)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(480)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 0, 60, 0)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        lbl_logo = QLabel("🏠")
        lbl_logo.setStyleSheet("font-size: 52px; background: transparent;")

        lbl_name = QLabel("Pinjemin Aja!")
        lbl_name.setStyleSheet(
            "color: white; font-size: 34px; font-weight: 700; background: transparent;"
        )

        lbl_tag = QLabel("Platform Berbagi Alat Komunitas")
        lbl_tag.setStyleSheet(
            "color: rgba(255,255,255,0.85); font-size: 15px; background: transparent;"
        )
        lbl_tag.setWordWrap(True)

        pills_widget = QWidget()
        pills_widget.setStyleSheet("background: transparent;")
        pills_layout = QHBoxLayout(pills_widget)
        pills_layout.setContentsMargins(0, 8, 0, 0)
        pills_layout.setSpacing(8)
        for text in ["🌿 Eco-friendly", "👥 Community", "💰 Savings"]:
            pill = QLabel(text)
            pill.setStyleSheet(
                "background: rgba(255,255,255,0.20); color: white;"
                "border-radius: 20px; padding: 6px 14px; font-size: 12px;"
            )
            pills_layout.addWidget(pill)
        pills_layout.addStretch()

        layout.addWidget(lbl_logo)
        layout.addWidget(lbl_name)
        layout.addWidget(lbl_tag)
        layout.addWidget(pills_widget)


class _FormCard(QWidget):
    """White rounded card for the form — pure QSS, no paintEvent."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(
            "background: white;"
            "border-radius: 20px;"
            f"border: 1px solid {UI.BORDER};"
        )


class LoginView(QWidget):
    """Layar 2 — Login ke Sistem (UC02)."""

    login_success = pyqtSignal(object)
    go_register   = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ctrl = PenggunaController()
        self._setup_ui()

    def _setup_ui(self):
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        outer.addWidget(_LeftPanel())

        # Right: light bg + centered form card
        right = QWidget()
        right.setStyleSheet(f"background: {UI.LIGHT_BG};")
        right_layout = QVBoxLayout(right)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.setContentsMargins(48, 48, 48, 48)

        card = _FormCard()
        card.setFixedWidth(400)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(0)

        # Title
        lbl_title = QLabel("Welcome back 👋")
        lbl_title.setStyleSheet(
            f"font-size: 22px; font-weight: 700; color: {UI.TEXT_DARK}; background: transparent;"
        )
        lbl_sub = QLabel("Masuk ke akun Pinjemin Aja! kamu")
        lbl_sub.setStyleSheet(
            f"font-size: 13px; color: {UI.TEXT_GRAY}; background: transparent;"
        )
        card_layout.addWidget(lbl_title)
        card_layout.addSpacing(4)
        card_layout.addWidget(lbl_sub)
        card_layout.addSpacing(24)

        # WhatsApp
        lbl_wa = QLabel("Nomor WhatsApp")
        lbl_wa.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {UI.TEXT_MID}; background: transparent;")
        self._tf_no_wa = UI.styled_input("Nomor WhatsApp terdaftar")
        card_layout.addWidget(lbl_wa)
        card_layout.addSpacing(6)
        card_layout.addWidget(self._tf_no_wa)
        card_layout.addSpacing(14)

        # Password
        lbl_pw = QLabel("Password")
        lbl_pw.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {UI.TEXT_MID}; background: transparent;")
        self._tf_password = UI.styled_password("Kata sandi")
        card_layout.addWidget(lbl_pw)
        card_layout.addSpacing(6)
        card_layout.addWidget(self._tf_password)
        card_layout.addSpacing(10)

        # Error
        self._lbl_error = QLabel("")
        self._lbl_error.setStyleSheet(f"color: {UI.RED}; font-size: 12px; background: transparent;")
        self._lbl_error.setWordWrap(True)
        self._lbl_error.hide()
        card_layout.addWidget(self._lbl_error)
        card_layout.addSpacing(18)

        # Login button
        btn_masuk = UI.primary_button("Log In")
        btn_masuk.setFixedHeight(46)
        btn_masuk.clicked.connect(self._on_masuk)
        self._tf_no_wa.returnPressed.connect(self._on_masuk)
        self._tf_password.returnPressed.connect(self._on_masuk)
        card_layout.addWidget(btn_masuk)
        card_layout.addSpacing(14)

        # Sign up link
        link_daftar = QPushButton("Don't have an account? Sign Up →")
        link_daftar.setCursor(Qt.CursorShape.PointingHandCursor)
        link_daftar.setStyleSheet(
            "QPushButton {"
            f"  background: transparent; color: {UI.TEXT_GRAY};"
            "  border: none; font-size: 12px;"
            "}"
            f"QPushButton:hover {{ color: {UI.BLUE}; }}"
        )
        link_daftar.clicked.connect(self.go_register)
        card_layout.addWidget(link_daftar, alignment=Qt.AlignmentFlag.AlignCenter)

        right_layout.addWidget(card)
        outer.addWidget(right, 1)

    # ── Public API ────────────────────────────────────────────────────────────

    def showFormLogin(self):
        self._tf_no_wa.clear()
        self._tf_password.clear()
        self._lbl_error.hide()

    def showPesanError(self, pesan: str):
        self._lbl_error.setText(pesan)
        self._lbl_error.show()

    # ── Internal ──────────────────────────────────────────────────────────────

    def _on_masuk(self):
        self._lbl_error.hide()
        no_wa      = self._tf_no_wa.text().strip()
        kata_sandi = self._tf_password.text()
        pengguna   = self._ctrl.login(no_wa, kata_sandi)
        if pengguna:
            Session.login(pengguna)
            self.login_success.emit(pengguna)
        else:
            self.showPesanError("Nomor WA atau kata sandi salah.")
