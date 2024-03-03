## Things to consider when designing a multiple knapsack algorithm

### Devices
* Number of devices
* Total Storage of the devices
* Average amount of time the device is online (how reliable) 
* Power consumption per unit storage
* Cost for each unit capacity and power consumption
* Average Upload and Download speed of device
* The current Upload and Download speed of the device 
### Files

* File index
* File Name
* Size of file
* File type
* File priority
* Frequency file visited
* File Location
* CID (Content Identifier in the decentralized network)
* File access permissions (private, public, read-only)
* File replication factor
* File versioning and update frequency
* File Encryption and security measures
* File owner and sharing permissions
### To run the server 
Start the backend server
* pip install flask
* python app.py
Start the frontend server
* npm install
* npm start


## Multiple Knapsack Algorithm

The knapsack, or more specifically the multiple knapsack problem is oftentime sused for optimization and resource allocation. It is a classic combinatorical optimization problem that arises in scenarios wher eyou have a set of items, each with a weight and value, and a knapsack with a limited capacity. The goal of the knapsack problem is to determine the best combination of items to include in teh knapsack, maximizing the total value while not exceeding the knapsack's weight capacity.

### Extensions, modifications and optimizations of the Multiple Knapsack Algorithm

* Priority-based allocation - if certain files are more critical or have higher priorities than others, you can introduce a priority value for each file
* File duplication - Allow files to be duplicated across devices if necessary. This could be useful to increase redundancy or ensure faster access to frequently used files
* Device constraints - if devices have additional constraints, include them in the algorithm and optimize the allocation accordingly
* Limited file sharing - Allow files to be partially shared across devices, meaning that a file can be split into parts and allocated to multiple devices
* Incremental updates - If the file sizes or device capacities change over time, consider using incremental updates to the dyynamic programming table instead of recomputing it frmo scratch
* Approximation algorithms - As the Multiple Knapsack Problem is NP-hard, consider using approximation algorithms to find near-opimal solutions more efficiently for large instances.
* Heuristic approaches - Develop heuristic algorithms to quickly find reasonably good solutions that might not guarantee optimality but are computationally less expensive
* Online/offline versions: In some scenarios, you may have to make allocation decisions in real-time as new files arrive or devices change. Develop online algorithms that can handle dynamic updates and make decisions without knowing the future input.
* Paralellization - If you have a large number of files or devices, consider paralellizing the computation of the dynamic programming table to speed up the solution process
* Memory optimixstion - For large instances, optimze the memory usage of the dynamic programming table to reduce memory requirements
* Handling conflicts - If two files cannot be placed on teh same devices due to some constraints, develop a strategy to resolve such conflicts and make the best allocation decisions.
