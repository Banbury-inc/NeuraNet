# Neuranet CLI Tool

### Run the inference server

```bash
python -m petals.cli.run_server meta-llama/Meta-Llama-3-8B-instruct --new_swarm  
```


- I did a ton of work related to connecting devices and sharing device resources
- Allocating files based on the device's capabilities 
- Allocating files based on the devices wifi speed
- I basically was able to successfully accomplish SSD sharing. 

- The next step is to do the same thing with RAM, CPU, GPU. 
- Which one is easiest?


- Allow devices to participate in distributed inference

- petals works and is actually pretty fast... what's next?
    - handle connection stuff better than it is now
    - advanced quantization
    - optimized load balancing
        - intelligent load balancing
        - dynamic resource allocation
    - improved fault tolerance

- ideas
    - similar to having multiple files, have mirrored blocks for the most unreliable devices
    - algorithm to determine the optimal allocation of blocks according to each devices capabilities
    - the purpose for the algorithm is to not only protect against failure, but also measure latency, 
    throughput, network performance, and all metrics in order to ensure that the inference is done 
    as quickly as possible.






