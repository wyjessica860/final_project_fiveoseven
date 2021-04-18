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
GENIUS_API_KEY = "o16ert87sxCWAIo5egqfGjcnp3kUKn4SK7KMDGkORSJTz6eFT5tZ_WWqfGgM5XLS"
base_url = 'http://api.genius.com'

headers ={
    'Authorization': 'Bearer ' +  GENIUS_API_KEY
}

def search_response(keywords):

    search_url = base_url+f'/search?q={keywords}' 

    search_response = requests.get(search_url,headers=headers)
    text = search_response.json()
    return text
def id_response(api_path):

    song_url = base_url + api_path
    search_response = requests.get(song_url,headers=headers)
    text = search_response.json()
    return text
def lyric_url_response(lyric_path):

    lyric_url = 'http://genius.com' + lyric_path
    response = requests.get(lyric_url)

    soup = BeautifulSoup(response.text, 'html.parser')
    class_of_lyrics = re.compile("lyrics|Lyrics__Root")
    lyrics = soup.find('div', class_=class_of_lyrics).get_text()
    return lyrics


if __name__ == "__main__":
    print(search_response('Kendrick Lamar'))
    print(id_response('/songs/3039923'))
    print(lyric_url_response('/Kendrick-lamar-humble-lyrics'))
