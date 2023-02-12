import socket
import json
import numpy as np
import random
import string

class TCPHandler:
    """
    Defines an application-layer protocol for sending and
    receiving data over TCP. 
    """

    def __init__(self):
        # Size of TCP packets in bytes
        self.MSGLEN = 4096
        # Marks end of message
        self.DELIMITER = b'###DELIMITER###\0'

        # Hostname and port no. of the frontend seller server
        self.address_book = {
            'customer_db': {'host': 'localhost', 'port': 65432},
            'seller_server': {'host': 'localhost', 'port': 65431},
            'buyer_server': {'host': 'localhost', 'port': 65429},
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
        msg = bytes(json.dumps(data), 'utf-8') + self.DELIMITER

        # Send until the data is all out
        sock.sendall(msg)

    def recv(self, sock: socket.socket) -> dict:
        """
        Handles receiving bytes over TCP. Messages will always
        be UTF-8 encoded JSON. 
        """
        chunks = []
        while True:
            # Receive some or all of a message from the socket
            chunk = sock.recv(self.MSGLEN)
            chunks.append(chunk)
            # Scan the message for the delimiter
            if self.DELIMITER in chunk:
                break
        
        # Put the message back together
        msg = b''.join(chunks)
        # Remove the delimiter
        msg = msg[:-len(self.DELIMITER)]
        # Return the decoded message
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
            msg = bytes(json.dumps(data), 'utf-8') + self.DELIMITER
            sock.sendall(msg)

            # Receive the response and decode it
            return self.recv(sock)

class ResponseTimeBenchmarker:
    """
    Object belonging to each client server for them to 
    record their average response times.
    """

    def __init__(self):
        self.accounts = [] # (username, password) pairs
        self.keyword_choices = ['foo', 'bar', 'baz', 'bat', 'who', 'two', 'woo', 'soo', 'gaz', 'raz', 'car']
        self.response_times = []

    def log_response_time(self, response_time: float) -> None:
        """
        Called by the client when a request has been send
        and a response recieved.
        """
        self.response_times.append(response_time)

    def compute_average_response_time(self):
        """
        Should be called after 10 runs are completed. Returns
        the average response time.
        """
        return np.average(self.response_times)

    def get_username_and_password(self):
        """
        Saves and returns a random username and password.
        """
        uname = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        pwd = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        self.accounts.append((uname, pwd))
        return uname, pwd

    def get_keywords(self):
        """
        Returns a random array of keywords.
        """
        return [random.choice(self.keyword_choices) for _ in range(1, random.choice(range(2,6)))]




"""
ResponseTimeBenchmarker:

    - Has n usernames and passwords for seller and buyer
        - n is 1, 100, or 1000
    - Has 500 dummy items to list for sale
    - Gets delegated to by clients
        - Clients will record the response time for each API 
          call and send the result to this object
        - Object then computes the average at the end of the 
          experiment

    - One 'run' consists of the following:
        - create account
        - login
        - add 500 items
        - remove 200 items
        - list the items 298 times

ThroughputBenchmarker:

    - Timer starts when the server gets a request divisible by
      1000, including the first one
"""