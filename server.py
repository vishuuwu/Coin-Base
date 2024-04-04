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
    MAX_COINS,
    MIN_GENERATE_INTERVAL,
    MAX_GENERATE_INTERVAL,
    SERVER,
    PORT,
    BUFFER_SIZE,
    WINNING_POINTS,
)

# Global variables
WINNER_FOUND = False
WINNER_NAME = None
COINS = []
PLAYERS = {}
coin_lock = threading.Lock()


def check_for_winner():
    """
    Check if any player has reached the winning score.
    If a winner is found, set the global variable WINNER_FOUND to True.
    """
    global WINNER_FOUND, WINNER_NAME
    for player_id, player in PLAYERS.items():
        if player.score >= WINNING_POINTS:
            WINNER_FOUND = True
            WINNER_NAME = player.name
            return
    WINNER_FOUND = False


def check_winner_thread():
    """Continuously check for a winner in a separate thread."""
    while not WINNER_FOUND:
        time.sleep(1)
        check_for_winner()


def generate_coins():
    """Generate coins at random time intervals."""
    global COINS
    while not WINNER_FOUND:
        if len(COINS) > MAX_COINS:
            continue

        time.sleep(random.randint(MIN_GENERATE_INTERVAL, MAX_GENERATE_INTERVAL))
        coin = generate_coin()  # Generate a new coin
        COINS.append(coin)  # Add the coin to the list


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
        coins_to_remove = []  # Store indices of coins to be removed
        for index, (coin_pos, coin_multiplier) in enumerate(COINS):
            coin_center = coin_pos
            coin_radius = COIN_RADIUS * coin_multiplier

            # Calculate the squared distance between the player and the coin
            dx = coin_center[0] - player_center[0]
            dy = coin_center[1] - player_center[1]
            distance_squared = dx * dx + dy * dy

            # Calculate the squared sum of radii
            sum_of_radii_squared = (player.rect.width / 2 + coin_radius) ** 2

            # Check if the squared distance is less than or equal to the squared sum of radii
            if distance_squared <= sum_of_radii_squared:
                multiplier = coin_multiplier
                coins_to_remove.append(index)  # Add index of coin to removal list

        # Remove grabbed coins from COINS (in reverse order to avoid index shifting)
        for index in reversed(coins_to_remove):
            del COINS[index]
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
    global WINNER_NAME
    try:
        # Send connected player's details
        conn.send(pickle.dumps(PLAYERS[player_id]))

        while True:
            # Receive data from the client
            data = conn.recv(BUFFER_SIZE)
            if not data:
                print("Player disconnected:", player_id)
                break

            try:
                received_data = pickle.loads(data)
                PLAYERS[player_id] = received_data

                multiplier = grab_coin(PLAYERS[player_id])

                # Send opponents' data to the player
                opponents = {
                    p_id: d for p_id, d in PLAYERS.items() if p_id != player_id
                }
                reply = {
                    "winner": WINNER_NAME,
                    "opponents": opponents,
                    "coins": COINS,
                    "multiplier": multiplier,
                }
                conn.sendall(pickle.dumps(reply))
            except pickle.UnpicklingError:
                print("Error: Invalid pickle data received")
    except Exception as e:
        print("Error:", str(e))
    finally:
        # Remove the disconnected player from opponents dictionary
        if player_id in opponents:
            del opponents[player_id]

        del PLAYERS[player_id]
        conn.close()


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

    # Start the winner checking thread
    threading.Thread(target=check_winner_thread).start()
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
