"""main.py — Entry point for Pinjemin Aja! (PyQt6)"""
import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget, QWidget

from database.database import initialize
from database.seeder import seed

from views.registrasi_view import RegistrasiView
from views.login_view      import LoginView
from views.main_window     import MainWindow


# ── Page indices ──────────────────────────────────────────────────────────────
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
        # MainWindow added on first login (index 2)

        # Signals
        self._login_view.go_register.connect(self._show_register)
        self._login_view.login_success.connect(self._on_login_success)
        self._reg_view.go_login.connect(self._show_login)

        self.setCurrentIndex(PAGE_LOGIN)

    # ── Transitions ───────────────────────────────────────────────────────────

    def _show_login(self):
        self._login_view.showFormLogin()
        self.setCurrentIndex(PAGE_LOGIN)

    def _show_register(self):
        self._reg_view.showFormRegistrasi()
        self.setCurrentIndex(PAGE_REGISTER)

    def _on_login_success(self, pengguna):
        # Build (or rebuild) MainWindow
        if self._main_window is not None:
            self.removeWidget(self._main_window)
            self._main_window.deleteLater()

        self._main_window = MainWindow()
        self._main_window.logout_requested.connect(self._on_logout)
        self.addWidget(self._main_window)   # becomes index 2
        self.setCurrentIndex(PAGE_MAIN)

    def _on_logout(self):
        self._login_view.showFormLogin()
        self.setCurrentIndex(PAGE_LOGIN)


def main():
    # 1. Init database
    initialize()
    seed()

    # 2. Start Qt app
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # 3. Apply global font
    from PyQt6.QtGui import QFont
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = App()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
