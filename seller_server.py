import socket
from utils import TCPHandler

class SellerServer:

    def __init__(self):
        self.handler = TCPHandler()

        # Used for routing clients' requests
        self.routes = {
            'create account': self.create_account,
            'login': self.login,
            'logout': self.logout
            # 'get seller rating': self.get_rating,
            # 'sell item': self.sell_item,
            # 'remove item': self.remove_item,
            # 'list item': self.list_items,
        }
    
    def create_account(self, data: dict) -> dict:
        """
        Adds the user to the customer database.

        :param data: The packet passed over TCP.
        :returns: A dictionary with one field containing a status
                  message.
        """
        # Get a socket connected to the DB
        db_socket = self.handler.get_conn('customer_db')
        self.handler.send(db_socket, data)

        # Get back the response
        db_response = self.handler.recv(db_socket)

        # Form the response to the client
        if 'Error' in db_response['status']:
            resp = {'status': 'Error: database'}
        else:
            resp = {'status': 'Success: account created'}

        db_socket.close()

        return resp

    def login(self, uname: str, pwd: str):
        pass

    def logout(self):
        pass

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