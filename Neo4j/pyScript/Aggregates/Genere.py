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

def generate_genre_book_file(books_df):
    genre_book_data = {
        "bookId": None,
        "genreId": None
    }
    df = pd.DataFrame(genre_book_data, index=[0])
    df.drop(0, inplace=True)
    for index, book in books_df.iterrows():
        genre_list = []
        for genres in book['genres']:
            genre_list.append(genres)
        for genre in genre_list:
            df.loc[len(df)] = [book['bookId'], genre]
    Manager.create_file(df, ["genre_book.csv", "genre_book.json"])