# Performance Results
Here are the throughput and average response time metrics for the three scenarios outlined in the assignment description:

One client pair:

    throughput: 3.0992730411977374
    average response time: 0.009425467332204182
    
Ten client pairs:

    throughput: 16.40571589703376
    average response time: 0.16181823141496812
    
100 client pairs: 

    throughput: N/A
    average response time: 0.6769386267312599
    
 Note that in the ten and 100 client pairs scenarios, some of the processes seemd to die, as not all of them reported their average response time. The mechanism for measuring throughput also failed in the 100 client pairs example, likely due to my lack of experience with concurrent programming.
 
 Nevertheless, the reported numbers are about what one would expect. The average response time increased as did the number of concurrent users. That is, the more requests the server has to deal with at once, the longer it takes to process any one request. Throughput increased as the number of concurrent users did from two to twenty because with the rate the client was sending requests, the server wasn't under much stress. When running 200 users at once, my whole computer because noticably slow, which wasn't the case for the first two experiments. 
