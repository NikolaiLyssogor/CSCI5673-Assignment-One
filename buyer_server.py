import socket
from utils import TCPHandler

class BuyerServer:

    def __init__(self):
        self.handler = TCPHandler()
    
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