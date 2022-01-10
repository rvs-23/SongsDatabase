import os
import pandas as pd
import json
import sys
from googleapiclient.discovery import build

base_path = os.path.dirname(__file__)
modules_path = os.path.join(base_path, '../modules/')
sys.path.insert(1, modules_path)

from module_extract_urls_1 import ParseYtHistory
from module_fetch_video_details_2 import FetchVideoDetails
from module_identify_music_video_3 import IdentifyMusicVideo

history_file_path = os.path.join(base_path, '../_private_data/watch-history.json')
api_key_path = os.path.join(base_path, '../_private_data/api_key.txt')
watched_urls_path = os.path.join(base_path, '../_private_data/WatchedURLs.csv')

def open_files(history_file_path, api_key_path, is_json=True):    
    with open(api_key_path, 'r') as file:
        ak = file.read()
        
    if is_json:
        with open(history_file_path, 'r', encoding='utf-8') as file:
            h = json.load(file)
    else:
        with open(history_file_path, 'r', encoding='utf-8') as file:
            h = file.read()
        
    return h, ak

# Check if we have already fetched all the details of all the URLs
complete_file_path = os.path.join(base_path, '../_private_data/WatchedURLs_allDetails.csv')
if os.path.isfile(complete_file_path):
    print("File with all details exists... Opening...")
    df_complete_history_details = pd.read_csv(complete_file_path)
    
else:
    
    history, api_key = open_files(history_file_path, api_key_path, is_json=True)
    
    # Check if we have already created a CSV of all the watched URLs
    if os.path.isfile(watched_urls_path):
        print("File with all URLs exists... Opening...")
        df_video_history = pd.read_csv(watched_urls_path)
    else:
        parse_obj = ParseYtHistory(history)
        df_video_history = parse_obj.createLinksCSV()
        df_video_history.to_csv(watched_urls_path, index=False, encoding='utf-8')
    
    yt = build('youtube', 'v3', developerKey=api_key)
    details_obj = FetchVideoDetails(yt, df_video_history)
    df_complete_history_details = details_obj.get_complete_details()

    # It's possible that some videos may be removed or are no longer available.
    # For those cases, the parameters returned are NaN, therefore we drop them.
    # df_complete_history_details[['CategoryId']].dropna(inplace=True)
    complete_file_path = os.path.join(base_path, '../_private_data/WatchedURLs_allDetails.csv')
    df_complete_history_details.to_csv(complete_file_path, index=False, encoding='utf-8')

music_file_path = os.path.join(base_path, '../_private_data/WatchedURLs_MusicVideos.csv')
watched_music_videos = IdentifyMusicVideo.filter_music_video(df_complete_history_details)
watched_music_videos.to_csv(music_file_path, index='False', encoding=False)

###############################################################################
