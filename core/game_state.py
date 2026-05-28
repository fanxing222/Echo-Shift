# core/game_state.py
# Game states enum.

from enum import Enum


class GameState(Enum):
    MENU = 1
    PLAYING = 2
    DYING = 3
    GAME_OVER = 4
    PAUSED = 5
