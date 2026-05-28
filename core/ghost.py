# core/ghost.py
# Ghost echo: replays a segment of recorded movement path.

import pygame
from core.settings import (
    PLAYER_SIZE, COLOR_GHOST, COLOR_GLOW_GHOST,
    GHOST_SPAWN_DELAY, GHOST_TRAIL_LENGTH, RECORD_INTERVAL, FPS,
    GHOST_SEGMENT_DURATION,
)


class Ghost:
    def __init__(self, recording, segment_index=0):
        """Create a ghost that replays a specific segment of the recording.

        Args:
            recording: list of (x, y) positions recorded every RECORD_INTERVAL frames
            segment_index: which time segment to replay (0 = first segment, 1 = second, etc.)
        """
        self.recording = recording.copy()
        self.recording_length = len(recording)
        self.segment_index = segment_index
        self.spawn_timer = 0.0
        self.alive = False
        self.trail = []  # last N positions for trail effect

        # Calculate recording FPS
        self.recording_fps = FPS / RECORD_INTERVAL  # e.g., 60/2 = 30 fps

        # Calculate segment boundaries in frame indices
        frames_per_segment = int(GHOST_SEGMENT_DURATION * self.recording_fps)
        self.segment_start = segment_index * frames_per_segment
        self.segment_end = min(self.segment_start + frames_per_segment, self.recording_length)

        # If segment is out of range, wrap around
        if self.segment_start >= self.recording_length:
            self.segment_start = self.segment_start % max(1, self.recording_length)
            self.segment_end = min(self.segment_start + frames_per_segment, self.recording_length)

        # Duration of this segment in seconds
        self.segment_frames = self.segment_end - self.segment_start
        self.segment_duration = self.segment_frames / self.recording_fps if self.recording_fps > 0 else 0

    def _get_position_at_time(self, game_time):
        """Get position within the assigned segment based on game time.

        Returns (x, y) or None if segment is invalid.
        """
        if self.recording_length == 0 or self.segment_frames == 0:
            return None

        # Calculate time within the segment (loops automatically)
        segment_time = game_time % self.segment_duration if self.segment_duration > 0 else 0

        # Convert to frame index within segment
        frame_float = segment_time * self.recording_fps
        frame_int = int(frame_float)
        frame_frac = frame_float - frame_int

        # Wrap within segment bounds
        frame_in_segment = frame_int % self.segment_frames

        # Get absolute index in recording
        abs_index = self.segment_start + frame_in_segment

        # Safety check
        if abs_index >= self.recording_length:
            abs_index = abs_index % self.recording_length

        # If at exact frame or last frame in segment, no interpolation
        if frame_frac < 0.001 or frame_in_segment >= self.segment_frames - 1:
            return self.recording[abs_index]

        # Linear interpolation with next frame
        next_index = self.segment_start + ((frame_in_segment + 1) % self.segment_frames)
        if next_index >= self.recording_length:
            next_index = next_index % self.recording_length

        x1, y1 = self.recording[abs_index]
        x2, y2 = self.recording[next_index]
        x = x1 + (x2 - x1) * frame_frac
        y = y1 + (y2 - y1) * frame_frac
        return (x, y)

    def update(self, dt, game_time):
        """Update ghost state based on current game time.

        Args:
            dt: delta time in seconds
            game_time: current game time in seconds
        """
        # Spawn delay (uses real time, not game time)
        if not self.alive:
            self.spawn_timer += dt
            if self.spawn_timer >= GHOST_SPAWN_DELAY:
                self.alive = True

        # Update trail with position from segment
        pos = self._get_position_at_time(game_time)
        if pos is not None:
            self.trail.append(pos)
            if len(self.trail) > GHOST_TRAIL_LENGTH:
                self.trail.pop(0)

    def get_position(self, game_time):
        """Get current position for rendering and collision.

        Args:
            game_time: current game time in seconds

        Returns:
            (x, y) tuple, or first recorded position if invalid
        """
        pos = self._get_position_at_time(game_time)
        if pos is None:
            if self.recording_length > 0:
                return self.recording[0]
            return (0, 0)
        return pos

    @property
    def rect(self):
        """Return pygame.Rect at current trail position for collision."""
        if self.trail:
            x, y = self.trail[-1]
        elif self.recording_length > 0:
            x, y = self.recording[0]
        else:
            x, y = (0, 0)
        return pygame.Rect(int(x), int(y), PLAYER_SIZE, PLAYER_SIZE)

    def render(self, surface, offset=(0, 0), game_time=0.0):
        """Render ghost with glow and trail.

        Args:
            surface: target surface
            offset: (x, y) camera offset for screen shake
            game_time: current game time for position calculation
        """
        if self.recording_length == 0:
            return

        ox, oy = offset
        x, y = self.get_position(game_time)
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
