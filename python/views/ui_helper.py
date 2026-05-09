"""UI helpers, styles, and widget factories — PyQt6, matching Java design system."""
from __future__ import annotations
from pathlib import Path

from PyQt6.QtWidgets import (
    QLabel, QWidget, QFrame, QPushButton, QLineEdit,
    QTextEdit, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QRectF
from PyQt6.QtGui import QColor, QPixmap, QPainter, QPainterPath

# ── Brand colours (matching Java UIHelper exactly) ────────────────────────────
BLUE        = "#3D5AF1"
BLUE_DARK   = "#2D46D6"
BLUE_LIGHT  = "#EEF1FF"
GREEN       = "#10B981"
GREEN_LIGHT = "#D1FAE5"
RED         = "#EF4444"
RED_LIGHT   = "#FEE2E2"
AMBER       = "#F59E0B"
AMBER_LIGHT = "#FEF3C7"
LIGHT_BG    = "#F7F8FC"
BORDER      = "#E8EAF0"
TEXT_DARK   = "#1A1D2E"
TEXT_MID    = "#4B5563"
TEXT_GRAY   = "#9CA3AF"
WHITE       = "#FFFFFF"
CARD_BG     = "#FFFFFF"

# ── Image map ─────────────────────────────────────────────────────────────────
_IMG_DIR = Path(__file__).parent.parent / "resources" / "images"
ITEM_IMAGE_MAP = {
    "Waffle Maker":        "waffle_maker.jpg",
    "Stand Mixer":         "stand_mixer.jpg",
    "Food Processor":      "food_processor.jpg",
    "Slow Juicer":         "slow_juicer.jpg",
    "Ice Cream Maker":     "ice_cream_maker.jpg",
    "Rice Cooker":         "rice_cooker.jpg",
    "Power Drill":         "power_drill.jpg",
    "Electric Sander":     "electric_sander.jpg",
    "Foldable Hand Truck": "hand_truck.jpg",
    "Step Ladder":         "step_ladder.jpg",
    "Pressure Washer":     "pressure_washer.jpg",
    "Vacuum Cleaner":      "vacuum_cleaner.jpg",
    "Portable Blower":     "portable_blower.jpg",
    "Garden Hose":         "garden_hose.jpg",
    "Lawn Mower":          "lawn_mower.jpg",
    "Portable Projector":  "projector.jpg",
}


def get_item_pixmap(nama_alat: str, w: int, h: int) -> QPixmap | None:
    fname = ITEM_IMAGE_MAP.get(nama_alat)
    if not fname:
        return None
    path = _IMG_DIR / fname
    if not path.exists():
        return None
    pm = QPixmap(str(path))
    return pm.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                     Qt.TransformationMode.SmoothTransformation)


# ── Category helpers ──────────────────────────────────────────────────────────
_CAT_COLORS = {
    "Kitchen":     "#FEF3C7",
    "Tools":       "#DBEAFE",
    "Cleaning":    "#D1FAE5",
    "Electronics": "#EDE9FE",
    "Gardening":   "#DCFCE7",
}
_CAT_EMOJIS = {
    "Kitchen": "🍳", "Tools": "🔧",
    "Cleaning": "🧹", "Electronics": "📱", "Gardening": "🌱",
}


def category_color(cat: str) -> str:
    return _CAT_COLORS.get(cat, "#F1F5F9")


def category_emoji(cat: str) -> str:
    return _CAT_EMOJIS.get(cat, "📦")


# ── Formatting ────────────────────────────────────────────────────────────────
def format_rupiah(amount: float) -> str:
    return "Rp {:,.0f}".format(amount).replace(",", ".")


# ── Stub (kept for API compat — no QGraphicsEffect applied) ───────────────────
def add_shadow(widget, **kwargs) -> None:
    """No-op: avoids nested QGraphicsEffect painter conflicts."""


# ── QSS helpers ───────────────────────────────────────────────────────────────
def input_style() -> str:
    return (
        f"background: white; border: 1.5px solid {BORDER}; border-radius: 8px;"
        f"padding: 8px 14px; font-size: 13px; color: {TEXT_DARK};"
    )


# ── Widget factories ──────────────────────────────────────────────────────────
def primary_button(text: str) -> QPushButton:
    btn = QPushButton(text)
    btn.setFixedHeight(42)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setStyleSheet(
        f"QPushButton {{"
        f"  background: qlineargradient(x1:0,y1:0,x2:1,y2:0,"
        f"  stop:0 {BLUE}, stop:1 #6B8EFF);"
        f"  color: white; border: none; border-radius: 8px;"
        f"  font-size: 13px; font-weight: 600; padding: 0 20px;"
        f"}}"
        f"QPushButton:hover {{"
        f"  background: qlineargradient(x1:0,y1:0,x2:1,y2:0,"
        f"  stop:0 {BLUE_DARK}, stop:1 {BLUE});"
        f"}}"
        f"QPushButton:pressed {{ padding-top: 1px; }}"
    )
    return btn


def outline_button(text: str) -> QPushButton:
    btn = QPushButton(text)
    btn.setFixedHeight(42)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setStyleSheet(
        f"QPushButton {{"
        f"  background: transparent; color: {BLUE};"
        f"  border: 1.5px solid {BLUE}; border-radius: 8px;"
        f"  font-size: 13px; font-weight: 600; padding: 0 20px;"
        f"}}"
        f"QPushButton:hover {{ background: {BLUE_LIGHT}; }}"
    )
    return btn


def styled_input(placeholder: str = "") -> QLineEdit:
    le = QLineEdit()
    le.setPlaceholderText(placeholder)
    le.setFixedHeight(42)
    le.setStyleSheet(
        f"QLineEdit {{"
        f"  background: white; border: 1.5px solid {BORDER}; border-radius: 8px;"
        f"  padding: 0 14px; font-size: 13px; color: {TEXT_DARK};"
        f"}}"
        f"QLineEdit:focus {{ border: 2px solid {BLUE}; }}"
    )
    return le


def styled_password(placeholder: str = "") -> QLineEdit:
    le = styled_input(placeholder)
    le.setEchoMode(QLineEdit.EchoMode.Password)
    return le


def styled_textarea(placeholder: str = "") -> QTextEdit:
    te = QTextEdit()
    te.setPlaceholderText(placeholder)
    te.setStyleSheet(
        f"QTextEdit {{"
        f"  background: white; border: 1.5px solid {BORDER}; border-radius: 8px;"
        f"  padding: 8px 14px; font-size: 13px; color: {TEXT_DARK};"
        f"}}"
        f"QTextEdit:focus {{ border: 2px solid {BLUE}; }}"
    )
    return te


def heading(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"font-size: 22px; font-weight: 700; color: {TEXT_DARK}; background: transparent;"
    )
    return lbl


def subheading(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"font-size: 15px; font-weight: 600; color: {TEXT_DARK}; background: transparent;"
    )
    return lbl


def separator() -> QFrame:
    sep = QFrame()
    sep.setFrameShape(QFrame.Shape.HLine)
    sep.setFixedHeight(1)
    sep.setStyleSheet(f"background: {BORDER}; border: none;")
    return sep


def badge(text: str, bg: str, fg: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"background: {bg}; color: {fg}; border-radius: 5px;"
        f"padding: 2px 9px; font-size: 11px; font-weight: 600;"
    )
    lbl.setFixedHeight(22)
    return lbl


def available_badge()   -> QLabel: return badge("● Tersedia", GREEN_LIGHT,  "#065F46")
def unavailable_badge() -> QLabel: return badge("● Dipinjam", RED_LIGHT,    "#991B1B")
def ongoing_badge()     -> QLabel: return badge("● Berjalan", AMBER_LIGHT,  "#92400E")
def completed_badge()   -> QLabel: return badge("● Selesai",  GREEN_LIGHT,  "#065F46")


# ── White card — pure QSS, zero QGraphicsEffect ───────────────────────────────
class ShadowCard(QWidget):
    """White rounded card styled entirely via QSS.

    No paintEvent, no QGraphicsEffect — safe inside any QGraphicsOpacityEffect
    parent (e.g. MainWindow._stack). The subtle top-left/bottom-right border
    gradient simulates depth without touching the painter stack.
    """

    def __init__(self, radius: int = 14, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._apply_style(radius)

    def _apply_style(self, r: int):
        self.setStyleSheet(
            f"ShadowCard, QWidget[shadowCard='true'] {{"
            f"  background: {CARD_BG};"
            f"  border-radius: {r}px;"
            f"  border: 1px solid {BORDER};"
            f"}}"
        )
        # Fallback: direct object-level sheet so nested inheritance works
        self.setStyleSheet(
            f"background: {CARD_BG};"
            f"border-radius: {r}px;"
            f"border: 1px solid {BORDER};"
        )


# ── Slide-in toast notification ───────────────────────────────────────────────
class _Toast(QWidget):
    _STYLES = {
        "success": ("#065F46", "#D1FAE5", "✓"),
        "error":   ("#991B1B", "#FEE2E2", "✕"),
        "warning": ("#92400E", "#FEF3C7", "⚠"),
        "info":    ("#1E40AF", "#DBEAFE", "ℹ"),
    }

    def __init__(self, message: str, kind: str, parent: QWidget):
        super().__init__(parent)
        fg, bg, icon = self._STYLES.get(kind, self._STYLES["info"])
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setStyleSheet(
            f"background: {bg}; border-radius: 10px; border: 1.5px solid {fg}55;"
        )
        lay = QHBoxLayout(self)
        lay.setContentsMargins(14, 11, 14, 11)
        lay.setSpacing(10)

        lbl_i = QLabel(icon)
        lbl_i.setStyleSheet(f"color: {fg}; font-size: 15px; font-weight: 700; background: transparent;")
        lbl_m = QLabel(message)
        lbl_m.setStyleSheet(f"color: {fg}; font-size: 13px; font-weight: 500; background: transparent;")
        lbl_m.setWordWrap(True)
        lbl_m.setMaximumWidth(340)
        lay.addWidget(lbl_i)
        lay.addWidget(lbl_m, 1)

        self.adjustSize()
        self._show_animated(parent)
        QTimer.singleShot(3500, self._hide_animated)

    def _show_animated(self, parent: QWidget):
        w = max(300, self.sizeHint().width())
        h = max(50, self.sizeHint().height())
        self.setFixedSize(w, h)
        x = parent.width() - w - 20
        self.move(x, -h - 10)
        self.show()
        anim = QPropertyAnimation(self, b"pos", self)
        anim.setDuration(300)
        anim.setStartValue(QPoint(x, -h - 10))
        anim.setEndValue(QPoint(x, 16))
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()
        self._anim = anim

    def _hide_animated(self):
        if not self.isVisible():
            return
        start = self.pos()
        anim = QPropertyAnimation(self, b"pos", self)
        anim.setDuration(220)
        anim.setStartValue(start)
        anim.setEndValue(QPoint(start.x(), -self.height() - 10))
        anim.setEasingCurve(QEasingCurve.Type.InCubic)
        anim.finished.connect(self.close)
        anim.start()
        self._anim = anim


def show_toast(message: str, parent: QWidget, kind: str = "success") -> _Toast:
    return _Toast(message, kind, parent)


# ── Dialog helpers ────────────────────────────────────────────────────────────
def show_alert(title: str, message: str, parent=None):
    QMessageBox.information(parent, title, message)


def show_error(title: str, message: str, parent=None):
    QMessageBox.critical(parent, title, message)


def show_confirm(message: str, parent=None) -> bool:
    reply = QMessageBox.question(
        parent, "Konfirmasi", message,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    return reply == QMessageBox.StandardButton.Yes
