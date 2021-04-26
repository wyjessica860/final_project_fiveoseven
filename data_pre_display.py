import plotly.graph_objs as go
from data_crawling import get_artist_id,get_song_id, search_response,id_response,lyric_url_response
from config import artist,song
import database
from datetime import datetime
import statistics
from collections import Counter

def artist_sort(artistlist):
    ainformation_dict_list= {'description' : [], 'url':[] , 'facebook':[],'twitter':[],'image_url':[]}
    
    for a in artistlist:
        result = database.select_artist(id = a,allflag = True)
        result = result[0]
        ainformation_dict_list['url'].append(result[2])
        ainformation_dict_list['description'].append(result[3])
        ainformation_dict_list['facebook'].append(result[4])
        ainformation_dict_list['twitter'].append(result[5])
        ainformation_dict_list['image_url'].append(result[6])
    
    return ainformation_dict_list
def song_sort(songlist):
    sinformation_dict_list = {'url':[], 'description': [], 'lyrics':[], 'release_date':[]}
    sin = {}
    for s in songlist:
        result = database.select_song(song_id = s,allflag = True)
        result = result[0]
        sinformation_dict_list['url'].append(result[3])
        sinformation_dict_list['description'].append(result[4])
        sinformation_dict_list['lyrics'].append(result[8])
        sinformation_dict_list['release_date'].append(result[5])
 

    return sinformation_dict_list
################################################################
#artlist 里面是id
def bar_num_songs_of_artists(artistnames, artistids):
    ## The number of songs of each artists 
    songlength = []
    for  a in artistids:
        info = database.select_song(artist_id = a)
        print(info)
        songlength.append(len(info))
    print(songlength)
    bar_data = go.Bar(x=artistnames,y=songlength)
    basic_layout = go.Layout(title = 'The songs of '+ ','.join(artistnames) + ' preserved in database')
    fig = go.Figure(data=bar_data, layout=basic_layout)
    fig.show()
def scttr_release_date(artistnames = [], artistids =[], songnames = [], songids =[] ):
    song_name_rel_date_dict = {}
    #trace the release date of the songs by scatter plot 
    for a in artistids :
        
        songs_info = database.select_song(artist_id = a,other = ['release_date'])
        for i in songs_info:
            song_name_rel_date_dict[i[2]]=i[-1]
    for s in songids :
        
        songs_info = database.select_song(song_id=s,other = ['release_date'])
        for i in songs_info:
            song_name_rel_date_dict[i[2]]=i[-1]

    df={k: datetime.strptime(v,'%Y-%m-%d') for k, v in sorted(song_name_rel_date_dict.items(), key=lambda item: item[1])} 
    
    bar_data = go.Scatter(x=list(df.values()),y=list(df.keys()))
    basic_layout = go.Layout(title = 'The release date of songs')
    fig = go.Figure(data=bar_data, layout=basic_layout)


    fig.show()
def lyrics_count_scatter(artistnames = [], artistids =[], songnames = [], songids =[] ):
    # using scatter plot for showing the exact number of lyric words of this artist or multiple songs
    # Note single artist. therefore, we will make scatter plot of a singer
    song_lyric_dict = {}
    if artistids == [] : flag = False
    else: flag = True
    for a in artistids:
        song_lyric_dict = {}
        songs_info = database.select_song(artist_id = a,other = ['lyrics'])
        for i in songs_info:
            lyrics_text = i[-1]
            lyrics_word_counting =  len(lyrics_text.split(' '))
            song_lyric_dict[i[2]] = lyrics_word_counting
        scatter_data = go.Scatter(y=list(song_lyric_dict.values()),x=list(list(song_lyric_dict.keys())))
        basic_layout = go.Layout(title = 'The word count of lyrics of song from ' + artistnames[artistids.index(a)] )
        fig = go.Figure(data=scatter_data, layout=basic_layout)
        fig.show()
    
    if flag == False:
        for s in  songnames :
            songs_info = database.select_song(title = s,other = ['lyrics'])
            for i in songs_info:
                lyrics_text = i[-1]
                lyrics_word_counting =  len(lyrics_text.split(' '))
                song_lyric_dict[i[2]] = lyrics_word_counting
            

        scatter_data = go.Scatter(y=list(song_lyric_dict.values()),x=list(list(song_lyric_dict.keys())))
        basic_layout = go.Layout(title = 'The word count of lyrics of songs')
        fig = go.Figure(data=scatter_data, layout=basic_layout)
        fig.show()

def bar_lyrics_mean(artistnames = [], artistids =[]):
    # and bar plot for the mean of lyrics words of multiple artists
    
    artist_lyric_dict = {}
    for a in artistids:
        song_lyric_dict = {}
        songs_info = database.select_song(artist_id = a,other = ['lyrics'])
        for i in songs_info:
            lyrics_text = i[-1]
            lyrics_word_counting =  len(lyrics_text.split(' '))
            song_lyric_dict[i[2]] = lyrics_word_counting
        artist_lyric_dict[a] = statistics.mean(list(song_lyric_dict.values()))

    bar_data = go.Bar(y=list(artist_lyric_dict.values()),x=artistnames)
    basic_layout = go.Layout(title = 'The word count of lyrics of songs of ' + ','.join(artistnames) )
    fig = go.Figure(data=bar_data, layout=basic_layout)
    fig.show()

def word_appearance(artistnames = [], artistids =[],word = 'love'):
    ## for example, we can count how many time does 'love' appears in each artist's songs on average:
    artist_lyric_dict = {}
    for a in artistids:
        song_lyric_dict = {}
        songs_info = database.select_song(artist_id = a,other = ['lyrics'])
        for i in songs_info:
            lyrics_text = i[-1]
            lyrics_love_counting =  Counter(lyrics_text.lower().split(' '))[word]
            song_lyric_dict[i[2]] = lyrics_love_counting
        artist_lyric_dict[a] = statistics.mean(list(song_lyric_dict.values()))

    bar_data = go.Bar(y=list(artist_lyric_dict.values()),x=artistnames)
    basic_layout = go.Layout(title = 'The appearance of word [love] in lyrics of songs of' + ','.join(artistnames) )
    fig = go.Figure(data=bar_data, layout=basic_layout)
    fig.show()
      
    
 

if __name__ == "__mainformation_dict_list__":
    #####################################################################################
    #[1] display the information of artist or song
    ## if you want detailed information of an artist:
    info = database.select_artist(name = 'Bruno Mars')
    print(info)
    ## the basic artist_ID will return, you can choose to get other information of her
    aid = info[0][0]
    ## the attributes including:   url, description, facebook_name, twitter_name, image_url
    info1 = database.select_artist(name = 'Bruno Mars', other= ['url', 'description',' facebook_name','twitter_name','imag_url'])
    print(info1)
    
    ## we can use the artist_ID to get the all song from this artist
    song_info = database.select_song(artist_id = aid)
    print(song_info)
    ## the other attributes including: 
    info1 = database.select_song(title = '24K Magic', 
    other= ['url', 'description','release_date','lyrics_state','lyrics_path','lyrics'])
    print(info1)
    '''
    I may use plots like bar chart or line chart to display the 
    songs in terms of the artist, 
    the birth date of the song the 
    length of words of the lyrics. 
    The type of the chart is dependent on the choice of the user.
     ''' 
    #####################################################################################
    #[2] plot type1: bar plot
    ## we can compare the number of songs from the same artist in the database
    ## e.g : 
    songlength = []
    
    artistlist =  ['Britney Spears','Bruno Mars','Ariana Grande','Michael Jackson',
        'The Beatles','Lady Gaga']
    for  a in artistlist:
        info = database.select_song(artist_id = database.select_artist(name = a)[0][0])
        print(info)
        songlength.append(len(info))
    print(songlength)
    bar_data = go.Bar(x=artistlist,y=songlength)
    basic_layout = go.Layout(title = 'The song preserved in database')
    fig = go.Figure(data=bar_data, layout=basic_layout)


    fig.show()

    #####################################################################################
    #[3] plot type2: scatter plot
    ## we can we can trace the release of the songs of a singer. The following picture displays the song released by 'Britney Spears', it is sorted by the release time. 
    ## Similarly, if correct input set, we can sort whatever songs.
    a = artistlist[0]
    song_name_rel_date_dict = {}
    songs_info = database.select_song(artist_id = database.select_artist(name = a)[0][0],other = ['release_date'])
    for i in songs_info:
    
        song_name_rel_date_dict[i[2]]=i[-1]
      
    df={k: datetime.strptime(v,'%Y-%m-%d') for k, v in sorted(song_name_rel_date_dict.items(), key=lambda item: item[1])} 
    
    bar_data = go.Scatter(x=list(df.values()),y=list(df.keys()))
    basic_layout = go.Layout(title = 'The release date of songs')
    fig = go.Figure(data=bar_data, layout=basic_layout)


    fig.show()
    #####################################################################################
    #[4] lyric words counting: using scatter plot for the single artist and bar plot for multiple artist
    ## this require the processing of text
    ## in the future, we can display more amazing graph if the processing is advanced
    artistlist = ['Britney Spears','Bruno Mars','Ariana Grande']
    
    artist_lyric_dict = {}
    for a in artistlist:
        song_lyric_dict = {}
        songs_info = database.select_song(artist_id = database.select_artist(name = a)[0][0],other = ['lyrics'])
        for i in songs_info:
            lyrics_text = i[-1]
            lyrics_word_counting =  len(lyrics_text.split(' '))
            song_lyric_dict[i[2]] = lyrics_word_counting
        scatter_data = go.Scatter(y=list(song_lyric_dict.values()),x=list(list(song_lyric_dict.keys())))
        basic_layout = go.Layout(title = 'The word count of lyrics of song from ' + a )
        fig = go.Figure(data=scatter_data, layout=basic_layout)
        fig.show()
        artist_lyric_dict[a] = statistics.mean(list(song_lyric_dict.values()))

    bar_data = go.Bar(y=list(artist_lyric_dict.values()),x=list(list(artist_lyric_dict.keys())))
    basic_layout = go.Layout(title = 'The word count of lyrics of songs of ' + ','.join(artistlist) )
    fig = go.Figure(data=bar_data, layout=basic_layout)
    fig.show()

    ## for example, we can count how many time does 'love' appears in each artist's songs on average:
    artist_lyric_dict = {}
    for a in artistlist:
        song_lyric_dict = {}
        songs_info = database.select_song(artist_id = database.select_artist(name = a)[0][0],other = ['lyrics'])
        for i in songs_info:
            lyrics_text = i[-1]
            lyrics_love_counting =  Counter(lyrics_text.lower().split(' '))['love']
            song_lyric_dict[i[2]] = lyrics_love_counting
        artist_lyric_dict[a] = statistics.mean(list(song_lyric_dict.values()))

    bar_data = go.Bar(y=list(artist_lyric_dict.values()),x=list(list(artist_lyric_dict.keys())))
    basic_layout = go.Layout(title = 'The appearance of word [love] in lyrics of songs of' + ','.join(artistlist) )
    fig = go.Figure(data=bar_data, layout=basic_layout)
    fig.show()
      
    
    
   
    






