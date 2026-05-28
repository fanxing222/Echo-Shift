# Echo Shift — Design Specification

**Date:** 2026-05-28
**Status:** Approved
**Framework:** pygame-ce
**Target:** Desktop + Browser (pygbag)

---

## 1. Game Concept

Echo Shift is a minimalist sci-fi survival arcade game where the player's past actions become future enemies.

**Core mechanic:** Each run records the player's movement. When the player dies, that recording becomes a "Ghost Echo" that replays the same path in all future runs. Over time, the arena fills with ghosts of the player's past behavior, creating increasing difficulty.

**Genre:** Survival arcade / time-loop mechanic
**Visual style:** Minimalist neon sci-fi — dark background, glowing entities, semi-transparent ghosts

---

## 2. Gameplay Rules

### Player
- Moves with WASD keys
- 32×32 pixel rectangle
- Neon cyan-green color with glow effect
- Cannot leave arena boundaries

### Ghosts
- Replay recorded positions exactly (frame-by-frame)
- Loop their recording continuously
- 32×32 pixel rectangle, semi-transparent purple/red
- 1-second spawn delay before becoming lethal
- Can overlap each other — no ghost-vs-ghost collision
- Only lethal to the player

### Death
- Player touching any alive ghost = instant death
- Triggers DYING state (0.3s freeze-frame with effects)
- Then transitions to GAME_OVER

### Scoring
- Primary: survival time in seconds
- Secondary: current ghost count
- Best score persists in memory (resets on app close)

### Restart
- Player presses SPACE to restart
- New run starts with all previous ghosts + the new one
- Player position reset, score reset, recorder reset
- Ghosts list and best score NOT reset

---

## 3. Game States

```
MENU ──(SPACE)──▶ PLAYING ──(collision)──▶ DYING ──(0.3s)──▶ GAME_OVER
  ▲                                                            │
  └──────────────────────────(SPACE)───────────────────────────┘
```

### MENU
- Display: title "ECHO SHIFT" with glow, "Press SPACE to Start"
- No game logic running

### PLAYING
- Player movement, ghost updates, recording, collision detection, score timer
- HUD: current time, ghost count, best score

### DYING
- Gameplay frozen
- Death effects: screen flash, screen shake
- Duration: 0.3 seconds
- Recording saved once (flag prevents duplicate save)
- New ghost created and appended to list

### GAME_OVER
- Display: final time, ghost count, best score, restart instruction
- Semi-transparent dark overlay
- Wait for SPACE to restart

---

## 4. Architecture

### Project Structure

```
Echo Shift/
├── main.py              # Entry point, game loop, state machine
├── requirements.txt
├── README.md
├── .gitignore
├── assets/              # Future: fonts, sounds
├── core/
│   ├── __init__.py
│   ├── settings.py      # All constants
│   ├── player.py        # Player class
│   ├── ghost.py         # Ghost class
│   ├── recorder.py      # RunRecorder class
│   ├── collision.py     # Collision helpers
│   ├── game_state.py    # GameState enum
│   └── utils.py         # draw_text, clamp, load_font
├── levels/
│   ├── __init__.py
│   └── arena.py         # Arena boundaries, grid, obstacles
```

### File Responsibilities

| File | Owns |
|------|------|
| `main.py` | Game loop, state machine, event handling, rendering orchestration |
| `settings.py` | All constants (colors, sizes, speeds, timings, debug flag) |
| `player.py` | Player class: position, movement, rect, render |
| `ghost.py` | Ghost class: replay, spawn delay, trail, render |
| `recorder.py` | RunRecorder: record/get/reset/is_full |
| `collision.py` | `check_player_ghost_collision(player, ghosts)` helper |
| `game_state.py` | `GameState` enum (MENU, PLAYING, DYING, GAME_OVER) |
| `arena.py` | Arena boundaries, grid rendering, future obstacles |
| `utils.py` | `draw_text()`, `clamp()`, `load_font()` |

---

## 5. Ghost Recording and Replay System

### Recording (recorder.py)
- `RunRecorder` stores `list[tuple[float, float]]` — one position per 2 frames
- `record(x, y)` called every 2nd frame during PLAYING
- `get_recording()` returns the list (called once on death)
- `reset()` clears buffer for new run
- `is_full()` checks against `MAX_RECORDING_FRAMES`
- Recording interval: every 2 frames (30 FPS recording in 60 FPS game)

### Ghost (ghost.py)
- Takes recording as constructor argument
- Stores `self.recording = recording.copy()` (critical: prevents reference bugs)
- `tick_counter` increments each game tick; `frame_index` advances every 2 ticks (matching recording interval)
- At end: `frame_index = 0` (loop)
- `position = recording[frame_index]`
- `alive` flag: starts False, becomes True after `GHOST_SPAWN_DELAY` (1.0s)
- Trail effect: stores last 5 positions, renders fading rectangles
- `get_rect()` returns `pygame.Rect` for collision

### Ghost Lifecycle
1. On death: create `Ghost(recording)`, append to `ghosts` list
2. On new run: reset all ghosts' `frame_index` to 0, reset spawn timers
3. Each frame: update all ghosts, check collision only with `alive` ghosts
4. Empty recordings (< 10 positions) are discarded

---

## 6. Collision System

- AABB collision via `pygame.Rect.colliderect()`
- Check each frame: `player.rect` vs `ghost.get_rect()` for all alive ghosts
- No pixel-perfect or circle collision — Rect only

---

## 7. Visual Design

### Colors (settings.py)
```
COLOR_BG           = (10, 10, 10)         # near-black
COLOR_PLAYER       = (0, 255, 200)        # neon cyan-green
COLOR_GHOST        = (200, 50, 255)       # purple
COLOR_GLOW_PLAYER  = (0, 255, 200, 40)    # transparent cyan
COLOR_GLOW_GHOST   = (200, 50, 255, 30)   # transparent purple
COLOR_TEXT         = (255, 255, 255)       # white
COLOR_ACCENT       = (255, 50, 80)         # red accent
COLOR_GRID         = (30, 30, 30)          # dark gray
```

### Rendering Order
1. Background fill
2. Grid lines (40px spacing, very low alpha)
3. Ghost glows (larger transparent rects)
4. Ghost bodies
5. Ghost trails (fading)
6. Player glow
7. Player body
8. HUD text
9. Death flash overlay (if DYING)
10. Game over overlay (if GAME_OVER)

### Effects
- **Glow:** larger semi-transparent rect behind entity (no blur shaders)
- **Screen shake:** `camera_offset = (random ±3, random ±3)` applied to all rendering
- **Death flash:** white screen fill for 2-3 frames, then fade
- **Ghost trail:** last 5 positions rendered as fading rects

### Transparency
- Use `pygame.Surface((w, h), pygame.SRCALPHA)` for alpha colors

---

## 8. Settings Constants

```python
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60

PLAYER_SIZE = 32
PLAYER_SPEED = 320          # pixels per second

GHOST_SPAWN_DELAY = 1.0     # seconds before ghost becomes lethal
DEATH_FREEZE_TIME = 0.3     # seconds of freeze-frame on death
SCREEN_SHAKE_DURATION = 0.2 # seconds of shake after death

GRID_SIZE = 40              # pixels between grid lines

MAX_RECORDING_FRAMES = 60 * 300  # 5 minutes at 60 FPS

DEBUG = False               # show FPS, collision boxes, ghost info
```

---

## 9. Main Loop Structure

```python
while running:
    dt = clock.tick(60) / 1000
    handle_events()

    if state == MENU:
        pass  # render title only

    elif state == PLAYING:
        player.update(dt)
        if frame_counter % 2 == 0:
            recorder.record(player.x, player.y)
        update_ghosts(dt)
        check_collisions()
        score_timer += dt

    elif state == DYING:
        death_timer -= dt
        if death_timer <= 0:
            save_recording()
            state = GAME_OVER

    elif state == GAME_OVER:
        pass  # wait for SPACE

    render()
```

---

## 10. Reset Behavior

On SPACE from GAME_OVER, reset:
- Player position
- Score timer
- Recorder buffer
- Death effects (shake, flash)
- All ghost frame indices to 0
- All ghost spawn timers

Do NOT reset:
- Ghosts list
- Best score

---

## 11. Debug Mode

When `DEBUG = True`:
- Show FPS counter (top-right)
- Show ghost frame indices
- Show recording lengths
- Draw collision boxes (red outlines)
- Show player coordinates

---

## 12. Browser Compatibility

Architecture avoids:
- Threading / multiprocessing
- Blocking `time.sleep()`
- Heavy shaders or blur
- Unsupported pygame APIs

Compatible with pygbag deployment.

---

## 13. Implementation Order

1. **Phase 1:** Window, player movement, state machine
2. **Phase 2:** Recorder, ghost replay
3. **Phase 3:** Collision + death flow
4. **Phase 4:** UI + effects
5. **Phase 5:** Polish + deployment
