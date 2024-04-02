import pygame

# Constants
WIDTH = 1000
HEIGHT = 800
FPS = 60

# Player constants
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 100
PLAYER_COLOR = (0, 0, 255)
PLAYER_VELOCITY = 3


class Player:
    """Class to represent the player."""

    def __init__(self, x, y, width, height, color):
        """Initialize player attributes."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.vel = PLAYER_VELOCITY

    def draw(self, win):
        """Draw the player on the window."""
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
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


def redraw_window(win, player):
    """Redraw the window with a white background and the player."""
    win.fill((255, 255, 255))
    player.draw(win)
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

    player = Player(50, 50, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR)
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(FPS)
        running = handle_events()

        player.move()
        redraw_window(win, player)

    pygame.quit()


if __name__ == "__main__":
    main()
