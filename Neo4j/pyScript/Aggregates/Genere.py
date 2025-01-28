import pandas as pd
import re
import Neo4j.pyScript.Manager.API_Manager as Manager

# Create the pandas dataframe
genre_data ={ 'name' : [] }

def generate_genre_file(books_df):
    books_df['genres'] = books_df['genres']
    
    for genres in books_df['genres']:
        for genre in genres:
            genre_data['name'].append(genre)
    
    df = pd.DataFrame(genre_data)
    Manager.create_file(df, ["genres.csv", "genres.json"])
