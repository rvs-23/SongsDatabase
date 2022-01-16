# SongsDatabase


An attempt to build a way to create Database of all the songs I ever heard on youtube.

<a href= "https://rvs.medium.com/how-to-build-a-database-of-all-the-songs-you-have-ever-heard-using-python-b34dfd4f5f3d"> Medium article. </a> 


## 0. music_vid_identify

Contains a script called: how_to_identify_a_music_video.py which identifies the top categories, tags and description words of the most played music videos.


## 1. modules

Contains three modules:-
<li>
  <ol>module_extract_urls_1.py : Extracts all the videos from the history file.</ol>
  <ol>module_fetch_video_details_2.py: Fetches the details of all the videos extracted. Details include - Title, Description, Tags, Duration.</ol>
  <ol>module_identify_music_video_3.py: Implements a system of classifying a video as music or not music.</ol>
</li>



## 2. song_database

Contains two scripts:
<li>
  <ol>create_song_db_1.py : Uses the above modules in sequence to create an initial database of possible music videos.</ol>
  <ol>create_song_db_2.py : Filters the initial database into three categories - Y(definitely music), N(definitely not music), Maybe(requires manually check).</ol>
</li>

## 3. animation

Contains script that creates a word cloud animation.

<hr>
