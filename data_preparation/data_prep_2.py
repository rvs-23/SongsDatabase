r'''

This script does the following:
    - for a given watched YouTube video link, it fetches all the relevant information
    - The relevant information includes: 
    - Creates a dictionary of information and adds it 
'''



####################################################################

# from googleapiclient.discovery import build


# api_key = 'AIzaSyCw2MwX6oGxgF-myyiYjzEqRv0Ze126sss'

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