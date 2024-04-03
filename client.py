import pygame
from network import Network
from game_config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COIN_RADIUS, COIN_COLOR
from os import listdir
from os.path import join, isfile


def flip_sprite(sprite):
    return pygame.transform.flip(sprite, True, False)

def load_character_sprites(direction=False):
    """
    Load character sprites from the assets folder.

    Args:
        direction (bool): Whether to load sprites for both directions.

    Returns:
        dict: Dictionary containing character sprites.
    """
    dir = "characters"
    path = join("assets", dir)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    character_sprites = {}

    for image in images:
        sprite = pygame.image.load(join(path, image)).convert_alpha()

        if direction:
            character_sprites[image.replace(".png", "") + "_right"] = sprite
            character_sprites[image.replace(".png", "") + "_left"] = flip_sprite(sprite)
        else:
            character_sprites[image.replace(".png", "")] = sprite
    return character_sprites

# --------------------------------------------------------
"""
TypeError: cannot pickle 'pygame.surface.Surface' object` 

pickle cant serialize (or i am not able to serialize..) pygame.surface object
"""

# def draw(player, win, SPRITES):
#     """
#         Draw the player on the window.

#         Args:
#             win (pygame.Surface): The window surface to draw the player on.
#     """
#     player.sprite = SPRITES[player.char + "_" + player.direction]
#     win.blit(player.sprite, (player.x, player.y))

# def redraw_window(win, player, opponents):
#     """
#     Redraw the window with a white background and the player.

#     Args:
#         win (pygame.Surface): The window surface to draw on.
#         player (Player): The player object to draw.
#     """
#     win.fill((255, 255, 255))
#     draw(player,win, SPRITES)
#     for opp_id, opp in opponents.items():
#         draw(opp,win, SPRITES)

#     pygame.display.update()

# --------------------------------------------------------

def draw(player, win):
    """
    Draw the player on the window.

    Args:
        player (Player): The player object to draw.
        win (pygame.Surface): The window surface to draw on.
    """
    pygame.draw.rect(win, player.color, player.rect)

def draw_coin(coin, win):
    """
    Draw a coin on the window.

    Args:
        coin (tuple): The coin object containing position and radius information.
                Format: (center_x, center_y, radius)
        win (pygame.Surface): The window surface to draw on.
    """
    (center_x, center_y), multiplier = coin
    pygame.draw.circle(win, COIN_COLOR, (center_x, center_y), COIN_RADIUS * multiplier)

def redraw_window(player, opponents, coins, win):
    """
    Redraw the window with a white background and the players.

    Args:
        win (pygame.Surface): The window surface to draw on.
        player (Player): The player object to draw.
        opponents (dict): Dictionary containing opponent players.
        coins (dict): Dictionary containing coin positions and multipliers.
    """
    win.fill((255, 255, 255))
    draw(player, win)
    for coin_id, coin in coins.items():
        draw_coin(coin, win)
    for opp_id, opp in opponents.items():
        draw(opp, win)

    draw(player, win)
    pygame.display.update()

def handle_events():
    """Handle events such as quitting the game."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def main():
    """Main function to run the game."""
    running = True
    n = Network()
    player = n.getPlayer()
    print(player.get_player_details())
    print(player.name)
    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)

        response = n.send(player)
        multiplier = response["multiplier"]
        if multiplier != 0:
            player.update_score(multiplier)

        opponents = response["opponents"]
        coins = response["coins"]

        running = handle_events()
        if not running:
            print("Disconnected")
            n.disconnect()

        player.move()
        redraw_window(player, opponents, coins, win)

    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Client")
    main()
