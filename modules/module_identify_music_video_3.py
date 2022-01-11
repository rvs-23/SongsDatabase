r'''
This is the third module of the project that accepts the dataframe of watch
history(containing video id, title, tags, categoryID, description) and does the
following:
    - Youtube identifies a music video by assigning a video Category 10. Although,
    this may not be 100% accurate.
    Source: https://stackoverflow.com/questions/31981358/youtube-api-search-only-music-videos
    
    - We use tags to add an additional layer of filter on the videos.
'''

import os
import re
import pickle
import pandas as pd

pd.options.mode.chained_assignment = None

class IdentifyMusicVideo:
    '''
    Class that attempts to identify a music video using the title, categoryID,
    tags and Description.
    '''
    base_path = os.path.dirname(__file__)
    
    def __init__(self, df_history_details):
        '''
        param df_history_details -> Dataframe containing watched VideoID, Title,
        CategoryID, Description and Tags.
        '''
        self.df_history_details = df_history_details
        self.cat_file = os.path.join(self.base_path, '../experiments/music_identify_data/top_categories.pkl')
        self.tags_file = os.path.join(self.base_path, '../experiments/music_identify_data/top_tags.pkl')
        self.desc_words_file = os.path.join(self.base_path, '../experiments/music_identify_data/top_desc_words.pkl')
        
        
    def get_cat_tag_desc(self):
        with open(self.cat_file, 'rb') as file:
            tc = pickle.load(file)
            # To obtain the list of top categories
            tc = list(tc.index)
            
        with open(self.tags_file, 'rb') as file:
            tt = pickle.load(file)
            # To obtain the list of top tags
            tt = [tag_value[0] for tag_value in tt]
            
        with open(self.desc_words_file, 'rb') as file:
            tdw = pickle.load(file)
            # To obtain the list of top description words
            tdw = [desc_word_value[0] for desc_word_value in tdw]
            
        return tc, tt, tdw
    
    def filter_by_category(self, category_ids):
        '''
        '''
        category_ids = list(map(int, category_ids))
        self.df_history_details['CategoryCheck'] = self.df_history_details['CategoryId'].apply(
            lambda x: 1 if x in category_ids else 0
            )
    
    def filter_by_tags(self, tags):
        
        self.df_history_details['TagExists'] = self.df_history_details['Tags'].apply(
            lambda x: x if pd.notna(x) else ['empty_tag']
            )
        self.df_history_details['TagsCheck'] = self.df_history_details['TagExists'].apply(
            lambda x: 1 if [tag for tag in x if tag in tags] else 0
            )
    
    def filter_by_description(self, desc_words):
        
        self.df_history_details['DescExists'] = self.df_history_details['Description'].apply(
            lambda x: x if pd.notna(x) else 'empty_description'
            )
        self.df_history_details['DescriptionCheck'] = self.df_history_details['DescExists'].apply(
            lambda x: 1 if [common_desc_words for common_desc_words in desc_words if common_desc_words in x] else 0
            )
    
    @staticmethod
    def removeShortsDesc(desc):
        pattern = r'#?short*'
        match = re.search(pattern, desc, re.IGNORECASE)
        if match is None:
            # not a short
            return 0
        else:
            return 1
    
    def filter_music_video(self):
        
        top_ids, top_tags, top_desc_words = self.get_cat_tag_desc()
        self.filter_by_category(top_ids)
        self.filter_by_tags(top_tags)
        self.filter_by_description(top_desc_words)
        
        df_music = self.df_history_details[~(
            (self.df_history_details['CategoryCheck'] == 0)
            & (self.df_history_details['TagsCheck'] == 0)
            & (self.df_history_details['DescriptionCheck'] == 0)
            )]
        
        
        # Filtering out shorts videos
        df_music['Shorts_by_Desc'] = df_music['DescExists'].apply(IdentifyMusicVideo.removeShortsDesc)
        
        df_music['TagExists'] = df_music['TagExists'].apply(lambda x: ' '.join(x))
        df_music['Shorts_by_Tags'] = df_music['TagExists'].apply(IdentifyMusicVideo.removeShortsDesc)
        
        df_filtered_music = df_music.loc[~((df_music['Shorts_by_Tags']==1) | (df_music['Shorts_by_Desc']==1))]
        df_filtered_music.reset_index(inplace=True, drop=True)
        
        return df_filtered_music[['Video_ID',             
                                    'Title',
                                    'CategoryId',
                                    'Description',
                                    'Tags',
                                    'CategoryCheck',
                                    'TagsCheck',
                                    'DescriptionCheck'
                                    ]] 
            
###############################################################################