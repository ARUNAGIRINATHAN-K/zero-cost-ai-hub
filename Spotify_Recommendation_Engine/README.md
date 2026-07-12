# Spotify Recommendation Engine

**Status:** 🚀 Completed  
**Tech Stack:** Python, Spotipy API, Pandas, Scikit-learn (Cosine Similarity)

## Overview
This project is a Content-Based Music Recommendation System. It connects directly to the Spotify Web API to dynamically fetch tracks from trending playlists, extracts the deep audio features of those tracks (like danceability, energy, acousticness, and tempo), and uses Machine Learning techniques to recommend similar songs based on a user's input track.

Unlike standard collaborative filtering (which relies on user history), this system recommends music purely based on the *mathematical audio profile* of the song.

## Setup & Installation

```Bash
cd Spotify_Music_Recommender_Engine
Install the required dependencies:
```
```Bash
pip install -r requirements.txt
Get Spotify Credentials:
```

Go to the Spotify Developer Dashboard.

Create an App and copy your Client ID and Client Secret.

Create a .env file in this directory and add them:

```
SPOTIPY_CLIENT_ID='your_client_id_here'
SPOTIPY_CLIENT_SECRET='your_client_secret_here'
```

## Usage
Run the script:

```Bash
python main.py
```

## Architecture & Flow
1. **API Authentication:** Uses OAuth 2.0 Client Credentials flow to generate a secure access token via Spotify's developer portal.
2. **Data Scraping (Spotipy):** Iterates through a given Spotify Playlist ID and extracts metadata (Artist, Album, Popularity) alongside 11 key audio features (Energy, Valence, Liveness, etc.) for every track.
3. **Data Normalization:** Converts release dates to a "weighted popularity score" to slightly prioritize newer releases, then scales all numerical audio features using `MinMaxScaler` so features like *Tempo* (e.g., 120 BPM) don't overpower features like *Danceability* (e.g., 0.8).
4. **Recommendation Engine:** Uses **Cosine Similarity** to plot the input song as a vector in multi-dimensional space, compares it against the matrix of all other songs in the dataset, and returns the top 5 tracks with the closest mathematical proximity.

