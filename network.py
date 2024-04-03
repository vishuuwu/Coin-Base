import socket
import pickle
from game_config import SERVER, PORT

class Network:
    """
    A class to handle network communication with the server.

    Attributes:
        server (str): The IP address of the server.
        port (int): The port number for communication.
        addr (tuple): A tuple containing the server IP address and port number.
        client (socket.socket): The client socket object.
        player (str): The unique identifier received upon connection.
    """

    def __init__(self, server=SERVER, port=PORT):
        """
        Initializes the Network object with the server address and port.

        Args:
            server (str): The IP address of the server. Defaults to the value in game_config.
            port (int): The port number for communication. Defaults to 5555.
        """
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player = self.connect()

    def getPlayer(self):
        return self.player

    def connect(self):
        """
        Connects to the server and receives a unique identifier upon successful connection.

        Returns:
            str: The unique identifier received from the server.
        """
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            print("Error connecting to the server:", e)
            return None

    def send(self, data):
        """
        Sends data to the server and receives a response.

        Args:
            data (str): The data to be sent to the server.

        Returns:
            str: The response received from the server.
        """
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            print("Error sending data:", e)
            return None

    def disconnect(self):
        """
        Disconnects from the server.
        """
        try:
            self.client.close()
        except Exception as e:
            print("Error disconnecting from the server:", e)
