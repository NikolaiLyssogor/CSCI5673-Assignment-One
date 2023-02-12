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
            'add item to cart': self.add_item_to_cart,
            'remove item from cart': self.remove_item_from_cart,
            'clear cart': self.clear_cart,
            'display cart': self.display_cart,
            'make purchase': self.make_purchase,
            'provide feedback': self.provide_feedback,
            'get seller rating': self.get_seller_rating_by_id,
            'get purchase history': self.get_purchase_history,
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
        self.username = ""
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

    def add_item_to_cart(self):
        """
        User provides an item ID and the item is added to 
        the local shopping cart. Checks if item exists in
        the database before doing so.

        Note: This function differs from the assignment's
        specification in that because all items have their
        own uniuqe ID, a buyer will have to specify the ID
        for each item individually, even if some of those
        items are the same type of product.
        """
        if not self.is_logged_in:
            print("\nYou must log in before adding items to your cart.")
        else:
            # Get user input
            item_id = int(input("\nPlease provide the ID for the item you wish to purchase.\n"))

            # Check if the item exists in the database
            try:
                data = {
                    'route': 'check_if_item_exists',
                    'data': {'id': item_id}
                }
                resp = self.handler.sendrecv('buyer_server', data)
            except:
                print("\nThere was a problem with the server. Please try again.")
            else:
                # Add the item to the cart
                self.cart.append(resp['data'])
                print(f"\nItem with ID {item_id} ({resp['data']['name']}) was added to the cart.")

    def remove_item_from_cart(self):
        """
        Removes the item ID specified by the user from
        the cart.
        """
        item_id = int(input("\nSpecify the ID of the item you wish to remove.\n"))
        item_found = False

        for item in self.cart:
            if item['id'] == item_id:
                self.cart.remove(item)
                item_found = True
                print(f"\nItem with ID {item_id} ({item['name']}) was removed from the cart.")
                break

        if not item_found:
            print("\nThe item specified is not in your cart.")

    def clear_cart(self):
        self.cart = []
        print("\nYour cart has been cleared.")

    def display_cart(self):
        if not self.cart:
            print("\nYour cart is empty.")
        else:
            for item in self.cart:
                print("")
                pp.pprint(item)

    def make_purchase(self):
        raise NotImplementedError

    def provide_feedback(self):
        raise NotImplementedError

    def get_seller_rating_by_id(self):
        # Get seller ID from user
        seller_id = int(input("\nPlease provide the ID for the seller whose rating you wish to view.\n"))

        # Check if the item exists in the database
        try:
            data = {
                'route': 'get_seller_rating_by_id',
                'data': {'id': seller_id}
            }
            resp = self.handler.sendrecv('buyer_server', data)
        except:
            print("\nThere was a problem with the server. Please try again.")
        else:
            # Print the seller's rating
            if 'Error' in resp['status']:
                print("\n", resp['status'])
            else:
                pos, neg = resp['data']['pos'], resp['data']['neg']
                print(f"\nSeller with ID {seller_id} has {pos} thumbs up and {neg} thumbs down.")

    def get_purchase_history(self):
        try:
            data = {
                'route': 'get_purchase_history',
                'data': {'username': self.username}
            }
            resp = self.handler.sendrecv('buyer_server', data)
        except:
            print("\nThere was a problem with the server. Please try again.")
        else:
            print(resp)
            if not resp['data']:
                print("\nYou have not made any purchases.")
            else:
                for purchase in resp['data']:
                    print("")
                    pp.pprint(purchase)

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



