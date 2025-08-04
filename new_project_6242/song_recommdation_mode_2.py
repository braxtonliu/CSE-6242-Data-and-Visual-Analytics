import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import pickle
import pandas as pd

# Load the CSV file
df = pd.read_csv('data/Music_Info.csv')

# Select only the required columns
selected_columns = ['track_id', 'danceability', 'energy', 'acousticness', 'instrumentalness', 'speechiness', 'valence', 'tempo']
df_selected = df[selected_columns]

selected_columns2 = ['track_id', 'name', 'artist']
df_selected2 = df[selected_columns2]

# Save the filtered DataFrame to a new CSV file
# df_selected.to_csv('data/Filtered_Music_Info.csv', index=False)
# df_selected2.to_csv('MusicLookup.csv', index=False)
#
# df = pd.read_csv('Filtered Music Info.csv')
features = ['danceability', 'energy', 'acousticness', 'instrumentalness', 'speechiness', 'valence', 'tempo']
X = df_selected[features].values

# Step 2: Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
knn = NearestNeighbors(n_neighbors=5, metric='euclidean')
knn.fit(X_scaled)
NearestNeighbors(metric='euclidean')


pickle.dump(knn, open('models/model_2.pkl','wb'))

# Function to get song names and artists for a list of track IDs
def get_song_info(track_ids):
    df2 = pd.read_csv('MusicLookup.csv')
    song_info = []
    for track_id in track_ids:
        song = df2.loc[df['track_id'] == track_id, ['name', 'artist']]
        if not song.empty:
            # Assuming each track_id is unique and only gets one row in the DataFrame
            name, artist = song.iloc[0]
            song_info.append((name, artist))
    return song_info