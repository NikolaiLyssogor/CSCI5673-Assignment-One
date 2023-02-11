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
            'items_purchased': 4
        }
        """
        self.handler = TCPHandler()
        # The 'database' itself
        self.sellers = []
        self.buyers = []

    def _route_request(self, route: str):
        """
        Returns the appropriate function if it exists,
        otherwise returns None.
        """
        if hasattr(self, route):
            return getattr(self, route)
        else:
            return None

    def create_account(self, data: dict) -> dict:
        if 'username' not in data.keys() or 'password' not in data.keys():
            return {'status': 'Error: Invalid packet supplied to create_account.'}

        # Add the new user
        self.sellers.append({
            'username': data['username'],
            'password': data['password'],
            'id': len(self.sellers) + 1,
            'feedback': {'pos': 0, 'neg': 0},
            'items_sold': 0
        })

        print(self.sellers)

        return {'status': 'Success: Account created.'}

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

    def serve(self):
        # Get a listening socket from the TCPHandler
        customerdb_socket = self.handler.get_listener('customer_db')
        print("Customer database waiting for incoming connections.\n")

        # Main accept() loop
        while True:
            # Accept a new request from a client
            new_sock, client_addr = customerdb_socket.accept()
            print(f"Accepted connection from {client_addr}.")
            data = self.handler.recv(new_sock)

            # Figure out what function was called from the header and call it
            route = self._route_request(data['route'])
            if route:
                response = route(data)
            else:
                response = {'staus': 'Error: Invalid database route.'}

            # Send the response and check for errors in doing so
            self.handler.send(new_sock, response)

            # No longer need that connection
            new_sock.close()
            print(f"Disconnected from {client_addr}.")



if __name__ == "__main__":
    db = CustomerDB()
    db.serve()