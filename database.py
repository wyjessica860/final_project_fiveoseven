import json
import os
import time
import sys
import pandas as pd
import re
from data_crawling import get_artist_id,get_song_id, search_response,id_response,lyric_url_response
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
    query = f"""SELECT * FROM [Artists] WHERE Artist_ID = {artist.Id}"""
    result = cur.execute(query).fetchall()
    if result == []:
        query = f"""INSERT INTO Artists VALUES (?,?,?,?,?,?,? )"""
        cur.execute(query,(artist.Id,artist.name,artist.url, artist.description,artist.facebook_name,artist.twitter_name,artist.image_url))
        con.commit()
    con.close()
def insert_into_Songs(song):
    con = sqlite3.connect("genius_artists.db")
    cur = con.cursor()
    query = f"""SELECT * FROM [Songs] WHERE Song_ID = {song.Song_Id}"""
    result = cur.execute(query).fetchall()
    if result == []:
        query = f"""INSERT INTO Songs VALUES (?,?,?,?,?,?,?,?,?)"""
        cur.execute(query, (song.Song_Id,song.Artist_ID,song.song_title,song.url,song.description,song.release_date,song.lyrics_state,song.lyrics_path,song.lyrics))
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
    test = 2 ##
    if test == 1:
        artist_list = ['Britney Spears','Bruno Mars','Ed Sheeran','Sia','Ariana Grande','Michael Jackson',
        'The Beatles','Lady Gaga','Rihanna','Taylor Swift','Madonna']
        for a in artist_list:
            text1 = search_response(a,'artist')
            artist_id = get_artist_id(text1, num = 0)
            a1 = artist(
                id_response('/artists/'+str(artist_id))['response']['artist'])
            #a2 = song(id_response('/songs/3039923')['response']['song'])
            #a2.get_lyrics()
            insert_into_Artists(a1)
            #insert_into_Songs(a2)
    if test == 2:
        song_list = ['Britney Spears','Bruno Mars','Ed Sheeran']
        for a in song_list:
            text1 = search_response(a,'song')
            song_id = get_song_id(text1, num = 4)
            a2 = song(
                id_response('/songs/'+str(song_id))['response']['song'])
            #a2 = song(id_response('/songs/3039923')['response']['song'])
            a2.get_lyrics()
            #insert_into_Artists(a1)
            insert_into_Songs(a2)