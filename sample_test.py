import requests
import json
import requests
import webbrowser
from lxml import etree
import requests
from bs4 import BeautifulSoup
import os
import json
import time
import sys
import pandas as pd
import re
##################################################################################
## basic settings
GENIUS_API_KEY = "o16ert87sxCWAIo5egqfGjcnp3kUKn4SK7KMDGkORSJTz6eFT5tZ_WWqfGgM5XLS"
base_url = 'http://api.genius.com'

headers ={
    'Authorization': 'Bearer ' +  GENIUS_API_KEY
}
######################################################################################3
## [1] response of a searching keywords
song_instr = 'save me'
artist_instr = 'Kendrick Lamar' 
params = {'q':artist_instr}
search_url = base_url+f'/search?q={song_instr}' 

search_response = requests.get(search_url,headers=headers)
text = search_response.json()
with open('response_of_search_songs.json', 'w') as f:
    json.dump(text, f)

search_url = 'https://genius.com/api/search/artist'
search_response = requests.get(search_url,params=params)
text = search_response.json()

with open('response_of_search_artists.json', 'w') as f:
    json.dump(text, f)




    
    
######################################################################################3
## [2] response of the song id and artist id
api_path = ['/songs/3039923', '/artists/1421']

song_url = base_url  +api_path[0]
song_response = requests.get(song_url, headers=headers)
text = song_response.json()
'''
with open('response_of_song_id.json', 'w') as f:
    json.dump(text, f)
'''
artist_url = base_url  +api_path[1]
artist_response = requests.get(artist_url, headers=headers)
text = artist_response.json()
'''
with open('response_of_artist_id.json', 'w') as f:
    json.dump(text, f)
'''
######################################################################################3
## [3] response of the song url path if lyrics_state is complete

#path = text['response']['song']['path']
path = '/Kendrick-lamar-humble-lyrics'
lyric_url = 'http://genius.com' + text['response']['song']['path']
response = requests.get(lyric_url)

soup = BeautifulSoup(response.text, 'html.parser')
'''
with open('response_of_lyric_path.html', 'wb') as f:
    f.write(soup.prettify("utf-8"))
'''

######################################################################################3
## [4] extract lyrcis
class_of_lyrics = re.compile("lyrics|Lyrics__Root")
lyrics = soup.find('div', class_=class_of_lyrics).get_text()
'''
with open('lyric_sample.txt', 'wb') as f:
    f.write(lyrics.encode('utf-8'))
    f.close()
'''   