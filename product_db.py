import socket
import copy
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
            'buyer': None                       # Buyer name if status is 'Sold'
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
        item = data['data']
        quantity = item['quantity']
        del item['quantity']
        
        item_ids = []
        for _ in range(quantity):
            item_copy = copy.deepcopy(item)
            _id = len(self.products) + 1
            item_copy['id'] = _id
            item_ids.append(_id)
            self.products.append(item_copy)

        return {'status': 'Sucess: Items listed.', 'ids': item_ids}

    def remove_item(self, data: dict) -> dict:
        ids = data['data']['ids']
        items_removed = 0
        
        for item in self.products:
            if item['id'] in ids:
                item['status'] = 'Removed'
                items_removed += 1

        if items_removed == len(ids):
            return {'status': 'Success: Items successfully removed.'}
        else:
            return {'status': 'Error: Some items may not have been removed.'}

    def list_items(self, data: dict) -> dict:
        """
        Returns items for sale by the seller specified.
        """
        sellers_items = []
        seller = data['data']['username']

        for item in self.products:
            if item['seller'] == seller and item['status'] == 'For Sale':
                sellers_items.append(item)

        resp = {
            'status': 'Success',
            'items': sellers_items
        }

        return resp

    def search(self, data: dict) -> dict:
        """
        Simply return the products. Processing happens
        on the buyer server.
        """
        return {'data': self.products}

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

            # Send the response
            self.handler.send(new_sock, response)

            # No longer need that connection
            new_sock.close()
            print(f"Disconnected from {client_addr}.")


if __name__ == "__main__":
    product_db = ProductDB()
    product_db.serve()