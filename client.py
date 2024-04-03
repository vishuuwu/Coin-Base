import pygame
from network import Network
# from player import Player
from game_config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from os import listdir
from os.path import join, isfile


def flip_sprite(sprite):
    return pygame.transform.flip(sprite, True, False)

def load_character_sprites(direction=False):
    dir = "characters"
    path = join("assets", dir)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_character_sprites = {}

    for image in images:
        sprite = pygame.image.load(join(path, image)).convert_alpha()

        if direction:
            all_character_sprites[image.replace(".png", "") + "_right"] = sprite
            all_character_sprites[image.replace(".png", "") + "_left"] = flip_sprite(sprite)
        else:
            all_character_sprites[image.replace(".png", "")] = sprite
    return all_character_sprites


#--------------------------------------------------------
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

#--------------------------------------------------------


#--------------------------------------------------------

def draw(player, win):
    """
    Draw the player on the window.

        Args:
        win (pygame.Surface): The window surface to draw the player on.
    """
    pygame.draw.rect(win, player.color, player.rect)

def redraw_window(win, player, opponents):
    """
    Redraw the window with a white background and the player.

    Args:
        win (pygame.Surface): The window surface to draw on.
        player (Player): The player object to draw.
    """
    win.fill((255, 255, 255))
    draw(player,win)
    for opp_id, opp in opponents.items():
        draw(opp,win)

    pygame.display.update()


#--------------------------------------------------------

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
    player =n.getPlayer()
    print(player)
    print(player.char)
    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)

        opponents = n.send(player)
        # print(len(opponents))
        running = handle_events()
        if running == False :
            print("Disconnected")
            n.disconnect()

        player.move()
        redraw_window(win, player, opponents)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Client")
    SPRITES = load_character_sprites(True)
    main()