"""MainWindow — top navbar layout matching Java MainView."""
from __future__ import annotations
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QStackedWidget, QGraphicsOpacityEffect,
    QLineEdit, QMenu, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QAction

from session import Session
import views.ui_helper as UI

PAGE_KATALOG    = 0
PAGE_KATALOG_SY = 1
PAGE_RIWAYAT    = 2
PAGE_WALLET     = 3
PAGE_PROFIL     = 4
PAGE_PEMINJAMAN = 5


class _NavButton(QPushButton):
    """Top navbar navigation link button."""

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(36)
        self._update_style(False)

    def setChecked(self, checked: bool):
        super().setChecked(checked)
        self._update_style(checked)

    def _update_style(self, active: bool):
        if active:
            self.setStyleSheet(
                f"QPushButton {{"
                f"  background: {UI.BLUE_LIGHT}; color: {UI.BLUE};"
                f"  border: none; border-radius: 8px;"
                f"  font-size: 13px; font-weight: 600; padding: 0 16px;"
                f"}}"
            )
        else:
            self.setStyleSheet(
                f"QPushButton {{"
                f"  background: transparent; color: {UI.TEXT_MID};"
                f"  border: none; border-radius: 8px;"
                f"  font-size: 13px; font-weight: 500; padding: 0 16px;"
                f"}}"
                f"QPushButton:hover {{"
                f"  background: {UI.BLUE_LIGHT}; color: {UI.BLUE};"
                f"}}"
            )


class MainWindow(QMainWindow):
    """Shell with top navbar + page stack — matching Java MainView."""

    logout_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pinjemin Aja!")
        self.setMinimumSize(1100, 700)
        self._peminjaman_widget = None
        self._fade_anim = None
        self._setup_ui()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Top Navbar ────────────────────────────────────────────────────────
        navbar = self._build_navbar()
        root.addWidget(navbar)

        # ── Content stack ─────────────────────────────────────────────────────
        self._stack = QStackedWidget()
        self._stack.setStyleSheet(f"background: {UI.LIGHT_BG};")

        self._opacity = QGraphicsOpacityEffect(self._stack)
        self._opacity.setOpacity(1.0)
        self._stack.setGraphicsEffect(self._opacity)

        from views.katalog_view      import KatalogView
        from views.katalog_saya_view import KatalogSayaView
        from views.riwayat_view      import RiwayatView
        from views.wallet_view       import WalletView
        from views.profil_view       import ProfilView

        self._katalog_view    = KatalogView()
        self._katalog_sy_view = KatalogSayaView()
        self._riwayat_view    = RiwayatView()
        self._wallet_view     = WalletView()
        self._profil_view     = ProfilView()

        self._stack.addWidget(self._katalog_view)    # 0
        self._stack.addWidget(self._katalog_sy_view) # 1
        self._stack.addWidget(self._riwayat_view)    # 2
        self._stack.addWidget(self._wallet_view)     # 3
        self._stack.addWidget(self._profil_view)     # 4

        self._katalog_view.open_detail.connect(self._open_peminjaman)
        self._wallet_view.go_profil.connect(lambda: self._switch_page(PAGE_PROFIL))
        self._wallet_view.logout_requested.connect(self._on_logout)
        self._profil_view.go_wallet.connect(lambda: self._switch_page(PAGE_WALLET))
        self._profil_view.logout_requested.connect(self._on_logout)

        root.addWidget(self._stack, 1)
        self._switch_page(PAGE_KATALOG, animated=False)

    # ── Navbar ────────────────────────────────────────────────────────────────

    def _build_navbar(self) -> QWidget:
        bar = QWidget()
        bar.setFixedHeight(62)
        bar.setStyleSheet(
            f"background: white; border-bottom: 1px solid {UI.BORDER};"
        )
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(28, 0, 28, 0)
        lay.setSpacing(0)

        # Logo
        lbl_logo = QLabel("🏠")
        lbl_logo.setStyleSheet("font-size: 20px; background: transparent;")
        lbl_name = QLabel("Pinjemin Aja!")
        lbl_name.setStyleSheet(
            f"font-size: 17px; font-weight: 700; color: {UI.TEXT_DARK}; background: transparent;"
        )
        lay.addWidget(lbl_logo)
        lay.addSpacing(8)
        lay.addWidget(lbl_name)
        lay.addSpacing(32)

        # Nav links
        self._nav_btns: dict[int, _NavButton] = {}
        for label, idx in [("Explore", PAGE_KATALOG), ("My Items", PAGE_KATALOG_SY), ("History", PAGE_RIWAYAT)]:
            btn = _NavButton(label)
            btn.clicked.connect(lambda _, i=idx: self._switch_page(i))
            self._nav_btns[idx] = btn
            lay.addWidget(btn)
            lay.addSpacing(4)

        lay.addStretch(1)

        # Search
        self._tf_search = QLineEdit()
        self._tf_search.setPlaceholderText("🔍  Search products...")
        self._tf_search.setFixedSize(220, 36)
        self._tf_search.setStyleSheet(
            f"QLineEdit {{"
            f"  background: {UI.LIGHT_BG}; border: 1.5px solid {UI.BORDER};"
            f"  border-radius: 18px; padding: 0 16px; font-size: 13px; color: {UI.TEXT_DARK};"
            f"}}"
            f"QLineEdit:focus {{ border: 1.5px solid {UI.BLUE}; }}"
        )
        self._tf_search.returnPressed.connect(self._on_search)
        lay.addWidget(self._tf_search)
        lay.addSpacing(16)

        # User avatar button with dropdown menu
        user = Session.get_current_user()
        initials = user.get_nama_lengkap()[:2].upper() if user else "?"
        name_short = user.get_nama_lengkap().split()[0] if user else "User"

        self._btn_user = QPushButton(f"  {initials}  {name_short} ▾")
        self._btn_user.setFixedHeight(36)
        self._btn_user.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_user.setStyleSheet(
            f"QPushButton {{"
            f"  background: {UI.BLUE_LIGHT}; color: {UI.BLUE};"
            f"  border: none; border-radius: 18px;"
            f"  font-size: 13px; font-weight: 600; padding: 0 16px;"
            f"}}"
            f"QPushButton:hover {{ background: #DDE3FD; }}"
        )

        menu = QMenu(self._btn_user)
        menu.setStyleSheet(
            f"QMenu {{ background: white; border: 1px solid {UI.BORDER}; border-radius: 8px; padding: 4px; }}"
            f"QMenu::item {{ padding: 8px 20px; font-size: 13px; color: {UI.TEXT_DARK}; border-radius: 6px; }}"
            f"QMenu::item:selected {{ background: {UI.BLUE_LIGHT}; color: {UI.BLUE}; }}"
            f"QMenu::separator {{ height: 1px; background: {UI.BORDER}; margin: 4px 8px; }}"
        )
        act_profil  = QAction("👤  Profile", self)
        act_wallet  = QAction("💳  My Wallet", self)
        act_logout  = QAction("⏻  Logout", self)
        act_profil.triggered.connect(lambda: self._switch_page(PAGE_PROFIL))
        act_wallet.triggered.connect(lambda: self._switch_page(PAGE_WALLET))
        act_logout.triggered.connect(self._on_logout)
        menu.addAction(act_profil)
        menu.addAction(act_wallet)
        menu.addSeparator()
        menu.addAction(act_logout)
        self._btn_user.setMenu(menu)

        lay.addWidget(self._btn_user)
        return bar

    # ── Search ────────────────────────────────────────────────────────────────

    def _on_search(self):
        kw = self._tf_search.text().strip()
        self._switch_page(PAGE_KATALOG)
        if kw:
            self._katalog_view.search(kw)
        self._tf_search.clear()

    # ── Page transitions ──────────────────────────────────────────────────────

    def _switch_page(self, page_idx: int, animated: bool = True,
                     widget: QWidget | None = None):
        if page_idx != PAGE_PEMINJAMAN and self._peminjaman_widget is not None:
            self._stack.removeWidget(self._peminjaman_widget)
            self._peminjaman_widget.deleteLater()
            self._peminjaman_widget = None

        if page_idx == PAGE_KATALOG:
            self._katalog_view.showKatalog()
        elif page_idx == PAGE_KATALOG_SY:
            self._katalog_sy_view.showKatalogSaya()
        elif page_idx == PAGE_RIWAYAT:
            self._riwayat_view.showRiwayat()
        elif page_idx == PAGE_WALLET:
            self._wallet_view.showSaldo()
        elif page_idx == PAGE_PROFIL:
            self._profil_view.showProfil()

        def _do_switch():
            if widget:
                self._stack.setCurrentWidget(widget)
            else:
                self._stack.setCurrentIndex(page_idx)
            if animated:
                a_in = QPropertyAnimation(self._opacity, b"opacity", self)
                a_in.setDuration(180)
                a_in.setStartValue(0.0)
                a_in.setEndValue(1.0)
                a_in.setEasingCurve(QEasingCurve.Type.InCubic)
                a_in.start()
                self._fade_anim = a_in

        if animated:
            a_out = QPropertyAnimation(self._opacity, b"opacity", self)
            a_out.setDuration(100)
            a_out.setStartValue(1.0)
            a_out.setEndValue(0.0)
            a_out.setEasingCurve(QEasingCurve.Type.OutCubic)
            a_out.finished.connect(_do_switch)
            a_out.start()
            self._fade_anim = a_out
        else:
            _do_switch()

        for idx, btn in self._nav_btns.items():
            btn.setChecked(idx == page_idx)

    # ── Peminjaman detail ─────────────────────────────────────────────────────

    def _open_peminjaman(self, id_alat: int):
        from views.peminjaman_view import PeminjamanView

        if self._peminjaman_widget is not None:
            self._stack.removeWidget(self._peminjaman_widget)
            self._peminjaman_widget.deleteLater()

        pv = PeminjamanView(id_alat)
        pv.go_back.connect(lambda: self._switch_page(PAGE_KATALOG))
        pv.go_riwayat.connect(lambda: self._switch_page(PAGE_RIWAYAT))

        self._peminjaman_widget = pv
        self._stack.addWidget(pv)
        self._switch_page(PAGE_PEMINJAMAN, widget=pv)

        for btn in self._nav_btns.values():
            btn.setChecked(False)

    # ── Logout ────────────────────────────────────────────────────────────────

    def _on_logout(self):
        if UI.show_confirm("Yakin ingin keluar dari akun?", self):
            Session.logout()
            self.logout_requested.emit()
