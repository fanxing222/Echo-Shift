# core/collision.py
# AABB collision detection between player and ghosts.


def check_player_ghost_collision(player, ghosts):
    """Return True if the player collides with any alive ghost."""
    player_rect = player.rect
    for ghost in ghosts:
        if ghost.alive and player_rect.colliderect(ghost.rect):
            return True
    return False
