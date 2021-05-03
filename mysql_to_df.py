import mysql.connector
import twitch
import pandas as pd

# Assume that separated tables are combined together e.g. Twitch_date1, Twitch_date2, ... are combined as twitch 
# and tag_date1,... are combined as tag

def streams(cur):
    """
    cur mysql.connector.cursor_cext.CMySQLCursor"""
    # stores information dictionaries 
    streams_info = []
    # executes query 
    query = "SELECT * FROM {}".format("twitch")
    cur.execute(query)
    returns = cur.fetchall()
    for stream in returns:
        about_stream = {}
        about_stream["date"] = stream[0]
        about_stream["id"] = stream[1]
        about_stream["user_id"] = stream[2]
        about_stream["user_login"] = stream[3]
        about_stream["user_name"] = stream[4]
        about_stream["game_id"] = stream[5]
        about_stream["game_name"] = stream[6]
        about_stream["title"] = stream[7]
        about_stream["viewer_count"] = stream[8]
        about_stream["started_at"] = stream[9]
        about_stream["language"] = stream[10]
        img = stream[11].format(width = '600', height = '430')
        about_stream["thumbnail_url"] = img
        about_stream["tag_ids"] = stream[12]
        streams_info.append(about_stream)
    return streams_info

def tags(cur):
    """
    gets tags information.
    cur mysql.connector.cursor_cext.CMySQLCursor"""
    # stores information dictionaries 
    tags_info = []
    # executes query 
    
    query = "SELECT * FROM {}".format("tag")
    cur.execute(query)
    returns = cur.fetchall()
    for tag in returns:
        about_tag = {}
        about_tag["date"] = tag[0]
        about_tag["tag_id"] = tag[1]
        about_tag["is_auto"] = tag[2]
        about_tag["localization_names"] = tag[3]
        about_tag["localization_descriptions"] = tag[4]
        tags_info.append(about_tag)
    return pd.DataFrame(tags_info)


def streamers(cur):
    """get streamer's background information.
    cur mysql.connector.cursor_cext.CMySQLCursor"""
    # get streams' information
    stream = streams(cur)
    top_streams = pd.DataFrame(stream)
    description_list = []
    profile_image_url_list=[]
    total_view_count_list = []
    created_at_list = []
    video_published_at_list = []
    video_url_list = []
    # for streamers who emerged in top streams, we further query 
    # their background information
    for i in top_streams['user_id']:
        user_query = twitch.get_user_query(i)
        user_response = twitch.get_response(user_query)
        for h, item in enumerate(user_response['data']):
            description = item.get('description', None)
            profile_image_url = item.get('profile_image_url', None)
            total_view_count = item.get('view_count', None)
            created_at = item.get('created_at', None)
            user_id = item.get('id', None)
            description_list.append(description)
            profile_image_url_list.append(profile_image_url)
            total_view_count_list.append(total_view_count)
            created_at_list.append(created_at)
        # get the recent video urls
        video_query = twitch.get_video_query(i)
        video_response = twitch.get_response(video_query)
        if len(video_response['data']) == 0:
            video_url_list.append('NaN')
            video_published_at_list.append('NaN')
        else:
            for h, item in enumerate(video_response['data'][:1]):
                video_published_at = item.get('published_at', None)
                video_url = item.get('url', None)
                video_url_list.append(video_url)
                video_published_at_list.append(video_published_at)
    # create new columns into the df 
    top_streams['description'] = description_list
    top_streams['profile_image_url'] = profile_image_url_list
    top_streams['total_view_count'] = total_view_count_list
    top_streams['created_at'] = created_at_list
    top_streams['video_url'] = video_url_list
    top_streams['video_published_at'] = video_published_at_list
    return top_streams

def get_games(cur):
    """get count information for each game.
    cur mysql.connector.cursor_cext.CMySQLCursor"""
    stream = streams(cur)
    top_streams = pd.DataFrame(stream)
    games_info = top_streams[['game_name', 'iewer_count']]
    games_info.to_csv("game_viewer_count.csv")
