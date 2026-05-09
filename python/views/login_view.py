"""LoginView — CD-05 / UC02 — Modern glassmorphism dark design."""
from __future__ import annotations
import math
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPainter, QPainterPath, QLinearGradient, QColor, QRadialGradient

from controllers.pengguna_controller import PenggunaController
from session import Session
import views.ui_helper as UI


class _AnimatedBg(QWidget):
    """Paints the dark-indigo gradient background with glowing orbs."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._t = 0.0
        timer = QTimer(self)
        timer.timeout.connect(self._tick)
        timer.start(40)

    def _tick(self):
        self._t += 0.012
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        # Base gradient
        grad = QLinearGradient(0, 0, w, h)
        grad.setColorAt(0.0, QColor("#0F0C29"))
        grad.setColorAt(0.5, QColor("#1E1B4B"))
        grad.setColorAt(1.0, QColor("#302B63"))
        p.fillRect(0, 0, w, h, grad)

        # Orb 1 — blue
        cx1 = w * 0.20 + math.sin(self._t * 0.7) * 40
        cy1 = h * 0.25 + math.cos(self._t * 0.5) * 30
        rg1 = QRadialGradient(cx1, cy1, 240)
        rg1.setColorAt(0.0, QColor(61, 90, 241, 55))
        rg1.setColorAt(1.0, QColor(0, 0, 0, 0))
        p.fillRect(0, 0, w, h, rg1)

        # Orb 2 — purple
        cx2 = w * 0.80 + math.cos(self._t * 0.6) * 50
        cy2 = h * 0.70 + math.sin(self._t * 0.8) * 35
        rg2 = QRadialGradient(cx2, cy2, 280)
        rg2.setColorAt(0.0, QColor(99, 102, 241, 50))
        rg2.setColorAt(1.0, QColor(0, 0, 0, 0))
        p.fillRect(0, 0, w, h, rg2)

        # Orb 3 — teal accent
        cx3 = w * 0.60 + math.sin(self._t * 0.4 + 1.2) * 60
        cy3 = h * 0.15 + math.cos(self._t * 0.35) * 25
        rg3 = QRadialGradient(cx3, cy3, 160)
        rg3.setColorAt(0.0, QColor(16, 185, 129, 35))
        rg3.setColorAt(1.0, QColor(0, 0, 0, 0))
        p.fillRect(0, 0, w, h, rg3)


class _GlassCard(QWidget):
    """Semi-transparent frosted-glass card."""

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0.0, 0.0, float(self.width()), float(self.height()), 20, 20)
        p.fillPath(path, QColor(255, 255, 255, 14))
        p.setPen(QColor(255, 255, 255, 35))
        p.drawPath(path)


class LoginView(QWidget):
    """Layar 2 — Login ke Sistem (UC02)."""

    login_success = pyqtSignal(object)
    go_register   = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ctrl = PenggunaController()
        self._setup_ui()

    def _setup_ui(self):
        # Animated background fills entire widget
        self._bg = _AnimatedBg(self)
        self._bg.setGeometry(self.rect())

        # ── Glass card ────────────────────────────────────────────────────────
        card = _GlassCard(self)
        card.setFixedSize(420, 560)
        UI.add_shadow(card, blur=60, color="#000000", opacity=0.45, offset=(0, 20))

        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(40, 40, 40, 40)
        card_lay.setSpacing(0)

        # Logo & brand
        logo = QLabel("🏠")
        logo.setStyleSheet("font-size: 38px; background: transparent;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        brand = QLabel("Pinjemin Aja!")
        brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand.setStyleSheet(
            "color: white; font-size: 22px; font-weight: 700; background: transparent;"
        )
        sub_brand = QLabel("Platform Berbagi Alat Komunitas")
        sub_brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_brand.setStyleSheet(
            "color: rgba(255,255,255,0.60); font-size: 12px; background: transparent;"
        )

        card_lay.addWidget(logo)
        card_lay.addSpacing(4)
        card_lay.addWidget(brand)
        card_lay.addWidget(sub_brand)
        card_lay.addSpacing(30)

        # Divider label
        lbl_login = QLabel("Log In")
        lbl_login.setStyleSheet(
            "color: white; font-size: 18px; font-weight: 700; background: transparent;"
        )
        card_lay.addWidget(lbl_login)
        card_lay.addSpacing(18)

        # Inputs styled for dark background
        _input_ss = (
            "QLineEdit {"
            "  background: rgba(255,255,255,0.10);"
            "  border: 1.5px solid rgba(255,255,255,0.20);"
            "  border-radius: 10px; padding: 0 14px;"
            "  font-size: 13px; color: white;"
            "}"
            "QLineEdit:focus {"
            "  border: 2px solid rgba(99,102,241,0.80);"
            "  background: rgba(255,255,255,0.14);"
            "}"
            "QLineEdit::placeholder { color: rgba(255,255,255,0.40); }"
        )

        lbl_wa = QLabel("WhatsApp Number")
        lbl_wa.setStyleSheet(
            "color: rgba(255,255,255,0.70); font-size: 11px; font-weight: 600;"
            "background: transparent;"
        )
        self._tf_no_wa = UI.styled_input("Nomor WhatsApp terdaftar")
        self._tf_no_wa.setFixedHeight(46)
        self._tf_no_wa.setStyleSheet(_input_ss)

        lbl_pass = QLabel("Password")
        lbl_pass.setStyleSheet(lbl_wa.styleSheet())
        self._tf_pass = UI.styled_password("Kata sandi")
        self._tf_pass.setFixedHeight(46)
        self._tf_pass.setStyleSheet(_input_ss)
        self._tf_pass.returnPressed.connect(self._on_masuk)

        self._lbl_error = QLabel()
        self._lbl_error.setStyleSheet(
            "color: #FCA5A5; font-size: 12px; background: transparent;"
        )
        self._lbl_error.setWordWrap(True)
        self._lbl_error.hide()

        # Login button
        btn_masuk = QPushButton("Log In")
        btn_masuk.setFixedHeight(48)
        btn_masuk.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_masuk.setStyleSheet(
            f"QPushButton {{"
            f"  background: qlineargradient(x1:0,y1:0,x2:1,y2:0,"
            f"  stop:0 {UI.BLUE}, stop:1 {UI.PURPLE});"
            f"  color: white; border: none; border-radius: 10px;"
            f"  font-size: 14px; font-weight: 700;"
            f"}}"
            f"QPushButton:hover {{"
            f"  background: qlineargradient(x1:0,y1:0,x2:1,y2:0,"
            f"  stop:0 {UI.BLUE_DARK}, stop:1 {UI.BLUE});"
            f"}}"
        )
        btn_masuk.clicked.connect(self._on_masuk)

        link_daftar = QPushButton("Don't have an account? Sign Up →")
        link_daftar.setCursor(Qt.CursorShape.PointingHandCursor)
        link_daftar.setStyleSheet(
            "background: transparent; color: rgba(165,180,252,0.90); border: none;"
            "font-size: 12px; font-weight: 500;"
            "QPushButton:hover { color: white; }"
        )
        link_daftar.clicked.connect(self.go_register)

        card_lay.addWidget(lbl_wa)
        card_lay.addSpacing(5)
        card_lay.addWidget(self._tf_no_wa)
        card_lay.addSpacing(14)
        card_lay.addWidget(lbl_pass)
        card_lay.addSpacing(5)
        card_lay.addWidget(self._tf_pass)
        card_lay.addSpacing(8)
        card_lay.addWidget(self._lbl_error)
        card_lay.addSpacing(14)
        card_lay.addWidget(btn_masuk)
        card_lay.addSpacing(14)
        card_lay.addWidget(link_daftar, alignment=Qt.AlignmentFlag.AlignCenter)

        self._card = card

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._bg.setGeometry(self.rect())
        # Center card
        cx = (self.width()  - self._card.width())  // 2
        cy = (self.height() - self._card.height()) // 2
        self._card.move(cx, cy)

    # ── Public API ─────────────────────────────────────────────────────────────

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

    # ── Internal ──────────────────────────────────────────────────────────────

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
