# levels/arena.py
# Arena class: background, grid, and border rendering.

import pygame
from core.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    COLOR_BG, COLOR_GRID,
    GRID_SIZE, COLOR_PLAYER,
)


class Arena:
    PADDING = 20  # pixels of padding from window edges

    def __init__(self):
        self.rect = pygame.Rect(
            self.PADDING,
            self.PADDING,
            WINDOW_WIDTH - self.PADDING * 2,
            WINDOW_HEIGHT - self.PADDING * 2,
        )

    def render(self, surface, offset=(0, 0)):
        """
        Draw the arena: background fill, grid lines, and border.
        - surface: target surface
        - offset: (x, y) camera offset tuple
        """
        ox, oy = offset

        # 1. Fill entire window with background color
        surface.fill(COLOR_BG)

        # 2. Draw vertical grid lines inside the arena
        x = self.rect.left
        while x <= self.rect.right:
            pygame.draw.line(
                surface, COLOR_GRID,
                (x + ox, self.rect.top + oy),
                (x + ox, self.rect.bottom + oy),
            )
            x += GRID_SIZE

        # 3. Draw horizontal grid lines inside the arena
        y = self.rect.top
        while y <= self.rect.bottom:
            pygame.draw.line(
                surface, COLOR_GRID,
                (self.rect.left + ox, y + oy),
                (self.rect.right + ox, y + oy),
            )
            y += GRID_SIZE

        # 4. Draw arena border (thin cyan outline)
        pygame.draw.rect(surface, COLOR_PLAYER, (
            self.rect.left + ox,
            self.rect.top + oy,
            self.rect.width,
            self.rect.height,
        ), width=2)
