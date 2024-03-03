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

Athena combines the concepts of web 3.0 file services and machine learning. The overall goal is to create a service that enables users to train/use/maintain artificial inteligence through a decentralized file sharing network. This could be an incredibly powerful and useful tool, as developing large language models are oftentimes limited to high net worth corporations. Our goal is to eliminate the necessity of cloud computing by empowering individuals with the tools necessary to seamlessly connect all of their devices. By allowing all of our devices to actively participate in the advancement on Artifical Intelligence, we can create tools beyond our imagination.

---

## Banbury Cloud

Banbury Cloud is a subset of Athena which serves as the decentralized file sharing network. This tool transforms personal and corporate networks into a decentralized cloud storage system, eliminating reliance on traditional cloud providers and offering unparalleled control over data security, compliance, and sovereignty. Our revolutionary concept aims to transform every household into a personal data center, leveraging the unused potential of existing devices for cloud storage needs. This addresses the common issue of limited storage capacity on individual devices and traditional cloud services. We have just released a beta version of the CLI tool. This serves as a prototype to the file sharing network. From here, you can connect devices, upload files, and download files without the use of a cloud service like Google Drive. Click here for more information on how to get started: https://website2-v3xlkt54dq-uc.a.run.app/

## Banbury Cloud Features

* Seamless connectivity of devices, regardless of what network they are on
* Predict device downtime
* predict future wifi speed
* GPU, CPU, RAM predictions
* Predicting the popularity and demand for specific content based on historical usage patterns, user preferences, and content characteristics.
* Anticipating user requests and pre-fetching or caching content to reduce latency and improve content delivery speed.
* predicit optimal allocation of files based on the values above

## To start developing athena

Athena is developed by Banbury and by users like you. We welcome bothh pull requests and issues on Github. Want to get paid to work on openpilot? Banbury is hiring and offers lots of bounties for external contributors. 

  * Information about [running athena](https://github.com/Banbury-inc/Athena/blob/main/docs/getstarted.md)
  * Read the [bounties](https://github.com/Banbury-inc/Athena/blob/main/docs/bounties.md) page to see how you can get paid!
  * Check out the [project page](https://github.com/orgs/Banbury-inc/projects/2) to see our workflow and timeline


## Table of Contents
* <a href="https://github.com/Banbury-inc/Athena/blob/main/Artificial_Intelligence/readme.md"> Artificial Intelligence </a>
* <a href="https://github.com/Banbury-inc/Athena/tree/main/Banbury_Cloud"> Banbury Cloud </a>
  * <a href="https://github.com/Banbury-inc/Athena/tree/main/Banbury_Cloud/frontend"> Frontend </a>
  * <a href="https://github.com/Banbury-inc/Athena/blob/main/Banbury_Cloud/backend/readme.md"> Backend </a>
* Getting Started
  * [Installation](https://github.com/Banbury-inc/Athena/blob/main/docs/getstarted.md)
  * [Bounties](https://github.com/Banbury-inc/Athena/blob/main/docs/bounties.md) 

  


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


