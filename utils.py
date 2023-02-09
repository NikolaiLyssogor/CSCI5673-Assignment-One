import socket
import json

class TCPHandler:
    """
    Defines an application-layer protocol for sending and
    receiving data over TCP. 
    """

    def __init__(self):
        self.MSGLEN = 2048

        # Hostname and port no. of the frontend seller server
        self.address_book = {
            'customer_db': {'host': 'localhost', 'port': 65432},
            'seller_server': {'host': 'localhost', 'port': 65431},
            'buyer_server': {'host': 'localhost', 'port': None},
            'products_db': {'host': 'localhost', 'port': None}
        }
        self.SELHOST = 'localhost'
        self.SELPORT = 65430

    def get_conn(self, dest: str) -> socket.socket:
        """
        Used by clients to connect to the seller server or 
        the buyer server.

        :param dest: One of 'seller', or 'buyer'.
        returns: A socket connected to the destination.
        """
        if dest not in ['seller', 'buyer']:
            raise ValueError("invalid destination supplied.")
        
        if dest == 'seller':
            new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_sock.connect((self.SELHOST, self.SELPORT))
            return new_sock
        elif dest == 'buyer':
            raise NotImplementedError

    def listen(self, host: str) -> socket.socket:
        """
        Returns an appropriate listening socket for the server
        specified as host.

        :param host: The server that needs the listening port. One of
                     'customer_db', 'seller_server', 'buyer_server',
                     'products_db'.
        returns: A socket listening to the appropriate port.
        """
        if host not in ['customer_db', 'seller_server',
                        'buyer_server', 'products_db']:
            raise ValueError("invalid host supplied")
        


    def send(self, sock: socket.socket, data: dict) -> None:
        """
        UTF-8 byte encodes JSON from the passed dictionary and
        sends it over the TCP socket.
        """
        # UTF-8 byte-encode the data as JSON
        msg = bytes(json.dumps(data), 'utf-8')

        # Send until the data is all out
        sock.sendall(msg)

    def recv(self, sock: socket.socket) -> dict:
        """
        Handles receiving bytes over TCP. Messages will always
        be UTF-8 encoded JSON. 
        """
        # Receive the message from the socket
        msg = sock.recv(self.MSGLEN)

        # Decode the message into a dictionary
        return json.loads(msg.decode('utf-8'))
