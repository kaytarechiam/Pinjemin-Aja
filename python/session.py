from __future__ import annotations
from typing import Optional
from models.pengguna import Pengguna


class Session:
    """Singleton session manager — tracks currently logged-in user."""
    _current_user: Optional[Pengguna] = None

    @classmethod
    def login(cls, pengguna: Pengguna):
        cls._current_user = pengguna

    @classmethod
    def logout(cls):
        cls._current_user = None

    @classmethod
    def get_current_user(cls) -> Optional[Pengguna]:
        return cls._current_user

    @classmethod
    def is_logged_in(cls) -> bool:
        return cls._current_user is not None
