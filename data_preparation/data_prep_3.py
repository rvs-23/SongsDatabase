r'''

This script does the following:
    - For a given watched YouTube video link, extracts the video id.
    - For a given video id, it fetches all the relevant information which include:
        - description
        - 
    - Creates a dictionary of information and adds it to the file.

'''





####################################################################

# from googleapiclient.discovery import build


# api_key = os.environ.get('YT-API_key_file')

# youtube = build('youtube', 'v3', developerKey=api_key)

# req = youtube.channels().list(
#     part='statistics',
#     forUsername='schafer5'
#     )

# response = req.execute()

# print(response)

######################################################################

# import json
# import urllib

# #change to yours VideoID or change url inparams
# VideoID = "3tfyYbCzfKk" 

# params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % VideoID}
# url = "https://www.youtube.com/oembed"
# query_string = urllib.parse.urlencode(params)
# url = url + "?" + query_string
# print(query_string)
# print(url)
# with urllib.request.urlopen(url) as response:
#     response_text = response.read()
#     data = json.loads(response_text.decode())
#     print(data['title'])

##########################################################################    