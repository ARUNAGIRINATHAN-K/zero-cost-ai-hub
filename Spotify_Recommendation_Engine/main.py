import requests
import base64
import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

# ====================== CONFIGURATION ======================
# Replace with your own Spotify credentials
CLIENT_ID = 'your_client_id_here'
CLIENT_SECRET = 'your_client_secret_here'

# Playlist ID (example: Today's Top Hits)
PLAYLIST_ID = ''

# Number of recommendations
NUM_RECOMMENDATIONS = 5
# ===========================================================

def get_access_token():
    """Obtain Spotify access token using Client Credentials Flow."""
    client_credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    client_credentials_base64 = base64.b64encode(client_credentials.encode()).decode()
    
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': f'Basic {client_credentials_base64}'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    
    response = requests.post(token_url, data=data, headers=headers)
    
    if response.status_code == 200:
        access_token = response.json()['access_token']
        print("✅ Access token obtained successfully.")
        return access_token
    else:
        print(f"❌ Error obtaining access token: {response.status_code}")
        print(response.text)
        exit(1)

def get_trending_playlist_data(playlist_id, access_token):
    """Fetch track data from a Spotify playlist including audio features."""
    sp = spotipy.Spotify(auth=access_token)
    
    # Get playlist tracks
    playlist_tracks = sp.playlist_tracks(
        playlist_id, 
        fields='items(track(id, name, artists, album(id, name)))'
    )
    
    music_data = []
    for track_info in playlist_tracks['items']:
        track = track_info['track']
        if not track:
            continue
            
        track_name = track['name']
        artists = ', '.join([artist['name'] for artist in track['artists']])
        album_name = track['album']['name']
        album_id = track['album']['id']
        track_id = track['id']
        
        # Audio features
        audio_features = sp.audio_features(track_id)[0] if track_id else None
        
        # Release date
        try:
            album_info = sp.album(album_id) if album_id else None
            release_date = album_info['release_date'] if album_info else None
        except:
            release_date = None
        
        # Popularity
        try:
            track_info_full = sp.track(track_id) if track_id else None
            popularity = track_info_full['popularity'] if track_info_full else None
            explicit = track_info_full.get('explicit') if track_info_full else None
            external_url = track_info_full.get('external_urls', {}).get('spotify') if track_info_full else None
        except:
            popularity = None
            explicit = None
            external_url = None
        
        track_data = {
            'Track Name': track_name,
            'Artists': artists,
            'Album Name': album_name,
            'Album ID': album_id,
            'Track ID': track_id,
            'Popularity': popularity,
            'Release Date': release_date,
            'Duration (ms)': audio_features['duration_ms'] if audio_features else None,
            'Explicit': explicit,
            'External URLs': external_url,
            'Danceability': audio_features['danceability'] if audio_features else None,
            'Energy': audio_features['energy'] if audio_features else None,
            'Key': audio_features['key'] if audio_features else None,
            'Loudness': audio_features['loudness'] if audio_features else None,
            'Mode': audio_features['mode'] if audio_features else None,
            'Speechiness': audio_features['speechiness'] if audio_features else None,
            'Acousticness': audio_features['acousticness'] if audio_features else None,
            'Instrumentalness': audio_features['instrumentalness'] if audio_features else None,
            'Liveness': audio_features['liveness'] if audio_features else None,
            'Valence': audio_features['valence'] if audio_features else None,
            'Tempo': audio_features['tempo'] if audio_features else None,
        }
        
        music_data.append(track_data)
    
    df = pd.DataFrame(music_data)
    return df

def calculate_weighted_popularity(release_date):
    """Calculate weighted popularity based on release date (newer = higher weight)."""
    if not release_date:
        return 0.0
    try:
        release_date = datetime.strptime(release_date, '%Y-%m-%d')
        time_span = datetime.now() - release_date
        weight = 1 / (time_span.days + 1)
        return weight
    except:
        return 0.0

def content_based_recommendations(input_song_name, music_df, music_features_scaled, num_recommendations=5):
    """Recommend songs based on audio feature similarity (cosine similarity)."""
    if input_song_name not in music_df['Track Name'].values:
        print(f"❌ '{input_song_name}' not found in the dataset.")
        return None
    
    input_song_index = music_df[music_df['Track Name'] == input_song_name].index[0]
    
    # Cosine similarity
    similarity_scores = cosine_similarity([music_features_scaled[input_song_index]], music_features_scaled)
    similar_song_indices = similarity_scores.argsort()[0][::-1][1:num_recommendations + 1]
    
    recommendations = music_df.iloc[similar_song_indices][[
        'Track Name', 'Artists', 'Album Name', 'Release Date', 'Popularity'
    ]].copy()
    
    return recommendations

def hybrid_recommendations(input_song_name, music_df, music_features_scaled, num_recommendations=5):
    """Hybrid recommendation: content-based + weighted popularity."""
    if input_song_name not in music_df['Track Name'].values:
        print(f"❌ '{input_song_name}' not found in the dataset.")
        return None
    
    # Get content-based recommendations
    content_based_rec = content_based_recommendations(
        input_song_name, music_df, music_features_scaled, num_recommendations
    )
    
    if content_based_rec is None:
        return None
    
    # Calculate weighted popularity for input song
    input_data = music_df[music_df['Track Name'] == input_song_name].iloc[0]
    popularity_score = input_data['Popularity']
    weighted_popularity_score = popularity_score * calculate_weighted_popularity(input_data['Release Date'])
    
    # Create entry for input song with weighted score
    new_entry = pd.DataFrame({
        'Track Name': [input_song_name],
        'Artists': [input_data['Artists']],
        'Album Name': [input_data['Album Name']],
        'Release Date': [input_data['Release Date']],
        'Popularity': [weighted_popularity_score]
    })
    
    # Combine and sort
    hybrid_rec = pd.concat([content_based_rec, new_entry], ignore_index=True)
    hybrid_rec = hybrid_rec.sort_values(by='Popularity', ascending=False)
    hybrid_rec = hybrid_rec[hybrid_rec['Track Name'] != input_song_name]
    
    return hybrid_rec

# ====================== MAIN EXECUTION ======================
if __name__ == "__main__":
    print("🚀 Starting Music Recommendation System...")
    
    # Step 1: Get Access Token
    access_token = get_access_token()
    
    # Step 2: Fetch Music Data
    print(f"📥 Fetching data from playlist: {PLAYLIST_ID}")
    music_df = get_trending_playlist_data(PLAYLIST_ID, access_token)
    
    print(f"✅ Fetched {len(music_df)} tracks.")
    print("\nNull values check:")
    print(music_df.isnull().sum())
    
    # Step 3: Prepare features for content-based filtering
    feature_columns = ['Danceability', 'Energy', 'Key', 'Loudness', 'Mode', 
                      'Speechiness', 'Acousticness', 'Instrumentalness', 
                      'Liveness', 'Valence', 'Tempo']
    
    music_features = music_df[feature_columns].fillna(0).values  # Handle any missing values
    scaler = MinMaxScaler()
    music_features_scaled = scaler.fit_transform(music_features)
    
    # Step 4: Get Recommendations
    input_song_name = "I'm Good (Blue)"  # Change this to any song in the playlist
    
    print(f"\n🎵 Generating hybrid recommendations for: '{input_song_name}'")
    recommendations = hybrid_recommendations(
        input_song_name, music_df, music_features_scaled, NUM_RECOMMENDATIONS
    )
    
    if recommendations is not None:
        print("\n✅ Hybrid Recommendations:")
        print(recommendations)
    
    # Optional: Save data to CSV
    music_df.to_csv('spotify_music_data.csv', index=False)
    print("\n💾 Data saved to 'spotify_music_data.csv'")