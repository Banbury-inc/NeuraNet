<img src="<img src="https://img.shields.io/github/downloads/mmills6060/Athena/total">">

<img src="https://img.shields.io/github/downloads/mmills6060/Athena/total"> <img src="https://img.shields.io/github/repo-size/mmills6060/Athena"> <img src="https://img.shields.io/github/last-commit/mmills6060/Athena">

<a href="https://www.buymeacoffee.com/mmills6060" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>


# Overview
This is a project that I have been working on that combines the concepts of web 3.0 file services and machine learning. My overal idea is to create a machine learning algorithm that will save and fetch data through a decentralized file sharing network. This could be an incredibly powerful and useful tool, as developing large language models are oftentimes limited to high net worth corporations. By allowing all of our devices to actively participate in the advancement on Artifical Intelligence, we can create tools beyond our imagination. 

Decentralized file sharing is also a major aspect of this project. Despite the existence of cloud services, I still believe that there is a lot of room to improve file sharing and file management. I oftentimes find myself wondering how I can transfer a photo from my Apple Iphone to my windows computer and vice versa. I am also constantly finding myself running out of storage on smaller devices like my phone, apple watch, even my laptop. I am passionate about creating a decentralized file sharing network where you can access every single file from every single device, all in one place. Not only would you be able to access every single file, but you have powerful algorithm's that will help make sure that your most important files are the ones that are the easiest to access. 

My hope for the future is to gradually continue with the development of this project. I aspire to make this a tool that can profoundly impact the lives of everyone throughout the world. I aspire to eventually produce a prototype that I can share with others. I want to continue past just a prototype and work towards building an MVP. I aspire to someday find investors that will help guide me through this journey. There is a lot of work to do, so any form of help would be greatly appreciated.

## Features
* 100% biometric log-in system
* Decentralized file sharing powered by IPFS for a fully asynchronous and autonomous file management experience
* Powerful algorithms to enable unrivaled performance and reliability
* Fully Autonomous AI Assistant powered by our decentralized IPFS network. 
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


## Basic Architecture
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
