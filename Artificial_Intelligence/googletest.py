import requests
import json
import os
import pandas as pd
import tensorflow as tf
import subprocess
import platform
import time
import pytrends
from pytrends.request import TrendReq





def main():
    
    # Set the language and timezone
    pytrends = TrendReq(hl='en-US', tz=360)

    # Get the real-time trending searches for US
    searches = pytrends.realtime_trending_searches(pn='US')

    # Extract entity names from each row and combine them into a list
    entity_names = []
    for index, row in searches.iterrows():
        entities = row['entityNames']
        for entity in entities:
            entity_names.append(entity)

    # Print the list of entity names
    print(entity_names)
if __name__ == "__main__":
    main()
    
