import random
import socket
import subprocess
import re

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FPS = 60
GUTTER = 50
CHARACTER_COLORS = ["blue", "green", "pink", "purple", "red", "yellow"]
PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64



def get_coin_multiplyer():
    return 1 + random.randint(0,7)/10

def generate_coin():
    coin_pos = get_random_pos()
    multiplyer = get_coin_multiplyer()
    return (coin_pos, multiplyer)

COIN_RADIUS = 16
COIN_COLOR = (255, 215, 0)


def get_random_color():
    """Generate random RGB color."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def get_random_character():
    """Choose random character color."""
    return random.choice(CHARACTER_COLORS)

def get_random_pos():
    """Generate random position within screen bounds."""
    return (random.randint(GUTTER, SCREEN_WIDTH - GUTTER), random.randint(GUTTER, SCREEN_HEIGHT - GUTTER))


def get_lan_ip():
    """Get LAN IP address."""
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.error as e:
        print("Error:", e)
        return None

def get_wifi_ip():
    """Get WiFi IP address."""
    try:
        ipconfig_output = subprocess.check_output(["ipconfig", "/all"], universal_newlines=True)
        wifi_info = re.findall(r"Wireless LAN adapter WiFi.*?IPv4 Address[.\s]*:\s*([\d.]+)", ipconfig_output, re.DOTALL)
        if wifi_info:
            return str(wifi_info[0])
        else:
            return None
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None

# Server IP address
SERVER = get_wifi_ip() or get_lan_ip()
PORT = 5555
BUFFER_SIZE = 2048
# print("Server IP Address:", SERVER)



