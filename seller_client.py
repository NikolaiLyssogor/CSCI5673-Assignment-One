import socket
from utils import TCPHandler
import sys

class SellerClient:

    def __init__(self):
        self.handler = TCPHandler()
        self.is_logged_in = False

        self.routes = {
            'create account': self.create_account,
            'login': self.login,
            'logout': self.logout,
            'get seller rating': self.get_rating,
            'sell item': self.sell_item,
            'remove item': self.remove_item,
            'list item': self.list_items,
            'exit': None # handled differently due to different args
        }

    def create_account(self, debug: bool = True) -> bool:
        """
        Gets a username and password from the user and sends
        it to the server to be stored. 

        :param debug: If true, runs the function in an interactive
                      mode on the command line. If false, uses pre-
                      generated input for performance testing.
        return: True, if a new account was succesfully created, false
                otherwise.
        """
        # User cannot create account if logged in
        if self.is_logged_in:
            print("You are already logged in. You cannot create an account.\n")
            return False

        if debug == True:
            # Get user input
            print("Please provide a username and password.")
            username = input("\nusername: ")
            password = input("password: ")

            data = {
                'route': 'create_account',
                'username': username,
                'password': password
            }

            # Get a connection and send the request to the server
            sock = self.handler.get_conn(dest='seller_server')
            self.handler.send(sock, data)

            # Handle the response from the server
            resp = self.handler.recv(sock)
            sock.close()

            if 'Success' in resp['status']:
                return True
            else:
                print(resp['status'])
                return False

        elif debug == False:
            return False


    def login(self, uname: str, pwd: str):
        pass

    def logout(self):
        pass

    def get_rating(self):
        pass

    def sell_item(self):
        raise NotImplementedError

    def remove_item(self):
        raise NotImplementedError

    def list_items(self):
        raise NotImplementedError

    def _get_route(self, route: str):
        return self.routes[route]

    def serve_debug(self):
        """
        Runs the server in an interactive mode through the 
        command line. Pass 'test' as argv[1] for performance
        testing.
        """
        while True:
            # Get user input
            actions = list(self.routes.keys())
            action = input(f"What would you like to do?\n{actions}\n")

            # Check that action is valid
            if action not in actions:
                print("\nUnknown action. Please select another.\n")
                continue

            # Execute the action specified
            if action == 'exit':
                exit()

            result = self.routes[action](debug=True)
            if result == False:
                print("Action failed, try again.\n")

    def serve_test(self):
        raise NotImplementedError



if __name__ == "__main__":
    seller = SellerClient()
    if sys.argv[1] == 'debug':
        seller.serve_debug()
    elif sys.argv[1] == 'test':
        seller.serve_test()
    else:
        print("Invalid command line argument supplied.")
        exit(1)



