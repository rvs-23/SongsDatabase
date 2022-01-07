r'''
This script parses the Video-Id from a given YouTube link and creates a csv file.
'''

import os
import urllib
import pandas as pd

base_path = os.path.dirname(__file__)
file_path_in = os.path.join(base_path, '../_private_data/Watched_Videos/WatchedURLs.csv')

def video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urllib.parse.urlparse(value)

    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = urllib.parse.parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

# Open the csv, name the columns appropriately
url_csv = pd.read_csv(file_path_in)
url_csv.columns = ['Sl. no', 'Link']
# Extract the Video ID from the link
url_csv['Video-ID'] = url_csv['Link'].apply(lambda x: video_id(x))

# Define the output path and covert the file to a csv.
file_path_out = os.path.join(base_path, '../_private_data/Watched_Videos/WatchedURLs-ID.csv')
url_csv[['Link', 'Video-ID']].to_csv(file_path_out, index=False, encoding='utf-8')

##############################################################################
