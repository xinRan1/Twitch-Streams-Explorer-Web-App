import mysql.connector
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.figure import Figure
import seaborn as sns
import statsmodels
from PIL import Image
from statsmodels.nonparametric.smoothers_lowess import lowess
import streamlit as st
from streamlit_player import st_player
import base64
import plotly.express as px
import twitch
import mysql_to_df as fromSQL
import time
import datetime
import re
import pycountry

# connects to database dsci551
cnx = mysql.connector.connect(user='dsci551', password='Dsci-551', host='127.0.0.1', database='dsci551')  
cursor = cnx.cursor()

@st.cache(allow_output_mutation = True)
def get_data(file_name):
    data = pd.read_csv(file_name)
    return data

@st.cache(allow_output_mutation = True)
def get_top_stream(number):
    top_stream_query = twitch.get_user_streams_query(number)
    top_stream_response = twitch.get_response(top_stream_query)
    list = []
    for i, item in enumerate(top_stream_response['data']):
        list.append({
            "id": item.get('id', None),
            'user_id' : item.get('user_id', None),
            'user_login': item.get('user_login', None),
            'video_url' : live_stream_base_url + item.get('user_login', None),
            'user_name': item.get('user_name', None),
            'game_id':item.get('game_id', None),
            'game_name' : item.get('game_name', None),
            'title' : item.get('title', None),
            'viewer_count': item.get('viewer_count', None),
            'started_at' : item.get('started_at', None),
            'language' : item.get('language', None),
            'thumbnail_url' : item.get('thumbnail_url', None)})
    return pd.DataFrame(list)

@st.cache(allow_output_mutation = True)
def get_viewer_count(user_login):
    stream_query = twitch.get_stream_query(user_login)
    stream_response = twitch.get_response(stream_query)
    for i, item in enumerate(stream_response['data']):
        return np.array(item.get('viewer_count', None))

@st.cache(allow_output_mutation = True)
def get_game_image(game_name):
    query = twitch.get_game_query(game_name)
    response = twitch.get_response(query)
    for h, item in enumerate(response['data']):
        game_url = item.get('box_art_url', None)
    return game_url

@st.cache(allow_output_mutation = True)
def get_game_streamer(game_name):
    gp = stream_data.groupby('game_name')
    game_group = gp.get_group(game_name)
    game_filter = game_group.loc[(game_group['viewer_count'] == max(game_group['viewer_count']))]
    return(game_filter['user_name'].values[0])


stream_data = fromSQL.streamers(cursor)

LANG = []

for lang in stream_data['language']:
    try:
        Lang = pycountry.languages.get(alpha_2=lang).name
    except:
        Lang = 'Other'
    LANG.append(Lang)

stream_data['languages'] = LANG



pd.to_datetime(stream_data['date'], format='%Y/%m/%d')
stream_data['viewer_count'] = pd.to_numeric(stream_data['viewer_count'])

languages = stream_data['languages'].unique()

remove_nan= stream_data[['id','user_name','date', 'profile_image_url', 'total_view_count', 'created_at', 'video_url', 'video_published_at', 'description','language','languages']]
recor=remove_nan.dropna()

top_games = pd.DataFrame(stream_data['game_name'])
live_stream_base_url = 'https://www.twitch.tv/'
games = get_data('game.csv')
game_data=games.sort_values(by = ['total_viewer_count'], ascending=False).reset_index(drop=True)
column = ['date', 'user_name', 'id', 'game_name', 'title', 'viewer_count', 'started_at', 'languages']


main_bg = "background.jpg"
main_bg_ext = "jpg"

side_bg = "sidebar.jpg"
side_bg_ext = "jpg"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    }}
   .sidebar .sidebar-content {{
        background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()})
    }}
    </style>
    """,
    unsafe_allow_html=True
)



not_available = Image.open('not_available.jpg')
twitch_logo = Image.open('twitch.jpg')

logo_1 = Image.open('twitch_logo.png')
logo_2 = Image.open('steam_logo.png')
st.image(twitch_logo, use_column_width = True)

st.title('Twitch Streams Explorer ')

selected_table = st.selectbox('Which section do you want to explore?', ['Home', 'Top Streams in Last Two Weeks', 'Streamer Info', 'Popular Games', 'Current Top Streams'])

_lock = RendererAgg.lock 
plt.style.use('default')




if selected_table == 'Home':

    st.markdown("<h2 style='text-align: center; color: purple;'>Welcome to Twitch Streams Explorer!</h1>", unsafe_allow_html=True)

    home_page_pic = Image.open('home_page_pic.jpg')
    st.image(home_page_pic, use_column_width = True)


    st.markdown('**Twitch is one of the most popular and biggest live-streaming platforms in the world. Millions of people come together to watch, chat, and enjoy gaming.\
          It is currently ranked 4th in the peak US internet traffic websites. As of February 2020, it had 3 million broadcasters monthly and 15 million daily active users,\
               with 1.4 million average concurrent users. Since last year, lockdowns due to COVID-19 even brought a surge in TV watching and online streaming,\
               and this live-streaming boom won’t slow down. In here, you can explore all kinds of data from Twitch: real-time information about most popular live-streaming, top games, recent top streams, your favorite streamers and their videos! Enjoy!!**')





elif selected_table == 'Top Streams in Last Two Weeks':
    st.header('Top Streams')
    streamer_keyword = st.sidebar.text_input('Streamer Name')
    id_search = st.sidebar.text_input('Streamer ID') 
    game_search = st.sidebar.text_input('Game Name') 

    viewer_count = st.sidebar.slider('Number of Viewers', min(stream_data['viewer_count']), max(stream_data['viewer_count']))
    

    orderby = st.sidebar.selectbox('Order By', ['viewer_count', 'date', "started_at"], key= 'date')
    order = st.sidebar.selectbox('Order', ['Descending','Ascending'], key= 'DESC') 
    order = True if order == 'Ascending' else False
    limit = st.sidebar.slider('Showing Number of Streams', min_value = 1, max_value = stream_data.shape[0], value = stream_data.shape[0])
    seletced_language = st.sidebar.multiselect('Language', languages) or languages

    st.dataframe(stream_data[column]\
        [
            (stream_data['user_name'].str.contains(streamer_keyword, flags=re.IGNORECASE)) &\
                (stream_data['id'].astype(str).str.match(id_search)) &\
                    (stream_data['game_name'].str.contains(game_search, flags=re.IGNORECASE)) &\
            (viewer_count <= stream_data['viewer_count']) &\
           (stream_data['languages'].isin(seletced_language))].sort_values(orderby, ascending = order).head(limit).reset_index(drop=True))

    st.text('')
    col1,col2 = st.beta_columns(2)

    col1.text('')
    col1.text('')
    col1.text('')
    col1.text('')
    col1.text('')
    col1.image(logo_1, width = 300)
    col2.image(logo_2, width = 300)


elif selected_table == 'Streamer Info':

    st.header('Streamer Information')
    

    records = recor.to_dict('records')
    selected_data = st.selectbox('Select a Streamer', options=records,
    format_func=lambda record: f'{record["user_name"]}')
    streamer = selected_data.get('user_name')

    streamer_filter = recor.loc[(recor['user_name'] == streamer)]
    profile_pic = streamer_filter['profile_image_url'].dropna().iloc[-1]
    video = streamer_filter['video_url'].dropna().iloc[-1]

    col1,col2 = st.beta_columns(2)

    col1.subheader('Streamer Profile Picture')
    col1.image(profile_pic, width=320)

    views = streamer_filter['total_view_count'].dropna().iloc[-1]
    language = streamer_filter['languages'].dropna().iloc[-1]
    col2.text('')
    col2.text('')
    col2.subheader('Historical Number of Views')
    col2.text(int(views))
    tags = set(list(streamer_filter['description'].dropna()))
    col2.subheader("Channel Description")
    col2.text('; '.join(tags))
    col2.subheader("Date When the Channel was Created")
    created_at = streamer_filter['created_at'].dropna().iloc[-1]
    date = datetime.datetime.strptime(created_at,"%Y-%m-%dT%H:%M:%S.%fZ")
    new_format = "%Y-%m-%d"
    date.strftime(new_format)
    col2.text(str(date).split()[0])


    col2.subheader("Language")
    col2.text(language)

    video_published_at = streamer_filter['video_published_at'].dropna().iloc[-1]
    video_date = datetime.datetime.strptime(video_published_at,"%Y-%m-%dT%H:%M:%SZ")
    video_date.strftime(new_format)
    st.subheader('Most Recent Video')
    st.text("published at {}".format(video_date))
    try:
        video = streamer_filter['video_url'].dropna().iloc[-1]
    except:
        video = "No Recent Video"
        st.subheader(video)
    else:
        st_player(video)
 



elif selected_table == 'Popular Games':

    st.header('Top Games on Twitch')
    


    total_viewer_count = st.sidebar.slider('Minimum Number of Viewers', min(game_data['total_viewer_count']), max(game_data['total_viewer_count']))
    average_viewer_count = st.sidebar.slider('Average Number of Viewers', min(game_data['average_viewer_count']), max(game_data['average_viewer_count']))
    stream_count = st.sidebar.slider('Number of Streams', min(game_data['stream_count']), max(game_data['stream_count']))
    orderby = st.sidebar.selectbox('Order by', ['total_viewer_count', 'average_viewer_count', 'stream_count'], key= 'total_viewer_count')
    order = st.sidebar.selectbox('Order', ['Descending','Ascending'], key= 'DESC') 
    order = True if order == 'Ascending' else False
    limit = st.sidebar.slider('Select number of records', min_value = 1, max_value = game_data.shape[0], value = game_data.shape[0])
  

            
    selected_game = st.sidebar.selectbox('Select a Game',game_data['game_name'])

    st.dataframe(game_data[['game_name', 'total_viewer_count', 'average_viewer_count','stream_count']]\
        [
            (total_viewer_count <= game_data['total_viewer_count']) &\
           (average_viewer_count <= game_data['average_viewer_count']) &\
               (stream_count <= game_data['stream_count'])].sort_values(orderby, ascending = order).head(limit))



    if st.sidebar.checkbox("Show Game Analysis", False, key=2):
        st.markdown("## **_Game Analysis for %s_**" % (selected_game))

        col1,col2 = st.beta_columns(2)

        col1.text('')
        col1.text('')
        col1.text('')
        col1.text('\n')
        game_filter = game_data.loc[(game_data['game_name'] == selected_game)]
        total_viewer_count = int(game_filter['total_viewer_count'].values)
        total_number_of_audience = int(sum(game_data['total_viewer_count']))


        
        try:
            game_image = get_game_image(selected_game)
            col1.image(game_image.format(width = 500, height = 500))
        except:
            col1.image(not_available, width = 400)


        col2.write('')
        col2.write('')
        col2.markdown('#### **Total Viewer Count:    {}**'.format(total_viewer_count))
        col2.write('')
        col2.markdown('#### **Average Viewer Count:    {}**'.format(int(game_filter['average_viewer_count'].values)))
        col2.write('')
        col2.markdown('#### **Number of Streams Playing This Game:    {}**'.format(int(game_filter['stream_count'].values)))
        col2.write('')
        col2.markdown('#### **Audience Percentage:    {} %**'.format(str(round(100*total_viewer_count/total_number_of_audience, 2))))
        col2.write('')
        col2.markdown('#### **Most Popular Streamer:    {}**'.format(get_game_streamer(selected_game)))
        col2.text('')
        streamer_filter_for_game = remove_nan.loc[(remove_nan['user_name'] == get_game_streamer(selected_game))]
        profile_pic_for_game = streamer_filter_for_game['profile_image_url'].dropna().iloc[-1]
        col2.image(profile_pic_for_game, width=150)


        st.subheader("Average Number of Audience Watching This Game")
        game_hist= px.bar(
            games[['game_name', 'average_viewer_count']], 
            x='game_name',
            y='average_viewer_count',
            color="game_name",
            labels={'Average Number of Audience Watching This Game':'Number of Games in %s' % (selected_game)})
        for d in game_hist['data']:
            if d['name'] == selected_game:
                d['marker']['color']='purple'
            else:
                d['marker']['color']='lightgrey'

        st.plotly_chart(game_hist)

        


elif selected_table == 'Current Top Streams':
    st.header('Current Top Streams on Twitch')
    top_stream_number = st.number_input("How many top streams do you want to explore? Maximum: 100", value=1, step=1, max_value=100)

    if st.checkbox("Click to Show"):
       
        current_top_stream = get_top_stream(top_stream_number)

        top_stream_recor = current_top_stream[['id','user_name','started_at', 'thumbnail_url', 'viewer_count', 'language', 'video_url', 'game_name']]   
        top_stream_records = top_stream_recor.to_dict('records')
        selected_top_stream = st.selectbox('Select a Streamer', options= top_stream_records, format_func=lambda record: f'{record["user_name"]}')
        top_streamer = selected_top_stream.get('user_name')
        if top_streamer:

            top_streamer_filter = top_stream_recor.loc[(top_stream_recor['user_name'] == top_streamer)]
            live_broadcast = top_streamer_filter['video_url'].dropna().iloc[-1]
            last_rows = get_viewer_count(top_streamer).reshape(1,1)

            st.subheader('Streamer Live Broadcast')
            st_player(live_broadcast)

            st.subheader('Game Playing')
            st.text(top_streamer_filter['game_name'].iloc[-1])

            st.subheader('Real-Time Viewer Count')
            chart = st.line_chart(last_rows)

            while True:
                new_rows = get_viewer_count(top_streamer).reshape(1,1)
                chart.add_rows(new_rows)
                time.sleep(4)

