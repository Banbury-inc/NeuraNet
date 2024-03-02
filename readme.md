<p align="center">
  <img src="https://github.com/mmills6060/Athena/blob/5c5af257a4f03597422a419f5a06e56f1940e7db/3yk0j06n.png" height="300" alt="Athena Logo"/>
</p>
<p align="center">  
  <em>🤖 Empowering Decentralized AI Advancement through Personal Device Networks 🤖  </em>
</p>
<p align="center">
  <img src="https://img.shields.io/github/downloads/mmills6060/Athena/total" alt="Badge 2">
  <img src="https://img.shields.io/github/repo-size/mmills6060/Athena" alt="Badge 3">
  <img src="https://img.shields.io/github/last-commit/mmills6060/Athena" alt="Badge 4">
  <img src="https://img.shields.io/github/actions/workflow/status/TheAlgorithms/Python/build.yml?branch=master&label=CI&logo=github&style=flat-square" alt="GitHub Workflow Status">
   <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
 
</p>



</p>


# Overview

This is a project that I have been working on that combines the concepts of web 3.0 file services and machine learning. My overal idea is to create a machine learning algorithm that will save and fetch data through a decentralized file sharing network. This could be an incredibly powerful and useful tool, as developing large language models are oftentimes limited to high net worth corporations. In other words, why pay a lot of money to rent out a server to train a machine learning model when you can achieve the same result by combining all of the resources of each deviec in your own home? By allowing all of our devices to actively participate in the advancement on Artifical Intelligence, we can create tools beyond our imagination.

## Banbury Cloud

Banbury Cloud is a subset of Athena which serves as the decentralized file sharing network. This tool transforms personal and corporate networks into a decentralized cloud storage system, eliminating reliance on traditional cloud providers and offering unparalleled control over data security, compliance, and sovereignty. Our revolutionary concept aims to transform every household into a personal data center, leveraging the unused potential of existing devices for cloud storage needs. This addresses the common issue of limited storage capacity on individual devices and traditional cloud services. We have just released a beta version of the CLI tool. This serves as a prototype to the file sharing network. From here, you can connect devices, upload files, and download files without the use of a cloud service like Google Drive. Click here for more information on how to get started: https://website2-v3xlkt54dq-uc.a.run.app/

## Banbury Cloud Features

* Predict device downtime
* predict future wifi speed
* GPU, CPU, RAM predictions
* User behavior analysis
* Predicting the popularity and demand for specific content based on historical usage patterns, user preferences, and content characteristics.
* Anticipating user requests and pre-fetching or caching content to reduce latency and improve content delivery speed.
* predicit optimal allocation of files based on the values above

# Table of Contents
* <a href="https://github.com/Banbury-inc/Athena/blob/main/Artificial_Intelligence/readme.md"> Artificial Intelligence </a>
* <a href="https://github.com/Banbury-inc/Athena/tree/main/Banbury_Cloud"> Banbury Cloud </a>
  * <a href="https://github.com/Banbury-inc/Athena/tree/main/Banbury_Cloud/frontend"> Frontend </a>
  * <a href="https://github.com/Banbury-inc/Athena/blob/main/Banbury_Cloud/backend/readme.md"> Backend </a>
## Athena Features

* 100% biometric log-in system
* Decentralized file sharing powered by cutting edge AI relay server for a fully asynchronous and autonomous file management experience
* Powerful algorithms to enable unrivaled performance and reliability
* Fully Autonomous AI Assistant powered by our AI relay server.
* Implementation of a remote access tunnel allows for seamless connection via NAT (Network Address Translation) devices such as Iphones connected via cellular data.

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

## API's I am looking to integrate

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
Frontend - HTML, CSS, Typescript
Backend - Python
Database - MongoDB

Artificial Intelligence Scripts

* Frontend - N/A
* Backend - Python
* Database - MongoDB

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

## User Management
Since this app is completely decentralized, that means that the user databse is decentralized as well. 

username + password(hashed) --> cid containing file of usernames + passwords --> cid of devices, all information needed for file directory of that particular user --> locate desired file and make query to download with cid of that file
