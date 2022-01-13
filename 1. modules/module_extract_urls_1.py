"""
This is the first module of the project which performs the following tasks:
    1. Watch History File: We need the history file that can be downloaded from Google takeouts.
    We can download our history in either an HTML or a JSON file format.
        (a) For HTML, we do the following:
            - Remove the HEAD tag from the file.
            - Extract all the links present and the texts associated with the links.
            - Remove the links which are from myactivity.google
            - Remove any videos that have 'short' in their title.
            - For all the YouTube links, extract the VideoID.
        
        (b) For JSON, we do the following:
            - Extract all the links present and the texts associated with the links.
            - Remove any videos that have 'short' in their title.
            - For all the YouTube links, extract the VideoID.
            
    2. Create a dataframe of the links, text associated with the link(Title) and the VideoID.
"""

import urllib
import pandas as pd
from bs4 import BeautifulSoup

class ParseYtHistory:
    """
    Class to parse out the necessary information from the HTML/JSON history file.
    
    NOTE: HTML file takes a lot more time that of the JSON file equivalent.
    To parse out aound 30000 links, it took 45 mins in case of HTML whereas it took only
    1 min in case of JSON.
    """
    def __init__(self, history_file, json_file=True):
        """
        param history_file -> The HTML file containing our YouTube history(HTML/JSON).
        param json_file -> True if you are passing a JSON file, False if passing an HTML.
        """
        self.history_file = history_file
        self.json_file = json_file

    @staticmethod
    def removeHeadtag(text, tag="head"):
        """
        Function to remove a certain tag from the HTML file.
        param text -> HTML file
        param tag -> tag that needs to be removed

        returns the HTML file without the "tag"
        """
        return (
            text[: text.find("<" + tag + ">")] + text[text.find("</" + tag + ">") + len(tag) + 3 :]
        )

    @staticmethod
    def getVideoID(link):
        """
        Source:
            https://stackoverflow.com/questions/4356538/how-can-i-extract-video-id-from-youtubes-link-in-python
        
        Examples:
        - http://youtu.be/SA2iWivDJiE
        - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
        - http://www.youtube.com/embed/SA2iWivDJiE
        - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US

        returns video ID if pattern matches any of the above, None otherwise.
        """
        query = urllib.parse.urlparse(link)

        if query.hostname == "youtu.be":
            return query.path[1:]
        if query.hostname in ("www.youtube.com", "youtube.com"):
            if query.path == "/watch":
                p = urllib.parse.parse_qs(query.query)
                return p["v"][0]
            if query.path[:7] == "/embed/":
                return query.path.split("/")[2]
            if query.path[:3] == "/v/":
                return query.path.split("/")[2]
        # fail?
        return None
    
    @staticmethod
    def removeShorts(list_words):
        '''
        If the videos have #short, #shorts etc in their title, it's an indication
        that such videos are YT shorts and therefore not relevant to us.
        
        param list_words -> list of string obtained by splitting the title on "#"
        
        return True if 'short' is present in the title, else False.
        '''
        for word in list_words:
            if 'short' in word.lower():
                return True
        return False

    def cleanHistory(self):
        """
        Function to remove the head tag from the HTML file.
        """
        watch_history_clean = ParseYtHistory.removeHeadtag(self.history_file)
        return watch_history_clean

    def extractURLs_HTML(self):
        """
        Function to parse out all the links from the HTML file.

        returns a dictionary of the link and its associated text.
        """
        # Removing the HEAD tag
        watch_history_clean = self.cleanHistory()
        # Creating a soup object with HTML parser
        soup = BeautifulSoup(watch_history_clean, "html.parser")
        # Dictionary to store the URL's and the associated text
        watched_urls = {}

        # Extracting the URL's from the anchor tag.
        # If confident that the watched links follow 1 single format, we could also use
        # soup.findAll('a', attrs={'href': re.compile("^https://www.youtube.com/w")})
        for link in soup.findAll("a"):
            watched_urls[(link.get("href"))] = link.text

        return watched_urls

    def extractURLs_JSON(self):
        """
        Function to parse out all the links from the JSON file.

        returns a dictionary with key: link and value: list of associated text(Title) and watch time.
        """
        watched_urls = {}
        for video_detail in self.history_file:
            url = video_detail.get("titleUrl")
            watched_urls[url] = [video_detail.get("title"), video_detail.get("time")]

        return watched_urls
    
    def createLinksCSV(self):
        """
        returns a Dataframe of the Video URL, Text and the Video ID of a YT video.
        
        For an HTML file, it removes links from 'myactivity.google'
        """

        # Check if the user sent a JSON file or an HTML file
        if self.json_file:
            # Dictionary: key-LINK, value-[text, watchTime]
            watched_urls_dict = self.extractURLs_JSON()
            # Converting the dictionary into dataframe and removing any rows with None URLs or Text
            df_video_history = pd.DataFrame(watched_urls_dict.items(), columns=["URLs", "TextDate"])
            # Extracting the text and WatchDate from the list.
            df_video_history[["Text", "WatchDate"]] = pd.DataFrame(
                df_video_history["TextDate"].tolist(), index=df_video_history.index
                )
            # Drop the TextDate column which is no longer needed
            df_video_history.drop(columns=["TextDate"], inplace=True)
        else:
            # Dictionary: key-LINK, value-text
            watched_urls_dict = self.extractURLs_HTML()
            df_video_history = pd.DataFrame(watched_urls_dict.items(), columns=["URLs", "Text"])
            # Ignoring those URL's which contains 'google' in the link. Necessary for HTML files only.
            df_video_history = df_video_history[~(df_video_history["URLs"].str.contains("google"))]
        
        # Parsing the VideoID from the YouTube URL.
        df_video_history["VideoID"] = df_video_history["URLs"].apply(ParseYtHistory.getVideoID)

        # If the links don't conform to the example patterns mentioned in the getVideoID function,
        # the corresponding row value becomes None. We ignore such links.
        df_video_history.dropna(inplace=True)

        # Most short videos have #short or a similar pattern in the title.
        # We can filter such videos. We create a list of strings by splitting on "#"
        is_short = df_video_history["Text"].apply(
            lambda x: ParseYtHistory.removeShorts(x.split("#"))
            )
        # Filter videos that are not shortsa and reset their index.
        df_video_history = df_video_history[~(is_short)]
        df_video_history.reset_index(inplace=True, drop=True)

        return df_video_history

###############################################################################
