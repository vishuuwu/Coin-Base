import pygame
from game_config import get_random_color, PLAYER_LIMIT_LEFT,PLAYER_LIMIT_RIGHT, PLAYER_LIMIT_DOWN,PLAYER_LIMIT_TOP

PLAYER_VELOCITY = 5

class Player:
    """A class representing a player."""

    def __init__(self, player_id, x, y, width, height, character_color):
        """
        Initialize a Player object.

        Args:
            player_id (int): The unique identifier for the player.
            x (int): The x-coordinate of the player's top-left corner.
            y (int): The y-coordinate of the player's top-left corner.
            width (int): The width of the player.
            height (int): The height of the player.
            character_color (tuple): The RGB color tuple representing the player's character.
        """
        self.id = player_id
        self.name = f"guest_{str(player_id)[:4]}"
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.score = 0
        self.character = character_color
        self.color = get_random_color()
        self.rect = pygame.Rect(x, y, width, height)
        self.direction = "left"
        self.vel = PLAYER_VELOCITY

    def move(self):
        """Move the player based on key inputs."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > PLAYER_LIMIT_LEFT + 2:
            self.x -= self.vel
        if keys[pygame.K_RIGHT] and self.x < PLAYER_LIMIT_RIGHT - self.height :
            self.x += self.vel
        if keys[pygame.K_UP] and self.y > PLAYER_LIMIT_TOP + 2 :
            self.y -= self.vel
        if keys[pygame.K_DOWN] and self.y < PLAYER_LIMIT_DOWN - self.height -2:
            self.y += self.vel
        self.update()

    def update(self):
        """Update the player's rectangle."""
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update_score(self, multiplier=1):
        """Update the player's score."""
        self.score += 1 * multiplier
        print(self.score)

    def get_player_details(self):
        """
        Get details of the player as a dictionary.

        Returns:
            dict: A dictionary containing the player's details.
        """
        return {
            "id": self.id,
            "name": self.name,
            "score": self.score,
            "navigation": {
                "x": self.x,
                "y": self.y,
                "direction": self.direction,
                "vel": self.vel,
            },
            "details": {
                "width": self.width,
                "height": self.height,
                "character": self.character,
                "color": self.color,
            },
        }
