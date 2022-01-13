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
    
    def __init__(self, df_music, ignore_words=None):
        self.df_music = df_music
        self.ignore_words = ignore_words
        if self.ignore_words is None:
            self.ignore_words = [
                'facebook', 'twitter', 'instagram', 'amzn', 'tiktok', 'https', 'bit', 'ly', 'smarturl', 'new', 'generated', 'sms', 'im', 'sax', 'tik', 'tok'
                ]
        
    @staticmethod
    def remove_punct(wstr):
        nwstr = ''
        for char in wstr:
            if (char not in string.punctuation) and (char not in ('|', '(', ')', '-', ':', '[', ']')):
                nwstr += char
            else:
                nwstr += ' '
        return nwstr
    
    def get_words_string(self, create_text_file=True):
        
        if os.path.isfile('AllWordsMusicDatabase.txt'):
            with open('AllWordsMusicDatabase.txt', 'r', encoding='utf-8') as file:
                words_string_clean = file.read()

        else:
            all_titles = list(self.df_music['Title'])
            all_titles_str = ' '.join(all_titles)
            
            all_tags = list(self.df_music['Tags'].str.strip('[]').str.split(','))
            all_tags = [tag for tag_list in all_tags for tag in tag_list]
            all_tags_str = ' '.join(all_tags)
            all_tags_str = all_tags_str.replace("'", '')
            
            all_desc = list(self.df_music['Description'].str.strip('[]').str.split(','))
            all_desc = [desc for desc_list in all_desc for desc in desc_list]
            all_desc_str = ' '.join(all_desc)
            all_desc_str = all_desc_str.replace("'", '')
            all_desc_str = all_desc_str.replace("#", '')
            
            words_string = all_titles_str + ' ' + all_tags_str #+ ' ' + all_desc_str
            words_string_clean = CreateWordCloud.remove_punct(words_string)
            words_string_clean = ' '.join([
                words.lower() for words in words_string_clean.split() if words.lower() not in self.ignore_words
                ])
            
            if create_text_file:
                with open('AllWordsMusicDatabase.txt', 'w', encoding='utf-8') as file:
                    file.write(words_string_clean)
        
        return words_string_clean
        
    def generateWC(self, part=999):
        words_clean = self.get_words_string()
        plt.figure(figsize=(12, 9))
        wc = WordCloud(
            width=600,
            height=700,
            margin=0,
            mask=None,
            scale=1,
            max_words=200,
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
            min_word_length=3
        )
        wc.generate(words_clean)
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(f'photos/WordCloud_{part}.png')
        plt.show()
        
    def randomWcs(self):
        words_clean = self.get_words_string()
        
        words_count = Counter(words_clean.split()).most_common(350)
        words_clean_ord = ''
        for word in words_count:
            words_clean_ord = (word[0]+' ')*int(word[1]) + words_clean_ord
    
        wc_count = 10
        for part in range(1, wc_count):
            plt.figure(figsize=(12, 9))
            wc = WordCloud(
                width=600,
                height=700,
                margin=0,
                mask=None,
                scale=1,
                max_words=250,
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
            least_to_most_freq_words = words_clean_ord[:(part*len(words_clean_ord)//10) + 1].split()
            random.shuffle(least_to_most_freq_words)
            least_to_most_freq_words_random = ' '.join(least_to_most_freq_words)
            wc.generate(least_to_most_freq_words_random)
            plt.imshow(wc, interpolation='bilinear')
            plt.axis('off')
            plt.savefig(f'photos/WordCloud_{part}.png')
            
        self.generateWC(part+1)
            
    def animateWC(self):
        self.randomWcs()
        images = list(glob.glob('photos/*.png'))
        list.sort(images, key=lambda x: int(x.split('\\')[1].split('.png')[0].split('_')[-1]))
        image_list = []
        for image_name in images:
            image_list.append(imageio.imread(image_name))
            
        imageio.mimwrite('FinalWordCloud_Anim.gif', image_list, loop=2, fps=120, duration=0.35)

############################

base_path = os.path.dirname(__file__)
db_path = os.path.join(base_path, '../2. song_database/FinalMUSICDatabase.csv')
df_music = pd.read_csv(db_path)
words_string = CreateWordCloud(df_music).animateWC()

###############################################################################
