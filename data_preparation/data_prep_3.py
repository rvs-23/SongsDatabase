r'''

'''
from googleapiclient.discovery import build
from pprint import pprint
import os
import pandas as pd

base_path = os.path.dirname(__file__)
api_file = os.path.join(base_path, '../_private_data/api_key.txt')

with open(api_file) as file:
    api_key = file.read()

def get_video_details(youtube_build, video_ids):
    '''
    Function to get the 
    video_ids -> list of video ids whose details we want to fetch
    
    '''
    # YouTube limits to only 50 requests per execute so we need to divide
    # the video_ids into batches of 50 to fetch the details.
    
    all_video_details = list()
    
    for limit in range(0, len(video_ids), 50):
        request = youtube_build.videos().list(part='snippet', id=','.join(video_ids))
        response = request.execute()
        # The response object will have the details of all 50 videos.
        # So, we loop over to extract info one by one. The 'items' key contains
        # all the details that we are after
        for video in response['items']:
            snippet = video['snippet']
            video_detail = dict(
                Title=snippet['title'],
                Category=snippet['categoryId'],
                PublishDate=snippet['publishedAt'],
                ChannelTitle=snippet['channelTitle'],
                Description=snippet['description'],
                Tags=snippet['tags'],
                )
            
            all_video_details.append(video_detail)
        
    return all_video_details

yt = build('youtube', 'v3', developerKey=api_key)
pprint(get_video_details(yt, ['WnU0lH6C0EA', '5MkfBNl_3pw']))

####################################################################

