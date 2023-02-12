import multiprocessing as mp

from seller_client import SellerClient
from buyer_client import BuyerClient

class Experiment:
    """
    Spins up the client servers and runs the experiment.
    """

    def single_server_experiment(self):
        """
        Makes 10,000 API calls from one instance of the seller
        and one instance of the buyer.
        """
        # # Initialize server object
        seller_client = SellerClient(debug = False)
        # buyer_client = BuyerClient(debug = False)
        seller_client.serve()
        average_response_time = seller_client.benchmarker.compute_average_response_time()
        print(f"The average response time was: {average_response_time}")

        # # Fork two processes in which to run the servers
        # seller_proc = mp.Process(target=seller_client.serve, args=(False,))
        # buyer_proc = mp.Process(target=buyer_client.serve, args=(False,))
        # seller_proc.start()
        # buyer_proc.start()

        # # Complete the processes
        # seller_proc.join()
        # buyer_proc.join()

if __name__ == "__main__":
    experiment = Experiment()
    experiment.single_server_experiment()