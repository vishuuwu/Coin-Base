import random
import socket
import subprocess
import re


WINNING_POINTS = 20

# Screen Constants
FPS = 60
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
HEADER_HEIGHT = 54
FOOTER_HEIGHT = 38
SCORECARD_HEIGHT = 28
SCORECARD_WIDTH = SCREEN_WIDTH // 6
SCREEN_COLOR = (253, 252, 238)

ACCENT_PINK = (255, 144, 232)
ACCENT_YELLOW = (255, 201, 0)

# Player Constants
PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64
CHARACTER_COLORS = ["blue", "green", "pink", "purple", "red", "yellow"]
PLAYER_LIMIT_LEFT = SCORECARD_WIDTH
PLAYER_LIMIT_RIGHT = SCREEN_WIDTH
PLAYER_LIMIT_TOP = HEADER_HEIGHT
PLAYER_LIMIT_DOWN = SCREEN_HEIGHT - FOOTER_HEIGHT

# Coin Constants
COIN_RADIUS = 16
COIN_COLOR = (255, 215, 0)
MAX_COINS = 5
MIN_GENERATE_INTERVAL = 1
MAX_GENERATE_INTERVAL = 5

# Networking Constants
PORT = 5555
BUFFER_SIZE = 2048

def get_coin_multiplier() -> float:
    """Generate random coin multiplier between 1.0 and 1.7."""
    return 1.0 + random.random() * 0.7

def generate_coin() -> tuple:
    """Generate a random coin position and multiplier."""
    coin_pos = get_random_pos(20)
    multiplier = get_coin_multiplier()
    return coin_pos, multiplier

def get_random_color() -> tuple:
    """Generate random RGB color."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def get_random_character() -> str:
    """Choose random character color."""
    return random.choice(CHARACTER_COLORS)

def get_random_pos(gutter: int = 50) -> tuple:
    """Generate random position within screen bounds."""
    return (
        random.randint(SCORECARD_WIDTH + gutter, SCREEN_WIDTH - gutter),
        random.randint(HEADER_HEIGHT + gutter, SCREEN_HEIGHT - FOOTER_HEIGHT - gutter),
    )

def get_lan_ip() -> str:
    """Get LAN IP address."""
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.error as e:
        print("Error:", e)
        return ""

def get_wifi_ip() -> str:
    """Get WiFi IP address."""
    try:
        ipconfig_output = subprocess.check_output(["ipconfig", "/all"], universal_newlines=True)
        wifi_info = re.findall(r"Wireless LAN adapter WiFi.*?IPv4 Address[.\s]*:\s*([\d.]+)", ipconfig_output, re.DOTALL)
        if wifi_info:
            return str(wifi_info[0])
        else:
            return ""
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return ""

# Server IP address
SERVER = get_wifi_ip() or get_lan_ip()
