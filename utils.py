import socket
import json

class TCPHandler:
    """
    Defines an application-layer protocol for sending and
    receiving data over TCP. 
    """

    def __init__(self):
        # Size of TCP packets in bytes
        self.MSGLEN = 2048

        # Hostname and port no. of the frontend seller server
        self.address_book = {
            'customer_db': {'host': 'localhost', 'port': 65432},
            'seller_server': {'host': 'localhost', 'port': 65431},
            'buyer_server': {'host': 'localhost', 'port': None},
            'product_db': {'host': 'localhost', 'port': 65430}
        }

    def get_conn(self, dest: str) -> socket.socket:
        """
        Used by clients to connect to the seller server or 
        the buyer server.

        :param dest: One of 'seller', 'buyer', 'customer_db', or 'product_db'.
        returns: A socket connected to the destination.
        """
        if dest not in ['seller_server', 'buyer_sever', 'customer_db', 'product_db']:
            raise ValueError("invalid destination supplied.")
        
        new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_sock.connect((self.address_book[dest]['host'],
                          self.address_book[dest]['port']))
        return new_sock

    def get_listener(self, host: str) -> socket.socket:
        """
        Returns an appropriate listening socket for the server
        specified as host.

        :param host: The server that needs the listening port. One of
                     'customer_db', 'seller_server', 'buyer_server',
                     'products_db'.
        returns: A socket listening to the appropriate port.
        """
        if host not in ['customer_db', 'seller_server',
                        'buyer_server', 'product_db']:
            raise ValueError("invalid host supplied")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.address_book[host]['host'],
                   self.address_book[host]['port']))
        sock.listen(5)
        return sock

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

    def sendrecv(self, dest: str, data: dict) -> dict:
        """
        Handles call and response over TCP.

        :param dest: The server we're sending the request to.
        :param data: The packet we're sending.

        :return: The response as a dictionary. Usually a status message.
        """
        # Get a new socket for each request
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to our destination port
            sock.connect((self.address_book[dest]['host'],
                          self.address_book[dest]['port']))

            # Encode the message and send it 
            msg = bytes(json.dumps(data), 'utf-8')
            sock.sendall(msg)

            # Receive the response and decoded it
            resp = sock.recv(self.MSGLEN)
            return json.loads(resp.decode('utf-8'))