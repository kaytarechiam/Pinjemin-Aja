"""MainWindow — CD-09 / Halaman Utama (Layar 3)
Navigation shell with sidebar + QStackedWidget content area.
"""
from __future__ import annotations
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QStackedWidget, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from session import Session
import views.ui_helper as UI


class MainWindow(QMainWindow):
    """Halaman Utama — shell with sidebar navbar and stacked content pages."""

    logout_requested = pyqtSignal()

    # Page indices in QStackedWidget
    PAGE_KATALOG    = 0
    PAGE_KATALOG_SY = 1
    PAGE_RIWAYAT    = 2
    PAGE_WALLET     = 3
    PAGE_PROFIL     = 4
    PAGE_PEMINJAMAN = 5   # dynamic; replaces itself

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pinjemin Aja!")
        self.setMinimumSize(1100, 700)
        self._peminjaman_widget = None
        self._setup_ui()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Sidebar ───────────────────────────────────────────────────────────
        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet(
            f"background: qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            f"stop:0 {UI.BLUE_DARK}, stop:1 {UI.BLUE});"
        )
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(0, 0, 0, 0)
        sb_layout.setSpacing(0)

        # Brand
        brand = QWidget()
        brand.setStyleSheet("background: transparent;")
        brand.setFixedHeight(80)
        brand_l = QHBoxLayout(brand)
        brand_l.setContentsMargins(20, 0, 20, 0)

        icon_lbl = QLabel("🏠")
        icon_lbl.setStyleSheet("font-size: 24px; background: transparent;")
        name_lbl = QLabel("Pinjemin Aja!")
        name_lbl.setStyleSheet(
            "color: white; font-size: 16px; font-weight: 700; background: transparent;"
        )
        brand_l.addWidget(icon_lbl)
        brand_l.addWidget(name_lbl)
        brand_l.addStretch()
        sb_layout.addWidget(brand)

        # Divider
        div = QWidget()
        div.setFixedHeight(1)
        div.setStyleSheet("background: rgba(255,255,255,0.2);")
        sb_layout.addWidget(div)
        sb_layout.addSpacing(12)

        # Nav items
        nav_items = [
            ("🔍", "Explore",       self.PAGE_KATALOG),
            ("📦", "Katalog Saya",  self.PAGE_KATALOG_SY),
            ("📋", "Riwayat",       self.PAGE_RIWAYAT),
            ("💳", "Dompet",        self.PAGE_WALLET),
            ("👤", "Profil",        self.PAGE_PROFIL),
        ]
        self._nav_buttons: dict[int, QPushButton] = {}
        for emoji, label, page_idx in nav_items:
            btn = self._make_nav_btn(emoji, label, page_idx)
            self._nav_buttons[page_idx] = btn
            sb_layout.addWidget(btn)

        sb_layout.addStretch()

        # User info + logout
        sb_layout.addWidget(div := QWidget())
        div.setFixedHeight(1)
        div.setStyleSheet("background: rgba(255,255,255,0.2);")

        user_box = QWidget()
        user_box.setStyleSheet("background: transparent;")
        user_box.setFixedHeight(72)
        ub_layout = QHBoxLayout(user_box)
        ub_layout.setContentsMargins(16, 8, 16, 8)
        ub_layout.setSpacing(10)

        user = Session.get_current_user()
        initials = (user.get_nama_lengkap()[:2].upper() if user else "?")
        avatar = QLabel(initials)
        avatar.setFixedSize(36, 36)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            "background: rgba(255,255,255,0.25); color: white; border-radius: 18px;"
            "font-size: 13px; font-weight: 700;"
        )

        user_info = QVBoxLayout()
        user_info.setSpacing(2)
        name_short = (user.get_nama_lengkap() if user else "Guest")
        if len(name_short) > 16:
            name_short = name_short[:14] + "…"
        lbl_name = QLabel(name_short)
        lbl_name.setStyleSheet("color: white; font-size: 12px; font-weight: 600; background: transparent;")
        lbl_wa = QLabel(user.get_no_wa() if user else "")
        lbl_wa.setStyleSheet("color: rgba(255,255,255,0.7); font-size: 10px; background: transparent;")
        user_info.addWidget(lbl_name)
        user_info.addWidget(lbl_wa)

        btn_logout = QPushButton("⏻")
        btn_logout.setFixedSize(30, 30)
        btn_logout.setToolTip("Logout")
        btn_logout.setStyleSheet(
            "background: rgba(255,255,255,0.15); color: white; border: none;"
            "border-radius: 15px; font-size: 14px;"
        )
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.clicked.connect(self._on_logout)

        ub_layout.addWidget(avatar)
        ub_layout.addLayout(user_info)
        ub_layout.addStretch()
        ub_layout.addWidget(btn_logout)
        sb_layout.addWidget(user_box)

        main_layout.addWidget(sidebar)

        # ── Content area ──────────────────────────────────────────────────────
        self._stack = QStackedWidget()
        self._stack.setStyleSheet(f"background: {UI.LIGHT_BG};")

        # Lazy-import views to avoid circular deps
        from views.katalog_view      import KatalogView
        from views.katalog_saya_view import KatalogSayaView
        from views.riwayat_view      import RiwayatView
        from views.wallet_view       import WalletView
        from views.profil_view       import ProfilView

        self._katalog_view   = KatalogView()
        self._katalog_sy_view = KatalogSayaView()
        self._riwayat_view   = RiwayatView()
        self._wallet_view    = WalletView()
        self._profil_view    = ProfilView()

        self._stack.addWidget(self._katalog_view)    # index 0
        self._stack.addWidget(self._katalog_sy_view) # index 1
        self._stack.addWidget(self._riwayat_view)    # index 2
        self._stack.addWidget(self._wallet_view)     # index 3
        self._stack.addWidget(self._profil_view)     # index 4
        # index 5 reserved for PeminjamanView (added/replaced dynamically)

        # Wire catalog → detail
        self._katalog_view.open_detail.connect(self._open_peminjaman)

        main_layout.addWidget(self._stack)

        # Show default page
        self._switch_page(self.PAGE_KATALOG)

    # ── Nav helpers ───────────────────────────────────────────────────────────

    def _make_nav_btn(self, emoji: str, label: str, page_idx: int) -> QPushButton:
        btn = QPushButton(f"  {emoji}  {label}")
        btn.setFixedHeight(46)
        btn.setCheckable(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(self._nav_style(False))
        btn.clicked.connect(lambda _, idx=page_idx: self._switch_page(idx))
        return btn

    @staticmethod
    def _nav_style(active: bool) -> str:
        if active:
            return (
                "background: rgba(255,255,255,0.20); color: white; border: none;"
                "text-align: left; padding-left: 20px; font-size: 14px; font-weight: 600;"
                "border-left: 3px solid white;"
            )
        return (
            "background: transparent; color: rgba(255,255,255,0.80); border: none;"
            "text-align: left; padding-left: 20px; font-size: 14px; font-weight: 500;"
            "border-left: 3px solid transparent;"
        )

    def _switch_page(self, page_idx: int):
        # Remove peminjaman view if going elsewhere
        if page_idx != self.PAGE_PEMINJAMAN and self._peminjaman_widget is not None:
            self._stack.removeWidget(self._peminjaman_widget)
            self._peminjaman_widget.deleteLater()
            self._peminjaman_widget = None

        # Refresh data on switch
        if page_idx == self.PAGE_KATALOG:
            self._katalog_view.showKatalog()
        elif page_idx == self.PAGE_KATALOG_SY:
            self._katalog_sy_view.showKatalogSaya()
        elif page_idx == self.PAGE_RIWAYAT:
            self._riwayat_view.showRiwayat()
        elif page_idx == self.PAGE_WALLET:
            self._wallet_view.showSaldo()
        elif page_idx == self.PAGE_PROFIL:
            self._profil_view.showProfil()

        self._stack.setCurrentIndex(page_idx)

        # Update nav highlights
        for idx, btn in self._nav_buttons.items():
            btn.setChecked(idx == page_idx)
            btn.setStyleSheet(self._nav_style(idx == page_idx))

    # ── Detail / Peminjaman ───────────────────────────────────────────────────

    def _open_peminjaman(self, id_alat: int):
        from views.peminjaman_view import PeminjamanView

        # Remove old one if present
        if self._peminjaman_widget is not None:
            self._stack.removeWidget(self._peminjaman_widget)
            self._peminjaman_widget.deleteLater()

        pv = PeminjamanView(id_alat)
        pv.go_back.connect(lambda: self._switch_page(self.PAGE_KATALOG))
        pv.go_riwayat.connect(lambda: self._switch_page(self.PAGE_RIWAYAT))

        self._peminjaman_widget = pv
        self._stack.addWidget(pv)
        self._stack.setCurrentWidget(pv)

        # Deactivate all nav buttons visually
        for btn in self._nav_buttons.values():
            btn.setChecked(False)
            btn.setStyleSheet(self._nav_style(False))

    # ── Logout ────────────────────────────────────────────────────────────────

    def _on_logout(self):
        if UI.show_confirm("Yakin ingin keluar dari akun?", self):
            Session.logout()
            self.logout_requested.emit()
