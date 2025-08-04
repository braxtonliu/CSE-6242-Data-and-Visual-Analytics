from flask import Flask, request,render_template, request, json, jsonify, g
import csv
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)


model_1 = pickle.load( open('models/model_1.pkl','rb'))
model_2 = pickle.load( open('models/model_2.pkl','rb'))
user_df = pd.read_csv('data/User_Listening_History.csv', usecols=['track_id', 'user_id', 'playcount'])
listen_songs = pd.read_csv(r'data/Music_Info.csv')

like_songs = {}
def popular_song_genre(genres):
    # genres is a list
    genres = [x.lower() for x in genres]
    popular_songs = pd.read_csv(r'data/popular_songs.csv')
    popular_songs['genre'] = popular_songs['genre'].apply(lambda x:x.lower())
    return popular_songs[popular_songs['genre'].isin(genres)]['track_id'].tolist()

@app.route("/")
def homepage():
    return render_template('homepage.html')


@app.route("/recom-10-songs-new-users", methods=['POST'])
def song_recommendation_genr():
    request_data =  request.json
    print(request_data)
    genr_song_ids = popular_song_genre(request_data['category'])
    songs = listen_songs[listen_songs['track_id'].isin(genr_song_ids)]
    data = recommend_songs(model_2, songs)
    return json.dumps({'data':data})


@app.route("/recom-10-songs", methods=['POST'])
def song_recommendation_list():
    ## use default 10 songs
    request_data = request.json
    user_id = request_data['id']
    print(user_id)
    song_ids = pd.unique(user_df[user_df['user_id'] == user_id]['track_id']).tolist()
    print(song_ids)
    if user_id in like_songs:
        song_ids = song_ids + like_songs[user_id]
    top_recommendations = get_recommendations(model_1, [], song_ids)
    songs = listen_songs[listen_songs['track_id'].isin(top_recommendations)]
    filter_songs = songs[['name','artist','spotify_preview_url','track_id']]
    filter_songs = filter_songs.reset_index()
    data = []
    for index, row in filter_songs.iterrows():
        data.append({'name': row['name'], 'artist': row['artist'], 'spotify_preview_url': row['spotify_preview_url']})

    if len(data) == 0:
        select_songs = listen_songs.sample(n=20)
        select_songs = select_songs[['name','artist','spotify_preview_url','track_id']]
        for index, row in select_songs.iterrows():
            data.append({'name': row['name'], 'artist': row['artist'], 'spotify_preview_url': row['spotify_preview_url']})

    return json.dumps({'data': data})

@app.route("/song-like", methods=['POST'])
def song_like():
    request_data = request.json
    user_name = request_data['name']
    song_id = request_data['song']
    if user_name not in like_songs:
        like_songs[user_name] = [song_id]
    else:
        like_songs[user_name].append(song_id)

    return json.dumps({'status': 'success'})
def get_recommendations(model, song_list, song_ids, top_n=20):
    """
    Generate recommendations for a list of songs without retraining the model.
    """
    # Create a placeholder pseudo user ID since Surprise requires it, but it won't affect the outcome.
    pseudo_user_id = '0'

    # Filter out the given songs from the list of all song IDs.
    songs_to_rate = [song for song in song_ids if song not in song_list]

    # Predict ratings for all other songs.
    predictions = [model.predict(pseudo_user_id, iid=song) for song in songs_to_rate]

    # Sort the predictions by the estimated rating in descending order.
    predictions.sort(key=lambda x: x.est, reverse=True)

    # Extract the song IDs for the top N recommendations.
    top_recommendations = [pred.iid for pred in predictions[:top_n]]

    return top_recommendations

def recommend_songs(knn,genr_songs, n_recommendations=20):
    features = ['danceability', 'energy', 'acousticness', 'instrumentalness', 'speechiness', 'valence', 'tempo']
    X = genr_songs[features].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    avg_vector = X_scaled.mean(axis=0).reshape(1, -1)
    distances, indices = knn.kneighbors(avg_vector, n_neighbors=n_recommendations + genr_songs.shape[0])

    recommendations = []
    for i in indices[0]:
        track_id = listen_songs.iloc[i]['track_id']
        if track_id not in genr_songs['track_id'].tolist():  # Exclude input songs from recommendations
            recommendations.append(track_id)
            if len(recommendations) == n_recommendations:  # Only return n recommendations
                break
    songs = listen_songs[listen_songs['track_id'].isin(recommendations)]
    filter_songs = songs[['name','artist','spotify_preview_url','track_id']]
    filter_songs = filter_songs.reset_index()
    data = []
    for index, row in filter_songs.iterrows():
        data.append({'name': row['name'], 'artist': row['artist'], 'spotify_preview_url': row['spotify_preview_url']})
    return data





if __name__ == "__main__":

    app.run()