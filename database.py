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

#connection = sqlite3.connect("genius_artists.db")
#cursor = connection.cursor()


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
    query = f"""SELECT * FROM [Songs] WHERE Song_ID = ?"""
    result = cur.execute(query,[song.Song_Id]).fetchall()
    if result == []:
        query = f"""INSERT INTO Songs VALUES (?,?,?,?,?,?,?,?,?)"""
        cur.execute(query, (song.Song_Id,song.Artist_ID,song.song_title,song.url,song.description,song.release_date,song.lyrics_state,song.lyrics_path,song.lyrics))
        con.commit()

    con.close()

def insert_lyrics(song):
    con = sqlite3.connect("genius_artists.db")
    cur = con.cursor()
    query = """UPDATE Songs set lyrics = ? where Song_ID = ?"""
    cur.execute(query,(song.lyrics,song.Song_Id))
    con.commit()
    con.close()

def select_artist(name=None,id=None,other = None, allflag = False):
    con = sqlite3.connect("genius_artists.db")
    cur = con.cursor()
    result = []
    other_str = ''
    if allflag == True: 
        query = 'SELECT * FROM [Artists] WHERE Artist_ID = ?'
        result = cur.execute(query,[id]).fetchall()
        return result
    if other != None:
        other_str = ','+','.join(other)
    if name == None:
        query = 'SELECT Artist_ID, Artist_name'+other_str+ ' FROM [Artists] WHERE Artist_ID = ?'
        result = cur.execute(query,[id]).fetchall()

    else:
        query = 'SELECT Artist_ID, Artist_name'+other_str+ ' FROM [Artists] WHERE Artist_name = ?'
        result = cur.execute(query,[name]).fetchall()
    con.close()    
    return result

def select_song(title=None,song_id=None,artist_id=None,other=None, allflag = False):
    con = sqlite3.connect("genius_artists.db")
    cur = con.cursor()
    other_str = ''
    result = []
    if allflag == True:
        query = 'SELECT * FROM [Songs] WHERE Song_ID = ?'
        result = cur.execute(query,[song_id]).fetchall()
        return result
    if other != None:
        other_str = ','+','.join(other)
    if title != None:
        query = 'SELECT Song_ID,Artist_ID, Song_title'+ other_str +' FROM [Songs] WHERE Song_title = ?'
        result = cur.execute(query,[title]).fetchall()
    elif song_id !=None:
        query = 'SELECT Song_ID,Artist_ID, Song_title'+ other_str +' FROM [Songs] WHERE Song_ID = ?'
        result = cur.execute(query,[song_id]).fetchall()
    elif artist_id !=None:
        query = 'SELECT Song_ID,Artist_ID, Song_title'+ other_str +' FROM [Songs] WHERE Artist_ID = ?'
        result = cur.execute(query,[artist_id]).fetchall()

    con.close()    
    return result
def select_total_song(other=None):
    con = sqlite3.connect("genius_artists.db")
    cur = con.cursor()
    other_str = ''
    result = []
    if other != None:
        other_str = ','+','.join(other)
    query = 'SELECT Song_ID'+ other_str +' FROM [Songs]'
    result = cur.execute(query).fetchall()

    con.close()    
    return result
def unknown_artist_search_and_insert(artist_name):
    text1 = search_response(artist_name,'artist')
    artist_id = get_artist_id(text1, num = 0)
    a1 = artist(
        id_response('/artists/'+str(artist_id))['response']['artist'])
    #a2 = song(id_response('/songs/3039923')['response']['song'])
    #a2.get_lyrics()
    insert_into_Artists(a1)
    return [(a1.Id,a1.name)]
def unknown_song_search_and_insert(song_name):
    text1 = search_response(song_name,'song')

    song_id = get_song_id(text1, num = 0)[0]
    a2 = song(
        id_response('/songs/'+str(song_id))['response']['song'])
    #a2 = song(id_response('/songs/3039923')['response']['song'])
    a2.get_lyrics()
    #insert_into_Artists(a1)
    insert_into_Songs(a2)
    return [(a2.Song_Id,a2.song_title)]
if __name__ == "__main__":
    '''
    text1 = search_response('Kendrick Lamar'))
    text2 = id_response('/songs/3039923'))
    lyric = (lyric_url_response('/Kendrick-lamar-humble-lyrics'))
    '''
    test = 5 ##
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
            song_id = get_song_id(text1, num = 4)[0]
            a2 = song(
                id_response('/songs/'+str(song_id))['response']['song'])
            #a2 = song(id_response('/songs/3039923')['response']['song'])
            a2.get_lyrics()
            #insert_into_Artists(a1)
            insert_into_Songs(a2)
    if test == 3:
      song_list = select_total_song()
      for song_id in song_list:
        a2 = song(
                id_response('/songs/'+str(song_id[0]))['response']['song'])
        #a2 = song(id_response('/songs/3039923')['response']['song'])
        a2.get_lyrics()
        #insert_into_Artists(a1)
        insert_lyrics(a2)
    if test == 4:
        select_artist(name = 'Rihanna')
    if test == 5:
        df = ['Coldplay', 'Radiohead', 'Red Hot Chili Peppers','Rihanna','Eminem','The Killers','Kanye West','Nirvana','Muse','Queen','Foo Fighters','Linkin Park','Lady Gaga','The Rolling Stones','Daft Punk','Green Day','Katy Perry','The Beatles','Oasis','Gorillaz','Beyoncé','Michael Jackson','Maroon 5','Arctic Monkeys','System of a Down','U2','Kings of Leon','Drake','David Bowie','The Black Eyed Peas','The Strokes','Britney Spears','Guns N’ Roses','Franz Ferdinand','The Doors','JAY-Z','Madonna','Pink Floyd','Weezer','Snow Patrol','blink‐182','The White Stripes','The Cure','Led Zeppelin','Beck','Aerosmith','The Offspring','Metallica','R.E.M.','Blur','Adele',
                'Rage Against the Machine','Death Cab for Cutie','Nickelback','Justin Timberlake','The Smashing Pumpkins','MGMT','Johnny Cash','Christina Aguilera','David Guetta','The Who','Jimi Hendrix','Fall Out Boy','Pearl Jam','AC/DC','Depeche Mode','Moby','Bob Dylan','Usher','50 Cent','The Kooks','Placebo','Avril Lavigne','Chris Brown','Christopher Brown','Incubus','Massive Attack','Arcade Fire','Korn','Jack Johnson','3 Doors Down','Amy Winehouse','Bloc Party','OutKast','Elton John','Yeah Yeah Yeahs','P!nk','Snoop Dogg','Kid Cudi','Kesha','Paramore','Queens of the Stone Age','Papa Roach','Mariah Carey','John Mayer','Black Sabbath','Kasabian','The Beach Boys','Kelly Clarkson','T.I.',
                'Keane','Eric Clapton','Florence + the Machine','Modest Mouse','Elvis Presley','Disturbed','Simon & Garfunkel','Evanescence','My Chemical Romance','Creedence Clearwater Revival','Thirty Seconds to Mars','Frank Sinatra','Bon Jovi','Slipknot','Shakira','The Shins','The Clash','Dr. Dre','Alicia Keys','Pixies','Limp Bizkit','The Smiths','OneRepublic','The Cranberries','The Police','Kaiser Chiefs','Jason Mraz','Interpol','Beastie Boys','Nelly Furtado','Three Days Grace','The Chemical Brothers','Sum 41','Marilyn Manson','The Prodigy','The Fray','Audioslave','Taylor Swift','Panic! at the Disco',
                'Calvin Harris','Wiz Khalifa','Björk','2Pac','Vampire Weekend','Nine Inch Nails','John Lennon','Lily Allen','Bruce Springsteen','The Black Keys','Gwen Stefani','Air','Fleetwood Mac','Stevie Wonder','Dire Straits','Flo Rida','Sia','Deep Purple','Iron Maiden','The Kinks','Jennifer Lopez','Portishead','Jimmy Eat World','Goo Goo Dolls','Iron & Wine','Eagles','The Notorious B.I.G.','Norah Jones','The Verve','Nicki Minaj','Sigur Rós','The Pussycat Dolls','James Blunt','Rise Against','Phoenix']
        for a in df:
            text1 = search_response(a,'artist')
            artist_id = get_artist_id(text1, num = 0)
            a1 = artist(
                id_response('/artists/'+str(artist_id))['response']['artist'])
            insert_into_Artists(a1)


            text1 = search_response(a1.name,'song')
            song_id = get_song_id(text1, all= True)
            for sid in song_id:
                a2 = song(
                    id_response('/songs/'+str(sid))['response']['song'])
                #a2 = song(id_response('/songs/3039923')['response']['song'])
                a2.get_lyrics()
                #insert_into_Artists(a1)
                insert_into_Songs(a2)
