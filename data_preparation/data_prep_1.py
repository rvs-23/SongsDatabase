'''
This is the first script of the project which does the follwing:
    - removes the head tag contents from the html file.
    - creates a new cleaned file without head.
    - parses all the links from the file subject to the condition that they are watched video links.
    - creates a csv file of the links.
'''

import os
import re
import pandas as pd
from bs4 import BeautifulSoup

def removeHeadtag(text, tag='head'):
    '''
    Function to remove a certain tag from the HTML file
    param text -> HTML file
    param tag -> tag that needs to be removed
    '''
    return text[:text.find("<"+tag+">")] + text[text.find("</"+tag+">") + len(tag)+3:]

base_path = os.getcwd()

# File path
in_path = os.path.join(base_path, '_private_data/watch-history.html')

# File path to store the cleaned HTML
out_path = os.path.join(base_path, '_private_data/watch-history-clean.html')

# Opening and removing the head tag.
# Important to set the encoding type.
print("Opening the HTML file containing history.")
with open(in_path, 'r', encoding='utf-8') as file:
    contents = str(file.read())
    print("Removing the head tag.")
    watch_history_clean = removeHeadtag(contents)

print("Storing the cleaned file to a safe space.")
with open(out_path, 'w', encoding='utf-8') as file:
    file.write(watch_history_clean)

# Opening the cleaned html file to parse the watched URLS
print("Opening the cleaned html file to parse out the URL's.")
with open(out_path, 'r', encoding='utf-8') as file:
    html_data = file.read()

print("Creating soup object.")
soup = BeautifulSoup(html_data, "html.parser")
watched_urls = []

print("Extracting URL's")
# The watched urls all follow the same pattern. Extracting the URL's
for link in soup.findAll('a', attrs={'href': re.compile("^https://www.youtube.com/w")}):
    watched_urls.append(link.get('href'))

print(f"{len(watched_urls)} URL's were extracted.")
print("Converting to csv...")
s = pd.Series(watched_urls)

csv_path = os.path.join(base_path, '_private_data/Watched_Videos/WatchedURLs.csv')
s.to_csv(csv_path, encoding='utf-8')
print("Done.")

#############################################

# Opening the HTML file containing history.
# Removing the head tag.
# Storing the cleaned file to a safe space.
# Opening the cleaned html file to parse out the URL's.
# Creating soup object.
# Extracting URL's
# 30550 URL's were extracted.
