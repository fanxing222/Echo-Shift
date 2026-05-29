# Echo Shift

A replay survival game built with pygame-ce & pygbag — your past movements become your future enemies.

## Features

- **Ghost Replay System** — Each death records your movement as a lethal "Ghost Echo"
- **Segmented Timeline Replay** — Ghosts replay distinct 5-second segments of past runs
- **Deterministic Gameplay** — Same inputs always produce the same outcome
- **Browser Playable Build** — Runs in the browser via pygbag (WebAssembly)
- **Pause / Restart System** — Full game state management (menu, playing, paused, game over)

## Technologies

- Python 3.8+
- [pygame-ce](https://github.com/pygame-community/pygame-ce)
- [pygbag](https://github.com/pygame-web/pygbag) (WebAssembly deployment)

## Controls

| Key | Action |
|-----|--------|
| `WASD` / Arrow Keys | Move |
| `SPACE` | Start / Restart |
| `ESC` | Pause / Quit to Menu |
| `R` | Restart (during gameplay) |
| `Q` | Quit |

## Run Locally

**Desktop:**

```bash
python main.py
```

**Web (local browser):**

```bash
python build_web.py --serve
```

## Web Demo

> **Live demo:** [COMING SOON — Vercel deployment link]

## Screenshots

> **Screenshots:** [COMING SOON]

## Algorithm Overview

The core mechanic is built on three systems:

1. **Trajectory Recording** — Player positions are sampled every 2 frames (30 FPS) and stored as `(x, y)` coordinate lists
2. **Replay Playback** — On death, the recording is saved. In the next run, a Ghost replays those positions using linear interpolation between frames
3. **Segmented Replay** — Each Ghost is assigned a 5-second segment of the full recording (Ghost 0 = 0–5s, Ghost 1 = 5–10s, etc.), creating diverse movement patterns from a single run

## Project Structure

```
Echo Shift/
├── main.py              # Entry point, game loop, state machine
├── build_web.py         # Web build script (pygbag)
├── requirements.txt     # Dependencies
├── core/
│   ├── settings.py      # Game constants
│   ├── player.py        # Player movement & rendering
│   ├── ghost.py         # Ghost replay logic
│   ├── recorder.py      # Position recording system
│   ├── collision.py     # AABB collision detection
│   ├── game_state.py    # GameState enum
│   └── utils.py         # Helpers
├── levels/
│   └── arena.py         # Arena rendering
└── build/web/           # Browser build output (index.html + wasm)
```

## License

MIT License — see [LICENSE](LICENSE) for details.
