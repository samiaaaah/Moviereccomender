import pickle
import pandas as pd
import streamlit as st
import requests

def set_background_image(image_url):
    # Apply custom CSS to set the background image
    page_bg_img = '''
    <style>
    .stApp {
        background-position: top;
        background-image: url(%s);
        background-size: cover;
    }

    @media (max-width: 768px) {
        /* Adjust background size for mobile devices */
        .stApp {
            background-position: top;
            background-size: contain;
            background-repeat: no-repeat;
        }
    }
    </style>
    ''' % image_url
    st.markdown(page_bg_img, unsafe_allow_html=True)


def main():
    # Set the background image URL
    background_image_url = "https://img.freepik.com/free-photo/top-view-arrangement-cinema-elements-yellow-background-with-copy-space_23-2148416777.jpg?w=1480&t=st=1705922795~exp=1705923395~hmac=1ce3a44cf4c363d282193c96479f517ed864303f85b0349a5a9135af480bd909"

    # Set the background image
    set_background_image(background_image_url)

    custom_css = """
       <style>
       body {
           background-color: #4699d4;
           color: #ffffff;
           font-family: Arial, sans-serif;
       }
       h1 {
           color: #ffffff !important; /* Set title color to white */
       }
       select {
           background-color: #000000 !important; /* Black background for select box */
           color: #ffffff !important; /* White text within select box */
       }
       label {
           color: #ffffff !important; /* White color for select box label */
       }
       </style>
       """
    st.markdown(custom_css, unsafe_allow_html=True)


if __name__ == "__main__":

    main()

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    try:
        data = requests.get(url)
        data.raise_for_status()  # Raise an HTTPError for bad responses
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return None

# Load pickled files
movie_list = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Convert movie_list to DataFrame if needed
movies = pd.DataFrame(movie_list)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

st.title("Samiya's Movie Recommender")

selected_movie_name = st.selectbox('List of movies', movie_list['title'].values)

if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
