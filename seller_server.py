import socket
from utils import TCPHandler

class SellerServer:

    def __init__(self):
        self.handler = TCPHandler()
    
    def create_account(self, debug: bool = True) -> bool:
        pass


    def login(self, uname: str, pwd: str):
        pass

    def logout(self):
        pass

    def serve(self):
        # Socket will close() on its own when context exited
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(('', self.handler.SELPORT))
            sock.listen(5) # Allow 5 clients to be queued
            print("seller server listening for connections")

            # Main accept() loop
            while True:
                new_sock, client_addr = sock.accept()
                print(f"Accepted connection from {client_addr}.")
                data = handler.recv(new_sock)
                route = db._route_request(data['route'])
                response = route(data)
                send_status = handler.send(new_sock, response)
                handler.send(new_sock, {"status":"success!"})
                new_sock.close()
                print(f"Disconnected from {client_addr}.")


if __name__ == "__main__":
    server = SellerServer()
    server.serve()