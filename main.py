# main.py
# Echo Shift — main entry point and game loop.
# Works on desktop (python main.py) and in browser (pygbag).

import asyncio
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


async def main():
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
    best_score = 0.0

    def reset_game():
        """Unified reset: clears run state, preserves ghosts and best score."""
        nonlocal state, game_time, ghost_count, death_timer, shake_timer
        player.reset()
        recorder.reset()
        game_time = 0.0
        ghost_count = 0
        death_timer = 0.0
        shake_timer = 0.0
        for ghost in ghosts:
            ghost.spawn_timer = 0.0
            ghost.alive = False
            ghost.trail = []
        state = GameState.PLAYING

    # --- Game Loop ---
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                # Q — quit from any state
                if event.key == pygame.K_q:
                    running = False
                    break

                # R — restart from any state (except MENU)
                if event.key == pygame.K_r:
                    if state != GameState.MENU:
                        reset_game()

                # ESC — pause toggle or quit from MENU
                if event.key == pygame.K_ESCAPE:
                    if state == GameState.MENU:
                        running = False
                        break
                    elif state == GameState.PLAYING:
                        state = GameState.PAUSED
                    elif state == GameState.PAUSED:
                        state = GameState.PLAYING
                    elif state == GameState.GAME_OVER:
                        state = GameState.MENU

                # SPACE — start / restart
                if event.key == pygame.K_SPACE:
                    if state == GameState.MENU:
                        reset_game()
                    elif state == GameState.GAME_OVER:
                        reset_game()

        # --- Update ---
        if state == GameState.PLAYING:
            player.update(dt, arena.rect)
            game_time += dt
            recorder.record(player.x, player.y)
            for ghost in ghosts:
                ghost.update(dt, game_time)
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
                # Create ghost with segment-based replay
                recording = recorder.get_recording()
                if len(recording) > 10:
                    segment_index = len(ghosts)
                    ghosts.append(Ghost(recording.copy(), segment_index=segment_index))
                # Update best score
                if game_time > best_score:
                    best_score = game_time
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
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60,
                      font_title, COLOR_PLAYER, center=True)
            draw_text(screen, "Your past becomes your enemy",
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10,
                      font_small, COLOR_TEXT_DIM, center=True)
            draw_text(screen, "Press SPACE to Start",
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60,
                      font_medium, COLOR_TEXT, center=True)
            draw_text(screen, "Click game window before using keyboard",
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100,
                      font_small, COLOR_TEXT_DIM, center=True)
            if best_score > 0:
                draw_text(screen, f"Best: {best_score:.1f}s",
                          WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 140,
                          font_small, COLOR_TEXT_DIM, center=True)

        elif state == GameState.PLAYING:
            arena.render(screen, camera_offset)
            for ghost in ghosts:
                ghost.render(screen, camera_offset, game_time)
            player.render(screen, camera_offset)

            # HUD
            draw_text(screen, f"Time: {game_time:.1f}s", 20, 20,
                      font_small, COLOR_TEXT)
            draw_text(screen, f"Ghosts: {ghost_count}", 20, 50,
                      font_small, COLOR_TEXT)
            if best_score > 0:
                draw_text(screen, f"Best: {best_score:.1f}s", 20, 80,
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
                    draw_text(screen, f"Ghost {i}: seg={ghost.segment_index} alive={ghost.alive}",
                              20, 200 + i * 30, font_small, COLOR_TEXT_DIM)

        elif state == GameState.DYING:
            # Render frozen game frame + white flash
            arena.render(screen, camera_offset)
            for ghost in ghosts:
                ghost.render(screen, camera_offset, game_time)
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
            # Dark background
            screen.fill((10, 10, 10))

            # Semi-transparent overlay panel
            panel_width, panel_height = 400, 280
            panel_x = (WINDOW_WIDTH - panel_width) // 2
            panel_y = (WINDOW_HEIGHT - panel_height) // 2
            panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            panel_surface.fill((0, 0, 0, 180))
            screen.blit(panel_surface, (panel_x, panel_y))

            # Panel border
            pygame.draw.rect(screen, COLOR_ACCENT,
                           (panel_x, panel_y, panel_width, panel_height), 2)

            # Text content
            center_x = WINDOW_WIDTH // 2
            draw_text(screen, "GAME OVER",
                      center_x, panel_y + 50,
                      font_title, COLOR_ACCENT, center=True)
            draw_text(screen, f"Survived: {game_time:.1f}s",
                      center_x, panel_y + 120,
                      font_medium, COLOR_TEXT, center=True)
            draw_text(screen, f"Ghosts: {ghost_count}",
                      center_x, panel_y + 160,
                      font_medium, COLOR_TEXT, center=True)
            if best_score > 0:
                draw_text(screen, f"Best: {best_score:.1f}s",
                          center_x, panel_y + 200,
                          font_medium, COLOR_TEXT_DIM, center=True)
            draw_text(screen, "SPACE to Restart | ESC to Menu",
                      center_x, panel_y + 250,
                      font_small, COLOR_TEXT_DIM, center=True)

        elif state == GameState.PAUSED:
            # Render frozen game frame
            arena.render(screen, camera_offset)
            for ghost in ghosts:
                ghost.render(screen, camera_offset, game_time)
            player.render(screen, camera_offset)

            # Dark overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            # Pause text
            draw_text(screen, "PAUSED",
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60,
                      font_title, COLOR_PLAYER, center=True)
            draw_text(screen, "ESC to Resume",
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20,
                      font_small, COLOR_TEXT, center=True)
            draw_text(screen, "R to Restart",
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50,
                      font_small, COLOR_TEXT, center=True)
            draw_text(screen, "Q to Quit",
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80,
                      font_small, COLOR_TEXT, center=True)

        pygame.display.flip()
        await asyncio.sleep(0)  # yield to browser event loop (pygbag)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
