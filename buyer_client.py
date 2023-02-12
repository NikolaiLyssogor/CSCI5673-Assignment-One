import socket
from utils import TCPHandler
import sys
import pprint

pp = pprint.PrettyPrinter()

class BuyerClient:

    def __init__(self):
        self.handler = TCPHandler()
        self.is_logged_in = False
        self.username = ""
        self.cart = []

        self.routes = {
            'create account': self.create_account,
            'login': self.login,
            'logout': self.logout,
            'search items': self.search,
            # 'add item to cart': self.add_item_to_cart,
            # 'remove item from cart': self.remove_item,
            # 'display cart': self.display_cart,
            # 'make purchase': self.make_purchase,
            # 'provide feedback': self.provide_feedback,
            # 'get seller rating': self.get_seller_rating,
            # 'get purchase history': self.get_purchase_history,
            'exit': None # handled differently due to different args
        }

    def create_account(self, debug=True):
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
                    'type': 'buyer',
                    'username': username,
                    'password': password
                }

                # Call the handler to send request and receive response
                resp = self.handler.sendrecv(dest='buyer_server', data=data)

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
            print("\nYou are already logged in.")
        else:
            # Get the username and password
            print("Please provide a username and password.")
            username = input("\nusername: ")
            password = input("password: ")

            data = {
                'route': 'login',
                'type': 'buyer',
                'username': username,
                'password': password
            }

            # Call the handler to send request and receive response
            resp = self.handler.sendrecv(dest='buyer_server', data=data)

            if 'Success' in resp['status']:
                self.is_logged_in = True
                self.username = data['username']
                print("\nYou are now logged in!")
            else:
                print("\n", resp['status'])

    def logout(self):
        self.is_logged_in = False
        print("\nYou are now logged out.")

    def search(self):
        """
        Search for items based on keywords.
        """
        print("Please provide the following information.")
        category = int(input("\nCategory (0-9): "))
        keywords = input("Keywords: ").split(',')

        data = {
            'route': 'search',
            'data': {
                'category': category,
                'keywords': keywords
            }
        }

        try:
            resp = self.handler.sendrecv('buyer_server', data)
            if 'Error' in resp['status']:
                print(resp['status'])
            else:
                if not resp['data']:
                    print("\nYour search did not return any results. Try a different query.")
                else:
                    for item in resp['data']:
                        print("")
                        pp.pprint(item)
        except:
            print('Error: Connection or server failed.')

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
    seller = BuyerClient()
    seller.serve_debug()



