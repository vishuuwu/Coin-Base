import socket
import threading

SERVER = "192.168.29.15"
PORT = 5555

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Bind the socket to the server address and port
    s.bind((SERVER, PORT))
except socket.error as e:
    print("Error:", str(e))

# Listen for incoming connections
s.listen(2)
print("Waiting for connections. Server started.")
pos = [(0, 0), (100, 100)]


def read_pos(str):
    str = str.split(",")
    return (int(str[0]), int(str[1]))


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def handle_client(conn, player):
    """
    Handle client connection.

    Args:
        conn (socket.socket): The client socket object.
    """
    # Send connection confirmation message to the client
    conn.send(str.encode(make_pos(pos[player])))

    while True:
        try:
            # Receive data from the client
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data
            if not data:
                print("Disconnected.")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                # print("Received:", reply)
                # print("Sending:", reply)
                # Send the received data back to the client
                conn.sendall(str.encode(make_pos(reply)))
        except Exception as e:
            print("Error:", str(e))
            break

    # Close the connection with the client
    
    conn.close()


currentPlayer = 0
while True:
    # Accept incoming connection
    conn, addr = s.accept()
    print("Connected to:", addr)
    # Start a new thread to handle the client
    threading.Thread(target=handle_client, args=(conn, currentPlayer)).start()
    currentPlayer += 1
