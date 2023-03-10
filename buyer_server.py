import socket
from utils import TCPHandler

class BuyerServer:

    def __init__(self):
        self.handler = TCPHandler()
        self.n_requests = 0
    
    def create_account(self, data: dict) -> dict:
        """
        Adds the user to the customer database.

        :param data: The packet passed over TCP.
        :returns: A dictionary with one field containing a status
                  message.
        """
        try:
            # Make a call to the customer database
            return self.handler.sendrecv(dest='customer_db', data=data)
        except:
            return {'status': 'Error: Customer database.'}

    def login(self, data: dict) -> dict:
        # Make a call to the customer database
        return self.handler.sendrecv(dest='customer_db', data=data)

    def search(self, data: dict) -> dict:
        """
        Returns an item as a search result if either the 
        category matches or at least one of the keywords
        match.
        """
        # Get all the items from the database
        db_req = {'route': 'search'}
        try:
            all_items = self.handler.sendrecv('product_db', db_req)['data']

            # Filtering criteria
            category = data['data']['category']
            keywords = data['data']['keywords']

            # Filter the ones that meet the criteria
            search_result = []
            for product in all_items:
                # Add the item if the category matches
                if product['category'] == category:
                    search_result.append(product)
                    continue
                
                # Add item if any keywords match
                if len(set(product['keywords']) & set(keywords)) > 0:
                    search_result.append(product)

            # Send the response back
            return {'status': 'Success', 'data': search_result}
        except:
            return {'status': 'Error: Database'}

    def check_if_item_exists(self, data: dict) -> dict:
        """
        Gets all the products from the database and
        checks if the specified product ID exists.
        """
        try:
            db_req = {'route': 'search'}
            all_products = self.handler.sendrecv('product_db', db_req)['data']
        except:
            return {'status': 'Error: Database connection.'}
        else:
            # Look for the product of interest
            for product in all_products:
                if product['id'] == data['data']['id']:
                    resp = {
                        'status': 'Success: Item found.',
                        'data': product
                    }
                    return resp

            # Item not found
            return {'status': 'Error: Item not found.'}

    def get_seller_rating_by_id(self, data: dict) -> dict:
        try:
            db_req = {'route': 'get_all_sellers'}
            db_resp = self.handler.sendrecv('customer_db', db_req)
        except:
            print("Error connecting server to customer database.")
            return {'status': 'Error: Cannot connect buyer server to customer database.'}
        else:
            seller_id = data['data']['id']
            for seller in db_resp['data']:
                if seller['id'] == seller_id:
                    resp = {
                        'status': db_resp['status'],
                        'data': {
                            'pos': seller['feedback']['pos'],
                            'neg': seller['feedback']['neg']
                        }
                        
                    }
                    return resp

            return {'status': 'Error: Seller not found.'}

    def get_purchase_history(self, data: dict) -> dict:
        try:
            db_req = {'route': 'search'}
            products = self.handler.sendrecv('product_db', db_req)['data']
        except:
            print("Error connecting buyer server to product database.")
            return {'status': 'Error: Cannot connect buyer server to product database.'}
        else:
            buyers_products = []
            for product in products:
                if product['buyer'] == data['data']['username']:
                    buyers_products.append(product)

            resp = {
                'status': "Success: Here's your filthy data.",
                'data': buyers_products
            }
            return resp

    def get_request_count(self, data: dict) -> dict:
        return {'requests': self.n_requests}

    def _route_request(self, route: str):
        """
        Returns the appropriate function if it exists,
        otherwise returns None.

        :param route: Name of the function as a string.
        :returns: The function object if it exists, else None.
        """
        if hasattr(self, route):
            return getattr(self, route)
        else:
            return None


    def serve(self):
        # Get a listening socket from the TCPHandler
        seller_socket = self.handler.get_listener('buyer_server')
        print("Buyer server waiting for incoming connections.\n")

        # Main accept() loop
        while True:
            # Accept a new request from a client
            new_sock, client_addr = seller_socket.accept()
            print(f"Accepted connection from {client_addr}.\n")
            self.n_requests += 1
            data = self.handler.recv(new_sock)

            # Figure out what function was called from the header and call it
            route = self._route_request(data['route'])
            response = route(data)

            # Send the response and check for errors in doing so
            self.handler.send(new_sock, response)

            # No longer need that connection
            new_sock.close()
            print(f"Disconnected from {client_addr}.\n")


if __name__ == "__main__":
    server = BuyerServer()
    server.serve()