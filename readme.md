# Overview
This is a project that I have been working on that combines the concepts of web 3.0 file services and machine learning. My overal idea is to create a machine learning algorithm that will save and fetch data through a decentralized file sharing network. 

## Features
100% biometric log-in system
## To-do
* based on the prompt, create an itinerary of tasks that will be completed until the end goal is complete.
* search the web for particular topics
* learn to code
* demonstrate feelings
* automatically tamper with the michine learning model until it is able to achieve a certain level of accuracy (increase epochs, find more datasets, add more layers)
* train on openwebtext dataset: https://github.com/karpathy/nanoGPT/tree/master/data/openwebtext#:~:text=GPT%2D2%20paper-,OpenWebText,-dataset
* better web scraping capabilities: https://github.com/dragnet-org/dragnet
* general language model, not classification
* voice to text generator https://github.com/openai/whisper
* a voice for athena
* multiple voices for athena
* " What will the weather be like this week?"
* "can you add tennis with hillman at 6 pm on thursday to my google calendar
* " what time does cvs pharmacy close?
* if response comes with less than 25% confidence, get help from openai API
* determine whether or not a model is overfit or underfit and automatically manipulat the model/data accordingly
* commands to complete tasks on the computer
* Youtube TV
* store information about the user for future reference

# API's I am looking to integrate
* Google Calendar API
* Weather API
* Google Maps API
* Google Cloud Translation API
* Google Search API
* Twitter API
* JOJ Unlimited Web Search
* Shazam API
* Spotify API
* Polygon.io API
* Jokeapi
* Soundcloud API
* OPEN Library API
* 


# Basic Architecture
File Management GUI
Frontend - HTML, CSS, Javascript
Backend - Go
Database - IPFS

Artificial Intelligence Scripts
* Frontend - N/A
* Backend - Python
* Database - IPFS

User Management GUI
* Frontend - HTML, CSS, Javascript
* Backend - Java
* Database - MySQL

# Multiple Knapsack Algorithm


# Extensions, modifications and optimizations of the Multiple Knapsack Algorithm
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