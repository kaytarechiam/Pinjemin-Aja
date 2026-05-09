"""Shared styling constants and widget factories for Pinjemin Aja! (PyQt6)."""
from __future__ import annotations
import os
from typing import Optional

from PyQt6.QtWidgets import (
    QLabel, QPushButton, QLineEdit, QTextEdit, QFrame,
    QMessageBox, QWidget, QHBoxLayout, QSizePolicy
)
from PyQt6.QtGui import QFont, QPixmap, QColor
from PyQt6.QtCore import Qt

# ── Colour palette ────────────────────────────────────────────────────────────
BLUE        = "#3D5AF1"
BLUE_DARK   = "#2D46D6"
BLUE_LIGHT  = "#EEF1FF"
LIGHT_BG    = "#F7F8FC"
BORDER      = "#E8EAF0"
TEXT_DARK   = "#1A1D2E"
TEXT_MID    = "#4B5563"
TEXT_GRAY   = "#9CA3AF"
WHITE       = "#FFFFFF"
GREEN       = "#10B981"
GREEN_LIGHT = "#D1FAE5"
RED         = "#EF4444"
RED_LIGHT   = "#FEE2E2"
YELLOW_LIGHT= "#FEF3C7"
YELLOW_DARK = "#92400E"

IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "images")

# ── Item → image filename map ─────────────────────────────────────────────────
_ITEM_IMAGE_MAP = {
    "Waffle Maker":         "waffle_maker.jpg",
    "Slow Juicer":          "slow_juicer.jpg",
    "High-Pressure Washer": "pressure_washer.jpg",
    "Wet & Dry Vacuum":     "vacuum_cleaner.jpg",
    "Cordless Power Drill": "power_drill.jpg",
    "Step Ladder":          "step_ladder.jpg",
    "Electric Sander":      "electric_sander.jpg",
    "Projector HD":         "projector.jpg",
    "Food Processor":       "food_processor.jpg",
    "Ice Cream Maker":      "ice_cream_maker.jpg",
    "Jumbo Rice Cooker":    "rice_cooker.jpg",
    "Artisan Stand Mixer":  "stand_mixer.jpg",
    "Foldable Hand Truck":  "hand_truck.jpg",
    "Garden Hose Set":      "garden_hose.jpg",
    "Electric Lawn Mower":  "lawn_mower.jpg",
    "Portable Blower":      "portable_blower.jpg",
}

def get_item_pixmap(nama_alat: str, w: int = 300, h: int = 180) -> Optional[QPixmap]:
    fname = _ITEM_IMAGE_MAP.get(nama_alat)
    if not fname:
        return None
    path = os.path.join(IMAGES_DIR, fname)
    if not os.path.exists(path):
        return None
    pm = QPixmap(path)
    if pm.isNull():
        return None
    return pm.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                     Qt.TransformationMode.SmoothTransformation)

# ── Category helpers ──────────────────────────────────────────────────────────
def category_color(kategori: str) -> str:
    return {
        "Kitchen":     "#FFF7ED",
        "Tools":       "#EFF6FF",
        "Cleaning":    "#F0FDF4",
        "Electronics": "#FAF5FF",
        "Gardening":   "#ECFDF5",
    }.get(kategori, LIGHT_BG)

def category_emoji(kategori: str) -> str:
    return {
        "Kitchen":     "🍳",
        "Tools":       "🔧",
        "Cleaning":    "🧹",
        "Electronics": "💡",
        "Gardening":   "🌱",
    }.get(kategori, "📦")

# ── Formatting ────────────────────────────────────────────────────────────────
def format_rupiah(amount: float) -> str:
    return f"Rp {amount:,.0f}".replace(",", ".")

# ── Stylesheet helpers ────────────────────────────────────────────────────────
def card_style() -> str:
    return (f"background: {WHITE}; border-radius: 12px;"
            f"border: 1px solid {BORDER};")

def input_style() -> str:
    return (f"background: {WHITE}; border: 1.5px solid {BORDER};"
            f"border-radius: 8px; padding: 8px 12px; font-size: 13px; color: {TEXT_DARK};")

def primary_btn_style() -> str:
    return (f"background: {BLUE}; color: white; border-radius: 8px;"
            f"padding: 10px 20px; font-size: 13px; font-weight: 600; border: none;")

def outline_btn_style() -> str:
    return (f"background: white; color: {BLUE}; border-radius: 8px;"
            f"border: 1.5px solid {BLUE}; padding: 9px 20px; font-size: 13px; font-weight: 600;")

def danger_btn_style() -> str:
    return (f"background: {RED}; color: white; border-radius: 8px;"
            f"padding: 8px 16px; font-size: 13px; font-weight: 600; border: none;")

# ── Widget factories ──────────────────────────────────────────────────────────
def heading(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(f"font-size: 22px; font-weight: 700; color: {TEXT_DARK}; background: transparent;")
    return lbl

def subheading(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_DARK}; background: transparent;")
    return lbl

def label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(f"font-size: 13px; color: {TEXT_DARK}; background: transparent;")
    return lbl

def secondary_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(f"font-size: 12px; color: {TEXT_GRAY}; background: transparent;")
    return lbl

def primary_button(text: str) -> QPushButton:
    btn = QPushButton(text)
    btn.setStyleSheet(primary_btn_style())
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setFixedHeight(42)
    return btn

def outline_button(text: str) -> QPushButton:
    btn = QPushButton(text)
    btn.setStyleSheet(outline_btn_style())
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setFixedHeight(42)
    return btn

def danger_button(text: str) -> QPushButton:
    btn = QPushButton(text)
    btn.setStyleSheet(danger_btn_style())
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setFixedHeight(38)
    return btn

def styled_input(placeholder: str = "") -> QLineEdit:
    inp = QLineEdit()
    inp.setPlaceholderText(placeholder)
    inp.setStyleSheet(input_style())
    inp.setFixedHeight(42)
    return inp

def styled_password(placeholder: str = "") -> QLineEdit:
    inp = styled_input(placeholder)
    inp.setEchoMode(QLineEdit.EchoMode.Password)
    return inp

def styled_textarea(placeholder: str = "") -> QTextEdit:
    ta = QTextEdit()
    ta.setPlaceholderText(placeholder)
    ta.setStyleSheet(input_style())
    return ta

def separator() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setStyleSheet(f"color: {BORDER};")
    return line

def badge(text: str, bg: str, fg: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"background: {bg}; color: {fg}; border-radius: 10px;"
        f"padding: 2px 10px; font-size: 10px; font-weight: 600;"
    )
    lbl.setFixedHeight(22)
    return lbl

def available_badge()   -> QLabel: return badge("TERSEDIA",       GREEN_LIGHT, "#065F46")
def unavailable_badge() -> QLabel: return badge("SEDANG DIPINJAM",RED_LIGHT,   "#991B1B")
def ongoing_badge()     -> QLabel: return badge("BERJALAN",       YELLOW_LIGHT,YELLOW_DARK)
def completed_badge()   -> QLabel: return badge("SELESAI",        GREEN_LIGHT, "#065F46")

# ── Dialogs ───────────────────────────────────────────────────────────────────
def show_alert(title: str, message: str, parent=None):
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setIcon(QMessageBox.Icon.Information)
    msg.exec()

def show_error(message: str, parent=None):
    msg = QMessageBox(parent)
    msg.setWindowTitle("Error")
    msg.setText(message)
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.exec()

def show_confirm(message: str, parent=None) -> bool:
    msg = QMessageBox(parent)
    msg.setWindowTitle("Konfirmasi")
    msg.setText(message)
    msg.setStandardButtons(
        QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
    )
    msg.setIcon(QMessageBox.Icon.Question)
    return msg.exec() == QMessageBox.StandardButton.Ok
