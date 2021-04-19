import json
from lxml import etree
import requests
from bs4 import BeautifulSoup
import os
import time
import sys
import pandas as pd
import re
## basic settings
GENIUS_API_KEY = "gulqB5H9cGgsk2Hzo5jX96Q2QAQrMJp2eSF66WUAShkpJxQG8kh0rd1UrJBY8HK5"
base_url = {'song': 'http://api.genius.com',
'artist': 'https://genius.com/api/search/artist'}
## other category can be obtained by changing 


headers ={
    'Authorization': 'Bearer ' +  GENIUS_API_KEY
}
CACHE_FILENAME = "ccache.json"
CACHE_DICT = {}

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

def search_response(keywords,category = 'song'):
    params = {'q':keywords}
    if category == 'artist':
        search_url = base_url[category] 
    else:
        search_url = base_url[category]+'/search' 
    
    cache_dict = open_cache()
    try:
        text = cache_dict[search_url+params['q']]
    except:
        if category == 'artist':
            search_response = requests.get(search_url,params = params)
        else:
            search_response = requests.get(search_url,params = params, headers = headers )
        text = search_response.json()
        cache_dict[search_url+keywords] = text
        save_cache(cache_dict)
    
    
    return text
def id_response(api_path):

    song_url = base_url['song'] + api_path
    cache_dict = open_cache()
    try:
        text = cache_dict[song_url]
    except:
        search_response = requests.get(song_url,headers=headers)
        text = search_response.json()
        cache_dict[song_url] = text
        save_cache(cache_dict)
    return text
def lyric_url_response(lyric_path):

    lyric_url = 'http://genius.com' + lyric_path
    cache_dict = open_cache()
    try:
        text = cache_dict[lyric_url]
    except:
        response = requests.get(lyric_url)
        text = response.text
        cache_dict[lyric_url] = text
        save_cache(cache_dict)
    
    soup = BeautifulSoup(text, 'html.parser')
    class_of_lyrics = re.compile("lyrics|Lyrics__Root")
    lyrics = soup.find('div', class_=class_of_lyrics).get_text()
    return lyrics

def get_artist_id(text, num = 0):

    
    return text['response']['sections'][0]['hits'][num]['result']['id']
def get_song_id(text, num = 0):
    return text['response']['hits'][num]['result']['id']
def get_artist_api_path(text, num = 0):

    
    return text['response']['sections'][0]['hits'][num]['result']['api_path']
def get_song_api_path(text, num = 0):
    return text['response']['hits'][num]['result']['api_path']
if __name__ == "__main__":
    print(search_response('Kendrick Lamar','artist'))
    print(search_response('Unstopable','song'))
    print(id_response('/songs/3039923'))
    print(lyric_url_response('/Kendrick-lamar-humble-lyrics'))
