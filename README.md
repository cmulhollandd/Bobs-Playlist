# Bob's Playlist
## A Simple Python script to add songs played by 102.9 Bob FM in Southwest Florida to a Spotify Playlist

### Setup
1. All dependencies can be installed by running ```pip install requirements.txt```
	* Or, alternatively, these can be installed manually through a different package manager
2. If this is the first time using selenium, you will need to also install chromedriver for Google Chrome.
    * This script uses the chrome driver because it can be run in a headless mode for use over ssh..
	* More instructions on this set are available [here](https://selenium-python.readthedocs.io/installation.html#drivers)
	* Whichever driver you download, needs to be placed in your environment's `PATH` (either `/usr/bin/` or `/usr/local/bin/` on UNIX systems)
3. Environment Variables
	* This script makes use of different environment variables for spotify access keys and playlist urls, namely:
		* `SPOTIPY_CLIENT_ID`: client id key provided by spotify
		* `SPOTIPY_CLIENT_SECRET`: client secret key provided by spotify
		* `SPOTIPY_CALLBACK_URI`: callback url for spotify, this requires additional setup, see below
		* `SPOTIPY_PLAYLIST_URL`: url for the spotify playlist for songs to be placed into, this needs to be a playlist created by the user signed into the API
	* All of these can be set using the syntax: `export VARIABLE_NAME="variable value"`
4. Spotify API Setup
	* This program requires a spotify API account and a registered application.
	* You can sign up for the api and make a new application [here](https://developer.spotify.com/dashboard/applications)
	* Once you make a new application, export the application's client id and client secret to your environment
	* Finally, set a callback URI for authentication.
		* Two good ones to use are `http://localhost:8080` or `http://example.com/callback`.
		* Whichever you choose will also need to be exported to the environment
		* __NOTE:__ `http://localhost:8080` will not work if you are running this on a remote machine (i.e. a remote server) through ssh, use `http://example.com/callback` instead.


### Usage:
* Basic usage is extremely simple: `python BobsPlaylist.py`
* You can also use `tmux` to continue this program and close the ssh session if running on a remote machine


### Known Issues:
* Authentication is finicky
	* if you are getting the error `400 Client Error: Bad Request for url: https://accounts.spotify.com/api/token` try deleteing `.cache` in this directory.
* This script keeps track of the songs it adds to the playlist and will not add duplicates __however__ it does not check through spotify if a song is already present so duplicates may be added that way. 
	* Along the same lines: it may add duplicates of a song if they are different versions (remastered, live, radio edit, etc).
