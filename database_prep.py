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
base_url = 'https://api.yelp.com/v3/businesses/search'
yelp_headers = {'Authorization': 'Bearer %s' % secrets.Yelp_api_key}

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

def make_request_with_cache(city_name,state_name,cache):
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
    
    if (city_name and statename) in cache.keys():
        print("Using cache")
        return cache[combine_str]
    else:
        print("Fetching")
        combine_str = city_name +', '+state_name
        location = [combine_str]
        offset = np.arange(0, 500, 50)
        tuples = list(product(location, offset))

        detail_data = []
        detail_info = []
        for loc, step in tuples:
            search_parameters = {
            'location': loc,
            'term': 'restaurant',
            'limit': 50,
            'radius': 2500,
            'offset': step
            }
            response = requests.get(base_url, headers=yelp_headers, params=search_parameters)
            detail_info.append(response.json())
        
        cache[combine_str] = detail_info
        save_cache(cache)

        return cache[combine_str]

        
#### Part 1: Database Preparation ####

## data_source_1 : create a table of cities in Final_proj.db
table_cities = pd.read_html('https://worldpopulationreview.com/us-cities')[0]
print(table_cities)


conn = sqlite3.connect('Final_proj.db')
print ("Opened database successfully")
cur = conn.cursor()

engine = create_engine('sqlite:///Final_proj.db')
table_cities.to_sql('Cities',engine)
conn.commit()
cur.close()

## data_source_2: create a table of restaurant in Final_proj.db
def get_city_restaurant(city_name,state_name):
    
    detail_info = make_request_with_cache(city_name,state_name,YELP_CACHE)

    info_list = []
    num_records = detail_info[0]['total']
    # print(num_records)

    for info in detail_info:
        data = info['businesses']
        if data:     
            for item in data:
                # print(item)
                categories = []
                for cat in item['categories']:
                    categories.append(cat['title'])
                try:
                    restaurants_dict = {
                        "restaurant_id": item['id'],    
                        "Name": item['name'],
                        "Phone": item['display_phone'],
                        "Price": item['price'],
                        "Rating": item['rating'],
                        "Url": item['url'],
                        "Address": ' '.join(item['location']['display_address']),
                        "Category": categories,
                        "City": item['location']['city'],
                        "State": item['location']['state'],
                        "zipcode":item['location']['zip_code']
                    }
                except:
                    restaurants_dict = {
                        "restaurant_id": item['id'],    
                        "Name": item['name'],
                        "Phone": item['display_phone'],
                        "Price": '',
                        "Rating": item['rating'],
                        "Url": item['url'],
                        "Address": ' '.join(item['location']['display_address']),
                        "Category": categories,
                        "City": item['location']['city'],
                        "State": item['location']['state'],
                        "zipcode":item['location']['zip_code']
                    }
                info_list.append(restaurants_dict)
    return info_list


if __name__ == "__main__":
    

    YELP_CACHE = open_cache()

    cities_list = []
    states_list =[]
    restaurants_df = pd.DataFrame(columns=["restaurant_id","Name","Phone","Price","Rating","Url","Address","Category","City","State","zipcode"])
    # print(restaurants_df)
    conn = sqlite3.connect('Final_proj.db')
    # print ("Opened database successfully")
    cur = conn.cursor()
    query = "SELECT Name,State FROM Cities"
    cur.execute(query)
    combine_data = cur.fetchall()
    # print(combine_data[0][0])
    for pair in combine_data:
        cities_list.append(pair[0])
        states_list.append(pair[1])
    
    # Test for Cache
    cityname = 'Akron'
    statename = 'OHIO'
    output = get_city_restaurant(cityname,statename)
    print(output)
    oh_to_df = pd.DataFrame(output)
    print(oh_to_df)
    



    for i in range(len(cities_list)):
        temp_city = cities_list[i]
        temp_state = states_list[i]
        temp_combine_list = get_city_restaurant(temp_city,temp_state)
        temp_df = pd.DataFrame(temp_combine_list)
        restaurants_df = pd.concat([restaurants_df,temp_df],axis=0)
    
    print(restaurants_df)
    restaurants_df.to_csv('restaurants_info.csv')
    restaurants_df = pd.read_csv('restaurants_info.csv')
    conn = sqlite3.connect('Final_proj.db')
    print ("Opened database successfully")
    cur = conn.cursor()
    engine = create_engine('sqlite:///Final_proj.db')
    restaurants_df.to_sql('Restaurants',engine)
    conn.commit()
    cur.close()