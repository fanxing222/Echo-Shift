# core/player.py
# Player class with WASD movement, arena clamping, and neon glow rendering.

import pygame
from core.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    PLAYER_SIZE, PLAYER_SPEED,
    COLOR_PLAYER, COLOR_GLOW_PLAYER,
)
from core.utils import clamp


class Player:
    def __init__(self):
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.reset()

    def reset(self):
        """Reset player to the center of the screen."""
        self.x = (WINDOW_WIDTH - self.size) / 2.0
        self.y = (WINDOW_HEIGHT - self.size) / 2.0

    @property
    def rect(self):
        """Return a pygame.Rect at the player's current position."""
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    def update(self, dt, arena_rect):
        """
        Update player position based on WASD input.
        - dt: delta time in seconds
        - arena_rect: pygame.Rect defining the movement boundary
        Diagonal movement is normalized so it's not faster than cardinal.
        """
        keys = pygame.key.get_pressed()
        dx = 0.0
        dy = 0.0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1

        # Normalize diagonal so speed doesn't exceed PLAYER_SPEED
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt

        # Clamp to arena boundaries (player rect must stay inside arena)
        self.x = clamp(self.x, arena_rect.left, arena_rect.right - self.size)
        self.y = clamp(self.y, arena_rect.top, arena_rect.bottom - self.size)

    def render(self, surface, offset=(0, 0)):
        """
        Draw the player with a neon glow effect.
        - surface: target surface to draw on
        - offset: (x, y) camera offset tuple
        """
        ox, oy = offset
        draw_x = int(self.x) + ox
        draw_y = int(self.y) + oy

        # Glow: larger semi-transparent rect behind the player body
        glow_expand = 12  # pixels of glow around the player
        glow_surface = pygame.Surface(
            (self.size + glow_expand * 2, self.size + glow_expand * 2),
            pygame.SRCALPHA,
        )
        glow_surface.fill(COLOR_GLOW_PLAYER)
        surface.blit(glow_surface, (draw_x - glow_expand, draw_y - glow_expand))

        # Player body: solid neon cyan rect
        pygame.draw.rect(surface, COLOR_PLAYER, (draw_x, draw_y, self.size, self.size))
