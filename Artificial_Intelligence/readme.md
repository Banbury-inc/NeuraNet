# Artificial Intelligence

## Introduction

This is a repository primarily responsible for training and interacting with AI. 


## Model Architecture

I have been thinking a lot about model architecture and what would be the best way
to approach this. I have been thinking about whether I should have an incredibly large, 
single model for all tasks and pieces of information. The other option would be to develop
an architecture of ML models that are task specific. There are obviously pros and cons to 
each strategy. Finally, I came up with the idea... why not do both!

- Task Specific Models
1. Computer Vision: Object Detection, Image Classification, Image Segmentation
2. Natural Language Processing (NLP): sentiment analysis, named entity recognition, text summarization 
3. Audio Processing: Speech Recognition, Speaker Identification, Sound Classification
4. Time-Series Analysis: time-series data, such as forcasting, anomaly detection, signaml processing.

- Large Model
1. Shared Representations: Topics that share underlying features or representations
2. 3 Multi-Model Fusion: Topics that require multiple modalities, such as text and images
would certainly be better off in a single model. 
3. Contextual Understanding: Topics that require contextual understanding acorss differe domains or tasks, 
such as dialogue systems or contextual recommendation systems, would benefit. 


At the end of the day, I think the architecture and how the models are trained can all
be boiled down into whether that data that is being trained is knowledge or a skill. 
If it's knowledge, it can be probably added on to a large model. If it's a skill, it can 
probably be kept separate and placed into their own individual models. 

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

  
https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.VotingClassifier.html
