"""KatalogView — CD-08 / UC09, UC14, UC15, UC16 — sidebar + card grid."""
from __future__ import annotations
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QGridLayout, QButtonGroup,
)
from PyQt6.QtCore import Qt, pyqtSignal, QRectF
from PyQt6.QtGui import QColor, QPixmap, QPainter, QPainterPath

from controllers.alat_controller import AlatController
from models.alat import Alat
import views.ui_helper as UI

CATEGORIES = ["Semua", "Kitchen", "Tools", "Cleaning", "Electronics", "Gardening"]


class _HoverCard(QWidget):
    """Item card with hover elevation painted via QPainter (no QGraphicsEffect)."""

    clicked = pyqtSignal(int)

    def __init__(self, alat: Alat, parent=None):
        super().__init__(parent)
        self._id = alat.get_id_alat()
        self._hovered = False
        self.setFixedSize(210, 220)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self._setup_content(alat)

    def _setup_content(self, alat: Alat):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        img = QLabel()
        img.setFixedHeight(132)
        img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bg = UI.category_color(alat.get_kategori())
        img.setStyleSheet(f"background: {bg}; border-radius: 14px 14px 0 0;")
        pm = UI.get_item_pixmap(alat.get_nama_alat(), 210, 132)
        if pm:
            img.setPixmap(pm)
            img.setScaledContents(True)
        else:
            img.setText(UI.category_emoji(alat.get_kategori()))
            img.setStyleSheet(img.styleSheet() + "font-size: 46px;")

        info = QWidget()
        info.setStyleSheet("background: white; border-radius: 0 0 14px 14px;")
        info_l = QVBoxLayout(info)
        info_l.setContentsMargins(12, 8, 12, 10)
        info_l.setSpacing(3)

        name_lbl = QLabel(alat.get_nama_alat())
        name_lbl.setStyleSheet(
            f"font-size: 12px; font-weight: 600; color: {UI.TEXT_DARK}; background: transparent;"
        )
        name_lbl.setWordWrap(True)

        cat_lbl = QLabel(alat.get_kategori())
        cat_lbl.setStyleSheet(f"font-size: 10px; color: {UI.TEXT_GRAY}; background: transparent;")

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
        w, h = float(self.width()), float(self.height())

        if self._hovered:
            p.setPen(Qt.PenStyle.NoPen)
            for dx, alpha in ((4, 8), (2, 16), (1, 24)):
                p.setBrush(QColor(61, 90, 241, alpha))
                p.drawRoundedRect(QRectF(dx, dx + 1, w - dx * 2, h - dx * 2), 14.0, 14.0)

        path = QPainterPath()
        path.addRoundedRect(QRectF(0.0, 0.0, w, h), 14.0, 14.0)
        p.fillPath(path, QColor("white"))

    def enterEvent(self, event):
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._id)


class _CatButton(QPushButton):
    """Category sidebar button."""

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(38)
        self._update_style(False)

    def setChecked(self, checked: bool):
        super().setChecked(checked)
        self._update_style(checked)

    def _update_style(self, active: bool):
        if active:
            self.setStyleSheet(
                f"QPushButton {{ background: {UI.BLUE_LIGHT}; color: {UI.BLUE};"
                f"  border: none; border-radius: 8px;"
                f"  font-size: 13px; font-weight: 600; padding: 0 16px; text-align: left; }}"
            )
        else:
            self.setStyleSheet(
                f"QPushButton {{ background: transparent; color: {UI.TEXT_MID};"
                f"  border: none; border-radius: 8px;"
                f"  font-size: 13px; padding: 0 16px; text-align: left; }}"
                f"QPushButton:hover {{ background: {UI.BLUE_LIGHT}; color: {UI.BLUE}; }}"
            )


class KatalogView(QWidget):
    """Layar 4 — Katalog Alat (UC09, UC14, UC15)."""

    open_detail = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ctrl = AlatController()
        self._current_kw = ""
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"background: {UI.LIGHT_BG};")
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── Left category sidebar ─────────────────────────────────────────────
        sidebar = QWidget()
        sidebar.setFixedWidth(210)
        sidebar.setStyleSheet(
            f"background: white; border-right: 1px solid {UI.BORDER};"
        )
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(16, 24, 16, 24)
        sb_layout.setSpacing(4)
        sb_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        lbl_cat = QLabel("Categories")
        lbl_cat.setStyleSheet(
            f"font-size: 11px; font-weight: 700; color: {UI.TEXT_GRAY};"
            f"letter-spacing: 1px; background: transparent; padding: 0 16px;"
        )
        sb_layout.addWidget(lbl_cat)
        sb_layout.addSpacing(8)

        self._btn_group = QButtonGroup(self)
        self._btn_group.setExclusive(True)
        self._cat_btns: dict[str, _CatButton] = {}

        cat_labels = {
            "Semua":       "📦  All Items",
            "Kitchen":     "🍳  Kitchen",
            "Tools":       "🔧  Tools",
            "Cleaning":    "🧹  Cleaning",
            "Electronics": "📱  Electronics",
            "Gardening":   "🌱  Gardening",
        }
        for cat, label in cat_labels.items():
            btn = _CatButton(label)
            self._btn_group.addButton(btn)
            self._cat_btns[cat] = btn
            btn.clicked.connect(lambda _, c=cat: self._on_cat(c))
            sb_layout.addWidget(btn)

        self._cat_btns["Semua"].setChecked(True)
        sb_layout.addStretch()
        outer.addWidget(sidebar)

        # ── Right content area ────────────────────────────────────────────────
        right = QWidget()
        right.setStyleSheet(f"background: {UI.LIGHT_BG};")
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(28, 24, 28, 24)
        right_layout.setSpacing(16)

        # Header row
        hdr = QHBoxLayout()
        self._lbl_title = UI.heading("Explore Items")
        hdr.addWidget(self._lbl_title)
        hdr.addStretch()
        right_layout.addLayout(hdr)

        # Scrollable grid
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
        right_layout.addWidget(scroll)
        right_layout.addWidget(self._lbl_kosong)

        outer.addWidget(right, 1)

    # ── Public API ────────────────────────────────────────────────────────────

    def showKatalog(self, daftar_alat: list[Alat] | None = None):
        self._current_kw = ""
        for cat, btn in self._cat_btns.items():
            btn.setChecked(cat == "Semua")
        if daftar_alat is None:
            daftar_alat = self._ctrl.get_semua_alat()
        self._lbl_title.setText("Explore Items")
        self._render_grid(daftar_alat)

    def search(self, kw: str):
        """Called by MainWindow navbar search."""
        self._current_kw = kw
        for btn in self._cat_btns.values():
            btn.setChecked(False)
        hasil = self._ctrl.cari_dan_filter(kw, "Semua")
        self._lbl_title.setText(f"Results for \"{kw}\"")
        if hasil:
            self._render_grid(hasil)
        else:
            self.showPesanKosong()

    def showFormPencarian(self):
        pass

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

    def _on_cat(self, kategori: str):
        hasil = self._ctrl.cari_dan_filter(self._current_kw, kategori)
        label = "Explore Items" if kategori == "Semua" else kategori
        self._lbl_title.setText(label)
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
        if daftar:
            rem = cols - (len(daftar) % cols)
            if rem < cols:
                last_row = (len(daftar) - 1) // cols
                for j in range(rem):
                    spacer = QWidget()
                    spacer.setFixedSize(210, 220)
                    spacer.setStyleSheet("background: transparent;")
                    self._grid.addWidget(spacer, last_row, (len(daftar) % cols) + j)
