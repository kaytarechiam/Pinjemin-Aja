"""WalletView — CD-07 / UC06, UC07, UC08"""
from __future__ import annotations
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt

from controllers.pengguna_controller import PenggunaController
from session import Session
import views.ui_helper as UI


class WalletView(QScrollArea):
    """Layar 7 — Dompet Digital (UC06, UC07, UC08)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ctrl = PenggunaController()
        self._setup_ui()

    def _setup_ui(self):
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet(f"background: {UI.LIGHT_BG}; border: none;")

        root = QWidget()
        root.setStyleSheet(f"background: {UI.LIGHT_BG};")
        layout = QVBoxLayout(root)
        layout.setContentsMargins(40, 30, 40, 40)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(UI.heading("Dompet Digital"))

        # Balance card
        balance_card = QWidget()
        balance_card.setStyleSheet(
            f"background: qlineargradient(x1:0,y1:0,x2:1,y2:1,"
            f"stop:0 {UI.BLUE}, stop:1 {UI.BLUE_DARK});"
            f"border-radius: 16px;"
        )
        balance_card.setMaximumWidth(600)
        balance_card.setFixedHeight(160)
        bc_layout = QVBoxLayout(balance_card)
        bc_layout.setContentsMargins(32, 28, 32, 28)
        bc_layout.setSpacing(8)

        lbl_title = QLabel("Saldo Tersedia")
        lbl_title.setStyleSheet("color: rgba(255,255,255,0.85); font-size: 13px; background: transparent;")

        self._lbl_saldo = QLabel("Rp 0")
        self._lbl_saldo.setStyleSheet(
            "color: white; font-size: 32px; font-weight: 700; background: transparent;"
        )

        lbl_id = QLabel()
        lbl_id.setStyleSheet("color: rgba(255,255,255,0.65); font-size: 12px; background: transparent;")
        user = Session.get_current_user()
        if user:
            lbl_id.setText(f"ID: {user.get_no_wa()}")

        bc_layout.addWidget(lbl_title)
        bc_layout.addWidget(self._lbl_saldo)
        bc_layout.addStretch()
        bc_layout.addWidget(lbl_id)

        layout.addWidget(balance_card)

        # Action buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        btn_topup = UI.primary_button("⬆  Top Up")
        btn_topup.setFixedWidth(150)
        btn_topup.clicked.connect(self._on_topup)

        btn_tarik = UI.outline_button("⬇  Tarik Dana")
        btn_tarik.setFixedWidth(150)
        btn_tarik.clicked.connect(self._on_tarik)

        btn_row.addWidget(btn_topup)
        btn_row.addWidget(btn_tarik)
        btn_row.addStretch()

        layout.addLayout(btn_row)

        # Top-up / withdraw form card
        form_card = QWidget()
        form_card.setStyleSheet(f"background: white; border-radius: 14px; border: 1px solid {UI.BORDER};")
        form_card.setMaximumWidth(600)
        fc_layout = QVBoxLayout(form_card)
        fc_layout.setContentsMargins(28, 28, 28, 28)
        fc_layout.setSpacing(14)

        self._lbl_form_title = QLabel("Top Up Saldo")
        self._lbl_form_title.setStyleSheet(
            f"font-size: 16px; font-weight: 700; color: {UI.TEXT_DARK};"
        )

        lbl_nominal = QLabel("Nominal (Rp)")
        lbl_nominal.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {UI.TEXT_MID};")

        self._tf_nominal = UI.styled_input("Masukkan nominal...")
        self._tf_nominal.setFixedHeight(46)

        # Quick-amount buttons
        quick_row = QHBoxLayout()
        quick_row.setSpacing(8)
        for amount in [50_000, 100_000, 200_000, 500_000]:
            btn = QPushButton(UI.format_rupiah(amount))
            btn.setStyleSheet(
                f"background: {UI.BLUE_LIGHT}; color: {UI.BLUE}; border: none;"
                f"border-radius: 6px; padding: 6px 10px; font-size: 12px; font-weight: 600;"
            )
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, a=amount: self._tf_nominal.setText(str(a)))
            quick_row.addWidget(btn)
        quick_row.addStretch()

        self._lbl_feedback = QLabel()
        self._lbl_feedback.setWordWrap(True)
        self._lbl_feedback.setStyleSheet(f"color: {UI.RED}; font-size: 12px;")
        self._lbl_feedback.hide()

        self._btn_submit = UI.primary_button("Konfirmasi Top Up")
        self._btn_submit.setFixedWidth(200)
        self._btn_submit.clicked.connect(self._on_submit)

        fc_layout.addWidget(self._lbl_form_title)
        fc_layout.addWidget(lbl_nominal)
        fc_layout.addWidget(self._tf_nominal)
        fc_layout.addLayout(quick_row)
        fc_layout.addWidget(self._lbl_feedback)
        fc_layout.addWidget(self._btn_submit)

        layout.addWidget(form_card)
        self.setWidget(root)

        self._mode = "topup"  # or "tarik"
        self._refresh_saldo()

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
        self._lbl_feedback.hide()

    def showFormTarikDana(self):
        self._mode = "tarik"
        self._lbl_form_title.setText("Tarik Dana")
        self._btn_submit.setText("Konfirmasi Penarikan")
        self._tf_nominal.clear()
        self._lbl_feedback.hide()

    def showPesanSukses(self, pesan: str):
        self._lbl_feedback.setStyleSheet(f"color: {UI.GREEN}; font-size: 12px;")
        self._lbl_feedback.setText(pesan)
        self._lbl_feedback.show()

    def showPesanError(self, pesan: str):
        self._lbl_feedback.setStyleSheet(f"color: {UI.RED}; font-size: 12px;")
        self._lbl_feedback.setText(pesan)
        self._lbl_feedback.show()

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
