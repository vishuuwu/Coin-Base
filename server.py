import socket
import threading

SERVER = "192.168.29.15"
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((SERVER, PORT))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for connections. Server started.")


def handle_client(conn):
    """Handle client connection."""
    conn.send(str.encode("connected"))
    while True:
        try:
            data = conn.recv(2048)
            if not data:
                print("Disconnected.")
                break
            else:
                reply = data.decode("utf-8")
                print("Received:", reply)
                print("Sending:", reply)
                conn.sendall(str.encode(reply))
        except Exception as e:
            print("Error:", str(e))
            break
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    threading.Thread(target=handle_client, args=(conn,)).start()