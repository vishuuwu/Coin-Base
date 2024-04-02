import pygame
from network import Network
from player import Player

# Constants
WIDTH = 1000
HEIGHT = 800
FPS = 60

# Player constants
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 100
PLAYER_COLOR = (0, 0, 255)
PLAYER_TWO_COLOR = (0, 255, 0)




def redraw_window(win, player, player2):
    """
    Redraw the window with a white background and the player.

    Args:
        win (pygame.Surface): The window surface to draw on.
        player (Player): The player object to draw.
    """
    win.fill((255, 255, 255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def handle_events():
    """Handle events such as quitting the game."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True



def main():
    """Main function to run the game."""
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Client")

    running = True
    n = Network()
    player =n.getPlayer()

  
    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)

        p2 = n.send(player)

        running = handle_events()

        player.move()
        redraw_window(win, player, p2)

    pygame.quit()


if __name__ == "__main__":
    main()
