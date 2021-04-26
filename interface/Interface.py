#FlaskInputApp.py
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from flask import Flask, render_template, request
from database import *
from data_crawling import get_artist_id,get_song_id, search_response,id_response,lyric_url_response
from data_pre_display import *
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('interface.html') # just the static HTML
    

@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    action = request.form['action']

    action_name_list = ['Display of detailed information',
    'The number of songs of each artists',
    'The release date of the songs',
    'The exact number of lyric words of the songs',
    'The mean of lyrics words number the songs of each artists',
    'The appearance of a word in lyrics of each artists']
    
    artists = request.form['artist']
    word = request.form['word']
    songs = request.form['song']
    artist_name, artist_id  = artist_search(artists)
    song_name, song_id  = song_search(songs)
    
    if action == '0':
        ainformation_dict_list = artist_sort(artist_id)
        sinformation_dict_list = song_sort(song_id)
        return render_template('response_0.html', alen = len(artist_name),
            aname=artist_name, sname = song_name, slen = len(song_name),
            ades = ainformation_dict_list['description'],
            aurl = ainformation_dict_list['url'],
            afacebook = ainformation_dict_list['facebook'],
            atwitter = ainformation_dict_list['twitter'],
            aimage = ainformation_dict_list['image_url'],
            surl = sinformation_dict_list['url'],
            sdes = sinformation_dict_list['description'],
            slyrics = sinformation_dict_list['lyrics'],
            srelease = sinformation_dict_list['release_date']
            )
    if action == '1':
        bar_num_songs_of_artists(artist_name, artist_id)
        return 'Done!'
    if action == '3':
        lyrics_count_scatter(artist_name, artist_id,song_name, song_id)
        return 'Done!'
    if action == '2':
        scttr_release_date(artist_name, artist_id,song_name, song_id )
        return 'Done!'
    if action == '4':
        bar_lyrics_mean(artist_name, artist_id )
        return 'Done!'
    if action == '5':
        word_appearance(artist_name,artist_id, word)
        return 'Done!'



def song_search(songs = ''):
    # return the list of name and id
    if songs == '': return [],[]
    song_name, song_id = [],[]
    song_list = songs.split(' # ')
    for i in song_list:    
        print('i')
        result = select_song(title = i)
        if result !=[]: 
            song_id.append(result[0][0])
            song_name.append(result[0][2])
        else:
            _result = unknown_song_search_and_insert(i)
            song_id.append(_result[0][0])
            song_name.append(_result[0][2])
    return song_name,song_id



def artist_search(artists = ''):
    # return the list of name and id
    if artists == '': return [],[]
    artist_name, artist_id = [],[]
    artist_list = artists.split(' # ')
    for i in artist_list:    
        result = select_artist(name = i)
        if result !=[]: 
            artist_id.append(result[0][0])
            artist_name.append(result[0][1])
        else:
            _result = unknown_artist_search_and_insert(i)
            artist_id.append(_result[0][0])
            artist_name.append(_result[0][1])
    return artist_name,artist_id


if __name__ == "__main__":
    app.run(debug=True) 