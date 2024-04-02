import pygame
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

