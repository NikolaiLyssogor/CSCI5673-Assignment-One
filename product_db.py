import socket
from utils import TCPHandler


class ProductDB:

    def __init__(self):
        """
        Products are dictionaries with the following format:
        {
            'name': 'Toothbrush',
            'category': 4                       # Integer 0-9
            'id': 1                             # Maintained by server
            'keywords': ['bathroom', 'clean']   # Up to 5, 8 char max each
            'condition': 'Used'                 # 'New' or 'Used'
            'price': 1.99
            'seller': 'Ashish Vaswani',         # Username of seller
            'status': 'For Sale'                # ['For Sale', 'Sold', 'Removed']
        }
        """
        self.handler = TCPHandler()
        self.products = []

    def sell_item(self, data: dict) -> dict:
        """
        Adds items to the database,

        :param data: The item information.
        :returns: A list of item IDs corresponding to the 
                  items just added.
        """
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
        productdb_socket = self.handler.get_listener('product_db')
        print("Product database waiting for incoming connections.\n")

        # Main accept() loop
        while True:
            # Accept a new request from a client
            new_sock, client_addr = productdb_socket.accept()
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