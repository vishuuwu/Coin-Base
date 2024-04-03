import socket
import threading
import uuid
import pickle

from player import Player
from game_config import (
    get_random_pos,
    get_random_color,
    get_random_character,
    get_wifi_ip,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    SERVER,
)

# SERVER = "192.168.29.15"
# SERVER = get_ip_address()


PORT = 5555

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Bind the socket to the server address and port
    s.bind((SERVER, PORT))
except socket.error as e:
    print("Error:", str(e))

# Listen for incoming connections
s.listen()
print("Waiting for connections. Server started.")


players = {}


def handle_client(conn, id):
    """
    Handle client connection.
    Args:
        conn (socket.socket): The client socket object.
    """
    # Send connected players details..
    conn.send(pickle.dumps(players[id]))

    while True:
        try:
            # Receive data from the client
            data = pickle.loads(conn.recv(2048))
            players[id] = data
            if not data:
                print("player id : ", id, " Disconnected.")

                break
            else:
                # sending oponents data to the player to draw them
                reply = {p_id: d for p_id, d in players.items() if p_id != id}
                conn.sendall(pickle.dumps(reply))
        except Exception as e:
            print("Error:", str(e))
            break
    del players[id]
    # print("on player diconnecting", len(players))
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    # Start a new thread to handle the client

    player_id = str(uuid.uuid4())
    players[player_id] = Player(
        *get_random_pos(), PLAYER_WIDTH, PLAYER_HEIGHT, get_random_character()
    )
    print(players[player_id])
    # print("on player connecting", len(players))
    threading.Thread(target=handle_client, args=(conn, player_id)).start()
