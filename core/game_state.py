# core/game_state.py
# Simple enum for the four game states.

from enum import Enum


class GameState(Enum):
    MENU = 1
    PLAYING = 2
    DYING = 3
    GAME_OVER = 4
