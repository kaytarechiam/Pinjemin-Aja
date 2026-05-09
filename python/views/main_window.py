"""MainWindow — Halaman Utama with animated sidebar + page fade transitions."""
from __future__ import annotations
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QStackedWidget, QGraphicsOpacityEffect,
    QSizePolicy, QScrollArea
)
from PyQt6.QtCore import (
    Qt, pyqtSignal, QPropertyAnimation, QEasingCurve,
    QParallelAnimationGroup, QPoint
)
from PyQt6.QtGui import QPainter, QPainterPath, QColor, QLinearGradient

from session import Session
import views.ui_helper as UI

# Sidebar widths
_SIDEBAR_FULL  = 230
_SIDEBAR_MINI  = 68

# Page indices
PAGE_KATALOG    = 0
PAGE_KATALOG_SY = 1
PAGE_RIWAYAT    = 2
PAGE_WALLET     = 3
PAGE_PROFIL     = 4
PAGE_PEMINJAMAN = 5   # dynamic


class _NavItem(QPushButton):
    """Single sidebar navigation button."""

    def __init__(self, emoji: str, label: str, parent=None):
        super().__init__(parent)
        self._emoji = emoji
        self._label = label
        self._expanded = True
        self.setFixedHeight(48)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_text()
        self._set_style(False)

    def _update_text(self):
        if self._expanded:
            self.setText(f"  {self._emoji}   {self._label}")
        else:
            self.setText(self._emoji)

    def set_expanded(self, expanded: bool):
        self._expanded = expanded
        self._update_text()

    def _set_style(self, active: bool):
        if active:
            self.setStyleSheet(
                f"QPushButton {{"
                f"  background: rgba(255,255,255,0.18); color: white;"
                f"  border: none; border-left: 3px solid white;"
                f"  text-align: left; padding-left: 18px;"
                f"  font-size: 14px; font-weight: 600; border-radius: 0px;"
                f"}}"
            )
        else:
            self.setStyleSheet(
                f"QPushButton {{"
                f"  background: transparent; color: rgba(255,255,255,0.75);"
                f"  border: none; border-left: 3px solid transparent;"
                f"  text-align: left; padding-left: 18px;"
                f"  font-size: 14px; font-weight: 500; border-radius: 0px;"
                f"}}"
                f"QPushButton:hover {{"
                f"  background: rgba(255,255,255,0.10); color: white;"
                f"}}"
            )

    def setChecked(self, checked: bool):
        super().setChecked(checked)
        self._set_style(checked)


class _GradientSidebar(QWidget):
    """Deep-indigo gradient sidebar panel."""

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        grad = QLinearGradient(0, 0, 0, self.height())
        grad.setColorAt(0.0, QColor("#1E1B4B"))
        grad.setColorAt(1.0, QColor("#312E81"))
        painter.fillRect(self.rect(), grad)


class MainWindow(QMainWindow):
    """Shell with animated collapsible sidebar and page-fade content area."""

    logout_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pinjemin Aja!")
        self.setMinimumSize(1100, 700)
        self._peminjaman_widget = None
        self._sidebar_expanded  = True
        self._fade_anim = None
        self._setup_ui()

    # ── Build UI ──────────────────────────────────────────────────────────────

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        outer = QHBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── Sidebar ───────────────────────────────────────────────────────────
        self._sidebar = _GradientSidebar()
        self._sidebar.setFixedWidth(_SIDEBAR_FULL)

        sb = QVBoxLayout(self._sidebar)
        sb.setContentsMargins(0, 0, 0, 0)
        sb.setSpacing(0)

        # Header: logo + toggle
        hdr = QWidget()
        hdr.setStyleSheet("background: transparent;")
        hdr.setFixedHeight(72)
        hdr_l = QHBoxLayout(hdr)
        hdr_l.setContentsMargins(20, 0, 12, 0)

        self._lbl_brand = QLabel("🏠  Pinjemin Aja!")
        self._lbl_brand.setStyleSheet(
            "color: white; font-size: 15px; font-weight: 700; background: transparent;"
        )
        btn_toggle = QPushButton("☰")
        btn_toggle.setFixedSize(36, 36)
        btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_toggle.setStyleSheet(
            "QPushButton {"
            "  background: rgba(255,255,255,0.12); color: white; border: none;"
            "  border-radius: 8px; font-size: 15px;"
            "}"
            "QPushButton:hover { background: rgba(255,255,255,0.20); }"
        )
        btn_toggle.clicked.connect(self._toggle_sidebar)
        hdr_l.addWidget(self._lbl_brand, 1)
        hdr_l.addWidget(btn_toggle)
        sb.addWidget(hdr)

        # Divider
        div = QWidget(); div.setFixedHeight(1)
        div.setStyleSheet("background: rgba(255,255,255,0.15);")
        sb.addWidget(div)
        sb.addSpacing(8)

        # Nav items
        nav_config = [
            ("🔍", "Explore",       PAGE_KATALOG),
            ("📦", "Katalog Saya",  PAGE_KATALOG_SY),
            ("📋", "Riwayat",       PAGE_RIWAYAT),
        ]
        self._nav_btns: dict[int, _NavItem] = {}
        for emoji, label, idx in nav_config:
            btn = _NavItem(emoji, label)
            btn.clicked.connect(lambda _, i=idx: self._switch_page(i))
            self._nav_btns[idx] = btn
            sb.addWidget(btn)

        sb.addStretch()

        # Bottom divider
        div2 = QWidget(); div2.setFixedHeight(1)
        div2.setStyleSheet("background: rgba(255,255,255,0.15);")
        sb.addWidget(div2)

        # Bottom nav items
        bot_config = [
            ("💳", "Dompet",  PAGE_WALLET),
            ("👤", "Profil",  PAGE_PROFIL),
        ]
        for emoji, label, idx in bot_config:
            btn = _NavItem(emoji, label)
            btn.clicked.connect(lambda _, i=idx: self._switch_page(i))
            self._nav_btns[idx] = btn
            sb.addWidget(btn)

        # User info + logout
        sb.addWidget(QWidget())  # small spacer
        user_bar = self._build_user_bar()
        sb.addWidget(user_bar)

        outer.addWidget(self._sidebar)

        # ── Content area ──────────────────────────────────────────────────────
        self._stack = QStackedWidget()
        self._stack.setStyleSheet(f"background: {UI.LIGHT_BG};")

        # Apply opacity effect for fade transition
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

        outer.addWidget(self._stack, 1)

        self._switch_page(PAGE_KATALOG, animated=False)

    def _build_user_bar(self) -> QWidget:
        w = QWidget()
        w.setFixedHeight(68)
        w.setStyleSheet("background: rgba(255,255,255,0.06); border-radius: 0px;")
        lay = QHBoxLayout(w)
        lay.setContentsMargins(16, 0, 12, 0)
        lay.setSpacing(10)

        user = Session.get_current_user()
        initials = user.get_nama_lengkap()[:2].upper() if user else "?"
        avatar = QLabel(initials)
        avatar.setFixedSize(36, 36)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            "background: rgba(255,255,255,0.25); color: white;"
            "border-radius: 18px; font-size: 13px; font-weight: 700;"
        )

        self._lbl_username = QLabel(
            (user.get_nama_lengkap()[:16] if user else "Guest")
        )
        self._lbl_username.setStyleSheet(
            "color: white; font-size: 12px; font-weight: 600; background: transparent;"
        )

        btn_logout = QPushButton("⏻")
        btn_logout.setFixedSize(30, 30)
        btn_logout.setToolTip("Logout")
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.setStyleSheet(
            "QPushButton {"
            "  background: rgba(255,255,255,0.12); color: white; border: none;"
            "  border-radius: 15px; font-size: 14px;"
            "}"
            "QPushButton:hover { background: rgba(239,68,68,0.40); }"
        )
        btn_logout.clicked.connect(self._on_logout)

        lay.addWidget(avatar)
        lay.addWidget(self._lbl_username, 1)
        lay.addWidget(btn_logout)
        return w

    # ── Sidebar collapse/expand ───────────────────────────────────────────────

    def _toggle_sidebar(self):
        target = _SIDEBAR_MINI if self._sidebar_expanded else _SIDEBAR_FULL
        self._sidebar_expanded = not self._sidebar_expanded

        anim = QPropertyAnimation(self._sidebar, b"minimumWidth", self)
        anim.setDuration(260)
        anim.setStartValue(self._sidebar.width())
        anim.setEndValue(target)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()
        self._sb_anim = anim

        anim2 = QPropertyAnimation(self._sidebar, b"maximumWidth", self)
        anim2.setDuration(260)
        anim2.setStartValue(self._sidebar.width())
        anim2.setEndValue(target)
        anim2.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim2.start()
        self._sb_anim2 = anim2

        # Toggle text visibility
        show = not self._sidebar_expanded
        self._lbl_brand.setVisible(show)
        self._lbl_username.setVisible(show)
        for btn in self._nav_btns.values():
            btn.set_expanded(show)

    # ── Page transitions ──────────────────────────────────────────────────────

    def _switch_page(self, page_idx: int, animated: bool = True,
                     widget: QWidget | None = None):
        # Remove dynamic peminjaman when going to a main page
        if page_idx != PAGE_PEMINJAMAN and self._peminjaman_widget is not None:
            self._stack.removeWidget(self._peminjaman_widget)
            self._peminjaman_widget.deleteLater()
            self._peminjaman_widget = None

        # Refresh data
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
                a_in.setDuration(200)
                a_in.setStartValue(0.0)
                a_in.setEndValue(1.0)
                a_in.setEasingCurve(QEasingCurve.Type.InCubic)
                a_in.start()
                self._fade_anim = a_in

        if animated:
            a_out = QPropertyAnimation(self._opacity, b"opacity", self)
            a_out.setDuration(110)
            a_out.setStartValue(1.0)
            a_out.setEndValue(0.0)
            a_out.setEasingCurve(QEasingCurve.Type.OutCubic)
            a_out.finished.connect(_do_switch)
            a_out.start()
            self._fade_anim = a_out
        else:
            _do_switch()

        # Update nav highlights
        for idx, btn in self._nav_btns.items():
            btn.setChecked(idx == page_idx)

    # ── Open detail / peminjaman ──────────────────────────────────────────────

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

        # Deactivate all nav highlights
        for btn in self._nav_btns.values():
            btn.setChecked(False)

    # ── Logout ────────────────────────────────────────────────────────────────

    def _on_logout(self):
        if UI.show_confirm("Yakin ingin keluar dari akun?", self):
            Session.logout()
            self.logout_requested.emit()
