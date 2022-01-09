import os
import pandas as pd
import json
from googleapiclient.discovery import build
from module_extract_urls_1 import ParseYtHistory
from module_fetch_video_details_2 import FetchVideoDetails

base_path = os.path.dirname(__file__)

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

history, api_key = open_files(history_file_path, api_key_path, is_json=True)

if os.path.isfile(watched_urls_path):
    print("File exists... Using the existing CSV.")
    df_video_history = pd.read_csv(watched_urls_path)
else:
    parse_obj = ParseYtHistory(history)
    df_video_history = parse_obj.createLinksCSV()
    df_video_history.to_csv(watched_urls_path, index=False, encoding='utf-8')

yt = build('youtube', 'v3', developerKey=api_key)
details_obj = FetchVideoDetails(yt, df_video_history)
df_complete_history_details = details_obj.get_complete_details()

complete_file_path = os.path.join(base_path, '../private_data/WatchedURLs_allDetails.csv')
df_complete_history_details.to_csv(complete_file_path, index=False, encoding='utf-8')

###############################################################################
