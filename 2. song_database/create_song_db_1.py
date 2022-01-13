r'''

Steps:
    - First we extract the URL, Text(title), Date(only for json) and VideoID from the history file and create a csv.
    - If this file already exists, we open it.
    - For all the VideoIDs present, we fetch the details and add it to the dataframe.
    - If this file already exists, we open it.
    - Figure out the duration of our Watched History.
    - Pass the dataframe to the filter_music_video pass through the first layer of music identification filter.
    - Create a csv of the database.
'''

import os
import pandas as pd
import json
import sys
from googleapiclient.discovery import build

base_path = os.path.dirname(__file__)
modules_path = os.path.join(base_path, '../1. modules/')
sys.path.insert(1, modules_path)

from module_extract_urls_1 import ParseYtHistory
from module_fetch_video_details_2 import FetchVideoDetails
from module_identify_music_video_3 import IdentifyMusicVideo

####################################

# 1. Opening HTML/JSON file and the API-key file.

history_file_path = os.path.join(base_path, '../_private_data/watch-history.json')
api_key_path = os.path.join(base_path, '../_private_data/api_key.txt')

def open_files(history_file_path, api_key_path, is_json=True):        
    if is_json:
        with open(history_file_path, 'r', encoding='utf-8') as file:
            h = json.load(file)
    else:
        with open(history_file_path, 'r', encoding='utf-8') as file:
            h = file.read()

    with open(api_key_path, 'r') as file:
        ak = file.read()
    
    return h, ak

#######################################

# 2. Creating/Opening csv file that contains all details of our YT history.

complete_history_details_path = os.path.join(base_path, '../_private_data/WatchedURLs_allDetails.csv')
# We check if file with all details already exists. If not, we create it
if os.path.isfile(complete_history_details_path):
    print("File with all details exists... Opening...")
    df_history_details = pd.read_csv(complete_history_details_path)
else:
    print("Fetching all details of your watched videos...")
    print("Need csv with watched history URLs...")
    history, api_key = open_files(history_file_path, api_key_path, is_json=True)
    # To create the file with all details, we first need the csv with history URLs
    # We open if it already exists, create it otherwise
    watched_urls_path = os.path.join(base_path, '../_private_data/WatchedURLs.csv')
    if os.path.isfile(watched_urls_path):
        print("File containing history URLs exists... Opening...")
        df_history_urls = pd.read_csv(watched_urls_path)
    else:
        print("Creating watched history URLs file from the history file...")
        # We create the file using the ParseYtHistory class
        df_history_urls = ParseYtHistory(history).createLinksCSV()
        df_history_urls.to_csv(watched_urls_path, index=False, encoding='utf-8')
        print("Watched history URL file created...")
        
    print("Fetching details using the API...")
    yt = build('youtube', 'v3', developerKey=api_key)
    df_history_details = FetchVideoDetails(yt, df_history_urls).get_complete_details()
    df_history_details.to_csv(complete_history_details_path, index=False, encoding='utf-8')
    print("File with all details created...")
    
# Figuring out the duration of our history.
if 'WatchDate' in df_history_details.columns:
    df_history_details['WatchDate'] = pd.to_datetime(df_history_details['WatchDate'])
    min_date = df_history_details['WatchDate'].min().date()
    max_date = df_history_details['WatchDate'].max().date()
    print(f"The history file contains data from dates(yy-mm-dd) {min_date.strftime('%y-%m-%d')} to {max_date.strftime('%y-%m-%d')}.")
    print(f"Number of days: {(max_date-min_date).days}.")
    print(f"Number of months (approx): {(max_date-min_date).days//30}.\n")

#########################################

print("Building an initial database...")
music_database_path = os.path.join(base_path, 'songs_heard/InitialMusicDatabase.csv')
watched_music_videos = IdentifyMusicVideo(df_history_details).filter_music_video()
watched_music_videos.to_csv(music_database_path, index=False, encoding='utf-8')
print("Done!")

##########################################

# Fetching all details of your watched videos...
# Need csv with watched history URLs...
# File containing history URLs exists... Opening...
# Fetching details using the API...
# File with all details created...
# The history file contains data from dates(yy-mm-dd) 21-08-03 to 22-01-09.
# Number of days: 159.
# Number of months (approx): 5.

# Building an initial database...
# Done!
