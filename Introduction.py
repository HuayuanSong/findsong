import streamlit as st
from streamlit import session_state as session

# Configure Streamlit page
st.set_page_config(page_title="Song Recommender🎶", page_icon="🎶")

st.title("Song Recommender🎶")
st.markdown("Click on '**Recommender**' from the side panel to get started.")
st.markdown("**How does it work?**")
st.markdown(
    "The songs come from the [Spotify and Genius Track Dataset](https://www.kaggle.com/datasets/saurabhshahane/spotgen-music-dataset) on Kaggle. The [k-Nearest Neighbor algorithm](https://scikit-learn.org/stable/modules/neighbors.html) is used to obtain recommendations, i.e., the top songs which are closest in distance to the set of parameter inputs specified by you."
)

st.markdown("This app will recommend you songs based on the characteristics below.")
st.markdown(
    """  
            **Acousticness**: A metric describing the 'acousticness' of a song. 1.0 represents high confidence the song is acoustic.<br>
            
            **Danceability**: Describes a song's suitability for dancing based on combination of elements including tempo, rhythm stability, beat strength, and overall regularity. 
                        0.0 is least danceable and 1.0 is most danceable.<br>

            **Energy**: Measure of intensity and activity. Often, energetic songs feel fast, loud, and noisy.<br>

            **Liveness**: A metric describing the likelihood that a track is a recording of a live performance.<br>

            **Speechiness**: How much lyrics the track contains.<br>

            **Valence**: A metric ranging from 0.0 to 1.0 describing the positivity conveyed by a track.<br>
            
            Source: [Spotify Web API](https://developer.spotify.com/documentation/web-api/reference)
            """,
    unsafe_allow_html=True,
)
