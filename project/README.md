# DSCI-551-Final-Project

This folder contains the source code and data for USC DSCI-551 (21 Spring Data Management) Final Project. Authors are Jiahang Song and Xinran Liang.

Folders:

All the data are stored in the data folder (for your convenience, I saved them in csv format, you can download, put them in the same directory as streamlit_twitch.py and use them for the UI!!).

All the pictures for the UI are stored in the picture folder (Before run streamlit_twitch.py, please put the pictures inside in the same directory as it!!).

Files:

twitch_to_mysql.py is our data crawler.

game_spark.py provides parallel processing using spark to analyze game data.

twitch.py contains several functions to request different kinds of data from Twitch.

streamlit_twitch.py is the script for runing web application. Please run the command "streamlit run streamli_twitch.py" to start the web application. 


Required packages: 

json, requests, mysql.connector, pandas, numpy, matplotlib, seaborn, datetime, statsmodels, streamlit, streamlit_player, plotly. 

(If necessary, run 'pip install streamlit' and/or 'pip install streamlit_player' and/or 'pip install plotly'first.)

For the need of inspecting the version with mysql directly connecting to UI and Spark, please check: 
https://github.com/xinRan1/Twitch-Streams-Explorer-Web-App.git 
