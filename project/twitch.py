import json
import requests
import sys

base_url = 'https://api.twitch.tv/helix/'
client_id = 'gp762nuuoqcoxypju8c569th9wz7q5'
token = '8dce0b615cnar1j3hnrq1pjaehes8v'
headers = {'Client-ID': client_id, 'Authorization': f'Bearer {token}',"Accept": "application/vnd.v5+json"}


#get reponse from twitch API call
def get_response(query):
        url = base_url+query
        response = requests.get(url, headers=headers).json()
        return response

#get stream tags  
def get_tags_query(tag_id):
    return 'tags/streams?first=100&tag_id={0}'.format(tag_id)

#get streams with top views 
def get_user_streams_query(top_number):
    return 'streams?first={0}'.format(top_number)

#get user's info
def get_user_query(user_id):
    return 'users?id={0}'.format(user_id)

#get user's info
def get_stream_query(user_login):
    return 'streams?user_login={0}'.format(user_login)

#get videos on user's page
def get_user_videos_query(user_id):
    return 'streams?login={0}&first=50'.format(user_id)

#get game info
def get_game_query(game_name):
    return 'games?name={0}'.format(game_name)

#get number of follows to certain user id
def get_follows(to_id):
    return 'users/follows?to_id={0}'.format(to_id)

#get videos
def get_video_query(id):
    return 'videos?user_id={}'.format(id)
