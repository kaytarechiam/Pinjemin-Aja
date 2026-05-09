"""WalletView — CD-07 / UC06, UC07, UC08"""
from __future__ import annotations
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal

from controllers.pengguna_controller import PenggunaController
from session import Session
import views.ui_helper as UI


class WalletView(QWidget):
    """Layar 7 — Dompet Digital (UC06, UC07, UC08)."""

    go_profil        = pyqtSignal()
    logout_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ctrl = PenggunaController()
        self._mode = "topup"
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"background: {UI.LIGHT_BG};")
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── Left sidebar ──────────────────────────────────────────────────────
        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet(
            f"background: white; border-right: 1px solid {UI.BORDER};"
        )
        sb = QVBoxLayout(sidebar)
        sb.setContentsMargins(16, 28, 16, 28)
        sb.setSpacing(4)
        sb.setAlignment(Qt.AlignmentFlag.AlignTop)

        lbl_section = QLabel("Account")
        lbl_section.setStyleSheet(
            f"font-size: 11px; font-weight: 700; color: {UI.TEXT_GRAY};"
            f"letter-spacing: 1px; background: transparent; padding: 0 12px;"
        )
        sb.addWidget(lbl_section)
        sb.addSpacing(8)

        btn_wallet = self._sidebar_btn("💳  My Wallet", active=True)
        btn_profil = self._sidebar_btn("👤  Profile",   active=False)
        sb.addWidget(btn_wallet)
        sb.addWidget(btn_profil)
        btn_profil.clicked.connect(self.go_profil)

        sb.addSpacing(8)
        sb.addWidget(UI.separator())
        sb.addSpacing(8)

        btn_logout = QPushButton("⏻  Logout")
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.setFixedHeight(38)
        btn_logout.setStyleSheet(
            f"QPushButton {{ background: transparent; color: {UI.RED};"
            f"  border: none; border-radius: 8px;"
            f"  font-size: 13px; padding: 0 12px; text-align: left; }}"
            f"QPushButton:hover {{ background: {UI.RED_LIGHT}; }}"
        )
        btn_logout.clicked.connect(self.logout_requested)
        sb.addWidget(btn_logout)
        sb.addStretch()
        outer.addWidget(sidebar)

        # ── Right scrollable content ──────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(f"background: {UI.LIGHT_BG}; border: none;")

        content = QWidget()
        content.setStyleSheet(f"background: {UI.LIGHT_BG};")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(36, 30, 36, 36)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(UI.heading("My Wallet"))

        # Balance card
        balance_card = QWidget()
        balance_card.setStyleSheet(
            f"background: qlineargradient(x1:0,y1:0,x2:1,y2:1,"
            f"stop:0 {UI.BLUE}, stop:1 {UI.BLUE_DARK});"
            f"border-radius: 16px;"
        )
        balance_card.setMaximumWidth(560)
        balance_card.setFixedHeight(160)
        bc = QVBoxLayout(balance_card)
        bc.setContentsMargins(32, 28, 32, 28)
        bc.setSpacing(8)

        lbl_title = QLabel("Saldo Tersedia")
        lbl_title.setStyleSheet(
            "color: rgba(255,255,255,0.85); font-size: 13px; background: transparent;"
        )
        self._lbl_saldo = QLabel("Rp 0")
        self._lbl_saldo.setStyleSheet(
            "color: white; font-size: 32px; font-weight: 700; background: transparent;"
        )
        lbl_id = QLabel()
        lbl_id.setStyleSheet(
            "color: rgba(255,255,255,0.65); font-size: 12px; background: transparent;"
        )
        user = Session.get_current_user()
        if user:
            lbl_id.setText(f"ID: {user.get_no_wa()}")
        bc.addWidget(lbl_title)
        bc.addWidget(self._lbl_saldo)
        bc.addStretch()
        bc.addWidget(lbl_id)
        layout.addWidget(balance_card)

        # Action buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)
        btn_topup = UI.primary_button("⬆  Top Up")
        btn_topup.setFixedWidth(140)
        btn_topup.clicked.connect(self._on_topup)
        btn_tarik = UI.outline_button("⬇  Tarik Dana")
        btn_tarik.setFixedWidth(140)
        btn_tarik.clicked.connect(self._on_tarik)
        btn_row.addWidget(btn_topup)
        btn_row.addWidget(btn_tarik)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        # Form card
        form_card = UI.ShadowCard(14)
        form_card.setMaximumWidth(560)
        fc = QVBoxLayout(form_card)
        fc.setContentsMargins(28, 28, 28, 28)
        fc.setSpacing(14)

        self._lbl_form_title = QLabel("Top Up Saldo")
        self._lbl_form_title.setStyleSheet(
            f"font-size: 16px; font-weight: 700; color: {UI.TEXT_DARK};"
        )

        lbl_nominal = QLabel("Nominal (Rp)")
        lbl_nominal.setStyleSheet(
            f"font-size: 12px; font-weight: 600; color: {UI.TEXT_MID};"
        )
        self._tf_nominal = UI.styled_input("Masukkan nominal...")
        self._tf_nominal.setFixedHeight(46)

        quick_row = QHBoxLayout()
        quick_row.setSpacing(8)
        for amount in [50_000, 100_000, 200_000, 500_000]:
            btn = QPushButton(UI.format_rupiah(amount))
            btn.setStyleSheet(
                f"QPushButton {{ background: {UI.BLUE_LIGHT}; color: {UI.BLUE}; border: none;"
                f"  border-radius: 6px; padding: 6px 10px; font-size: 12px; font-weight: 600; }}"
                f"QPushButton:hover {{ background: #DDE3FD; }}"
            )
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, a=amount: self._tf_nominal.setText(str(a)))
            quick_row.addWidget(btn)
        quick_row.addStretch()

        self._btn_submit = UI.primary_button("Konfirmasi Top Up")
        self._btn_submit.setFixedWidth(210)
        self._btn_submit.clicked.connect(self._on_submit)

        fc.addWidget(self._lbl_form_title)
        fc.addWidget(lbl_nominal)
        fc.addWidget(self._tf_nominal)
        fc.addLayout(quick_row)
        fc.addWidget(self._btn_submit)
        layout.addWidget(form_card)

        scroll.setWidget(content)
        outer.addWidget(scroll, 1)

        self._refresh_saldo()

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _sidebar_btn(self, text: str, active: bool) -> QPushButton:
        btn = QPushButton(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedHeight(38)
        if active:
            btn.setStyleSheet(
                f"QPushButton {{ background: {UI.BLUE_LIGHT}; color: {UI.BLUE};"
                f"  border: none; border-radius: 8px;"
                f"  font-size: 13px; font-weight: 600; padding: 0 12px; text-align: left; }}"
            )
        else:
            btn.setStyleSheet(
                f"QPushButton {{ background: transparent; color: {UI.TEXT_MID};"
                f"  border: none; border-radius: 8px;"
                f"  font-size: 13px; padding: 0 12px; text-align: left; }}"
                f"QPushButton:hover {{ background: {UI.BLUE_LIGHT}; color: {UI.BLUE}; }}"
            )
        return btn

    # ── Public API ────────────────────────────────────────────────────────────

    def showSaldo(self, saldo: float | None = None):
        if saldo is None:
            self._refresh_saldo()
        else:
            self._lbl_saldo.setText(UI.format_rupiah(saldo))

    def showFormIsiUlang(self):
        self._mode = "topup"
        self._lbl_form_title.setText("Top Up Saldo")
        self._btn_submit.setText("Konfirmasi Top Up")
        self._tf_nominal.clear()

    def showFormTarikDana(self):
        self._mode = "tarik"
        self._lbl_form_title.setText("Tarik Dana")
        self._btn_submit.setText("Konfirmasi Penarikan")
        self._tf_nominal.clear()

    def showPesanSukses(self, pesan: str):
        UI.show_toast(pesan, self, "success")

    def showPesanError(self, pesan: str):
        UI.show_toast(pesan, self, "error")

    # ── Internal ──────────────────────────────────────────────────────────────

    def _refresh_saldo(self):
        user = Session.get_current_user()
        if user:
            saldo = self._ctrl.lihat_saldo(user.get_id_pengguna())
            self._lbl_saldo.setText(UI.format_rupiah(saldo))

    def _on_topup(self):
        self.showFormIsiUlang()

    def _on_tarik(self):
        self.showFormTarikDana()

    def _on_submit(self):
        user = Session.get_current_user()
        if user is None:
            return
        raw = self._tf_nominal.text().strip()
        try:
            nominal = float(raw)
        except ValueError:
            self.showPesanError("Nominal harus berupa angka.")
            return
        if nominal <= 0:
            self.showPesanError("Nominal harus lebih dari 0.")
            return

        if self._mode == "topup":
            ok = self._ctrl.proses_isi_ulang(user.get_id_pengguna(), nominal)
            if ok:
                self._refresh_saldo()
                self._tf_nominal.clear()
                self.showPesanSukses(f"Top up {UI.format_rupiah(nominal)} berhasil.")
            else:
                self.showPesanError("Gagal melakukan top up.")
        else:
            ok = self._ctrl.proses_tarik_dana(user.get_id_pengguna(), nominal)
            if ok:
                self._refresh_saldo()
                self._tf_nominal.clear()
                self.showPesanSukses(f"Penarikan {UI.format_rupiah(nominal)} berhasil.")
            else:
                self.showPesanError("Saldo tidak mencukupi untuk penarikan.")
