# Echo Shift Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a minimalist sci-fi survival arcade game where the player's past movements become ghost enemies.

**Architecture:** Frame-by-frame position recording with deterministic ghost replay. Four game states (MENU, PLAYING, DYING, GAME_OVER) managed in main.py. Modular file structure with player, ghost, recorder, and arena separated.

**Tech Stack:** Python 3.10+, pygame-ce

---

## File Structure

```
Echo Shift/
├── main.py                  # Entry point, game loop, state machine
├── requirements.txt         # pygame-ce dependency
├── README.md                # Project documentation
├── .gitignore               # Python/pygame gitignore
├── assets/                  # Future: fonts, sounds
├── core/
│   ├── __init__.py
│   ├── settings.py          # All constants
│   ├── game_state.py        # GameState enum
│   ├── player.py            # Player class
│   ├── ghost.py             # Ghost class
│   ├── recorder.py          # RunRecorder class
│   ├── collision.py         # Collision helpers
│   └── utils.py             # draw_text, clamp, load_font
├── levels/
│   ├── __init__.py
│   └── arena.py             # Arena boundaries, grid
```

---

## Task 1: Project Scaffolding

**Files:**
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `README.md`
- Create: `core/__init__.py`
- Create: `levels/__init__.py`
- Create: `assets/` directory

- [ ] **Step 1: Create requirements.txt**

```
pygame-ce>=2.5.0
```

- [ ] **Step 2: Create .gitignore**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Game assets (large files)
assets/*.wav
assets/*.mp3
assets/*.ogg
```

- [ ] **Step 3: Create README.md**

```markdown
# Echo Shift

A minimalist sci-fi survival arcade game where your past actions become future enemies.

## How to Play

- **WASD** — Move
- **SPACE** — Start / Restart
- **ESC** — Quit

## Concept

Each run records your movement. When you die, that recording becomes a "Ghost Echo" that replays your exact path in all future runs. Survive as long as possible while the arena fills with echoes of your past behavior.

## Setup

```bash
pip install -r requirements.txt
python main.py
```

## Project Structure

```
core/           — Game logic (player, ghosts, recorder)
levels/         — Arena and map data
assets/         — Fonts, sounds (future)
main.py         — Entry point
```
```

- [ ] **Step 4: Create core/__init__.py and levels/__init__.py**

```python
# core/__init__.py
```

```python
# levels/__init__.py
```

- [ ] **Step 5: Create assets directory**

```bash
mkdir -p assets
```

- [ ] **Step 6: Verify project structure**

Run: `ls -R` from project root
Expected: All files and directories exist

---

## Task 2: Settings and Constants

**Files:**
- Create: `core/settings.py`

- [ ] **Step 1: Create settings.py with all constants**

```python
# core/settings.py
# All game constants in one place for easy tuning.

# Window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
TITLE = "Echo Shift"

# Colors (R, G, B) or (R, G, B, A) for transparency
COLOR_BG = (10, 10, 10)
COLOR_PLAYER = (0, 255, 200)
COLOR_GHOST = (200, 50, 255)
COLOR_GLOW_PLAYER = (0, 255, 200, 40)
COLOR_GLOW_GHOST = (200, 50, 255, 30)
COLOR_TEXT = (255, 255, 255)
COLOR_TEXT_DIM = (150, 150, 150)
COLOR_ACCENT = (255, 50, 80)
COLOR_GRID = (30, 30, 30)
COLOR_OVERLAY = (0, 0, 0, 180)

# Player
PLAYER_SIZE = 32
PLAYER_SPEED = 320  # pixels per second

# Ghost
GHOST_SPAWN_DELAY = 1.0  # seconds before ghost becomes lethal
GHOST_TRAIL_LENGTH = 5   # number of trail positions to keep

# Timing
DEATH_FREEZE_TIME = 0.3     # seconds of freeze-frame on death
SCREEN_SHAKE_DURATION = 0.2 # seconds of shake after death
SCREEN_SHAKE_INTENSITY = 4  # max pixel offset for shake

# Arena
GRID_SIZE = 40  # pixels between grid lines

# Recording
RECORD_INTERVAL = 2  # record every N frames (2 = 30 FPS recording)
MAX_RECORDING_FRAMES = 60 * 300  # 5 minutes at 60 FPS

# Debug
DEBUG = False
```

- [ ] **Step 2: Verify import works**

Run: `python -c "from core.settings import *; print(WINDOW_WIDTH)"`
Expected: `1280`

---

## Task 3: Game State Enum

**Files:**
- Create: `core/game_state.py`

- [ ] **Step 1: Create game_state.py**

```python
# core/game_state.py
# Simple enum for the four game states.

from enum import Enum


class GameState(Enum):
    MENU = 1
    PLAYING = 2
    DYING = 3
    GAME_OVER = 4
```

- [ ] **Step 2: Verify import works**

Run: `python -c "from core.game_state import GameState; print(GameState.PLAYING)"`
Expected: `GameState.PLAYING`

---

## Task 4: Utility Functions

**Files:**
- Create: `core/utils.py`

- [ ] **Step 1: Create utils.py**

```python
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
```

- [ ] **Step 2: Verify import works**

Run: `python -c "from core.utils import draw_text, clamp; print(clamp(150, 0, 100))"`
Expected: `100`

---

## Task 5: Player Class

**Files:**
- Create: `core/player.py`

- [ ] **Step 1: Create player.py**

```python
# core/player.py
# Player character: handles movement, position, and rendering.

import pygame
from core.settings import (
    PLAYER_SIZE, PLAYER_SPEED, COLOR_PLAYER, COLOR_GLOW_PLAYER,
    WINDOW_WIDTH, WINDOW_HEIGHT,
)
from core.utils import clamp


class Player:
    def __init__(self):
        # Start at center of screen
        self.x = WINDOW_WIDTH / 2 - PLAYER_SIZE / 2
        self.y = WINDOW_HEIGHT / 2 - PLAYER_SIZE / 2
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED

    def reset(self):
        """Reset player to center position."""
        self.x = WINDOW_WIDTH / 2 - PLAYER_SIZE / 2
        self.y = WINDOW_HEIGHT / 2 - PLAYER_SIZE / 2

    def update(self, dt, arena_rect):
        """Update player position based on input. dt is delta time in seconds."""
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1/sqrt(2)
            dy *= 0.7071

        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt

        # Clamp to arena boundaries
        self.x = clamp(self.x, arena_rect.left, arena_rect.right - self.size)
        self.y = clamp(self.y, arena_rect.top, arena_rect.bottom - self.size)

    @property
    def rect(self):
        """Return pygame.Rect for collision detection."""
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    def render(self, surface, offset=(0, 0)):
        """Render player with glow effect. offset is for screen shake."""
        ox, oy = offset
        x = int(self.x) + ox
        y = int(self.y) + oy

        # Glow (larger transparent rect behind)
        glow_size = self.size + 12
        glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        glow_surface.fill(COLOR_GLOW_PLAYER)
        surface.blit(glow_surface, (x - 6, y - 6))

        # Body
        pygame.draw.rect(surface, COLOR_PLAYER, (x, y, self.size, self.size))
```

- [ ] **Step 2: Verify import works**

Run: `python -c "from core.player import Player; p = Player(); print(p.rect)"`
Expected: `<rect(...)>` showing centered position

---

## Task 6: Arena Class

**Files:**
- Create: `levels/arena.py`

- [ ] **Step 1: Create arena.py**

```python
# levels/arena.py
# Arena boundaries and grid rendering.

import pygame
from core.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, COLOR_GRID, COLOR_BG,
)


class Arena:
    def __init__(self):
        # Arena fills the whole window with a small padding
        padding = 20
        self.rect = pygame.Rect(
            padding, padding,
            WINDOW_WIDTH - padding * 2,
            WINDOW_HEIGHT - padding * 2,
        )

    def render(self, surface):
        """Render background and grid lines."""
        # Background
        surface.fill(COLOR_BG)

        # Grid lines (vertical)
        for x in range(self.rect.left, self.rect.right, GRID_SIZE):
            pygame.draw.line(surface, COLOR_GRID, (x, self.rect.top), (x, self.rect.bottom))

        # Grid lines (horizontal)
        for y in range(self.rect.top, self.rect.bottom, GRID_SIZE):
            pygame.draw.line(surface, COLOR_GRID, (self.rect.left, y), (self.rect.right, y))

        # Arena border
        pygame.draw.rect(surface, COLOR_GRID, self.rect, 2)
```

- [ ] **Step 2: Verify import works**

Run: `python -c "from levels.arena import Arena; a = Arena(); print(a.rect)"`
Expected: `<rect(20, 20, 1240, 680)>`

---

## Task 7: Basic Game Window (main.py Phase 1)

**Files:**
- Create: `main.py`

- [ ] **Step 1: Create main.py with game loop and player movement**

```python
# main.py
# Echo Shift — main entry point and game loop.

import pygame
import sys

from core.settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TITLE, COLOR_TEXT
from core.game_state import GameState
from core.player import Player
from core.utils import draw_text, load_font


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Fonts
    font_large = load_font(72)
    font_medium = load_font(36)
    font_small = load_font(24)

    # Game objects
    player = Player()

    # State
    state = GameState.MENU

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    if state == GameState.MENU:
                        state = GameState.PLAYING
                    elif state == GameState.GAME_OVER:
                        player.reset()
                        state = GameState.PLAYING

        # --- Update ---
        if state == GameState.PLAYING:
            # Temporary arena rect until we use the Arena class
            arena_rect = pygame.Rect(20, 20, WINDOW_WIDTH - 40, WINDOW_HEIGHT - 40)
            player.update(dt, arena_rect)

        # --- Render ---
        screen.fill((10, 10, 10))

        if state == GameState.MENU:
            draw_text(screen, "ECHO SHIFT", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3,
                      font_large, (0, 255, 200), center=True)
            draw_text(screen, "Press SPACE to Start", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                      font_medium, COLOR_TEXT, center=True)

        elif state == GameState.PLAYING:
            # Temporary grid rendering
            for x in range(20, WINDOW_WIDTH - 20, 40):
                pygame.draw.line(screen, (30, 30, 30), (x, 20), (x, WINDOW_HEIGHT - 20))
            for y in range(20, WINDOW_HEIGHT - 20, 40):
                pygame.draw.line(screen, (30, 30, 30), (20, y), (WINDOW_WIDTH - 20, y))
            player.render(screen)

        elif state == GameState.GAME_OVER:
            draw_text(screen, "GAME OVER", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3,
                      font_large, (255, 50, 80), center=True)
            draw_text(screen, "Press SPACE to restart", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                      font_medium, COLOR_TEXT, center=True)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the game and verify**

Run: `python main.py`
Expected: Window opens, MENU state shows title, SPACE starts game, player moves with WASD, ESC quits

- [ ] **Step 3: Commit Phase 1**

```bash
git add -A
git commit -m "feat: project scaffolding, player movement, basic game loop"
```

---

## Task 8: RunRecorder

**Files:**
- Create: `core/recorder.py`

- [ ] **Step 1: Create recorder.py**

```python
# core/recorder.py
# Records player positions each frame for ghost replay.

from core.settings import MAX_RECORDING_FRAMES, RECORD_INTERVAL


class RunRecorder:
    def __init__(self):
        self.positions = []
        self.frame_counter = 0

    def record(self, x, y):
        """Record position if on the right frame interval."""
        self.frame_counter += 1
        if self.frame_counter % RECORD_INTERVAL == 0:
            if len(self.positions) < MAX_RECORDING_FRAMES:
                self.positions.append((x, y))

    def get_recording(self):
        """Return the recorded positions list."""
        return self.positions.copy()

    def reset(self):
        """Clear recording for a new run."""
        self.positions = []
        self.frame_counter = 0

    def is_full(self):
        """Check if recording has reached max length."""
        return len(self.positions) >= MAX_RECORDING_FRAMES

    @property
    def length(self):
        """Number of recorded positions."""
        return len(self.positions)
```

- [ ] **Step 2: Verify import works**

Run: `python -c "from core.recorder import RunRecorder; r = RunRecorder(); r.record(10, 20); print(r.get_recording())"`
Expected: `[(10, 20)]`

---

## Task 9: Ghost Class

**Files:**
- Create: `core/ghost.py`

- [ ] **Step 1: Create ghost.py**

```python
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
```

- [ ] **Step 2: Verify import works**

Run: `python -c "from core.ghost import Ghost; g = Ghost([(10,20),(30,40)]); print(g.position)"`
Expected: `(10, 20)`

---

## Task 10: Collision Helper

**Files:**
- Create: `core/collision.py`

- [ ] **Step 1: Create collision.py**

```python
# core/collision.py
# Collision detection between player and ghosts.


def check_player_ghost_collision(player, ghosts):
    """Check if player collides with any alive ghost. Returns True on collision."""
    for ghost in ghosts:
        if ghost.alive and player.rect.colliderect(ghost.rect):
            return True
    return False
```

- [ ] **Step 2: Verify import works**

Run: `python -c "from core.collision import check_player_ghost_collision; print(check_player_ghost_collision.__name__)"`
Expected: `check_player_ghost_collision`

---

## Task 11: Ghost Replay Integration (main.py Phase 2)

**Files:**
- Modify: `main.py`

- [ ] **Step 1: Update main.py with recorder and ghost system**

```python
# main.py
# Echo Shift — main entry point and game loop.

import pygame
import sys
import random

from core.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TITLE, COLOR_TEXT, COLOR_TEXT_DIM,
    COLOR_ACCENT, COLOR_PLAYER, COLOR_BG,
    DEATH_FREEZE_TIME, SCREEN_SHAKE_DURATION, SCREEN_SHAKE_INTENSITY,
    DEBUG,
)
from core.game_state import GameState
from core.player import Player
from core.ghost import Ghost
from core.recorder import RunRecorder
from core.collision import check_player_ghost_collision
from core.utils import draw_text, load_font
from levels.arena import Arena


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Fonts
    font_large = load_font(72)
    font_medium = load_font(36)
    font_small = load_font(24)

    # Game objects
    player = Player()
    arena = Arena()
    recorder = RunRecorder()

    # Ghost list persists across runs
    ghosts = []

    # State
    state = GameState.MENU
    score_timer = 0.0
    best_score = 0.0
    death_timer = 0.0
    recording_saved = False

    # Screen shake
    shake_timer = 0.0
    shake_offset = (0, 0)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    if state == GameState.MENU:
                        # Start first run
                        recorder.reset()
                        score_timer = 0.0
                        recording_saved = False
                        state = GameState.PLAYING
                    elif state == GameState.GAME_OVER:
                        # Start new run
                        player.reset()
                        recorder.reset()
                        score_timer = 0.0
                        recording_saved = False
                        # Reset all ghosts to frame 0
                        for ghost in ghosts:
                            ghost.frame_index = 0
                            ghost.tick_counter = 0
                            ghost.spawn_timer = 0.0
                            ghost.alive = False
                            ghost.trail = []
                        state = GameState.PLAYING

        # --- Update ---
        if state == GameState.PLAYING:
            player.update(dt, arena.rect)
            recorder.record(player.x, player.y)

            # Update ghosts
            for ghost in ghosts:
                ghost.update(dt)

            # Check collision
            if check_player_ghost_collision(player, ghosts):
                state = GameState.DYING
                death_timer = DEATH_FREEZE_TIME
                shake_timer = SCREEN_SHAKE_DURATION

            score_timer += dt

        elif state == GameState.DYING:
            death_timer -= dt
            shake_timer -= dt

            # Save recording once
            if not recording_saved:
                recording = recorder.get_recording()
                if len(recording) > 10:  # ignore very short recordings
                    ghosts.append(Ghost(recording))
                recording_saved = True

            if death_timer <= 0:
                # Update best score
                if score_timer > best_score:
                    best_score = score_timer
                state = GameState.GAME_OVER

        # Screen shake
        if shake_timer > 0:
            shake_offset = (
                random.randint(-SCREEN_SHAKE_INTENSITY, SCREEN_SHAKE_INTENSITY),
                random.randint(-SCREEN_SHAKE_INTENSITY, SCREEN_SHAKE_INTENSITY),
            )
        else:
            shake_offset = (0, 0)

        # --- Render ---
        arena.render(screen)

        if state == GameState.MENU:
            draw_text(screen, "ECHO SHIFT", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3,
                      font_large, COLOR_PLAYER, center=True)
            draw_text(screen, "Press SPACE to Start", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                      font_medium, COLOR_TEXT, center=True)

        elif state in (GameState.PLAYING, GameState.DYING, GameState.GAME_OVER):
            # Render ghosts
            for ghost in ghosts:
                ghost.render(screen, shake_offset)

            # Render player (skip flash during DYING)
            if state != GameState.DYING or int(death_timer * 20) % 2 == 0:
                player.render(screen, shake_offset)

            # HUD
            draw_text(screen, f"Time: {score_timer:.1f}s", 30, 20, font_small, COLOR_TEXT)
            draw_text(screen, f"Ghosts: {len(ghosts)}", 30, 50, font_small, COLOR_TEXT_DIM)
            if best_score > 0:
                draw_text(screen, f"Best: {best_score:.1f}s", 30, 80, font_small, COLOR_TEXT_DIM)

            # Death flash
            if state == GameState.DYING:
                flash_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                flash_alpha = int(255 * (death_timer / DEATH_FREEZE_TIME))
                flash_surface.fill((255, 255, 255, min(flash_alpha, 100)))
                screen.blit(flash_surface, (0, 0))

            # Game over overlay
            if state == GameState.GAME_OVER:
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))

                draw_text(screen, "GAME OVER", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4,
                          font_large, COLOR_ACCENT, center=True)
                draw_text(screen, f"Time Survived: {score_timer:.1f}s",
                          WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40,
                          font_medium, COLOR_TEXT, center=True)
                draw_text(screen, f"Ghosts Created: {len(ghosts)}",
                          WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                          font_medium, COLOR_TEXT, center=True)
                if best_score > 0:
                    draw_text(screen, f"Best Time: {best_score:.1f}s",
                              WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40,
                              font_medium, COLOR_TEXT_DIM, center=True)
                draw_text(screen, "Press SPACE to restart",
                          WINDOW_WIDTH // 2, WINDOW_HEIGHT * 3 // 4,
                          font_medium, COLOR_TEXT, center=True)

        # Debug overlay
        if DEBUG:
            fps_text = f"FPS: {clock.get_fps():.0f}"
            draw_text(screen, fps_text, WINDOW_WIDTH - 120, 20, font_small, COLOR_PLAYER)
            draw_text(screen, f"Recorder: {recorder.length}", WINDOW_WIDTH - 120, 50,
                      font_small, COLOR_TEXT_DIM)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the game and verify full gameplay loop**

Run: `python main.py`
Expected:
- MENU: title screen, SPACE starts
- PLAYING: player moves, score counts up
- Die by waiting (no ghosts yet, so start a run, die manually by adding a test collision, or just verify movement works)
- GAME_OVER: shows stats, SPACE restarts
- Second run: ghost from first run appears after 1s delay

- [ ] **Step 3: Commit Phase 2**

```bash
git add -A
git commit -m "feat: ghost recording, replay, collision, death flow, full game loop"
```

---

## Task 12: Polish and Final Verification

**Files:**
- Modify: `main.py` (if needed)
- Modify: any files needing fixes

- [ ] **Step 1: Run full gameplay test**

1. Start game → MENU shows
2. SPACE → PLAYING, player moves with WASD
3. Score counts up, HUD visible
4. Let timer run for a few seconds, then restart (for testing, temporarily lower GHOST_SPAWN_DELAY or add a key to self-destruct)
5. GAME_OVER shows time, ghost count
6. SPACE → new run with ghost visible
7. Ghost spawns after 1 second, replays path
8. Touch ghost → DYING (flash + shake) → GAME_OVER
9. Repeat several times, verify ghosts accumulate

- [ ] **Step 2: Verify all states work correctly**

- MENU: renders correctly, SPACE transitions
- PLAYING: movement, recording, ghosts, collision all work
- DYING: freeze-frame, flash, shake, recording saved once
- GAME_OVER: overlay, stats, SPACE restarts

- [ ] **Step 3: Final commit**

```bash
git add -A
git commit -m "feat: complete Echo Shift game with ghost replay system"
```

---

## Summary

| Task | Description | Files |
|------|-------------|-------|
| 1 | Project scaffolding | requirements.txt, .gitignore, README.md, __init__.py |
| 2 | Settings | core/settings.py |
| 3 | Game state enum | core/game_state.py |
| 4 | Utilities | core/utils.py |
| 5 | Player | core/player.py |
| 6 | Arena | levels/arena.py |
| 7 | Basic window | main.py (Phase 1) |
| 8 | Recorder | core/recorder.py |
| 9 | Ghost | core/ghost.py |
| 10 | Collision | core/collision.py |
| 11 | Full integration | main.py (Phase 2) |
| 12 | Polish & verify | All files |
