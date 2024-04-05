import random
import pygame
from game_config import COIN_RADIUS, COIN_COLOR, get_random_pos


def get_coin_multiplier() -> float:
    """
    Generate a random coin multiplier between 1.0 and 1.7.

    Returns:
        float: Random coin multiplier.
    """
    return 1.0 + random.random() * 0.7


def generate_coin() -> 'Coin':
    """
    Generate a random coin with a random position and multiplier.

    Returns:
        Coin: A Coin instance with random attributes.
    """
    coin_pos = get_random_pos(COIN_RADIUS*1.7)
    multiplier = get_coin_multiplier()
    return Coin(*coin_pos, multiplier)


class Coin:
    """Class representing a coin in the game."""

    def __init__(self, x: int, y: int, multiplier: float):
        """
        Initialize a Coin instance with the given attributes.

        Args:
            x (int): The x-coordinate of the center of the coin.
            y (int): The y-coordinate of the center of the coin.
            multiplier (float): The multiplier of the coin's radius.
        """
        self.center_x = x
        self.center_y = y
        self.multiplier = multiplier
        self.radius = COIN_RADIUS * multiplier
        self.color = COIN_COLOR

    def draw(self, win: pygame.Surface):
        """
        Draw the coin on the given surface.

        Args:
            win (pygame.Surface): The window surface to draw the coin on.
        """
        pygame.draw.circle(win, self.color, (self.center_x, self.center_y), self.radius)
