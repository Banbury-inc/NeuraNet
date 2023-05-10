# Overview
This is a project that I have been working on that combines the concepts of web 3.0 file services and machine learning. My overal idea is to create a machine learning algorithm that will save and fetch data through a decentralized file sharing network. 

## Features


## To-do
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


# Prerequisites
wget
```

pip install tensorflow
pip install matplotlib
pip install tiktoken
pip install hparams
pip install datasets
pip install numpy
pip install googlesearch
pip install openai
pip install datetime
pip install pandas
pip install praw
pip install pytrends
pip install bs4
pip install googlesearch-python
pip install playwright
pip install ipfshttpclient==0.8.0
npm install -g @web3-storage/w3cli
wget https://dist.ipfs.tech/kubo/v0.20.0/kubo_v0.20.0_windows-amd64.zip -Outfile kubo_v0.20.0.zip
Expand-Archive -Path kubo_v0.20.0.zip -DestinationPath ~\Apps\kubo_v0.20.0
cd ~\Apps\kubo_v0.20.0\kubo
.\ipfs.exe --version
$GO_IPFS_LOCATION = pwd
if (!(Test-Path -Path $PROFILE)) { New-Item -ItemType File -Path $PROFILE -Force }
notepad $PROFILE
Add-Content $PROFILE "`n[System.Environment]::SetEnvironmentVariable('PATH',`$Env:PATH+';;$GO_IPFS_LOCATION')"
& $profile   
cd ~
ipfs --version

```
