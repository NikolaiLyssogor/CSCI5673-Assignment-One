import socket

class TCPHandler:
    """
    Defines an application-layer protocol for sending and
    receiving data over TCP. 
    """

    def __init__(self):
        pass

    def send(sock: socket.socket, msg: bytes):
        raise NotImplementedError

    def recv(sock: socket.socket) -> bytes:
        raise NotImplementedError