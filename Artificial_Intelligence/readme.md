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


https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.VotingClassifier.html
