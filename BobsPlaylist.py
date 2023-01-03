import re
import time
import os

from spotipy import Spotify

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(options=chrome_options)

bob_page_url = "https://1029bobfm.com"

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
CALLBACK_URI = os.getenv("SPOTIPY_CALLBACK_URI")
PLAYLIST_URL = os.getenv("SPOTIPY_PLAYLIST_URL")

# Sleep interval IN SECONDS between requests to the website
sleep_interval = 120

creds = SpotifyOAuth(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     redirect_uri=CALLBACK_URI,
                     scope="playlist-modify-public",
                     open_browser=False)
spotify = Spotify(auth_manager=creds)

# Initialize .songs.tmp file for song history
with open(".songs.tmp", "w") as f:
    f.write("Processed URIs:\n")


def check_song_exists(new_uri: str) -> bool:
    """
    Checks if a song has already been added to this playlist by this script.
    """
    with open(".songs.tmp", "r") as songs_f:
        for uri in songs_f:
            if (uri == new_uri):
                return True
    return False


def get_song_info(driver: webdriver, page_url: str) -> (str, str):
    """
    Loads 1029bobfm.com and gets the artist and title of the most recently played song.
    """
    driver.get(page_url)
    song_info = driver.find_element(By.CLASS_NAME, "song").find_element(By.CLASS_NAME, "info")
    artist = song_info.find_element(By.CLASS_NAME, "artist").text
    title = song_info.find_element(By.CLASS_NAME, "title").text

    artist = re.sub(r"[^a-zA-Z0-9 ]", "", artist)
    title = re.sub(r"[^a-zA-Z0-9 ]", "", title)

    return (title, artist)


def spotify_search(api: Spotify, query_text: str) -> str:
    """
    Searches spotify for information about a song.
    """
    search_result = api.search(query_text, limit=1)["tracks"]

    if (int(search_result["total"]) == 0):
        return None

    return search_result["items"][0]["uri"]


def add_to_playlist(api: Spotify, playlist_url: str, song_uri: str) -> None:
    """
    Adds a song to a playlist, playlist MUST be public
    """
    with open(".songs.tmp", "a") as songs_f:
        songs_f.write(f"{song_uri}\n")

    api.playlist_add_items(playlist_url, [song_uri])


while True:
    title, artist = get_song_info(driver, bob_page_url)

    query_text = "{} artist:{}".format(title, artist)

    print("Searching for {}".format(query_text))

    search_result = spotify.search(query_text, limit=1)

    uri = spotify_search(spotify, query_text)

    if (uri is None):
        print("Couldn't find song match, continuing")
        continue

    if (not check_song_exists(uri)):
        print("Adding song to playlist")
        add_to_playlist(spotify, PLAYLIST_URL, uri)
    else:
        print("Song already in playlist, skipping")


    time.sleep(sleep_interval)
