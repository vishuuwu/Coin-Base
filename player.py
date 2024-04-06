import pygame
from game_config import (
    get_random_color,
    PLAYER_LIMIT_LEFT,
    PLAYER_LIMIT_RIGHT,
    PLAYER_LIMIT_DOWN,
    PLAYER_LIMIT_TOP,
    PLAYER_VELOCITY,
    PLAYER_SHADOW,
    PLAYER_BORDER_RADIUS,
    TERTIARY_COLOR,
    BORDER_WIDTH,
    DRAW_GUI
)


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
        self.shadowRect = pygame.Rect(
            x + PLAYER_SHADOW, y + PLAYER_SHADOW, width, height
        )
        self.borderRect = pygame.Rect(
            x - BORDER_WIDTH,
            y - BORDER_WIDTH,
            width + 2 * BORDER_WIDTH,
            height + 2 * BORDER_WIDTH,
        )
        self.direction = "left"
        self.vel = PLAYER_VELOCITY

    def move(self):
        """
        Move the player based on key inputs.

        Controls:
            - Left Arrow: Move left.
            - Right Arrow: Move right.
            - Up Arrow: Move up.
            - Down Arrow: Move down.
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x > PLAYER_LIMIT_LEFT:
            self.x -= self.vel
            if self.x < PLAYER_LIMIT_LEFT:
                self.x = PLAYER_LIMIT_LEFT

        if keys[pygame.K_RIGHT] and self.x < PLAYER_LIMIT_RIGHT - self.width:
            self.x += self.vel
            if self.x > PLAYER_LIMIT_RIGHT - self.width:
                self.x = PLAYER_LIMIT_RIGHT - self.width

        if keys[pygame.K_UP] and self.y > PLAYER_LIMIT_TOP:
            self.y -= self.vel
            if self.y < PLAYER_LIMIT_TOP:
                self.y = PLAYER_LIMIT_TOP

        if keys[pygame.K_DOWN] and self.y < PLAYER_LIMIT_DOWN - self.height:
            self.y += self.vel
            if self.y > PLAYER_LIMIT_DOWN - self.height:
                self.y = PLAYER_LIMIT_DOWN - self.height

        self.update()

    def update(self):
        """Update the player's rectangle."""
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if DRAW_GUI:
            self.shadowRect = pygame.Rect(
                self.x + PLAYER_SHADOW, self.y + PLAYER_SHADOW, self.width, self.height
            )
            self.borderRect = pygame.Rect(
                self.x - BORDER_WIDTH,
                self.y - BORDER_WIDTH,
                self.width + 2 * BORDER_WIDTH,
                self.height + 2 * BORDER_WIDTH,
            )

    def update_score(self, multiplier=1):
        """
        Update the player's score.

        Args:
            multiplier (int, optional): The multiplier to apply to the score (default is 1).
        """
        self.score += 1 * multiplier

    def draw(self, win: pygame.Surface) -> None:
        """
        Draw the player on the window.

        Args:
            win (pygame.Surface): The window surface to draw on.
        """
        if DRAW_GUI:
            pygame.draw.rect(
                win, TERTIARY_COLOR, self.shadowRect, border_radius=PLAYER_BORDER_RADIUS
            )
            pygame.draw.rect(
                win, TERTIARY_COLOR, self.borderRect, border_radius=PLAYER_BORDER_RADIUS
            )

        pygame.draw.rect(win, self.color, self.rect, border_radius=PLAYER_BORDER_RADIUS)

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
