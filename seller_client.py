import socket
import sys
import pprint
import time
import random
import string

from utils import TCPHandler, ResponseTimeBenchmarker

pp = pprint.PrettyPrinter()

class SellerClient:

    def __init__(self, debug: bool = True):
        self.handler = TCPHandler()
        self.benchmarker = ResponseTimeBenchmarker()
        self.is_logged_in = False
        self.username = ""
        self.debug = debug

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

    def create_account(self):
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
            if self.debug == True:
                # Get user input
                print("Please provide a username and password.")
                username = input("\nusername: ")
                password = input("password: ")
            else:
                username, password = self.benchmarker.get_username_and_password()

            data = {
                'route': 'create_account',
                'type': 'seller',
                'username': username,
                'password': password
            }

            # Call the handler to send request and receive response
            start = time.time()
            resp = self.handler.sendrecv(dest='seller_server', data=data)
            end = time.time()

            if not self.debug:
                self.benchmarker.log_response_time(end-start)

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
            if self.debug:
                # Get the username and password
                print("Please provide a username and password.")
                username = input("\nusername: ")
                password = input("password: ")
            else:
                # Login with any account that's already been created
                username, password = random.choice(self.benchmarker.accounts)

            data = {
                'route': 'login',
                'type': 'seller',
                'username': username,
                'password': password
            }

            # Call the handler to send request and receive response
            start = time.time()
            resp = self.handler.sendrecv(dest='seller_server', data=data)
            end = time.time()

            if not self.debug:
                self.benchmarker.log_response_time(end-start)

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
            start = time.time()
            resp = self.handler.sendrecv(dest='seller_server', data=data)
            end = time.time()

            if not self.debug:
                self.benchmarker.log_response_time(end-start)
            
            if 'Error' in resp['status']:
                print("\n", resp['status']),
            else:
                print(f"\nYou have {resp['pos']} thumbs up and {resp['neg']} thumbs down.")


    def sell_item(self):
        """
        Gather the attributes needed to list an item
        for sale.
        """
        if not self.is_logged_in:
            print("\nYou must be logged in to sell an item.")
        else:
            if self.debug:
                name = input("\nItem name: ")
                category = int(input("Item category: "))
                keywords = input("Item keywords: ").split(',')
                condition = input("Item condition: ")
                price = float(input("Item price: "))
                quantity = int(input("Item quantity: "))

                item = {
                    'name': name,
                    'category': category,
                    'keywords': keywords,
                    'condition': condition,
                    'price': round(price, 2),
                    'quantity': quantity,
                    'seller': self.username,
                    'status': 'For Sale',
                    'buyer': None
                }
            else:
                item = {
                    'name': ''.join(random.choice(string.ascii_lowercase) for _ in range(10)),
                    'category': random.choice(range(10)),
                    'keywords': self.benchmarker.get_keywords(),
                    'condition': random.choice(['New', 'Used']),
                    'price': round(random.uniform(0, 100), 2),
                    'quantity': random.choice(range(1,6)),
                    'seller': self.username,
                    'status': 'For Sale',
                    'buyer': None
                }

            data = {
                'route': 'sell_item',
                'data': item
            }

            start = time.time()
            resp = self.handler.sendrecv(dest='seller_server', data=data)
            end = time.time()

            if not self.debug:
                self.benchmarker.log_response_time(end-start)

            if 'Error' in resp['status']:
                print("\nUnable to list items for sale. Try again.")
            else:
                print("\nSuccessfully added items with IDs ", resp['ids'])


    def remove_item(self):
        """
        Asks user for a list of item ids to remove from the 
        database.
        """
        if not self.is_logged_in:
            print("\nPlease log in first.")
        else:
            if self.debug:
                ids = input("\nEnter a list of item IDs you want to remove:\n")
                ids = [int(i) for i in ids.split(',')]
            else:
                # Randomly remove 2 items with ids in [0, 500]
                ids = [random.choice(range(500)) for _ in range(2)]

            req = {
                'route': 'remove_item',
                'data': {
                    'ids': ids
                }
            }

            start = time.time()
            resp = self.handler.sendrecv('seller_server', req)
            end = time.time()

            if not self.debug:
                self.benchmarker.log_response_time(end-start)

            print(f"\n{resp['status']}")

    def list_items(self):
        """
        Display items currently on sale by this seller.
        """
        data = {
            'route': 'list_items',
            'data': {'username': self.username}
        }

        start = time.time()
        resp = self.handler.sendrecv('seller_server', data)
        end = time.time()

        if not self.debug:
            self.benchmarker.log_response_time(end-start)

        if not resp['items']:
            print("\nYou have no items for sale.")
        else:
            print("\nYou have the following items listed for sale:")
            for item in resp['items']:
                print('')
                pp.pprint(item)


    def _get_route(self, route: str):
        return self.routes[route]

    def serve(self):
        """
        Runs the server either in an interactive mode for debugging
        or an automated mode for performance testing.
        """
        if self.debug:
            # Run in interactive terminal mode
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
        else:
            # Calls functions in a predetermined order
            self.create_account()
            time.sleep(0.5)
            self.login()
            time.sleep(0.5)
            for _ in range(600):
                self.sell_item()
                time.sleep(0.5)
            for _ in range(300):
                self.remove_item()
                time.sleep(0.5)
            for _ in range(98):
                self.list_items()
                time.sleep(0.5)

            # Print average response time
            avg_response_time = self.benchmarker.compute_average_response_time()
            print("#######################################")
            print(f"Seller average response time: {avg_response_time}")
            print("***************************************")

            with open('art_dump.txt', 'a') as f:
                f.write(str(avg_response_time) + '\n')



if __name__ == "__main__":
    seller = SellerClient()
    seller.serve()



