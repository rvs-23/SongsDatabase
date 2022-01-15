r"""
This is the second module of the project which performs the following tasks:
    - For a given video ID, fetches the details mentioned below.
    - Create a dataframe of the details associated to a VideoID.

Details that are fetched:
    -VideoID
    -Title
    -CategoryID
    -PublishDate
    -ChannelTitle
    -Duration
    -Description
    -Tags
        
Note: Youtube API allows for only 50 calls in one shot.
  
"""

import re
import pandas as pd
from datetime import timedelta

class FetchVideoDetails:
    """
    Class to fetch the necessary infromation of all VideoIDs and create
    a dataframe of the required details.
    """

    def __init__(self, YT_build, df_video_history):
        """
        param YT_build -> YouTube API resource
        param df_video_history -> dataframe containing the watched video URLs, Title
        and VideoIDs
        """
        self.YT_build = YT_build
        self.df_video_history = df_video_history

    def get_video_details(self, video_ids):
        """
        param video_ids -> All the video_ids present in the watched history.

        returns a dataframe of all the necessary video details for every VideoID
        """

        all_video_details = []

        # Breaking into batches of 50
        for limit in range(0, len(video_ids), 50):
            # Slicing 50 video IDs
            fifty_videos = video_ids[limit : limit + 50]
            # The contentDetails parameter contains the video duration.
            # The snippet parameter contains the rest of the information we need.
            request = self.YT_build.videos().list(
                part="snippet, contentDetails", id=",".join(fifty_videos)
            )
            response = request.execute()

            # Zip the video details and the ID together
            for details, yt_id in zip(response["items"], fifty_videos):
                snippet = details["snippet"]
                duration = details['contentDetails'].get('duration')
                # Fetching the necessary details from the snippet key
                every_video_detail = dict(
                    VideoID=yt_id,
                    Title=snippet.get("title"),
                    CategoryID=snippet.get("categoryId"),
                    PublishDate=snippet.get("publishedAt"),
                    ChannelTitle=snippet.get("channelTitle"),
                    Duration=duration,
                    Description=snippet.get("description"),
                    Tags=snippet.get("tags"),
                )

                # Adding every video one by one
                all_video_details.append(every_video_detail)

        return pd.DataFrame(all_video_details)

    @staticmethod
    def fetch_duration_sec(x):
        '''
        The Duration returned by YouTube is of the format: 1H2M31S
        
        This function uses regex to parse out the hours, minutes and seconds
        to calculate the total duration of the video in seconds.
        '''
        # Match the pattern to extract hours, minutes and seconds.
        hrs_pattern = re.compile(r'(\d+)H')
        mins_pattern = re.compile(r'(\d+)M')
        secs_pattern = re.compile(r'(\d+)S')
        
        hours = hrs_pattern.search(x)
        mins = mins_pattern.search(x)
        secs = secs_pattern.search(x)
        
        # If any result is None, return 0 else the duration
        hours = int(hours.group(1)) if hours else 0
        mins = int(mins.group(1)) if mins else 0
        secs = int(secs.group(1)) if secs else 0
        
        # Compute the total duration in seconds
        return timedelta(
            hours=hours,
            minutes=mins,
            seconds=secs
            ).total_seconds()
    
    
    def get_complete_details(self):
        '''
        Function that builds the DataFrame by merging details of every VideoID
        with the history Dataframe.
        '''
        video_ids = list(self.df_video_history["VideoID"])
        df_video_details = self.get_video_details(video_ids)
        df_video_details['Duration'] = df_video_details['Duration'].apply(FetchVideoDetails.fetch_duration_sec)
        
        # df_video_details contains the necessary details with the VideoID
        # self.df_video_history contains the VideoID, URL and title.
        # The merging part is totally optional, because self.df_video_history doesn't 
        # contain any extra information but we do it anyway.
        df_complete_history_details = pd.merge(
            self.df_video_history, df_video_details, on="VideoID"
        )
        # Text and Title columns both contain the same thing, so we can drop Text
        df_complete_history_details.drop(columns=["Text"], inplace=True)
        
        return df_complete_history_details

###############################################################################
