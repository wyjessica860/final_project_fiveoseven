import json
import os
import time
import sys
import pandas as pd
import re
from data_crawling import search_response,id_response,lyric_url_response
from config import artist,song

import sqlite3 
##database structure 
#connection:
connection = sqlite3.connect("genius_artists.db")
cursor = connection.cursor()


## D1: Artists
'''
    This database should contain artist information (response_of_artist_id)
    priimary key: Artist Id 
    atrributes: Artist name
            AKA
            url
            Description
            facebook_name
            twitter_name
            imag_url
'''
## D2: Songs
'''
    This database should contain song information (response_of_song_id)
    priimary key: song Id
    foreign key: artist ID 
    atrributes: Song title
            url
            Description
            release_date
            lyrics_state
            lyrics_path
            lyrcis
'''
def insert_into_Artists(artist):
    con = sqlite3.connect("genius_artists.db")
    cur = con.cursor()
    query = f"""INSERT INTO Artists VALUES ( {artist.Id},'{artist.name}','{artist.url}', '{artist.description}','{artist.facebook_name}','{artist.twitter_name}', '{artist.image_url}')"""
    cur.execute(query)
    con.commit()
    con.close()
def insert_into_Songs(song):
    con = sqlite3.connect("genius_artists.db")
    cur = con.cursor()
    query = f"""INSERT INTO Songs VALUES ( {song.Song_Id},'{song.Artist_ID}','{song.song_title}','{song.url}', '{song.description}','{song.release_date}','{song.lyrics_state}', '{song.lyrics_path}','{song.lyrics}')"""
    cur.execute(query)
    con.commit()
    con.close()

def insert_lyrics(song):
    con = sqlite3.connect("genius_artists.db")
    cur = con.cursor()
    query = f"""UPDATE Songs set lyrics = '{song.lyrics}' where Song_ID = {song.Song_Id}"""
    cur.execute(query)
    con.commit()
    con.close()

if __name__ == "__main__":
    '''
    text1 = search_response('Kendrick Lamar'))
    text2 = id_response('/songs/3039923'))
    lyric = (lyric_url_response('/Kendrick-lamar-humble-lyrics'))
    '''
    a1 = artist(id_response('/artists/1421')['response']['artist'])
    a2 = song(id_response('/songs/3039923')['response']['song'])
    insert_into_Artists(a1)
    insert_into_Songs(a2)