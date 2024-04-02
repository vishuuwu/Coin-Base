import socket
import pickle

class Network:
    """
    A class to handle network communication.

    Attributes:
        server (str): The IP address of the server.
        port (int): The port number for communication.
        addr (tuple): A tuple containing the server IP address and port number.
        client (socket.socket): The client socket object.
        id (str): The unique identifier received upon connection.
    """

    def __init__(self):
        """
        Initializes the Network object.
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.29.15"
        self.port = 5555
        self.addr = (self.server, self.port)
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
            print("Error:", e)
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
        except socket.error as e:
            print("Error:", e)
            return None


# Example usage
# if __name__ == "__main__":
#     n = Network()
#     print(n.send("hello"))
