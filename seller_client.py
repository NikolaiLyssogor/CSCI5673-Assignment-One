import socket
from utils import TCPHandler
import sys

class SellerClient:

    def __init__(self):
        self.handler = TCPHandler()
        self.is_logged_in = False
        self.username = ""

        self.routes = {
            'create account': self.create_account,
            'login': self.login,
            'logout': self.logout,
            'get seller rating': self.get_seller_rating,
            'sell item': self.sell_item,
            'remove item': self.remove_item,
            'list item': self.list_items,
            'exit': None # handled differently due to different args
        }

    def create_account(self, debug: bool = True):
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
        else:
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

                # Call the handler to send request and receive response
                resp = self.handler.sendrecv(dest='seller_server', data=data)

                if 'Success' in resp['status']:
                    print("\nAccount created successfully!")
                else:
                    print(resp['status'])


    def login(self):
        """
        Change the local state to reflect that the user
        is logged in.
        """
        if self.is_logged_in:
            print("You are already logged in.")
        else:
            # Get the username and password
            print("Please provide a username and password.")
            username = input("\nusername: ")
            password = input("password: ")

            data = {
                'route': 'login',
                'username': username,
                'password': password
            }

            # Call the handler to send request and receive response
            resp = self.handler.sendrecv(dest='seller_server', data=data)

            if 'Success' in resp['status']:
                self.is_logged_in = True
                self.username = data['username']
                print("\nYou are now logged in!")
            else:
                print("\n", resp['status'])

    def logout(self):
        self.is_logged_in = False
        print("\nYou are now logged out.")

    def get_seller_rating(self):
        """
        Get the rating for the seller that is currently logged in.
        """
        if not self.is_logged_in:
            print("\nYou must log in to view your rating.")
        else:
            data = {
                'route': 'get_seller_rating',
                'username': self.username
            }
            
            # Send data to the server and get response back
            resp = self.handler.sendrecv(dest='seller_server', data=data)
            
            if 'Error' in resp['status']:
                print("\n", resp['status']),
            else:
                print(f"\nYou have {resp['pos']} thumbs up and {resp['neg']} thumbs down.")


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
            action = input(f"\nWhat would you like to do?\n{actions}\n")

            # Check that action is valid
            if action not in actions:
                print("\nUnknown action. Please select another.\n")
                continue

            # Execute the action specified
            if action == 'exit':
                exit()

            self.routes[action]()



if __name__ == "__main__":
    seller = SellerClient()
    seller.serve_debug()



