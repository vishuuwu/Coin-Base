import socket
import threading
import uuid
import pickle
import random
import time
from player import Player
from game_config import (
    get_random_pos,
    get_random_character,
    generate_coin,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    COIN_RADIUS,
    SERVER,
    PORT,
    BUFFER_SIZE
    
)

# Constants
MAX_COINS = 20
MIN_GENERATE_INTERVAL = 1
MAX_GENERATE_INTERVAL = 5

# Global variables
COINS = {}
PLAYERS = {}
coin_lock = threading.Lock()


def grab_coin(player):
    """
    Check if the player's rectangle coincides with any of the coins' circle,
    return the multiplier of the coin, and delete the coin from the COINS.

    Args:
        player (Player): The player object.

    Returns:
        int: The multiplier of the coin (if any).
    """
    player_center = player.rect.center
    multiplier = 0

    # Acquire the lock
    coin_lock.acquire()

    try:
        # Iterate over coins to check if the player overlaps with any of them
        for coin_id, (coin_pos, coin_multiplier) in COINS.items():
            coin_center = coin_pos
            coin_radius = COIN_RADIUS * coin_multiplier

            # Calculate the distance between the centers of the player and the coin
            distance = (
                (coin_center[0] - player_center[0]) ** 2
                + (coin_center[1] - player_center[1]) ** 2
            ) ** 0.5

            # Check if the distance is less than the sum of the player's radius and coin's radius
            if distance <= (player.rect.width / 2 + coin_radius):
                multiplier = coin_multiplier
                del COINS[coin_id]  # Remove the grabbed coin from COINS
                break  # No need to check further if a coin is grabbed
    finally:
        # Release the lock
        coin_lock.release()

    return multiplier

def handle_client(conn, player_id):
    """
    Handle client connection.

    Args:
        conn (socket.socket): The client socket object.
        player_id (str): The unique identifier for the player.
    """
    try:
        # Send connected player's details
        conn.send(pickle.dumps(PLAYERS[player_id]))

        while True:
            # Receive data from the client
            data = pickle.loads(conn.recv(BUFFER_SIZE))
            PLAYERS[player_id] = data

            multiplier = grab_coin(PLAYERS[player_id])

            if not data:
                print("Player disconnected:", player_id)
                break
            else:
                # Send opponents' data to the player
                opponents = {
                    p_id: d for p_id, d in PLAYERS.items() if p_id != player_id
                }
                reply = {
                    "opponents": opponents,
                    "coins": COINS,
                    "multiplier": multiplier,
                }
                conn.sendall(pickle.dumps(reply))
    except Exception as e:
        print("Error:", str(e))
    finally:
        del PLAYERS[player_id]
        conn.close()

def generate_coins():
    """Generate coins at random time intervals."""
    while True:
        if len(COINS) > MAX_COINS:
            pass
        time.sleep(random.randint(MIN_GENERATE_INTERVAL, MAX_GENERATE_INTERVAL))
        coin_id = str(uuid.uuid4())
        COINS[coin_id] = generate_coin()

def main():
    """Main function to run the server."""
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the socket to the server address and port
        s.bind((SERVER, PORT))
        print("Waiting for connections. Server started.")
    except socket.error as e:
        print("Error:", str(e))
        return

    # Start the coin generation thread
    threading.Thread(target=generate_coins).start()

    while True:
        # Listen for incoming connections
        s.listen()
        conn, addr = s.accept()
        print("Connected to:", addr)

        # Start a new thread to handle the client
        player_id = str(uuid.uuid4())
        PLAYERS[player_id] = Player(
            player_id,
            *get_random_pos(),
            PLAYER_WIDTH,
            PLAYER_HEIGHT,
            get_random_character(),
        )
        threading.Thread(target=handle_client, args=(conn, player_id)).start()

if __name__ == "__main__":
    main()
