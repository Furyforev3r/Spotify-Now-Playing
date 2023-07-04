import os
import time
from dotenv import load_dotenv, find_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

load_dotenv(find_dotenv())

client_id = os.environ.get("client_id")
client_secret = os.environ.get("client_secret")
redirect_uri = "https://github.com/furyforev3r"

scope = "user-read-currently-playing"


class SpotifyMusicChecker:
    def __init__(self):
        self.last_music = ""
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri
        ))

    def verify_music(self):
        try:
            current_track = self.sp.current_user_playing_track()

            if current_track is not None:
                track_name = current_track['item']['name']
                artist_name = current_track['item']['artists'][0]['name']
                current_music = f"{track_name} - {artist_name}"
                if current_music != self.last_music:
                    self.last_music = current_music
                    return f"You are listening: {current_music}"
            else:
                return "No music currently playing."

        except spotipy.SpotifyException as e:
            return f"An error occurred: {str(e)}"

    def run(self):
        while True:
            verify_results = self.verify_music()

            if verify_results is not None:
                print(verify_results)
            sleep(1)


if __name__ == "__main__":
    spotify_checker = SpotifyMusicChecker()
    spotify_checker.run()
