import os
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split

# load single json file
def load_df(json_path):
    cur_d = os.path.dirname(os.path.abspath(__file__))
    file_d = os.path.join(cur_d, '..', 'data', 'data_raw')
    
    # Code/spotify_million_playlist_dataset/data/mpd.slice.XXXX.json
    file_path = os.path.join(file_d, json_path)
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data['playlists'])
        os.remove(file_path)
        return df
    else:
        print("incorrect file path")
        return None

# process data
def process_data(n=10):
    folder_path = "code/data/data_raw/"
    file_names = os.listdir(folder_path)
    print(len(file_names))
    file_names = file_names[:n]

    for json_file in file_names:
        playlist_df = load_df(json_file)
        reformatted = []

        for index, row in playlist_df.iterrows():
            playlist_name = row['name']
            if row['num_followers'] > 0:
                for track in row['tracks']:
                    reformatted.append({'track': track['track_name'], 'artist': track['artist_name'], 'album': track['album_name'], 'playlist': playlist_name})

        track_df = pd.DataFrame(reformatted)

        cur_d = os.path.dirname(os.path.abspath(__file__))
        file_d = os.path.join(cur_d, '..', 'data', 'data_processed')
        file_path = os.path.join(file_d, json_file[:-5]+ ".csv")
        track_df.to_csv(file_path, index=False)

playlist_dict = {}
track_dict = {}
artist_dict = {}
album_dict = {}

playlist_count = 0;
track_count = 0;
artist_count = 0;
album_count = 0;

# process_data(10)

folder_path = "code/data/data_processed/"
file_names = os.listdir(folder_path)
file_names = list(filter(lambda x: x != '.DS_Store', file_names)) # bruh
file_names = file_names[:1]

# load dataset in single dataframe
df = pd.DataFrame()
for csv_file in file_names:
    cur_d = os.path.dirname(os.path.abspath(__file__))
    file_d = os.path.join(cur_d, '..', 'data', 'data_processed')
    file_path = os.path.join(file_d, csv_file)
    append_df = pd.read_csv(file_path)
    df = pd.concat([df, append_df], ignore_index=True)

for index, row in df.iterrows():
    track = row[0]
    if track not in track_dict:
        new_number = track_count + 1
        track_count = track_count + 1;
        track_dict[track] = new_number
        df.at[index, 'track'] = new_number
    else:
        df.at[index, 'track'] = track_dict[track]

    artist = row[1]
    if artist not in artist_dict:
        new_number = artist_count + 1
        artist_count = artist_count + 1;
        artist_dict[artist] = new_number
        df.at[index, 'artist'] = new_number
    else:
        df.at[index, 'artist'] = artist_dict[artist]

    album = row[2]
    if album not in album_dict:
        new_number = album_count + 1
        album_count = album_count + 1;
        album_dict[album] = new_number
        df.at[index, 'album'] = new_number
    else:
        df.at[index, 'album'] = album_dict[album]    

    playlist = row[3]
    if playlist not in playlist_dict:
        new_number = playlist_count + 1
        playlist_count = playlist_count + 1;
        playlist_dict[playlist] = new_number
        df.at[index, 'playlist'] = new_number
    else:
        df.at[index, 'playlist'] = playlist_dict[playlist]

kmeans = KMeans(n_clusters=30)

kmeans.fit(df)

cluster_labels = kmeans.labels_

cluster_centers = kmeans.cluster_centers_

df['cluster'] = cluster_labels

# print("Cluster Labels:", cluster_labels)
# print("Cluster Centers:", cluster_centers)
# print(df)


input_songs = [1, 2003, 54, 204, 1912, 21]
input_clusters = kmeans.predict(df[df['track'].isin(input_songs)][['track', 'artist', 'album', 'playlist']])
recommendations = df[df['cluster'].isin(input_clusters)]
recommendations = recommendations[~recommendations['track'].isin(input_songs)]
recommendations = recommendations[:len(input_songs)]

track_dict = {v: k for k, v in track_dict.items()}
artist_dict = {v: k for k, v in artist_dict.items()}
album_dict = {v: k for k, v in album_dict.items()}
playlist_dict = {v: k for k, v in playlist_dict.items()}

recommendations['track'] = recommendations['track'].map(track_dict)
recommendations['artist'] = recommendations['artist'].map(artist_dict)
recommendations['album'] = recommendations['album'].map(album_dict)
recommendations['playlist'] = recommendations['playlist'].map(playlist_dict)

print(recommendations)
