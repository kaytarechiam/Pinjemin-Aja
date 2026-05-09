"""ProfilView — CD-06 / UC03, UC04, UC05"""
from __future__ import annotations
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QStackedWidget
)
from PyQt6.QtCore import Qt

from controllers.pengguna_controller import PenggunaController
from session import Session
import views.ui_helper as UI


class ProfilView(QScrollArea):
    """Layar 6 — Profil Pengguna (UC03, UC04, UC05)."""

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

        layout.addWidget(UI.heading("My Account"))

        # Profile card — use ShadowCard
        card = UI.ShadowCard(14)
        card.setMaximumWidth(600)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 28, 28, 28)
        card_layout.setSpacing(16)

        card_layout.addWidget(UI.subheading("Profil"))

        # Avatar
        user = Session.get_current_user()
        initials = (user.get_nama_lengkap()[:2].upper() if user else "?")
        avatar = QLabel(initials)
        avatar.setFixedSize(70, 70)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            f"background: {UI.BLUE_LIGHT}; color: {UI.BLUE}; border-radius: 35px;"
            f"font-size: 22px; font-weight: 700;"
        )
        card_layout.addWidget(avatar)

        # Fields
        self._tf_nama  = UI.styled_input("Nama lengkap")
        self._tf_no_wa = UI.styled_input("Nomor WhatsApp")
        self._tf_alamat = UI.styled_textarea("Alamat")
        self._tf_alamat.setFixedHeight(70)

        if user:
            self._tf_nama.setText(user.get_nama_lengkap())
            self._tf_no_wa.setText(user.get_no_wa())
            self._tf_alamat.setPlainText(user.get_alamat())

        for lbl_text, widget in [
            ("Full Name", self._tf_nama),
            ("WhatsApp Number", self._tf_no_wa),
            ("Address", self._tf_alamat),
        ]:
            lbl = QLabel(lbl_text)
            lbl.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {UI.TEXT_MID};")
            card_layout.addWidget(lbl)
            card_layout.addWidget(widget)

        card_layout.addWidget(UI.separator())

        # Password section
        lbl_pass = QLabel("Ganti Password")
        lbl_pass.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {UI.TEXT_DARK};")
        card_layout.addWidget(lbl_pass)

        self._tf_sandi_lama  = UI.styled_password("Kata sandi saat ini")
        self._tf_sandi_baru  = UI.styled_password("Kata sandi baru")
        self._tf_konfirmasi  = UI.styled_password("Konfirmasi kata sandi baru")

        for lbl_text, widget in [
            ("Current Password (kosongkan jika tidak ingin ganti)", self._tf_sandi_lama),
            ("New Password", self._tf_sandi_baru),
            ("Confirm New Password", self._tf_konfirmasi),
        ]:
            lbl = QLabel(lbl_text)
            lbl.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {UI.TEXT_MID};")
            card_layout.addWidget(lbl)
            card_layout.addWidget(widget)

        btn_simpan = UI.primary_button("💾  Save Changes")
        btn_simpan.setFixedWidth(200)
        btn_simpan.clicked.connect(self._on_simpan)

        card_layout.addWidget(btn_simpan)

        layout.addWidget(card)
        self.setWidget(root)

    # ── Actions ───────────────────────────────────────────────────────────────

    def showProfil(self, pengguna=None):
        if pengguna is None:
            pengguna = Session.get_current_user()
        if pengguna:
            self._tf_nama.setText(pengguna.get_nama_lengkap())
            self._tf_no_wa.setText(pengguna.get_no_wa())
            self._tf_alamat.setPlainText(pengguna.get_alamat())

    def showFormEditProfil(self, pengguna=None):
        self.showProfil(pengguna)

    def showFormUbahKataSandi(self):
        self._tf_sandi_lama.clear()
        self._tf_sandi_baru.clear()
        self._tf_konfirmasi.clear()

    def showPesanSukses(self, pesan: str):
        UI.show_toast(pesan, self, "success")

    def showPesanError(self, pesan: str):
        UI.show_toast(pesan, self, "error")

    def _on_simpan(self):
        user = Session.get_current_user()
        if user is None:
            return
        nama   = self._tf_nama.text().strip()
        no_wa  = self._tf_no_wa.text().strip()
        alamat = self._tf_alamat.toPlainText().strip()

        if not nama or not no_wa or not alamat:
            self.showPesanError("Nama, WhatsApp, dan alamat tidak boleh kosong.")
            return

        # UC04 update profil
        self._ctrl.update_profil(user.get_id_pengguna(), {
            "nama_lengkap": nama, "no_wa": no_wa, "alamat": alamat
        })

        # UC05 ubah kata sandi (jika diisi)
        sandi_lama = self._tf_sandi_lama.text()
        sandi_baru = self._tf_sandi_baru.text()
        konfirmasi = self._tf_konfirmasi.text()
        if sandi_lama or sandi_baru:
            if not sandi_lama or not sandi_baru:
                self.showPesanError("Isi password lama dan baru untuk mengganti password.")
                return
            if sandi_baru != konfirmasi:
                self.showPesanError("Password baru dan konfirmasi tidak cocok.")
                return
            ok = self._ctrl.ubah_kata_sandi(user.get_id_pengguna(), sandi_lama, sandi_baru)
            if not ok:
                self.showPesanError("Password lama salah.")
                return

        # Refresh session
        updated = self._ctrl.ambil_data_profil(user.get_id_pengguna())
        if updated:
            Session.login(updated)
        self.showPesanSukses("Profil berhasil diperbarui.")
        self._tf_sandi_lama.clear()
        self._tf_sandi_baru.clear()
        self._tf_konfirmasi.clear()
