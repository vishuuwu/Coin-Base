import pygame
from network import Network


# Constants
WIDTH = 1000
HEIGHT = 800
FPS = 60

# Player constants
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 100
PLAYER_COLOR = (0, 0, 255)
PLAYER_TWO_COLOR = (0, 255, 0)
PLAYER_VELOCITY = 3


class Player:
    """A class representing the player."""

    def __init__(self, x, y, width, height, color):
        """
        Initialize a Player object.

        Args:
            x (int): The x-coordinate of the player's top-left corner.
            y (int): The y-coordinate of the player's top-left corner.
            width (int): The width of the player.
            height (int): The height of the player.
            color (tuple): The RGB color tuple representing the player's color.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.vel = PLAYER_VELOCITY

    def draw(self, win):
        """
        Draw the player on the window.

        Args:
            win (pygame.Surface): The window surface to draw the player on.
        """
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        """Move the player based on key inputs."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel
        self.update()

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


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


def read_pos(str):
    str = str.split(",")
    return (int(str[0]), int(str[1]))


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def main():
    """Main function to run the game."""
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Client")

    running = True
    n = Network()
    startPos = read_pos(n.getPos())
    player = Player(startPos[0], startPos[1], PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR)

    # other player statPos
    p2 = Player(startPos[0], startPos[1], PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_TWO_COLOR)

    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)

        p2pos = read_pos(n.send(make_pos((player.x, player.y))))
        p2.x, p2.y = p2pos
        p2.update()
        running = handle_events()

        player.move()
        redraw_window(win, player, p2)

    pygame.quit()


if __name__ == "__main__":
    main()
