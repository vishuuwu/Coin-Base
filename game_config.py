import random
import socket
import subprocess
import re 






SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FPS = 60


CHARACTER_COLORS = ["blue", "green", "pink", "purple", "red", "yellow"]

PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64
# PLAYER_COLOR = (0, 0, 255)
# PLAYER_TWO_COLOR = (0, 255, 0)


GUTTER = 50


def get_random_pos(SCREEN_WIDTH = 1000, SCREEN_HEIGHT = 800 ):
    return(random.randint(GUTTER, SCREEN_WIDTH - GUTTER),random.randint(GUTTER, SCREEN_HEIGHT - GUTTER ))

def get_random_color():
    return(random.randint(0,255),random.randint(0,255),random.randint(0,255))
# print(get_random_pos())
# print(get_random_color())

def get_random_character():
    return random.choice(CHARACTER_COLORS)



def get_lan_ip():# LAN
    try:
        # Get the hostname
        hostname = socket.gethostname()
        # Get the IP address corresponding to the hostname
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.error as e:
        print("Error:", e)
        return None

# Get and print the IP address
# ip_address = get_ip_address()
# if ip_address:
#     print("IP Address:", ip_address)




def get_wifi_ip():#wifi
    try:
        # Run the ipconfig command and capture its output
        ipconfig_output = subprocess.check_output(["ipconfig", "/all"], universal_newlines=True)
    
        wifi_info = re.findall(r"Wireless LAN adapter WiFi.*?IPv4 Address[.\s]*:\s*([\d.]+)", ipconfig_output, re.DOTALL)
        # print (wifi_info)
        if wifi_info:
            return str(wifi_info[0])
        else:
            return None
        
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None



SERVER = str(get_wifi_ip())

# print (SERVER)
# wifi_ip = get_wifi_ip()
# if wifi_ip:
#     print("WiFi Interface IP Address:", wifi_ip)
# else:
#     print("WiFi Interface IP Address not found.")
