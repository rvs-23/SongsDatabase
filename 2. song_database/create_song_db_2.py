import pandas as pd
import os

base_path = os.path.dirname(__file__)

df_init_db = pd.read_csv(os.path.join(base_path, 'songs_heard/InitialMusicDatabase.csv'))

def is_music(cid, cc, tc, dc):
    '''
    Function to categorize a video into a music video.
    
    Returns Y, N or Maybe
    
    Working:
        - YouTube identifies music video as 10. Therefore, classify a video as 
        a music vidoe if CategoryID -> 10 or all three checks = 1
        - Otherwise:
            -> If all three checks = 0, video is definitely not music
            -> In all other cases, the video may or may not be music.
    '''
    if int(cid)==10 or cc+tc+dc==3:
        return 'Y'
    else:
        if cc+tc+dc==0:
            return 'N'
        
        return 'Maybe'

#########################################

print(f"Categorizing {len(df_init_db)} videos into Music, Not Music or Maybe Music...")
df_init_db['Is_Music'] = df_init_db[['CategoryID', 'CategoryCheck', 'TagsCheck', 'DescriptionCheck']].apply(
    lambda x: is_music(*x), axis=1
    )

music_videos_db = df_init_db.loc[df_init_db['Is_Music']=='Y']
print(f"{len(music_videos_db)} videos are categorized as music...")
print("Storing as csv...")
music_videos_db.to_csv(
    os.path.join(base_path, 'songs_heard/MusicDB-1.csv'), index=False, encoding='utf-8'
    )

manual_check_db = df_init_db.loc[df_init_db['Is_Music']=='Maybe']
print(f"{len(manual_check_db)} videos must be manually checked if you want a thorough list :(")
print("Creating an excel file of videos to be manually checked...")
manual_check_db['Is_Music_Manual'] = pd.Series(['N']*len(manual_check_db), dtype='object')
manual_check_db.to_excel(
    os.path.join(base_path, 'songs_heard/ManuallyCheckMusic.xlsx'), sheet_name='ManualCheck', index=False, encoding='utf-8'
    )
print("Done...")
print("Checking if the manual file is already sorted...")

if os.path.isfile(os.path.join(base_path, 'songs_heard/ManuallyCHECKEDMusic.xlsx')):
    print("Opening the Checked file to create a final database...")
    manually_checked_db = pd.read_excel(os.path.join(base_path, 'songs_heard/ManuallyCHECKEDMusic.xlsx'))
    music_video_db_manual = manually_checked_db.loc[manually_checked_db['Is_Music_Manual']=='Y']
    final_music_db = pd.concat([music_video_db_manual, music_videos_db], ignore_index=True)
    final_music_db.to_csv('FinalMusicDATABASE.csv', index=False, encoding='utf-8')
    print("Database created... :D")
else:
    print("You need to create a file with manual checks...")

###############################################################################

# Categorizing 1664 videos into Music, Not Music or Maybe Music...
# 456 videos are categorized as music...
# Storing as csv...
# 1208 videos must be manually checked if you want a thorough list :(
# Creating an excel file of videos to be manually checked...
# Done...
# Checking if the manual file is already sorted...
# Opening the Checked file to create a final database...
# Database created... :D
