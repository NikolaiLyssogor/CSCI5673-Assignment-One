import socket
from utils import TCPHandler
import json

class CustomerDB:

    def __init__(self):
        """
        Sets up data structures used for saving information about
        buyers and sellers. See the example below for the objects
        that hold seller and buyer info.

        Seller:
        {
            'name': 'John Carmack',
            'id': 1,
            'feedback': {'pos': 10, 'neg': 0},
            'items_sold': 4
        }

        Buyer:
        {
            'name': 'Andrej Karpathy',
            'id': 1,
            'items_purchased': 19
        }
        """
        self.sellers = []
        self.buyers = []

    def _route_request(self, msg: bytes):
        """
        Parses the TCP byte stream to determine the appropriate action.
        """
        raise NotImplementedError

    def create_account(self):
        raise NotImplementedError

    def login(self):
        raise NotImplementedError

    def logout(self):
        raise NotImplementedError

    def get_seller_rating(self):
        raise NotImplementedError

    def get_num_items_sold(self):
        raise NotImplementedError

    def provide_feedback(self):
        raise NotImplementedError

    def get_num_items_bought(self):
        raise NotImplementedError



if __name__ == "__main__":
    db = CustomerDB()
    handler = TCPHandler()
    PORT = 65432

    # Socket will close() on its own when context exited
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('', PORT))
        sock.listen(5) # Allow 5 clients to be queued
        print("customer database listening for connections")

        # Main accept() loop
        while True:
            new_sock, client_addr = sock.accept()
            print(f"Accepted connection from {client_addr}.")
            data = handler.recv(new_sock)
            route = db._route_request(data['route'])
            response = route(data)
            send_status = handler.send(new_sock, response)
            handler.send(new_sock, {"status":"success!"})
            new_sock.close()
            print(f"Disconnected from {client_addr}.")