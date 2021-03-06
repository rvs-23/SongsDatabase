r'''
This is the third module of the project that uses the dataframe of watch history
(containing VideoID, Title, Tags, categoryID, Description) and tries to figure out 
if a video is a music video:
    
    Layer 1: Using CategoryID:
        - As understood from our experiment, Youtube identifies a music video by assigning a video Category 10.
        Although, this may not be 100% accurate. Refer the following link:
            https://stackoverflow.com/questions/17698040/youtube-api-v3-where-can-i-find-a-list-of-each-videocategoryid
    
    Layer 2: Using Tags and Description:
        - This playlist contains about 5000 of the most played songs on YouTube.
            https://www.youtube.com/watch?v=JGwWNGJdvx8&list=PLhsz9CILh357zA1yMT-K5T9ZTNEU6Fl6n
        In our experiments script, we screened the most popular tags and most commonly used
        description words in a music video. We can use those to add another layer to our
        music video identification system.
'''

import os
import pickle
import pandas as pd
from nltk.corpus import stopwords

# SettingWithCopy Warning disable
pd.options.mode.chained_assignment = None

class IdentifyMusicVideo:
    '''
    Class that attempts to identify a music video using the categoryID,
    Tags and Description.
    '''
    
    base_path = os.path.dirname(__file__)
    
    def __init__(self, df_history_details):
        '''
        param df_history_details -> Dataframe containing watched VideoID, Title,
        CategoryID, Description and Tags.
        '''
        self.df_history_details = df_history_details
        self.cat_file = os.path.join(self.base_path, '../0. music_vid_identify/music_identify_data/top_categories.pkl')
        self.tags_file = os.path.join(self.base_path, '../0. music_vid_identify/music_identify_data/top_tags.pkl')
        self.desc_words_file = os.path.join(self.base_path, '../0. music_vid_identify/music_identify_data/top_desc_words.pkl')
        
    def get_cat_tag_desc(self):
        '''
        Function to open the pickle file containing the most popular CategoryID,
        Tags and Description words. 
        
        Returns a list of each.
        '''
        with open(self.cat_file, 'rb') as file:
            tc = pickle.load(file)
            # To obtain the list of top categories
            tc = list(map(int, tc.index))
            
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
        Filter the dataframe by the top 2 music categories.
        
        Function creates a column called CategoryCheck which is 1 if the category
        belongs the identified Top-2 from the experiments, 0 otherwise.
        '''
        category_ids = list(map(int, category_ids))
        
        self.df_history_details['CategoryCheck'] = self.df_history_details['CategoryID'].apply(
            lambda x: 1 if int(x) in category_ids else 0
            )
    
    def filter_by_tags(self, tags):
        '''
        Filter the dataframe by the 750 most popular tags used in the playlist.
        
        Function creates a column called TagsCheck which is 1 if the tag belongs
        to the top 750, 0 otherwise.
        '''
        # Replacing nan/None tags (if any) with an empty string
        self.df_history_details['Tags'].fillna(' ', inplace=True)
        
        # Setting TagsCheck=1, if tags belong to the top-750
        self.df_history_details['TagsCheck'] = self.df_history_details['Tags'].apply(
            lambda x: 1 if [common_tag for common_tag in x if common_tag in tags] else 0
            )
        
    def filter_by_description(self, desc_words):
        '''
        Filter the dataframe by the 250 most popular words used in description of
        music videos.
        
        Function creates a column called DescriptionCheck which is 1 if the Description
        contains words that belong to the top 500, 0 otherwise.
        '''
        stopwords_en = stopwords.words('english')
        
        # self.df_history_details['AllDescWords'] = self.df_history_details.apply(lambda x: desc_words, axis=1)
        # If Description is empty, add a blank string, else convert it to lower case.
        self.df_history_details['DescExists'] = self.df_history_details['Description'].apply(
            lambda x: x.lower() if pd.notna(x) else ' '
            )
        
        # Split the description into a list of words and remove the stopwords.
        self.df_history_details['Description'] = self.df_history_details['DescExists'].apply(
            lambda x: [word for word in x.split() if word not in stopwords_en]
            )
        # DescriptionCheck column = 1 if description has words that belong to top-250
        self.df_history_details['DescriptionCheck'] = self.df_history_details['Description'].apply(
            lambda x: 1 if [cw for cw in x if cw in desc_words] else 0
            )
        
    def filter_music_video(self):
        '''
        If a video doesn't satisfy any of the category, tags or description checks
        it's almost certainly not a Music Video.
        
        This function filters such videos and returns a dataframe only with necessary
        details which are: 
            'VideoID', 'Title', 'CategoryID', 'Description',
            'Tags', 'CategoryCheck', 'AllDescWordsTagsCheck',
            'DescriptionCheck'.
        '''

        # Removing YouTube shorts(videos with duration 60s or less)
        self.df_history_details = self.df_history_details.loc[self.df_history_details['Duration']>60]
        
        # Creating checks for tags, category and description words.
        top_ids, top_tags, top_desc_words = self.get_cat_tag_desc()
        self.filter_by_category(top_ids)
        self.filter_by_tags(top_tags)
        self.filter_by_description(top_desc_words)
        
        # Ignoring all videos that don't pass any of the checks.
        df_filtered_music = self.df_history_details[~(
            (self.df_history_details['CategoryCheck'] == 0)
            & (self.df_history_details['TagsCheck'] == 0)
            & (self.df_history_details['DescriptionCheck'] == 0)
            )]
        
        # Reseting the index and choosing a subset of necessary columns
        df_filtered_music.reset_index(drop=True, inplace=True)
        reqd_details = ['VideoID', 'Title', 'CategoryID', 'Description', 'Tags', 'CategoryCheck', 'TagsCheck', 'DescriptionCheck']
        return df_filtered_music[reqd_details] 

###############################################################################
