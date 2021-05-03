import twitch 
import pandas as pd
import re
from mysql.connector import errorcode
from datetime import datetime
import pymysql

date = datetime.today().strftime('%Y%m%d')
twitch_date = "Twitch_" + date
tag_date = "tag_" + date

# assume we have this user and database already
cnx = pymysql.connect(user='dsci551', password='Dsci-551', host='127.0.0.1', database='dsci551')
cursor = cnx.cursor()

# check the existence of tables
check_twitch_table = "DROP TABLE IF EXISTS {}".format(twitch_date)
cursor.execute(check_twitch_table)

check_tag_table = "DROP TABLE IF EXISTS {}".format(tag_date)
cursor.execute(check_tag_table)


def get_stream(top_number):
    """returns top 100 streams from twitch
    top_number number"""
    query = twitch.get_user_streams_query(top_number)
    response = twitch.get_response(query)
    return response 

def get_tags(streams):
    """returns tags for top 30 streams' tags and queries their descriptions
    streams dictionary"""
    tag_list = []
    for stream in streams:
        for tags in stream["tag_ids"]:
            if tags not in tag_list:
                tag_list.append(tags)
    # adds tag_id parameters
    id = '&tag_id='.join(tag_list)
    query = twitch.get_tags_query(id)
    response = twitch.get_response(query)
    return response


 
"""
Create Table for Popular Streams
"""

cursor.execute("CREATE TABLE {} (date VARCHAR(255), id VARCHAR(255), user_id VARCHAR(255), user_login VARCHAR(255), user_name VARCHAR(255),\
       game_id VARCHAR(255), game_name VARCHAR(255), title VARCHAR(255), viewer_count VARCHAR(255), \
           started_at VARCHAR(255), language VARCHAR(255), thumbnail_url VARCHAR(255), tag_ids LONGTEXT)".format(twitch_date))

resp = get_stream(100)


for i, item in enumerate(resp['data']):
    id = item.get('id', None)
    user_id = item.get('user_id', None)
    user_login = item.get('user_login', None)
    user_name = item.get('user_name', None)
    game_id = item.get('game_id', None)
    game_name = item.get('game_name', None)
    title = item.get('title', None)
    viewer_count = item.get('viewer_count', None)
    started_at = item.get('started_at', None)
    language = item.get('language', None)
    thumbnail_url = item.get('thumbnail_url', None)
    tags = item.get('tag_ids', None)
    if len(tags) > 1:
        tag_ids = "&tag_id=".join(tags)
    else:
        tag_ids = tags
    attributes = (date, id, user_id, user_login, user_name, game_id, game_name, title, viewer_count, started_at, language, thumbnail_url, tag_ids)

    query = "INSERT INTO {} (date, id, user_id, user_login, user_name,\
        game_id, game_name, title, viewer_count, started_at, language, thumbnail_url, tag_ids) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s)".format(twitch_date)

    cursor.execute(query, attributes)
    cnx.commit()


"""
Create Table for Popular Tags
"""
tags = get_tags(resp['data'])
cursor.execute("CREATE TABLE {} (date VARCHAR(255), tag_id LONGTEXT, is_auto VARCHAR(255), localization_names LONGTEXT, localization_descriptions LONGTEXT)".format(tag_date))

for i, item in enumerate(tags['data']):
    tag_id = item.get('tag_id', None)
    is_auto = item.get('is_auto', None)
    tag_names = item.get('localization_names', None)
    localization_names = tag_names['en-us']
    tag_description = item.get('localization_descriptions', None)
    localization_descriptions = tag_description['en-us']
    columns = (date, tag_id, is_auto, localization_names, localization_descriptions)
    query = "INSERT INTO {} (date, tag_id, is_auto, localization_names, localization_descriptions) VALUES (%s, %s, %s, %s, %s)".format(tag_date)
    cursor.execute(query, columns)
    cnx.commit()



# except mysql.connector.Error as err:
#   print(err.msg)

cnx.close()
cursor.close() 



