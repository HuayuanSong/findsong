import spotipy
import streamlit as st
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials
from PIL import Image
import requests
import pandas as pd

st.set_page_config(
    page_title="Find Songs Similar to Yours🎤", page_icon="🎤", layout="wide"
)

# Spotify API
SPOTIPY_CLIENT_ID = st.secrets.spot_creds.spot_client_id
SPOTIPY_CLIENT_SECRET = st.secrets.spot_creds.spot_client_secret

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET
    )
)

"""
# Analyze Song and Get Recommendations🎤

Input a song title and the app will return recommendations as well as the features of the song.

Data is obtained using the Python library [Spotipy](https://spotipy.readthedocs.io/en/2.18.0/) that uses [Spotify Web API.](https://developer.spotify.com/documentation/web-api/)

"""
song = st.text_input("Enter a song title", value="Somebody Else")
search = sp.search(q="track:" + song, type="track")


class GetSongInfo:
    def __init__(self, search):
        self.search = search

    def song_id(self):
        song_id = search["tracks"]["items"][0]["id"]  # -gets song id
        return song_id

    def song_album(self):
        song_album = search["tracks"]["items"][0]["album"][
            "name"
        ]  # -gets song album name
        return song_album

    def song_image(self):
        song_image = search["tracks"]["items"][0]["album"]["images"][0][
            "url"
        ]  # -gets song image URL
        return song_image

    def song_artist_name(self):
        song_artist_name = search["tracks"]["items"][0]["artists"][0][
            "name"
        ]  # -gets artist for song
        return song_artist_name

    def song_name(self):
        song_name = search["tracks"]["items"][0]["name"]  # -gets song name
        return song_name

    def song_preview(self):
        song_preview = search["tracks"]["items"][0]["preview_url"]
        return song_preview


songs = GetSongInfo(song)

###


def url(song):
    url_to_song = "https://open.spotify.com/track/" + songs.song_id()
    st.write(
        f"Link to stream '{songs.song_name()}' by {songs.song_artist_name()} on Spotify: {url_to_song}"
    )


# Set up two-column layout for Streamlit app
image, stats = st.columns(2)

with image:
    try:
        url(song)
        r = requests.get(songs.song_image())
        open("img/" + songs.song_id() + ".jpg", "w+b").write(r.content)
        image_album = Image.open("img/" + songs.song_id() + ".jpg")
        st.image(
            image_album,
            caption=f"{songs.song_artist_name()} - {songs.song_album()}",
            use_column_width="auto",
        )

        feat = sp.audio_features(tracks=[songs.song_id()])
        features = feat[0]
        p = pd.Series(features).to_frame()
        data_feat = p.loc[
            [
                "acousticness",
                "danceability",
                "energy",
                "liveness",
                "speechiness",
                "valence",
            ]
        ]
        bpm = p.loc[["tempo"]]
        values = bpm.values[0]
        bpms = values.item()
        ticks = np.linspace(0, 1, 11)

        plot = data_feat.plot.barh(
            xticks=ticks, legend=False, color="limegreen"
        )  # Use Pandas plot
        plot.set_xlabel("Value")
        plot.set_ylabel("Parameters")
        plot.set_title(f"Analysing '{songs.song_name()}' by {songs.song_artist_name()}")
        plot.invert_yaxis()
        st.pyplot(plot.figure)
        st.subheader(f"BPM (Beats Per Minute): {bpms}")

        st.warning(
            "Note: Audio previews may have very high default volume and will reset after page refresh"
        )
        st.audio(songs.song_preview(), format="audio/wav")

    except IndexError or NameError:
        st.error(
            "This error is possibly due to the API being unable to find the song. Maybe try to retype it using the song title followed by artist without any hyphens (e.g. In my Blood Shawn Mendes)"
        )

# Recommendations
with stats:
    st.subheader("You might also like")

    reco = sp.recommendations(
        seed_artists=None, seed_tracks=[songs.song_id()], seed_genres=[], limit=10
    )

    for i in reco["tracks"]:
        st.write(f"\"{i['name']}\" - {i['artists'][0]['name']}")
        image_reco = requests.get(i["album"]["images"][2]["url"])
        open("img/" + i["id"] + ".jpg", "w+b").write(image_reco.content)
        st.image(Image.open("img/" + i["id"] + ".jpg"))
