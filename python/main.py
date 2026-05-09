"""main.py — Entry point for Pinjemin Aja! (PyQt6)"""
import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from PyQt6.QtGui import QFont

from database.database import initialize
from database.seeder import seed

from views.registrasi_view import RegistrasiView
from views.login_view      import LoginView
from views.main_window     import MainWindow

PAGE_LOGIN    = 0
PAGE_REGISTER = 1
PAGE_MAIN     = 2


class App(QStackedWidget):
    """Root stacked widget: Login ↔ Register ↔ MainWindow."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pinjemin Aja!")
        self.setMinimumSize(1100, 700)
        self._main_window: MainWindow | None = None
        self._setup()

    def _setup(self):
        self._login_view = LoginView()
        self._reg_view   = RegistrasiView()

        self.addWidget(self._login_view)   # 0
        self.addWidget(self._reg_view)     # 1

        self._login_view.go_register.connect(self._show_register)
        self._login_view.login_success.connect(self._on_login_success)
        self._reg_view.go_login.connect(self._show_login)

        self.setCurrentIndex(PAGE_LOGIN)

    # ── Transitions ───────────────────────────────────────────────────────────

    def _show_login(self):
        self._login_view.showFormLogin()
        self._fade_to(PAGE_LOGIN)

    def _show_register(self):
        self._reg_view.showFormRegistrasi()
        self._fade_to(PAGE_REGISTER)

    def _on_login_success(self, pengguna):
        if self._main_window is not None:
            self.removeWidget(self._main_window)
            self._main_window.deleteLater()

        self._main_window = MainWindow()
        self._main_window.logout_requested.connect(self._on_logout)
        self.addWidget(self._main_window)
        self._fade_to(PAGE_MAIN)

    def _on_logout(self):
        self._login_view.showFormLogin()
        self._fade_to(PAGE_LOGIN)

    def _fade_to(self, index: int):
        """Switch between top-level screens (instant — avoids nested QGraphicsEffect
        conflict between App-level opacity and MainWindow's stack opacity effect)."""
        self.setCurrentIndex(index)


def main():
    initialize()
    seed()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Global font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Global stylesheet — clean scrollbars + remove QStackedWidget borders
    app.setStyleSheet(
        "QScrollBar:vertical {"
        "  width: 6px; background: transparent; margin: 0;"
        "}"
        "QScrollBar::handle:vertical {"
        "  background: #CBD5E1; border-radius: 3px; min-height: 30px;"
        "}"
        "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {"
        "  height: 0px;"
        "}"
        "QScrollBar:horizontal {"
        "  height: 6px; background: transparent; margin: 0;"
        "}"
        "QScrollBar::handle:horizontal {"
        "  background: #CBD5E1; border-radius: 3px; min-width: 30px;"
        "}"
        "QToolTip {"
        "  background: #1E293B; color: white; border: none;"
        "  border-radius: 6px; padding: 5px 10px; font-size: 12px;"
        "}"
    )

    window = App()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
