import streamlit as st
import pandas as pd
import pickle
import requests

# Load the movie similarity matrix from the pickle file
try:
    with open('movie_similarity.pkl', 'rb') as f:
        movie_similarity_df = pickle.load(f)
except FileNotFoundError:
    st.error("Movie similarity pickle file not found.")
    st.stop()

# Load the movie titles dataset
#try:
    # Load the movie titles dataset
#movie_titles = pd.read_csv(r"C:\Users\shadopc\Desktop\Projects\Movie reccommendation\Movie_Id_Titles.csv")
#movie_titles_url = "https://raw.githubusercontent.com/your-username/your-repo/main/Movie_Id_Titles.csv"
#response = requests.get(movie_titles_url)
#movie_data = response.json()
#movie_titles = pd.DataFrame(movie_data)
movie_dataset_url = "https://raw.githubusercontent.com/your-username/your-repo/main/Movie_Id_Titles.csv"
response = requests.get(movie_dataset_url)
with open('movie_dataset.csv', 'wb') as f:
    f.write(response.content)
movie_titles = pd.read_csv('movie_dataset.csv')
#except FileNotFoundError:
    #st.error("Movie titles CSV file not found.")
    #st.stop()

# Map movie IDs to titles and vice versa
try:
    movie_id_to_title = dict(zip(movie_titles['item_id'], movie_titles['title']))
    movie_title_to_id = dict(zip(movie_titles['title'], movie_titles['item_id']))
except KeyError as e:
    st.error(f"Error mapping movie IDs to titles: {str(e)}")
    st.stop()

# Streamlit app title
st.title('Movie Recommendation App')

# Select movie
selected_movie = st.selectbox('Choose a movie', movie_title_to_id.keys())

# Number of recommendations
num_recommendations = st.slider('Number of recommendations', 1, 10, 5)

# Function to generate movie recommendations
def get_movie_recommendations(selected_movie_title, num_recommendations=5):
    try:
        selected_movie_id = movie_title_to_id[selected_movie_title]
        similarity_scores = movie_similarity_df.loc[selected_movie_id]
        similar_movies = similarity_scores.sort_values(ascending=False)[1:num_recommendations+1]
        recommended_movies = similar_movies.index.map(movie_id_to_title)
        return recommended_movies
    except KeyError:
        st.error(f"Movie '{selected_movie_title}' not found in the similarity matrix.")
        return None
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return None

# Display recommendations when the button is clicked
if st.button('Recommend'):
    if not selected_movie:
        st.error("Please select a movie.")
    else:
        recommended_movies = get_movie_recommendations(selected_movie, num_recommendations)
        if recommended_movies is not None:
            st.write(f"Recommendations for '{selected_movie}':")
            for movie in recommended_movies:
                st.write(movie)

if __name__ == "__app__":
    app.run()
