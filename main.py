# main.py
# Echo Shift — main entry point and game loop.

import sys
import random
import pygame

from core.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TITLE,
    COLOR_TEXT, COLOR_TEXT_DIM, COLOR_ACCENT, COLOR_PLAYER,
    DEATH_FREEZE_TIME, SCREEN_SHAKE_DURATION, SCREEN_SHAKE_INTENSITY,
    SEED_GHOST_TIMER, DEBUG,
)
from core.collision import check_player_ghost_collision
from core.game_state import GameState
from core.utils import draw_text, load_font
from core.player import Player
from levels.arena import Arena
from core.recorder import RunRecorder
from core.ghost import Ghost


def main():
    # --- Init ---
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # --- Fonts ---
    font_title = load_font(72)
    font_medium = load_font(36)
    font_small = load_font(24)

    # --- Objects ---
    player = Player()
    arena = Arena()
    recorder = RunRecorder()
    ghosts = []

    # --- State ---
    state = GameState.MENU
    game_time = 0.0
    ghost_count = 0
    death_timer = 0.0
    shake_timer = 0.0
    camera_offset = (0, 0)

    # --- Game Loop ---
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
                        player.reset()
                        game_time = 0.0
                        ghost_count = 0
                        death_timer = 0.0
                        shake_timer = 0.0
                        recorder.reset()
                    elif state == GameState.GAME_OVER:
                        state = GameState.PLAYING
                        player.reset()
                        game_time = 0.0
                        ghost_count = 0
                        death_timer = 0.0
                        shake_timer = 0.0
                        recorder.reset()
                        for ghost in ghosts:
                            ghost.frame_index = 0
                            ghost.tick_counter = 0
                            ghost.spawn_timer = 0.0
                            ghost.alive = False
                            ghost.trail = []

        # --- Update ---
        if state == GameState.PLAYING:
            player.update(dt, arena.rect)
            game_time += dt
            recorder.record(player.x, player.y)
            for ghost in ghosts:
                ghost.update(dt)
            ghost_count = len(ghosts)

            # Collision check
            if check_player_ghost_collision(player, ghosts):
                state = GameState.DYING
                death_timer = 0.0
                shake_timer = SCREEN_SHAKE_DURATION

            # Seed ghost: auto-death on first run after timer expires
            elif len(ghosts) == 0 and game_time >= SEED_GHOST_TIMER:
                state = GameState.DYING
                death_timer = 0.0
                shake_timer = SCREEN_SHAKE_DURATION

        elif state == GameState.DYING:
            death_timer += dt
            if death_timer >= DEATH_FREEZE_TIME:
                # Create ghost from this run's recording
                recording = recorder.get_recording()
                if len(recording) > 10:
                    ghosts.append(Ghost(recording.copy()))
                state = GameState.GAME_OVER

        # Screen shake
        if shake_timer > 0:
            shake_timer -= dt
            intensity = SCREEN_SHAKE_INTENSITY
            camera_offset = (
                random.randint(-intensity, intensity),
                random.randint(-intensity, intensity),
            )
        else:
            camera_offset = (0, 0)

        # --- Render ---
        if state == GameState.MENU:
            screen.fill((10, 10, 10))
            draw_text(screen, "ECHO SHIFT",
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40,
                      font_title, COLOR_PLAYER, center=True)
            draw_text(screen, "Press SPACE to Start",
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40,
                      font_medium, COLOR_TEXT, center=True)

        elif state == GameState.PLAYING:
            arena.render(screen, camera_offset)
            for ghost in ghosts:
                ghost.render(screen, camera_offset)
            player.render(screen, camera_offset)

            # HUD
            draw_text(screen, f"Time: {game_time:.1f}s", 20, 20,
                      font_small, COLOR_TEXT)
            draw_text(screen, f"Ghosts: {ghost_count}", 20, 50,
                      font_small, COLOR_TEXT)
            draw_text(screen, f"REC: {recorder.length}", 20, 80,
                      font_small, COLOR_TEXT_DIM)

            # Seed timer warning (first run only, last 5 seconds)
            if len(ghosts) == 0 and game_time >= SEED_GHOST_TIMER - 5:
                remaining = max(0, SEED_GHOST_TIMER - game_time)
                draw_text(screen, f"Echo incoming: {remaining:.0f}s",
                          WINDOW_WIDTH // 2, 20,
                          font_small, COLOR_ACCENT, center=True)

            # Debug HUD
            if DEBUG:
                est_memory_kb = recorder.length * 8 / 1024  # 2 floats * 4 bytes each
                draw_text(screen, f"REC frames: {recorder.length}", 20, 110,
                          font_small, COLOR_TEXT_DIM)
                draw_text(screen, f"REC memory: {est_memory_kb:.1f} KB", 20, 140,
                          font_small, COLOR_TEXT_DIM)
                draw_text(screen, f"REC full: {recorder.is_full()}", 20, 170,
                          font_small, COLOR_TEXT_DIM)
                for i, ghost in enumerate(ghosts):
                    draw_text(screen, f"Ghost {i}: frame={ghost.frame_index} alive={ghost.alive}",
                              20, 200 + i * 30, font_small, COLOR_TEXT_DIM)

        elif state == GameState.DYING:
            # Render frozen game frame + white flash
            arena.render(screen, camera_offset)
            for ghost in ghosts:
                ghost.render(screen, camera_offset)
            player.render(screen, camera_offset)

            # White flash overlay (fades out over DEATH_FREEZE_TIME)
            flash_progress = death_timer / DEATH_FREEZE_TIME
            flash_alpha = int(200 * (1.0 - flash_progress))
            if flash_alpha > 0:
                flash_surface = pygame.Surface(
                    (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA
                )
                flash_surface.fill((255, 255, 255, flash_alpha))
                screen.blit(flash_surface, (0, 0))

        elif state == GameState.GAME_OVER:
            screen.fill((10, 10, 10))
            draw_text(screen, "GAME OVER",
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60,
                      font_title, COLOR_ACCENT, center=True)
            draw_text(screen, f"Survived: {game_time:.1f}s",
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10,
                      font_medium, COLOR_TEXT, center=True)
            draw_text(screen, f"Ghosts: {ghost_count}",
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50,
                      font_medium, COLOR_TEXT, center=True)
            draw_text(screen, "Press SPACE to restart",
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100,
                      font_small, COLOR_TEXT_DIM, center=True)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
