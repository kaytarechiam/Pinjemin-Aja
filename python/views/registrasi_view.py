"""RegistrasiView — CD-01 / UC01 — Glassmorphism dark design."""
from __future__ import annotations
import math
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QPainter, QPainterPath, QLinearGradient, QColor, QRadialGradient

from controllers.pengguna_controller import PenggunaController
import views.ui_helper as UI


class _AnimatedBg(QWidget):
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
        grad = QLinearGradient(0, 0, w, h)
        grad.setColorAt(0.0, QColor("#0F0C29"))
        grad.setColorAt(0.5, QColor("#1E1B4B"))
        grad.setColorAt(1.0, QColor("#24243e"))
        p.fillRect(0, 0, w, h, grad)
        for cx_f, cy_f, r, col, phase in [
            (0.15, 0.30, 220, QColor(61, 90, 241, 48), 0.0),
            (0.85, 0.65, 260, QColor(99, 102, 241, 44), 1.5),
            (0.55, 0.85, 150, QColor(16, 185, 129, 30), 0.8),
        ]:
            cx = w * cx_f + math.sin(self._t * 0.6 + phase) * 40
            cy = h * cy_f + math.cos(self._t * 0.5 + phase) * 30
            rg = QRadialGradient(cx, cy, r)
            rg.setColorAt(0.0, col)
            rg.setColorAt(1.0, QColor(0, 0, 0, 0))
            p.fillRect(0, 0, w, h, rg)


class _GlassCard(QWidget):
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0.0, 0.0, float(self.width()), float(self.height()), 20, 20)
        p.fillPath(path, QColor(255, 255, 255, 14))
        p.setPen(QColor(255, 255, 255, 35))
        p.drawPath(path)


class RegistrasiView(QWidget):
    """Layar 1 — Registrasi Akun Baru (UC01)."""

    go_login = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ctrl = PenggunaController()
        self._setup_ui()

    def _setup_ui(self):
        self._bg = _AnimatedBg(self)
        self._bg.setGeometry(self.rect())

        self._card = _GlassCard(self)
        self._card.setFixedSize(460, 610)
        UI.add_shadow(self._card, blur=60, color="#000000", opacity=0.45, offset=(0, 20))

        scroll = QScrollArea(self._card)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent; border: none;")
        scroll.setGeometry(0, 0, self._card.width(), self._card.height())

        inner = QWidget()
        inner.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(inner)
        lay.setContentsMargins(40, 40, 40, 40)
        lay.setSpacing(0)

        logo = QLabel("🏠")
        logo.setStyleSheet("font-size: 32px; background: transparent;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title = QLabel("Buat Akun Baru")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "color: white; font-size: 20px; font-weight: 700; background: transparent;"
        )
        lay.addWidget(logo)
        lay.addSpacing(4)
        lay.addWidget(title)
        lay.addSpacing(24)

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
        _ta_ss = (
            "QTextEdit {"
            "  background: rgba(255,255,255,0.10);"
            "  border: 1.5px solid rgba(255,255,255,0.20);"
            "  border-radius: 10px; padding: 10px 14px;"
            "  font-size: 13px; color: white;"
            "}"
            "QTextEdit:focus { border: 2px solid rgba(99,102,241,0.80); }"
        )
        _lbl_ss = (
            "color: rgba(255,255,255,0.70); font-size: 11px; font-weight: 600;"
            "background: transparent;"
        )

        self._tf_nama    = UI.styled_input("Nama lengkap Anda")
        self._tf_no_wa   = UI.styled_input("08xxxxxxxxxx")
        self._tf_alamat  = UI.styled_textarea("Alamat lengkap")
        self._tf_sandi   = UI.styled_password("Minimal 6 karakter")
        self._tf_konfirm = UI.styled_password("Ulangi kata sandi")

        for w in [self._tf_nama, self._tf_no_wa, self._tf_sandi, self._tf_konfirm]:
            w.setFixedHeight(44)
            w.setStyleSheet(_input_ss)
        self._tf_alamat.setFixedHeight(72)
        self._tf_alamat.setStyleSheet(_ta_ss)

        for lbl_text, widget in [
            ("Full Name", self._tf_nama),
            ("WhatsApp Number", self._tf_no_wa),
            ("Address", self._tf_alamat),
            ("Password", self._tf_sandi),
            ("Confirm Password", self._tf_konfirm),
        ]:
            lbl = QLabel(lbl_text)
            lbl.setStyleSheet(_lbl_ss)
            lay.addWidget(lbl)
            lay.addSpacing(5)
            lay.addWidget(widget)
            lay.addSpacing(12)

        self._lbl_feedback = QLabel()
        self._lbl_feedback.setStyleSheet(
            "color: #FCA5A5; font-size: 12px; background: transparent;"
        )
        self._lbl_feedback.setWordWrap(True)
        self._lbl_feedback.hide()

        btn_daftar = QPushButton("Buat Akun  →")
        btn_daftar.setFixedHeight(48)
        btn_daftar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_daftar.setStyleSheet(
            "QPushButton {"
            f"  background: qlineargradient(x1:0,y1:0,x2:1,y2:0,"
            f"  stop:0 {UI.BLUE}, stop:1 {UI.PURPLE});"
            "  color: white; border: none; border-radius: 10px;"
            "  font-size: 14px; font-weight: 700;"
            "}"
            "QPushButton:hover {"
            f"  background: qlineargradient(x1:0,y1:0,x2:1,y2:0,"
            f"  stop:0 {UI.BLUE_DARK}, stop:1 {UI.BLUE});"
            "}"
        )
        btn_daftar.clicked.connect(self._on_daftar)

        link = QPushButton("Sudah punya akun? Log In  →")
        link.setCursor(Qt.CursorShape.PointingHandCursor)
        link.setStyleSheet(
            "background: transparent; color: rgba(165,180,252,0.90); border: none;"
            "font-size: 12px; font-weight: 500;"
        )
        link.clicked.connect(self.go_login)

        lay.addWidget(self._lbl_feedback)
        lay.addSpacing(6)
        lay.addWidget(btn_daftar)
        lay.addSpacing(12)
        lay.addWidget(link, alignment=Qt.AlignmentFlag.AlignCenter)
        lay.addSpacing(20)
        scroll.setWidget(inner)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._bg.setGeometry(self.rect())
        cx = (self.width()  - self._card.width())  // 2
        cy = (self.height() - self._card.height()) // 2
        self._card.move(cx, cy)

    # ── Public API ─────────────────────────────────────────────────────────────

    def showFormRegistrasi(self):
        for w in [self._tf_nama, self._tf_no_wa, self._tf_sandi, self._tf_konfirm]:
            w.clear()
        self._tf_alamat.clear()
        self._lbl_feedback.hide()

    def getInputData(self) -> dict:
        return {
            "nama_lengkap":     self._tf_nama.text().strip(),
            "no_wa":            self._tf_no_wa.text().strip(),
            "alamat":           self._tf_alamat.toPlainText().strip(),
            "kata_sandi":       self._tf_sandi.text(),
            "konfirmasi_sandi": self._tf_konfirm.text(),
        }

    def showPesanError(self, pesan: str):
        self._lbl_feedback.setStyleSheet(
            "color: #FCA5A5; font-size: 12px; background: transparent;"
        )
        self._lbl_feedback.setText(pesan)
        self._lbl_feedback.show()

    def showPesanSukses(self, pesan: str):
        self._lbl_feedback.setStyleSheet(
            "color: #6EE7B7; font-size: 12px; background: transparent;"
        )
        self._lbl_feedback.setText(pesan)
        self._lbl_feedback.show()

    def _on_daftar(self):
        data = self.getInputData()
        if not all([data["nama_lengkap"], data["no_wa"], data["alamat"],
                    data["kata_sandi"], data["konfirmasi_sandi"]]):
            self.showPesanError("Semua field harus diisi.")
            return
        if data["kata_sandi"] != data["konfirmasi_sandi"]:
            self.showPesanError("Kata sandi dan konfirmasi tidak cocok.")
            return
        ok = self._ctrl.proses_registrasi(data)
        if ok:
            self.showPesanSukses("Akun berhasil dibuat! Silakan login.")
            QTimer.singleShot(1500, self.go_login.emit)
        else:
            self.showPesanError("Nomor WhatsApp sudah terdaftar.")
