"""
This is the first module of the project which performs the following tasks:
    1. Cleans the watched history HTML file by removing the HEAD tag.
    2. Extracts all the links and the texts associated with the link form
    the HTML file.
    3. For all the YouTube videos(non-shorts),parses the video ID.
    4. Returns a dataframe of the link, text and the video ID.
"""

import urllib
import pandas as pd
from bs4 import BeautifulSoup


class ParseYtHistory:
    """
    Class to parse out the necessary information from the history HTML/JSON file.
    NOTE: HTML file takes upto a lot more time that the JSON file equivalent.

    To parse out 30000 links, it took 45 mins in case of HTML whereas it took only
    1 min in case of JSON.
    """

    def __init__(self, history_file, json_file=True):
        """
        param history_file -> The HTML file containing our YouTube history.
        """
        self.history_file = history_file
        self.json_file = json_file

    @staticmethod
    def removeHeadtag(text, tag="head"):
        """
        Function to remove a certain tag from the HTML file
        param text -> HTML file
        param tag -> tag that needs to be removed

        returns the HTML file without the "tag"
        """
        return (
            text[: text.find("<" + tag + ">")]
            + text[text.find("</" + tag + ">") + len(tag) + 3 :]
        )

    @staticmethod
    def getVideoID(link):
        """
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

        returns a dictionary of the link and its associated text.
        """
        watched_urls = {}

        for video_detail in self.history_file:
            url = video_detail.get("titleUrl")
            watched_urls[url] = video_detail.get("title")

        return watched_urls

    def createLinksCSV(self):
        """
        returns a Dataframe of the Video URL, Text and the Video ID of a YT video.
        Function also removes any links that contain the word 'google' and also removes any video
        whose text has the words 'shorts'.
        """

        # Check if the user sent a JSON file or an HTML file
        if self.json_file:
            # Dictionary: key-LINK, value-text
            watched_urls_dict = self.extractURLs_JSON()
        else:
            # Dictionary: key-LINK, value-text
            watched_urls_dict = self.extractURLs_HTML()

        # Converting the dictionary into dataframe and removing any rows with None URLs or Text
        df_video_history = pd.DataFrame(
            watched_urls_dict.items(), columns=["URLs", "Text"]
        )
        df_video_history.dropna(inplace=True)

        # Ignoring those URL's which contains 'google' in the link. Necessary for HTML files only.
        df_video_history = df_video_history[
            ~(df_video_history["URLs"].str.contains("google"))
        ]

        # Parsing the Video-ID from the URL
        df_video_history["Video_ID"] = df_video_history["URLs"].apply(
            lambda x: ParseYtHistory.getVideoID(x)
        )

        # If the links don't conform to the example patterns shown in the getVideoID function,
        # it becomes None. We ignore such links.
        df_video_history.dropna(inplace=True)

        # Check if a video text has 'short' in it. If yes, most likely, it's a YouTube
        # short and can be ignored.
        is_short = df_video_history["Text"].str.lower().str.contains("short")
        df_video_history = df_video_history[~(is_short)]
        df_video_history.reset_index(inplace=True, drop=True)

        return df_video_history


###############################################################################
