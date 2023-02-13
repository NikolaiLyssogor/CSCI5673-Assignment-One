import multiprocessing as mp
import numpy as np
import time

from seller_client import SellerClient
from buyer_client import BuyerClient
from seller_server import SellerServer
from buyer_server import BuyerServer
from utils import TCPHandler

"""
Code taken from:
https://www.youtube.com/watch?v=35yYObtZ95o
"""
handler = TCPHandler()
start = time.time() # For measuring server throughput

processes = []
for i in range(1):
    # Initialize server object
    seller_client = SellerClient(debug = False)
    buyer_client = BuyerClient(debug = False)
    # Fork two processes in which to run the servers
    seller_proc = mp.Process(target=seller_client.serve)
    buyer_proc = mp.Process(target=buyer_client.serve)

    # Needed to start the processes
    if __name__ == "__main__":
        # Start client processes
        seller_proc.start()
        buyer_proc.start()
        processes.append((seller_proc, buyer_proc))

# Let all the processes finish
for sp, bp in processes:
    sp.join()
    bp.join()

end = time.time()

# Send message to frontend servers to get request count
data = {'route': 'get_request_count'}
buyer_server_reqs = handler.sendrecv('buyer_server', data)['requests']
seller_server_reqs = handler.sendrecv('seller_server', data)['requests']

# Compute the throughput,
throughput = (buyer_server_reqs + seller_server_reqs)/(end-start)
print("Throughput:", throughput)

# Get the average from the text file dump
with open('tp_dump.txt', 'a') as file:
    file.write('Throughput: ' + str(throughput) + '\n')