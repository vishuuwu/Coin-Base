import random
import socket
import subprocess
import re

# Screen Constants
FPS = 60
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
HEADER_HEIGHT = 54
FOOTER_HEIGHT = 38
SCORECARD_HEIGHT = 28
SCORECARD_WIDTH = SCREEN_WIDTH // 6
BORDER_WIDTH = 1
SCREEN_COLOR = (253, 252, 238)
SECONDARY_COLOR = (255, 144, 232)  # Accent Pink
PRIMARY_COLOR = (255, 201, 0)  # Accent Yellow
TERTIARY_COLOR = (0, 0, 0)  # black

# Font Constants
SECONDARY_FONT = "Roboto"
PRIMARY_FONT = "MabryPro-Regular"
TITLE_TEXT_SIZE = 48
SUB_TITLE_TEXT_SIZE = 18
BODY_TEXT_SIZE = 14

# Player Constants
PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64
PLAYER_VELOCITY = 5
CHARACTER_COLORS = ["blue", "green", "pink", "purple", "red", "yellow"]
PLAYER_LIMIT_LEFT = SCORECARD_WIDTH + 2 * BORDER_WIDTH
PLAYER_LIMIT_RIGHT = SCREEN_WIDTH - BORDER_WIDTH
PLAYER_LIMIT_TOP = HEADER_HEIGHT + 2* BORDER_WIDTH
PLAYER_LIMIT_DOWN = SCREEN_HEIGHT - FOOTER_HEIGHT - 2 * BORDER_WIDTH

# Coin Constants
COIN_RADIUS = 16
COIN_COLOR = (255, 215, 0)
MAX_COINS = 5
MIN_GENERATE_INTERVAL = 1
MAX_GENERATE_INTERVAL = 5

# server Constants
PORT = 5555
BUFFER_SIZE = 2048
WINNING_POINTS = 10 

def get_random_color() -> tuple:
    """
    Generate a random RGB color tuple.

    Returns:
        tuple: Random RGB color tuple.
    """
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def get_random_character() -> str:
    """
    Choose a random character color.

    Returns:
        str: Random character color.
    """
    return random.choice(CHARACTER_COLORS)


def get_random_pos(gutter: int = 50) -> tuple:
    """
    Generate a random position within the screen bounds.

    Args:
        gutter (int): Minimum distance from the screen edges. Defaults to 50.

    Returns:
        tuple: Random position coordinates (x, y).
    """
    return (
        random.randint(SCORECARD_WIDTH + gutter, SCREEN_WIDTH - gutter),
        random.randint(HEADER_HEIGHT + gutter, SCREEN_HEIGHT - FOOTER_HEIGHT - gutter),
    )


def get_lan_ip() -> str:
    """
    Get the LAN IP address of the device.

    Returns:
        str: LAN IP address.
    """
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.error as e:
        print("Error:", e)
        return ""


def get_wifi_ip() -> str:
    """
    Get the WiFi IP address of the device.

    Returns:
        str: WiFi IP address.
    """
    try:
        ipconfig_output = subprocess.check_output(
            ["ipconfig", "/all"], universal_newlines=True
        )
        wifi_info = re.findall(
            r"Wireless LAN adapter WiFi.*?IPv4 Address[.\s]*:\s*([\d.]+)",
            ipconfig_output,
            re.DOTALL,
        )
        if wifi_info:
            return str(wifi_info[0])
        else:
            return ""
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return ""


# Server IP address
SERVER = get_wifi_ip() or get_lan_ip()
