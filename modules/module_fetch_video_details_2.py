"""
This is the second module of the project which performs the following tasks:
    - For a given video ID, it fetched the title, categoryID, publishDate, Channel name,
    Description and tags.
    - Creates a dataframe containing the URL, Video_ID and the above details.
    - Note: Youtube API allows for only 50 calls in one shot.
  
"""
import pandas as pd

class FetchVideoDetails:
    """
    Class to fetch the necessary infromation of all the video ids and create
    a dataframe of the complete information.
    """

    def __init__(self, YT_build, df_video_history):
        """
        param YT_build -> API build
        param df_video_history -> dataframe containing the watched video history
        """
        self.YT_build = YT_build
        self.df_video_history = df_video_history

    def get_video_details(self, video_ids):
        """
        param video_ids -> All the video_ids present in the watched history.

        returns a dataframe of all the necessary video details
        """

        all_video_details = []

        # Breaking into batches of 50
        for limit in range(0, len(video_ids), 50):
            # Slicing 50 video IDs
            fifty_videos = video_ids[limit : limit + 50]
            # The snippet parameter contains the information we are after
            request = self.YT_build.videos().list(
                part="snippet", id=",".join(fifty_videos)
            )
            response = request.execute()

            # Zip the video details and the ID together
            for details, yt_id in zip(response["items"], fifty_videos):
                snippet = details["snippet"]
                # Fetching the necessary details from the snippet key
                every_video_detail = dict(
                    Video_ID=yt_id,
                    Title=snippet.get("title"),
                    CategoryID=snippet.get("categoryId"),
                    PublishDate=snippet.get("publishedAt"),
                    ChannelTitle=snippet.get("channelTitle"),
                    Description=snippet.get("description"),
                    Tags=snippet.get("tags"),
                )

                # Adding every video one by one
                all_video_details.append(every_video_detail)

        return pd.DataFrame(all_video_details)

    def get_complete_details(self):
        video_ids = list(self.df_video_history["Video_ID"])
        # The function returns a Dataframe containing the necessary information
        # with the Video ID. Although, not necessary but for verification, we can
        # merger this with df_video_history on the Video_ID key which is same for both.
        df_video_details = self.get_video_details(video_ids)

        # Merging
        df_complete_history_details = pd.merge(
            self.df_video_history, df_video_details, on="Video_ID"
        )
        # Text and Title columns both contain the same thing, so we can drop one.
        df_complete_history_details.drop(columns=["Text"], inplace=True)
        
        return df_complete_history_details

###############################################################################
