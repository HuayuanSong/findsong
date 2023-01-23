import streamlit as st

# Configure Streamlit page
st.set_page_config(
    page_title="Find the Song that You Like🎸", page_icon="🎸", layout="wide"
)

import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
from sklearn.neighbors import NearestNeighbors


@st.cache(allow_output_mutation=True)
def data_import():
    """Function for loading in cleaned data csv file."""
    df = pd.read_csv("data/clean_data.csv")
    df["genres"] = df.genres.apply(
        lambda x: [i[1:-1] for i in str(x)[1:-1].split(", ")]
    )
    df_explode = df.explode("genres")
    return df_explode


genre_names = [
    "Dance Pop",
    "Electronic",
    "Electropop",
    "Hip Hop",
    "Jazz",
    "K-pop",
    "Latin",
    "Pop",
    "Pop Rap",
    "R&B",
    "Rock",
]
audio_params = [
    "acousticness",
    "danceability",
    "energy",
    "instrumentalness",
    "valence",
    "tempo",
]

df_explode = data_import()


def match_song(genre, yr_start, yr_end, test_feat):
    """Function for finding similar songs with KNN algorithm."""
    genre = genre.lower()
    genre_data = df_explode[
        (df_explode["genres"] == genre)
        & (df_explode["release_year"] >= yr_start)
        & (df_explode["release_year"] <= yr_end)
    ]
    genre_data = genre_data.sort_values(by="popularity", ascending=False)[:500]

    # Load KNN from SkLearn
    neigh = NearestNeighbors()
    neigh.fit(genre_data[audio_params].to_numpy())

    n_neighbors = neigh.kneighbors(
        [test_feat], n_neighbors=len(genre_data), return_distance=False
    )[0]

    uris = genre_data.iloc[n_neighbors]["uri"].tolist()
    audios = genre_data.iloc[n_neighbors][audio_params].to_numpy()

    return uris, audios


# Setup page order
def page():
    title = "Find Your Song🎸"
    st.title(title)

    st.write(
        "Get recommended songs on Spotify based on genre and key audio parameters."
    )
    st.markdown("##")

    # Streamlit column layout
    with st.container():
        col1, col2, col3, col4 = st.columns((2, 0.5, 0.5, 0.5))

        with col3:
            st.markdown("***Select genre:***")
            genre = st.radio("", genre_names, index=genre_names.index("Rock"))

        with col1:
            st.markdown("***Select audio parameters to customize:***")
            yr_start, yr_end = st.slider(
                "Select the year range", 1908, 2022, (1980, 2022)
            )
            acousticness = st.slider("Acousticness", 0.0, 1.0, 0.5)
            danceability = st.slider("Danceability", 0.0, 1.0, 0.5)
            energy = st.slider("Energy", 0.0, 1.0, 0.5)
            instrumentalness = st.slider("Instrumentalness", 0.0, 1.0, 0.5)
            valence = st.slider("Valence", 0.0, 1.0, 0.45)
            tempo = st.slider("Tempo", 0.0, 244.0, 125.01)

    pr_page_tracks = 6
    test_feat = [acousticness, danceability, energy, instrumentalness, valence, tempo]
    uris, audios = match_song(genre, yr_start, yr_end, test_feat)

    tracks = []
    for uri in uris:
        track = """<iframe src="https://open.spotify.com/embed/track/{}" width="280" height="400" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(
            uri
        )
        tracks.append(track)

    if "previous_inputs" not in st.session_state:
        st.session_state["previous_inputs"] = [genre, yr_start, yr_end] + test_feat

    current_inputs = [genre, yr_start, yr_end] + test_feat
    if current_inputs != st.session_state["previous_inputs"]:
        if "start_track_i" in st.session_state:
            st.session_state["start_track_i"] = 0

        st.session_state["previous_inputs"] = current_inputs

    if "start_track_i" not in st.session_state:
        st.session_state["start_track_i"] = 0

    with st.container():
        col1, col2, col3 = st.columns([2, 1, 2])
        if st.button("More Songs"):
            if st.session_state["start_track_i"] < len(tracks):
                st.session_state["start_track_i"] += pr_page_tracks

        current_tracks = tracks[
            st.session_state["start_track_i"] : st.session_state["start_track_i"]
            + pr_page_tracks
        ]
        current_audios = audios[
            st.session_state["start_track_i"] : st.session_state["start_track_i"]
            + pr_page_tracks
        ]
        if st.session_state["start_track_i"] < len(tracks):
            for i, (track, audio) in enumerate(zip(current_tracks, current_audios)):
                if i % 2 == 0:
                    with col1:
                        components.html(
                            track,
                            height=400,
                        )
                        with st.expander("Display Chart"):
                            df = pd.DataFrame(dict(r=audio[:5], theta=audio_params[:5]))
                            fig = px.line_polar(
                                df, r="r", theta="theta", line_close=True
                            )
                            fig.update_layout(height=400, width=340)
                            st.plotly_chart(fig)

                else:
                    with col3:
                        components.html(
                            track,
                            height=400,
                        )
                        with st.expander("Display Chart"):
                            df = pd.DataFrame(dict(r=audio[:5], theta=audio_params[:5]))
                            fig = px.line_polar(
                                df, r="r", theta="theta", line_close=True
                            )
                            fig.update_layout(height=400, width=340)
                            st.plotly_chart(fig)
        else:
            st.write("No more songs")


page()
