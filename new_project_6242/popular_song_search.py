import pandas as pd
## check if the path is right
music_genre = pd.read_csv(r'data/Music_Info.csv')[['track_id','genre']]
history = pd.read_csv(r'data/User_Listening_History.csv')[['track_id','playcount']]

total_playcount = history.groupby(by='track_id').sum().reset_index()
## merge and delete rows with missing genre
total_playcount_genre = total_playcount.merge(music_genre, how = 'left', on='track_id').dropna().reset_index(drop=True)

def top_10(group):
    return group.sort_values(by='playcount', ascending=False).head(10)

## store the popular songs of every genre for later search
## check if path need to modify
popular_songs = total_playcount_genre.groupby('genre').apply(top_10).reset_index(drop=True)
popular_songs.to_csv('data/popular_songs.csv')

## function to search songs base on provide genres, check if the path need to modify
