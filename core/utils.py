# core/utils.py
# Small helper functions used across the game.

import pygame


def draw_text(surface, text, x, y, font, color=(255, 255, 255), center=False):
    """Draw text on the surface at (x, y). If center=True, center the text at that point."""
    text_surface = font.render(text, True, color)
    if center:
        rect = text_surface.get_rect(center=(x, y))
        surface.blit(text_surface, rect)
    else:
        surface.blit(text_surface, (x, y))


def clamp(value, min_val, max_val):
    """Clamp value between min_val and max_val."""
    return max(min_val, min(value, max_val))


def load_font(size):
    """Load the default pygame font at the given size."""
    return pygame.font.Font(None, size)
