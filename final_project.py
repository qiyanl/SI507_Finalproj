import requests
import json
from yelpapi import YelpAPI
import numpy as np
import sqlite3
from itertools import product
import pandas as pd
import matplotlib.pyplot as plt
import secrets
from sqlalchemy import create_engine


CACHE_FILENAME = "finalproj.json"
YELP_DICT = {}

# Part 0: Caching
def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

YELP_CACHE = open_cache()

def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def make_request_with_cache(baseurl,cache):
    '''Check the cache for a saved result for this baseurl. 
    If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    cache: dict
        The cache that make request with
    
    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    if baseurl in cache.keys():
        print("Using cache")
        return cache[baseurl]
    else:
        print("Fetching")
        cache[baseurl] = requests.get(baseurl).text
        save_cache(cache)
        return cache[baseurl]
        
### data_source_2: Yelp Fusion




if __name__ == "__main__":
    # YELP_CACHE = open_cache()
    # first_command_enter = True

    # while True:
    #     if first_command_enter:
    #         command_enter = input('Please enter a city name or state name or zipcode, or exit:')

