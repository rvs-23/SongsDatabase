r'''
This module does the following:
    - Creates a text file of all the words used in the title, tags and description.
    - Creates 10 wordcloud images from the text file and combines them to form a GIF.
'''

import os
import glob
import string
import random
import imageio
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud, STOPWORDS

class CreateWordCloud:
    '''
    Class to create the wordcloud animation.
    '''
    
    def __init__(self, df_music, ignore_words=None):
        '''
        param df_music -> DataFrame of the final music database
        param ignore_words -> Words that we choose to ignore from our wordclouds.
        '''
        self.df_music = df_music
        self.ignore_words = ignore_words
        if self.ignore_words is None:
            self.ignore_words = [
                'facebook',
                'twitter',
                'instagram',
                'amzn',
                'tiktok',
                'https',
                'bit',
                'ly',
                'smarturl',
                'new',
                'generated',
                'sms',
                'im',
                'sax',
                'tik',
                'tok',
                'unknown',
                'provided',
                'want',
                'associated',
                'apple',
                'engineer',
                'make',
                'produced'
                ]
    

    @staticmethod
    def remove_punct(wstr):
        '''
        param wstr -> string containing all the texts that we extracted from the
        music databse.
        
        Function removes punctuation and some special characters and replaces them
        with a blank space.
        
        returns updated string with no punctuations and some special characters.
        '''
        nwstr = ''
        for char in wstr:
            if (char not in string.punctuation) and (char not in ('|', '(', ')', '-', ':', '[', ']')):
                nwstr += char
            else:
                nwstr += ' '
        return nwstr
    
    
    def get_words_string(self, create_text_file=True):
        '''
        param create_text_file -> Set to True(default), if we want to save the words
        we will be using in a text file.
        
        Combines the Title, Tags and description to create a text file of all 
        the words present in our database.
        '''
        
        # Check if the file already exists. If not, extract words 
        if os.path.isfile('AllWordsMusicDatabase.txt'):
            with open('AllWordsMusicDatabase.txt', 'r', encoding='utf-8') as file:
                words_string_clean = file.read()
        else:
            
            # Creating a continuous string of all the Titles.
            all_titles = list(self.df_music['Title'])
            all_titles_str = ' '.join(all_titles)
            
            # Since tags are a list of strings, we perform the following sequence
            # to create a continuous string of all the Tags used.
            all_tags = list(self.df_music['Tags'].str.strip('[]').str.split(','))
            all_tags = [tag for tag_list in all_tags for tag in tag_list]
            all_tags_str = ' '.join(all_tags)
            all_tags_str = all_tags_str.replace("'", '')
            
            # We perform a similar operation as above for the description.
            all_desc = list(self.df_music['Description'].str.strip('[]').str.split(','))
            all_desc = [desc for desc_list in all_desc for desc in desc_list]
            all_desc_str = ' '.join(all_desc)
            all_desc_str = all_desc_str.replace("'", '')
            all_desc_str = all_desc_str.replace("#", '')
            
            # Join the titles, tags and description to form one single string and
            # remove unnecessary punctuation.
            words_string = all_titles_str + ' ' + all_tags_str + ' ' + all_desc_str
            words_string_clean = CreateWordCloud.remove_punct(words_string)
            words_string_clean = ' '.join([
                words.lower() for words in words_string_clean.split() if words.lower() not in self.ignore_words
                ])
            
            if create_text_file:
                with open('AllWordsMusicDatabase.txt', 'w', encoding='utf-8') as file:
                    file.write(words_string_clean)
        
        return words_string_clean
        
    def generateWC(self, part=999):
        '''
        param part -> Used to specify the name of the Final WordCloud image.
        
        Function generates a random cloud using all the words stored from
        title, tag and description.
        '''
        words_clean = self.get_words_string()
        fig = plt.figure(figsize=(9,9))
        fig.patch.set_facecolor('white')
        wc = WordCloud(
            width=1100,
            height=1300,
            margin=0,
            mask=None,
            max_words=190,
            min_font_size=5,
            stopwords=STOPWORDS,
            random_state=23,
            background_color='white',
            max_font_size=None,
            font_step=1,
            mode='RGB',
            collocations=True,
            colormap='ocean',
            contour_width=0,
            contour_color='black',
            min_word_length=4
        )
        wc.generate(words_clean)
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(f'photos/WordCloud_{part}.png')
        
        
    def randomWcs(self):
        '''
        To build the animation, we have adopted the following strategy:
            - We build 10 random wordclouds using words in such a way,
            that the least frequent mords appear first, and so on.
            - We, them combine the images to form a gif.
            
        This function generates 10 random wordclouds using our text file.
        '''
        words_clean = self.get_words_string()
        self.generateWC(part=0)
        
        # Find the top 350 words from out text file.
        # Create a new string which has words listed in increasing
        # order of their frequency.
        # This is necessary so that we can show how new words are added
        # to our word cloud animation.
        words_count = Counter(words_clean.split()).most_common(350)
        words_clean_ord = ''
        for word in words_count:
            words_clean_ord = (word[0]+' ')*int(word[1]) + words_clean_ord
    
        wc_count = 5
        for part in range(1, wc_count):
            # plt.figure(figsize=(9, 9))
            
            fig = plt.figure(figsize=(9,9))
            fig.patch.set_facecolor('white')
            wc = WordCloud(
                width=1100,
                height=1300,
                margin=0,
                mask=None,
                scale=1,
                max_words=200,
                min_font_size=5,
                stopwords=STOPWORDS,
                random_state=15,
                background_color='white',
                max_font_size=None,
                font_step=1,
                mode='RGB',
                collocations=True,
                colormap='ocean',
                contour_width=0,
                contour_color='black',
                min_word_length=3
            )
            # We divide the whole text file into 10 parts, and for each iteration 
            # choose a tenth of the file to add to our wordcloud.
            # The tenth is randomly shuffled so that the wordcloud looks 
            # more realistic.
            least_to_most_freq_words = words_clean_ord[:(part*len(words_clean_ord)//10) + 1].split()
            random.shuffle(least_to_most_freq_words)
            least_to_most_freq_words_random = ' '.join(least_to_most_freq_words)
            wc.generate(least_to_most_freq_words_random)
            plt.imshow(wc, interpolation='bilinear')
            plt.axis('off')
            plt.savefig(f'photos/WordCloud_{part}.png')
            
        # Adding our final animation with the whole picture.
        self.generateWC(part+1)
            
    def animateWC(self):
        '''
        Function that completes the animation.
        Saves the final gif into the same directory as the file.
        '''
        self.randomWcs()
        
        # Choosing all the wordcloud images.
        images = list(glob.glob('photos/*.png'))
        # Sorting according to the numbers added to the names, so that the wordcloud
        # appears in order.
        list.sort(images, key=lambda x: int(x.split('\\')[1].split('.png')[0].split('_')[-1]))
        image_list = []
        for image_name in images:
            image_list.append(imageio.imread(image_name))
        
        # Use the following if there are many images:
        # with imageio.get_writer('test.gif', mode='I') as writer:
        #     for filename in images:
        #         image = imageio.imread(filename)
        #         writer.append_data(image)
        imageio.mimwrite('FinalWordCloud_Anim_medium.gif', image_list, loop=2, fps=120, duration=0.3)

############################

base_path = os.path.dirname(__file__)
db_path = os.path.join(base_path, '../2. song_database/FinalMUSICDatabase.csv')
df_music = pd.read_csv(db_path)
words_string = CreateWordCloud(df_music).animateWC()

###############################################################################
