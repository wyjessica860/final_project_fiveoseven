from data_crawling import search_response,id_response,lyric_url_response

class artist():
    def __init__(self, json_dict):
        self.Id = json_dict['id']
        self.name = json_dict['name']
        self.url = json_dict['url']
        self.facebook_name = json_dict['facebook_name']
        self.twitter_name = json_dict['twitter_name']
        self.image_url = json_dict['image_url']
        self.description = ''
        for i in json_dict['description']['dom']['children']:
            try:
                for x in i['children']:
                    if type(x) == str: self.description += x
            except:
                continue
class song():
    def __init__(self, json_dict):
        self.Song_Id = json_dict['id']
        self.Artist_ID = json_dict['primary_artist']['id']
        self.song_title = json_dict['title']
        self.url = json_dict['url']
        self.release_date = json_dict['release_date']
        self.lyrics_state = json_dict['lyrics_state']
        self.lyrics_path = json_dict['path']
        self.lyrics = ''
        self.description = ''
        for i in json_dict['description']['dom']['children']:
            try:
                for x in i['children']:
                    if type(x) == str: self.description += x
            except:
                continue                   
    def get_lyrics(self):
        if self.lyrics_state == 'complete':
            self.lyrics = lyric_url_response('/Kendrick-lamar-humble-lyrics')


if __name__ == "__main__":
    '''
    text1 = search_response('Kendrick Lamar'))
    text2 = id_response('/songs/3039923'))
    lyric = (lyric_url_response('/Kendrick-lamar-humble-lyrics'))
    '''
    X = artist(id_response('/artists/1421')['response']['artist'])
    a2 = song(id_response('/songs/3039923')['response']['song'])
    print('')


