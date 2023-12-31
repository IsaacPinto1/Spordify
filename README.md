# Spordify

## Description
Spordify is a python script that allows users to sort their playlists based on several different criteria, including song title, artist name, album name, duration, BPM, musical key, as well as a randomized option. This project leverages the Spotipy API to manage the user's playlists, as well as Selenium and Beautiful Soup to pull data from songbpm.com for the key and BPM.

## Installation

### Prerequisites
* [Register for a Spotify app](https://developer.spotify.com/dashboard)

### Setup
Once registered for a Spotify App, add a Redirect URI to the Application settings (which can just be http://example.com). Before running the script, store the SPOTIPY_REDIRECT_URI, SPOTIFY_CLIENT_ID, and SPOTIFY_CLIENT_SECRET in environment variables by writing the following in your code environment:
```
export SPOTIPY_CLIENT_ID=<CLIENT_ID>
export SPOTIPY_CLIENT_SECRET=<CLIENT_SECRET>
export SPOTIPY_REDIRECT_URI="<REDIRECT_URI>"
```

## Usage
Run the script and follow the instructions to sign into Spotify before entering your Spotify playlist link. You will then be able to choose which option to sort your playlist by.

## Disclaimer
Spordify sorts playlists by removing songs and adding them back in sorted order. Therefore, it is recommended to use this application on **copies** of your playlists to protect the 'date added' data and ensure you don't lose any songs if you accidentally quit the script or it crashes while it is running.
