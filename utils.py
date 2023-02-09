import socket
import json

class TCPHandler:
    """
    Defines an application-layer protocol for sending and
    receiving data over TCP. 
    """

    def __init__(self):
        self.MSGLEN = 2048

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
