import socket
from utils import TCPHandler

class SellerServer:

    def __init__(self):
        self.handler = TCPHandler()
    
    def create_account(self, data: dict) -> dict:
        """
        Adds the user to the customer database.

        :param data: The packet passed over TCP.
        :returns: A dictionary with one field containing a status
                  message.
        """
        # Make a call to the customer database
        db_response = self.handler.sendrecv(dest='customer_db', data=data)

        # Form the response to the client
        if 'Error' in db_response['status']:
            resp = {'status': 'Error: database'}
        else:
            resp = {'status': 'Success: account created'}

        return resp

    def login(self, data: dict) -> dict:
        # Make a call to the customer database
        return self.handler.sendrecv(dest='customer_db', data=data)

    def get_seller_rating(self, data: dict) -> dict:
        db_resp = self.handler.sendrecv(dest='customer_db', data=data)
        pos, neg = db_resp['user']['feedback']['pos'], db_resp['user']['feedback']['neg']
        resp = {
            'status': db_resp['status'],
            'pos': pos,
            'neg': neg
        }
        return resp

    def sell_item(self, data: dict) -> dict:
        """
        Adds the item to the product database and the item's
        ID to the list of items for sale by this user. Returns
        the IDs of the items added.
        """
        # Add the items and get a list of item ids
        prodDB_resp = self.handler.sendrecv('product_db', data)

        # Packet to send to customer DB
        custDB_req = {
            'route': 'sell_item',
            'ids': prodDB_resp['ids'],
            'username': data['data']['seller']
        }

        return self.handler.sendrecv('customer_db', custDB_req)

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
        seller_socket = self.handler.get_listener('seller_server')
        print("Seller server waiting for incoming connections.\n")

        # Main accept() loop
        while True:
            # Accept a new request from a client
            new_sock, client_addr = seller_socket.accept()
            print(f"Accepted connection from {client_addr}.\n")
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
    server = SellerServer()
    server.serve()