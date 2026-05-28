# core/ghost.py
# Ghost echo: replays a recorded movement path.

import pygame
from core.settings import (
    PLAYER_SIZE, COLOR_GHOST, COLOR_GLOW_GHOST,
    GHOST_SPAWN_DELAY, GHOST_TRAIL_LENGTH, RECORD_INTERVAL,
)


class Ghost:
    def __init__(self, recording):
        # Store copy to prevent reference bugs
        self.recording = recording.copy()
        self.recording_length = len(recording)
        self.frame_index = 0
        self.tick_counter = 0
        self.spawn_timer = 0.0
        self.alive = False
        self.trail = []  # last N positions for trail effect

    def update(self, dt):
        """Advance ghost replay by one tick."""
        # Spawn delay
        if not self.alive:
            self.spawn_timer += dt
            if self.spawn_timer >= GHOST_SPAWN_DELAY:
                self.alive = True

        # Advance frame index every RECORD_INTERVAL ticks (matching recording rate)
        self.tick_counter += 1
        if self.tick_counter % RECORD_INTERVAL == 0:
            if self.recording_length > 0:
                # Store current position in trail
                pos = self.recording[self.frame_index]
                self.trail.append(pos)
                if len(self.trail) > GHOST_TRAIL_LENGTH:
                    self.trail.pop(0)

                # Advance frame
                self.frame_index += 1
                if self.frame_index >= self.recording_length:
                    self.frame_index = 0  # loop

    @property
    def position(self):
        """Current position from recording."""
        if self.recording_length == 0:
            return (0, 0)
        return self.recording[self.frame_index]

    @property
    def rect(self):
        """Return pygame.Rect for collision."""
        x, y = self.position
        return pygame.Rect(int(x), int(y), PLAYER_SIZE, PLAYER_SIZE)

    def render(self, surface, offset=(0, 0)):
        """Render ghost with glow and trail. offset is for screen shake."""
        if self.recording_length == 0:
            return

        ox, oy = offset
        x, y = self.position
        x = int(x) + ox
        y = int(y) + oy

        # Trail (fading rectangles)
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(40 * (i + 1) / len(self.trail)) if self.trail else 0
            trail_surface = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
            trail_surface.fill((200, 50, 255, alpha))
            surface.blit(trail_surface, (int(tx) + ox, int(ty) + oy))

        # Glow
        glow_size = PLAYER_SIZE + 10
        glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        glow_surface.fill(COLOR_GLOW_GHOST)
        surface.blit(glow_surface, (x - 5, y - 5))

        # Body (dimmer if not alive yet)
        body_color = COLOR_GHOST if self.alive else (100, 30, 130)
        pygame.draw.rect(surface, body_color, (x, y, PLAYER_SIZE, PLAYER_SIZE))
