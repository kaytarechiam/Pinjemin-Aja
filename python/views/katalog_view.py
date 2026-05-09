"""KatalogView — CD-08 / UC09, UC14, UC15, UC16 — animated card grid."""
from __future__ import annotations
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QScrollArea, QGridLayout,
    QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QPixmap, QPainter, QPainterPath

from controllers.alat_controller import AlatController
from models.alat import Alat
import views.ui_helper as UI

CATEGORIES = ["Semua", "Kitchen", "Tools", "Cleaning", "Electronics", "Gardening"]


class _HoverCard(QWidget):
    """Item card with smooth shadow-elevation on hover."""

    clicked = pyqtSignal(int)

    def __init__(self, alat: Alat, parent=None):
        super().__init__(parent)
        self._id = alat.get_id_alat()
        self.setFixedSize(210, 220)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        # Shadow effect — animatable
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(12)
        self._shadow.setOffset(0, 3)
        self._shadow.setColor(QColor(0, 0, 0, 28))
        self.setGraphicsEffect(self._shadow)

        self._setup_content(alat)

    def _setup_content(self, alat: Alat):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # Image area
        img = QLabel()
        img.setFixedHeight(132)
        img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bg = UI.category_color(alat.get_kategori())
        img.setStyleSheet(
            f"background: {bg}; border-radius: 14px 14px 0 0;"
        )
        pm = UI.get_item_pixmap(alat.get_nama_alat(), 210, 132)
        if pm:
            img.setPixmap(pm)
            img.setScaledContents(True)
        else:
            img.setText(UI.category_emoji(alat.get_kategori()))
            img.setStyleSheet(img.styleSheet() + "font-size: 46px;")

        # Info area
        info = QWidget()
        info.setStyleSheet(
            f"background: white; border-radius: 0 0 14px 14px;"
        )
        info_l = QVBoxLayout(info)
        info_l.setContentsMargins(12, 8, 12, 10)
        info_l.setSpacing(3)

        name_lbl = QLabel(alat.get_nama_alat())
        name_lbl.setStyleSheet(
            f"font-size: 12px; font-weight: 600; color: {UI.TEXT_DARK};"
            "background: transparent;"
        )
        name_lbl.setWordWrap(True)

        cat_lbl = QLabel(alat.get_kategori())
        cat_lbl.setStyleSheet(
            f"font-size: 10px; color: {UI.TEXT_GRAY}; background: transparent;"
        )

        row = QHBoxLayout()
        row.setSpacing(6)
        badge = (UI.available_badge() if alat.get_status_ketersediaan() == "Tersedia"
                 else UI.unavailable_badge())
        price = QLabel(UI.format_rupiah(alat.get_harga_sewa()) + "/hr")
        price.setStyleSheet(
            f"font-size: 11px; font-weight: 600; color: {UI.BLUE}; background: transparent;"
        )
        row.addWidget(badge)
        row.addStretch()
        row.addWidget(price)

        info_l.addWidget(name_lbl)
        info_l.addWidget(cat_lbl)
        info_l.addLayout(row)

        lay.addWidget(img)
        lay.addWidget(info)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0.0, 0.0, float(self.width()), float(self.height()), 14, 14)
        p.fillPath(path, QColor("white"))

    def enterEvent(self, event):
        self._animate_shadow(28, 0.14, 8)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animate_shadow(12, 0.07, 3)
        super().leaveEvent(event)

    def _animate_shadow(self, blur: int, opacity: float, offset: int):
        c = QColor(0, 0, 0)
        c.setAlphaF(opacity)
        self._shadow.setBlurRadius(blur)
        self._shadow.setColor(c)
        self._shadow.setOffset(0, offset)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._id)


class KatalogView(QWidget):
    """Layar 4 — Katalog Alat (UC09, UC14, UC15)."""

    open_detail = pyqtSignal(int)

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
        lbl_h = UI.heading("Explore Items")
        hdr.addWidget(lbl_h)
        hdr.addStretch()

        # Search + filter
        self._tf_cari = UI.styled_input("Search products...")
        self._tf_cari.setFixedWidth(240)
        self._tf_cari.returnPressed.connect(self._on_cari)

        self._ddl_kategori = QComboBox()
        self._ddl_kategori.addItems(CATEGORIES)
        self._ddl_kategori.setStyleSheet(
            f"QComboBox {{"
            f"  background: white; border: 1.5px solid {UI.BORDER}; border-radius: 10px;"
            f"  padding: 0 14px; font-size: 13px; color: {UI.TEXT_DARK};"
            f"  min-height: 44px;"
            f"}}"
            f"QComboBox::drop-down {{ border: none; }}"
            f"QComboBox QAbstractItemView {{ border-radius: 8px; }}"
        )
        self._ddl_kategori.setFixedHeight(44)
        self._ddl_kategori.setFixedWidth(160)
        self._ddl_kategori.currentTextChanged.connect(self._on_filter)

        btn_cari = UI.primary_button("Cari")
        btn_cari.setFixedWidth(90)
        btn_cari.clicked.connect(self._on_cari)

        hdr.addWidget(self._ddl_kategori)
        hdr.addWidget(self._tf_cari)
        hdr.addWidget(btn_cari)
        root.addLayout(hdr)

        # Smooth scroll grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
            "QScrollBar:vertical { width: 6px; background: transparent; }"
            "QScrollBar::handle:vertical { background: #CBD5E1; border-radius: 3px; }"
        )

        self._grid_container = QWidget()
        self._grid_container.setStyleSheet("background: transparent;")
        self._grid = QGridLayout(self._grid_container)
        self._grid.setSpacing(18)
        self._grid.setContentsMargins(4, 4, 4, 4)

        self._lbl_kosong = QLabel("Tidak ada alat yang sesuai dengan pencarian.")
        self._lbl_kosong.setStyleSheet(
            f"color: {UI.TEXT_GRAY}; font-size: 14px; background: transparent;"
        )
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
        pass

    def showPesanKosong(self):
        self._clear_grid()
        self._lbl_kosong.show()

    def showDetailAlat(self, alat: Alat):
        self.open_detail.emit(alat.get_id_alat())

    def refresh(self):
        self.showKatalog()

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
        cols = 4
        for i, alat in enumerate(daftar):
            card = _HoverCard(alat)
            card.clicked.connect(self.open_detail)
            self._grid.addWidget(card, i // cols, i % cols)
        # Spacer for left alignment
        if daftar:
            rem = cols - (len(daftar) % cols)
            if rem < cols:
                last_row = (len(daftar) - 1) // cols
                for j in range(rem):
                    spacer = QWidget()
                    spacer.setFixedSize(210, 220)
                    spacer.setStyleSheet("background: transparent;")
                    self._grid.addWidget(spacer, last_row, (len(daftar) % cols) + j)
