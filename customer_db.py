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
            'username': 'John Carmack',
            'id': 1,
            'feedback': {'pos': 10, 'neg': 0},
            'items_sold': [2, 3, 5, 4]
        }

        Buyer:
        {
            'username': 'Andrej Karpathy',
            'id': 1,
            'items_purchased': [2, 3]
        }
        """
        self.handler = TCPHandler()
        # The 'database' itself
        self.sellers = []
        self.buyers = []

    def create_account(self, data: dict) -> dict:
        if 'username' not in data.keys() or 'password' not in data.keys():
            return {'status': 'Error: Invalid packet supplied to create_account.'}

        if data['type'] == 'seller':
            # Add the new user
            self.sellers.append({
                'username': data['username'],
                'password': data['password'],
                'id': len(self.sellers) + 1,
                'feedback': {'pos': 0, 'neg': 0},
                'items_sold': 0
            })
        elif data['type'] == 'buyer':
            self.buyers.append({
                'username': data['username'],
                'password': data['password'],
                'id': len(self.buyers) + 1,
                'items_purchased': 0
            })

        return {'status': 'Success: Account created.'}

    def login(self, data: dict) -> dict:
        """
        Search the database for a user with the provided
        username and password.
        """
        unm, pwd = data['username'], data['password']
        users = self.sellers if data['type'] == 'seller' else self.buyers

        for user in users:
            if user['username'] == unm and user['password'] == pwd:
                return {'status': 'Success: Logged in successfully.'}
        
        return {'status': 'Error: Incorrect username or password.'}

    def get_seller_rating(self, data: dict) -> dict:
        """
        Return the seller feedback of a the specified user.
        """
        # Find the user we're looking for
        user_of_interest = None
        for user in self.sellers:
            if user['username'] == data['username']:
                user_of_interest = user
                break
        
        # Return the packet
        if user_of_interest == None:
            resp = {'status': 'Error: User not found.'}
        else:
            resp = {
                'status': 'Success',
                'user': user_of_interest 
            }

        return resp

    def get_all_sellers(self, data: dict) -> dict:
        data = {
            'status': 'Success: Here ya go.',
            'data': self.sellers
        }
        return data

    def get_num_items_sold(self):
        raise NotImplementedError

    def provide_feedback(self):
        raise NotImplementedError

    def get_num_items_bought(self):
        raise NotImplementedError

    def _route_request(self, route: str):
        """
        Returns the appropriate function if it exists,
        otherwise returns None.
        """
        if hasattr(self, route):
            return getattr(self, route)
        else:
            return None

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