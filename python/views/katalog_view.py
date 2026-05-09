"""KatalogView — CD-08 / UC09, UC14, UC15, UC16"""
from __future__ import annotations
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QScrollArea, QFrame, QSizePolicy, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap

from controllers.alat_controller import AlatController
from models.alat import Alat
import views.ui_helper as UI

CATEGORIES = ["Semua", "Kitchen", "Tools", "Cleaning", "Electronics", "Gardening"]


class KatalogView(QWidget):
    """Layar 4 — Katalog Alat (UC09, UC14, UC15)."""

    open_detail = pyqtSignal(int)   # emits id_alat

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ctrl = AlatController()
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"background: {UI.LIGHT_BG};")
        root = QVBoxLayout(self)
        root.setContentsMargins(30, 24, 30, 24)
        root.setSpacing(16)

        # Header
        hdr = QHBoxLayout()
        hdr.addWidget(UI.heading("Explore Items"))
        hdr.addStretch()

        self._tf_cari = UI.styled_input("Search products...")
        self._tf_cari.setFixedWidth(240)
        self._tf_cari.returnPressed.connect(self._on_cari)

        self._ddl_kategori = QComboBox()
        self._ddl_kategori.addItems(CATEGORIES)
        self._ddl_kategori.setStyleSheet(
            f"background: white; border: 1.5px solid {UI.BORDER}; border-radius: 8px;"
            f"padding: 8px 12px; font-size: 13px; color: {UI.TEXT_DARK};"
        )
        self._ddl_kategori.setFixedHeight(42)
        self._ddl_kategori.setFixedWidth(160)
        self._ddl_kategori.currentTextChanged.connect(self._on_filter)

        btn_cari = UI.primary_button("Cari")
        btn_cari.setFixedWidth(80)
        btn_cari.clicked.connect(self._on_cari)

        hdr.addWidget(self._ddl_kategori)
        hdr.addWidget(self._tf_cari)
        hdr.addWidget(btn_cari)
        root.addLayout(hdr)

        # Scroll area for cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent; border: none;")

        self._grid_container = QWidget()
        self._grid_container.setStyleSheet("background: transparent;")
        self._grid = QGridLayout(self._grid_container)
        self._grid.setSpacing(16)
        self._grid.setContentsMargins(0, 0, 0, 0)

        self._lbl_kosong = QLabel("Tidak ada alat yang sesuai dengan pencarian atau kategori.")
        self._lbl_kosong.setStyleSheet(f"color: {UI.TEXT_GRAY}; font-size: 14px;")
        self._lbl_kosong.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._lbl_kosong.hide()

        scroll.setWidget(self._grid_container)
        root.addWidget(scroll)
        root.addWidget(self._lbl_kosong)

    # ── Public API ────────────────────────────────────────────────────────────

    def showKatalog(self, daftar_alat: list[Alat] | None = None):
        if daftar_alat is None:
            daftar_alat = self._ctrl.get_semua_alat()
        self._render_grid(daftar_alat)

    def showFormPencarian(self):
        self._tf_cari.setFocus()

    def showFilterKategori(self, kategori: list[str]):
        pass  # dropdown already built

    def showPesanKosong(self):
        self._clear_grid()
        self._lbl_kosong.show()

    def showDetailAlat(self, alat: Alat):
        self.open_detail.emit(alat.get_id_alat())

    # ── Internal ──────────────────────────────────────────────────────────────

    def _on_cari(self):
        kw  = self._tf_cari.text().strip()
        kat = self._ddl_kategori.currentText()
        hasil = self._ctrl.cari_dan_filter(kw, kat)
        if hasil:
            self._render_grid(hasil)
        else:
            self.showPesanKosong()

    def _on_filter(self, kategori: str):
        kw = self._tf_cari.text().strip()
        hasil = self._ctrl.cari_dan_filter(kw, kategori)
        if hasil:
            self._render_grid(hasil)
        else:
            self.showPesanKosong()

    def _clear_grid(self):
        while self._grid.count():
            item = self._grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._lbl_kosong.hide()

    def _render_grid(self, daftar: list[Alat]):
        self._clear_grid()
        self._lbl_kosong.hide()
        cols = 4
        for i, alat in enumerate(daftar):
            card = self._make_card(alat)
            self._grid.addWidget(card, i // cols, i % cols)
        # fill remaining cells so alignment is left
        if daftar:
            rem = cols - (len(daftar) % cols)
            if rem < cols:
                last_row = (len(daftar) - 1) // cols
                for j in range(rem):
                    spacer = QWidget()
                    self._grid.addWidget(spacer, last_row, (len(daftar) % cols) + j)

    def _make_card(self, alat: Alat) -> QWidget:
        card = QWidget()
        card.setFixedWidth(210)
        card.setStyleSheet(
            f"background: white; border-radius: 12px; border: 1px solid {UI.BORDER};"
        )
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Image area
        img_area = QLabel()
        img_area.setFixedHeight(130)
        img_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bg = UI.category_color(alat.get_kategori())
        img_area.setStyleSheet(
            f"background: {bg}; border-radius: 12px 12px 0 0;"
        )
        pm = UI.get_item_pixmap(alat.get_nama_alat(), 210, 130)
        if pm:
            img_area.setPixmap(pm)
            img_area.setScaledContents(True)
        else:
            img_area.setText(UI.category_emoji(alat.get_kategori()))
            img_area.setStyleSheet(img_area.styleSheet() + "font-size: 48px;")

        # Info area
        info = QWidget()
        info.setStyleSheet("background: transparent;")
        info_layout = QVBoxLayout(info)
        info_layout.setContentsMargins(12, 10, 12, 12)
        info_layout.setSpacing(4)

        name_lbl = QLabel(alat.get_nama_alat())
        name_lbl.setStyleSheet(
            f"font-size: 13px; font-weight: 600; color: {UI.TEXT_DARK}; background: transparent;"
        )
        name_lbl.setWordWrap(True)

        cat_lbl = QLabel(alat.get_kategori())
        cat_lbl.setStyleSheet(f"font-size: 11px; color: {UI.TEXT_GRAY}; background: transparent;")

        status_row = QHBoxLayout()
        status_row.setSpacing(6)
        badge_lbl = (UI.available_badge() if alat.get_status_ketersediaan() == "Tersedia"
                     else UI.unavailable_badge())
        price_lbl = QLabel(UI.format_rupiah(alat.get_harga_sewa()) + "/hr")
        price_lbl.setStyleSheet(
            f"font-size: 12px; font-weight: 600; color: {UI.TEXT_DARK}; background: transparent;"
        )
        status_row.addWidget(badge_lbl)
        status_row.addStretch()
        status_row.addWidget(price_lbl)

        info_layout.addWidget(name_lbl)
        info_layout.addWidget(cat_lbl)
        info_layout.addLayout(status_row)

        layout.addWidget(img_area)
        layout.addWidget(info)

        # Click
        id_alat = alat.get_id_alat()
        card.mousePressEvent = lambda _e, aid=id_alat: self.open_detail.emit(aid)
        return card

    def refresh(self):
        self.showKatalog()
