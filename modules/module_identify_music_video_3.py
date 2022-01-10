r'''
This is the third module of the project that accepts the dataframe of watch
history(containing video id, title, tags, categoryID, description) and does the
following:
    - Youtube identifies a music video by assigning a video Category 10. Although,
    this may not be 100% accurate.
    Source: https://stackoverflow.com/questions/31981358/youtube-api-search-only-music-videos
    
    - We use tags to add an additional layer of filter on the videos.
'''

class IdentifyMusicVideo:
    '''
    Class that attempts to identify a music video using the title, categoryID,
    tags and Description.
    '''
    
    def __init__(self, df_history_details):
        '''
        param df_history_details -> Dataframe containing watched VideoID, Title,
        CategoryID, Description and Tags.
        '''
        self.df_history_details = df_history_details 
        
    @staticmethod
    def filter_by_category(df, category_id=10):
        '''
        param df -> dataframe involved
        param category_id -> The category that we want to filter
        
        returns a filtered dataframe with the mentioned category_id
        '''
        return df.loc[df['CategoryID']==category_id]
    
    @staticmethod
    def filter_by_tags(df):
        pass
    
    def filter_music_video(self):
        df_filter_category = IdentifyMusicVideo.filter_by_category(self.df_history_details, 10)
        df_filter_category.reset_index(inplace=True, drop=True)
        df_filter_tags = IdentifyMusicVideo.filter_by_tags(self.df_history_details)
        df_filter_tags.reset_index(inplace=True, drop=True)
        
###############################################################################