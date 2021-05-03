# Twitch-Streams-Explorer-Web-App
This App gives people a shortcut to know latest information about Twitch.tv streams, streamers and games.
If you wanna try out the UI, please go to the folder, project, which contains testing data. Running time will be reduced with the testing codes.

Authors: Xinran Liang, Jiahang Song 
 (This Web App is used as final project for DSCI551 sp21 @ USC)

streamlit_twitch.py is the script for runing web application. Please run the command "streamlit run streamli_twitch.py" to start the web application. 
twitch_to_mysql.py is our data crawler.
twitch.py contains several functions to request different kinds of data from Twitch.
game_spark.py provides parallel processing using spark to analyze game data.
mysql_to_df.py is the script for grabbing data from mysql and reformatted them for UI building. 

Logic:

twitch.py + twitch_to_mysql.py to cumulate data for nonsynchronous part -> in mysql integrate tables in same type by syntax like "INSERT INTO Table_A SELECT * from Table_B" -> (mysql_to_df.py) game_spark.py -> (mysql_to_df.py) streamlit_twitch.py containing streaming part

Required packages: 

json, requests, mysql.connector, pandas, numpy, matplotlib, seaborn, datetime, statsmodels, streamlit, streamlit_player, plotly. 

(If necessary, run 'pip install streamlit' and/or 'pip install streamlit_player' and/or 'pip install plotly'first.)

