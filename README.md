# Echo Shift

A minimalist sci-fi survival arcade game where your past actions become future enemies.

## Gameplay

Each run records your movement. When you die, that recording becomes a "Ghost Echo" that replays your exact path in all future runs. Survive as long as possible while the arena fills with echoes of your past behavior.

### Core Mechanics

- **Movement Recording** — Every run records your exact positions
- **Ghost Echoes** — Past recordings become lethal enemies
- **Increasing Difficulty** — More deaths = more ghosts = harder survival
- **Time Pressure** — First death is forced after 30 seconds if you survive that long

## Controls

| Key | Action |
|-----|--------|
| `WASD` | Move |
| `SPACE` | Start / Restart |
| `ESC` | Quit |

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/fanxing222/Echo-Shift.git
cd Echo-Shift

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

## Project Structure

```
Echo Shift/
├── main.py              # Entry point, game loop, state machine
├── requirements.txt     # Python dependencies
├── LICENSE              # MIT License
├── README.md            # This file
├── assets/              # Fonts, sounds (future)
├── core/
│   ├── __init__.py
│   ├── settings.py      # All constants and configuration
│   ├── player.py        # Player class
│   ├── ghost.py         # Ghost class
│   ├── recorder.py      # RunRecorder class
│   ├── collision.py     # Collision detection
│   ├── game_state.py    # GameState enum
│   └── utils.py         # Utility functions
└── levels/
    ├── __init__.py
    └── arena.py         # Arena boundaries and rendering
```

## Technical Details

- **Framework:** pygame-ce
- **Resolution:** 1280×720
- **FPS:** 60
- **Recording:** 30 FPS (every 2 frames)
- **Max Recording:** 5 minutes per run

## Game States

```
MENU ──(SPACE)──▶ PLAYING ──(collision)──▶ DYING ──(0.3s)──▶ GAME_OVER
  ▲                                                            │
  └──────────────────────────(SPACE)───────────────────────────┘
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [pygame-ce](https://github.com/pygame-community/pygame-ce)
- Inspired by time-loop and echo mechanics in games
