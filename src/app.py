import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

import os


# Define the URL
url = "https://www.siriusxm.com/api/mountain/thebridge"

def handler(event, context):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Access the 'channels.thebridge.content' object
            content = data.get("channels", {}).get("thebridge", {}).get("content")
            artist = content.get("artists", [""])[0].get("name")
            title = content.get("title")

            # Print the content
            print(artist)
            print(title)
        else:
            print(f"Request failed with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")


    # Replace these with your own credentials
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = os.getenv("CLIENT_SECRET")  # Set this to a valid redirect URI in your Spotify Developer Application

    # Initialize the Spotipy client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope="playlist-modify-private"))

    # Search for tracks based on the artist and song title
    query = f"artist:{artist} track:{title}"
    query = query.replace("'", "")
    results = sp.search(q=query, type="track")

    # Check if the "tracks" array is not empty
    if results["tracks"]["items"]:
        first_track = results["tracks"]["items"][0]
        print(f"Track Name: {first_track['name']}")
        print(f"Artist(s): {', '.join([artist['name'] for artist in first_track['artists']])}")
        track_uri = first_track['uri']
        print(f"Spotify URI: {track_uri}")
        
        # The Bridge playlist
        playlist_uri = os.getenv("PLAYLIST")


        # Check if the track is already in the playlist
        playlist = sp.playlist_tracks(playlist_uri)
        track_uris_in_playlist = [track["track"]["uri"] for track in playlist["items"]]

        if track_uri not in track_uris_in_playlist:
            # Add the track to the playlist
            sp.playlist_add_items(playlist_uri, [track_uri])
            print(f"Added track {track_uri} to playlist {playlist_uri}")
        else:
            print(f"The track {track_uri} is already in the playlist.")

    else:
        print("No matching tracks found.")


if __name__ == '__main__':
    handler({}, {})