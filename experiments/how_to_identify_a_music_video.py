r'''

Once we have obtained a list of videos alongwith all the necessary details, how
do we identify if a particular video is a MUSIC video?

Idea: we could use a combination of CategoryID and Video Tags.
Problem: How do we know which values to pick?

Solution:
    This script experiments with a playlist of ONLY MUSIC videos to figure out
    the most common Video Tags used and CategoryID assigned for music videos.

    Playlist used: https://www.youtube.com/watch?v=JGwWNGJdvx8&list=PLhsz9CILh357zA1yMT-K5T9ZTNEU6Fl6n

    This playlist contains around 5000 most played music videos on YouTube. We
    could use information from these videos to create a system that can best
    identify a music video.

'''

import os
import string
from collections import Counter
import pandas as pd
import pickle
from nltk.corpus import stopwords
from googleapiclient.discovery import build

# If you have never downloaded list of stopwords, uncomment the following lines:
# import nltk
# nltk.download('stopwords')

# Opening the API key.
base_path = os.path.dirname(__file__)
with open(os.path.join(base_path, '../_private_data/api_key.txt'), 'r', encoding='utf-8') as f:
    api_key = f.read()
    
# Creating a YouTube resource
yt = build('youtube', 'v3', developerKey=api_key)

# Variable to keep track of pages from the playlist.
nextPageToken = None

# List to store the video details from the playlist
all_video_details = []

playlist_id = 'PLhsz9CILh357zA1yMT-K5T9ZTNEU6Fl6n'
# What's the idea, here?
# We loop through each page of the playlist, fetch the video ID of all present
# videos, fetch the details of those videos and append that to a list. Repeat
# the process, until the playlist is exhausted.
while True:
    # YouTube resource to fetch playlist video IDs.
    pl_req = yt.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50,
        pageToken=nextPageToken
        )
    pl_response = pl_req.execute()

    # Fetching the video ID's of 50 (maximum allowed) videos.
    video_ids = []
    for item in pl_response['items']:
        video_ids.append(item['contentDetails'].get('videoId'))

    # YouTube resource to fetch details of the obtained 50 videos
    vid_req = yt.videos().list(
        part='snippet',
        id=','.join(video_ids)
        )
    vid_response = vid_req.execute()

    # Adding the necessary information to a dictionary and appending
    # to a list for all the playlist videos.
    for details, yt_id in zip(vid_response["items"], video_ids):
        snippet = details["snippet"]
        # Fetching the necessary details from the snippet key
        every_video_detail = dict(
            VideoID=yt_id,
            Title=snippet.get("title"),
            CategoryID=snippet.get("categoryId"),
            PublishDate=snippet.get("publishedAt"),
            ChannelTitle=snippet.get("channelTitle"),
            Description=snippet.get("description"),
            Tags=snippet.get("tags"),
        )
        all_video_details.append(every_video_detail)

    # Returns None if we have exhausted all pages. Break if it returns None.
    # not None returns True.
    nextPageToken = pl_response.get('nextPageToken')
    if not nextPageToken:
        break

df = pd.DataFrame(all_video_details)

######################################

# 1. Filtering CategoryID
# Filtering the top 5 CategoryIDs which YT identifies as music.
top_categories = df['CategoryID'].value_counts()[:3]
print(f"Fetched Top-3 video categories which account for {round(sum(top_categories)/len(df)*100, 2)} % music videos...")

# 2. Filtering Tags
# The tags column contains a list of tags associated with each video.
# Creating a single list of all the tags associated with the videos.
all_tags = [
    tag.lower() for tags in df['Tags'].tolist() if tags is not None for tag in tags
    ]
# Fetching the top 0.1% most common tags in music videos.
top_tags = Counter(all_tags).most_common(int(0.001*len(all_tags)))
print(f"Fetched {len(top_tags)} most common tags...")

# 3. Filtering Description
desc_words = ''.join(df['Description'].str.lower()).split()
# From these words, we need to remove the stop words.
stopwords_en = stopwords.words('english')
desc_words_filtered = [word for word in desc_words if word not in stopwords_en]
# Fetching the top 0.1% most common words.
desc_most_common = Counter(desc_words_filtered).most_common(int(0.001*len(desc_words_filtered)))
desc_most_common = [word for word in desc_most_common if word[0] not in string.punctuation]
print(f"Fetched {len(desc_most_common)} most common words...")

print("Dumping categories, tags and most common words into pickle...")
with open(os.path.join(base_path, 'music_identify_data/top_categories.pkl'), 'wb') as cats:
    pickle.dump(top_categories, cats)

with open(os.path.join(base_path, 'music_identify_data/top_tags.pkl'), 'wb') as tags:
    pickle.dump(top_tags, tags)

with open(os.path.join(base_path, 'music_identify_data/top_desc_words.pkl'), 'wb') as desc:
    pickle.dump(desc_most_common, desc)

print("Complete...")

#########################################

# Fetched Top-3 video categories which account for 98.65 % music videos...
# Fetched 81 most common tags...
# Fetched 492 most common words...
# Dumping categories, tags and most common words into pickle...
# Complete...

# print(top_categories)
# Out[20]: 
# 10    4089
# 24     165
# 22      49
# Name: CategoryID, dtype: int64

# print(top_tags)
# Out[21]: 
# [('pop', 870),
#  ('music', 597),
#  ('music video', 511),
#  ('official', 495),
#  ('vevo', 401),
#  ('video', 373),
#  ('hip hop', 352),
#  ('rap', 351),
#  ('lyrics', 330),
#  ('official video', 313),
#  ('records', 311),
#  ('album', 229),
#  ('single', 223),
#  ('dance', 218),
#  ('official music video', 214),
#  ('pop music', 213),
#  ('rock', 212),
#  ('the', 206),
#  ('remix', 180),
#  ('remastered music videos', 179),
#  ('#remastered', 176),
#  ('hd music videos', 176),
#  ('alternative', 166),
#  ('acoustic', 145),
#  ('cover', 135),
#  ('hip', 129),
#  ('hop', 126),
#  ('atlantic records', 124),
#  ('download', 120),
#  ('warner records', 109),
#  ('r&b', 106),
#  ('edm', 105),
#  ('live', 105),
#  ('audio', 102),
#  ('instrumental', 102),
#  ('karaoke', 100),
#  ('interscope', 96),
#  ('new', 94),
#  ('country', 92),
#  ('house', 90),
#  ('you', 89),
#  ('song', 87),
#  ('love', 86),
#  ('drake', 84),
#  ('vevo music', 77),
#  ('electronic', 76),
#  ('wmg', 75),
#  ('chris brown', 75),
#  ('trap', 74),
#  ('sony', 72),
#  ('ed sheeran', 70),
#  ('rihanna', 65),
#  ('eminem', 64),
#  ('nicki minaj', 64),
#  ('island', 64),
#  ('jam', 62),
#  ('new music', 62),
#  ('columbia', 61),
#  ('hq', 59),
#  ('universal', 57),
#  ('justin bieber', 56),
#  ('epic', 56),
#  ('warner music group (record label)', 56),
#  ('beyonce', 55),
#  ('dance music', 54),
#  ('def', 53),
#  ('official audio', 52),
#  ('indie', 51),
#  ('country music', 51),
#  ('english songs', 49),
#  ('songs', 49),
#  ('maroon 5', 49),
#  ('selena gomez', 49),
#  ('music (tv genre)', 49),
#  ('soundtrack', 49),
#  ('summer', 48),
#  ('marshmello', 48),
#  ('money', 48),
#  ('tiktok', 48),
#  ('new years eve', 47),
#  ('sheeran', 46)]
