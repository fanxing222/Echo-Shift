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
SEED_GHOST_TIMER = 15.0  # seconds before first-run auto-death (seeds the ghost loop)

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
